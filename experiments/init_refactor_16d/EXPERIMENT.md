# init_refactor_16d — `init_test`'s grid on the general-d bridge, `hyper_dim = 16`

First run of the arbitrary-dimension bridge (`HyperBridge.bridge` /
`Loss.weighted_loss`, the `claude/init-refactor-nd` branch) at a dimension the
binary code path cannot reach. One of three sibling projects — `init_refactor_16d`,
`init_refactor_9d`, `init_refactor_16d` — that differ only in `hyper_dim`.

## Hypothesis

1. **The general-d path is a valid ELBO at d = 16.** `test_wnelbo_ref >= H(p)` in
   every trained cell (`H(naive_ps) = 0.5003`, `H(cmplx_ps) = 1.6664` nats), and the
   best cells land on it from above, as the d = 2 `init_test` cells do. Pre-check
   (Bayes-optimal model, `mode=opt`, `cmplx_ps`, 1M test samples, 2080 Ti, with
   the tabulated sampler below): `wnelbo_ref = 1.7336 ± 0.0449` — on `H(p)` within 1.5 SE.
2. **The d = 2 findings carry over**: `cross_entropy` and `poincare_polar` training
   both reach `H(p)`, the `exp` rate sweet spot stays at or below the ~0.304
   variance cliff, and more steps help the `poincare_polar` cells more than the CE
   cells.
3. **Across the siblings** (3 → 9 → 16), the bridge identifies the word sooner in
   `t` (drift `(d-1)/2`), so `wce_ref` shrinks with d while the ELBO stays pinned
   at `H(p)`; the importance-weighted estimator's standard deviation grows with d
   (measured at the Bayes model: `wnelbo_ref_std` 6.5 → 23 → 29 for d = 3 → 9 → 11).

## The even-d radial sampler had to be tabulated

`HyperbolicHeatKernel.sample_radial` seeds the even-d Millson recurrence from the
McKean `p_2` integral — a `(B, ngrid=2000, nu=1024)` float64 quadrature per call.
Measured on the 2080 Ti at `B = 2048`: **3.3 s per `bridge()` call** for d = 2 and
d = 16, vs 5–9 ms for d = 3 / 9. Two calls per step (loss + reference path) is ~7
s/step — a 200k-step cell would take ~16 days — so d = 16 was not runnable as is.

The radial law depends on `t` alone, so `HyperBridge.sample_radial_tabulated`
tabulates its quantile function once per `(d, device)` from `sample_radial`'s own
CDF (`radial_cdf`, the exact code path, now split out of `sample_radial`) on a
log-`t` grid — 64 rows per decade over `[1e-12, _radial_t_max(d)]`, 8192 `u`
nodes, rows stored as `x = rho / sqrt(t)` — and samples by bilinear interpolation
in `(log t, u)`. `bridge()` uses it for even d only; odd d keep the direct sampler.

Validation (2080 Ti, `validate_table.py`; KS = max CDF gap between 2^16 samples):

| d | t | exact mean / std | table mean / std | KS |
|---|---|---|---|---|
| 2 | 1e-6 | 0.0013 / 0.0007 | 0.0013 / 0.0007 | 0.0064 |
| 2 | 0.01 | 0.1254 / 0.0660 | 0.1258 / 0.0658 | 0.0081 |
| 2 | 0.1 | 0.4001 / 0.2088 | 0.3991 / 0.2088 | 0.0062 |
| 2 | 1 | 1.3544 / 0.7000 | 1.3480 / 0.7049 | 0.0084 |
| 2 | 10 | 6.3338 / 2.7256 | 6.3420 / 2.7425 | 0.0037 |
| 2 | 50 | 26.359 / 6.855 | 26.343 / 6.887 | 0.0045 |
| 2 | 395 (t_max) | 198.55 / 19.83 | 198.55 / 19.76 | 0.0046 |
| 2 | exp(0.1) batch | 6.317 / 5.957 | 6.287 / 5.906 | 0.0042 |
| 16 | 1e-6 | 0.0040 / 0.0008 | 0.0040 / 0.0008 | 0.0087 |
| 16 | 0.01 | 0.3989 / 0.0715 | 0.3992 / 0.0714 | 0.0055 |
| 16 | 0.1 | 1.4042 / 0.2466 | 1.4062 / 0.2480 | 0.0056 |
| 16 | 0.3 | 2.9732 / 0.4795 | 2.9670 / 0.4826 | 0.0089 |
| 16 | 1 | 8.2316 / 0.9605 | 8.2293 / 0.9630 | 0.0070 |
| 16 | 1.51 (t_max) | 12.052 / 1.206 | 12.057 / 1.196 | 0.0063 |
| 16 | exp(0.1) batch | 11.266 / 2.607 | 11.268 / 2.608 | 0.0054 |

Every KS sits at the two-sample noise floor (0.0106 at 95% for 2^15 vs 2^15
draws). At d = 2 the table is also as close to the closed-form Gruet sampler as
the exact sampler is (KS 0.004–0.015 for both). At t = 1e-6 the d = 16 mean equals
the Euclidean limit sqrt(t) E[chi_16] = 0.0039. `bridge()` at B = 2048:
3.3 s → 0.6 ms for both d = 2 and d = 16 (table build: 0.6–1.1 s, once).
Bayes-optimal ELBO through the table: d = 2 `1.6741 ± 0.0066`, d = 16
`1.7336 ± 0.0449` (H = 1.6664) — on `H(p)` within 1.2 / 1.5 SE; the weighted
estimator's std grows from 6.6 at d = 2 to 45 at d = 16.

## What changed in the code to run this

- `geo_bridge.py`: `sample_radial` split into `radial_cdf` + `_radial_inverse_cdf`
  (same RNG call order; bit-identical samples).
- `loss.py`: `HyperBridge.sample_radial_tabulated` + `_radial_quantile_table`;
  `bridge()` dispatches on `d % 2`.

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

Fixed: `hyper_dim=16`, `lr=1e-3`, `gradient_clip_val=1.0`, `test_size=4e6`,
`batch_size=2048`, `ref_proposal_type=exp`, `ref_proposal_exp_rate=0.1`.

`run_name` is byte-identical to `init_test`'s (the dimension is carried by the
project name), so `experiments/report.py init_refactor_16d` works unchanged and the
cells pair 1:1 with `init_test` for a d = 2 vs d = 16 comparison.

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

Pilot on an A5000: 500 steps + 100 test batches in 24–30 s for d = 16 (the tabulated even-d radial
sampler costs 0.6 ms per `bridge()` call after a one-off 0.6 s table build), 4M-sample test ≈ 80 s. Per
(ps, rate, geometry, seed) column: 360k steps ≈ 4.5 h → **~390 GPU-h** per
project. With the ~10 GPUs free at submission (the rest hold the user's `simpflm`
jobs and other users' work) that is ~1.5–2 days per project; faster as GPUs free up.

## Reporting

- `python experiments/report.py init_refactor_16d` → `RESULTS.md`.
- Cross-dimension comparison: the same command for `_9d` / `_16d`, plus
  `experiments/init_test/RESULTS.md` for d = 2.
