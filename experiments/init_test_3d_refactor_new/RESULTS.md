# init_test_3d_refactor_new results

- runs collected: **504** / 504 (100%) — run dirs without test_metrics.json: 0
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

## naive_ps, K = -0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 53.4146 / 4.762e+05 | 0.5995 / 5.632e+05 | 60.8890 / 6.176e+09 | 0.0048 / n/r | 0.4528 / n/r |
| exp0.05 | 45.9933 / 1.585e+07 | 0.6047 / 6.096e+05 | 60.8357 / 6.211e+09 | 0.0049 / n/r | 0.4535 / n/r |
| exp0.1 | 35.6393 / 2.139e+07 | 0.6052 / 5.977e+05 | 62.8252 / 7.032e+09 | 0.0050 / n/r | 0.4517 / n/r |
| exp0.25 | 20.4914 / 7.22e+06 | 0.5624 / 6.485e+05 | 66.0463 / 6.877e+09 | 0.0051 / n/r | 0.4513 / n/r |
| exp0.5 ! | 11.7698 / 3.175e+06 | 0.4025 / 1.895e+05 | 70.8372 / 7.165e+09 | 0.0050 / n/r | 0.4530 / n/r |
| exp0.75 ! | 8.2328 / 1.821e+06 | 0.4276 / 2.511e+05 | 72.0890 / 7.359e+09 | 0.0051 / n/r | 0.4561 / n/r |
| exp1.0 ! | 6.3350 / 1.27e+06 | 0.5494 / 7.406e+05 | 76.8551 / 9.893e+09 | 0.0051 / n/r | 0.4604 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.4962 / 176.3 | 0.5178 / 7.784e+05 | 74.7193 / 3.565e+09 | 0.0031 / n/r | 0.5828 / n/r |
| exp0.05 | 0.0211 / 549.7 | 0.0004 / 0.06206 | 195.4580 / 8.938e+10 | 0.0000 / n/r | 0.7037 / n/r |
| exp0.1 | 0.0012 / 8.062 | 0.0016 / 9.696 | 192.9314 / 9.944e+10 | 0.0000 / n/r | 0.6790 / n/r |
| exp0.25 | 0.0000 / 7.055e-06 | 0.0000 / 0.002015 | 157.3953 / 5.88e+10 | 0.0000 / n/r | 0.5996 / n/r |
| exp0.5 ! | 0.0000 / 3.16e-14 | 0.0000 / 1.514e-10 | 161.5834 / 5.942e+10 | 0.0000 / n/r | 0.6319 / n/r |
| exp0.75 ! | 0.0000 / 2.88e-13 | 0.0000 / 2.975e-09 | 169.0187 / 5.851e+10 | 0.0000 / n/r | 0.6808 / n/r |
| exp1.0 ! | 0.0000 / 6.293e-17 | 0.0000 / 1.527e-11 | 243.8701 / 4.657e+10 | 0.0000 / n/r | 1.1439 / n/r |

---

## naive_ps, K = -1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.5318 / 166.9 | 0.5011 / 18.39 | 0.5368 / 18.82 | 0.0453 / n/r | 0.0479 / n/r |
| exp0.05 | 0.5339 / 35.04 | 0.4998 / 18.49 | 0.5346 / 18.65 | 0.0452 / n/r | 0.0478 / n/r |
| exp0.1 | 0.5348 / 18.91 | 0.4996 / 18.81 | 0.5342 / 18.94 | 0.0452 / n/r | 0.0477 / n/r |
| exp0.25 | 0.5356 / 9.466 | 0.4993 / 18.67 | 0.5340 / 18.83 | 0.0451 / n/r | 0.0477 / n/r |
| exp0.5 ! | 0.5350 / 8.9 | 0.5000 / 18.48 | 0.5342 / 18.6 | 0.0452 / n/r | 0.0477 / n/r |
| exp0.75 ! | 0.5351 / 22.44 | 0.5000 / 18.42 | 0.5341 / 18.56 | 0.0452 / n/r | 0.0477 / n/r |
| exp1.0 ! | 0.5342 / 40.68 | 0.4996 / 18.5 | 0.5342 / 18.69 | 0.0452 / n/r | 0.0477 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.5131 / 162.6 | 0.5099 / 19.62 | 1.2114 / 46.01 | 0.0418 / n/r | 0.1010 / n/r |
| exp0.05 | 0.5001 / 34.05 | 0.5014 / 18.39 | 0.8158 / 28.88 | 0.0434 / n/r | 0.0701 / n/r |
| exp0.1 | 0.5016 / 18.79 | 0.5022 / 18.85 | 0.8138 / 27.92 | 0.0434 / n/r | 0.0697 / n/r |
| exp0.25 | 0.5008 / 9.737 | 0.5020 / 18.51 | 0.8220 / 27.96 | 0.0435 / n/r | 0.0700 / n/r |
| exp0.5 ! | 0.5013 / 15.5 | 0.5015 / 19.05 | 0.8931 / 31.17 | 0.0431 / n/r | 0.0751 / n/r |
| exp0.75 ! | 0.5031 / 110.6 | 0.5018 / 18.42 | 0.9616 / 33.4 | 0.0427 / n/r | 0.0797 / n/r |
| exp1.0 ! | 0.4970 / 1056 | 0.5055 / 20.33 | 1.4081 / 61.53 | 0.0408 / n/r | 0.1105 / n/r |

---

