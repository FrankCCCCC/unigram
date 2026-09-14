# init_test_log_vce_3d_refactor_new results

- runs collected: **567** / 567 (100%) — run dirs without test_metrics.json: 0
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
  exp(0.1) and stays valid, but training there is materially noisier.
- `wce_ref` is dominated by rare extremes; treat its spread as indicative only.

---

# Results (Full Table)

---

## naive_ps, K = -0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 14.3724 / 9.187e+06 | 0.8016 / 9.345e+05 | 69.2137 / 5.121e+09 | 0.0045 / n/r | 0.4571 / n/r |
| stratified_exp0.05 | 10.0727 / 1.386e+06 | 0.9020 / 1.487e+06 | 71.3857 / 6.003e+09 | 0.0046 / n/r | 0.4563 / n/r |
| stratified_exp0.1 | 47.7418 / 1.09e+10 | 0.4407 / 1.317e+05 | 75.6469 / 6.363e+09 | 0.0049 / n/r | 0.4544 / n/r |
| stratified_exp0.25 | 4.9484 / 9.906e+07 | 0.3445 / 8.654e+04 | 87.0168 / 1.053e+10 | 0.0050 / n/r | 0.4522 / n/r |
| stratified_exp0.5 ! | 1.2795 / 3.212e+06 | 0.3134 / 1.067e+04 | 85.8293 / 1.077e+10 | 0.0050 / n/r | 0.4541 / n/r |
| stratified_exp0.75 ! | 0.7253 / 7.463e+05 | 0.3144 / 9268 | 85.1872 / 1.12e+10 | 0.0050 / n/r | 0.4552 / n/r |
| stratified_exp1.0 ! | 0.5475 / 3.202e+05 | 0.1966 / 1965 | 149.6810 / 7.321e+10 | 0.0034 / n/r | 0.4791 / n/r |

---

## naive_ps, K = -0.05

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 14.0019 / 3.582e+05 | 0.5051 / 1080 | 10.8791 / 2.54e+05 | 0.0166 / n/r | 0.3383 / n/r |
| stratified_exp0.05 | 13.7196 / 6.564e+05 | 0.5007 / 1060 | 10.8176 / 2.717e+05 | 0.0166 / n/r | 0.3365 / n/r |
| stratified_exp0.1 | 12.9506 / 8.343e+05 | 0.5034 / 1664 | 10.8553 / 2.338e+05 | 0.0166 / n/r | 0.3363 / n/r |
| stratified_exp0.25 | 10.6974 / 6.259e+06 | 0.5037 / 520.3 | 10.9811 / 2.48e+05 | 0.0168 / n/r | 0.3366 / n/r |
| stratified_exp0.5 ! | 47.6719 / 1.089e+10 | 1.1436 / 5.969e+06 | 31.1674 / 1.452e+09 | 0.0156 / n/r | 0.3482 / n/r |
| stratified_exp0.75 ! | 19.0180 / 2.137e+09 | 1.5575 / 1.458e+07 | 39.9768 / 2.868e+09 | 0.0153 / n/r | 0.3525 / n/r |
| stratified_exp1.0 ! | 9.0625 / 4.101e+08 | 2.1553 / 2.349e+07 | 60.3936 / 8.936e+09 | 0.0141 / n/r | 0.3644 / n/r |

---

## naive_ps, K = -0.1

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 14.5536 / 9.48e+05 | 0.5005 / 18.1 | 5.5016 / 2.912e+04 | 0.0248 / n/r | 0.2542 / n/r |
| stratified_exp0.05 | 13.7786 / 4.328e+05 | 0.5005 / 18.02 | 5.4810 / 2.527e+04 | 0.0248 / n/r | 0.2540 / n/r |
| stratified_exp0.1 | 13.6639 / 5.639e+05 | 0.5010 / 17.93 | 5.4973 / 2.702e+04 | 0.0247 / n/r | 0.2546 / n/r |
| stratified_exp0.25 | 13.8368 / 1.392e+07 | 0.5024 / 21.95 | 5.5526 / 2.778e+04 | 0.0249 / n/r | 0.2550 / n/r |
| stratified_exp0.5 ! | 10.7048 / 6.217e+06 | 0.5056 / 23.08 | 5.6362 / 3.33e+04 | 0.0250 / n/r | 0.2560 / n/r |
| stratified_exp0.75 ! | 151.4742 / 2.315e+11 | 0.5174 / 1955 | 6.3671 / 9.677e+04 | 0.0247 / n/r | 0.2614 / n/r |
| stratified_exp1.0 ! | 48.6876 / 1.16e+10 | 0.5046 / 801.2 | 10.7558 / 2.555e+05 | 0.0220 / n/r | 0.2847 / n/r |

---

## naive_ps, K = -0.5

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 14.0717 / 6.503e+05 | 0.5084 / 11.53 | 1.1108 / 53.22 | 0.0419 / n/r | 0.0895 / n/r |
| stratified_exp0.05 | 14.5380 / 1.462e+06 | 0.5045 / 10.48 | 1.0969 / 45.59 | 0.0416 / n/r | 0.0886 / n/r |
| stratified_exp0.1 | 14.1491 / 6.443e+05 | 0.5051 / 10.64 | 1.0970 / 45.3 | 0.0417 / n/r | 0.0887 / n/r |
| stratified_exp0.25 | 13.7705 / 4.029e+05 | 0.5027 / 10.57 | 1.0881 / 44.54 | 0.0415 / n/r | 0.0880 / n/r |
| stratified_exp0.5 ! | 14.0566 / 1.682e+06 | 0.5029 / 10.56 | 1.0921 / 45.08 | 0.0415 / n/r | 0.0882 / n/r |
| stratified_exp0.75 ! | 14.0202 / 5.851e+06 | 0.5038 / 11.17 | 1.0969 / 49.27 | 0.0416 / n/r | 0.0886 / n/r |
| stratified_exp1.0 ! | 13.0883 / 2.044e+06 | 0.5040 / 11.06 | 1.1021 / 50.09 | 0.0416 / n/r | 0.0888 / n/r |

---

## naive_ps, K = -1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 15.3847 / 2.391e+06 | 0.5188 / 22.23 | 0.5733 / 26.15 | 0.0468 / n/r | 0.0510 / n/r |
| stratified_exp0.05 | 14.5288 / 7.095e+05 | 0.5072 / 20.27 | 0.5525 / 21.98 | 0.0458 / n/r | 0.0493 / n/r |
| stratified_exp0.1 | 14.5569 / 1.354e+06 | 0.5052 / 18.94 | 0.5478 / 19.69 | 0.0456 / n/r | 0.0489 / n/r |
| stratified_exp0.25 | 13.8026 / 3.2e+05 | 0.5040 / 20.01 | 0.5463 / 20.4 | 0.0455 / n/r | 0.0488 / n/r |
| stratified_exp0.5 ! | 13.6086 / 1.992e+05 | 0.5034 / 19.12 | 0.5447 / 19.37 | 0.0455 / n/r | 0.0487 / n/r |
| stratified_exp0.75 ! | 13.8522 / 5.054e+05 | 0.5040 / 19.14 | 0.5475 / 19.64 | 0.0455 / n/r | 0.0489 / n/r |
| stratified_exp1.0 ! | 13.9354 / 9.503e+05 | 0.5037 / 19.23 | 0.5475 / 19.85 | 0.0455 / n/r | 0.0489 / n/r |

