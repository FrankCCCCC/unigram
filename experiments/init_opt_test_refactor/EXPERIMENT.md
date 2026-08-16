# init_opt_test_refactor — does the refactor reproduce `init_opt_test`?

A reproduction run, not new science. `init_opt_test`'s grid re-executed against the
post-refactor tree, so that every number the refactor might have moved is measured
rather than argued about.

The refactor under test (`dde51e1` "refactor draft", plus the correctness fixes on
top of it) did two things: it pulled the Lightning boilerplate — per-step RNG
seeding, the six-metric logging vocabulary, pooled-sum std accumulation, the
recorder writes — out of `main.py:HyperbolicDLM` into a new
`trainer.py:BaseTrainer`, and it pushed the `word_embedding` accessor down into
the model classes. Neither move is supposed to touch arithmetic.

## Hypothesis

**Every cell reproduces its `init_opt_test` counterpart bit-exactly.**

This project is the sharper of the two reproduction checks, because `mode=opt`
skips `trainer.fit` entirely. `OptimalModel` is deterministic and has no
parameters, so there is no optimizer trajectory and no training noise to absorb a
regression. The only moving parts left are the proposal, the bridge sampler, the
horosphere geometry, the loss, and the metric plumbing — exactly the surfaces the
refactor touched. A mismatch here localizes the fault immediately.

Bit-exactness (rather than "within noise") is the right bar for three reasons:

1. Every RNG stream is explicitly seeded — `L.seed_everything(..., workers=True)`
   for init and shuffling, `_make_step_generator(salt, batch_idx, stage)` for the
   `t` draws.
2. A prior CPU-and-GPU parity run of the refactored tree against pre-refactor
   `HEAD` came back at `0.000e+00` max relative difference on all 8 metrics across
   4 configs, with the run-to-run nondeterminism floor also measuring exactly 0.
3. The 2-cell pilot for this project reproduced bit-exactly on two *different* GPU
   architectures (2080 Ti `sm_75`, A5000 `sm_86`), so architecture drift is not a
   confound either.

Two invariants come along for free and are checked by the same run:

- **The reference pass is invariant.** `test_wnelbo_ref` / `test_nelbo_ref` /
  `test_wce_ref` / `test_ce_ref` are computed on a proposal pinned to `exp(0.1)`
  fed by an independent RNG stream (`salt=1`), so all 14 `(loss_geometry, rate)`
  cells of a given `(ps, seed)` must return identical reference numbers. This
  holds in the reference outputs; if the refactor crossed the loss and reference
  streams, it breaks here.
- **`test_wnelbo_ref >= H(p)`** at the optimum (`H(naive_ps) = 0.5003`,
  `H(cmplx_ps) = 1.6664`, `H(c1e*_exp1.0) = 1.0407` nats).

## Design

Grid from `setup.md`, byte-identical to `init_opt_test` — 5 × 2 × 7 × 3 =
**210 runs**, one SLURM job each:

| variable | values |
|---|---|
| `ps` | `naive_ps`, `cmplx_ps`, `c1e2_exp1.0`, `c1e3_exp1.0`, `c1e4_exp1.0` |
| `loss_geometry` | `cross_entropy`, `poincare_polar` |
| `loss_proposal_exp_rate` | 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0 |
| `seed` | 0, 1, 2 |

Fixed: `mode=opt`, `hyper_dim=2`, `lr=1e-3`, `max_steps=20000` (inert — no
`fit`), `gradient_clip_val=1.0`, `test_size=4e6`, `batch_size=2048`,
`ref_proposal_type=exp`, `ref_proposal_exp_rate=0.1`.

`run_name` is byte-identical to `init_opt_test`'s, so cells pair 1:1 with their
reference by directory name and the comparison needs no mapping table.

## GPU allocation

Both owned partitions, all four nodes — `--partition=thickstun,desa`, 1 GPU per
job, 4 CPUs, 16 GB, 1 h limit.

`desa-compute-01` (8× 2080 Ti, 11 GB) is deliberately **not** excluded. Agent.md
excludes it because 11 GB OOMs at seq 1024; that does not apply to a 3×128 MLP
over a ≤10-word vocab using well under 1 GB, its `sm_75` cards are covered by the
env's torch cu128 cubins, and `init_test/sweep.py` set the same precedent. The
pilot confirmed it: a cell ran there and reproduced bit-exactly.

Short time limits are deliberate — these are minutes-long jobs sharing nodes with
long-running sweeps, and a 1 h limit lets them backfill instead of waiting behind
the queue.

## Wall clock (expected)

No training; each job is a single ~1954-batch test pass, a few minutes. 210 jobs
over the slots free on the two partitions — a few hours wall clock, dominated by
queueing behind the other sweeps on these nodes rather than by compute.

## Reporting

- `python experiments/report.py init_opt_test_refactor` → `RESULTS.md` in the same
  dense-table layout as `init_opt_test`, so the two tables can be read side by side.
- `python experiments/compare_reproduction.py init_opt_test_refactor init_opt_test`
  → the per-cell verdict. Exits non-zero if any paired cell exceeds tolerance, so
  "reproduced" is a checked claim rather than an eyeballed one.
