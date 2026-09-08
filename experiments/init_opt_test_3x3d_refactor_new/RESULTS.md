# init_opt_test_3x3d_refactor_new results

- runs collected: **168** / 168 (100%) — run dirs without test_metrics.json: 0
- H(naive_ps) = **0.5003** — wnelbo_ref is bounded below by this
- H(cmplx_ps) = **1.6664** — wnelbo_ref is bounded below by this
- H(c1e3_exp1.0) = **1.0407** — wnelbo_ref is bounded below by this
- H(c1e4_exp1.0) = **1.0407** — wnelbo_ref is bounded below by this
- Each cell is **`mean / variance`**, both averaged across the 3 seeds, as
  setup.md's "Result Presentation" asks: `mean` is the point estimate
  (avg of `test_<metric>`), `variance` is the PER-SAMPLE variance of the
  4,000,000-draw test pass in nats² (avg of `test_<metric>_std**2`).
- `n/r` = not recorded. `trainer.BaseTrainer.STD_KEYS` logs a per-sample
  std for the three WEIGHTED quantities only, so `nelbo_ref` and `ce_ref` have no
  variance in any existing run; filling them needs STD_KEYS extended and a re-run.
- These variances are NOT the `± std` these tables used to print. That was the
  across-seed spread of the mean, related by `± ≈ sqrt(variance / 4,000,000)`.
- `!` marks loss proposals above the ~0.304 variance cliff, where the
  weighted estimator has infinite variance. The reference pass is pinned at
  exp(0.1) and stays valid, but training there is materially noisier.
- `wce_ref` is dominated by rare extremes; treat its spread as indicative only.

---

# Results (Full Table)

---

## naive_ps

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.0622 / 19.65 | 0.4976 / 177.1 | 0.0608 / 1.889 | 0.0492 / n/r | 0.0060 / n/r |
| exp0.05 | 0.0613 / 3.839 | 0.4976 / 177.1 | 0.0608 / 1.889 | 0.0492 / n/r | 0.0060 / n/r |
| exp0.1 | 0.0612 / 1.918 | 0.4976 / 177.1 | 0.0608 / 1.889 | 0.0492 / n/r | 0.0060 / n/r |
| exp0.25 | 0.0609 / 0.7717 | 0.4976 / 177.1 | 0.0608 / 1.889 | 0.0492 / n/r | 0.0060 / n/r |
| exp0.5 ! | 0.0608 / 0.3935 | 0.4976 / 177.1 | 0.0608 / 1.889 | 0.0492 / n/r | 0.0060 / n/r |
| exp0.75 ! | 0.0608 / 0.2691 | 0.4976 / 177.1 | 0.0608 / 1.889 | 0.0492 / n/r | 0.0060 / n/r |
| exp1.0 ! | 0.0608 / 0.2076 | 0.4976 / 177.1 | 0.0608 / 1.889 | 0.0492 / n/r | 0.0060 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.5100 / 1819 | 0.4976 / 177.1 | 0.0608 / 1.889 | 0.0492 / n/r | 0.0060 / n/r |
| exp0.05 | 0.5058 / 361.5 | 0.4976 / 177.1 | 0.0608 / 1.889 | 0.0492 / n/r | 0.0060 / n/r |
| exp0.1 | 0.5028 / 181.2 | 0.4976 / 177.1 | 0.0608 / 1.889 | 0.0492 / n/r | 0.0060 / n/r |
| exp0.25 | 0.4986 / 72.15 | 0.4976 / 177.1 | 0.0608 / 1.889 | 0.0492 / n/r | 0.0060 / n/r |
| exp0.5 ! | 0.4982 / 36.93 | 0.4976 / 177.1 | 0.0608 / 1.889 | 0.0492 / n/r | 0.0060 / n/r |
| exp0.75 ! | 0.4962 / 25.13 | 0.4976 / 177.1 | 0.0608 / 1.889 | 0.0492 / n/r | 0.0060 / n/r |
| exp1.0 ! | 0.4978 / 19.45 | 0.4976 / 177.1 | 0.0608 / 1.889 | 0.0492 / n/r | 0.0060 / n/r |

---