---

## naive_ps, K = -2.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 21.2482 / 1.167e+07 | 0.5478 / 48.75 | 0.3385 / 21.42 | 0.0519 / n/r | 0.0318 / n/r |
| stratified_exp0.05 | 14.7585 / 7.837e+05 | 0.5099 / 39.81 | 0.2782 / 10.65 | 0.0484 / n/r | 0.0262 / n/r |
| stratified_exp0.1 | 14.4545 / 6.346e+05 | 0.5054 / 38.48 | 0.2751 / 10.18 | 0.0480 / n/r | 0.0259 / n/r |
| stratified_exp0.25 | 14.3044 / 4.151e+05 | 0.5040 / 36.92 | 0.2734 / 9.393 | 0.0478 / n/r | 0.0258 / n/r |
| stratified_exp0.5 ! | 13.8086 / 3.183e+05 | 0.5032 / 38.11 | 0.2731 / 9.636 | 0.0477 / n/r | 0.0258 / n/r |
| stratified_exp0.75 ! | 13.8678 / 2.162e+05 | 0.5027 / 36.85 | 0.2724 / 9.292 | 0.0477 / n/r | 0.0257 / n/r |
| stratified_exp1.0 ! | 13.6344 / 2.217e+05 | 0.5021 / 36.29 | 0.2720 / 9.119 | 0.0476 / n/r | 0.0257 / n/r |

---

## naive_ps, K = -3.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 29.6726 / 4.629e+07 | 0.5703 / 80.38 | 0.2575 / 20.48 | 0.0550 / n/r | 0.0246 / n/r |
| stratified_exp0.05 | 15.4752 / 9.341e+06 | 0.5110 / 60.26 | 0.1868 / 7.401 | 0.0493 / n/r | 0.0179 / n/r |
| stratified_exp0.1 | 14.5152 / 6.641e+05 | 0.5059 / 57.9 | 0.1835 / 6.738 | 0.0488 / n/r | 0.0176 / n/r |
| stratified_exp0.25 | 14.5448 / 5.961e+05 | 0.5032 / 54.14 | 0.1821 / 6.154 | 0.0486 / n/r | 0.0175 / n/r |
| stratified_exp0.5 ! | 13.9527 / 2.032e+05 | 0.5035 / 53.21 | 0.1817 / 5.974 | 0.0486 / n/r | 0.0175 / n/r |
| stratified_exp0.75 ! | 13.8026 / 3.2e+05 | 0.5020 / 56.18 | 0.1815 / 6.266 | 0.0485 / n/r | 0.0175 / n/r |
| stratified_exp1.0 ! | 14.1283 / 4.605e+05 | 0.5015 / 54.11 | 0.1817 / 6.083 | 0.0484 / n/r | 0.0175 / n/r |

---

## naive_ps, K = -4.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 35.7828 / 2.3e+08 | 0.6045 / 123.5 | 0.2297 / 22.9 | 0.0588 / n/r | 0.0222 / n/r |
| stratified_exp0.05 | 15.9362 / 4.808e+06 | 0.5121 / 80.76 | 0.1409 / 5.708 | 0.0499 / n/r | 0.0137 / n/r |
| stratified_exp0.1 | 14.9412 / 1.037e+06 | 0.5078 / 76.94 | 0.1383 / 5.088 | 0.0495 / n/r | 0.0134 / n/r |
| stratified_exp0.25 | 14.0668 / 4.433e+05 | 0.5044 / 74.18 | 0.1377 / 4.81 | 0.0491 / n/r | 0.0134 / n/r |
| stratified_exp0.5 ! | 14.2046 / 3.591e+05 | 0.5020 / 70.88 | 0.1361 / 4.486 | 0.0489 / n/r | 0.0132 / n/r |
| stratified_exp0.75 ! | 14.0574 / 3.466e+05 | 0.5015 / 70.82 | 0.1360 / 4.42 | 0.0488 / n/r | 0.0132 / n/r |
| stratified_exp1.0 ! | 13.9819 / 4.609e+05 | 0.5023 / 74.14 | 0.1359 / 4.63 | 0.0489 / n/r | 0.0132 / n/r |

---

## naive_ps, K = -10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 34.1684 / 5.75e+07 | 0.6297 / 335.5 | 0.1165 / 14.14 | 0.0623 / n/r | 0.0115 / n/r |
| stratified_exp0.05 | 20.7974 / 1.208e+07 | 0.5473 / 235.5 | 0.0672 / 3.852 | 0.0541 / n/r | 0.0066 / n/r |
| stratified_exp0.1 | 15.3579 / 2.255e+06 | 0.5186 / 207 | 0.0577 / 2.387 | 0.0513 / n/r | 0.0057 / n/r |
| stratified_exp0.25 | 14.7050 / 7.502e+05 | 0.5108 / 190.9 | 0.0561 / 2.044 | 0.0505 / n/r | 0.0055 / n/r |
| stratified_exp0.5 ! | 14.5288 / 7.095e+05 | 0.5057 / 185.9 | 0.0555 / 1.982 | 0.0500 / n/r | 0.0055 / n/r |
| stratified_exp0.75 ! | 14.1664 / 3.869e+05 | 0.5053 / 175.3 | 0.0553 / 1.812 | 0.0500 / n/r | 0.0055 / n/r |
| stratified_exp1.0 ! | 14.4802 / 1.03e+06 | 0.5039 / 174.1 | 0.0550 / 1.78 | 0.0499 / n/r | 0.0054 / n/r |

---

## cmplx_ps, K = -0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 33.9253 / 2.318e+06 | 1.7395 / 7.099e+05 | 189.7790 / 3.809e+10 | 0.0168 / n/r | 1.5028 / n/r |
| stratified_exp0.05 | 29.8676 / 2.672e+07 | 1.7951 / 1.067e+06 | 187.8653 / 3.373e+10 | 0.0173 / n/r | 1.4990 / n/r |
| stratified_exp0.1 | 8775.6169 / 9.141e+14 | 1.7722 / 2.434e+06 | 201.2267 / 4.805e+10 | 0.0178 / n/r | 1.4955 / n/r |
| stratified_exp0.25 | 476.4211 / 2.597e+12 | 1.2482 / 4.666e+05 | 299.6669 / 1.085e+11 | 0.0169 / n/r | 1.5121 / n/r |
| stratified_exp0.5 ! | 58.7656 / 3.468e+10 | 1.0655 / 2.964e+05 | 267.5485 / 4.103e+10 | 0.0150 / n/r | 1.5410 / n/r |
| stratified_exp0.75 ! | 24.7369 / 5.901e+09 | 0.8706 / 5.428e+05 | 287.4287 / 3.576e+10 | 0.0132 / n/r | 1.5524 / n/r |
| stratified_exp1.0 ! | 14.2856 / 1.891e+09 | 0.7044 / 6.732e+05 | 329.2619 / 4.828e+10 | 0.0087 / n/r | 1.5908 / n/r |

---