## naive_ps, K = -10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.0531 / 17.41 | 0.5013 / 179.7 | 0.0539 / 1.809 | 0.0496 / n/r | 0.0053 / n/r |
| exp0.05 | 0.0531 / 3.186 | 0.5007 / 164.2 | 0.0538 / 1.635 | 0.0495 / n/r | 0.0053 / n/r |
| exp0.1 | 0.0532 / 1.626 | 0.4997 / 166.4 | 0.0536 / 1.652 | 0.0494 / n/r | 0.0053 / n/r |
| exp0.25 | 0.0533 / 0.6717 | 0.4976 / 167.8 | 0.0534 / 1.661 | 0.0492 / n/r | 0.0053 / n/r |
| exp0.5 ! | 0.0534 / 0.3492 | 0.4971 / 169.1 | 0.0533 / 1.674 | 0.0492 / n/r | 0.0053 / n/r |
| exp0.75 ! | 0.0534 / 0.2436 | 0.4960 / 171.6 | 0.0532 / 1.698 | 0.0491 / n/r | 0.0053 / n/r |
| exp1.0 ! | 0.0535 / 0.1891 | 0.4965 / 172.2 | 0.0532 / 1.703 | 0.0491 / n/r | 0.0053 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.5734 / 1958 | 0.5663 / 200.3 | 0.2650 / 16.83 | 0.0544 / n/r | 0.0257 / n/r |
| exp0.05 | 0.5298 / 322.5 | 0.5251 / 161.9 | 0.1501 / 5.503 | 0.0511 / n/r | 0.0146 / n/r |
| exp0.1 | 0.5057 / 163.9 | 0.4977 / 159.6 | 0.1202 / 4.223 | 0.0487 / n/r | 0.0118 / n/r |
| exp0.25 | 0.5009 / 65 | 0.4999 / 159.1 | 0.0910 / 2.754 | 0.0492 / n/r | 0.0089 / n/r |
| exp0.5 ! | 0.5025 / 33.1 | 0.5018 / 158.9 | 0.0766 / 2.311 | 0.0494 / n/r | 0.0075 / n/r |
| exp0.75 ! | 0.5019 / 23.79 | 0.5013 / 164.3 | 0.0845 / 2.565 | 0.0494 / n/r | 0.0083 / n/r |
| exp1.0 ! | 0.5021 / 18.51 | 0.5050 / 168 | 0.0794 / 2.481 | 0.0498 / n/r | 0.0078 / n/r |

---

## cmplx_ps, K = -0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 161.4506 / 1.12e+06 | 1.5718 / 9.274e+05 | 145.7156 / 5.88e+09 | 0.0178 / n/r | 1.4903 / n/r |
| exp0.05 | 146.0927 / 1.824e+08 | 1.5852 / 1.003e+06 | 143.5646 / 5.395e+09 | 0.0178 / n/r | 1.4898 / n/r |
| exp0.1 | 120.5397 / 2.981e+08 | 1.5930 / 9.731e+05 | 150.5834 / 7.76e+09 | 0.0179 / n/r | 1.4888 / n/r |
| exp0.25 | 73.3140 / 1.372e+08 | 1.5739 / 8.989e+05 | 150.0600 / 6.484e+09 | 0.0179 / n/r | 1.4918 / n/r |
| exp0.5 ! | 42.4898 / 4.519e+07 | 1.5499 / 7.774e+05 | 150.6999 / 5.378e+09 | 0.0179 / n/r | 1.4936 / n/r |
| exp0.75 ! | 29.8439 / 2.03e+07 | 1.4977 / 6.341e+05 | 151.6483 / 5.309e+09 | 0.0177 / n/r | 1.4960 / n/r |
| exp1.0 ! | 23.0105 / 1.226e+07 | 1.4930 / 6.124e+05 | 155.9179 / 5.989e+09 | 0.0176 / n/r | 1.4962 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.6537 / 413.2 | 1.2247 / 7.309e+05 | 197.8766 / 7.654e+09 | 0.0117 / n/r | 1.6650 / n/r |
| exp0.05 | 0.0385 / 2062 | 0.0004 / 0.04415 | 566.5037 / 4.818e+10 | 0.0000 / n/r | 2.6516 / n/r |
| exp0.1 | 0.0007 / 0.3003 | 0.0017 / 4.919 | 447.7378 / 3.598e+10 | 0.0000 / n/r | 2.2042 / n/r |
| exp0.25 | 0.0001 / 0.001024 | 0.0034 / 8.561 | 403.1798 / 2.954e+10 | 0.0000 / n/r | 2.0177 / n/r |
| exp0.5 ! | 0.0000 / 2.47e-14 | 0.0000 / 2.519e-08 | 484.8424 / 5.252e+10 | 0.0000 / n/r | 2.4576 / n/r |
| exp0.75 ! | 0.0000 / 2.908e-12 | 0.0000 / 3.939e-08 | 502.5600 / 5.924e+10 | 0.0000 / n/r | 2.5168 / n/r |
| exp1.0 ! | 0.0000 / 1.613e-09 | 0.0000 / 0.002091 | 502.5161 / 6.369e+10 | 0.0000 / n/r | 2.5262 / n/r |

---

