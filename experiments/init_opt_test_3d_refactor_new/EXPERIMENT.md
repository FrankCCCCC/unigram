# init_opt_test_3d_refactor_new — Bayes-optimal control on `H^3_K`, curvature swept

`mode=opt`: `trainer.fit` is skipped and only the 4M-sample test pass runs against
`OptimalModelRefactor`, whose logits are the exact log-posterior. Same curvature grid and
the same pinned reference proposal as the trained twins `init_test_3d_refactor_new`
(`cross_entropy`, `poincare_polar`) and `init_test_log_vce_3d_refactor_new`
(`var_cross_entropy`), so they pair **cell for cell**.

## Revision (2026-09-15): `stratified_exp` proposals and the VCE objective

`setup.md` changed three things, so the whole grid is re-run from scratch:

| | previous grid | this grid |
|---|---|---|
| `loss_proposal_type` | `exp` | `stratified_exp` |
| `ref_proposal_type` | `exp` | `stratified_exp` |
| `loss_geometry` | `cross_entropy`, `poincare_polar` | + `var_cross_entropy` |

Plain `exp` no longer runs: `Proposal.proposal` gates it behind `allowed_exp` (commit
`40e02bd`), which `hyper_proposal` never passes. The previous 1512-cell `exp` grid is no
longer in `output/`; its headline numbers are quoted below as the prior this revision is
tested against.

## What this project is for

`test_wnelbo_ref >= H(p)` is Invariant 2 of the repo: the ELBO cannot beat the entropy,
so a trained model that dips below it has leaked a side channel. That reading only holds
if the *estimator* is sound. This project measures the estimator directly — the model
here is exactly right by construction, has no parameters and no training noise, so
whatever `wnelbo_ref` it reports at a given curvature **is** the estimator's answer for
that curvature.

- Lands on `H(p)` ⟹ the estimator is valid at that `K`, and the trained project's
  distance from `H(p)` is the model's.
- Lands **below** `H(p)` ⟹ the estimator under-reports at that `K`, and a trained cell
  below `H(p)` there is not evidence of a leak.

**Second role, new in this revision.** `var_cross_entropy` weights the denoising CE by
`sum_m (d_m-1)^2 kappa_m^2 / (min_v D_{e_v,m})^2`, a function of `z_t` alone, so the Bayes
posterior is its minimiser (`../init_test_log_vce_3d_refactor_new/vce_bayes.md`). This
project's VCE `wloss` is therefore the population floor the trained VCE twin's
`test_wloss` can only approach from above. Unlike the ELBO it has no distribution-only
closed form to check against.

## What stratification does and does not change

`stratified_exp` draws one `u` in each stratum `[i/n, (i+1)/n)` of an `n = 2048` batch,
shuffles them, and maps `t = -ln(u)/rate` with weight `1/(rate·u)`. Each sample's
marginal is still `Exp(rate)`, so:

- the **per-sample variance** — what `*_std` records, and the ~0.304 cliff at `K = -1` —
  is unchanged;
- the **batch mean** is less noisy: every batch puts exactly one sample in each proposal
  quantile, so the across-seed spread of `wnelbo_ref` should shrink, and `std/sqrt(4e6)`
  now *over*states the standard error;
- the **reach** is unchanged: the lowest stratum `[0, 1/2048)` gets one draw per batch,
  1953 over the test pass, which is the expected count plain `exp` puts there too. The
  largest `t` drawn stays ~`-ln(2.5e-7)/0.1 ≈ 150`.

The last point is why the flat-curvature collapse should survive the revision: at
`K = -0.01` the integral runs out to the heat-time ceiling 9696, and neither proposal
draws anywhere near it.

## Why curvature should move it

`K` fixes `R = 1/sqrt(-K)`. `main_refactor.py` clamps the heat time to
`_radial_t_max(3) · R^2 = 96.96 R^2` — **9.7** at `K = -10`, **97** at `K = -1`, **9696**
at `K = -0.01` — and the bridge concentrates in the dimensionless `u = rho / R`, so the
per-`t` loss decays ~`R^2` times more slowly as `K` flattens. The reference proposal is
pinned at `stratified_exp(0.1)` for every cell. The ~0.304 variance cliff measured at
`K = -1` (`L(t) ~ e^{-0.152 t}`) therefore scales as `1/R^2`:

| `K` | `R^2` | heat-time ceiling | approx. variance cliff | pinned ref rate 0.1, over the cliff |
|---|---|---|---|---|
| -10 | 0.1 | 9.7 | ~3.04 | 0.03× — far below |
| -4 | 0.25 | 24.2 | ~1.216 | 0.08× |
| -3 | 0.33 | 32.3 | ~0.912 | 0.11× |
| -2 | 0.5 | 48.5 | ~0.608 | 0.16× |
| -1 | 1 | 97 | ~0.304 | 0.33× |
| -0.5 | 2 | 194 | ~0.152 | 0.66× — just under |
| -0.1 | 10 | 970 | ~0.0304 | **3.3× — over** |
| -0.05 | 20 | 1939 | ~0.0152 | **6.6× — over** |
| -0.01 | 100 | 9696 | ~0.00304 | **32.9× — over** |