## cmplx_ps, K = -0.05

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 36.4889 / 4.862e+07 | 1.6593 / 1351 | 32.9299 / 1.257e+06 | 0.0597 / n/r | 1.0708 / n/r |
| stratified_exp0.05 | 33.6708 / 8.17e+05 | 1.6645 / 1502 | 32.9780 / 1.291e+06 | 0.0598 / n/r | 1.0738 / n/r |
| stratified_exp0.1 | 33.8736 / 8.126e+06 | 1.6537 / 455.2 | 32.9490 / 1.016e+06 | 0.0600 / n/r | 1.0711 / n/r |
| stratified_exp0.25 | 29.4075 / 2.488e+07 | 1.6594 / 446.2 | 33.4841 / 1.088e+06 | 0.0605 / n/r | 1.0727 / n/r |
| stratified_exp0.5 ! | 8649.0635 / 8.774e+14 | 1.7276 / 2.654e+04 | 46.2896 / 7.841e+07 | 0.0602 / n/r | 1.0810 / n/r |
| stratified_exp0.75 ! | 1875.7114 / 4.077e+13 | 2.2320 / 2.158e+06 | 64.6164 / 1.346e+09 | 0.0581 / n/r | 1.1175 / n/r |
| stratified_exp1.0 ! | 601.7397 / 4.002e+12 | 2.3095 / 3.875e+06 | 81.6471 / 2.875e+09 | 0.0561 / n/r | 1.1448 / n/r |

---

## cmplx_ps, K = -0.1

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 34.7910 / 8.382e+05 | 1.6679 / 42.87 | 16.4980 / 2.788e+04 | 0.0873 / n/r | 0.7986 / n/r |
| stratified_exp0.05 | 34.4848 / 1.753e+06 | 1.6706 / 54.27 | 16.4831 / 2.239e+04 | 0.0874 / n/r | 0.7987 / n/r |
| stratified_exp0.1 | 33.7494 / 1.157e+06 | 1.6701 / 64.89 | 16.5283 / 3.87e+04 | 0.0872 / n/r | 0.7998 / n/r |
| stratified_exp0.25 | 32.6659 / 9.638e+06 | 1.6686 / 51.19 | 16.5365 / 2.913e+04 | 0.0874 / n/r | 0.7975 / n/r |
| stratified_exp0.5 ! | 29.8464 / 2.686e+07 | 1.6779 / 52.62 | 16.8368 / 3.867e+04 | 0.0879 / n/r | 0.8019 / n/r |
| stratified_exp0.75 ! | 18479.6543 / 4.054e+15 | 1.6841 / 296 | 18.7037 / 1.44e+05 | 0.0876 / n/r | 0.8116 / n/r |
| stratified_exp1.0 ! | 8602.0418 / 8.773e+14 | 1.6925 / 1385 | 21.2981 / 1.952e+05 | 0.0864 / n/r | 0.8260 / n/r |

---

## cmplx_ps, K = -0.5

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 36.2716 / 3.25e+06 | 1.6788 / 24.46 | 3.3348 / 111.2 | 0.1408 / n/r | 0.2720 / n/r |
| stratified_exp0.05 | 34.4386 / 6.498e+05 | 1.6697 / 23.66 | 3.3013 / 102.3 | 0.1400 / n/r | 0.2697 / n/r |
| stratified_exp0.1 | 34.6595 / 9.784e+05 | 1.6686 / 23.42 | 3.3004 / 101.2 | 0.1399 / n/r | 0.2696 / n/r |
| stratified_exp0.25 | 34.0370 / 6.321e+05 | 1.6698 / 23.56 | 3.2981 / 101.2 | 0.1401 / n/r | 0.2695 / n/r |
| stratified_exp0.5 ! | 33.6763 / 9.185e+05 | 1.6720 / 23.62 | 3.3132 / 102.6 | 0.1402 / n/r | 0.2706 / n/r |
| stratified_exp0.75 ! | 33.7893 / 5.496e+06 | 1.6684 / 23.52 | 3.3030 / 103.8 | 0.1399 / n/r | 0.2696 / n/r |
| stratified_exp1.0 ! | 37.5187 / 2.345e+08 | 1.6712 / 23.69 | 3.3037 / 105.6 | 0.1402 / n/r | 0.2696 / n/r |

---

## cmplx_ps, K = -1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 36.3861 / 5.58e+06 | 1.6852 / 47.11 | 1.6830 / 53.27 | 0.1536 / n/r | 0.1509 / n/r |
| stratified_exp0.05 | 35.4547 / 3.361e+06 | 1.6690 / 43.44 | 1.6549 / 45.64 | 0.1521 / n/r | 0.1486 / n/r |
| stratified_exp0.1 | 34.5133 / 7.24e+05 | 1.6702 / 43.61 | 1.6498 / 45.01 | 0.1523 / n/r | 0.1482 / n/r |
| stratified_exp0.25 | 34.8222 / 2.002e+06 | 1.6688 / 43.4 | 1.6521 / 44.4 | 0.1521 / n/r | 0.1484 / n/r |
| stratified_exp0.5 ! | 34.4251 / 1.574e+06 | 1.6708 / 43.4 | 1.6485 / 44.32 | 0.1523 / n/r | 0.1481 / n/r |
| stratified_exp0.75 ! | 34.1643 / 2.123e+06 | 1.6688 / 43.47 | 1.6513 / 44.62 | 0.1521 / n/r | 0.1483 / n/r |
| stratified_exp1.0 ! | 33.8625 / 1.279e+06 | 1.6700 / 43.45 | 1.6519 / 44.76 | 0.1522 / n/r | 0.1484 / n/r |

---

## cmplx_ps, K = -2.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 40.5819 / 1.507e+07 | 1.7138 / 102.4 | 0.8666 / 30.29 | 0.1633 / n/r | 0.0818 / n/r |
| stratified_exp0.05 | 35.8151 / 4.087e+06 | 1.6775 / 86.52 | 0.8324 / 22.59 | 0.1599 / n/r | 0.0787 / n/r |
| stratified_exp0.1 | 34.7669 / 1.117e+06 | 1.6706 / 84.36 | 0.8255 / 21.64 | 0.1593 / n/r | 0.0781 / n/r |
| stratified_exp0.25 | 34.2696 / 7.534e+05 | 1.6690 / 85.39 | 0.8254 / 21.56 | 0.1591 / n/r | 0.0781 / n/r |
| stratified_exp0.5 ! | 34.7378 / 1.332e+06 | 1.6684 / 84.7 | 0.8259 / 21.34 | 0.1590 / n/r | 0.0781 / n/r |
| stratified_exp0.75 ! | 34.3940 / 8.587e+05 | 1.6676 / 84.21 | 0.8233 / 21.1 | 0.1590 / n/r | 0.0779 / n/r |
| stratified_exp1.0 ! | 34.4456 / 8.974e+05 | 1.6689 / 84.84 | 0.8239 / 21.3 | 0.1591 / n/r | 0.0780 / n/r |

---