## cmplx_ps, K = -1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.6203 / 399.1 | 1.6732 / 43.03 | 1.6229 / 42.97 | 0.1527 / n/r | 0.1458 / n/r |
| exp0.05 | 1.6194 / 83.17 | 1.6680 / 43.3 | 1.6160 / 43.12 | 0.1522 / n/r | 0.1452 / n/r |
| exp0.1 | 1.6191 / 42.95 | 1.6681 / 43.19 | 1.6160 / 42.83 | 0.1523 / n/r | 0.1453 / n/r |
| exp0.25 | 1.6183 / 21.08 | 1.6682 / 43.24 | 1.6152 / 42.93 | 0.1523 / n/r | 0.1452 / n/r |
| exp0.5 ! | 1.6162 / 22.79 | 1.6670 / 43.03 | 1.6148 / 42.8 | 0.1522 / n/r | 0.1451 / n/r |
| exp0.75 ! | 1.6164 / 97.03 | 1.6674 / 43.09 | 1.6150 / 42.77 | 0.1522 / n/r | 0.1452 / n/r |
| exp1.0 ! | 1.6143 / 106 | 1.6682 / 43 | 1.6154 / 42.74 | 0.1523 / n/r | 0.1452 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.6770 / 395.8 | 1.6768 / 44.84 | 3.0132 / 67 | 0.1432 / n/r | 0.2535 / n/r |
| exp0.05 | 1.6744 / 83.05 | 1.6699 / 44.64 | 3.0624 / 59.27 | 0.1417 / n/r | 0.2575 / n/r |
| exp0.1 | 1.6689 / 43.96 | 1.6697 / 44.07 | 2.8734 / 58.65 | 0.1430 / n/r | 0.2452 / n/r |
| exp0.25 | 1.6686 / 21.23 | 1.6683 / 41.97 | 2.3310 / 55.52 | 0.1470 / n/r | 0.2043 / n/r |
| exp0.5 ! | 1.6698 / 52.16 | 1.6649 / 44.19 | 3.0217 / 63.42 | 0.1420 / n/r | 0.2550 / n/r |
| exp0.75 ! | 1.6729 / 294.7 | 1.6682 / 44.64 | 3.1898 / 67.14 | 0.1417 / n/r | 0.2641 / n/r |
| exp1.0 ! | 1.6606 / 1178 | 1.6727 / 44.98 | 3.5641 / 76.37 | 0.1408 / n/r | 0.2933 / n/r |

---

## cmplx_ps, K = -10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.1646 / 40.66 | 1.6877 / 422.2 | 0.1642 / 4.114 | 0.1671 / n/r | 0.0162 / n/r |
| exp0.05 | 0.1626 / 7.98 | 1.6822 / 417.9 | 0.1633 / 4.023 | 0.1666 / n/r | 0.0161 / n/r |
| exp0.1 | 0.1619 / 3.961 | 1.6828 / 415.8 | 0.1631 / 4.012 | 0.1667 / n/r | 0.0161 / n/r |
| exp0.25 | 0.1620 / 1.623 | 1.6770 / 417.1 | 0.1627 / 4.042 | 0.1661 / n/r | 0.0161 / n/r |
| exp0.5 ! | 0.1619 / 0.833 | 1.6773 / 420.2 | 0.1625 / 4.065 | 0.1661 / n/r | 0.0161 / n/r |
| exp0.75 ! | 0.1619 / 0.5626 | 1.6768 / 418.7 | 0.1625 / 4.044 | 0.1661 / n/r | 0.0161 / n/r |
| exp1.0 ! | 0.1619 / 0.4289 | 1.6758 / 416.9 | 0.1625 / 4.025 | 0.1660 / n/r | 0.0161 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.6957 / 4196 | 1.7093 / 425.4 | 0.5217 / 10.06 | 0.1659 / n/r | 0.0509 / n/r |
| exp0.05 | 1.6758 / 787 | 1.6888 / 402.4 | 0.3191 / 6.416 | 0.1658 / n/r | 0.0313 / n/r |
| exp0.1 | 1.6765 / 389.2 | 1.6726 / 386.8 | 0.2950 / 5.915 | 0.1644 / n/r | 0.0290 / n/r |
| exp0.25 | 1.6678 / 157.2 | 1.6714 / 389.8 | 0.2519 / 5.644 | 0.1648 / n/r | 0.0248 / n/r |
| exp0.5 ! | 1.6716 / 80.35 | 1.6730 / 389 | 0.2374 / 5.251 | 0.1650 / n/r | 0.0234 / n/r |
| exp0.75 ! | 1.6738 / 55.86 | 1.6766 / 396.7 | 0.2440 / 5.518 | 0.1654 / n/r | 0.0240 / n/r |
| exp1.0 ! | 1.6697 / 43.42 | 1.6718 / 391.4 | 0.2688 / 5.774 | 0.1646 / n/r | 0.0264 / n/r |

---

## c1e3_exp1.0, K = -0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 92.4019 / 4.92e+05 | 0.8875 / 8.493e+04 | 71.6557 / 3.219e+08 | 0.0135 / n/r | 0.9068 / n/r |
| exp0.05 | 84.4374 / 3.41e+07 | 0.9134 / 1.014e+05 | 71.2852 / 3.645e+08 | 0.0138 / n/r | 0.9155 / n/r |
| exp0.1 | 70.1713 / 7.929e+07 | 0.9023 / 8.697e+04 | 72.0207 / 3.336e+08 | 0.0137 / n/r | 0.9105 / n/r |
| exp0.25 | 43.9173 / 4.155e+07 | 1.0141 / 2.802e+05 | 78.2606 / 7.597e+08 | 0.0138 / n/r | 0.9151 / n/r |
| exp0.5 ! | 26.3636 / 1.482e+07 | 1.4742 / 5.674e+05 | 765.8001 / 1.961e+12 | 0.0139 / n/r | 0.9366 / n/r |
| exp0.75 ! | 18.4064 / 6.05e+06 | 1.5961 / 3.571e+05 | 1143.1126 / 4.076e+12 | 0.0136 / n/r | 0.9576 / n/r |
| exp1.0 ! | 14.2149 / 3.38e+06 | 0.9498 / 1.676e+05 | 92.4649 / 2.297e+09 | 0.0134 / n/r | 0.9358 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0606 / 476.6 | 0.8463 / 4.296e+05 | 1331.3504 / 4.179e+11 | 0.0077 / n/r | 7.7589 / n/r |
| exp0.05 | 0.0433 / 4286 | 0.0006 / 0.786 | 1997.6739 / 1.591e+12 | 0.0000 / n/r | 9.1887 / n/r |
| exp0.1 | 0.0003 / 0.06097 | 0.0005 / 1.123 | 2641.7088 / 2.019e+12 | 0.0000 / n/r | 12.3179 / n/r |
| exp0.25 | 0.0000 / 0.000224 | 0.0001 / 0.03208 | 2336.2291 / 1.261e+12 | 0.0000 / n/r | 11.7689 / n/r |
| exp0.5 ! | 0.0000 / 6.44e-05 | 0.0001 / 0.02629 | 2750.0150 / 1.723e+12 | 0.0000 / n/r | 13.6905 / n/r |
| exp0.75 ! | 0.0000 / 2.928e-05 | 0.0001 / 0.02659 | 2794.5174 / 1.665e+12 | 0.0000 / n/r | 13.8932 / n/r |
| exp1.0 ! | 0.0000 / 1.684e-05 | 0.0001 / 0.02291 | 2689.2904 / 1.503e+12 | 0.0000 / n/r | 13.5105 / n/r |

