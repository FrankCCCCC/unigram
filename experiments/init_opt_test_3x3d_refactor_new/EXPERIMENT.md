# init_opt_test_3x3d_refactor_new — Bayes-optimal control on `H^3 × H^3 × H^3`, ten curvature vectors

`mode=opt`: `trainer.fit` is skipped and only the 4M-sample test pass runs against
`OptimalModelRefactor`, whose logits are the exact log-posterior. It uses the same product
geometries, grid and pinned reference proposal as the trained twins:
`init_test_3x3d_refactor_new` (`cross_entropy`, `poincare_polar`) and
`init_test_log_vce_3x3d_refactor_new` (`var_cross_entropy`, the same ten vectors).

## Revision (2026-09-15)

| | previous grid | this grid |
|---|---|---|
| `loss_proposal_type` / `ref_proposal_type` | `exp` / `exp` | `stratified_exp` / `stratified_exp` |
| `loss_geometry` | `cross_entropy`, `poincare_polar` | + `var_cross_entropy` |
| `prod_factor_gaussian_curvature` | `[-0.01,-10.0,-1.0]` only | that vector + nine uniform `[K,K,K]` |
| runs | 168 | 2520 |

`setup.md` had already listed the ten vectors (commits `fef4ece`, `b05af07`), but the sweep
still pinned the mixed one. It now sweeps them, via `sweep_lib.Project.prod_curvature_for`.
Plain `exp` no longer runs (`allowed_exp` gate, commit `40e02bd`). The previous 168 cells
are no longer in `output/`. What stratification does and does not change is spelled out in
`../init_opt_test_3d_refactor_new/EXPERIMENT.md`: the per-sample variance and the
proposal's reach are unchanged, and only the batch mean gets quieter.

## What this project is for

Identical in role to `init_opt_test_3d_refactor_new`, one geometry over: it measures the
**estimator**, not a model. `test_wnelbo_ref >= H(p)` (Invariant 2) is the check every
trained cell is read against, and that check is only meaningful where the importance-
weighted estimator can actually resolve the integral. Here the model is exact by
construction, parameter-free and training-noise-free, so whatever `wnelbo_ref` it reports
is the estimator's own answer for that product manifold. Its VCE `wloss` is likewise the
population floor for the trained VCE twin, since the Bayes posterior minimises VCE.

## The mechanism under test: one heat-time ceiling for all factors

`main_refactor.py` clamps `t` to the **minimum** over factors of
`_radial_t_max(3) · R_m^2`, `R_m = 1/sqrt(-K_m)`:

| vector | binding factor | ceiling |
|---|---|---|
| `[-0.01,-10.0,-1.0]` | `K = -10` | **9.7** |
| `[-10,-10,-10]` | all | 9.7 |
| `[-4,-4,-4]` / `[-3,-3,-3]` / `[-2,-2,-2]` | all | 24.2 / 32.3 / 48.5 |
| `[-1,-1,-1]` / `[-0.5,-0.5,-0.5]` | all | 97 / 194 |
| `[-0.1,-0.1,-0.1]` / `[-0.05,-0.05,-0.05]` | all | 970 / 1939 |
| `[-0.01,-0.01,-0.01]` | all | **9696** |

The previous `exp` grid measured only the mixed vector. On every reference metric it
was numerically indistinguishable from the pure single-manifold `K = -10` control:

- `wnelbo_ref` 0.4976 vs 0.4974 on `naive_ps`;
- per-sample std 13.3 vs 13.0.

The sharp factor sets the ceiling, so the flat factor never reaches the regime where the
pinned proposal loses the integral. The uniform vectors test the converse that result
predicted but never measured: with no sharp factor to bind the ceiling, a flat product
should inherit the flat factor's measurement problem.

## Hypothesis

1. **Mixed vector lands on `H(p)`** for all four `ps` specs (`H(naive_ps) = 0.5003`,
   `H(cmplx_ps) = 1.6664`, `H(c1e3) = H(c1e4) = 1.0407` nats). It reproduces the
   single-manifold `K = -10` reading, and is **not** the same as `[-10,-10,-10]`: there
   all three factors are informative within the ceiling, so the posterior sharpens faster
   and `ce_ref` / `wce_ref` should come out lower.