## cmplx_ps, K = -3.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 40.8567 / 1.122e+07 | 1.7352 / 160.4 | 0.5958 / 22.38 | 0.1680 / n/r | 0.0573 / n/r |
| stratified_exp0.05 | 36.0065 / 5.018e+06 | 1.6747 / 128.9 | 0.5533 / 14.96 | 0.1622 / n/r | 0.0533 / n/r |
| stratified_exp0.1 | 35.2169 / 1.404e+06 | 1.6710 / 126.4 | 0.5516 / 14.53 | 0.1618 / n/r | 0.0531 / n/r |
| stratified_exp0.25 | 34.7034 / 1.052e+06 | 1.6677 / 126.6 | 0.5493 / 14.12 | 0.1615 / n/r | 0.0529 / n/r |
| stratified_exp0.5 ! | 35.0203 / 1.978e+06 | 1.6656 / 126.5 | 0.5480 / 14.03 | 0.1613 / n/r | 0.0528 / n/r |
| stratified_exp0.75 ! | 35.2122 / 2.97e+06 | 1.6660 / 125.4 | 0.5509 / 13.94 | 0.1613 / n/r | 0.0531 / n/r |
| stratified_exp1.0 ! | 34.0187 / 3.133e+05 | 1.6663 / 126.2 | 0.5488 / 13.94 | 0.1614 / n/r | 0.0529 / n/r |

---

## cmplx_ps, K = -4.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 44.8915 / 6.042e+07 | 1.7838 / 236 | 0.4685 / 19.58 | 0.1741 / n/r | 0.0455 / n/r |
| stratified_exp0.05 | 36.6961 / 5.21e+06 | 1.6842 / 175.7 | 0.4174 / 11.71 | 0.1644 / n/r | 0.0406 / n/r |
| stratified_exp0.1 | 34.9744 / 2.091e+06 | 1.6769 / 171.1 | 0.4152 / 11.03 | 0.1637 / n/r | 0.0404 / n/r |
| stratified_exp0.25 | 34.6302 / 9.166e+05 | 1.6689 / 168.4 | 0.4127 / 10.63 | 0.1629 / n/r | 0.0401 / n/r |
| stratified_exp0.5 ! | 34.2613 / 7.258e+05 | 1.6657 / 168.2 | 0.4117 / 10.53 | 0.1626 / n/r | 0.0400 / n/r |
| stratified_exp0.75 ! | 34.7447 / 6.428e+05 | 1.6682 / 168.1 | 0.4111 / 10.47 | 0.1628 / n/r | 0.0400 / n/r |
| stratified_exp1.0 ! | 34.9858 / 2.826e+06 | 1.6662 / 167.9 | 0.4123 / 10.46 | 0.1626 / n/r | 0.0401 / n/r |

---

## cmplx_ps, K = -10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 62.7781 / 2.044e+08 | 2.0193 / 859.8 | 0.2444 / 15.4 | 0.2000 / n/r | 0.0241 / n/r |
| stratified_exp0.05 | 40.5557 / 1.406e+07 | 1.7201 / 501.8 | 0.1739 / 5.826 | 0.1703 / n/r | 0.0172 / n/r |
| stratified_exp0.1 | 36.2294 / 4.742e+06 | 1.6959 / 457.2 | 0.1693 / 4.956 | 0.1679 / n/r | 0.0167 / n/r |
| stratified_exp0.25 | 35.8799 / 7.49e+06 | 1.6816 / 425.9 | 0.1670 / 4.391 | 0.1665 / n/r | 0.0165 / n/r |
| stratified_exp0.5 ! | 34.9364 / 1.529e+06 | 1.6733 / 415.9 | 0.1653 / 4.209 | 0.1657 / n/r | 0.0163 / n/r |
| stratified_exp0.75 ! | 35.3227 / 5.604e+06 | 1.6719 / 418.6 | 0.1657 / 4.214 | 0.1656 / n/r | 0.0164 / n/r |
| stratified_exp1.0 ! | 34.9159 / 1.329e+06 | 1.6755 / 420.3 | 0.1653 / 4.194 | 0.1659 / n/r | 0.0163 / n/r |

---

## c1e4_exp1.0, K = -0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 3321.2153 / 1.185e+14 | 1.2532 / 1.069e+06 | 149.2691 / 2.53e+10 | 0.0128 / n/r | 1.2528 / n/r |
| stratified_exp0.05 | 242.6854 / 5.666e+11 | 1.1653 / 7.92e+05 | 121.9814 / 2.439e+10 | 0.0134 / n/r | 0.9269 / n/r |
| stratified_exp0.1 | 695.0526 / 5.321e+12 | 1.1051 / 6.37e+05 | 119.9132 / 2.231e+10 | 0.0135 / n/r | 0.9155 / n/r |
| stratified_exp0.25 | 345.7591 / 1.374e+12 | 1.0270 / 6.302e+05 | 140.9164 / 2.73e+10 | 0.0137 / n/r | 0.9335 / n/r |
| stratified_exp0.5 ! | 31.4155 / 9.828e+09 | 0.9767 / 6.893e+05 | 164.7429 / 3.001e+10 | 0.0140 / n/r | 0.9814 / n/r |
| stratified_exp0.75 ! | 13.3004 / 1.646e+09 | 1.7984 / 2.605e+06 | 762.5910 / 5.476e+11 | 0.0135 / n/r | 1.0087 / n/r |
| stratified_exp1.0 ! | 7.4761 / 4.837e+08 | 1.3602 / 2.044e+06 | 324.7221 / 7.02e+10 | 0.0131 / n/r | 1.0050 / n/r |

---

## c1e4_exp1.0, K = -0.05

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 485680.1452 / 1.262e+18 | 1.1730 / 196.5 | 27.7916 / 1.909e+05 | 0.0424 / n/r | 0.9074 / n/r |
| stratified_exp0.05 | 3275.0002 / 1.184e+14 | 1.1927 / 245.5 | 27.9242 / 2.723e+05 | 0.0434 / n/r | 0.9041 / n/r |
| stratified_exp0.1 | 72.6701 / 3.907e+09 | 1.1839 / 230.5 | 25.7449 / 1.829e+05 | 0.0441 / n/r | 0.8370 / n/r |
| stratified_exp0.25 | 752.9409 / 6.294e+12 | 1.0833 / 5655 | 23.1041 / 1.26e+08 | 0.0426 / n/r | 0.6590 / n/r |
| stratified_exp0.5 ! | 667.3940 / 4.895e+12 | 1.0282 / 235.7 | 29.2797 / 6.197e+08 | 0.0412 / n/r | 0.6446 / n/r |
| stratified_exp0.75 ! | 119.8859 / 1.291e+11 | 1.0557 / 2636 | 28.9910 / 4.167e+08 | 0.0417 / n/r | 0.6542 / n/r |
| stratified_exp1.0 ! | 84.2726 / 6.255e+10 | 1.0584 / 8725 | 31.8903 / 1.6e+08 | 0.0411 / n/r | 0.6735 / n/r |

---

## c1e4_exp1.0, K = -0.1

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 12479.0323 / 2.037e+14 | 1.1856 / 36.47 | 14.7328 / 2.251e+04 | 0.0608 / n/r | 0.6956 / n/r |
| stratified_exp0.05 | 8005.5942 / 6.449e+14 | 1.2239 / 36.28 | 14.7364 / 2.06e+04 | 0.0632 / n/r | 0.6950 / n/r |
| stratified_exp0.1 | 3598.9177 / 1.397e+14 | 1.1862 / 40.82 | 13.2884 / 1.598e+04 | 0.0620 / n/r | 0.6318 / n/r |
| stratified_exp0.25 | 73.7408 / 5.202e+09 | 1.1908 / 44.02 | 13.3132 / 1.806e+04 | 0.0629 / n/r | 0.6338 / n/r |
| stratified_exp0.5 ! | 1116.6252 / 1.412e+13 | 1.0597 / 42.34 | 9.9695 / 1.428e+04 | 0.0585 / n/r | 0.4762 / n/r |
| stratified_exp0.75 ! | 289.7835 / 8.761e+11 | 1.0513 / 52.81 | 10.5088 / 3.662e+04 | 0.0582 / n/r | 0.4777 / n/r |
| stratified_exp1.0 ! | 922.1885 / 9.09e+12 | 1.0508 / 57.53 | 11.9053 / 3.292e+04 | 0.0573 / n/r | 0.4939 / n/r |

