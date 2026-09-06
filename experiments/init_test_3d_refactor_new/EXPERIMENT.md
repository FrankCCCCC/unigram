# init_test_3d_refactor_new — trained model on `H^3_K`, curvature swept

First sweep of **Gaussian curvature** as an experimental variable. `main_refactor.py`
(the product-manifold trainer: `MLPLMRefactor` / `OptimalModelRefactor`,
`Loss.weighted_loss_refactor`, `HyperbolicHeatKernel.poincare_bridge_prod`) is run on a
single factor `H^3_K` at `K ∈ {-1.0, -10.0, -0.01}`.

Three sibling projects share the design:

| project | model | geometry |
|---|---|---|
| **`init_test_3d_refactor_new`** (this) | trained `MLPLMRefactor` | `H^3_K`, `K` swept |
| `init_opt_test_3d_refactor_new` | Bayes-optimal, no fit | `H^3_K`, `K` swept |
| `init_test_3x3d_refactor_new` | trained | `H^3_{-0.01} × H^3_{-10} × H^3_{-1}` |
| `init_opt_test_3x3d_refactor_new` | Bayes-optimal, no fit | same product |

## Why curvature is not a cosmetic rescaling

`K` fixes the radius `R = 1/sqrt(-K)`, and three things move with it:

1. **The heat-time ceiling.** `main_refactor.py` clamps `t` at
   `min_m _radial_t_max(d_m) · R_m^2`. At `d = 3`, `_radial_t_max = 97`, so the ceiling is
   **9.7** at `K = -10`, **97** at `K = -1` and **9700** at `K = -0.01`. The shipped
   proposal reaches `t = 1e5`, so every curvature clamps — but by wildly different factors.
2. **How fast the per-`t` loss decays.** The bridge's angular concentration is
   `1 - alpha ~ e^{-2u}` in the *dimensionless* `u = rho / R`, so at `K = -0.01` the
   integrand needs ~`R^2 = 100`× more physical time to reach the same concentration.
3. **The importance-weighted estimator's variance.** The reference proposal stays pinned
   at `exp(0.1)` for every cell — that is what makes `wnelbo_ref` comparable across the
   rate axis — but the ~0.304 variance cliff was measured at `K = -1` (`L(t) ~ e^{-0.152 t}`).
   Scaling the decay by `1/R^2` moves the cliff to ~0.00304 at `K = -0.01`, i.e. the pinned
   reference proposal sits **32× above** it.

Point 3 is the reason the `mode=opt` twin exists: it is what separates "the trained model
is bad at this curvature" from "the estimator cannot measure this curvature".

## Hypothesis

1. **`K = -1` reproduces `init_refactor_3d`.** Same `d = 3`, same grid, and the refactored
   trainer differs only in the horosphere readout convention, so the `K = -1` slice should
   land on `H(p)` from above like the `init_refactor_3d` cells do
   (`H(naive_ps) = 0.5003`, `H(cmplx_ps) = 1.6664`, `H(c1e3) = H(c1e4) = 1.0407` nats).
2. **`K = -10` is safe, `K = -0.01` is not.** Sharper curvature compresses `t`, so the
   pinned `exp(0.1)` reference stays far below its (now larger) variance cliff. At
   `K = -0.01` the estimator should under-report: `wnelbo_ref` below `H(p)`, with a large
   `wnelbo_ref_std` and a `wce_ref` dominated by rare extremes.
3. **Where the estimator is valid, curvature does not change the optimum.** `wnelbo_ref`
   at the best rate should sit on `H(p)` at both `K = -1` and `K = -10`: the ELBO is a
   property of the target distribution, not of the manifold it is embedded in.

### Pilot evidence for (2) — not yet a result

A 9-cell pilot (200 train steps, 409 600 test samples, RTX 6000 Ada, 2026-09-06;
scratchpad, not checked in) already shows the shape:

| cell | `wnelbo_ref` | `wnelbo_ref_std` | `wce_ref` |
|---|---|---|---|
| `K = -1`, `naive_ps`, CE | 0.5096 | 4.25 | 0.70 |
| `K = -10`, `naive_ps`, PP | 0.5018 | 12.83 | 0.09 |
| **`K = -0.01`, `naive_ps`, PP** | **0.2210** | 11.00 | **63.3** |

`H(naive_ps) = 0.5003`. The `K = -0.01` cell is ~16 standard errors *below* the entropy
and its weighted CE is 90× the others' — the signature of an integrand whose mass sits
where the proposal never samples. These are 200-step runs, so they say nothing about the
trained optimum; they are here only to state what the full grid is expected to confirm.

## Design

Grid from `setup.md`: 4 × 3 × 7 × 2 × 3 = **504 runs**, one SLURM job each.