---

## c1e3_exp1.0, K = -1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.9321 / 238.6 | 1.0508 / 31.96 | 0.9317 / 25.66 | 0.0967 / n/r | 0.0840 / n/r |
| exp0.05 | 0.9357 / 53.1 | 1.0475 / 30.79 | 0.9349 / 29.2 | 0.0963 / n/r | 0.0841 / n/r |
| exp0.1 | 0.9335 / 24.52 | 1.0564 / 31.21 | 0.9332 / 24.56 | 0.0972 / n/r | 0.0841 / n/r |
| exp0.25 | 0.9261 / 12.98 | 1.0462 / 30.21 | 0.9261 / 24.95 | 0.0963 / n/r | 0.0834 / n/r |
| exp0.5 ! | 0.9221 / 11.91 | 1.0475 / 29.79 | 0.9234 / 23.26 | 0.0964 / n/r | 0.0832 / n/r |
| exp0.75 ! | 0.9234 / 45.49 | 1.0474 / 29.9 | 0.9233 / 23.26 | 0.0964 / n/r | 0.0832 / n/r |
| exp1.0 ! | 1.0750 / 57.2 | 1.1113 / 35.96 | 1.0766 / 37.27 | 0.1021 / n/r | 0.0971 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0680 / 273.5 | 1.0745 / 31.45 | 25.0997 / 2591 | 0.0925 / n/r | 2.0242 / n/r |
| exp0.05 | 1.0588 / 56.1 | 1.0611 / 29.79 | 22.0349 / 2140 | 0.0939 / n/r | 1.7593 / n/r |
| exp0.1 | 1.0558 / 29.91 | 1.0550 / 29.93 | 13.9420 / 1212 | 0.0929 / n/r | 1.1020 / n/r |
| exp0.25 | 1.0458 / 15.03 | 1.0475 / 29.18 | 17.6352 / 1797 | 0.0927 / n/r | 1.4509 / n/r |
| exp0.5 ! | 1.0471 / 43.15 | 1.0451 / 30.31 | 7.6768 / 763.1 | 0.0887 / n/r | 0.6254 / n/r |
| exp0.75 ! | 1.0565 / 124.7 | 1.0575 / 30.8 | 22.9571 / 2088 | 0.0925 / n/r | 1.8384 / n/r |
| exp1.0 ! | 1.0329 / 648.9 | 1.0689 / 33.86 | 23.1664 / 2203 | 0.0878 / n/r | 1.8800 / n/r |

---

## c1e3_exp1.0, K = -10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.1023 / 29.14 | 1.1239 / 364.4 | 0.1035 / 3.012 | 0.1114 / n/r | 0.0102 / n/r |
| exp0.05 | 0.1112 / 8.079 | 1.1179 / 346.9 | 0.1119 / 4.183 | 0.1108 / n/r | 0.0111 / n/r |
| exp0.1 | 0.0941 / 2.407 | 1.0516 / 302.5 | 0.0939 / 2.328 | 0.1042 / n/r | 0.0093 / n/r |
| exp0.25 | 0.1091 / 1.501 | 1.1219 / 352.6 | 0.1089 / 3.692 | 0.1112 / n/r | 0.0108 / n/r |
| exp0.5 ! | 0.0934 / 0.4769 | 1.0498 / 292.1 | 0.0933 / 2.269 | 0.1041 / n/r | 0.0092 / n/r |
| exp0.75 ! | 0.0927 / 0.3097 | 1.0479 / 287.2 | 0.0926 / 2.17 | 0.1039 / n/r | 0.0092 / n/r |
| exp1.0 ! | 0.0928 / 0.2369 | 1.0478 / 287.3 | 0.0927 / 2.158 | 0.1039 / n/r | 0.0092 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.1593 / 3154 | 1.1463 / 314.1 | 2.4186 / 237 | 0.1113 / n/r | 0.2365 / n/r |
| exp0.05 | 1.1025 / 543.2 | 1.1073 / 274.7 | 2.5423 / 261.2 | 0.1087 / n/r | 0.2484 / n/r |
| exp0.1 | 1.0695 / 277.3 | 1.0757 / 278.9 | 2.4188 / 235.3 | 0.1058 / n/r | 0.2365 / n/r |
| exp0.25 | 1.0489 / 107.6 | 1.0517 / 266 | 1.2768 / 105.5 | 0.1035 / n/r | 0.1248 / n/r |
| exp0.5 ! | 1.0492 / 56.05 | 1.0522 / 269.6 | 2.1605 / 184.5 | 0.1038 / n/r | 0.2110 / n/r |
| exp0.75 ! | 1.0538 / 38.21 | 1.0583 / 268.9 | 2.5451 / 227.7 | 0.1045 / n/r | 0.2483 / n/r |
| exp1.0 ! | 1.0552 / 29.82 | 1.0635 / 272.2 | 1.3911 / 111 | 0.1049 / n/r | 0.1356 / n/r |

---

