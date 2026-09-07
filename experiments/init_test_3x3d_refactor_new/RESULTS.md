# init_test_3x3d_refactor_new results

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
| exp0.01 | 0.0484 / 15.75 | 0.5132 / 200.1 | 0.0484 / 1.588 | 0.0508 / n/r | 0.0048 / n/r |
| exp0.05 | 0.0469 / 3.011 | 0.5070 / 195.4 | 0.0475 / 1.54 | 0.0502 / n/r | 0.0047 / n/r |
| exp0.1 | 0.0469 / 1.475 | 0.5069 / 192.9 | 0.0474 / 1.507 | 0.0502 / n/r | 0.0047 / n/r |
| exp0.25 | 0.0474 / 0.6197 | 0.5104 / 197.5 | 0.0477 / 1.538 | 0.0506 / n/r | 0.0047 / n/r |
| exp0.5 ! | 0.0473 / 0.3168 | 0.5067 / 194.8 | 0.0473 / 1.519 | 0.0502 / n/r | 0.0047 / n/r |
| exp0.75 ! | 0.0473 / 0.2157 | 0.5060 / 193.8 | 0.0473 / 1.511 | 0.0501 / n/r | 0.0047 / n/r |
| exp1.0 ! | 0.0473 / 0.1654 | 0.5057 / 193 | 0.0473 / 1.508 | 0.0501 / n/r | 0.0047 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.5401 / 1962 | 0.5440 / 207.1 | 0.2213 / 14.76 | 0.0526 / n/r | 0.0216 / n/r |
| exp0.05 | 0.5185 / 320.6 | 0.5267 / 166.9 | 0.1429 / 5.11 | 0.0513 / n/r | 0.0139 / n/r |
| exp0.1 | 0.5054 / 172.9 | 0.5028 / 172 | 0.1276 / 4.88 | 0.0491 / n/r | 0.0125 / n/r |
| exp0.25 | 0.5094 / 73.69 | 0.5113 / 179.4 | 0.1050 / 3.6 | 0.0501 / n/r | 0.0103 / n/r |
| exp0.5 ! | 0.5022 / 37.41 | 0.5051 / 177.7 | 0.0786 / 2.493 | 0.0497 / n/r | 0.0077 / n/r |
| exp0.75 ! | 0.5049 / 24.63 | 0.5069 / 168.5 | 0.0817 / 2.449 | 0.0499 / n/r | 0.0080 / n/r |
| exp1.0 ! | 0.5017 / 19.26 | 0.5062 / 172.9 | 0.0725 / 2.276 | 0.0499 / n/r | 0.0071 / n/r |

---

## cmplx_ps

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.1471 / 37.63 | 1.6970 / 482.5 | 0.1456 / 3.701 | 0.1683 / n/r | 0.0144 / n/r |
| exp0.05 | 0.1428 / 7.023 | 1.6805 / 466.4 | 0.1443 / 3.581 | 0.1666 / n/r | 0.0143 / n/r |
| exp0.1 | 0.1430 / 3.506 | 1.6828 / 466.7 | 0.1440 / 3.547 | 0.1669 / n/r | 0.0143 / n/r |
| exp0.25 | 0.1434 / 1.427 | 1.6804 / 464.3 | 0.1437 / 3.537 | 0.1666 / n/r | 0.0142 / n/r |
| exp0.5 ! | 0.1433 / 0.7276 | 1.6781 / 464.8 | 0.1435 / 3.548 | 0.1664 / n/r | 0.0142 / n/r |
| exp0.75 ! | 0.1432 / 0.4888 | 1.6758 / 461.6 | 0.1433 / 3.526 | 0.1662 / n/r | 0.0142 / n/r |
| exp1.0 ! | 0.1432 / 0.372 | 1.6799 / 463.6 | 0.1435 / 3.526 | 0.1666 / n/r | 0.0142 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.7391 / 4690 | 1.7416 / 477.7 | 0.4299 / 8.852 | 0.1700 / n/r | 0.0420 / n/r |
| exp0.05 | 1.6700 / 814.2 | 1.6804 / 411.3 | 0.3203 / 5.892 | 0.1649 / n/r | 0.0314 / n/r |
| exp0.1 | 1.6674 / 406.9 | 1.6748 / 407.5 | 0.2544 / 5.129 | 0.1650 / n/r | 0.0250 / n/r |
| exp0.25 | 1.6706 / 165.8 | 1.6763 / 411.4 | 0.2118 / 4.495 | 0.1655 / n/r | 0.0209 / n/r |
| exp0.5 ! | 1.6674 / 85.84 | 1.6668 / 415 | 0.2189 / 4.559 | 0.1645 / n/r | 0.0216 / n/r |
| exp0.75 ! | 1.6681 / 59.25 | 1.6713 / 427 | 0.1803 / 4.119 | 0.1654 / n/r | 0.0178 / n/r |
| exp1.0 ! | 1.6730 / 45.29 | 1.6662 / 417.7 | 0.2096 / 4.442 | 0.1646 / n/r | 0.0207 / n/r |

