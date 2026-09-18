# init_test_log_vce_3x3d_refactor_new results

- runs collected: **630** / 630 (100%) — run dirs without test_metrics.json: 0
- H(naive_ps) = **0.5003** — wnelbo_ref is bounded below by this
- H(cmplx_ps) = **1.6664** — wnelbo_ref is bounded below by this
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
  stratified_exp(0.1) and stays valid, but training there is materially noisier.
- `wce_ref` is dominated by rare extremes; treat its spread as indicative only.

---

# Results (Full Table)

---

## naive_ps, K = -0.01x-0.01x-0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 7.0528 / 1.335e+04 | 0.5085 / 5156 | 18.3373 / 8.088e+07 | 0.0117 / n/r | 0.3846 / n/r |
| stratified_exp0.05 | 8.2755 / 1.796e+06 | 0.5227 / 8915 | 19.2451 / 1.022e+08 | 0.0118 / n/r | 0.3845 / n/r |
| stratified_exp0.1 | 7.5392 / 1.02e+07 | 0.5311 / 2.402e+04 | 19.3907 / 1.053e+08 | 0.0119 / n/r | 0.3838 / n/r |
| stratified_exp0.25 | 5.9529 / 1.04e+07 | 0.5254 / 3.914e+04 | 25.5067 / 2.143e+08 | 0.0120 / n/r | 0.3854 / n/r |
| stratified_exp0.5 ! | 3.2997 / 6.383e+06 | 0.4959 / 7.069e+04 | 48.1768 / 1.358e+09 | 0.0114 / n/r | 0.3946 / n/r |
| stratified_exp0.75 ! | 2.0559 / 2.024e+06 | 0.4801 / 4.264e+04 | 38.6754 / 3.269e+08 | 0.0113 / n/r | 0.4042 / n/r |
| stratified_exp1.0 ! | 1.5250 / 1.097e+06 | 0.4907 / 4.414e+04 | 39.2567 / 3.528e+08 | 0.0115 / n/r | 0.4108 / n/r |

---

## naive_ps, K = -0.01x-10.0x-1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 31.5117 / 5.835e+07 | 0.6895 / 400.6 | 0.1006 / 8.948 | 0.0682 / n/r | 0.0099 / n/r |
| stratified_exp0.05 | 18.2699 / 9.339e+06 | 0.5598 / 263 | 0.0575 / 2.808 | 0.0554 / n/r | 0.0057 / n/r |
| stratified_exp0.1 | 14.7142 / 6.053e+06 | 0.5233 / 200.4 | 0.0500 / 1.738 | 0.0518 / n/r | 0.0049 / n/r |
| stratified_exp0.25 | 13.1061 / 6.899e+05 | 0.5174 / 202.1 | 0.0494 / 1.699 | 0.0512 / n/r | 0.0049 / n/r |
| stratified_exp0.5 ! | 12.9298 / 3.381e+06 | 0.4992 / 196.8 | 0.0476 / 1.598 | 0.0494 / n/r | 0.0047 / n/r |
| stratified_exp0.75 ! | 12.4301 / 5.097e+05 | 0.4973 / 192.6 | 0.0474 / 1.553 | 0.0493 / n/r | 0.0047 / n/r |
| stratified_exp1.0 ! | 13.0066 / 4.275e+06 | 0.4943 / 190.2 | 0.0471 / 1.531 | 0.0490 / n/r | 0.0047 / n/r |

---

## naive_ps, K = -0.05x-0.05x-0.05

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 7.1396 / 1.696e+04 | 0.5025 / 6.444 | 3.2469 / 281.1 | 0.0306 / n/r | 0.1965 / n/r |
| stratified_exp0.05 | 7.0449 / 1.025e+04 | 0.5012 / 6.235 | 3.2424 / 272 | 0.0305 / n/r | 0.1962 / n/r |
| stratified_exp0.1 | 8.7725 / 8.794e+06 | 0.5022 / 6.292 | 3.2534 / 286.3 | 0.0305 / n/r | 0.1963 / n/r |
| stratified_exp0.25 | 8.1848 / 2.322e+06 | 0.5043 / 7.095 | 3.3461 / 381.1 | 0.0305 / n/r | 0.1977 / n/r |
| stratified_exp0.5 ! | 8.9787 / 3.168e+07 | 0.5062 / 8.323 | 3.5231 / 525.5 | 0.0304 / n/r | 0.2005 / n/r |
| stratified_exp0.75 ! | 7.5589 / 9.675e+06 | 0.5099 / 29 | 3.9739 / 4880 | 0.0299 / n/r | 0.2065 / n/r |
| stratified_exp1.0 ! | 5.9142 / 4.579e+06 | 0.5138 / 20.93 | 4.4853 / 3327 | 0.0295 / n/r | 0.2140 / n/r |

---

## naive_ps, K = -0.1x-0.1x-0.1

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 7.2276 / 1.371e+05 | 0.5018 / 6.823 | 1.6242 / 72.12 | 0.0380 / n/r | 0.1221 / n/r |
| stratified_exp0.05 | 7.0449 / 1.341e+04 | 0.5009 / 6.782 | 1.6185 / 71.18 | 0.0379 / n/r | 0.1219 / n/r |
| stratified_exp0.1 | 7.0811 / 1.368e+04 | 0.5017 / 6.746 | 1.6208 / 70.5 | 0.0380 / n/r | 0.1221 / n/r |
| stratified_exp0.25 | 8.0914 / 1.711e+06 | 0.5021 / 6.774 | 1.6373 / 73.3 | 0.0380 / n/r | 0.1227 / n/r |
| stratified_exp0.5 ! | 8.1194 / 7.917e+05 | 0.5037 / 6.913 | 1.6755 / 80.41 | 0.0379 / n/r | 0.1240 / n/r |
| stratified_exp0.75 ! | 8.2751 / 1.184e+07 | 0.5049 / 6.966 | 1.7104 / 86.72 | 0.0379 / n/r | 0.1253 / n/r |
| stratified_exp1.0 ! | 8.3648 / 2.737e+07 | 0.5056 / 6.817 | 1.7590 / 92.13 | 0.0378 / n/r | 0.1268 / n/r |

---

## naive_ps, K = -0.5x-0.5x-0.5

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 8.0872 / 6.226e+05 | 0.5139 / 27.76 | 0.3356 / 11.95 | 0.0482 / n/r | 0.0314 / n/r |
| stratified_exp0.05 | 7.2445 / 1.409e+05 | 0.5015 / 26 | 0.3245 / 10.55 | 0.0471 / n/r | 0.0304 / n/r |
| stratified_exp0.1 | 7.1407 / 1.606e+04 | 0.5009 / 26.33 | 0.3244 / 10.67 | 0.0470 / n/r | 0.0304 / n/r |
| stratified_exp0.25 | 7.0715 / 3.374e+04 | 0.5000 / 26.08 | 0.3229 / 10.46 | 0.0470 / n/r | 0.0303 / n/r |
| stratified_exp0.5 ! | 6.9744 / 7160 | 0.4993 / 25.89 | 0.3225 / 10.39 | 0.0469 / n/r | 0.0302 / n/r |
| stratified_exp0.75 ! | 7.0934 / 2.155e+04 | 0.4998 / 26.11 | 0.3235 / 10.51 | 0.0469 / n/r | 0.0303 / n/r |
| stratified_exp1.0 ! | 8.4379 / 6.524e+06 | 0.5015 / 26.47 | 0.3254 / 10.77 | 0.0471 / n/r | 0.0305 / n/r |

---

## naive_ps, K = -1.0x-1.0x-1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 8.1569 / 5.85e+05 | 0.5357 / 63.47 | 0.1804 / 7.794 | 0.0519 / n/r | 0.0174 / n/r |
| stratified_exp0.05 | 7.3303 / 8.527e+04 | 0.5022 / 51.34 | 0.1636 / 5.278 | 0.0486 / n/r | 0.0158 / n/r |
| stratified_exp0.1 | 7.1355 / 1.294e+05 | 0.5006 / 50.59 | 0.1619 / 5.105 | 0.0485 / n/r | 0.0157 / n/r |
| stratified_exp0.25 | 7.0806 / 1.234e+04 | 0.4994 / 51.38 | 0.1615 / 5.17 | 0.0484 / n/r | 0.0156 / n/r |
| stratified_exp0.5 ! | 7.0337 / 9889 | 0.5000 / 51.06 | 0.1616 / 5.122 | 0.0484 / n/r | 0.0156 / n/r |
| stratified_exp0.75 ! | 7.0273 / 9579 | 0.5003 / 50.22 | 0.1615 / 5.002 | 0.0485 / n/r | 0.0156 / n/r |
| stratified_exp1.0 ! | 7.0528 / 1.335e+04 | 0.5002 / 51.57 | 0.1616 / 5.189 | 0.0484 / n/r | 0.0156 / n/r |

