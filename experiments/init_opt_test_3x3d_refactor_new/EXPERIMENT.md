# init_opt_test_3x3d_refactor_new — Bayes-optimal control on `H^3_{-0.01} × H^3_{-10} × H^3_{-1}`

`mode=opt`: `trainer.fit` is skipped and only the 4M-sample test pass runs against
`OptimalModelRefactor`, whose logits are the exact log-posterior. Same product geometry,
same grid and the same pinned reference proposal as `init_test_3x3d_refactor_new`, so
the two pair **cell for cell**.

## What this project is for

Identical in role to `init_opt_test_3d_refactor_new`, one geometry over: it measures the
**estimator**, not a model. `test_wnelbo_ref >= H(p)` (Invariant 2) is the check every
trained cell is read against, and that check is only meaningful where the importance-
weighted estimator can actually resolve the integral. Here the model is exact by
construction, parameter-free and training-noise-free, so whatever `wnelbo_ref` it reports
is the estimator's own answer for this product manifold.

## Why the product should be well-conditioned

The reference proposal is pinned at `exp(0.1)`, and the ~0.304 variance cliff measured at
`K = -1` scales as `1/R^2` with `R = 1/sqrt(-K)` — so a flat factor alone (`K = -0.01`,
`R^2 = 100`, cliff ~0.00304) is far past it. The product does **not** inherit that,
because `main_refactor.py` clamps the heat time to the **minimum** over factors of
`_radial_t_max(3) · R_m^2`:

| factor | `K` | `R^2` | own ceiling |
|---|---|---|---|
| 1 | -0.01 | 100 | 9700 |
| 2 | -10 | 0.1 | **9.7 ← binds** |
| 3 | -1 | 1 | 97 |

`t` never exceeds 9.7, which is the sharpest factor's regime, where `exp(0.1)` is
comfortably below the cliff. If that reasoning is right this project lands on `H(p)`;
if it lands below, the ceiling is not what governs the estimator's conditioning and the
single-factor `K = -0.01` reading needs a different explanation.

## Hypothesis

1. **`wnelbo_ref` = `H(p)` within the standard error** for all four `ps` specs
   (`H(naive_ps) = 0.5003`, `H(cmplx_ps) = 1.6664`, `H(c1e3) = H(c1e4) = 1.0407` nats),
   i.e. the product geometry is measurable under the pinned reference proposal.
2. **The estimator is noisier than at `d = 3`.** `wnelbo_ref_std` grows with dimension
   (measured on earlier projects: 6.5 → 23 → 29 for `d` = 3 → 9 → 16 at the Bayes model),
   so expect roughly the `d = 9` figure at `D = 9` here, and a correspondingly wider
   standard error on the `>= H(p)` check.
3. **Free consistency check**: `wnelbo_ref`, `nelbo_ref`, `wce_ref` and `ce_ref` all come
   from the reference pass, which is pinned to `exp(0.1)` on its own RNG stream
   (`salt=1`) and is independent of `loss_geometry` and `loss_proposal_exp_rate`. They
   must be **identical across all 14 (geometry, rate) cells** of a given `(ps, seed)`.
   Only `wloss` may vary.

### Pilot evidence — not yet a result

A 409 600-sample `mode=opt` pilot cell (`naive_ps`, CE, RTX 6000 Ada, 2026-09-06;
scratchpad, not checked in) returned `wnelbo_ref = 0.5016` against
`H(naive_ps) = 0.5003`, with `wnelbo_ref_std = 13.5`. That is +0.0013 on a standard error
of 0.021, i.e. on `H(p)` — consistent with (1) and (2) at a tenth of the production
sample size.

## Design

Grid from `setup.md`: 4 × 7 × 2 × 3 = **168 runs**, one SLURM job each.

| variable | values |
|---|---|
| `ps` | `naive_ps`, `cmplx_ps`, `c1e3_exp1.0`, `c1e4_exp1.0` |
| `loss_geometry` | `cross_entropy`, `poincare_polar` |
| `loss_proposal_exp_rate` | 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0 |
| `seed` | 0, 1, 2 |

Fixed: `mode=opt`, `prod_factor_dim=[3,3,3]`,
`prod_factor_gaussian_curvature=[-0.01,-10.0,-1.0]`, `test_size=4e6`,
`batch_size=2048`, `ref_proposal_type=exp`, `ref_proposal_exp_rate=0.1`. `lr` and
`max_steps` are inert (no `trainer.fit`) but stay in `run_name` so cells pair 1:1 with
the trained twin.

The geometry is fixed, so it lives in the project name and `run_name` carries no `_k-`
field — `experiments/report.py` parses it unchanged.

## GPU allocation

Both owned partitions (`--partition=thickstun,desa`), 1 GPU / 2 CPUs / 16 GB per job.
No training, so a cell is startup + one 4M-sample test pass: 35–160 s of GPU work at the
Ada rate. Peak memory is the trained project's (same forward shapes), so `c1e4` at
`D = 9` (17.86 GiB measured) is excluded from `desa-compute-01`'s 2080 Ti and everything
else is eligible on all four nodes.

Per-cell `--time` is floored at 20 minutes; a shorter limit buys backfill that is not
worth the risk of losing a cell to a slow cold start.

## Wall clock (expected)

~**6 GPU-h** for the full 168-cell grid — the cheapest of the four projects. Run it and
`init_opt_test_3d_refactor_new` first: every conclusion the two trained projects draw is
conditioned on what these two report.

## Reporting

- `python experiments/report.py init_opt_test_3x3d_refactor_new` → `RESULTS.md`.
- The comparison that matters: this project's `wnelbo_ref` vs `H(p)` per `ps`, then
  `init_test_3x3d_refactor_new`'s `wnelbo_ref` vs **this** number.
- Cross-geometry: `init_opt_test_3d_refactor_new` gives the same estimator reading with
  the three curvatures taken one at a time.