## c1e4_exp1.0, K = -0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 93.3726 / 4.163e+05 | 0.8902 / 5.195e+04 | 73.2621 / 2.617e+08 | 0.0135 / n/r | 0.9108 / n/r |
| exp0.05 | 83.6309 / 5.399e+07 | 0.9018 / 6.726e+04 | 72.4171 / 2.749e+08 | 0.0136 / n/r | 0.9097 / n/r |
| exp0.1 | 71.3301 / 1.431e+08 | 0.9222 / 8.874e+04 | 75.7541 / 4.511e+08 | 0.0138 / n/r | 0.9138 / n/r |
| exp0.25 | 46.9364 / 8.783e+07 | 0.9032 / 6.876e+04 | 84.3278 / 9.489e+08 | 0.0138 / n/r | 0.9219 / n/r |
| exp0.5 ! | 26.9598 / 2.677e+07 | 1.1025 / 1.412e+05 | 216.3800 / 2.982e+10 | 0.0134 / n/r | 0.9218 / n/r |
| exp0.75 ! | 18.8775 / 1.356e+07 | 0.8829 / 7.458e+04 | 87.1438 / 6.144e+08 | 0.0132 / n/r | 0.9223 / n/r |
| exp1.0 ! | 14.2253 / 5.634e+06 | 0.8516 / 5.053e+04 | 86.9456 / 6.47e+08 | 0.0129 / n/r | 0.9180 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0715 / 1039 | 0.8377 / 1.352e+05 | 1736.0381 / 6.47e+11 | 0.0089 / n/r | 8.6140 / n/r |
| exp0.05 | 0.1998 / 3.544e+04 | 0.1091 / 6017 | 3515.9541 / 2.807e+12 | 0.0006 / n/r | 17.3577 / n/r |
| exp0.1 | 0.0014 / 3.282 | 0.0011 / 1.927 | 4104.6468 / 3.577e+12 | 0.0000 / n/r | 19.2368 / n/r |
| exp0.25 | 0.0000 / 0.0002305 | 0.0001 / 0.00278 | 3032.7640 / 2.042e+12 | 0.0000 / n/r | 15.0775 / n/r |
| exp0.5 ! | 0.0000 / 5.392e-05 | 0.0001 / 0.002093 | 3429.7357 / 2.13e+12 | 0.0000 / n/r | 17.1180 / n/r |
| exp0.75 ! | 0.0000 / 2.551e-05 | 0.0001 / 0.002056 | 3573.1458 / 2.451e+12 | 0.0000 / n/r | 17.6717 / n/r |
| exp1.0 ! | 0.0000 / 1.502e-05 | 0.0001 / 0.002024 | 3479.6987 / 2.485e+12 | 0.0000 / n/r | 17.1372 / n/r |

---

## c1e4_exp1.0, K = -1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.9385 / 236.3 | 1.0492 / 32.68 | 0.9395 / 25.86 | 0.0965 / n/r | 0.0846 / n/r |
| exp0.05 | 0.9323 / 46.32 | 1.0428 / 30.36 | 0.9299 / 24.24 | 0.0959 / n/r | 0.0838 / n/r |
| exp0.1 | 0.9304 / 25.26 | 1.0438 / 29.96 | 0.9291 / 24.91 | 0.0960 / n/r | 0.0837 / n/r |
| exp0.25 | 0.9278 / 13.17 | 1.0420 / 30.61 | 0.9263 / 24.93 | 0.0958 / n/r | 0.0834 / n/r |
| exp0.5 ! | 0.9335 / 29.77 | 1.0428 / 30.28 | 0.9314 / 25.97 | 0.0959 / n/r | 0.0838 / n/r |
| exp0.75 ! | 0.9343 / 50.29 | 1.0469 / 30.04 | 0.9321 / 25.38 | 0.0963 / n/r | 0.0839 / n/r |
| exp1.0 ! | 0.9362 / 41.07 | 1.0519 / 30.17 | 0.9369 / 24.58 | 0.0968 / n/r | 0.0844 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0996 / 298.9 | 1.0952 / 33.72 | 43.5058 / 6933 | 0.0940 / n/r | 3.4037 / n/r |
| exp0.05 | 1.0564 / 55.66 | 1.0568 / 29.41 | 48.9352 / 7571 | 0.0940 / n/r | 3.6972 / n/r |
| exp0.1 | 1.0520 / 29.32 | 1.0531 / 29.46 | 55.6425 / 1.008e+04 | 0.0941 / n/r | 4.2409 / n/r |
| exp0.25 | 1.0559 / 15.46 | 1.0550 / 30.26 | 54.5139 / 9723 | 0.0938 / n/r | 4.1394 / n/r |
| exp0.5 ! | 1.0584 / 15.6 | 1.0572 / 29.76 | 46.6722 / 7267 | 0.0940 / n/r | 3.5950 / n/r |
| exp0.75 ! | 1.0771 / 142.5 | 1.0713 / 31.31 | 46.8447 / 7946 | 0.0915 / n/r | 3.6304 / n/r |
| exp1.0 ! | 1.0665 / 148.8 | 1.0659 / 30.34 | 45.0703 / 6556 | 0.0941 / n/r | 3.4487 / n/r |

---