---

## naive_ps, K = -2.0x-2.0x-2.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 12.5735 / 7.437e+07 | 0.5899 / 162.6 | 0.1147 / 7.137 | 0.0580 / n/r | 0.0113 / n/r |
| stratified_exp0.05 | 7.8222 / 5.058e+05 | 0.5070 / 102.2 | 0.0828 / 2.697 | 0.0499 / n/r | 0.0081 / n/r |
| stratified_exp0.1 | 7.3824 / 9.558e+04 | 0.5023 / 98.19 | 0.0814 / 2.483 | 0.0494 / n/r | 0.0080 / n/r |
| stratified_exp0.25 | 7.1522 / 3.364e+04 | 0.5000 / 101.1 | 0.0810 / 2.546 | 0.0492 / n/r | 0.0080 / n/r |
| stratified_exp0.5 ! | 7.1022 / 1.749e+04 | 0.4990 / 100.2 | 0.0805 / 2.492 | 0.0491 / n/r | 0.0079 / n/r |
| stratified_exp0.75 ! | 7.0528 / 2.831e+04 | 0.4993 / 98.08 | 0.0805 / 2.436 | 0.0491 / n/r | 0.0079 / n/r |
| stratified_exp1.0 ! | 7.0300 / 9475 | 0.4992 / 100.9 | 0.0806 / 2.526 | 0.0491 / n/r | 0.0079 / n/r |

---

## naive_ps, K = -3.0x-3.0x-3.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 11.9825 / 1.909e+06 | 0.6278 / 271.1 | 0.0895 / 6.424 | 0.0621 / n/r | 0.0089 / n/r |
| stratified_exp0.05 | 7.7869 / 4.704e+05 | 0.5125 / 157.9 | 0.0556 / 1.867 | 0.0507 / n/r | 0.0055 / n/r |
| stratified_exp0.1 | 7.9379 / 4.713e+05 | 0.5086 / 145 | 0.0549 / 1.642 | 0.0503 / n/r | 0.0054 / n/r |
| stratified_exp0.25 | 7.5214 / 1.786e+05 | 0.4998 / 144.9 | 0.0541 / 1.619 | 0.0494 / n/r | 0.0054 / n/r |
| stratified_exp0.5 ! | 7.2499 / 1.234e+05 | 0.4989 / 148.3 | 0.0537 / 1.635 | 0.0494 / n/r | 0.0053 / n/r |
| stratified_exp0.75 ! | 7.0626 / 1.093e+04 | 0.4982 / 149.9 | 0.0536 / 1.655 | 0.0493 / n/r | 0.0053 / n/r |
| stratified_exp1.0 ! | 7.0614 / 1.152e+04 | 0.4979 / 151.1 | 0.0535 / 1.668 | 0.0493 / n/r | 0.0053 / n/r |

---

## naive_ps, K = -4.0x-4.0x-4.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 13.2412 / 6.785e+06 | 0.6340 / 363.7 | 0.0700 / 5.217 | 0.0629 / n/r | 0.0069 / n/r |
| stratified_exp0.05 | 9.9582 / 2.231e+07 | 0.5190 / 226.3 | 0.0427 / 1.592 | 0.0515 / n/r | 0.0042 / n/r |
| stratified_exp0.1 | 9.5045 / 1.213e+07 | 0.4996 / 199.8 | 0.0407 / 1.304 | 0.0496 / n/r | 0.0040 / n/r |
| stratified_exp0.25 | 7.3217 / 8.466e+04 | 0.5025 / 195.3 | 0.0405 / 1.216 | 0.0498 / n/r | 0.0040 / n/r |
| stratified_exp0.5 ! | 7.1841 / 8.23e+04 | 0.4958 / 203.6 | 0.0400 / 1.274 | 0.0492 / n/r | 0.0040 / n/r |
| stratified_exp0.75 ! | 7.1182 / 1.934e+04 | 0.4971 / 200.9 | 0.0400 / 1.247 | 0.0493 / n/r | 0.0040 / n/r |
| stratified_exp1.0 ! | 7.0999 / 1.877e+04 | 0.4968 / 201.3 | 0.0400 / 1.246 | 0.0493 / n/r | 0.0040 / n/r |

---

## naive_ps, K = -10.0x-10.0x-10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 15.1290 / 8.727e+06 | 0.6493 / 917 | 0.0314 / 2.608 | 0.0647 / n/r | 0.0031 / n/r |
| stratified_exp0.05 | 13.0046 / 7.444e+07 | 0.5903 / 815.1 | 0.0237 / 1.535 | 0.0588 / n/r | 0.0024 / n/r |
| stratified_exp0.1 | 8.1908 / 5.636e+05 | 0.5285 / 605.9 | 0.0177 / 0.7346 | 0.0527 / n/r | 0.0018 / n/r |
| stratified_exp0.25 | 10.1208 / 1.517e+07 | 0.5023 / 510.3 | 0.0163 / 0.5365 | 0.0501 / n/r | 0.0016 / n/r |
| stratified_exp0.5 ! | 7.3303 / 8.527e+04 | 0.4996 / 498.6 | 0.0161 / 0.4989 | 0.0498 / n/r | 0.0016 / n/r |
| stratified_exp0.75 ! | 7.4858 / 3.287e+05 | 0.4991 / 492.3 | 0.0161 / 0.4908 | 0.0497 / n/r | 0.0016 / n/r |
| stratified_exp1.0 ! | 7.1355 / 1.294e+05 | 0.4939 / 485.9 | 0.0159 / 0.4815 | 0.0492 / n/r | 0.0016 / n/r |

---

## cmplx_ps, K = -0.01x-0.01x-0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 20.4915 / 1.122e+05 | 1.7416 / 1.306e+05 | 53.4278 / 2.82e+08 | 0.0434 / n/r | 1.2356 / n/r |
| stratified_exp0.05 | 23.9512 / 1.793e+07 | 1.6824 / 1.462e+04 | 52.4815 / 9.559e+07 | 0.0436 / n/r | 1.2371 / n/r |
| stratified_exp0.1 | 20.7132 / 1.338e+07 | 1.6704 / 1.495e+04 | 52.8782 / 6.884e+07 | 0.0437 / n/r | 1.2477 / n/r |
| stratified_exp0.25 | 14.0968 / 2.044e+07 | 1.6955 / 2.595e+04 | 59.4728 / 8.9e+07 | 0.0434 / n/r | 1.2617 / n/r |
| stratified_exp0.5 ! | 14.4425 / 3.857e+08 | 1.6142 / 2.359e+04 | 88.9247 / 5.254e+08 | 0.0405 / n/r | 1.2955 / n/r |
| stratified_exp0.75 ! | 29.9736 / 7.029e+09 | 1.5288 / 2.664e+04 | 92.5559 / 2.754e+08 | 0.0385 / n/r | 1.3237 / n/r |
| stratified_exp1.0 ! | 15.3633 / 1.465e+09 | 1.5259 / 3.47e+04 | 95.8788 / 2.303e+08 | 0.0380 / n/r | 1.3264 / n/r |

---

## cmplx_ps, K = -0.01x-10.0x-1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 50.5557 / 3.464e+07 | 2.0643 / 925.3 | 0.2113 / 11.41 | 0.2046 / n/r | 0.0209 / n/r |
| stratified_exp0.05 | 38.3094 / 9.407e+07 | 1.7296 / 531.4 | 0.1524 / 4.528 | 0.1715 / n/r | 0.0151 / n/r |
| stratified_exp0.1 | 32.9553 / 2.498e+06 | 1.7072 / 498.8 | 0.1484 / 4.068 | 0.1692 / n/r | 0.0147 / n/r |
| stratified_exp0.25 | 32.8780 / 2.351e+06 | 1.6694 / 460.1 | 0.1450 / 3.699 | 0.1655 / n/r | 0.0144 / n/r |
| stratified_exp0.5 ! | 31.8283 / 1.504e+06 | 1.6703 / 468.1 | 0.1445 / 3.726 | 0.1656 / n/r | 0.0143 / n/r |
| stratified_exp0.75 ! | 31.3351 / 9.842e+05 | 1.6698 / 461 | 0.1441 / 3.599 | 0.1655 / n/r | 0.0143 / n/r |
| stratified_exp1.0 ! | 31.3634 / 4.874e+05 | 1.6646 / 458.5 | 0.1441 / 3.637 | 0.1650 / n/r | 0.0143 / n/r |

---