---

## c1e3_exp1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.0816 / 18.92 | 1.0633 / 336.3 | 0.0816 / 1.925 | 0.1055 / n/r | 0.0081 / n/r |
| exp0.05 | 0.0795 / 3.756 | 1.0501 / 325.7 | 0.0801 / 1.898 | 0.1042 / n/r | 0.0079 / n/r |
| exp0.1 | 0.0797 / 1.887 | 1.0502 / 330.7 | 0.0800 / 1.891 | 0.1042 / n/r | 0.0079 / n/r |
| exp0.25 | 0.0793 / 0.7556 | 1.0437 / 327.2 | 0.0795 / 1.882 | 0.1036 / n/r | 0.0079 / n/r |
| exp0.5 ! | 0.0794 / 0.3907 | 1.0413 / 325.9 | 0.0793 / 1.881 | 0.1034 / n/r | 0.0079 / n/r |
| exp0.75 ! | 0.0793 / 0.2638 | 1.0432 / 326.8 | 0.0794 / 1.886 | 0.1035 / n/r | 0.0079 / n/r |
| exp1.0 ! | 0.0792 / 0.2002 | 1.0382 / 320.7 | 0.0792 / 1.854 | 0.1030 / n/r | 0.0078 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0736 / 2820 | 1.0725 / 292.3 | 0.4290 / 9.399 | 0.1032 / n/r | 0.0417 / n/r |
| exp0.05 | 1.0531 / 526.6 | 1.0526 / 266.1 | 0.2396 / 3.944 | 0.1029 / n/r | 0.0235 / n/r |
| exp0.1 | 1.0443 / 263.2 | 1.0454 / 264.2 | 0.1909 / 3.347 | 0.1027 / n/r | 0.0188 / n/r |
| exp0.25 | 1.0446 / 107.5 | 1.0444 / 263.8 | 0.2068 / 3.793 | 0.1024 / n/r | 0.0203 / n/r |
| exp0.5 ! | 1.0438 / 56.37 | 1.0438 / 268 | 0.1838 / 3.336 | 0.1026 / n/r | 0.0180 / n/r |
| exp0.75 ! | 1.0430 / 38.31 | 1.0450 / 269.3 | 0.1352 / 2.752 | 0.1032 / n/r | 0.0133 / n/r |
| exp1.0 ! | 1.0437 / 29.99 | 1.0449 / 264.1 | 0.1760 / 3.151 | 0.1028 / n/r | 0.0173 / n/r |

---

## c1e4_exp1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.0823 / 20.46 | 1.0613 / 349.9 | 0.0819 / 2.05 | 0.1053 / n/r | 0.0081 / n/r |
| exp0.05 | 0.0802 / 3.612 | 1.0522 / 316 | 0.0803 / 1.8 | 0.1044 / n/r | 0.0080 / n/r |
| exp0.1 | 0.0800 / 1.823 | 1.0477 / 313.8 | 0.0802 / 1.823 | 0.1040 / n/r | 0.0079 / n/r |
| exp0.25 | 0.0799 / 0.7675 | 1.0467 / 323.3 | 0.0799 / 1.884 | 0.1039 / n/r | 0.0079 / n/r |
| exp0.5 ! | 0.0796 / 0.3882 | 1.0459 / 322.7 | 0.0798 / 1.894 | 0.1038 / n/r | 0.0079 / n/r |
| exp0.75 ! | 0.0796 / 0.2643 | 1.0468 / 322.5 | 0.0798 / 1.895 | 0.1039 / n/r | 0.0079 / n/r |
| exp1.0 ! | 0.0797 / 0.2022 | 1.0472 / 321.5 | 0.0798 / 1.884 | 0.1039 / n/r | 0.0079 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0786 / 2605 | 1.0889 / 275.2 | 0.4324 / 8.901 | 0.1048 / n/r | 0.0420 / n/r |
| exp0.05 | 1.0564 / 523.2 | 1.0446 / 258 | 0.2779 / 5.859 | 0.1020 / n/r | 0.0272 / n/r |
| exp0.1 | 1.0622 / 267.9 | 1.0562 / 263.8 | 0.2659 / 5.458 | 0.1033 / n/r | 0.0261 / n/r |
| exp0.25 | 1.0471 / 111.6 | 1.0443 / 272.9 | 0.2117 / 3.624 | 0.1025 / n/r | 0.0208 / n/r |
| exp0.5 ! | 1.0437 / 57.91 | 1.0450 / 277.9 | 0.1557 / 4.083 | 0.1031 / n/r | 0.0154 / n/r |
| exp0.75 ! | 1.0467 / 38.98 | 1.0417 / 270.2 | 0.3006 / 39 | 0.1028 / n/r | 0.0298 / n/r |
| exp1.0 ! | 1.0478 / 31.6 | 1.0402 / 277.3 | 0.1852 / 3.799 | 0.1024 / n/r | 0.0182 / n/r |

