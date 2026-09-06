# init_test_3x3d_refactor_new — trained model on `H^3_{-0.01} × H^3_{-10} × H^3_{-1}`

The product-manifold arm of the curvature study. Where `init_test_3d_refactor_new` runs
three *separate* models at three curvatures, this project gives **one** model all three
curvatures at once, as three factors of a product manifold — the configuration
`main_refactor.py`'s `prod_factor_dim` / `prod_factor_gaussian_curvature` path was
written for.

Sibling projects: `init_test_3d_refactor_new` (single factor, `K` swept),
`init_opt_test_3d_refactor_new` and `init_opt_test_3x3d_refactor_new` (the Bayes-optimal
controls for each).

## What the product changes

`HyperbolicHeatKernel.poincare_bridge_prod` samples an independent bridge on every
factor: `rhos` is `(N, 1, M)` — one intrinsic radius per factor — and `thetas` is
`(N, 1, sum d_m)`, the per-factor unit directions concatenated. So with
`prod_factor_dim=[3,3,3]`:

- The model input is 3 radii + 9 direction components, and `D = sum(d_m) = 9` sets the
  width of the `(batch, V, D)` float64 tensors the horosphere readout materialises.
- The word embedding is one `(V, 9)` table, split across factors — the same `lm_head`
  weight the bridge samples toward, the loss scores against, and the model's horosphere
  readout uses.
- **The heat-time ceiling is the MINIMUM over factors**, `min_m _radial_t_max(3) · R_m^2`
  = `min(9700, 9.7, 97)` = **9.7**, set by the sharpest factor `K = -10`. The flattest
  factor `K = -0.01` never sees more than 1/1000 of the physical time it would get alone.

That last point is the interesting one: the product is *not* the union of the three
single-curvature runs. Its `t` range is the sharpest factor's, so the `K = -0.01` factor
operates deep in its small-`t` regime, where its bridge has barely concentrated.

## Hypothesis

1. **The product is a valid ELBO**: `wnelbo_ref >= H(p)` in every trained cell, landing
   on `H(p)` from above at the best rate (`H(naive_ps) = 0.5003`,
   `H(cmplx_ps) = 1.6664`, `H(c1e3) = H(c1e4) = 1.0407` nats).
2. **The product behaves like its sharpest factor, not its flattest.** Because the heat
   ceiling collapses to 9.7, the estimator should look like the `K = -10` single-factor
   cells — well-conditioned under the pinned `exp(0.1)` reference — and **not** like the
   `K = -0.01` cells, which the pilot shows reporting far below `H(p)`. If instead the
   product inherits the flat factor's pathology, the ceiling is not the operative
   mechanism and the hypothesis is wrong.
3. **Three factors identify the word sooner than one.** Nine direction components carry
   more information per unit `t` than three, so `wce_ref` / `ce_ref` should sit below the
   single-factor `d = 3` cells at matched `ps`, while `wnelbo_ref` stays pinned at `H(p)`.

### Pilot evidence — not yet a result

200-step, 409 600-sample cells (RTX 6000 Ada, 2026-09-06; scratchpad, not checked in):

| cell | `wnelbo_ref` | `wce_ref` |
|---|---|---|
| product, `naive_ps`, PP | 0.5935 | 0.073 |
| single `K = -1`, `naive_ps`, CE | 0.5096 | 0.703 |
| single `K = -0.01`, `naive_ps`, PP | 0.2210 | 63.3 |

The product sits **above** `H(naive_ps) = 0.5003` and its `wce_ref` is an order of
magnitude below the single-factor cells' — consistent with (2) and (3), from runs far too
short to be evidence about the optimum.

## Design

Grid from `setup.md`: 4 × 7 × 2 × 3 = **168 runs**, one SLURM job each.

| variable | values |
|---|---|
| `ps` | `naive_ps`, `cmplx_ps`, `c1e3_exp1.0`, `c1e4_exp1.0` |
| `loss_geometry` | `cross_entropy`, `poincare_polar` |
| `loss_proposal_exp_rate` | 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0 |
| `seed` | 0, 1, 2 |