## cmplx_ps, K = -0.05x-0.05x-0.05

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 20.4523 / 2.753e+05 | 1.6722 / 15.46 | 9.8901 / 807.1 | 0.1060 / n/r | 0.6116 / n/r |
| stratified_exp0.05 | 20.3748 / 8.235e+04 | 1.6702 / 14.22 | 9.8648 / 688.5 | 0.1059 / n/r | 0.6107 / n/r |
| stratified_exp0.1 | 21.0612 / 5.195e+05 | 1.6704 / 15.85 | 9.8919 / 733.4 | 0.1058 / n/r | 0.6114 / n/r |
| stratified_exp0.25 | 29.2857 / 3.647e+08 | 1.6779 / 15.32 | 10.0787 / 976.4 | 0.1060 / n/r | 0.6156 / n/r |
| stratified_exp0.5 ! | 22.1659 / 4.556e+07 | 1.6868 / 16.77 | 10.4180 / 1027 | 0.1059 / n/r | 0.6243 / n/r |
| stratified_exp0.75 ! | 21.4731 / 1.599e+08 | 1.7039 / 22.41 | 11.0793 / 1914 | 0.1060 / n/r | 0.6381 / n/r |
| stratified_exp1.0 ! | 24.5947 / 4.715e+08 | 1.7083 / 36.94 | 12.0606 / 5398 | 0.1045 / n/r | 0.6527 / n/r |

---

## cmplx_ps, K = -0.1x-0.1x-0.1

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 21.1130 / 7.753e+05 | 1.6720 / 15.13 | 4.9434 / 155.8 | 0.1295 / n/r | 0.3769 / n/r |
| stratified_exp0.05 | 20.3101 / 4.762e+04 | 1.6676 / 14.93 | 4.9240 / 152.7 | 0.1292 / n/r | 0.3757 / n/r |
| stratified_exp0.1 | 20.2591 / 6.442e+04 | 1.6698 / 14.94 | 4.9331 / 152.2 | 0.1293 / n/r | 0.3764 / n/r |
| stratified_exp0.25 | 25.1334 / 1.152e+08 | 1.6703 / 15.09 | 4.9406 / 156 | 0.1294 / n/r | 0.3764 / n/r |
| stratified_exp0.5 ! | 24.9725 / 3.612e+07 | 1.6732 / 15.25 | 5.0317 / 168.9 | 0.1292 / n/r | 0.3800 / n/r |
| stratified_exp0.75 ! | 22.7858 / 3.229e+07 | 1.6877 / 15.55 | 5.1361 / 183.5 | 0.1301 / n/r | 0.3854 / n/r |
| stratified_exp1.0 ! | 21.6198 / 4.204e+07 | 1.6857 / 15.56 | 5.1857 / 192.2 | 0.1297 / n/r | 0.3874 / n/r |

---

## cmplx_ps, K = -0.5x-0.5x-0.5

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 21.5482 / 1.121e+06 | 1.6723 / 63.14 | 0.9958 / 24.81 | 0.1579 / n/r | 0.0936 / n/r |
| stratified_exp0.05 | 20.5351 / 1.044e+05 | 1.6742 / 63.45 | 0.9891 / 24.54 | 0.1581 / n/r | 0.0930 / n/r |
| stratified_exp0.1 | 20.5004 / 9.207e+04 | 1.6671 / 62.81 | 0.9848 / 24.33 | 0.1575 / n/r | 0.0926 / n/r |
| stratified_exp0.25 | 20.2158 / 2.566e+04 | 1.6650 / 62.06 | 0.9830 / 23.84 | 0.1573 / n/r | 0.0925 / n/r |
| stratified_exp0.5 ! | 20.3811 / 1.486e+05 | 1.6669 / 62.58 | 0.9827 / 23.98 | 0.1574 / n/r | 0.0925 / n/r |
| stratified_exp0.75 ! | 22.1455 / 7.077e+06 | 1.6660 / 62.65 | 0.9830 / 24.12 | 0.1574 / n/r | 0.0925 / n/r |
| stratified_exp1.0 ! | 25.2316 / 1.098e+08 | 1.6694 / 63.28 | 0.9847 / 24.44 | 0.1577 / n/r | 0.0926 / n/r |

---

## cmplx_ps, K = -1.0x-1.0x-1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 23.2788 / 4.787e+06 | 1.6870 / 128.7 | 0.5041 / 12.74 | 0.1638 / n/r | 0.0488 / n/r |
| stratified_exp0.05 | 21.0656 / 5.414e+05 | 1.6681 / 124.2 | 0.4945 / 12 | 0.1620 / n/r | 0.0479 / n/r |
| stratified_exp0.1 | 21.0700 / 4.882e+05 | 1.6728 / 125.3 | 0.4942 / 12.09 | 0.1625 / n/r | 0.0479 / n/r |
| stratified_exp0.25 | 20.5359 / 1.068e+05 | 1.6684 / 123.6 | 0.4929 / 11.91 | 0.1621 / n/r | 0.0478 / n/r |
| stratified_exp0.5 ! | 20.2644 / 4.317e+04 | 1.6670 / 122.7 | 0.4921 / 11.75 | 0.1619 / n/r | 0.0477 / n/r |
| stratified_exp0.75 ! | 20.5379 / 1.793e+05 | 1.6716 / 123.1 | 0.4927 / 11.74 | 0.1624 / n/r | 0.0478 / n/r |
| stratified_exp1.0 ! | 20.2562 / 4.541e+04 | 1.6650 / 122.9 | 0.4918 / 11.77 | 0.1617 / n/r | 0.0477 / n/r |

---

## cmplx_ps, K = -2.0x-2.0x-2.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 25.5714 / 4.873e+07 | 1.7161 / 284.3 | 0.2570 / 7.04 | 0.1691 / n/r | 0.0253 / n/r |
| stratified_exp0.05 | 21.9192 / 2.748e+06 | 1.6841 / 251.5 | 0.2499 / 6.074 | 0.1659 / n/r | 0.0246 / n/r |
| stratified_exp0.1 | 20.7504 / 2.921e+05 | 1.6764 / 248.8 | 0.2481 / 5.985 | 0.1652 / n/r | 0.0244 / n/r |
| stratified_exp0.25 | 20.7725 / 2.809e+05 | 1.6750 / 249.5 | 0.2470 / 5.968 | 0.1651 / n/r | 0.0243 / n/r |
| stratified_exp0.5 ! | 20.7257 / 7.323e+05 | 1.6683 / 245.1 | 0.2462 / 5.851 | 0.1644 / n/r | 0.0242 / n/r |
| stratified_exp0.75 ! | 20.1983 / 2.917e+04 | 1.6658 / 244.9 | 0.2462 / 5.843 | 0.1642 / n/r | 0.0242 / n/r |
| stratified_exp1.0 ! | 20.2996 / 4.159e+04 | 1.6687 / 244.4 | 0.2461 / 5.819 | 0.1644 / n/r | 0.0242 / n/r |

---

## cmplx_ps, K = -3.0x-3.0x-3.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 25.7834 / 1.956e+07 | 1.7850 / 487.5 | 0.1802 / 5.484 | 0.1767 / n/r | 0.0178 / n/r |
| stratified_exp0.05 | 22.4922 / 4.312e+06 | 1.6849 / 378.1 | 0.1669 / 4.056 | 0.1668 / n/r | 0.0165 / n/r |
| stratified_exp0.1 | 20.5957 / 5.298e+05 | 1.6774 / 375.6 | 0.1653 / 3.987 | 0.1661 / n/r | 0.0164 / n/r |
| stratified_exp0.25 | 20.5159 / 2.1e+05 | 1.6827 / 376.6 | 0.1657 / 4 | 0.1666 / n/r | 0.0164 / n/r |
| stratified_exp0.5 ! | 20.3157 / 9.157e+04 | 1.6747 / 373.6 | 0.1643 / 3.947 | 0.1658 / n/r | 0.0163 / n/r |
| stratified_exp0.75 ! | 20.5475 / 1.001e+05 | 1.6693 / 368.1 | 0.1641 / 3.901 | 0.1653 / n/r | 0.0162 / n/r |
| stratified_exp1.0 ! | 20.3029 / 3.505e+04 | 1.6712 / 367.6 | 0.1644 / 3.871 | 0.1655 / n/r | 0.0163 / n/r |

---