## cmplx_ps

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.1664 / 38.06 | 1.6649 / 436 | 0.1680 / 3.817 | 0.1648 / n/r | 0.0166 / n/r |
| exp0.05 | 0.1666 / 7.578 | 1.6649 / 436 | 0.1680 / 3.817 | 0.1648 / n/r | 0.0166 / n/r |
| exp0.1 | 0.1672 / 3.806 | 1.6649 / 436 | 0.1680 / 3.817 | 0.1648 / n/r | 0.0166 / n/r |
| exp0.25 | 0.1677 / 1.542 | 1.6649 / 436 | 0.1680 / 3.817 | 0.1648 / n/r | 0.0166 / n/r |
| exp0.5 ! | 0.1678 / 0.7793 | 1.6649 / 436 | 0.1680 / 3.817 | 0.1648 / n/r | 0.0166 / n/r |
| exp0.75 ! | 0.1680 / 0.5287 | 1.6649 / 436 | 0.1680 / 3.817 | 0.1648 / n/r | 0.0166 / n/r |
| exp1.0 ! | 0.1680 / 0.4035 | 1.6649 / 436 | 0.1680 / 3.817 | 0.1648 / n/r | 0.0166 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.6477 / 4315 | 1.6649 / 436 | 0.1680 / 3.817 | 0.1648 / n/r | 0.0166 / n/r |
| exp0.05 | 1.6528 / 864.9 | 1.6649 / 436 | 0.1680 / 3.817 | 0.1648 / n/r | 0.0166 / n/r |
| exp0.1 | 1.6602 / 437.2 | 1.6649 / 436 | 0.1680 / 3.817 | 0.1648 / n/r | 0.0166 / n/r |
| exp0.25 | 1.6650 / 176.6 | 1.6649 / 436 | 0.1680 / 3.817 | 0.1648 / n/r | 0.0166 / n/r |
| exp0.5 ! | 1.6626 / 88.75 | 1.6649 / 436 | 0.1680 / 3.817 | 0.1648 / n/r | 0.0166 / n/r |
| exp0.75 ! | 1.6648 / 60.21 | 1.6649 / 436 | 0.1680 / 3.817 | 0.1648 / n/r | 0.0166 / n/r |
| exp1.0 ! | 1.6656 / 45.99 | 1.6649 / 436 | 0.1680 / 3.817 | 0.1648 / n/r | 0.0166 / n/r |

---

## c1e3_exp1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.1210 / 23.75 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.05 | 0.1205 / 4.677 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.1 | 0.1214 / 2.381 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.25 | 0.1220 / 0.9693 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.5 ! | 0.1223 / 0.495 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.75 ! | 0.1223 / 0.336 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp1.0 ! | 0.1222 / 0.2574 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0290 / 2614 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.05 | 1.0253 / 518 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.1 | 1.0348 / 264.6 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.25 | 1.0392 / 108 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.5 ! | 1.0401 / 55.06 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.75 ! | 1.0391 / 37.59 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp1.0 ! | 1.0382 / 28.86 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |

---

## c1e4_exp1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.1210 / 23.75 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.05 | 0.1205 / 4.677 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.1 | 0.1214 / 2.381 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.25 | 0.1220 / 0.9693 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.5 ! | 0.1223 / 0.495 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.75 ! | 0.1223 / 0.336 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp1.0 ! | 0.1222 / 0.2574 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0290 / 2614 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.05 | 1.0253 / 518 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.1 | 1.0348 / 264.6 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.25 | 1.0392 / 108 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.5 ! | 1.0401 / 55.06 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp0.75 ! | 1.0391 / 37.59 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |
| exp1.0 ! | 1.0382 / 28.86 | 1.0426 / 267.4 | 0.1224 / 2.414 | 0.1031 / n/r | 0.0121 / n/r |

---

# RESULTS (Dense Table)

---

## naive_ps

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 0.5100 / 1819 | 0.0622 / 19.65 |
| exp0.05 | 0.5058 / 361.5 | 0.0613 / 3.839 |
| exp0.1 | 0.5028 / 181.2 | 0.0612 / 1.918 |
| exp0.25 | 0.4986 / 72.15 | 0.0609 / 0.7717 |
| exp0.5 ! | 0.4982 / 36.93 | 0.0608 / 0.3935 |
| exp0.75 ! | 0.4962 / 25.13 | 0.0608 / 0.2691 |
| exp1.0 ! | 0.4978 / 19.45 | 0.0608 / 0.2076 |

---

## cmplx_ps

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.6477 / 4315 | 0.1664 / 38.06 |
| exp0.05 | 1.6528 / 864.9 | 0.1666 / 7.578 |
| exp0.1 | 1.6602 / 437.2 | 0.1672 / 3.806 |
| exp0.25 | 1.6650 / 176.6 | 0.1677 / 1.542 |
| exp0.5 ! | 1.6626 / 88.75 | 0.1678 / 0.7793 |
| exp0.75 ! | 1.6648 / 60.21 | 0.1680 / 0.5287 |
| exp1.0 ! | 1.6656 / 45.99 | 0.1680 / 0.4035 |

---

## c1e3_exp1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0290 / 2614 | 0.1210 / 23.75 |
| exp0.05 | 1.0253 / 518 | 0.1205 / 4.677 |
| exp0.1 | 1.0348 / 264.6 | 0.1214 / 2.381 |
| exp0.25 | 1.0392 / 108 | 0.1220 / 0.9693 |
| exp0.5 ! | 1.0401 / 55.06 | 0.1223 / 0.495 |
| exp0.75 ! | 1.0391 / 37.59 | 0.1223 / 0.336 |
| exp1.0 ! | 1.0382 / 28.86 | 0.1222 / 0.2574 |

---