Fixed: `mode=tnb`, `prod_factor_dim=[3,3,3]`,
`prod_factor_gaussian_curvature=[-0.01,-10.0,-1.0]`, `lr=1e-3`, `max_steps=20000`,
`gradient_clip_val=1.0`, `test_size=4e6`, `batch_size=2048`,
`ref_proposal_type=exp`, `ref_proposal_exp_rate=0.1`.

The geometry is fixed, so it lives in the **project name** and `run_name` carries no
`_k-` field — byte-identical to `init_test`'s scheme, and `experiments/report.py` parses
it unchanged.

`setup.md`'s result templates carry the four-step layout inherited from `init_test`; its
Training section pins `max_steps` to **{20000}**, which is what is run.

Caution carried over from `dev_log/sep05_2026/numerics.md` §"run_name collides": the
config's `run_name` template interpolates `${hyper_dim}` / `${gaussian_curvature}`, both
ignored under a product geometry, so two different product configs resolve to the same
default folder. The sweep sets `folder` explicitly for every cell, so that trap is not
reachable here — but any ad-hoc run of `main_refactor.py` on a product manifold hits it.

## GPU allocation

Both owned partitions (`--partition=thickstun,desa`), 1 GPU / 2 CPUs / 16 GB per job.

Measured at batch 2048 on an RTX 6000 Ada, `D = 9`:

| `ps` | V | s/step (incl. val + ref pass) | 4M test pass | peak GiB (ce) | peak GiB (pp) |
|---|---|---|---|---|---|
| `naive_ps` / `cmplx_ps` | 10 | 0.040 | 35 s | 0.87 | 0.87 |
| `c1e3_exp1.0` | 1 000 | 0.045 | 50 s | — | 3.01 |
| `c1e4_exp1.0` | 10 000 | 0.290 | 160 s | 17.86 | **25.34** |

**Sizing must use the `poincare_polar` column.** `pp` runs the ELBO geometry on the loss
pass *and* the reference pass; `cross_entropy` runs it only on the reference. The gap is
7.5 GiB at `c1e4`, and sizing on the `ce` measurement is exactly what cost two cells: two
`c1e4` × `pp` jobs OOM'd on `kuleshov-compute-03`'s 24 GB A5000 at 23.5 GiB (in
`horosphere_geometry`, `cos_half_sq = sums.square().sum(-1) / 4`) before the model was
corrected.

`c1e4` at `D = 9` is the **only** cell in the four projects that does not fit every node:
25.34 GiB × 1.15 clears both `desa-compute-01` (10.5 GiB) and `kuleshov-compute-03`
(24 GiB), so it runs only on the two 48 GB nodes and carries the extra `--nice` penalty
that keeps it from gate-keeping hardware it can never use. Everything else is eligible
everywhere — including `c1e4` at `D = 3` under `pp`, which polls 10.5 GiB on a 48 GB card
but has completed on `desa-compute-01`'s 11 GB cards 11 times, i.e. that poll reads the
caching allocator's reservation, not the requirement.

Per-cell `--time` is the budgeted rate scaled to the slowest *eligible* node (the loss is
float64-bound, so the node spread follows fp64 throughput: 1.0 / 2.5 / 3.5 / 4.5 for the
Ada / A6000 / A5000 / 2080 Ti) with a 1.5× margin: ~1 h 35 for V ≤ 1000, ~6 h 14 for
`c1e4` (whose slowest eligible node is the A6000, not the A5000).

## Wall clock (expected)

~**103 GPU-h** at the Ada rate for the full grid, of which `c1e4` is ~68 GPU-h; two to
three times that if the cells land on the slower cards. Idempotent and resumable, so it
fills in over a day or two rather than in one sitting.

## Reporting

- `python experiments/report.py init_test_3x3d_refactor_new` → `RESULTS.md`.
- Read against `experiments/init_opt_test_3x3d_refactor_new/RESULTS.md` (same geometry,
  exact posterior — is the estimator sound here?) and against
  `experiments/init_test_3d_refactor_new/RESULTS.md` (same three curvatures, one at a
  time instead of all at once).