## cmplx_ps, K = -4.0x-4.0x-4.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 25.5296 / 8.524e+06 | 1.8740 / 749.9 | 0.1435 / 4.965 | 0.1860 / n/r | 0.0142 / n/r |
| stratified_exp0.05 | 23.2819 / 1.441e+07 | 1.6875 / 512.4 | 0.1251 / 3.089 | 0.1675 / n/r | 0.0124 / n/r |
| stratified_exp0.1 | 21.9192 / 2.748e+06 | 1.6863 / 502.9 | 0.1247 / 3.002 | 0.1674 / n/r | 0.0124 / n/r |
| stratified_exp0.25 | 20.5757 / 1.892e+05 | 1.6812 / 498.9 | 0.1237 / 2.951 | 0.1669 / n/r | 0.0123 / n/r |
| stratified_exp0.5 ! | 20.8327 / 3.195e+05 | 1.6723 / 496.9 | 0.1231 / 2.947 | 0.1660 / n/r | 0.0122 / n/r |
| stratified_exp0.75 ! | 20.1943 / 5.292e+04 | 1.6732 / 498.2 | 0.1230 / 2.944 | 0.1661 / n/r | 0.0122 / n/r |
| stratified_exp1.0 ! | 20.5359 / 1.068e+05 | 1.6718 / 492.5 | 0.1230 / 2.915 | 0.1659 / n/r | 0.0122 / n/r |

---

## cmplx_ps, K = -10.0x-10.0x-10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 40.7496 / 2.148e+07 | 2.3527 / 3084 | 0.0912 / 5.666 | 0.2345 / n/r | 0.0091 / n/r |
| stratified_exp0.05 | 22.8875 / 3.594e+06 | 1.7078 / 1381 | 0.0509 / 1.346 | 0.1703 / n/r | 0.0051 / n/r |
| stratified_exp0.1 | 27.6715 / 7.926e+07 | 1.6932 / 1286 | 0.0504 / 1.252 | 0.1688 / n/r | 0.0050 / n/r |
| stratified_exp0.25 | 21.9493 / 2.767e+06 | 1.6766 / 1243 | 0.0496 / 1.185 | 0.1672 / n/r | 0.0049 / n/r |
| stratified_exp0.5 ! | 20.7362 / 2.245e+05 | 1.6694 / 1235 | 0.0493 / 1.174 | 0.1664 / n/r | 0.0049 / n/r |
| stratified_exp0.75 ! | 20.5649 / 1.493e+05 | 1.6871 / 1274 | 0.0495 / 1.198 | 0.1682 / n/r | 0.0049 / n/r |
| stratified_exp1.0 ! | 20.6721 / 2.804e+05 | 1.6786 / 1248 | 0.0494 / 1.189 | 0.1674 / n/r | 0.0049 / n/r |

---

## c1e4_exp1.0, K = -0.01x-0.01x-0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 104.0993 / 5.341e+10 | 1.1292 / 8.017e+04 | 28.4344 / 3.249e+07 | 0.0320 / n/r | 0.7355 / n/r |
| stratified_exp0.05 | 11.0331 / 6.279e+05 | 1.0606 / 3113 | 27.5335 / 3.829e+06 | 0.0321 / n/r | 0.7356 / n/r |
| stratified_exp0.1 | 10.2416 / 1.501e+06 | 1.0612 / 3130 | 27.7675 / 4.05e+06 | 0.0326 / n/r | 0.7376 / n/r |
| stratified_exp0.25 | 6.7906 / 7.139e+05 | 1.0759 / 4109 | 31.0195 / 1.066e+07 | 0.0322 / n/r | 0.7380 / n/r |
| stratified_exp0.5 ! | 7.3183 / 1.02e+08 | 1.1718 / 4.219e+04 | 56.0098 / 1.515e+09 | 0.0315 / n/r | 0.7447 / n/r |
| stratified_exp0.75 ! | 14.8925 / 1.528e+09 | 1.1222 / 1.763e+04 | 41.6825 / 4.041e+07 | 0.0309 / n/r | 0.7625 / n/r |
| stratified_exp1.0 ! | 41.5627 / 1.807e+10 | 1.5892 / 1.296e+05 | 136.2931 / 4.228e+09 | 0.0296 / n/r | 0.7922 / n/r |

---

## c1e4_exp1.0, K = -0.01x-10.0x-1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 189.1190 / 1.729e+10 | 1.4194 / 799.4 | 0.1632 / 11.72 | 0.1408 / n/r | 0.0162 / n/r |
| stratified_exp0.05 | 95.2412 / 6.422e+09 | 1.1125 / 383.7 | 0.0878 / 2.728 | 0.1104 / n/r | 0.0087 / n/r |
| stratified_exp0.1 | 356.2914 / 6.614e+11 | 1.0710 / 380 | 0.0841 / 2.548 | 0.1063 / n/r | 0.0083 / n/r |
| stratified_exp0.25 | 1875.1889 / 1.918e+13 | 1.0604 / 337.3 | 0.0816 / 2.077 | 0.1052 / n/r | 0.0081 / n/r |
| stratified_exp0.5 ! | 13179.0032 / 9.952e+14 | 1.0483 / 328.3 | 0.0809 / 2.007 | 0.1040 / n/r | 0.0080 / n/r |
| stratified_exp0.75 ! | 3446.2424 / 6.993e+13 | 1.0448 / 333.9 | 0.0808 / 2.024 | 0.1037 / n/r | 0.0080 / n/r |
| stratified_exp1.0 ! | 4424.3242 / 4.223e+13 | 1.0419 / 333.5 | 0.0803 / 2.034 | 0.1034 / n/r | 0.0080 / n/r |

---

## c1e4_exp1.0, K = -0.05x-0.05x-0.05

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 41.7741 / 1.935e+09 | 1.0577 / 9.095 | 5.4363 / 352 | 0.0710 / n/r | 0.3476 / n/r |
| stratified_exp0.05 | 1148.8611 / 8.548e+12 | 1.0425 / 9.884 | 5.3579 / 407.3 | 0.0700 / n/r | 0.3424 / n/r |
| stratified_exp0.1 | 18.4506 / 2.044e+08 | 1.0459 / 9.598 | 5.3589 / 457 | 0.0703 / n/r | 0.3427 / n/r |
| stratified_exp0.25 | 11.0350 / 6.768e+05 | 1.0542 / 9.596 | 5.4256 / 535.2 | 0.0708 / n/r | 0.3452 / n/r |
| stratified_exp0.5 ! | 10.5234 / 3.856e+06 | 1.0663 / 16.81 | 5.5871 / 883.8 | 0.0713 / n/r | 0.3490 / n/r |
| stratified_exp0.75 ! | 9.0924 / 2.885e+06 | 1.0827 / 936.6 | 5.9447 / 4.33e+04 | 0.0705 / n/r | 0.3512 / n/r |
| stratified_exp1.0 ! | 7.8167 / 1.143e+06 | 1.1679 / 3.481e+04 | 6.9651 / 1.732e+06 | 0.0707 / n/r | 0.3556 / n/r |

---

## c1e4_exp1.0, K = -0.1x-0.1x-0.1

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 16.8875 / 4.541e+07 | 1.0524 / 11.53 | 2.6949 / 90.62 | 0.0843 / n/r | 0.2097 / n/r |
| stratified_exp0.05 | 105.0614 / 1.83e+10 | 1.0494 / 11.15 | 2.6893 / 94.06 | 0.0841 / n/r | 0.2091 / n/r |
| stratified_exp0.1 | 1402.0170 / 2.049e+13 | 1.0492 / 11.14 | 2.6953 / 116.2 | 0.0840 / n/r | 0.2094 / n/r |
| stratified_exp0.25 | 13.1270 / 1.155e+07 | 1.0468 / 10.99 | 2.6861 / 97.18 | 0.0839 / n/r | 0.2086 / n/r |
| stratified_exp0.5 ! | 10.8609 / 7.212e+05 | 1.0473 / 10.89 | 2.7076 / 106.8 | 0.0838 / n/r | 0.2094 / n/r |
| stratified_exp0.75 ! | 11.1487 / 6.07e+06 | 1.0538 / 10.9 | 2.7463 / 103.3 | 0.0842 / n/r | 0.2109 / n/r |
| stratified_exp1.0 ! | 10.6483 / 3.85e+06 | 1.3522 / 368.1 | 4.2938 / 1.156e+04 | 0.0863 / n/r | 0.2178 / n/r |

---

