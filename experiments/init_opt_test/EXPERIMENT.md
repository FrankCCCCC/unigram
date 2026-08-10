# init_opt_test — ELBO of the Bayes-optimal model vs loss type and proposal

Companion to `init_test`. Same grid, same reference pass, but the trained `MLPLM`
is swapped for the closed-form `OptimalModel` (`mode=opt`), so `trainer.fit` is
skipped and only the 4M-sample test pass runs.

## Hypothesis

With the model held *exact*, every remaining cell-to-cell difference is the
importance-weighted **estimator**, not learning. Three claims to test:

1. **The reference pass is invariant.** `test_wnelbo_ref`, `test_nelbo_ref`,
   `test_wce_ref`, `test_ce_ref` are computed on a proposal pinned to `exp(0.1)`
   fed by an independent RNG stream (`salt=1`), and `OptimalModel` is
   deterministic with `word_embedding=None`. So all 14 `(loss_geometry, rate)`
   cells of a given `(ps, seed)` must return the *same* reference numbers. Any
   drift means the loss path is leaking into the reference path.
2. **`test_wnelbo_ref >= H(p)`** for the exact model, sitting just above the
   bound rather than far above it — this is the ELBO's tightness at the optimum,
   and it is the number a trained run is chasing. `H(naive_ps) = 0.5003`,
   `H(cmplx_ps) = 1.6664` nats.
3. **The variance cliff is visible in `test_wloss`.** The per-`t` loss decays like
   `exp(-0.152 t)`, so a proposal `exp(rate)` with `rate > 2*0.152 ≈ 0.304` gives
   the weighted estimator infinite variance. Rates `{0.5, 0.75, 1.0}` should fan
   out across seeds and show a blown-up `test_wloss_std`, while
   `{0.01, 0.05, 0.1, 0.25}` should agree tightly. Because the model is exact,
   this isolates the proposal's contribution with nothing else moving.

## Design

Grid from `setup.md` — 5 × 2 × 7 × 3 = **210 runs**, one SLURM job each:

| variable | values |
|---|---|
| `ps` | `naive_ps`, `cmplx_ps`, `c1e2_exp1.0`, `c1e3_exp1.0`, `c1e4_exp1.0` |
| `loss_geometry` | `cross_entropy` (`ce`), `poincare_polar` (`pp`) |
| `loss_proposal_type` | `exp` |
| `loss_proposal_exp_rate` | 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0 |
| `seed` | 0, 1, 2 |

Fixed: `mode=opt`, `hyper_dim=2`, `lr=0.001`, `max_steps=20000`,
`gradient_clip_val=1.0`, `test_size=4e6`, `batch_size=2048`,
`ref_proposal_type=exp`, `ref_proposal_exp_rate=0.1`.

`lr` and `max_steps` are **inert** under `mode=opt` (no `trainer.fit`); they are
carried anyway so the run names line up 1:1 with the `init_test` cells at
`st=20000` and `experiments/report.py` parses them unchanged.

The three `c1e*_exp1.0` specs are the same geometric distribution `p_i ∝ e^-i`
truncated at V = 100 / 1000 / 10000, so all three have
`H(p) = 1.0406518523` nats and only ~16 tokens ever appear in a 4M draw. They
vary the **vocabulary** — the packing of the boundary angles
`phi_v = (v+0.5)·2π/V` — at constant entropy, which is what isolates
vocabulary-size effects from distribution effects. This makes hypothesis 2 above
sharper: `wnelbo_ref` must be identical across the three, and anything that is
not is a property of the metric rather than of the model.

Run name (only searched variables are semantic; `mode` is fixed for the project
and is carried by the project name):

```
ps-{ps}_lg-{ce|pp}_q-exp{rate}_qref-exp0.1_lr0.001_st20000_s{seed}
```

Orchestration: `sweep.py` submits `script/train/{ce,pp}.sh` with `EXTRA="mode=opt"`.
Idempotent — a cell whose `test_metrics.json` exists, or whose job name is
already in `squeue`, is skipped.

## GPU allocation

`desa` and `thickstun` are deliberately **not** used: the `init_test` sweep
already has its full grid queued there. These jobs go to the cluster-wide
community pool instead.

| | |
|---|---|
| partition | `gpu` (PriorityTier 15 vs 20 for the owned partitions; `PreemptMode=REQUEUE`) |
| constraint | `ampere\|ada\|hopper\|blackwell` |
| excluded nodes | `desa-compute-01,kuleshov-compute-02,kuleshov-compute-03,thickstun-compute-01,yu-compute-01` |
| per job | 1 GPU, 4 CPU, 16 GB, `--time=01:00:00` |

The constraint is load-bearing, not a preference. The community pool still holds
GTX 1080 Ti / Titan X / Titan Xp / V100 nodes, and the `sfm` env's
torch 2.7.0+cu128 ships cubins for sm_75/80/86/90/100/120 only — a probe job
landed on `snavely-compute-09` (GTX TITAN X, sm_52) and torch refused the device.
The cluster tags GPU architecture as a node feature but has no `turing` tag, so
constraining to `ampere|ada|hopper|blackwell` drops the (usable) 2080 Ti nodes
along with the unusable ones; that still leaves 90 of 143 nodes, all sm_80+.

`yu-compute-01` is excluded for an unrelated reason: the desa NFS export is
permission-denied there, so slurmd cannot chdir into the submit dir or create the
`--output` file. Jobs land in `/tmp` and die in <15 s with no log at all
(observed: 9 cells, all on that node, ExitCode `0:53`). Resubmitting with it
excluded filled the gaps.

Preemption costs nothing here: runs are ~1 minute and `TaskMgr`'s `finished.json`
makes a resubmit a no-op.

## Wall clock (actual)

The 1954-batch test pass only, no training:

| ps | V | per run |
|---|---|---|
| `naive_ps`, `cmplx_ps` | 10 | ~1 min |
| `c1e2_exp1.0` … `c1e4_exp1.0` | 100 … 10000 | ~2–5 min |

V=10000 costs surprisingly little: the `(2048, V)` float64 horosphere tensors
stay under 1.7 GB peak RSS and the run finishes in ~2.5 min, so `mem=16G` and
`--time=01:00:00` cover the whole grid. The 84-cell V=10 sweep finished in ~4 min
wall clock end to end; the 126-cell extension took ~12 min, queueing included,
running many-wide on the community pool. For comparison, the equivalent
`init_test` cells (which do train) take ~8–9 min each.

## Reporting

```
python experiments/report.py init_opt_test
```

Read `wloss` as the headline here, not `wnelbo_ref`: under `mode=opt` the
reference columns are constant across the swept axes by construction (that is
hypothesis 1), so they serve as the consistency check while `wloss` carries the
signal.

`report.py` emits both the Full Table (all five metric columns per geometry) and
the Dense Table (`wloss` under each geometry) laid out as in `setup.md`, and it
carries the hand-written "Insights and conclusions" trailer across a
regeneration verbatim — it splits the existing file on that heading.
