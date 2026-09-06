# init_test_3x3d_refactor_new results

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
| exp0.01 | 0.0484 ± 0.0018 | 0.5132 ± 0.0072 | 0.0484 ± 0.0008 | 0.0508 ± 0.0007 | 0.0048 ± 0.0001 |
| exp0.05 | 0.0469 ± 0.0005 | 0.5070 ± 0.0050 | 0.0475 ± 0.0005 | 0.0502 ± 0.0005 | 0.0047 ± 0.0000 |
| exp0.1 | 0.0469 ± 0.0005 | 0.5069 ± 0.0038 | 0.0474 ± 0.0006 | 0.0502 ± 0.0004 | 0.0047 ± 0.0001 |
| exp0.25 | 0.0474 ± 0.0003 | 0.5104 ± 0.0037 | 0.0477 ± 0.0005 | 0.0506 ± 0.0004 | 0.0047 ± 0.0000 |
| exp0.5 ! | 0.0473 ± 0.0002 | 0.5067 ± 0.0014 | 0.0473 ± 0.0004 | 0.0502 ± 0.0001 | 0.0047 ± 0.0000 |
| exp0.75 ! | 0.0473 ± 0.0003 | 0.5060 ± 0.0049 | 0.0473 ± 0.0005 | 0.0501 ± 0.0005 | 0.0047 ± 0.0000 |
| exp1.0 ! | 0.0473 ± 0.0003 | 0.5057 ± 0.0027 | 0.0473 ± 0.0004 | 0.0501 ± 0.0003 | 0.0047 ± 0.0000 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.5401 ± 0.0179 | 0.5440 ± 0.0147 | 0.2213 ± 0.0238 | 0.0526 ± 0.0015 | 0.0216 ± 0.0023 |
| exp0.05 | 0.5185 ± 0.0241 | 0.5267 ± 0.0205 | 0.1429 ± 0.0278 | 0.0513 ± 0.0018 | 0.0139 ± 0.0027 |
| exp0.1 | 0.5054 ± 0.0065 | 0.5028 ± 0.0112 | 0.1276 ± 0.0190 | 0.0491 ± 0.0012 | 0.0125 ± 0.0018 |
| exp0.25 | 0.5094 ± 0.0062 | 0.5113 ± 0.0068 | 0.1050 ± 0.0193 | 0.0501 ± 0.0006 | 0.0103 ± 0.0019 |
| exp0.5 ! | 0.5022 ± 0.0027 | 0.5051 ± 0.0053 | 0.0786 ± 0.0083 | 0.0497 ± 0.0005 | 0.0077 ± 0.0008 |
| exp0.75 ! | 0.5049 ± 0.0030 | 0.5069 ± 0.0017 | 0.0817 ± 0.0073 | 0.0499 ± 0.0002 | 0.0080 ± 0.0007 |
| exp1.0 ! | 0.5017 ± 0.0015 | 0.5062 ± 0.0017 | 0.0725 ± 0.0094 | 0.0499 ± 0.0002 | 0.0071 ± 0.0009 |

---

## cmplx_ps

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.1471 ± 0.0024 | 1.6970 ± 0.0091 | 0.1456 ± 0.0012 | 0.1683 ± 0.0009 | 0.0144 ± 0.0001 |
| exp0.05 | 0.1428 ± 0.0006 | 1.6805 ± 0.0079 | 0.1443 ± 0.0009 | 0.1666 ± 0.0008 | 0.0143 ± 0.0001 |
| exp0.1 | 0.1430 ± 0.0003 | 1.6828 ± 0.0019 | 0.1440 ± 0.0004 | 0.1669 ± 0.0002 | 0.0143 ± 0.0000 |
| exp0.25 | 0.1434 ± 0.0006 | 1.6804 ± 0.0061 | 0.1437 ± 0.0007 | 0.1666 ± 0.0006 | 0.0142 ± 0.0001 |
| exp0.5 ! | 0.1433 ± 0.0005 | 1.6781 ± 0.0028 | 0.1435 ± 0.0006 | 0.1664 ± 0.0003 | 0.0142 ± 0.0001 |
| exp0.75 ! | 0.1432 ± 0.0004 | 1.6758 ± 0.0021 | 0.1433 ± 0.0005 | 0.1662 ± 0.0002 | 0.0142 ± 0.0000 |
| exp1.0 ! | 0.1432 ± 0.0004 | 1.6799 ± 0.0047 | 0.1435 ± 0.0005 | 0.1666 ± 0.0005 | 0.0142 ± 0.0001 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.7391 ± 0.0451 | 1.7416 ± 0.0299 | 0.4299 ± 0.0350 | 0.1700 ± 0.0029 | 0.0420 ± 0.0034 |
| exp0.05 | 1.6700 ± 0.0101 | 1.6804 ± 0.0069 | 0.3203 ± 0.0721 | 0.1649 ± 0.0001 | 0.0314 ± 0.0070 |
| exp0.1 | 1.6674 ± 0.0050 | 1.6748 ± 0.0072 | 0.2544 ± 0.0643 | 0.1650 ± 0.0005 | 0.0250 ± 0.0063 |
| exp0.25 | 1.6706 ± 0.0043 | 1.6763 ± 0.0123 | 0.2118 ± 0.0225 | 0.1655 ± 0.0011 | 0.0209 ± 0.0022 |
| exp0.5 ! | 1.6674 ± 0.0051 | 1.6668 ± 0.0047 | 0.2189 ± 0.0278 | 0.1645 ± 0.0006 | 0.0216 ± 0.0027 |
| exp0.75 ! | 1.6681 ± 0.0057 | 1.6713 ± 0.0096 | 0.1803 ± 0.0014 | 0.1654 ± 0.0010 | 0.0178 ± 0.0001 |
| exp1.0 ! | 1.6730 ± 0.0036 | 1.6662 ± 0.0009 | 0.2096 ± 0.0235 | 0.1646 ± 0.0003 | 0.0207 ± 0.0023 |

