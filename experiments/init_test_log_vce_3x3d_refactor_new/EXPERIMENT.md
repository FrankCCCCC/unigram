# init_test_log_vce_3x3d_refactor_new — variational CE on `H^3 × H^3 × H^3`

Does the Bayes-posterior variational CE stay tight to `H(p)` on a **product** manifold, and
what does mixing curvatures across factors cost? `main_refactor.py` runs
`prod_factor_dim=[3,3,3]` at ten curvature vectors with
`loss_geometry=var_cross_entropy`.

| project | objective | geometry |
|---|---|---|
| **`init_test_log_vce_3x3d_refactor_new`** (this) | `var_cross_entropy` | `H^3×H^3×H^3`, 10 vectors |
| `init_test_log_vce_3d_refactor_new` | `var_cross_entropy` | single `H^3_K`, 9 `K` |
| `init_test_3x3d_refactor_new` | `cross_entropy`, `poincare_polar` | `H^3×H^3×H^3`, mixed vector |

## The objective

    CE(y, p_θ) · Σ_m (d_m − 1)² κ_m² / (min_v D_{e_v,m})²

with `D_{e_v,m} = cosh u_m − sinh u_m ⟨φ_v, θ_m⟩`, `u_m = κ_m ρ_m`, and the minimum taken
over the whole vocabulary **per factor**. `min_v D_{e_v,m} ≤ D_{x,m}` termwise, so the weight
only grows and the bound survives, while depending on `z_t` alone — which is what keeps the
Bayes posterior the minimiser (`../init_test_log_vce_3d_refactor_new/vce_bayes.md`).

## What the product changes

1. **One heat-time ceiling for all three factors.** `t` is clamped to
   `min_m _radial_t_max(3) · R_m²`, `R_m = 1/√(−K_m)`. At `d=3`, `_radial_t_max = 97`, so the
   mixed vector `[-0.01, -10.0, -1.0]` has its ceiling set by the `K = -10` factor at **9.7**,
   not by the `K = -0.01` factor's 9700. The flat factor is therefore sampled over ~1/1000 of
   its natural range — the single-manifold `K = -0.01` cells (which broke the estimator, see
   the sibling project's `RESULTS.md` §2) may behave completely differently here.
2. **The weight sums over factors.** The sharpest factor dominates the weight magnitude; the
   flattest dominates the variance. The `d+2` tilt identity in `vce_bayes.md` is exact only
   at `M = 1`; what carries over to `M > 1` is the property that matters — the weight is
   target-free, so the minimiser is still `q`.
3. **`D = 9` triples the tensors.** Both the horosphere readout and the min-over-vocabulary
   weight materialise `(batch, V, M, d)` float64, driving cost and node eligibility.

## Hypothesis

1. **Headline: `test_wnelbo_ref ≥ H(p)`, and tight, on the uniform vectors.** For
   `[K,K,K]` with `K ∈ [−4, −0.1]` the result should match the single-manifold project's
   +0.0–2.4% band. `H(naive_ps) = 0.5003`, `H(cmplx_ps) = 1.6664`, `H(c1e4_exp1.0) = 1.0407`.
2. **The mixed vector `[-0.01,-10.0,-1.0]` should be BETTER behaved than single-manifold
   `K = -0.01`.** The `K = -10` factor pulls the shared heat-time ceiling down to 9.7, which
   keeps the reference proposal inside its variance-cliff range — the opposite of what
   happens when `K = -0.01` sets the ceiling alone. If this holds, the sub-`H(p)` readings
   that plagued flat single manifolds should not appear here.
3. **Uniform `[-0.01,-0.01,-0.01]` should still break the estimator**, since nothing pulls
   the ceiling down. This is the control for (2).
4. **Seed stability degrades at `c1e4_exp1.0`.** The sibling project found one of three seeds
   diverging at `V = 10 000` (+42.6% vs +3.2%/+3.9%), with `wloss` *anti-correlated* with
   ELBO quality. `D = 9` spreads the same gradient budget over three factors, so this should
   be at least as bad here. Watch per-seed spread, not just the 3-seed mean.

## Design

Grid from `setup.md`: 3 × 10 × 7 × 1 × 3 = **630 runs**.

| axis | values |
|---|---|
| `ps` | `naive_ps`, `cmplx_ps`, `c1e4_exp1.0` |
| `prod_factor_gaussian_curvature` | `[-0.01,-10.0,-1.0]`, plus `[K,K,K]` for K ∈ {−0.01, −0.05, −0.1, −0.5, −1.0, −2.0, −3.0, −4.0, −10.0} |
| `loss_proposal_exp_rate` | 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0 (`stratified_exp`) |
| `loss_geometry` | `var_cross_entropy` |
| `seed` | 0, 1, 2 |

Fixed: `mode=tnb`, `prod_factor_dim=[3,3,3]`, `lr=1e-3`, `max_steps=20000`,
`gradient_clip_val=1.0`, `test_size=4e6`, `batch_size=2048`,
`ref_proposal_type=stratified_exp`, `ref_proposal_exp_rate=0.1`.

No deviation from `setup.md` this time — it already specifies `stratified_exp` for the
reference path, so `wnelbo_ref` is measured the same way as in the sibling project.

`sweep_lib.Project` gained the ability to SWEEP a product curvature vector (previously it
could only fix one): the vector rides in the run name as the `x`-joined tag and
`prod_curvature_for()` rebuilds the hydra list per cell. Without that, sweeping would have
changed only the run name while every cell trained the same geometry.

## GPU allocation and expected wall clock

One job per cell, `gpu:1`, 2 CPUs, 16 GB, partition `thickstun,desa`, time limit and node
exclusions from the cost model. Seed 0 at `nice=0`, replicates at `nice=100`.

| cell | budgeted |
|---|---|
| `naive_ps` / `cmplx_ps` (V = 10, D = 9) | ~895 GPU-s |
| `c1e4_exp1.0` (V = 10 000, D = 9) | ~6020 GPU-s |
| **full grid** | **~456 GPU-h** |

Nearly 3× the single-manifold project. `PEAK_GB[(10000, 9)]` was measured under the OLD
target-indexed loss; the min-over-vocabulary weight materialises `(batch, V, M, d)` tensors
that are 3× larger at `M = 3`, so the figure is re-measured before submitting and
`sweep_lib.PEAK_GB` updated if it moved — an understated peak is what cost two cells to OOM
on a 24 GB A5000 previously.

## Success criteria

- Every cell finishes with a finite `test_wloss` — no NaN, no overflow, no OOM.
- Uniform `[K,K,K]` for `K ∈ [−4, −0.1]`: `test_wnelbo_ref ≥ H(p)` and within a few percent,
  matching the single-manifold project.
- Any cell below `H(p)` is also below it for the Bayes-optimal model on the same geometry
  (`init_opt_test_3x3d_refactor_new` where available), i.e. attributable to the estimator.
- Per-seed spread reported separately for `c1e4_exp1.0`, not hidden in a 3-seed mean.

`experiments/report.py init_test_log_vce_3x3d_refactor_new` writes `RESULTS.md`.