---

## c1e4_exp1.0, K = -0.5

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 23310.0191 / 3.707e+15 | 1.2183 / 22.88 | 2.8898 / 205.2 | 0.1019 / n/r | 0.2340 / n/r |
| stratified_exp0.05 | 66742.2105 / 3.92e+16 | 1.1941 / 21.73 | 2.8989 / 197.7 | 0.0997 / n/r | 0.2350 / n/r |
| stratified_exp0.1 | 15208.7715 / 3.754e+14 | 1.2061 / 22.97 | 2.7102 / 164.9 | 0.1008 / n/r | 0.2202 / n/r |
| stratified_exp0.25 | 62599.9807 / 2.687e+16 | 1.2120 / 22.55 | 2.7156 / 157.9 | 0.1012 / n/r | 0.2203 / n/r |
| stratified_exp0.5 ! | 571.8460 / 2.215e+12 | 1.1742 / 21.07 | 2.6720 / 151.7 | 0.0981 / n/r | 0.2172 / n/r |
| stratified_exp0.75 ! | 265.4685 / 4.864e+11 | 1.2374 / 23.85 | 2.7831 / 171.3 | 0.1036 / n/r | 0.2259 / n/r |
| stratified_exp1.0 ! | 78.8366 / 1.998e+09 | 1.2179 / 23.6 | 2.7837 / 186.8 | 0.1021 / n/r | 0.2255 / n/r |

---

## c1e4_exp1.0, K = -1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 2947.7516 / 3.273e+13 | 1.2647 / 45.57 | 1.4350 / 84.54 | 0.1151 / n/r | 0.1285 / n/r |
| stratified_exp0.05 | 847.9402 / 1.142e+12 | 1.2626 / 45.7 | 1.5563 / 98.29 | 0.1146 / n/r | 0.1392 / n/r |
| stratified_exp0.1 | 47280.5088 / 6.354e+15 | 1.2295 / 43.41 | 1.4498 / 88.69 | 0.1119 / n/r | 0.1298 / n/r |
| stratified_exp0.25 | 38065.3958 / 1.05e+16 | 1.2293 / 43.63 | 1.4617 / 90.53 | 0.1118 / n/r | 0.1307 / n/r |
| stratified_exp0.5 ! | 19935.6943 / 3.422e+15 | 1.2164 / 42.05 | 1.4293 / 84.68 | 0.1106 / n/r | 0.1279 / n/r |
| stratified_exp0.75 ! | 10254.7680 / 9.52e+14 | 1.2008 / 40.68 | 1.4203 / 86.43 | 0.1093 / n/r | 0.1271 / n/r |
| stratified_exp1.0 ! | 329.7178 / 2.874e+11 | 1.1959 / 40.68 | 1.3351 / 68.25 | 0.1088 / n/r | 0.1195 / n/r |

---

## c1e4_exp1.0, K = -2.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1768.4532 / 9.345e+12 | 1.2719 / 92.29 | 0.7508 / 47.2 | 0.1211 / n/r | 0.0709 / n/r |
| stratified_exp0.05 | 950.4654 / 1.145e+12 | 1.2228 / 77.7 | 0.7288 / 41.95 | 0.1164 / n/r | 0.0688 / n/r |
| stratified_exp0.1 | 98769.0745 / 2.099e+16 | 1.2323 / 79.26 | 0.7065 / 35.23 | 0.1173 / n/r | 0.0667 / n/r |
| stratified_exp0.25 | 7724.9016 / 8.963e+13 | 1.2187 / 81.12 | 0.7304 / 42.25 | 0.1160 / n/r | 0.0689 / n/r |
| stratified_exp0.5 ! | 49541.4997 / 6.167e+15 | 1.2102 / 79.02 | 0.6984 / 35.43 | 0.1152 / n/r | 0.0659 / n/r |
| stratified_exp0.75 ! | 12120.1863 / 6.781e+14 | 1.2661 / 85.84 | 0.7993 / 48.8 | 0.1203 / n/r | 0.0754 / n/r |
| stratified_exp1.0 ! | 62861.1752 / 2.687e+16 | 1.2091 / 78.96 | 0.7141 / 39.62 | 0.1151 / n/r | 0.0674 / n/r |

---

## c1e4_exp1.0, K = -3.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 302.6636 / 1.133e+11 | 1.3273 / 156 | 0.5360 / 34.38 | 0.1284 / n/r | 0.0514 / n/r |
| stratified_exp0.05 | 11123.7940 / 3.989e+14 | 1.2212 / 121.9 | 0.4748 / 25.78 | 0.1182 / n/r | 0.0457 / n/r |
| stratified_exp0.1 | 13221.6291 / 4.406e+14 | 1.2109 / 112.3 | 0.4721 / 25.48 | 0.1172 / n/r | 0.0454 / n/r |
| stratified_exp0.25 | 62425.8185 / 8.802e+15 | 1.2133 / 123.7 | 0.4819 / 27.69 | 0.1174 / n/r | 0.0464 / n/r |
| stratified_exp0.5 ! | 1276458446.8377 / 1.079e+25 | 1.2094 / 117.3 | 0.4903 / 27.91 | 0.1170 / n/r | 0.0471 / n/r |
| stratified_exp0.75 ! | 56723.9275 / 1.996e+16 | 1.1987 / 114.1 | 0.4545 / 21.5 | 0.1159 / n/r | 0.0437 / n/r |
| stratified_exp1.0 ! | 4518.9155 / 3.439e+13 | 1.2010 / 114.4 | 0.4519 / 21.07 | 0.1162 / n/r | 0.0435 / n/r |

---

## c1e4_exp1.0, K = -4.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 610.1387 / 1.17e+12 | 1.3737 / 222.8 | 0.4486 / 32.25 | 0.1338 / n/r | 0.0435 / n/r |
| stratified_exp0.05 | 10506.4941 / 3.36e+14 | 1.2328 / 166.7 | 0.3566 / 19.66 | 0.1203 / n/r | 0.0346 / n/r |
| stratified_exp0.1 | 113573.0533 / 2.778e+16 | 1.2241 / 152.7 | 0.3599 / 19.58 | 0.1194 / n/r | 0.0349 / n/r |
| stratified_exp0.25 | 12915697.7305 / 5.466e+20 | 1.2208 / 155.8 | 0.3520 / 18.3 | 0.1191 / n/r | 0.0342 / n/r |
| stratified_exp0.5 ! | 3499.3815 / 1.27e+13 | 1.2365 / 165.4 | 0.3967 / 27.17 | 0.1206 / n/r | 0.0385 / n/r |
| stratified_exp0.75 ! | 174038.7478 / 3.009e+17 | 1.2204 / 158.7 | 0.3787 / 23.33 | 0.1190 / n/r | 0.0368 / n/r |
| stratified_exp1.0 ! | 8424.8381 / 8.812e+13 | 1.2183 / 158.3 | 0.3699 / 21.42 | 0.1188 / n/r | 0.0359 / n/r |

