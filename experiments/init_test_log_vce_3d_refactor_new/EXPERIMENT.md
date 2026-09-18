# init_test_log_vce_3d_refactor_new — the variational-CE objective on `H^3_K`

Does the **variational cross-entropy** objective train a model whose reference ELBO is tight
to `H(p)`, and how does that hold up across curvature? `main_refactor.py` runs on a single
factor `H^3_K` at nine curvatures with `loss_geometry=var_cross_entropy`.

| project | objective | geometry |
|---|---|---|
| **`init_test_log_vce_3d_refactor_new`** (this) | `var_cross_entropy` | `H^3_K`, 9 `K` |
| `init_test_3d_refactor_new` | `cross_entropy`, `poincare_polar` | `H^3_K`, same grid |

## The objective

With `u_m = κ_m ρ_m` and `D_{e_v,m} = cosh u_m − sinh u_m ⟨φ_v, θ_m⟩`,

    CE(y, p_θ) · Σ_m (d_m − 1)² κ_m² / (min_v D_{e_v,m})²

an upper bound on the shared-`D_x` angular path-KL (slides/aug26_2026). Two properties
shape the experiment:

1. **The weight is unbounded.** `poincare_polar`'s integrand is capped at `2(d_m−1)²κ_m²`
   because `‖w_v‖ = 1`; here `1/D²` grows like `e^{2u_m}`. `RHO_MAX = 350` caps it at
   `~1e304`, leaving no headroom to sum `M` terms linearly — hence the log-space
   accumulation, and hence curvature (`κ = √(−K)`, the blow-up rate) as the stress axis.
2. **The denominator is `min_v D_{e_v,m}`, not the target's `D_{x,m}`.** This is what makes
   the weight a function of `z_t` alone. A target-indexed weight turns the objective into a
   proper scoring rule for the *tilted* posterior `ν ∝ q·w` rather than for `q`; the full
   derivation, including the exact identity `L(p) = Z·(H(ν) + KL(ν‖p))` and the result that
   `ν` is the Bayes posterior at dimension `d+2`, is in `vce_bayes.md`. The minimum
   dominates the target's term factor by factor, so the bound survives.

Note `wloss` bounds the **angular surrogate**, not the ELBO — it is not comparable to
`H(p)`. The quantity that must respect `H(p)` is `wnelbo_ref`, always measured with
`poincare_polar` on the independent reference stream.

## Hypothesis

1. **Headline (Invariant 2): `test_wnelbo_ref ≥ H(p)`, and tight.** `H(naive_ps) = 0.5003`,
   `H(cmplx_ps) = 1.6664`, `H(c1e4_exp1.0) = 1.0407` nats. At the rates below the variance
   cliff the trained model should land on `H(p)` from above, matching the `cross_entropy`
   column of `init_test_3d_refactor_new` to within seed spread.
2. **`wloss` is large and grows as the rate falls.** The `1/D²` weight is unbounded, so the
   integral over `t` need not converge; a loose-but-correct bound still trains a model whose
   `wnelbo_ref` is tight. `wloss` magnitude is therefore not evidence of a problem.
3. **Curvature bounds the usable range.** The `~0.304` variance cliff was measured at
   `K = −1` and the per-`t` decay scales with `−K`, so at `K = −0.01` the pinned rate-0.1
   reference sits ~32× above its cliff. Expect `wnelbo_ref` below `H(p)` there with a large
   `wnelbo_ref_std`, in **both** this project and the `cross_entropy` baseline — which is
   what identifies it as an estimator artifact rather than an objective failure.
4. **Sharper curvature is the easy end.** `K ∈ {−2, −3, −4, −10}` compresses `t`, keeping the
   reference proposal far below its cliff, so those should be the tightest cells.

### Prior evidence

A 3-cell pilot at (`naive_ps`, `K = −1`, seed 0, 20 000 steps, 4M test) gave `wnelbo_ref`
0.5084 / 0.5042 / 0.5039 at rates 0.05 / 0.1 / 0.25 against `H = 0.5003` — i.e. 0.7–1.6%
above, on the `cross_entropy` baseline (0.4999–0.5004). The target-indexed weight gave
0.7002 / 0.7505 / 0.7602 on the identical cells. See `RESULTS.md`.

## Design

Grid from `setup.md`: 3 × 9 × 7 × 1 × 3 = **567 runs**, one SLURM job each.

| axis | values |
|---|---|
| `ps` | `naive_ps`, `cmplx_ps`, `c1e4_exp1.0` |
| `gaussian_curvature` | −1.0, −2.0, −3.0, −4.0, −10.0, −0.5, −0.1, −0.05, −0.01 |
| `loss_proposal_exp_rate` | 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0 (`stratified_exp`) |
| `loss_geometry` | `var_cross_entropy` |
| `seed` | 0, 1, 2 |

Fixed: `mode=tnb`, `hyper_dim=3`, `lr=1e-3`, `max_steps=20000`, `gradient_clip_val=1.0`,
`test_size=4e6`, `batch_size=2048`, `ref_proposal_type=stratified_exp`,
`ref_proposal_exp_rate=0.1`.

**Deviation from `setup.md`:** its "Ref ELBO & CE" section reads `ref_proposal_type: exp`,
but `exp` now raises through `hyper_proposal` (which does not pass `allowed_exp`), so the
reference path runs `stratified_exp` at rate 0.1, matching the train scripts. This means
`wnelbo_ref` is no longer measured on the same reference path as the
`init_test_3d_refactor_new` baselines, which used `exp(0.1)`.

`gradient_clip_val=1.0` is load-bearing: the `1/D²` weight is heavier-tailed than `1/π(t)`
alone.

## GPU allocation and expected wall clock

`sweep.py` via `experiments/sweep_lib.py`: one job per cell, `gpu:1`, 2 CPUs, 16 GB,
partition `thickstun,desa`, time limit from the cost model, nodes whose GPU cannot hold the
cell excluded. Seed 0 at `nice=0`, replicates at `nice=100`, so a complete single-seed grid
lands first.

| cell | budgeted |
|---|---|
| `naive_ps` / `cmplx_ps` (V = 10, D = 3) | ~430 GPU-s |
| `c1e4_exp1.0` (V = 10 000, D = 3) | ~2160 GPU-s |
| **full grid** | **~168 GPU-h** |

Wall clock depends on free capacity on `thickstun,desa`; the sweep is idempotent, so a
partial run resumes by re-running it.

## Success criteria

- Every cell finishes with a finite `test_wloss` — no NaN, no overflow.
- At `K ∈ {−1, −2, −3, −4, −10}` below the cliff, `test_wnelbo_ref ≥ H(p)` and within a few
  percent, matching `init_test_3d_refactor_new`'s `cross_entropy` column.
- Any cell below `H(p)` is also below it in the `cross_entropy` baseline at the same
  `(ps, K, rate)` — i.e. attributable to the estimator, not the objective.

`experiments/report.py init_test_log_vce_3d_refactor_new` writes the table to `RESULTS.md`.
