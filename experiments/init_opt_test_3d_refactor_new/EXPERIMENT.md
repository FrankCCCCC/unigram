# init_opt_test_3d_refactor_new — Bayes-optimal control on `H^3_K`, curvature swept

`mode=opt`: `trainer.fit` is skipped and only the 4M-sample test pass runs against
`OptimalModelRefactor`, whose logits are the exact log-posterior. Same grid, same
geometry and same pinned reference proposal as the trained twin
`init_test_3d_refactor_new`, so the two pair **cell for cell**.

## What this project is for

`test_wnelbo_ref >= H(p)` is Invariant 2 of the repo: the ELBO cannot beat the entropy,
so a trained model that dips below it has leaked a side channel. That reading only holds
if the *estimator* is sound. This project measures the estimator directly — the model
here is exactly right by construction, has no parameters and no training noise, so
whatever `wnelbo_ref` it reports at a given curvature **is** the estimator's answer for
that curvature.

Concretely: `wnelbo_ref` here is the numerator of every claim the trained project makes.

- Lands on `H(p)` ⟹ the estimator is valid at that `K`, and the trained project's
  distance from `H(p)` is the model's.
- Lands **below** `H(p)` ⟹ the estimator under-reports at that `K`, and a trained cell
  below `H(p)` there is not evidence of a leak.

## Why curvature should move it

`K` fixes `R = 1/sqrt(-K)`. `main_refactor.py` clamps the heat time to
`_radial_t_max(3) · R^2 = 96.96 R^2` — **9.7** at `K = -10`, **97** at `K = -1`, **9696**
at `K = -0.01` — and the bridge concentrates in the dimensionless `u = rho / R`, so the
per-`t` loss decays ~`R^2` times more slowly as `K` flattens. The reference proposal is
pinned at `exp(0.1)` for every cell. The ~0.304 variance cliff measured at `K = -1`
(`L(t) ~ e^{-0.152 t}`) therefore scales as `1/R^2`:

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

Past the cliff the weighted estimator is still unbiased in expectation but has infinite
variance, and in a finite sample it under-reports: the mass sits at large `t`, where
`e^{0.1 t}` is enormous and the proposal essentially never draws.

The cliff crosses the pinned rate at `0.304 / R^2 = 0.1`, i.e. `R^2 = 3.04`,
**`K ≈ -0.33`**. The original three-curvature grid only bracketed that crossing between
`K = -1` and `K = -0.01`, two decades apart. The six curvatures `setup.md` adds (-4, -3,
-2 on the safe side; -0.5, -0.1, -0.05 straddling the crossing) narrow the bracket to
`K ∈ (-0.5, -0.1)` and turn a yes/no reading into a curve.

## Hypothesis

1. **`K <= -0.5`** (-10, -4, -3, -2, -1, -0.5): `wnelbo_ref` = `H(p)` within the standard
   error, for all four `ps` specs. (`H(naive_ps) = 0.5003`, `H(cmplx_ps) = 1.6664`,
   `H(c1e3) = H(c1e4) = 1.0407` nats.)
2. **`K >= -0.1`** (-0.1, -0.05, -0.01): `wnelbo_ref` materially **below** `H(p)`, with a
   large `wnelbo_ref_std` and an inflated `wce_ref`. This is the estimator failing, not
   the model — which is exactly the point of running the exact posterior here. The
   deficit should grow monotonically as `K` flattens, and the transition has to sit
   between `K = -0.5` and `K = -0.1` if the `1/R^2` cliff scaling is the right
   explanation. A deficit that turns on well before `K = -0.33` refutes that mechanism.
3. **Free consistency check**: `wnelbo_ref`, `nelbo_ref`, `wce_ref` and `ce_ref` all come
   from the reference pass, which is pinned to `exp(0.1)` on its own RNG stream
   (`salt=1`) and is independent of `loss_geometry` and `loss_proposal_exp_rate`. They
   must therefore be **identical across all 14 (geometry, rate) cells** of a given
   `(ps, K, seed)`. Only `wloss` may vary. Any drift is a bug in the RNG split.

## Design

Grid from `setup.md`: 4 × 9 × 7 × 2 × 3 = **1512 runs**, one SLURM job each.
The first 504 — `K` ∈ {-10, -1, -0.01} — were collected before the six curvatures
were added; the rest go into the same `output/` tree and the earlier cells are skipped
by the sweep's `test_metrics.json` idempotency guard.

| variable | values |
|---|---|
| `ps` | `naive_ps`, `cmplx_ps`, `c1e3_exp1.0`, `c1e4_exp1.0` |
| `gaussian_curvature` | -10.0, -4.0, -3.0, -2.0, -1.0, -0.5, -0.1, -0.05, -0.01 |
| `loss_geometry` | `cross_entropy`, `poincare_polar` |
| `loss_proposal_exp_rate` | 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0 |
| `seed` | 0, 1, 2 |

Fixed: `mode=opt`, `hyper_dim=3`, `test_size=4e6`, `batch_size=2048`,
`ref_proposal_type=exp`, `ref_proposal_exp_rate=0.1`. `lr` and `max_steps` are inert
(no `trainer.fit`) but stay in `run_name` so cells pair 1:1 with the trained twin.

`setup.md`'s result templates carry the four-step layout inherited from `init_test`; its
Training section pins `max_steps` to **{20000}**, which is what is run. Under `mode=opt`
the step count changes nothing anyway.

## GPU allocation

Both owned partitions (`--partition=thickstun,desa`), 1 GPU / 2 CPUs / 16 GB per job.
No training, so a cell is startup + one 4M-sample test pass: 30–60 s of GPU work at
`D = 3`. Peak memory is the trained project's (same forward shapes): 0.85 GiB at V = 10,
7.93 GiB at V = 10000 — all four nodes are eligible.

Per-cell `--time` is floored at 20 minutes; a shorter limit buys backfill that is not
worth the risk of losing a cell to a slow cold start.

## Wall clock (expected)

~**42 GPU-h** for the full 1512-cell grid — ~14 GPU-h already spent on the first three
curvatures, ~28 GPU-h for the six added ones. Still the cheapest of the four projects, and
the one to read first, since every conclusion the trained projects draw is conditioned
on it.

## Reporting

- `python experiments/report.py init_opt_test_3d_refactor_new` → `RESULTS.md`.
- The comparison that matters: this project's `wnelbo_ref` vs `H(p)` per `(ps, K)`,
  then `init_test_3d_refactor_new`'s `wnelbo_ref` vs **this** number. With nine
  curvatures, `wnelbo_ref` vs `K` reads as a curve: flat on `H(p)` while the pinned
  reference rate sits under the cliff, falling away once it does not.
- The trained twin still sweeps only `K` ∈ {-10, -1, -0.01}, so six of the nine
  curvatures here have no trained counterpart to pair with — they measure the estimator
  alone.
- `experiments/init_opt_test_refactor/RESULTS.md` is the `d = 2`, `K = -1` predecessor.