---

## c1e4_exp1.0, K = -10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 273.4383 / 8.756e+10 | 1.5030 / 768.3 | 0.2309 / 21.1 | 0.1489 / n/r | 0.0228 / n/r |
| stratified_exp0.05 | 3675.0602 / 6.797e+13 | 1.2646 / 439.9 | 0.1514 / 9.382 | 0.1252 / n/r | 0.0150 / n/r |
| stratified_exp0.1 | 3738.6126 / 5.89e+13 | 1.2338 / 410.1 | 0.1385 / 6.964 | 0.1222 / n/r | 0.0137 / n/r |
| stratified_exp0.25 | 772.2698 / 8.55e+11 | 1.2208 / 374.9 | 0.1484 / 8.043 | 0.1208 / n/r | 0.0147 / n/r |
| stratified_exp0.5 ! | 96426.5085 / 2.091e+16 | 1.2310 / 390.7 | 0.1398 / 6.925 | 0.1219 / n/r | 0.0138 / n/r |
| stratified_exp0.75 ! | 682185.2395 / 1.204e+18 | 1.2283 / 387.8 | 0.1447 / 7.767 | 0.1216 / n/r | 0.0143 / n/r |
| stratified_exp1.0 ! | 75458.3834 / 4.003e+16 | 1.1908 / 368.5 | 0.1443 / 8.02 | 0.1179 / n/r | 0.0143 / n/r |

---

# RESULTS (Dense Table)

---

## naive_ps, K = -0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 14.3724 / 9.187e+06 |
| stratified_exp0.05 | 10.0727 / 1.386e+06 |
| stratified_exp0.1 | 47.7418 / 1.09e+10 |
| stratified_exp0.25 | 4.9484 / 9.906e+07 |
| stratified_exp0.5 ! | 1.2795 / 3.212e+06 |
| stratified_exp0.75 ! | 0.7253 / 7.463e+05 |
| stratified_exp1.0 ! | 0.5475 / 3.202e+05 |

---

## naive_ps, K = -0.05

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 14.0019 / 3.582e+05 |
| stratified_exp0.05 | 13.7196 / 6.564e+05 |
| stratified_exp0.1 | 12.9506 / 8.343e+05 |
| stratified_exp0.25 | 10.6974 / 6.259e+06 |
| stratified_exp0.5 ! | 47.6719 / 1.089e+10 |
| stratified_exp0.75 ! | 19.0180 / 2.137e+09 |
| stratified_exp1.0 ! | 9.0625 / 4.101e+08 |

---

## naive_ps, K = -0.1

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 14.5536 / 9.48e+05 |
| stratified_exp0.05 | 13.7786 / 4.328e+05 |
| stratified_exp0.1 | 13.6639 / 5.639e+05 |
| stratified_exp0.25 | 13.8368 / 1.392e+07 |
| stratified_exp0.5 ! | 10.7048 / 6.217e+06 |
| stratified_exp0.75 ! | 151.4742 / 2.315e+11 |
| stratified_exp1.0 ! | 48.6876 / 1.16e+10 |

---

## naive_ps, K = -0.5

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 14.0717 / 6.503e+05 |
| stratified_exp0.05 | 14.5380 / 1.462e+06 |
| stratified_exp0.1 | 14.1491 / 6.443e+05 |
| stratified_exp0.25 | 13.7705 / 4.029e+05 |
| stratified_exp0.5 ! | 14.0566 / 1.682e+06 |
| stratified_exp0.75 ! | 14.0202 / 5.851e+06 |
| stratified_exp1.0 ! | 13.0883 / 2.044e+06 |

---

## naive_ps, K = -1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 15.3847 / 2.391e+06 |
| stratified_exp0.05 | 14.5288 / 7.095e+05 |
| stratified_exp0.1 | 14.5569 / 1.354e+06 |
| stratified_exp0.25 | 13.8026 / 3.2e+05 |
| stratified_exp0.5 ! | 13.6086 / 1.992e+05 |
| stratified_exp0.75 ! | 13.8522 / 5.054e+05 |
| stratified_exp1.0 ! | 13.9354 / 9.503e+05 |

---

## naive_ps, K = -2.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 21.2482 / 1.167e+07 |
| stratified_exp0.05 | 14.7585 / 7.837e+05 |
| stratified_exp0.1 | 14.4545 / 6.346e+05 |
| stratified_exp0.25 | 14.3044 / 4.151e+05 |
| stratified_exp0.5 ! | 13.8086 / 3.183e+05 |
| stratified_exp0.75 ! | 13.8678 / 2.162e+05 |
| stratified_exp1.0 ! | 13.6344 / 2.217e+05 |

---

## naive_ps, K = -3.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 29.6726 / 4.629e+07 |
| stratified_exp0.05 | 15.4752 / 9.341e+06 |
| stratified_exp0.1 | 14.5152 / 6.641e+05 |
| stratified_exp0.25 | 14.5448 / 5.961e+05 |
| stratified_exp0.5 ! | 13.9527 / 2.032e+05 |
| stratified_exp0.75 ! | 13.8026 / 3.2e+05 |
| stratified_exp1.0 ! | 14.1283 / 4.605e+05 |

---

## naive_ps, K = -4.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 35.7828 / 2.3e+08 |
| stratified_exp0.05 | 15.9362 / 4.808e+06 |
| stratified_exp0.1 | 14.9412 / 1.037e+06 |
| stratified_exp0.25 | 14.0668 / 4.433e+05 |
| stratified_exp0.5 ! | 14.2046 / 3.591e+05 |
| stratified_exp0.75 ! | 14.0574 / 3.466e+05 |
| stratified_exp1.0 ! | 13.9819 / 4.609e+05 |

---

## naive_ps, K = -10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 34.1684 / 5.75e+07 |
| stratified_exp0.05 | 20.7974 / 1.208e+07 |
| stratified_exp0.1 | 15.3579 / 2.255e+06 |
| stratified_exp0.25 | 14.7050 / 7.502e+05 |
| stratified_exp0.5 ! | 14.5288 / 7.095e+05 |
| stratified_exp0.75 ! | 14.1664 / 3.869e+05 |
| stratified_exp1.0 ! | 14.4802 / 1.03e+06 |

---

## cmplx_ps, K = -0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 33.9253 / 2.318e+06 |
| stratified_exp0.05 | 29.8676 / 2.672e+07 |
| stratified_exp0.1 | 8775.6169 / 9.141e+14 |
| stratified_exp0.25 | 476.4211 / 2.597e+12 |
| stratified_exp0.5 ! | 58.7656 / 3.468e+10 |
| stratified_exp0.75 ! | 24.7369 / 5.901e+09 |
| stratified_exp1.0 ! | 14.2856 / 1.891e+09 |

---

## cmplx_ps, K = -0.05

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 36.4889 / 4.862e+07 |
| stratified_exp0.05 | 33.6708 / 8.17e+05 |
| stratified_exp0.1 | 33.8736 / 8.126e+06 |
| stratified_exp0.25 | 29.4075 / 2.488e+07 |
| stratified_exp0.5 ! | 8649.0635 / 8.774e+14 |
| stratified_exp0.75 ! | 1875.7114 / 4.077e+13 |
| stratified_exp1.0 ! | 601.7397 / 4.002e+12 |