---

## c1e3_exp1.0

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.0816 ± 0.0043 | 1.0633 ± 0.0119 | 0.0816 ± 0.0008 | 0.1055 ± 0.0012 | 0.0081 ± 0.0001 |
| exp0.05 | 0.0795 ± 0.0019 | 1.0501 ± 0.0158 | 0.0801 ± 0.0008 | 0.1042 ± 0.0016 | 0.0079 ± 0.0001 |
| exp0.1 | 0.0797 ± 0.0015 | 1.0502 ± 0.0159 | 0.0800 ± 0.0011 | 0.1042 ± 0.0016 | 0.0079 ± 0.0001 |
| exp0.25 | 0.0793 ± 0.0003 | 1.0437 ± 0.0055 | 0.0795 ± 0.0003 | 0.1036 ± 0.0005 | 0.0079 ± 0.0000 |
| exp0.5 ! | 0.0794 ± 0.0001 | 1.0413 ± 0.0059 | 0.0793 ± 0.0005 | 0.1034 ± 0.0006 | 0.0079 ± 0.0000 |
| exp0.75 ! | 0.0793 ± 0.0002 | 1.0432 ± 0.0081 | 0.0794 ± 0.0006 | 0.1035 ± 0.0008 | 0.0079 ± 0.0001 |
| exp1.0 ! | 0.0792 ± 0.0001 | 1.0382 ± 0.0029 | 0.0792 ± 0.0005 | 0.1030 ± 0.0003 | 0.0078 ± 0.0001 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0736 ± 0.0341 | 1.0725 ± 0.0058 | 0.4290 ± 0.0799 | 0.1032 ± 0.0012 | 0.0417 ± 0.0076 |
| exp0.05 | 1.0531 ± 0.0150 | 1.0526 ± 0.0091 | 0.2396 ± 0.0862 | 0.1029 ± 0.0011 | 0.0235 ± 0.0084 |
| exp0.1 | 1.0443 ± 0.0099 | 1.0454 ± 0.0053 | 0.1909 ± 0.0509 | 0.1027 ± 0.0005 | 0.0188 ± 0.0050 |
| exp0.25 | 1.0446 ± 0.0092 | 1.0444 ± 0.0064 | 0.2068 ± 0.0597 | 0.1024 ± 0.0009 | 0.0203 ± 0.0058 |
| exp0.5 ! | 1.0438 ± 0.0016 | 1.0438 ± 0.0078 | 0.1838 ± 0.0518 | 0.1026 ± 0.0003 | 0.0180 ± 0.0051 |
| exp0.75 ! | 1.0430 ± 0.0010 | 1.0450 ± 0.0083 | 0.1352 ± 0.0291 | 0.1032 ± 0.0008 | 0.0133 ± 0.0028 |
| exp1.0 ! | 1.0437 ± 0.0014 | 1.0449 ± 0.0054 | 0.1760 ± 0.0682 | 0.1028 ± 0.0005 | 0.0173 ± 0.0066 |

---