## c1e4_exp1.0, K = -0.5x-0.5x-0.5

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 17.4587 / 9.517e+06 | 1.0776 / 49.42 | 0.5542 / 14.91 | 0.1025 / n/r | 0.0524 / n/r |
| stratified_exp0.05 | 17.0608 / 2.974e+07 | 1.0499 / 47.02 | 0.5392 / 13.39 | 0.0999 / n/r | 0.0509 / n/r |
| stratified_exp0.1 | 25.0699 / 1.893e+08 | 1.0461 / 44.29 | 0.5361 / 12.72 | 0.0995 / n/r | 0.0507 / n/r |
| stratified_exp0.25 | 70.9458 / 1.211e+10 | 1.0511 / 46.88 | 0.5388 / 13.49 | 0.1000 / n/r | 0.0509 / n/r |
| stratified_exp0.5 ! | 1534.6373 / 2.08e+13 | 1.0433 / 45.43 | 0.5364 / 13.57 | 0.0993 / n/r | 0.0506 / n/r |
| stratified_exp0.75 ! | 107.8185 / 3.98e+10 | 1.0504 / 46.57 | 0.5384 / 13.6 | 0.1000 / n/r | 0.0508 / n/r |
| stratified_exp1.0 ! | 44.4616 / 5.757e+09 | 1.0421 / 45.19 | 0.5349 / 13.11 | 0.0992 / n/r | 0.0505 / n/r |

---

## c1e4_exp1.0, K = -1.0x-1.0x-1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 21.6155 / 1.162e+08 | 1.0975 / 99.71 | 0.2823 / 7.578 | 0.1070 / n/r | 0.0274 / n/r |
| stratified_exp0.05 | 18.6797 / 9.517e+07 | 1.0515 / 94.6 | 0.2693 / 6.666 | 0.1025 / n/r | 0.0262 / n/r |
| stratified_exp0.1 | 16.8875 / 4.541e+07 | 1.0509 / 93.98 | 0.2691 / 6.603 | 0.1025 / n/r | 0.0261 / n/r |
| stratified_exp0.25 | 239.3759 / 2.235e+11 | 1.0431 / 90.35 | 0.2679 / 6.582 | 0.1017 / n/r | 0.0260 / n/r |
| stratified_exp0.5 ! | 204.3249 / 8.295e+10 | 1.0544 / 91.32 | 0.2703 / 6.652 | 0.1028 / n/r | 0.0263 / n/r |
| stratified_exp0.75 ! | 193.0352 / 1.34e+11 | 1.0453 / 89.5 | 0.2686 / 6.539 | 0.1019 / n/r | 0.0261 / n/r |
| stratified_exp1.0 ! | 100.3686 / 5.242e+10 | 1.0481 / 92.22 | 0.2692 / 6.671 | 0.1022 / n/r | 0.0261 / n/r |

---

## c1e4_exp1.0, K = -2.0x-2.0x-2.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 23.9675 / 1.027e+07 | 1.1814 / 256.5 | 0.1558 / 5.181 | 0.1166 / n/r | 0.0154 / n/r |
| stratified_exp0.05 | 16.8399 / 8.749e+06 | 1.0559 / 185.2 | 0.1362 / 3.426 | 0.1043 / n/r | 0.0134 / n/r |
| stratified_exp0.1 | 33.1527 / 1.023e+09 | 1.0680 / 193 | 0.1368 / 3.351 | 0.1054 / n/r | 0.0135 / n/r |
| stratified_exp0.25 | 19.7227 / 1.993e+08 | 1.0472 / 180.5 | 0.1342 / 3.154 | 0.1034 / n/r | 0.0132 / n/r |
| stratified_exp0.5 ! | 56.1084 / 2.698e+09 | 1.0502 / 175.8 | 0.1349 / 3.152 | 0.1037 / n/r | 0.0133 / n/r |
| stratified_exp0.75 ! | 147.2921 / 8.938e+10 | 1.0563 / 183.1 | 0.1351 / 3.281 | 0.1043 / n/r | 0.0133 / n/r |
| stratified_exp1.0 ! | 70.9458 / 1.211e+10 | 1.0509 / 183.5 | 0.1347 / 3.261 | 0.1038 / n/r | 0.0133 / n/r |

---

## c1e4_exp1.0, K = -3.0x-3.0x-3.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 37.4706 / 5.656e+07 | 1.3898 / 575.9 | 0.1466 / 7.83 | 0.1378 / n/r | 0.0145 / n/r |
| stratified_exp0.05 | 17.8261 / 1.179e+07 | 1.0820 / 292.5 | 0.0928 / 2.411 | 0.1073 / n/r | 0.0092 / n/r |
| stratified_exp0.1 | 20.7131 / 2.437e+08 | 1.0732 / 288.1 | 0.0918 / 2.319 | 0.1064 / n/r | 0.0091 / n/r |
| stratified_exp0.25 | 16.5248 / 3.263e+07 | 1.0472 / 270.8 | 0.0897 / 2.117 | 0.1038 / n/r | 0.0089 / n/r |
| stratified_exp0.5 ! | 104.5100 / 2.47e+10 | 1.0498 / 266.3 | 0.0899 / 2.135 | 0.1041 / n/r | 0.0089 / n/r |
| stratified_exp0.75 ! | 67.8681 / 8.874e+09 | 1.0477 / 265.9 | 0.0896 / 2.099 | 0.1039 / n/r | 0.0089 / n/r |
| stratified_exp1.0 ! | 703.2983 / 3.827e+12 | 1.0804 / 280.6 | 0.0918 / 2.206 | 0.1071 / n/r | 0.0091 / n/r |

---

## c1e4_exp1.0, K = -4.0x-4.0x-4.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 57.1879 / 1.067e+09 | 1.4456 / 853 | 0.1317 / 8.736 | 0.1436 / n/r | 0.0131 / n/r |
| stratified_exp0.05 | 19.1130 / 1.812e+07 | 1.0958 / 390 | 0.0704 / 1.813 | 0.1089 / n/r | 0.0070 / n/r |
| stratified_exp0.1 | 16.8399 / 8.749e+06 | 1.0595 / 370.4 | 0.0681 / 1.688 | 0.1053 / n/r | 0.0068 / n/r |
| stratified_exp0.25 | 23.2824 / 2.785e+08 | 1.0773 / 395.5 | 0.0687 / 1.683 | 0.1070 / n/r | 0.0068 / n/r |
| stratified_exp0.5 ! | 15.9701 / 3.336e+07 | 1.0506 / 351.5 | 0.0673 / 1.555 | 0.1044 / n/r | 0.0067 / n/r |
| stratified_exp0.75 ! | 341.8827 / 1.118e+12 | 1.0580 / 357.1 | 0.0675 / 1.571 | 0.1051 / n/r | 0.0067 / n/r |
| stratified_exp1.0 ! | 239.3759 / 2.235e+11 | 1.0461 / 360 | 0.0671 / 1.602 | 0.1039 / n/r | 0.0067 / n/r |

---

## c1e4_exp1.0, K = -10.0x-10.0x-10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 79.9586 / 3.499e+08 | 1.6385 / 2532 | 0.0730 / 6.029 | 0.1634 / n/r | 0.0073 / n/r |
| stratified_exp0.05 | 23.9675 / 1.027e+07 | 1.1792 / 1267 | 0.0310 / 1.003 | 0.1176 / n/r | 0.0031 / n/r |
| stratified_exp0.1 | 18.3929 / 2.339e+06 | 1.1149 / 970 | 0.0286 / 0.7309 | 0.1112 / n/r | 0.0029 / n/r |
| stratified_exp0.25 | 18.6222 / 4.871e+07 | 1.0616 / 929 | 0.0273 / 0.6823 | 0.1059 / n/r | 0.0027 / n/r |
| stratified_exp0.5 ! | 22.8151 / 2.113e+08 | 1.0527 / 918.2 | 0.0270 / 0.6351 | 0.1050 / n/r | 0.0027 / n/r |
| stratified_exp0.75 ! | 35.1235 / 1.95e+09 | 1.0604 / 947.7 | 0.0272 / 0.6481 | 0.1058 / n/r | 0.0027 / n/r |
| stratified_exp1.0 ! | 18.0713 / 6.604e+07 | 1.0459 / 896.5 | 0.0268 / 0.6175 | 0.1043 / n/r | 0.0027 / n/r |

---

# RESULTS (Dense Table)

---

## naive_ps, K = -0.01x-0.01x-0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 7.0528 / 1.335e+04 |
| stratified_exp0.05 | 8.2755 / 1.796e+06 |
| stratified_exp0.1 | 7.5392 / 1.02e+07 |
| stratified_exp0.25 | 5.9529 / 1.04e+07 |
| stratified_exp0.5 ! | 3.2997 / 6.383e+06 |
| stratified_exp0.75 ! | 2.0559 / 2.024e+06 |
| stratified_exp1.0 ! | 1.5250 / 1.097e+06 |

---