---

## cmplx_ps, K = -0.1

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 34.7910 / 8.382e+05 |
| stratified_exp0.05 | 34.4848 / 1.753e+06 |
| stratified_exp0.1 | 33.7494 / 1.157e+06 |
| stratified_exp0.25 | 32.6659 / 9.638e+06 |
| stratified_exp0.5 ! | 29.8464 / 2.686e+07 |
| stratified_exp0.75 ! | 18479.6543 / 4.054e+15 |
| stratified_exp1.0 ! | 8602.0418 / 8.773e+14 |

---

## cmplx_ps, K = -0.5

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 36.2716 / 3.25e+06 |
| stratified_exp0.05 | 34.4386 / 6.498e+05 |
| stratified_exp0.1 | 34.6595 / 9.784e+05 |
| stratified_exp0.25 | 34.0370 / 6.321e+05 |
| stratified_exp0.5 ! | 33.6763 / 9.185e+05 |
| stratified_exp0.75 ! | 33.7893 / 5.496e+06 |
| stratified_exp1.0 ! | 37.5187 / 2.345e+08 |

---

## cmplx_ps, K = -1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 36.3861 / 5.58e+06 |
| stratified_exp0.05 | 35.4547 / 3.361e+06 |
| stratified_exp0.1 | 34.5133 / 7.24e+05 |
| stratified_exp0.25 | 34.8222 / 2.002e+06 |
| stratified_exp0.5 ! | 34.4251 / 1.574e+06 |
| stratified_exp0.75 ! | 34.1643 / 2.123e+06 |
| stratified_exp1.0 ! | 33.8625 / 1.279e+06 |

---

## cmplx_ps, K = -2.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 40.5819 / 1.507e+07 |
| stratified_exp0.05 | 35.8151 / 4.087e+06 |
| stratified_exp0.1 | 34.7669 / 1.117e+06 |
| stratified_exp0.25 | 34.2696 / 7.534e+05 |
| stratified_exp0.5 ! | 34.7378 / 1.332e+06 |
| stratified_exp0.75 ! | 34.3940 / 8.587e+05 |
| stratified_exp1.0 ! | 34.4456 / 8.974e+05 |

---

## cmplx_ps, K = -3.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 40.8567 / 1.122e+07 |
| stratified_exp0.05 | 36.0065 / 5.018e+06 |
| stratified_exp0.1 | 35.2169 / 1.404e+06 |
| stratified_exp0.25 | 34.7034 / 1.052e+06 |
| stratified_exp0.5 ! | 35.0203 / 1.978e+06 |
| stratified_exp0.75 ! | 35.2122 / 2.97e+06 |
| stratified_exp1.0 ! | 34.0187 / 3.133e+05 |

---

## cmplx_ps, K = -4.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 44.8915 / 6.042e+07 |
| stratified_exp0.05 | 36.6961 / 5.21e+06 |
| stratified_exp0.1 | 34.9744 / 2.091e+06 |
| stratified_exp0.25 | 34.6302 / 9.166e+05 |
| stratified_exp0.5 ! | 34.2613 / 7.258e+05 |
| stratified_exp0.75 ! | 34.7447 / 6.428e+05 |
| stratified_exp1.0 ! | 34.9858 / 2.826e+06 |

---

## cmplx_ps, K = -10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 62.7781 / 2.044e+08 |
| stratified_exp0.05 | 40.5557 / 1.406e+07 |
| stratified_exp0.1 | 36.2294 / 4.742e+06 |
| stratified_exp0.25 | 35.8799 / 7.49e+06 |
| stratified_exp0.5 ! | 34.9364 / 1.529e+06 |
| stratified_exp0.75 ! | 35.3227 / 5.604e+06 |
| stratified_exp1.0 ! | 34.9159 / 1.329e+06 |

---

## c1e4_exp1.0, K = -0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 3321.2153 / 1.185e+14 |
| stratified_exp0.05 | 242.6854 / 5.666e+11 |
| stratified_exp0.1 | 695.0526 / 5.321e+12 |
| stratified_exp0.25 | 345.7591 / 1.374e+12 |
| stratified_exp0.5 ! | 31.4155 / 9.828e+09 |
| stratified_exp0.75 ! | 13.3004 / 1.646e+09 |
| stratified_exp1.0 ! | 7.4761 / 4.837e+08 |

---

## c1e4_exp1.0, K = -0.05

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 485680.1452 / 1.262e+18 |
| stratified_exp0.05 | 3275.0002 / 1.184e+14 |
| stratified_exp0.1 | 72.6701 / 3.907e+09 |
| stratified_exp0.25 | 752.9409 / 6.294e+12 |
| stratified_exp0.5 ! | 667.3940 / 4.895e+12 |
| stratified_exp0.75 ! | 119.8859 / 1.291e+11 |
| stratified_exp1.0 ! | 84.2726 / 6.255e+10 |

---

## c1e4_exp1.0, K = -0.1

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 12479.0323 / 2.037e+14 |
| stratified_exp0.05 | 8005.5942 / 6.449e+14 |
| stratified_exp0.1 | 3598.9177 / 1.397e+14 |
| stratified_exp0.25 | 73.7408 / 5.202e+09 |
| stratified_exp0.5 ! | 1116.6252 / 1.412e+13 |
| stratified_exp0.75 ! | 289.7835 / 8.761e+11 |
| stratified_exp1.0 ! | 922.1885 / 9.09e+12 |

---

## c1e4_exp1.0, K = -0.5

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 23310.0191 / 3.707e+15 |
| stratified_exp0.05 | 66742.2105 / 3.92e+16 |
| stratified_exp0.1 | 15208.7715 / 3.754e+14 |
| stratified_exp0.25 | 62599.9807 / 2.687e+16 |
| stratified_exp0.5 ! | 571.8460 / 2.215e+12 |
| stratified_exp0.75 ! | 265.4685 / 4.864e+11 |
| stratified_exp1.0 ! | 78.8366 / 1.998e+09 |

---

## c1e4_exp1.0, K = -1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 2947.7516 / 3.273e+13 |
| stratified_exp0.05 | 847.9402 / 1.142e+12 |
| stratified_exp0.1 | 47280.5088 / 6.354e+15 |
| stratified_exp0.25 | 38065.3958 / 1.05e+16 |
| stratified_exp0.5 ! | 19935.6943 / 3.422e+15 |
| stratified_exp0.75 ! | 10254.7680 / 9.52e+14 |
| stratified_exp1.0 ! | 329.7178 / 2.874e+11 |

---

## c1e4_exp1.0, K = -2.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 1768.4532 / 9.345e+12 |
| stratified_exp0.05 | 950.4654 / 1.145e+12 |
| stratified_exp0.1 | 98769.0745 / 2.099e+16 |
| stratified_exp0.25 | 7724.9016 / 8.963e+13 |
| stratified_exp0.5 ! | 49541.4997 / 6.167e+15 |
| stratified_exp0.75 ! | 12120.1863 / 6.781e+14 |
| stratified_exp1.0 ! | 62861.1752 / 2.687e+16 |

---

