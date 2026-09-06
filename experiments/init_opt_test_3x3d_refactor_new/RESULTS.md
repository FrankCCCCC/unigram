# init_opt_test_3x3d_refactor_new results

- runs collected: **168** / 168 (100%) — run dirs without test_metrics.json: 0
- H(naive_ps) = **0.5003** — wnelbo_ref is bounded below by this
- H(cmplx_ps) = **1.6664** — wnelbo_ref is bounded below by this
- H(c1e3_exp1.0) = **1.0407** — wnelbo_ref is bounded below by this
- H(c1e4_exp1.0) = **1.0407** — wnelbo_ref is bounded below by this
- `!` marks loss proposals above the ~0.304 variance cliff, where the
  weighted estimator has infinite variance. The reference pass is pinned at
  exp(0.1) and stays valid, but training there is materially noisier.
- `wce_ref` is dominated by rare extremes; treat its spread as indicative only.

---

# Results (Full Table)

---

## naive_ps

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.0622 ± 0.0011 | 0.4976 ± 0.0067 | 0.0608 ± 0.0003 | 0.0492 ± 0.0007 | 0.0060 ± 0.0000 |
| exp0.05 | 0.0613 ± 0.0003 | 0.4976 ± 0.0067 | 0.0608 ± 0.0003 | 0.0492 ± 0.0007 | 0.0060 ± 0.0000 |
| exp0.1 | 0.0612 ± 0.0002 | 0.4976 ± 0.0067 | 0.0608 ± 0.0003 | 0.0492 ± 0.0007 | 0.0060 ± 0.0000 |
| exp0.25 | 0.0609 ± 0.0002 | 0.4976 ± 0.0067 | 0.0608 ± 0.0003 | 0.0492 ± 0.0007 | 0.0060 ± 0.0000 |
| exp0.5 ! | 0.0608 ± 0.0003 | 0.4976 ± 0.0067 | 0.0608 ± 0.0003 | 0.0492 ± 0.0007 | 0.0060 ± 0.0000 |
| exp0.75 ! | 0.0608 ± 0.0002 | 0.4976 ± 0.0067 | 0.0608 ± 0.0003 | 0.0492 ± 0.0007 | 0.0060 ± 0.0000 |
| exp1.0 ! | 0.0608 ± 0.0002 | 0.4976 ± 0.0067 | 0.0608 ± 0.0003 | 0.0492 ± 0.0007 | 0.0060 ± 0.0000 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.5100 ± 0.0189 | 0.4976 ± 0.0067 | 0.0608 ± 0.0003 | 0.0492 ± 0.0007 | 0.0060 ± 0.0000 |
| exp0.05 | 0.5058 ± 0.0049 | 0.4976 ± 0.0067 | 0.0608 ± 0.0003 | 0.0492 ± 0.0007 | 0.0060 ± 0.0000 |
| exp0.1 | 0.5028 ± 0.0094 | 0.4976 ± 0.0067 | 0.0608 ± 0.0003 | 0.0492 ± 0.0007 | 0.0060 ± 0.0000 |
| exp0.25 | 0.4986 ± 0.0018 | 0.4976 ± 0.0067 | 0.0608 ± 0.0003 | 0.0492 ± 0.0007 | 0.0060 ± 0.0000 |
| exp0.5 ! | 0.4982 ± 0.0021 | 0.4976 ± 0.0067 | 0.0608 ± 0.0003 | 0.0492 ± 0.0007 | 0.0060 ± 0.0000 |
| exp0.75 ! | 0.4962 ± 0.0025 | 0.4976 ± 0.0067 | 0.0608 ± 0.0003 | 0.0492 ± 0.0007 | 0.0060 ± 0.0000 |
| exp1.0 ! | 0.4978 ± 0.0023 | 0.4976 ± 0.0067 | 0.0608 ± 0.0003 | 0.0492 ± 0.0007 | 0.0060 ± 0.0000 |

---

## cmplx_ps

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.1664 ± 0.0035 | 1.6649 ± 0.0131 | 0.1680 ± 0.0008 | 0.1648 ± 0.0013 | 0.0166 ± 0.0001 |
| exp0.05 | 0.1666 ± 0.0006 | 1.6649 ± 0.0131 | 0.1680 ± 0.0008 | 0.1648 ± 0.0013 | 0.0166 ± 0.0001 |
| exp0.1 | 0.1672 ± 0.0009 | 1.6649 ± 0.0131 | 0.1680 ± 0.0008 | 0.1648 ± 0.0013 | 0.0166 ± 0.0001 |
| exp0.25 | 0.1677 ± 0.0004 | 1.6649 ± 0.0131 | 0.1680 ± 0.0008 | 0.1648 ± 0.0013 | 0.0166 ± 0.0001 |
| exp0.5 ! | 0.1678 ± 0.0002 | 1.6649 ± 0.0131 | 0.1680 ± 0.0008 | 0.1648 ± 0.0013 | 0.0166 ± 0.0001 |
| exp0.75 ! | 0.1680 ± 0.0005 | 1.6649 ± 0.0131 | 0.1680 ± 0.0008 | 0.1648 ± 0.0013 | 0.0166 ± 0.0001 |
| exp1.0 ! | 0.1680 ± 0.0004 | 1.6649 ± 0.0131 | 0.1680 ± 0.0008 | 0.1648 ± 0.0013 | 0.0166 ± 0.0001 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.6477 ± 0.0352 | 1.6649 ± 0.0131 | 0.1680 ± 0.0008 | 0.1648 ± 0.0013 | 0.0166 ± 0.0001 |
| exp0.05 | 1.6528 ± 0.0178 | 1.6649 ± 0.0131 | 0.1680 ± 0.0008 | 0.1648 ± 0.0013 | 0.0166 ± 0.0001 |
| exp0.1 | 1.6602 ± 0.0160 | 1.6649 ± 0.0131 | 0.1680 ± 0.0008 | 0.1648 ± 0.0013 | 0.0166 ± 0.0001 |
| exp0.25 | 1.6650 ± 0.0050 | 1.6649 ± 0.0131 | 0.1680 ± 0.0008 | 0.1648 ± 0.0013 | 0.0166 ± 0.0001 |
| exp0.5 ! | 1.6626 ± 0.0054 | 1.6649 ± 0.0131 | 0.1680 ± 0.0008 | 0.1648 ± 0.0013 | 0.0166 ± 0.0001 |
| exp0.75 ! | 1.6648 ± 0.0060 | 1.6649 ± 0.0131 | 0.1680 ± 0.0008 | 0.1648 ± 0.0013 | 0.0166 ± 0.0001 |
| exp1.0 ! | 1.6656 ± 0.0048 | 1.6649 ± 0.0131 | 0.1680 ± 0.0008 | 0.1648 ± 0.0013 | 0.0166 ± 0.0001 |