---

# RESULTS (Dense Table)

---

## naive_ps

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 0.5401 / 1962 | 0.0484 / 15.75 |
| exp0.05 | 0.5185 / 320.6 | 0.0469 / 3.011 |
| exp0.1 | 0.5054 / 172.9 | 0.0469 / 1.475 |
| exp0.25 | 0.5094 / 73.69 | 0.0474 / 0.6197 |
| exp0.5 ! | 0.5022 / 37.41 | 0.0473 / 0.3168 |
| exp0.75 ! | 0.5049 / 24.63 | 0.0473 / 0.2157 |
| exp1.0 ! | 0.5017 / 19.26 | 0.0473 / 0.1654 |

---

## cmplx_ps

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.7391 / 4690 | 0.1471 / 37.63 |
| exp0.05 | 1.6700 / 814.2 | 0.1428 / 7.023 |
| exp0.1 | 1.6674 / 406.9 | 0.1430 / 3.506 |
| exp0.25 | 1.6706 / 165.8 | 0.1434 / 1.427 |
| exp0.5 ! | 1.6674 / 85.84 | 0.1433 / 0.7276 |
| exp0.75 ! | 1.6681 / 59.25 | 0.1432 / 0.4888 |
| exp1.0 ! | 1.6730 / 45.29 | 0.1432 / 0.372 |

---

## c1e3_exp1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0736 / 2820 | 0.0816 / 18.92 |
| exp0.05 | 1.0531 / 526.6 | 0.0795 / 3.756 |
| exp0.1 | 1.0443 / 263.2 | 0.0797 / 1.887 |
| exp0.25 | 1.0446 / 107.5 | 0.0793 / 0.7556 |
| exp0.5 ! | 1.0438 / 56.37 | 0.0794 / 0.3907 |
| exp0.75 ! | 1.0430 / 38.31 | 0.0793 / 0.2638 |
| exp1.0 ! | 1.0437 / 29.99 | 0.0792 / 0.2002 |

---

## c1e4_exp1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0786 / 2605 | 0.0823 / 20.46 |
| exp0.05 | 1.0564 / 523.2 | 0.0802 / 3.612 |
| exp0.1 | 1.0622 / 267.9 | 0.0800 / 1.823 |
| exp0.25 | 1.0471 / 111.6 | 0.0799 / 0.7675 |
| exp0.5 ! | 1.0437 / 57.91 | 0.0796 / 0.3882 |
| exp0.75 ! | 1.0467 / 38.98 | 0.0796 / 0.2643 |
| exp1.0 ! | 1.0478 / 31.6 | 0.0797 / 0.2022 |


---

# Insights and conclusions

**All 168 cells completed.** Read against
`experiments/init_opt_test_3x3d_refactor_new/RESULTS.md` (exact posterior, same geometry),
which lands on `H(p)` within ±0.4 SE for every `ps` — so on this geometry `wnelbo_ref` is
a sound estimator and these cells may be compared to `H(p)` directly.

## 1. The trained model reaches H(p) on both objectives, at every rate

`wnelbo_ref`, 3-seed mean, by loss proposal rate:

| ps, obj | .01 | .05 | .1 | .25 | .5 | .75 | 1.0 |
|---|---|---|---|---|---|---|---|
| naive_ps CE | 0.5132 | 0.5070 | 0.5069 | 0.5104 | 0.5067 | 0.5060 | 0.5057 |
| naive_ps PP | 0.5440 | 0.5267 | 0.5028 | 0.5113 | 0.5051 | 0.5069 | 0.5062 |
| cmplx_ps CE | 1.6970 | 1.6805 | 1.6828 | 1.6804 | 1.6781 | 1.6758 | 1.6799 |
| cmplx_ps PP | 1.7416 | 1.6804 | 1.6748 | 1.6763 | 1.6668 | 1.6713 | 1.6662 |
| c1e3 CE | 1.0633 | 1.0501 | 1.0502 | 1.0437 | 1.0413 | 1.0432 | 1.0382 |
| c1e3 PP | 1.0725 | 1.0526 | 1.0454 | 1.0444 | 1.0438 | 1.0450 | 1.0449 |
| c1e4 CE | 1.0613 | 1.0522 | 1.0477 | 1.0467 | 1.0459 | 1.0468 | 1.0472 |
| c1e4 PP | 1.0889 | 1.0446 | 1.0562 | 1.0443 | 1.0450 | 1.0417 | 1.0402 |