## naive_ps, K = -0.01x-10.0x-1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 31.5117 / 5.835e+07 |
| stratified_exp0.05 | 18.2699 / 9.339e+06 |
| stratified_exp0.1 | 14.7142 / 6.053e+06 |
| stratified_exp0.25 | 13.1061 / 6.899e+05 |
| stratified_exp0.5 ! | 12.9298 / 3.381e+06 |
| stratified_exp0.75 ! | 12.4301 / 5.097e+05 |
| stratified_exp1.0 ! | 13.0066 / 4.275e+06 |

---

## naive_ps, K = -0.05x-0.05x-0.05

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 7.1396 / 1.696e+04 |
| stratified_exp0.05 | 7.0449 / 1.025e+04 |
| stratified_exp0.1 | 8.7725 / 8.794e+06 |
| stratified_exp0.25 | 8.1848 / 2.322e+06 |
| stratified_exp0.5 ! | 8.9787 / 3.168e+07 |
| stratified_exp0.75 ! | 7.5589 / 9.675e+06 |
| stratified_exp1.0 ! | 5.9142 / 4.579e+06 |

---

## naive_ps, K = -0.1x-0.1x-0.1

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 7.2276 / 1.371e+05 |
| stratified_exp0.05 | 7.0449 / 1.341e+04 |
| stratified_exp0.1 | 7.0811 / 1.368e+04 |
| stratified_exp0.25 | 8.0914 / 1.711e+06 |
| stratified_exp0.5 ! | 8.1194 / 7.917e+05 |
| stratified_exp0.75 ! | 8.2751 / 1.184e+07 |
| stratified_exp1.0 ! | 8.3648 / 2.737e+07 |

---

## naive_ps, K = -0.5x-0.5x-0.5

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 8.0872 / 6.226e+05 |
| stratified_exp0.05 | 7.2445 / 1.409e+05 |
| stratified_exp0.1 | 7.1407 / 1.606e+04 |
| stratified_exp0.25 | 7.0715 / 3.374e+04 |
| stratified_exp0.5 ! | 6.9744 / 7160 |
| stratified_exp0.75 ! | 7.0934 / 2.155e+04 |
| stratified_exp1.0 ! | 8.4379 / 6.524e+06 |

---

## naive_ps, K = -1.0x-1.0x-1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 8.1569 / 5.85e+05 |
| stratified_exp0.05 | 7.3303 / 8.527e+04 |
| stratified_exp0.1 | 7.1355 / 1.294e+05 |
| stratified_exp0.25 | 7.0806 / 1.234e+04 |
| stratified_exp0.5 ! | 7.0337 / 9889 |
| stratified_exp0.75 ! | 7.0273 / 9579 |
| stratified_exp1.0 ! | 7.0528 / 1.335e+04 |

---

## naive_ps, K = -2.0x-2.0x-2.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 12.5735 / 7.437e+07 |
| stratified_exp0.05 | 7.8222 / 5.058e+05 |
| stratified_exp0.1 | 7.3824 / 9.558e+04 |
| stratified_exp0.25 | 7.1522 / 3.364e+04 |
| stratified_exp0.5 ! | 7.1022 / 1.749e+04 |
| stratified_exp0.75 ! | 7.0528 / 2.831e+04 |
| stratified_exp1.0 ! | 7.0300 / 9475 |

---

## naive_ps, K = -3.0x-3.0x-3.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 11.9825 / 1.909e+06 |
| stratified_exp0.05 | 7.7869 / 4.704e+05 |
| stratified_exp0.1 | 7.9379 / 4.713e+05 |
| stratified_exp0.25 | 7.5214 / 1.786e+05 |
| stratified_exp0.5 ! | 7.2499 / 1.234e+05 |
| stratified_exp0.75 ! | 7.0626 / 1.093e+04 |
| stratified_exp1.0 ! | 7.0614 / 1.152e+04 |

---

## naive_ps, K = -4.0x-4.0x-4.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 13.2412 / 6.785e+06 |
| stratified_exp0.05 | 9.9582 / 2.231e+07 |
| stratified_exp0.1 | 9.5045 / 1.213e+07 |
| stratified_exp0.25 | 7.3217 / 8.466e+04 |
| stratified_exp0.5 ! | 7.1841 / 8.23e+04 |
| stratified_exp0.75 ! | 7.1182 / 1.934e+04 |
| stratified_exp1.0 ! | 7.0999 / 1.877e+04 |

---

## naive_ps, K = -10.0x-10.0x-10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 15.1290 / 8.727e+06 |
| stratified_exp0.05 | 13.0046 / 7.444e+07 |
| stratified_exp0.1 | 8.1908 / 5.636e+05 |
| stratified_exp0.25 | 10.1208 / 1.517e+07 |
| stratified_exp0.5 ! | 7.3303 / 8.527e+04 |
| stratified_exp0.75 ! | 7.4858 / 3.287e+05 |
| stratified_exp1.0 ! | 7.1355 / 1.294e+05 |

---

## cmplx_ps, K = -0.01x-0.01x-0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 20.4915 / 1.122e+05 |
| stratified_exp0.05 | 23.9512 / 1.793e+07 |
| stratified_exp0.1 | 20.7132 / 1.338e+07 |
| stratified_exp0.25 | 14.0968 / 2.044e+07 |
| stratified_exp0.5 ! | 14.4425 / 3.857e+08 |
| stratified_exp0.75 ! | 29.9736 / 7.029e+09 |
| stratified_exp1.0 ! | 15.3633 / 1.465e+09 |

---

## cmplx_ps, K = -0.01x-10.0x-1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 50.5557 / 3.464e+07 |
| stratified_exp0.05 | 38.3094 / 9.407e+07 |
| stratified_exp0.1 | 32.9553 / 2.498e+06 |
| stratified_exp0.25 | 32.8780 / 2.351e+06 |
| stratified_exp0.5 ! | 31.8283 / 1.504e+06 |
| stratified_exp0.75 ! | 31.3351 / 9.842e+05 |
| stratified_exp1.0 ! | 31.3634 / 4.874e+05 |

---

## cmplx_ps, K = -0.05x-0.05x-0.05

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 20.4523 / 2.753e+05 |
| stratified_exp0.05 | 20.3748 / 8.235e+04 |
| stratified_exp0.1 | 21.0612 / 5.195e+05 |
| stratified_exp0.25 | 29.2857 / 3.647e+08 |
| stratified_exp0.5 ! | 22.1659 / 4.556e+07 |
| stratified_exp0.75 ! | 21.4731 / 1.599e+08 |
| stratified_exp1.0 ! | 24.5947 / 4.715e+08 |

---

## cmplx_ps, K = -0.1x-0.1x-0.1

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 21.1130 / 7.753e+05 |
| stratified_exp0.05 | 20.3101 / 4.762e+04 |
| stratified_exp0.1 | 20.2591 / 6.442e+04 |
| stratified_exp0.25 | 25.1334 / 1.152e+08 |
| stratified_exp0.5 ! | 24.9725 / 3.612e+07 |
| stratified_exp0.75 ! | 22.7858 / 3.229e+07 |
| stratified_exp1.0 ! | 21.6198 / 4.204e+07 |

---

## cmplx_ps, K = -0.5x-0.5x-0.5

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 21.5482 / 1.121e+06 |
| stratified_exp0.05 | 20.5351 / 1.044e+05 |
| stratified_exp0.1 | 20.5004 / 9.207e+04 |
| stratified_exp0.25 | 20.2158 / 2.566e+04 |
| stratified_exp0.5 ! | 20.3811 / 1.486e+05 |
| stratified_exp0.75 ! | 22.1455 / 7.077e+06 |
| stratified_exp1.0 ! | 25.2316 / 1.098e+08 |

---

## cmplx_ps, K = -1.0x-1.0x-1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 23.2788 / 4.787e+06 |
| stratified_exp0.05 | 21.0656 / 5.414e+05 |
| stratified_exp0.1 | 21.0700 / 4.882e+05 |
| stratified_exp0.25 | 20.5359 / 1.068e+05 |
| stratified_exp0.5 ! | 20.2644 / 4.317e+04 |
| stratified_exp0.75 ! | 20.5379 / 1.793e+05 |
| stratified_exp1.0 ! | 20.2562 / 4.541e+04 |

---

## cmplx_ps, K = -2.0x-2.0x-2.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 25.5714 / 4.873e+07 |
| stratified_exp0.05 | 21.9192 / 2.748e+06 |
| stratified_exp0.1 | 20.7504 / 2.921e+05 |
| stratified_exp0.25 | 20.7725 / 2.809e+05 |
| stratified_exp0.5 ! | 20.7257 / 7.323e+05 |
| stratified_exp0.75 ! | 20.1983 / 2.917e+04 |
| stratified_exp1.0 ! | 20.2996 / 4.159e+04 |

---