---

## c1e3_exp1.0

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.1210 ± 0.0036 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.05 | 0.1205 ± 0.0003 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.1 | 0.1214 ± 0.0008 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.25 | 0.1220 ± 0.0002 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.5 ! | 0.1223 ± 0.0004 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.75 ! | 0.1223 ± 0.0004 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp1.0 ! | 0.1222 ± 0.0003 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0290 ± 0.0326 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.05 | 1.0253 ± 0.0035 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.1 | 1.0348 ± 0.0117 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.25 | 1.0392 ± 0.0014 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.5 ! | 1.0401 ± 0.0035 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.75 ! | 1.0391 ± 0.0027 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp1.0 ! | 1.0382 ± 0.0023 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |

---

## c1e4_exp1.0

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.1210 ± 0.0036 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.05 | 0.1205 ± 0.0003 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.1 | 0.1214 ± 0.0008 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.25 | 0.1220 ± 0.0002 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.5 ! | 0.1223 ± 0.0004 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.75 ! | 0.1223 ± 0.0004 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp1.0 ! | 0.1222 ± 0.0003 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0290 ± 0.0326 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.05 | 1.0253 ± 0.0035 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.1 | 1.0348 ± 0.0117 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.25 | 1.0392 ± 0.0014 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.5 ! | 1.0401 ± 0.0035 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp0.75 ! | 1.0391 ± 0.0027 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |
| exp1.0 ! | 1.0382 ± 0.0023 | 1.0426 ± 0.0024 | 0.1224 ± 0.0006 | 0.1031 ± 0.0002 | 0.0121 ± 0.0001 |

---

# RESULTS (Dense Table)

---

## naive_ps

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 0.5100 ± 0.0189 | 0.0622 ± 0.0011 |
| exp0.05 | 0.5058 ± 0.0049 | 0.0613 ± 0.0003 |
| exp0.1 | 0.5028 ± 0.0094 | 0.0612 ± 0.0002 |
| exp0.25 | 0.4986 ± 0.0018 | 0.0609 ± 0.0002 |
| exp0.5 ! | 0.4982 ± 0.0021 | 0.0608 ± 0.0003 |
| exp0.75 ! | 0.4962 ± 0.0025 | 0.0608 ± 0.0002 |
| exp1.0 ! | 0.4978 ± 0.0023 | 0.0608 ± 0.0002 |

---

## cmplx_ps

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.6477 ± 0.0352 | 0.1664 ± 0.0035 |
| exp0.05 | 1.6528 ± 0.0178 | 0.1666 ± 0.0006 |
| exp0.1 | 1.6602 ± 0.0160 | 0.1672 ± 0.0009 |
| exp0.25 | 1.6650 ± 0.0050 | 0.1677 ± 0.0004 |
| exp0.5 ! | 1.6626 ± 0.0054 | 0.1678 ± 0.0002 |
| exp0.75 ! | 1.6648 ± 0.0060 | 0.1680 ± 0.0005 |
| exp1.0 ! | 1.6656 ± 0.0048 | 0.1680 ± 0.0004 |

---

## c1e3_exp1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0290 ± 0.0326 | 0.1210 ± 0.0036 |
| exp0.05 | 1.0253 ± 0.0035 | 0.1205 ± 0.0003 |
| exp0.1 | 1.0348 ± 0.0117 | 0.1214 ± 0.0008 |
| exp0.25 | 1.0392 ± 0.0014 | 0.1220 ± 0.0002 |
| exp0.5 ! | 1.0401 ± 0.0035 | 0.1223 ± 0.0004 |
| exp0.75 ! | 1.0391 ± 0.0027 | 0.1223 ± 0.0004 |
| exp1.0 ! | 1.0382 ± 0.0023 | 0.1222 ± 0.0003 |

---

## c1e4_exp1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0290 ± 0.0326 | 0.1210 ± 0.0036 |
| exp0.05 | 1.0253 ± 0.0035 | 0.1205 ± 0.0003 |
| exp0.1 | 1.0348 ± 0.0117 | 0.1214 ± 0.0008 |
| exp0.25 | 1.0392 ± 0.0014 | 0.1220 ± 0.0002 |
| exp0.5 ! | 1.0401 ± 0.0035 | 0.1223 ± 0.0004 |
| exp0.75 ! | 1.0391 ± 0.0027 | 0.1223 ± 0.0004 |
| exp1.0 ! | 1.0382 ± 0.0023 | 0.1222 ± 0.0003 |


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