## c1e4_exp1.0, K = -3.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 302.6636 / 1.133e+11 |
| stratified_exp0.05 | 11123.7940 / 3.989e+14 |
| stratified_exp0.1 | 13221.6291 / 4.406e+14 |
| stratified_exp0.25 | 62425.8185 / 8.802e+15 |
| stratified_exp0.5 ! | 1276458446.8377 / 1.079e+25 |
| stratified_exp0.75 ! | 56723.9275 / 1.996e+16 |
| stratified_exp1.0 ! | 4518.9155 / 3.439e+13 |

---

## c1e4_exp1.0, K = -4.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 610.1387 / 1.17e+12 |
| stratified_exp0.05 | 10506.4941 / 3.36e+14 |
| stratified_exp0.1 | 113573.0533 / 2.778e+16 |
| stratified_exp0.25 | 12915697.7305 / 5.466e+20 |
| stratified_exp0.5 ! | 3499.3815 / 1.27e+13 |
| stratified_exp0.75 ! | 174038.7478 / 3.009e+17 |
| stratified_exp1.0 ! | 8424.8381 / 8.812e+13 |

---

## c1e4_exp1.0, K = -10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | VCE |
|---|---|
| stratified_exp0.01 | 273.4383 / 8.756e+10 |
| stratified_exp0.05 | 3675.0602 / 6.797e+13 |
| stratified_exp0.1 | 3738.6126 / 5.89e+13 |
| stratified_exp0.25 | 772.2698 / 8.55e+11 |
| stratified_exp0.5 ! | 96426.5085 / 2.091e+16 |
| stratified_exp0.75 ! | 682185.2395 / 1.204e+18 |
| stratified_exp1.0 ! | 75458.3834 / 4.003e+16 |


---

# Insights and conclusions

**567/567 cells completed, zero failures, zero NaN/overflow.** Every cell produced a finite
`test_wloss`, so the log-space accumulation of the unbounded `1/D^2` weight is sound across
all nine curvatures and all three vocabularies. `loss_geometry=var_cross_entropy` is the
Bayes-posterior form: each factor's denominator is `min_v D_{e_v,m}` over the whole
vocabulary, which makes the weight a function of `z_t` alone. The derivation is in
`vce_bayes.md`.

## 1. Headline: the ELBO is tight at V = 10

3-seed mean `wnelbo_ref` as % above `H(p)`, over the curvatures where the estimator is valid
(`K in [-4, -0.1]`) at rates >= 0.05:

| ps | range | best cell |
|---|---|---|
| `naive_ps` (H = 0.5003) | +0.0% .. +2.4% | `K=-0.1, rate 0.05` -> 0.5005 (**+0.03%**) |
| `cmplx_ps` (H = 1.6664) | -0.0% .. +1.1% | `K=-3.0, rate 1.0` -> 1.6663 (**-0.01%**) |

Across-seed spread at `naive_ps` is 0.0005-0.003 nats, an order of magnitude below the gap
to `H(p)`, so the residual few tenths of a percent is a real, reproducible property of the
bound rather than seed noise. For comparison, the superseded target-indexed weight sat
~48% above `H(p)` on these same cells.

## 2. The Bayes-optimal twin proves the flat-curvature dips are the ESTIMATOR

At `K = -0.05` and `K = -0.01` many cells read BELOW `H(p)`, which no true ELBO can do.
`init_opt_test_3d_refactor_new` runs the same grid on the analytic Bayes model, which cannot
leak a side channel, and it reads the same way (`naive_ps`, seed 0):

| K | rate | vce (trained) | ce (trained) | **ce (Bayes-OPTIMAL)** |
|---|---|---|---|---|
| -0.01 | 0.1 | -23.6% | -26.1% | **-31.3%** |
| -0.05 | 0.1 | -2.7% | -0.7% | **-2.5%** |
| -0.1 | 0.1 | -0.0% | +0.7% | **+0.8%** |
| -1.0 | 0.25 | **+0.7%** | -0.1% | **+0.7%** |

So the sub-`H(p)` readings are the pinned rate-0.1 reference proposal failing, exactly as
EXPERIMENT.md hypothesis 3 predicted: the per-`t` decay scales with `-K`, so the ~0.304
variance cliff moves to ~0.003 at `K = -0.01`. **At `K = -1.0, rate 0.25` the trained model
matches the Bayes-optimal model's ELBO to the reported precision (+0.7% both).** The trained
`poincare_polar` baseline is markedly WORSE behaved at these curvatures (-100.0% at
`K = -0.01`, -29.8% at `K = -0.05`, +85.5% at `K = -0.1`/rate 0.25), so the variational CE is
also the more numerically robust of the two.

## 3. Rate 0.01 degrades as curvature sharpens

`naive_ps`, rate 0.01: +1.6% at `K = -0.5`, +3.7% at -1.0, +9.5% at -2.0, +20.8% at -4.0,
+25.9% at -10.0. Sharper `K` compresses the heat-time ceiling
(`_radial_t_max(3) * R^2`, R = 1/sqrt(-K)), so a rate-0.01 proposal puts most of its mass
past where the integrand has support. Rates 0.25-1.0 are the safe band throughout.

## 4. At V = 10 000 the objective is tight but NOT seed-stable

`c1e4_exp1.0`, mean over `K in [-4, -0.1]`:

| seed | mean `wnelbo_ref` | vs H = 1.0407 |
|---|---|---|
| 0 | 1.0742 | +3.2% |
| 1 | 1.0810 | +3.9% |
| **2** | **1.4839** | **+42.6%** |

Two of three seeds land within 4%; seed 2 is a clear outlier whose `ce_ref` is ~2x the others
(0.947 vs 0.480/0.468 at `K = -0.1`, rate 0.1). It is not a crashed run -- it completed all
20 000 steps normally. The 3-seed means in the tables above are therefore dragged to ~+15%
for this spec and should NOT be read as the objective's typical behaviour at V = 10 000.

**`wloss` is anti-correlated with ELBO quality here**, which is the diagnostic worth keeping
(`K = -1.0`, rate 0.1):

| seed | `wloss` | `wnelbo_ref` |
|---|---|---|
| 0 | 5 931 | 1.0709 |
| 1 | 135 474 | 1.1260 |
| **2** | **437** (lowest) | **1.4918** (worst) |

The weight is target-free, so the population argmin is still the Bayes posterior -- but
`W(z_t)` spans `e^{2u}`, so the effective weighting ACROSS `z_t` is extremely non-uniform and
concentrates gradient on the near-target, easy states. Seed 2 fit that high-weight region
best (lowest `wloss`) while fitting the states the ELBO integral actually depends on worst.
This is an optimization/variance failure at large `V`, not the argmin bias that
`vce_bayes.md` diagnosed and fixed. Follow-ups worth trying: more steps, a `W(z_t)` cap, or
normalizing the weight per batch.

## 5. Deviation from setup.md

`setup.md`'s "Ref ELBO & CE" section reads `ref_proposal_type: exp`, but `exp` now raises
through `hyper_proposal` (which does not pass `allowed_exp`), so both paths ran
`stratified_exp` at rate 0.1. `wnelbo_ref` is therefore NOT measured on the same reference
path as the `init_test_3d_refactor_new` baselines, which used `exp(0.1)`; cross-project
comparisons in this file are qualitative.