## cmplx_ps, K = -3.0x-3.0x-3.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 25.7834 / 1.956e+07 |
| stratified_exp0.05 | 22.4922 / 4.312e+06 |
| stratified_exp0.1 | 20.5957 / 5.298e+05 |
| stratified_exp0.25 | 20.5159 / 2.1e+05 |
| stratified_exp0.5 ! | 20.3157 / 9.157e+04 |
| stratified_exp0.75 ! | 20.5475 / 1.001e+05 |
| stratified_exp1.0 ! | 20.3029 / 3.505e+04 |

---

## cmplx_ps, K = -4.0x-4.0x-4.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 25.5296 / 8.524e+06 |
| stratified_exp0.05 | 23.2819 / 1.441e+07 |
| stratified_exp0.1 | 21.9192 / 2.748e+06 |
| stratified_exp0.25 | 20.5757 / 1.892e+05 |
| stratified_exp0.5 ! | 20.8327 / 3.195e+05 |
| stratified_exp0.75 ! | 20.1943 / 5.292e+04 |
| stratified_exp1.0 ! | 20.5359 / 1.068e+05 |

---

## cmplx_ps, K = -10.0x-10.0x-10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 40.7496 / 2.148e+07 |
| stratified_exp0.05 | 22.8875 / 3.594e+06 |
| stratified_exp0.1 | 27.6715 / 7.926e+07 |
| stratified_exp0.25 | 21.9493 / 2.767e+06 |
| stratified_exp0.5 ! | 20.7362 / 2.245e+05 |
| stratified_exp0.75 ! | 20.5649 / 1.493e+05 |
| stratified_exp1.0 ! | 20.6721 / 2.804e+05 |

---

## c1e4_exp1.0, K = -0.01x-0.01x-0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 104.0993 / 5.341e+10 |
| stratified_exp0.05 | 11.0331 / 6.279e+05 |
| stratified_exp0.1 | 10.2416 / 1.501e+06 |
| stratified_exp0.25 | 6.7906 / 7.139e+05 |
| stratified_exp0.5 ! | 7.3183 / 1.02e+08 |
| stratified_exp0.75 ! | 14.8925 / 1.528e+09 |
| stratified_exp1.0 ! | 41.5627 / 1.807e+10 |

---

## c1e4_exp1.0, K = -0.01x-10.0x-1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 189.1190 / 1.729e+10 |
| stratified_exp0.05 | 95.2412 / 6.422e+09 |
| stratified_exp0.1 | 356.2914 / 6.614e+11 |
| stratified_exp0.25 | 1875.1889 / 1.918e+13 |
| stratified_exp0.5 ! | 13179.0032 / 9.952e+14 |
| stratified_exp0.75 ! | 3446.2424 / 6.993e+13 |
| stratified_exp1.0 ! | 4424.3242 / 4.223e+13 |

---

## c1e4_exp1.0, K = -0.05x-0.05x-0.05

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 41.7741 / 1.935e+09 |
| stratified_exp0.05 | 1148.8611 / 8.548e+12 |
| stratified_exp0.1 | 18.4506 / 2.044e+08 |
| stratified_exp0.25 | 11.0350 / 6.768e+05 |
| stratified_exp0.5 ! | 10.5234 / 3.856e+06 |
| stratified_exp0.75 ! | 9.0924 / 2.885e+06 |
| stratified_exp1.0 ! | 7.8167 / 1.143e+06 |

---

## c1e4_exp1.0, K = -0.1x-0.1x-0.1

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 16.8875 / 4.541e+07 |
| stratified_exp0.05 | 105.0614 / 1.83e+10 |
| stratified_exp0.1 | 1402.0170 / 2.049e+13 |
| stratified_exp0.25 | 13.1270 / 1.155e+07 |
| stratified_exp0.5 ! | 10.8609 / 7.212e+05 |
| stratified_exp0.75 ! | 11.1487 / 6.07e+06 |
| stratified_exp1.0 ! | 10.6483 / 3.85e+06 |

---

## c1e4_exp1.0, K = -0.5x-0.5x-0.5

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 17.4587 / 9.517e+06 |
| stratified_exp0.05 | 17.0608 / 2.974e+07 |
| stratified_exp0.1 | 25.0699 / 1.893e+08 |
| stratified_exp0.25 | 70.9458 / 1.211e+10 |
| stratified_exp0.5 ! | 1534.6373 / 2.08e+13 |
| stratified_exp0.75 ! | 107.8185 / 3.98e+10 |
| stratified_exp1.0 ! | 44.4616 / 5.757e+09 |

---

## c1e4_exp1.0, K = -1.0x-1.0x-1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 21.6155 / 1.162e+08 |
| stratified_exp0.05 | 18.6797 / 9.517e+07 |
| stratified_exp0.1 | 16.8875 / 4.541e+07 |
| stratified_exp0.25 | 239.3759 / 2.235e+11 |
| stratified_exp0.5 ! | 204.3249 / 8.295e+10 |
| stratified_exp0.75 ! | 193.0352 / 1.34e+11 |
| stratified_exp1.0 ! | 100.3686 / 5.242e+10 |

---

## c1e4_exp1.0, K = -2.0x-2.0x-2.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 23.9675 / 1.027e+07 |
| stratified_exp0.05 | 16.8399 / 8.749e+06 |
| stratified_exp0.1 | 33.1527 / 1.023e+09 |
| stratified_exp0.25 | 19.7227 / 1.993e+08 |
| stratified_exp0.5 ! | 56.1084 / 2.698e+09 |
| stratified_exp0.75 ! | 147.2921 / 8.938e+10 |
| stratified_exp1.0 ! | 70.9458 / 1.211e+10 |

---

## c1e4_exp1.0, K = -3.0x-3.0x-3.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 37.4706 / 5.656e+07 |
| stratified_exp0.05 | 17.8261 / 1.179e+07 |
| stratified_exp0.1 | 20.7131 / 2.437e+08 |
| stratified_exp0.25 | 16.5248 / 3.263e+07 |
| stratified_exp0.5 ! | 104.5100 / 2.47e+10 |
| stratified_exp0.75 ! | 67.8681 / 8.874e+09 |
| stratified_exp1.0 ! | 703.2983 / 3.827e+12 |

---

## c1e4_exp1.0, K = -4.0x-4.0x-4.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 57.1879 / 1.067e+09 |
| stratified_exp0.05 | 19.1130 / 1.812e+07 |
| stratified_exp0.1 | 16.8399 / 8.749e+06 |
| stratified_exp0.25 | 23.2824 / 2.785e+08 |
| stratified_exp0.5 ! | 15.9701 / 3.336e+07 |
| stratified_exp0.75 ! | 341.8827 / 1.118e+12 |
| stratified_exp1.0 ! | 239.3759 / 2.235e+11 |

---

## c1e4_exp1.0, K = -10.0x-10.0x-10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 79.9586 / 3.499e+08 |
| stratified_exp0.05 | 23.9675 / 1.027e+07 |
| stratified_exp0.1 | 18.3929 / 2.339e+06 |
| stratified_exp0.25 | 18.6222 / 4.871e+07 |
| stratified_exp0.5 ! | 22.8151 / 2.113e+08 |
| stratified_exp0.75 ! | 35.1235 / 1.95e+09 |
| stratified_exp1.0 ! | 18.0713 / 6.604e+07 |


---

# Insights and conclusions

Geometry `prod_factor_dim=[3,3,3]` (`D = 9`), `loss_geometry=var_cross_entropy` (the
Bayes-posterior form: each factor's denominator is `min_v D_{e_v,m}`; see
`../init_test_log_vce_3d_refactor_new/vce_bayes.md`). Both paths ran `stratified_exp`;
the reference is `stratified_exp(0.1)` -- the report header's "pinned at exp(0.1)" line is
generic boilerplate and does not apply here.

Percentages below are `100 * (wnelbo_ref - H) / H`, 3-seed mean ± across-seed sd.

## 1. Headline: tight on the product manifold at V = 10

Uniform vectors `[-4.0]^3 .. [-0.1]^3`, loss-proposal rates 0.1-0.5:

| ps | range vs `H(p)` | tightest cells |
|---|---|---|
| `naive_ps` (H = 0.5003) | -0.9% .. +1.7% | `[-1.0]^3` rate 0.1: +0.1% ± 0.7; `[-0.5]^3` rate 0.1: +0.1% ± 0.2 |
| `cmplx_ps` (H = 1.6664) | -0.1% .. +1.2% | `[-1.0]^3` rate 0.5: +0.0% ± 0.3; `[-0.5]^3` rate 0.1: +0.0% ± 0.1 |