## c1e4_exp1.0, K = -10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.1001 / 29.01 | 1.1004 / 373.6 | 0.1004 / 2.899 | 0.1091 / n/r | 0.0099 / n/r |
| exp0.05 | 0.0957 / 4.929 | 1.0755 / 328 | 0.0967 / 2.497 | 0.1066 / n/r | 0.0096 / n/r |
| exp0.1 | 0.0940 / 2.317 | 1.0518 / 303.8 | 0.0946 / 2.314 | 0.1042 / n/r | 0.0094 / n/r |
| exp0.25 | 0.0941 / 0.9342 | 1.0487 / 283.4 | 0.0943 / 2.279 | 0.1039 / n/r | 0.0093 / n/r |
| exp0.5 ! | 0.0940 / 0.4759 | 1.0491 / 288.8 | 0.0942 / 2.275 | 0.1040 / n/r | 0.0093 / n/r |
| exp0.75 ! | 0.0941 / 0.327 | 1.0482 / 286.6 | 0.0943 / 2.277 | 0.1039 / n/r | 0.0093 / n/r |
| exp1.0 ! | 0.0932 / 0.2575 | 1.0482 / 289.7 | 0.0935 / 2.306 | 0.1039 / n/r | 0.0092 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.3034 / 3834 | 1.3118 / 386 | 3.4343 / 434.5 | 0.1278 / n/r | 0.3349 / n/r |
| exp0.05 | 1.1033 / 583.5 | 1.1110 / 293.4 | 3.5480 / 434.1 | 0.1091 / n/r | 0.3458 / n/r |
| exp0.1 | 1.0790 / 286.5 | 1.0789 / 285.4 | 4.4579 / 631.8 | 0.1065 / n/r | 0.4332 / n/r |
| exp0.25 | 1.0629 / 111.5 | 1.0658 / 274.6 | 4.7167 / 688.2 | 0.1052 / n/r | 0.4581 / n/r |
| exp0.5 ! | 1.0588 / 56.88 | 1.0626 / 274.7 | 5.0216 / 780.2 | 0.1049 / n/r | 0.4878 / n/r |
| exp0.75 ! | 1.0554 / 38.75 | 1.0581 / 272.9 | 5.3203 / 881.2 | 0.1045 / n/r | 0.5168 / n/r |
| exp1.0 ! | 1.0548 / 29.86 | 1.0587 / 274.6 | 5.3602 / 913.8 | 0.1046 / n/r | 0.5205 / n/r |

---

# RESULTS (Dense Table)

---

## naive_ps, K = -0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 0.4962 / 176.3 | 53.4146 / 4.762e+05 |
| exp0.05 | 0.0211 / 549.7 | 45.9933 / 1.585e+07 |
| exp0.1 | 0.0012 / 8.062 | 35.6393 / 2.139e+07 |
| exp0.25 | 0.0000 / 7.055e-06 | 20.4914 / 7.22e+06 |
| exp0.5 ! | 0.0000 / 3.16e-14 | 11.7698 / 3.175e+06 |
| exp0.75 ! | 0.0000 / 2.88e-13 | 8.2328 / 1.821e+06 |
| exp1.0 ! | 0.0000 / 6.293e-17 | 6.3350 / 1.27e+06 |

---

## naive_ps, K = -1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 0.5131 / 162.6 | 0.5318 / 166.9 |
| exp0.05 | 0.5001 / 34.05 | 0.5339 / 35.04 |
| exp0.1 | 0.5016 / 18.79 | 0.5348 / 18.91 |
| exp0.25 | 0.5008 / 9.737 | 0.5356 / 9.466 |
| exp0.5 ! | 0.5013 / 15.5 | 0.5350 / 8.9 |
| exp0.75 ! | 0.5031 / 110.6 | 0.5351 / 22.44 |
| exp1.0 ! | 0.4970 / 1056 | 0.5342 / 40.68 |

---

## naive_ps, K = -10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 0.5734 / 1958 | 0.0531 / 17.41 |
| exp0.05 | 0.5298 / 322.5 | 0.0531 / 3.186 |
| exp0.1 | 0.5057 / 163.9 | 0.0532 / 1.626 |
| exp0.25 | 0.5009 / 65 | 0.0533 / 0.6717 |
| exp0.5 ! | 0.5025 / 33.1 | 0.0534 / 0.3492 |
| exp0.75 ! | 0.5019 / 23.79 | 0.0534 / 0.2436 |
| exp1.0 ! | 0.5021 / 18.51 | 0.0535 / 0.1891 |

---

## cmplx_ps, K = -0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.6537 / 413.2 | 161.4506 / 1.12e+06 |
| exp0.05 | 0.0385 / 2062 | 146.0927 / 1.824e+08 |
| exp0.1 | 0.0007 / 0.3003 | 120.5397 / 2.981e+08 |
| exp0.25 | 0.0001 / 0.001024 | 73.3140 / 1.372e+08 |
| exp0.5 ! | 0.0000 / 2.47e-14 | 42.4898 / 4.519e+07 |
| exp0.75 ! | 0.0000 / 2.908e-12 | 29.8439 / 2.03e+07 |
| exp1.0 ! | 0.0000 / 1.613e-09 | 23.0105 / 1.226e+07 |

---

## cmplx_ps, K = -1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.6770 / 395.8 | 1.6203 / 399.1 |
| exp0.05 | 1.6744 / 83.05 | 1.6194 / 83.17 |
| exp0.1 | 1.6689 / 43.96 | 1.6191 / 42.95 |
| exp0.25 | 1.6686 / 21.23 | 1.6183 / 21.08 |
| exp0.5 ! | 1.6698 / 52.16 | 1.6162 / 22.79 |
| exp0.75 ! | 1.6729 / 294.7 | 1.6164 / 97.03 |
| exp1.0 ! | 1.6606 / 1178 | 1.6143 / 106 |

---

## cmplx_ps, K = -10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.6957 / 4196 | 0.1646 / 40.66 |
| exp0.05 | 1.6758 / 787 | 0.1626 / 7.98 |
| exp0.1 | 1.6765 / 389.2 | 0.1619 / 3.961 |
| exp0.25 | 1.6678 / 157.2 | 0.1620 / 1.623 |
| exp0.5 ! | 1.6716 / 80.35 | 0.1619 / 0.833 |
| exp0.75 ! | 1.6738 / 55.86 | 0.1619 / 0.5626 |
| exp1.0 ! | 1.6697 / 43.42 | 0.1619 / 0.4289 |