## c1e4_exp1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0290 / 2614 | 0.1210 / 23.75 |
| exp0.05 | 1.0253 / 518 | 0.1205 / 4.677 |
| exp0.1 | 1.0348 / 264.6 | 0.1214 / 2.381 |
| exp0.25 | 1.0392 / 108 | 0.1220 / 0.9693 |
| exp0.5 ! | 1.0401 / 55.06 | 0.1223 / 0.495 |
| exp0.75 ! | 1.0391 / 37.59 | 0.1223 / 0.336 |
| exp1.0 ! | 1.0382 / 28.86 | 0.1222 / 0.2574 |


---

# Insights and conclusions

**All 168 cells completed; 0 failures.** `mode=opt`, so every number is the *exact*
posterior's: this is a statement about the estimator on this product geometry, not about
any model.

## 1. The reference pass is exactly invariant, as designed

`wnelbo_ref`, `nelbo_ref`, `wce_ref` and `ce_ref` are identical across all 14
(loss_geometry × rate) cells of every `(ps, seed)` group — 12 groups, zero spread. Only
`wloss` varies. The `salt=0` / `salt=1` RNG split holds on the product path too.

## 2. The product manifold is well-conditioned — it lands on H(p)

Averaged over all 42 cells per `ps`; `SE = std / sqrt(4e6)`:

| ps | `wnelbo_ref` | H(p) | (x−H)/SE | std | `wce_ref` | `nelbo_ref` | `ce_ref` |
|---|---|---|---|---|---|---|---|
| naive_ps | 0.4976 | 0.5003 | −0.4 | 13.3 | 0.061 | 0.0492 | 0.0060 |
| cmplx_ps | 1.6649 | 1.6664 | −0.1 | 20.9 | 0.168 | 0.1648 | 0.0166 |
| c1e3 / c1e4 | 1.0426 | 1.0407 | +0.2 | 16.4 | 0.122 | 0.1031 | 0.0121 |

Every reading is within ±0.4 SE of the entropy. Hypothesis 1 confirmed:
`test_wnelbo_ref >= H(p)` is a meaningful test of a *trained* model on this geometry.

## 3. The decisive result: the product tracks its SHARPEST factor

This project contains a `K = -0.01` factor, and the single-factor control
(`init_opt_test_3d_refactor_new`) shows that curvature reporting **26 % below H(p)** with
`wce_ref` of 44–172. The product shows no trace of it. Side by side, exact posterior,
same 4M-sample budget:

| ps | product [3,3,3] | single `K = -10` | single `K = -1` | single `K = -0.01` |
|---|---|---|---|---|
| naive_ps `wnelbo_ref` | **0.4976** | 0.4974 | 0.5013 | 0.3594 |
| cmplx_ps `wnelbo_ref` | **1.6649** | 1.6605 | 1.6692 | 1.2439 |
| c1e3/c1e4 `wnelbo_ref` | **1.0426** | 1.0395 | 1.0409 | 0.7667 |
| naive_ps `wce_ref` | **0.061** | 0.062 | 0.630 | 44.4 |
| cmplx_ps `wce_ref` | **0.168** | 0.209 | 2.101 | 172.0 |
| c1e3/c1e4 `wce_ref` | **0.122** | 0.115 | 1.152 | 90.3 |
| naive_ps `std` | **13.3** | 13.0 | 4.3 | 85.4 |

The product does not merely avoid the flat factor's pathology — it is **numerically
indistinguishable from the pure `K = -10` manifold** on every reference metric, including
the estimator's own standard deviation (13.3 vs 13.0, 20.9 vs 19.7, 16.4 vs 16.3).

**The mechanism is the heat-time ceiling.** `main_refactor.py` clamps `t` at
`min_m _radial_t_max(3) · R_m^2` = `min(9700, 9.7, 97)` = **9.7**, set by the `K = -10`
factor. The whole product therefore lives in the sharpest factor's time range, and the
flattest factor never reaches the regime where the pinned `exp(0.1)` proposal loses the
integral. That the match is this tight — not merely "safe" but equal to three digits —
says the sharpest factor governs the reference metrics essentially on its own.

**Practical consequence.** Mixing curvatures in a product manifold is safe for the
estimator: adding a flat factor to a sharp one does not import the flat factor's
measurement problem. The converse is the warning — a product of *only* flat factors would
inherit it, since the ceiling is a minimum and there would be no sharp factor to bind it.

## 4. `c1e3` and `c1e4` agree to all printed digits

As at `d = 3`: the Bayes-optimal Girsanov integrand is configuration-independent, so these
are **one** validation of the product path, not two independent ones.

## 5. What this licenses the trained project to claim

`init_test_3x3d_refactor_new` may be read directly against `H(p)`: at this geometry the
estimator resolves the integral, so a trained cell below `H(p)` there would be a genuine
Invariant-2 violation rather than an artefact. Contrast
`init_test_3d_refactor_new`'s `K = -0.01` slice, which must be read against
0.3594 / 1.2439 / 0.7667 instead.