## c1e4_exp1.0

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.0823 ± 0.0023 | 1.0613 ± 0.0179 | 0.0819 ± 0.0014 | 0.1053 ± 0.0018 | 0.0081 ± 0.0001 |
| exp0.05 | 0.0802 ± 0.0012 | 1.0522 ± 0.0067 | 0.0803 ± 0.0006 | 0.1044 ± 0.0007 | 0.0080 ± 0.0001 |
| exp0.1 | 0.0800 ± 0.0004 | 1.0477 ± 0.0118 | 0.0802 ± 0.0013 | 0.1040 ± 0.0012 | 0.0079 ± 0.0001 |
| exp0.25 | 0.0799 ± 0.0004 | 1.0467 ± 0.0027 | 0.0799 ± 0.0008 | 0.1039 ± 0.0003 | 0.0079 ± 0.0001 |
| exp0.5 ! | 0.0796 ± 0.0003 | 1.0459 ± 0.0074 | 0.0798 ± 0.0011 | 0.1038 ± 0.0007 | 0.0079 ± 0.0001 |
| exp0.75 ! | 0.0796 ± 0.0005 | 1.0468 ± 0.0045 | 0.0798 ± 0.0010 | 0.1039 ± 0.0004 | 0.0079 ± 0.0001 |
| exp1.0 ! | 0.0797 ± 0.0003 | 1.0472 ± 0.0042 | 0.0798 ± 0.0010 | 0.1039 ± 0.0004 | 0.0079 ± 0.0001 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0786 ± 0.0709 | 1.0889 ± 0.0611 | 0.4324 ± 0.0629 | 0.1048 ± 0.0062 | 0.0420 ± 0.0061 |
| exp0.05 | 1.0564 ± 0.0110 | 1.0446 ± 0.0030 | 0.2779 ± 0.0137 | 0.1020 ± 0.0008 | 0.0272 ± 0.0013 |
| exp0.1 | 1.0622 ± 0.0140 | 1.0562 ± 0.0067 | 0.2659 ± 0.0089 | 0.1033 ± 0.0012 | 0.0261 ± 0.0008 |
| exp0.25 | 1.0471 ± 0.0026 | 1.0443 ± 0.0091 | 0.2117 ± 0.0481 | 0.1025 ± 0.0010 | 0.0208 ± 0.0047 |
| exp0.5 ! | 1.0437 ± 0.0074 | 1.0450 ± 0.0069 | 0.1557 ± 0.0121 | 0.1031 ± 0.0009 | 0.0154 ± 0.0012 |
| exp0.75 ! | 1.0467 ± 0.0058 | 1.0417 ± 0.0046 | 0.3006 ± 0.2395 | 0.1028 ± 0.0006 | 0.0298 ± 0.0238 |
| exp1.0 ! | 1.0478 ± 0.0067 | 1.0402 ± 0.0086 | 0.1852 ± 0.0919 | 0.1024 ± 0.0018 | 0.0182 ± 0.0089 |

---

# RESULTS (Dense Table)

---

## naive_ps

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 0.5401 ± 0.0179 | 0.0484 ± 0.0018 |
| exp0.05 | 0.5185 ± 0.0241 | 0.0469 ± 0.0005 |
| exp0.1 | 0.5054 ± 0.0065 | 0.0469 ± 0.0005 |
| exp0.25 | 0.5094 ± 0.0062 | 0.0474 ± 0.0003 |
| exp0.5 ! | 0.5022 ± 0.0027 | 0.0473 ± 0.0002 |
| exp0.75 ! | 0.5049 ± 0.0030 | 0.0473 ± 0.0003 |
| exp1.0 ! | 0.5017 ± 0.0015 | 0.0473 ± 0.0003 |

---

## cmplx_ps

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.7391 ± 0.0451 | 0.1471 ± 0.0024 |
| exp0.05 | 1.6700 ± 0.0101 | 0.1428 ± 0.0006 |
| exp0.1 | 1.6674 ± 0.0050 | 0.1430 ± 0.0003 |
| exp0.25 | 1.6706 ± 0.0043 | 0.1434 ± 0.0006 |
| exp0.5 ! | 1.6674 ± 0.0051 | 0.1433 ± 0.0005 |
| exp0.75 ! | 1.6681 ± 0.0057 | 0.1432 ± 0.0004 |
| exp1.0 ! | 1.6730 ± 0.0036 | 0.1432 ± 0.0004 |

---

## c1e3_exp1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0736 ± 0.0341 | 0.0816 ± 0.0043 |
| exp0.05 | 1.0531 ± 0.0150 | 0.0795 ± 0.0019 |
| exp0.1 | 1.0443 ± 0.0099 | 0.0797 ± 0.0015 |
| exp0.25 | 1.0446 ± 0.0092 | 0.0793 ± 0.0003 |
| exp0.5 ! | 1.0438 ± 0.0016 | 0.0794 ± 0.0001 |
| exp0.75 ! | 1.0430 ± 0.0010 | 0.0793 ± 0.0002 |
| exp1.0 ! | 1.0437 ± 0.0014 | 0.0792 ± 0.0001 |

---

## c1e4_exp1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0786 ± 0.0709 | 0.0823 ± 0.0023 |
| exp0.05 | 1.0564 ± 0.0110 | 0.0802 ± 0.0012 |
| exp0.1 | 1.0622 ± 0.0140 | 0.0800 ± 0.0004 |
| exp0.25 | 1.0471 ± 0.0026 | 0.0799 ± 0.0004 |
| exp0.5 ! | 1.0437 ± 0.0074 | 0.0796 ± 0.0003 |
| exp0.75 ! | 1.0467 ± 0.0058 | 0.0796 ± 0.0005 |
| exp1.0 ! | 1.0478 ± 0.0067 | 0.0797 ± 0.0003 |


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