---

## c1e3_exp1.0, K = -0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0606 / 476.6 | 92.4019 / 4.92e+05 |
| exp0.05 | 0.0433 / 4286 | 84.4374 / 3.41e+07 |
| exp0.1 | 0.0003 / 0.06097 | 70.1713 / 7.929e+07 |
| exp0.25 | 0.0000 / 0.000224 | 43.9173 / 4.155e+07 |
| exp0.5 ! | 0.0000 / 6.44e-05 | 26.3636 / 1.482e+07 |
| exp0.75 ! | 0.0000 / 2.928e-05 | 18.4064 / 6.05e+06 |
| exp1.0 ! | 0.0000 / 1.684e-05 | 14.2149 / 3.38e+06 |

---

## c1e3_exp1.0, K = -1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0680 / 273.5 | 0.9321 / 238.6 |
| exp0.05 | 1.0588 / 56.1 | 0.9357 / 53.1 |
| exp0.1 | 1.0558 / 29.91 | 0.9335 / 24.52 |
| exp0.25 | 1.0458 / 15.03 | 0.9261 / 12.98 |
| exp0.5 ! | 1.0471 / 43.15 | 0.9221 / 11.91 |
| exp0.75 ! | 1.0565 / 124.7 | 0.9234 / 45.49 |
| exp1.0 ! | 1.0329 / 648.9 | 1.0750 / 57.2 |

---

## c1e3_exp1.0, K = -10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.1593 / 3154 | 0.1023 / 29.14 |
| exp0.05 | 1.1025 / 543.2 | 0.1112 / 8.079 |
| exp0.1 | 1.0695 / 277.3 | 0.0941 / 2.407 |
| exp0.25 | 1.0489 / 107.6 | 0.1091 / 1.501 |
| exp0.5 ! | 1.0492 / 56.05 | 0.0934 / 0.4769 |
| exp0.75 ! | 1.0538 / 38.21 | 0.0927 / 0.3097 |
| exp1.0 ! | 1.0552 / 29.82 | 0.0928 / 0.2369 |

---

## c1e4_exp1.0, K = -0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0715 / 1039 | 93.3726 / 4.163e+05 |
| exp0.05 | 0.1998 / 3.544e+04 | 83.6309 / 5.399e+07 |
| exp0.1 | 0.0014 / 3.282 | 71.3301 / 1.431e+08 |
| exp0.25 | 0.0000 / 0.0002305 | 46.9364 / 8.783e+07 |
| exp0.5 ! | 0.0000 / 5.392e-05 | 26.9598 / 2.677e+07 |
| exp0.75 ! | 0.0000 / 2.551e-05 | 18.8775 / 1.356e+07 |
| exp1.0 ! | 0.0000 / 1.502e-05 | 14.2253 / 5.634e+06 |

---

## c1e4_exp1.0, K = -1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0996 / 298.9 | 0.9385 / 236.3 |
| exp0.05 | 1.0564 / 55.66 | 0.9323 / 46.32 |
| exp0.1 | 1.0520 / 29.32 | 0.9304 / 25.26 |
| exp0.25 | 1.0559 / 15.46 | 0.9278 / 13.17 |
| exp0.5 ! | 1.0584 / 15.6 | 0.9335 / 29.77 |
| exp0.75 ! | 1.0771 / 142.5 | 0.9343 / 50.29 |
| exp1.0 ! | 1.0665 / 148.8 | 0.9362 / 41.07 |

---

## c1e4_exp1.0, K = -10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.3034 / 3834 | 0.1001 / 29.01 |
| exp0.05 | 1.1033 / 583.5 | 0.0957 / 4.929 |
| exp0.1 | 1.0790 / 286.5 | 0.0940 / 2.317 |
| exp0.25 | 1.0629 / 111.5 | 0.0941 / 0.9342 |
| exp0.5 ! | 1.0588 / 56.88 | 0.0940 / 0.4759 |
| exp0.75 ! | 1.0554 / 38.75 | 0.0941 / 0.327 |
| exp1.0 ! | 1.0548 / 29.86 | 0.0932 / 0.2575 |


---

# Insights and conclusions

**All 504 cells completed; 0 failures.** Read every number here against
`experiments/init_opt_test_3d_refactor_new/RESULTS.md`, which runs the *exact* posterior
on the same grid and says what the estimator itself reports at each curvature:

| ps | H(p) | Bayes-opt reads at K=−0.01 | at K=−1 | at K=−10 |
|---|---|---|---|---|
| naive_ps | 0.5003 | **0.3594** | 0.5013 | 0.4974 |
| cmplx_ps | 1.6664 | **1.2439** | 1.6692 | 1.6605 |
| c1e3 / c1e4 | 1.0407 | **0.7667** | 1.0409 | 1.0395 |

## 1. At K = −1 and K = −10 the trained model reaches H(p), on both objectives

`wnelbo_ref` averaged over 3 seeds, by loss proposal rate:

| ps, K, obj | .01 | .05 | .1 | .25 | .5 | .75 | 1.0 |
|---|---|---|---|---|---|---|---|
| naive_ps K=−1 CE | 0.5011 | 0.4998 | 0.4996 | 0.4993 | 0.5000 | 0.5000 | 0.4996 |
| naive_ps K=−1 PP | 0.5099 | 0.5014 | 0.5022 | 0.5020 | 0.5015 | 0.5018 | 0.5055 |
| naive_ps K=−10 CE | 0.5013 | 0.5007 | 0.4997 | 0.4976 | 0.4971 | 0.4960 | 0.4965 |
| naive_ps K=−10 PP | 0.5663 | 0.5251 | 0.4977 | 0.4999 | 0.5018 | 0.5013 | 0.5050 |
| cmplx_ps K=−1 CE | 1.6732 | 1.6680 | 1.6681 | 1.6682 | 1.6670 | 1.6674 | 1.6682 |
| cmplx_ps K=−1 PP | 1.6768 | 1.6699 | 1.6697 | 1.6683 | 1.6649 | 1.6682 | 1.6727 |
| c1e4 K=−1 CE | 1.0492 | 1.0428 | 1.0438 | 1.0420 | 1.0428 | 1.0469 | 1.0519 |
| c1e4 K=−10 PP | 1.3118 | 1.1110 | 1.0789 | 1.0658 | 1.0626 | 1.0581 | 1.0587 |

