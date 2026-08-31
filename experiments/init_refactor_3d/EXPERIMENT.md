# init_refactor_3d — `init_test`'s grid on the general-d bridge, `hyper_dim = 3`

First run of the arbitrary-dimension bridge (`HyperBridge.bridge` /
`Loss.weighted_loss`, the `claude/init-refactor-nd` branch) at a dimension the
binary code path cannot reach. One of three sibling projects — `init_refactor_3d`,
`init_refactor_9d`, `init_refactor_16d` — that differ only in `hyper_dim`.

## Hypothesis

1. **The general-d path is a valid ELBO at d = 3.** `test_wnelbo_ref >= H(p)` in
   every trained cell (`H(naive_ps) = 0.5003`, `H(cmplx_ps) = 1.6664` nats), and the
   best cells land on it from above, as the d = 2 `init_test` cells do. Pre-check
   (Bayes-optimal model, `mode=opt`, `cmplx_ps`, 1M test samples, 2080 Ti):
   `wnelbo_ref = 1.6712 ± 0.0065` — on `H(p)`.
2. **The d = 2 findings carry over**: `cross_entropy` and `poincare_polar` training
   both reach `H(p)`, the `exp` rate sweet spot stays at or below the ~0.304
   variance cliff, and more steps help the `poincare_polar` cells more than the CE
   cells.
3. **Across the siblings** (3 → 9 → 16), the bridge identifies the word sooner in
   `t` (drift `(d-1)/2`), so `wce_ref` shrinks with d while the ELBO stays pinned
   at `H(p)`; the importance-weighted estimator's standard deviation grows with d
   (measured at the Bayes model: `wnelbo_ref_std` 6.5 → 23 → 29 for d = 3 → 9 → 11).

## What changed in the code to run this

- `main.py`: the model input is `z = (rho, u)` with `u` the bridge direction, a
  unit vector in `R^hyper_dim` — so `MLPLM.input_dim = hyper_dim + 1` and `z` is a
  `cat`, not the binary `stack([rho, theta])`. `bridge()` is handed
  `emb_dim=hyper_dim` for the `word_embedding is None` fallback.
- `script/train/{ce,pp}.sh`: `hyper_dim` comes from a `HYPER_DIM` env var
  (default 2, so `init_test` is unchanged).
- `word_embedding` is the trained `lm_head` weight `(V, hyper_dim)`, as at d = 2
  (`trainable_word_embedding=true`, `unif_word_embedding=false` — config defaults).

## Design

Grid from `setup.md` — identical to `init_test` except `hyper_dim`:
2 × 2 × 7 × 4 × 3 = **336 runs**, one SLURM job each.

| variable | values |
|---|---|
| `ps` | `naive_ps`, `cmplx_ps` |
| `loss_geometry` | `cross_entropy`, `poincare_polar` |
| `loss_proposal_exp_rate` | 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0 |
| `max_steps` | 20000, 40000, 100000, 200000 |
| `seed` | 0, 1, 2 |

Fixed: `hyper_dim=3`, `lr=1e-3`, `gradient_clip_val=1.0`, `test_size=4e6`,
`batch_size=2048`, `ref_proposal_type=exp`, `ref_proposal_exp_rate=0.1`.

`run_name` is byte-identical to `init_test`'s (the dimension is carried by the
project name), so `experiments/report.py init_refactor_3d` works unchanged and the
cells pair 1:1 with `init_test` for a d = 2 vs d = 3 comparison.

Note on the bridge at d > 2: `bridge()` clamps `t` at `_radial_t_max(d)` (97 at
d = 3, 5.6 at d = 9, 1.5 at d = 16) because the radial marginal is formed in linear
float64. Past that `t` the direction already identifies the word to full precision,
so the loss there is 0 regardless — statistically a no-op, but it means most of
the `exp(0.1)` mass at d = 9 / 16 sits on the clamp.

## GPU allocation

Both owned partitions, all four nodes — `--partition=thickstun,desa`, 1 GPU, 4
CPUs, 16 GB per job; `desa-compute-01` included (the model uses well under 1 GB).
Per-cell `--time` scales with `max_steps` (2× the 2080 Ti pilot rate of ~0.05
s/step + 5 min test): 43 min / 1 h 10 / 3 h 10 / 5 h 50.

Seed 0 at `--nice=0`, replicates at `--nice=50`, so a complete single-seed grid
lands first.

## Wall clock (expected)