2. **Uniform `[K,K,K]` with `K ∈ [-10, -0.1]` lands on `H(p)`**, like the single manifold.
3. **`[-0.05]^3` reads slightly low and `[-0.01]^3` collapses** by roughly the ~25% of the
   single-manifold `K = -0.01` control. This is the control for the ceiling mechanism: if
   `[-0.01]^3` lands on `H(p)`, the ceiling is not what governs the estimator.
4. **Free consistency check**: the four reference metrics are **identical across all 21
   (geometry, rate) cells** of a given `(ps, vector, seed)` (own RNG stream, `salt=1`).
   Only `wloss` may vary.
5. **VCE `wloss` is finite in every cell**, with heavier tails than `poincare_polar`. The
   weight *sums* over factors, so the sharpest factor dominates its magnitude and the
   flattest dominates its variance.

## Design

Grid from `setup.md`: 4 × 10 × 7 × 3 × 3 = **2520 runs**, one SLURM job each.

| variable | values |
|---|---|
| `ps` | `naive_ps`, `cmplx_ps`, `c1e3_exp1.0`, `c1e4_exp1.0` |
| `prod_factor_gaussian_curvature` | `[-0.01,-10.0,-1.0]`, and `[K,K,K]` for K ∈ {-0.01, -0.05, -0.1, -0.5, -1.0, -2.0, -3.0, -4.0, -10.0} |
| `loss_geometry` | `cross_entropy`, `poincare_polar`, `var_cross_entropy` |
| `loss_proposal_exp_rate` | 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0 (`stratified_exp`) |
| `seed` | 0, 1, 2 |

Fixed: `mode=opt`, `prod_factor_dim=[3,3,3]`, `test_size=4e6`, `batch_size=2048`,
`ref_proposal_type=stratified_exp`, `ref_proposal_exp_rate=0.1`. `lr` and `max_steps` are
inert but stay in `run_name` so cells pair 1:1 with the trained twins.

The vector is swept, so it rides in `run_name` as the `x`-joined `_k-` tag
(`_k--0.01x-10.0x-1.0`), which `experiments/report.py` parses and orders flattest-first.

## GPU allocation

Both owned partitions (`--partition=thickstun,desa`), 1 GPU / 2 CPUs / 16 GB per job.
`c1e4` at `D = 9` is sized at `PEAK_GB[(10000, 9)] = 25.4 GiB` × 1.15, which excludes
`desa-compute-01` (11 GB) and `kuleshov-compute-03` (24 GB). Its 630 cells therefore run
on the 18 48-GB GPUs.

That peak is a *training* measurement and conservative for a forward-only pass. It is kept
because VCE's `(batch, V, M, d)` min-over-vocabulary tensors at this shape are unmeasured
in `mode=opt`. Every other cell is eligible on all four nodes. `--time` is the 20-minute
floor; the previous grids' longest `D = 9` test pass was 750 s.

## Wall clock (expected)

Measured on the previous `D = 9` opt grids (sacct): a mean of 82 / 80 / 93 / 500 s per cell for
`naive` / `cmplx` / `c1e3` / `c1e4`. At 630 cells per `ps` that is **~132 GPU-h**, dominated
by `c1e4` (~88 GPU-h) on the 48-GB cards. (`sweep_lib`'s cost model budgets 91.)

## Reporting

- `python experiments/report.py init_opt_test_3x3d_refactor_new` → `RESULTS.md`, one section
  per `(ps, vector)`.
- The comparisons that matter:
  - `wnelbo_ref` vs `H(p)` per `(ps, vector)`;
  - each uniform vector vs the single-manifold control `init_opt_test_3d_refactor_new` at
    the same `K`;
  - the trained twins' `wnelbo_ref` / VCE `test_wloss` vs this project's numbers.