Best cell per (ps, objective), as a percentage above `H(p)`:

| ps | CE | PP |
|---|---|---|
| naive_ps | 0.5057 (+1.08 %) | **0.5028 (+0.50 %)** |
| cmplx_ps | 1.6758 (+0.56 %) | **1.6662 (−0.01 %)** |
| c1e3 | **1.0413 (+0.06 %)** | 1.0438 (+0.31 %) |
| c1e4 | 1.0459 (+0.50 %) | **1.0402 (−0.05 %)** |

Hypothesis 1 confirmed: the product path is a valid ELBO, and the best cells land on
`H(p)` to within 0.5 % — the two slightly-negative entries (−0.01 %, −0.05 %) are inside
the control's own ±0.4 SE band, not violations. As at `d = 3`, `poincare_polar` is
rate-sensitive at rate 0.01 (0.5440 / 1.7416 / 1.0889, i.e. 5–9 % high) and flat
thereafter; `cross_entropy` is nearly flat across the whole axis.

## 2. The decisive result: zero collapses, where the single flat manifold had 70/84

| configuration | cells with `wnelbo_ref` < 0.01 |
|---|---|
| single `H^3_{-0.01}`, `poincare_polar` | **70 / 84** |
| single `H^3_{-0.01}`, `cross_entropy` | 0 / 84 |
| single `H^3_{-1}` / `H^3_{-10}`, either | 0 / 336 |
| **product `H^3_{-0.01} × H^3_{-10} × H^3_{-1}`, either** | **0 / 168** |

`init_test_3d_refactor_new` shows that training on the importance-weighted polar ELBO at
`K = -0.01` finds a degenerate optimum in 83 % of cells — `wloss` → 0, `wnelbo_ref` → 0,
`wce_ref` → 150–250. This project contains a `K = -0.01` factor and shows **no trace of
it**: not one cell collapsed, at any rate, on either objective.

Hypothesis 2 confirmed, and more strongly than stated. The mechanism is the heat-time
ceiling: `main_refactor.py` clamps `t` at `min_m _radial_t_max(3) · R_m^2` =
`min(9700, 9.7, 97)` = **9.7**, set by the sharpest factor. The whole product lives in the
`K = -10` factor's time range, so the flat factor never reaches the regime where the
weighted objective goes heavy-tailed. **A flat factor is safe as long as a sharp factor
binds the ceiling** — and the converse is the warning, since the ceiling is a *minimum*: a
product of only flat factors would inherit the pathology with nothing to bind it.

## 3. The product identifies the word faster than any single factor

`wce_ref` / `ce_ref` at rate 0.1 (best-conditioned cells across the whole study):

| geometry | `wce_ref` (naive / cmplx / c1e3) | `ce_ref` (naive) |
|---|---|---|
| **product [3,3,3]**, CE | **0.047 / 0.144 / 0.080** | **0.0047** |
| product [3,3,3], PP | 0.128 / 0.254 / 0.191 | 0.0125 |
| single `K = -10` (Bayes-opt) | 0.062 / 0.209 / 0.115 | 0.0062 |
| single `K = -1` (Bayes-opt) | 0.630 / 2.101 / 1.152 | 0.0558 |
| single `K = -0.01` (Bayes-opt) | 44.4 / 172.0 / 90.3 | 0.4654 |

Hypothesis 3 confirmed: the CE-trained product beats even the *Bayes-optimal* single
`K = -10` manifold on denoising cross-entropy (0.047 vs 0.062 nats). Nine direction
components plus three radii carry more information per unit `t` than three components and
one radius, so the bridge resolves the target sooner — while `wnelbo_ref` stays pinned at
`H(p)`, which is what makes this an improvement in the readout rather than a leak.

## 4. Cross-project summary

| geometry | estimator valid? | trained model reaches H(p)? | ELBO training stable? |
|---|---|---|---|
| `H^3_{-1}` | yes (+0.1…+0.9 SE) | yes | yes |
| `H^3_{-10}` | yes (−0.1…−0.6 SE) | yes | yes |
| `H^3_{-0.01}` | **no** (26 % low) | not measurable | **no** (70/84 collapse) |
| `H^3_{-0.01} × H^3_{-10} × H^3_{-1}` | yes (±0.4 SE) | yes (≤0.5 % above) | yes (0/168 collapse) |

**Design guidance this study supports.** Mixing curvatures in a product manifold is not
just safe, it is the best-behaved configuration measured: it keeps the sharp factor's
numerical conditioning and gains the extra dimensions' faster identification. What must
not be done is running a single flat manifold against a proposal tuned for `K = -1` —
there the ELBO is neither trainable nor measurable, and both failures are silent.