Pilot on the 2080 Ti (the slowest node): ~0.04 s/step for d = 3 (the odd-d radial
sampler costs ~5 ms per `bridge()` call), 4M-sample test ≈ 80 s. Per
(ps, rate, geometry, seed) column: 360k steps ≈ 4.5 h → **~390 GPU-h** per
project. With the ~10 GPUs free at submission (the rest hold the user's `simpflm`
jobs and other users' work) that is ~1.5–2 days per project; faster as GPUs free up.

## Reporting

- `python experiments/report.py init_refactor_3d` → `RESULTS.md`.
- Cross-dimension comparison: the same command for `_9d` / `_16d`, plus
  `experiments/init_test/RESULTS.md` for d = 2.

## Grid extension (2026-08-23)

Added on request: the `init_test` `c1e4_exp1.0` slice at d = 3 —
`ps=c1e4_exp1.0` (V = 10^4 geometric, H = 1.0407), `max_steps=20000`, both
geometries × 7 rates × 3 seeds = 42 runs. Same run-name scheme, same output root,
so `report.py` picks it up as its own section. ~38 min/cell at d = 2 on the
2080 Ti; similar at d = 3 (the V = 10^4 loss matrices dominate, not the sampler).

## Grid extension (2026-08-25): `c1e3_exp1.0` and `c1e4_exp1.0`

`setup.md` now lists four `ps` specs. The two new ones are the same geometric law
`p_i ∝ e^-i` truncated at `V = 1000` / `10000`, so both share one analytic entropy,
`H = 1.040652` nats (`-log(1-q) + q/(1-q)`, `q = e^-1`) — the same `>= H(p)` check
applies to them as to `naive_ps` / `cmplx_ps`. They extend the grid from 336 to
**672 cells** (4 × 7 × 2 × 4 × 3); the full `max_steps` and `seed` axes are swept,
not just the 20000-step slice the earlier c1e4 extension covered.

### Why they are expensive

`HyperBridge.horosphere_geometry` and `bridge_loss_poincare_disk_polar` materialize
several `(batch, V, d)` float64 tensors, so both step time and peak GPU memory scale
with `V·d`. Measured at `batch=2048` on an RTX A6000, `hyper_dim = 3`:

| `ps` | V | train s/step | test s/batch | peak train GiB |
|---|---|---|---|---|
| `naive_ps` / `cmplx_ps` | 10 | ~0.022 | ~0.013 | 0.4 |
| `c1e3_exp1.0` | 1 000 | 0.027 | 0.0192 | 0.5 |
| `c1e4_exp1.0` | 10 000 | 0.170 | 0.1029 | 5.0 |

### GPU allocation

Both owned partitions stay in play (`--partition=thickstun,desa`). Only cells whose
measured peak exceeds a node's GPU are steered off it, per `sweep.excluded_nodes`
(measured peak × 1.25 for fragmentation and the CUDA context):

- `naive_ps`, `cmplx_ps`, `c1e3_exp1.0` — all four nodes.
- `c1e4_exp1.0` at `hyper_dim = 3` — excluded: none — all four nodes.

This exclusion is not theoretical: a `mode=opt` `c1e4` × `d = 16` validation run
died with `torch.OutOfMemoryError` on a 2080 Ti at the `ws` allocation in
`bridge_loss_poincare_disk_polar` (2.44 GiB requested, 1.36 GiB free).

Per-cell `--time` is now keyed by vocabulary size (`SEC_PER_STEP` / `TEST_SEC`),
doubled for headroom; `--nice` orders the queue by cost within a seed (small V and
short runs first), so a complete coarse picture lands before the expensive cells.

### Wall clock (expected)

At the measured rate, per project: **~114 GPU-h** for `c1e3_exp1.0` and
**~723 GPU-h** for `c1e4_exp1.0` (minus ~42 GPU-h already finished)
— **~795 GPU-h** for this project, ~5300 GPU-h across the three
siblings. That is ~220 GPU-days: the sweep is idempotent and resumable, so it fills
in over days rather than completing in one sitting.

### Pre-check (Bayes-optimal, `mode=opt`, 4M test samples)

The general-d bridge remains a valid ELBO at these vocabulary sizes — all readings
sit on `H(p)` within noise (the importance-weighted estimator's std grows with `d`,
so the standard error does too):

| run | `wnelbo_ref` | SE | `(x - H)/SE` |
|---|---|---|---|
| `c1e3` / `c1e4`, d = 3 | 1.0415 | 0.0027 | +0.31 |
| `c1e3` / `c1e4`, d = 9 | 1.0379 | 0.0094 | −0.30 |
| `c1e3` / `c1e4`, d = 16 | 1.0725 | 0.0202 | +1.58 |

`c1e3` and `c1e4` agree to ~15 significant figures at a given `d`
(`wnelbo_ref` byte-identical; `ce_ref` differs in the last ulp). Verified:

- Both runs really do use the distinct vocabularies — the `c1e3` log prints 1001
  `log_ps` entries, the `c1e4` log elides a 10000-entry tensor.
- The boundary tables are **not** shared: `uniform_sphere_points(1000, d)` differs
  from `uniform_sphere_points(10000, d)[:1000]` at `d = 3` (max|diff| 1.57) and
  `d = 9` (1.27). Only at `d = 16` do they coincide exactly. So an earlier
  "shared prefix" explanation for this is **wrong** and has been retracted.

**Resolved 2026-08-25.** The Bayes-optimal Girsanov integrand is
configuration-independent to float64 precision. Holding `ts`, `targets` and the RNG
fixed (so `rho` and the spike direction in the `e_1` frame are identical) and varying
only the boundary table, the per-sample losses agree to **1e-14 absolute**:

| d | ρ draws identical | max abs diff | mean (V=1000) | mean (V=10000) |
|---|---|---|---|---|
| 3 | yes | 2.7e-15 | 0.333634 | 0.333634 |
| 9 | yes | 3.6e-14 | 0.422465 | 0.422465 |
| 16 | yes | 2.8e-14 | 0.232466 | 0.232466 |

(Max *relative* diff looks large — up to 3.9 at d = 16 — but only on entries whose own
value is ~1e-15; against a mean of 0.23 the absolute agreement is what matters.)

Combined with identical RNG streams (same `seed`; `mode=opt` skips `trainer.fit` so the
global RNG never advances; same `test_size` / `batch_size`; `counts_from_ps` gives the
same counts for the only tokens that ever appear, `i <~ 15`), the two runs estimate the
same integrand on the same draws — hence agreement to ~15 significant figures.

**Practical consequence: the c1e3 and c1e4 Bayes-optimal checks are ONE validation of
the general-d bridge, not two independent ones.** Do not quote them as mutual
corroboration.