| variable | values |
|---|---|
| `ps` | `naive_ps`, `cmplx_ps`, `c1e3_exp1.0`, `c1e4_exp1.0` |
| `gaussian_curvature` | -1.0, -10.0, -0.01 |
| `loss_geometry` | `cross_entropy`, `poincare_polar` |
| `loss_proposal_exp_rate` | 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0 |
| `seed` | 0, 1, 2 |

Fixed: `mode=tnb`, `hyper_dim=3`, `lr=1e-3`, `max_steps=20000`,
`gradient_clip_val=1.0`, `test_size=4e6`, `batch_size=2048`,
`ref_proposal_type=exp`, `ref_proposal_exp_rate=0.1`.

`setup.md`'s result templates carry the four-step layout inherited from `init_test`
(20000 / 40000 / 100000 / 200000), but its Training section pins `max_steps` to
**{20000}**. The single-step reading is authoritative here: only the 20000-step
tables are filled, and the section headings collapse to `## {ps}, K = {K}`.

`run_name` adds one field to the `init_test` scheme —
`ps-{ps}_k-{K}_lg-{geom}_q-exp{rate}_qref-exp0.1_lr0.001_st20000_s{seed}`. The `_k-`
field is optional in `experiments/report.py`'s parser, so the fixed-geometry projects
and every pre-existing project keep parsing byte-identically (verified: regenerating
`init_refactor_3d/RESULTS.md` is a no-op diff).

## What changed in the code to run this

- `script/train/{ce_redactor,pp_refactor}.sh`: new `CURVATURE`, `PROD_DIM`,
  `PROD_CURVATURE` env knobs, passed to hydra as `gaussian_curvature=`,
  `prod_factor_dim=`, `prod_factor_gaussian_curvature=`. Defaults (`-1.0`, `null`,
  `null`) reproduce the previous behaviour exactly.
- `experiments/sweep_lib.py`: the submission machinery shared by all four projects,
  which differ only in `(mode, geometry)`.
- `experiments/report.py`: `_k-<K>` is an optional field in `RUN_RE`, and sections are
  keyed `(ps, K, steps)` instead of `(ps, steps)`.

## GPU allocation

Both owned partitions (`--partition=thickstun,desa`), 1 GPU / 2 CPUs / 16 GB per job.
2 CPUs, not 4: the pilot's `TotalCPU ≈ Elapsed` says the work is one GPU-bound thread
(`num_workers=0`), and the GPU-rich nodes are CPU-poor.

Measured at batch 2048 on an RTX 6000 Ada (`D = sum(prod_factor_dim) = 3` here):

| `ps` | V | s/step (incl. val + ref pass) | 4M test pass | peak GiB (ce) | peak GiB (pp) |
|---|---|---|---|---|---|
| `naive_ps` / `cmplx_ps` | 10 | 0.020 | 30 s | 0.85 | 0.85 |
| `c1e3_exp1.0` | 1 000 | 0.020 | 40 s | 1.27 | — |
| `c1e4_exp1.0` | 10 000 | 0.105 | 60 s | 7.93 | 10.53 |

`poincare_polar` peaks above `cross_entropy` because it runs the ELBO geometry on the
loss pass as well as the reference pass. At `D = 9` that gap decides node eligibility
(see the sibling project); at `D = 3` it does not — **every cell fits all four nodes**.
The `c1e4` × `pp` poll of 10.53 GiB on a 48 GB card sits right at `desa-compute-01`'s
10.5 GiB usable, but 11 such cells have completed there, so that reading is the caching
allocator's reservation rather than the requirement.

Per-cell `--time` is the budgeted rate scaled to the slowest *eligible* node (the loss is
float64-bound, so the node spread follows fp64 throughput: 1.0 / 2.5 / 3.5 / 4.5 for the
Ada / A6000 / A5000 / 2080 Ti) with a 1.5× margin: ~49 min for V ≤ 1000, ~4 h 04 for
`c1e4`. Calibrating on the fastest node instead would have killed every `naive_ps` cell
that landed on the 2080 Ti — caught on a validation cell before the grid went out.

`--nice` orders the queue: seed 0 at 0 (+10/+30 for the larger vocabularies) so a
complete single-seed grid lands first, replicates at +100.

## Wall clock (expected)

~**130 GPU-h** for the full grid (`c1e4` is 70% of it). Against the ~10–25 GPUs
typically free on the two partitions, roughly a day. The sweep is idempotent and
resumable — a cell with `test_metrics.json` or a live `squeue` entry is skipped — so
partial progress costs nothing.

## Reporting

- `python experiments/report.py init_test_3d_refactor_new` → `RESULTS.md`
  (one `## {ps}, K = {K}` section per curvature, CE and Polar-ELBO tables in each).
- Read against `experiments/init_opt_test_3d_refactor_new/RESULTS.md` cell-for-cell:
  that project is the estimator's own reading at the same curvature.
- Read against `experiments/init_refactor_3d/RESULTS.md` for the `K = -1`,
  20000-step slice (`main.py` vs `main_refactor.py` at the same geometry).