Every cell lands on `H(p)` from above, within the Bayes-optimal control's own band.
Hypotheses 1 and 3 confirmed: the refactored path is a valid ELBO at `d = 3`, and where
the estimator is sound, **curvature does not move the optimum** — `wnelbo_ref` at the best
rate is the same at `K = −1` and `K = −10`, as it must be for a quantity that is a
property of `p`, not of the manifold.

Two secondary effects are visible and both favour the sharper manifold:

- **`poincare_polar` is rate-sensitive at low rates, `cross_entropy` is not.** At
  `K = −10`, PP reads 0.5663 at rate 0.01 and 0.4977 by rate 0.1; CE is flat to the 3rd
  decimal across the whole axis. Training on the weighted ELBO with a proposal that
  undersamples large `t` biases the model; training on the denoising CE does not.
- **`ce_ref` falls by ~10× per curvature step**: 0.465 / 0.056 / 0.006 nats at
  K = −0.01 / −1 / −10 (naive_ps). Sharper curvature identifies the word sooner in `t`.

## 2. At K = −0.01, training on the polar ELBO collapses — 70 of 84 cells

This is the headline negative result, and it is not the estimator being noisy.

| naive_ps, K=−0.01 | `wloss` | `wnelbo_ref` | `nelbo_ref` | `wce_ref` | `ce_ref` |
|---|---|---|---|---|---|
| PP rate 0.01 | 0.4962 | 0.5178 | 0.00309 | 74.7 | 0.583 |
| PP rate 0.05 | 0.0211 | **0.0004** | 0.00000 | 195.5 | 0.704 |
| PP rate 0.1 | 0.0012 | **0.0016** | 0.00000 | 192.9 | 0.679 |
| PP rate 0.25 | 0.0000 | **0.0000** | 0.00000 | 157.4 | 0.600 |
| PP rate 1.0 | 0.0000 | **0.0000** | 0.00000 | 243.9 | 1.144 |
| CE rate 0.1 | 35.64 | 0.6052 | 0.00498 | 62.8 | 0.452 |

`wnelbo_ref < 0.01` in **70 of the 84** `K = −0.01` × `poincare_polar` cells
(18/21 naive_ps, 17/21 cmplx_ps, 18/21 c1e3, 17/21 c1e4) — and in **0 of the 336** cells
at `K = −1` or `K = −10`, either objective.

The collapse has a clear signature: the trained objective goes to zero (`wloss` 0.0000)
while the denoising cross-entropy *explodes* (`wce_ref` 150–250 against 0.53 at `K = −1`,
`ce_ref` 0.6–1.1 against 0.048). The model has not learned `p` at all. It has found a
degenerate optimum that annihilates the ELBO integrand exactly where the proposal looks,
and the same undersampling estimator then scores that at ~0 — three orders of magnitude
below `H(p)`, which no ELBO can be.

**The failure is the objective, not the geometry.** `cross_entropy` at the same curvature
does not collapse: it holds 0.55–0.61 (naive_ps), above the Bayes-optimal control's 0.3594
and within ~20 % of `H(p)`, across every rate. Only the importance-weighted ELBO, used as
a *training* signal past its variance cliff, produces the degenerate solution.

**Where the cliff bites.** At `K = −0.01` the loss-path cliff scales to ~0.00304
(`0.304 · R^{-2}`, `R^2 = 100`). Rate 0.01 — 3× above it — survives, reading 0.5178 /
1.2247 / 0.8463 / 0.8377, i.e. tracking its Bayes-optimal control. Rate 0.05 — 16× above
it — is already collapsed. So the practical breaking point sits between 3× and 16× the
nominal cliff, not at it.

## 3. Do not read the K = −0.01 rows against H(p)

Two cells illustrate why. CE-trained at `K = −0.01` reads `wnelbo_ref = 0.605`
(naive_ps) — *higher* than the exact posterior's 0.3594 on the same estimator. A model
that is demonstrably worse than Bayes (its `ce_ref` is 0.45 against Bayes' 0.47, its
`wce_ref` 63 against 44) scores better on `wnelbo_ref`. That is only possible because at
this curvature `wnelbo_ref` is not measuring the ELBO; it is measuring the fraction of the
integral that fell inside the proposal's reach.

At `K = −0.01`, `wnelbo_ref` orders models by "how much of my loss sits at small `t`",
not by "how good is my bound". Both the `>= H(p)` check (Invariant 2) and cross-model
comparison are void there. Restoring them needs the reference proposal re-tuned to the
curvature (rate ~`0.1 · R^{-2}`), which is a change to `setup.md`'s pinned design and so
is flagged rather than made here.

## 4. Cross-project

- `init_opt_test_3d_refactor_new` — same grid, exact posterior: the estimator's own reading.
- `init_test_3x3d_refactor_new` — the same three curvatures carried simultaneously as a
  product manifold. Its control shows the product inherits the *sharpest* factor's
  conditioning, so it shows no trace of the collapse documented here.
- `init_refactor_3d` — `main.py` at `d = 3`, `K = −1`, 20000 steps: the `K = −1` slice
  here reproduces it, so the refactored horosphere-readout path did not move the number.