This matches the single-manifold project's band with three factors instead of one. The
derivation's exact `d+2` tilt identity only covers `M = 1`, but the property the fix rests
on -- the weight is a function of `z_t` alone -- holds for any `M`, and the data bear it out.

## 2. The shared heat-time ceiling makes a flat factor measurable (variance, not bias)

`t` is clamped to `min_m _radial_t_max(3) * R_m^2`, `R_m = 1/sqrt(-K_m)`. For the mixed vector
the `K = -10` factor sets that ceiling at 9.7 instead of the flat factor's 9700.

| vector (`naive_ps`) | rate 0.5 | rate 1.0 |
|---|---|---|
| `[-0.01,-0.01,-0.01]` | -0.9% ± **15.8** | -1.9% ± **17.8** |
| `[-0.01,-10.0,-1.0]` | -0.2% ± **0.4** | -1.2% ± **0.5** |

The means of the uniform flat product are not systematically off; its across-seed spread is
~40x larger. (An earlier seed-0-only reading of "-16%" there was one draw from that spread.)
`cmplx_ps` shows the same split: ± 6.8-10.3 vs ± 0.5-1.0 at rates 0.5-1.0.

## 3. Cross-check against the Bayes-optimal twin

`init_opt_test_3x3d_refactor_new` (exact Bayes model, cannot leak) and the trained `ce`
baseline `init_test_3x3d_refactor_new`. Both name the uniform product by its scalar `K`
(`k--2.0` = `[-2,-2,-2]`); verified against each run's `.hydra/config.yaml`, so the tags are
correct. **Caveat: both baselines used an `exp(0.1)` reference path, this project
`stratified_exp(0.1)`, so this is a qualitative comparison.** The Bayes-optimal numbers are
identical across rates because `mode=opt` does no training and the rate only drives training.

| vector (`naive_ps`) | rate | vce (trained) | ce (trained) | Bayes-optimal |
|---|---|---|---|---|
| `[-1.0]^3` | 0.25 | -0.2% ± 0.9 | +0.8% ± 1.0 | -0.4% ± 0.3 |
| `[-0.05]^3` | 0.1 | +0.4% ± 0.1 | +0.3% ± 0.2 | -0.4% ± 0.1 |
| `[-0.05]^3` | 1.0 | **+2.7% ± 2.2** | +1.1% ± 1.0 | -0.4% ± 0.1 |
| `[-10.0]^3` | 0.1 | **+5.6% ± 2.9** | +0.8% ± 1.7 | -0.4% ± 1.9 |
| `[-0.01,-10.0,-1.0]` | 0.5 | -0.2% ± 0.4 | +1.3% ± 0.3 | -0.5% ± 1.3 |
| `[-0.01]^3` | 0.5 | -0.9% ± 15.8 | -5.0% ± 5.0 | **-6.4% ± 3.3** |

Three conclusions:

1. **Small negatives are the estimator.** The exact model itself reads ~-0.4% below `H(p)` on
   this manifold (-0.4% ± 0.1 at `[-0.05]^3`, well resolved). vce readings of -0.1% to -1.3%
   at high rates are in that regime, not a side channel.
2. **`[-0.01]^3` is unmeasurable even for the exact model** (-6.4% ± 3.3 naive,
   -2.1% ± 3.8 cmplx). The trained vce spread there (13-18%) is well above the exact model's
   3.3%, so it also carries training variance on top of estimator noise.
3. **At the band edges vce trains worse than `ce`.** Where the exact model is well-measured
   (`[-0.05]^3`, `[-10.0]^3`), vce is looser than `ce` at rate 1.0 on flat vectors and rate
   0.1 on sharp ones. That is a training effect of the loss-proposal rate on this objective,
   not the estimator. Inside rate 0.25-0.5 vce, `ce` and the exact model agree to about a point.

## 4. Recommended operating band

Loss-proposal rate **0.25-0.5**. Sharp vectors degrade at low rates (`[-10.0]^3` rate 0.05:
+18.0% naive); flat-ish ones at high rates (`[-0.05]^3` rate 1.0: +2.7%). 0.25-0.5 is the
only band that holds for every usable vector on both distributions.

## 5. `c1e4_exp1.0` (V = 10 000)

All 210 cells, three seeds. The reference-path caveat of §3 applies to every comparison below.

### 5.1 The single-manifold seed divergence does not recur

Uniform `[-4.0]^3 .. [-0.1]^3`, loss-proposal rates 0.1-0.5, per seed:

| seed | product mean | median | worst cell | single `H^3` mean |
|---|---|---|---|---|
| 0 | +1.9% | +1.4% | +6.5% | +2.3% |
| 1 | +0.3% | +0.1% | +2.4% | +2.6% |
| 2 | +1.3% | +1.2% | +3.2% | **+42.3%** |

On the single manifold seed 2 trained to a much worse model; here no seed does. Seeds 0 and 1
are about as tight on both manifolds, so the product's advantage at `V = 10 000` is the absence
of that divergence, not a uniformly tighter bound. With one diverging seed out of three in the
sibling project, this is suggestive; it is too few runs to attribute to the product structure.

*Correction:* an interim progress note compared product seed 0 against the sibling's 3-seed
means and called the product "an order of magnitude tighter". The per-seed numbers above do
not support that.

### 5.2 Against the trained `ce` baseline and the exact model

3-seed mean ± sd, % of `H = 1.0407`:

| vector | rate | vce (trained) | ce (trained) | Bayes-optimal |
|---|---|---|---|---|
| `[-10.0]^3` | 0.5 | +1.2% ± 0.8 | +2.4% ± 1.4 | -1.8% ± 0.1 |
| `[-4.0]^3` | 0.5 | +1.0% ± 1.4 | +1.1% ± 0.3 | -0.9% ± 0.3 |
| `[-1.0]^3` | 0.25 | +0.2% ± 0.6 | +0.6% ± 0.5 | -0.4% ± 0.2 |
| `[-0.5]^3` | 0.5 | +0.3% ± 0.6 | +1.0% ± 0.8 | -0.1% ± 0.1 |
| `[-0.1]^3` | 0.25 | +0.6% ± 0.4 | +0.6% ± 0.3 | -0.1% ± 0.1 |
| `[-0.01,-10.0,-1.0]` | 0.5 | +0.7% ± 1.1 | +0.5% ± 0.7 | -0.8% ± 0.7 |
| `[-0.01]^3` | 0.25 | +3.4% ± 3.8 | +1.1% ± 4.6 | -3.7% ± 0.9 |

Inside the band vce and `ce` agree to about a point. At this vocabulary the exact model's
under-reading on the `exp(0.1)` reference grows with curvature (-0.1% at `[-0.5]^3` to -1.8% at
`[-10.0]^3`), so part of the 1-3 point gap between trained and exact models is the estimator.

### 5.3 The failure corners are worse at V = 10 000, and they are training failures

- **High rate on flat curvature.** `[-0.1]^3` rate 1.0: +29.9% ± 47.6 (seed 2 alone +84.8%);
  `[-0.05]^3` rate 1.0: +12.2% ± 16.5; `[-0.01]^3` rate 0.5: +12.6% ± 11.8, rate 1.0:
  +52.7% ± 52.0. The `ce` baseline fails in the same corner, harder (+26.7% ± 44.5 at
  `[-0.05]^3` rate 1.0; +178% ± 310 at `[-0.01]^3` rate 0.5), while the exact model reads
  -0.0% to -3.7% with sd <= 0.9. The estimator can measure these geometries; what fails is
  training with a high loss-proposal rate on flat curvature (the worst `[-0.01]^3` seeds have
  `ce_ref` 0.78 and 0.81).
- **Low rate on sharp curvature.** `[-10.0]^3` rate 0.01: +52.0% to +63.6% on all three seeds,
  with `ce_ref` of only 0.007-0.008. A tiny reference CE next to a bad ELBO: `ce_ref` is not a
  proxy for ELBO quality in this corner. Same low-rate effect as every other spec.

### 5.4 `wloss` carries no signal about ELBO quality

The lowest-`wloss` seed is also the worst-ELBO seed in 27 of 70 cells, against ~23 expected by
chance (binomial sd ~4). The strong anti-correlation seen on the single manifold (sibling
`RESULTS.md` §4) does not hold here; `wloss` simply does not indicate which seed has the better
ELBO, so it cannot be used for seed or rate selection.

### 5.5 Operating band at V = 10 000

Rate **0.25** stays within +3.5% for every vector in the table above, including the flat
uniform product (`[-0.01]^3`: +3.4% ± 3.8). Rate 0.5 matches it except on `[-0.01]^3`
(+12.6% ± 11.8). Avoid rates >= 0.75 on flat vectors and 0.01 on sharp ones.