The previous `exp` grid measured where this actually bites. `wnelbo_ref` was within ±1%
of `H(p)` for `K ∈ [-10, -0.1]`, 1–2% low at `K = -0.05`, and 25–28% low at `K = -0.01`.
So the estimator stays usable to ~3.3× past the cliff, not merely up to it.

## Hypothesis

1. **`K ∈ [-10, -0.1]`**: `wnelbo_ref` = `H(p)` within noise, for all four `ps` specs
   (`H(naive_ps) = 0.5003`, `H(cmplx_ps) = 1.6664`, `H(c1e3) = H(c1e4) = 1.0407` nats),
   with a **smaller across-seed spread** than the `exp` grid had.
2. **`K = -0.05` stays 1–2% low and `K = -0.01` stays ~25% low**: stratification evens out
   *which* quantiles a batch hits but cannot reach `t` the proposal never draws. If the
   `K = -0.01` deficit shrinks materially, the reach argument above is wrong.
3. **Free consistency check**: `wnelbo_ref`, `nelbo_ref`, `wce_ref` and `ce_ref` all come
   from the reference pass, which runs on its own RNG stream (`salt=1`) and is independent
   of `loss_geometry` and `loss_proposal_exp_rate`. They must therefore be **identical
   across all 21 (geometry, rate) cells** of a given `(ps, K, seed)`. Only `wloss` may vary.
   Any drift is a bug in the RNG split.
4. **VCE `wloss` is finite in every cell** (the weight is accumulated in log space), with a
   per-sample variance far above `poincare_polar`'s. Its `1/D^2` weight grows like `e^{2u}`
   and is unbounded, so the integral over `t` need not converge, and where it does not the
   mean will drift with the loss rate instead of settling on one value.
5. **VCE breaks the `c1e3` / `c1e4` degeneracy.** The ELBO and CE readings of those two specs
   were identical to every printed digit on the `exp` grid. VCE's weight takes a minimum
   over the *whole* vocabulary, and 10× more boundary points put the nearest one closer to
   `theta`, so its `wloss` is expected to differ between them.

## Design

Grid from `setup.md`: 4 × 9 × 7 × 3 × 3 = **2268 runs**, one SLURM job each.

| variable | values |
|---|---|
| `ps` | `naive_ps`, `cmplx_ps`, `c1e3_exp1.0`, `c1e4_exp1.0` |
| `gaussian_curvature` | -10.0, -4.0, -3.0, -2.0, -1.0, -0.5, -0.1, -0.05, -0.01 |
| `loss_geometry` | `cross_entropy`, `poincare_polar`, `var_cross_entropy` |
| `loss_proposal_exp_rate` | 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0 (`stratified_exp`) |
| `seed` | 0, 1, 2 |

Fixed: `mode=opt`, `hyper_dim=3`, `test_size=4e6`, `batch_size=2048`,
`ref_proposal_type=stratified_exp`, `ref_proposal_exp_rate=0.1`. `lr` and `max_steps` are
inert (no `trainer.fit`) but stay in `run_name` so cells pair 1:1 with the trained twins.

## GPU allocation

Both owned partitions (`--partition=thickstun,desa`), 1 GPU / 2 CPUs / 16 GB per job, no
training — a cell is startup plus one 4M-sample test pass. `sweep_lib.PEAK_GB` is the
*training* peak, so it is conservative for a forward-only pass. At `V = 10000, D = 3` all
four nodes stay eligible; the 2080 Ti has already completed 40 *trained* VCE cells at that
shape.

`--time` is the 20-minute floor for every cell; the previous grid's longest test pass was
401 s.

## Wall clock (expected)

Measured on the previous `exp` grid (sacct, 1512 cells, 51.8 GPU-h): a mean of 81 / 86 / 97 /
228 s per cell for `naive` / `cmplx` / `c1e3` / `c1e4`. At 567 cells per `ps` that projects to
**~78 GPU-h**. VCE's test pass costs between CE's and PP's on the trained twins, so budget
~80 GPU-h. (`sweep_lib`'s cost model budgets 63.)

## Reporting

- `python experiments/report.py init_opt_test_3d_refactor_new` → `RESULTS.md`: CE,
  Polar-ELBO and Variational-CE tables per `(ps, K)`, plus the dense table.
- The comparisons that matter:
  - this project's `wnelbo_ref` vs `H(p)` per `(ps, K)`;
  - the trained twins' `wnelbo_ref` vs **this** number;
  - the trained VCE twin's `test_wloss` vs this project's VCE `wloss`.
- `visualization/wloss_exp_var_vs_curvature.py` → `imgs/`.
- `experiments/init_opt_test_refactor/RESULTS.md` is the `d = 2`, `K = -1` predecessor.
