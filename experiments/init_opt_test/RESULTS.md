# init_opt_test results

- runs collected: **210** / 210 (100%) — run dirs without test_metrics.json: 0
- H(naive_ps) = **0.5003** — wnelbo_ref is bounded below by this
- H(cmplx_ps) = **1.6664** — wnelbo_ref is bounded below by this
- H(c1e2_exp1.0) = **1.0407** — wnelbo_ref is bounded below by this
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
| exp0.01 | 2.4249 ± 0.0040 | 0.5019 ± 0.0009 | 2.4447 ± 0.0060 | 0.0339 ± 0.0000 | 0.1619 ± 0.0003 |
| exp0.05 | 2.4306 ± 0.0154 | 0.5019 ± 0.0009 | 2.4447 ± 0.0060 | 0.0339 ± 0.0000 | 0.1619 ± 0.0003 |
| exp0.1 | 2.4420 ± 0.0111 | 0.5019 ± 0.0009 | 2.4447 ± 0.0060 | 0.0339 ± 0.0000 | 0.1619 ± 0.0003 |
| exp0.25 | 2.4474 ± 0.0329 | 0.5019 ± 0.0009 | 2.4447 ± 0.0060 | 0.0339 ± 0.0000 | 0.1619 ± 0.0003 |
| exp0.5 ! | 2.3829 ± 0.0363 | 0.5019 ± 0.0009 | 2.4447 ± 0.0060 | 0.0339 ± 0.0000 | 0.1619 ± 0.0003 |
| exp0.75 ! | 2.3110 ± 0.0135 | 0.5019 ± 0.0009 | 2.4447 ± 0.0060 | 0.0339 ± 0.0000 | 0.1619 ± 0.0003 |
| exp1.0 ! | 2.2450 ± 0.1038 | 0.5019 ± 0.0009 | 2.4447 ± 0.0060 | 0.0339 ± 0.0000 | 0.1619 ± 0.0003 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.5001 ± 0.0044 | 0.5019 ± 0.0009 | 2.4447 ± 0.0060 | 0.0339 ± 0.0000 | 0.1619 ± 0.0003 |
| exp0.05 | 0.4990 ± 0.0024 | 0.5019 ± 0.0009 | 2.4447 ± 0.0060 | 0.0339 ± 0.0000 | 0.1619 ± 0.0003 |
| exp0.1 | 0.4999 ± 0.0019 | 0.5019 ± 0.0009 | 2.4447 ± 0.0060 | 0.0339 ± 0.0000 | 0.1619 ± 0.0003 |
| exp0.25 | 0.5024 ± 0.0056 | 0.5019 ± 0.0009 | 2.4447 ± 0.0060 | 0.0339 ± 0.0000 | 0.1619 ± 0.0003 |
| exp0.5 ! | 0.4939 ± 0.0094 | 0.5019 ± 0.0009 | 2.4447 ± 0.0060 | 0.0339 ± 0.0000 | 0.1619 ± 0.0003 |
| exp0.75 ! | 0.4859 ± 0.0092 | 0.5019 ± 0.0009 | 2.4447 ± 0.0060 | 0.0339 ± 0.0000 | 0.1619 ± 0.0003 |
| exp1.0 ! | 0.4716 ± 0.0207 | 0.5019 ± 0.0009 | 2.4447 ± 0.0060 | 0.0339 ± 0.0000 | 0.1619 ± 0.0003 |

---

## cmplx_ps

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 6.7929 ± 0.0216 | 1.6687 ± 0.0008 | 6.8236 ± 0.0016 | 0.1202 ± 0.0000 | 0.4666 ± 0.0001 |
| exp0.05 | 6.8092 ± 0.0145 | 1.6687 ± 0.0008 | 6.8236 ± 0.0016 | 0.1202 ± 0.0000 | 0.4666 ± 0.0001 |
| exp0.1 | 6.8225 ± 0.0115 | 1.6687 ± 0.0008 | 6.8236 ± 0.0016 | 0.1202 ± 0.0000 | 0.4666 ± 0.0001 |
| exp0.25 | 6.8086 ± 0.0394 | 1.6687 ± 0.0008 | 6.8236 ± 0.0016 | 0.1202 ± 0.0000 | 0.4666 ± 0.0001 |
| exp0.5 ! | 6.7264 ± 0.1171 | 1.6687 ± 0.0008 | 6.8236 ± 0.0016 | 0.1202 ± 0.0000 | 0.4666 ± 0.0001 |
| exp0.75 ! | 6.5370 ± 0.1078 | 1.6687 ± 0.0008 | 6.8236 ± 0.0016 | 0.1202 ± 0.0000 | 0.4666 ± 0.0001 |
| exp1.0 ! | 6.4613 ± 0.4541 | 1.6687 ± 0.0008 | 6.8236 ± 0.0016 | 0.1202 ± 0.0000 | 0.4666 ± 0.0001 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.6607 ± 0.0059 | 1.6687 ± 0.0008 | 6.8236 ± 0.0016 | 0.1202 ± 0.0000 | 0.4666 ± 0.0001 |
| exp0.05 | 1.6650 ± 0.0023 | 1.6687 ± 0.0008 | 6.8236 ± 0.0016 | 0.1202 ± 0.0000 | 0.4666 ± 0.0001 |
| exp0.1 | 1.6683 ± 0.0020 | 1.6687 ± 0.0008 | 6.8236 ± 0.0016 | 0.1202 ± 0.0000 | 0.4666 ± 0.0001 |
| exp0.25 | 1.6669 ± 0.0067 | 1.6687 ± 0.0008 | 6.8236 ± 0.0016 | 0.1202 ± 0.0000 | 0.4666 ± 0.0001 |
| exp0.5 ! | 1.6519 ± 0.0197 | 1.6687 ± 0.0008 | 6.8236 ± 0.0016 | 0.1202 ± 0.0000 | 0.4666 ± 0.0001 |
| exp0.75 ! | 1.6244 ± 0.0120 | 1.6687 ± 0.0008 | 6.8236 ± 0.0016 | 0.1202 ± 0.0000 | 0.4666 ± 0.0001 |
| exp1.0 ! | 1.6223 ± 0.1060 | 1.6687 ± 0.0008 | 6.8236 ± 0.0016 | 0.1202 ± 0.0000 | 0.4666 ± 0.0001 |

---

## c1e2_exp1.0

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 9.5098 ± 0.0158 | 1.0429 ± 0.0014 | 9.5427 ± 0.0082 | 0.0488 ± 0.0001 | 0.5532 ± 0.0003 |
| exp0.05 | 9.5243 ± 0.0133 | 1.0429 ± 0.0014 | 9.5427 ± 0.0082 | 0.0488 ± 0.0001 | 0.5532 ± 0.0003 |
| exp0.1 | 9.5318 ± 0.0139 | 1.0429 ± 0.0014 | 9.5427 ± 0.0082 | 0.0488 ± 0.0001 | 0.5532 ± 0.0003 |
| exp0.25 | 9.5305 ± 0.0727 | 1.0429 ± 0.0014 | 9.5427 ± 0.0082 | 0.0488 ± 0.0001 | 0.5532 ± 0.0003 |
| exp0.5 ! | 9.3903 ± 0.3537 | 1.0429 ± 0.0014 | 9.5427 ± 0.0082 | 0.0488 ± 0.0001 | 0.5532 ± 0.0003 |
| exp0.75 ! | 9.0730 ± 0.5716 | 1.0429 ± 0.0014 | 9.5427 ± 0.0082 | 0.0488 ± 0.0001 | 0.5532 ± 0.0003 |
| exp1.0 ! | 8.3804 ± 0.3670 | 1.0429 ± 0.0014 | 9.5427 ± 0.0082 | 0.0488 ± 0.0001 | 0.5532 ± 0.0003 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0386 ± 0.0056 | 1.0429 ± 0.0014 | 9.5427 ± 0.0082 | 0.0488 ± 0.0001 | 0.5532 ± 0.0003 |
| exp0.05 | 1.0425 ± 0.0008 | 1.0429 ± 0.0014 | 9.5427 ± 0.0082 | 0.0488 ± 0.0001 | 0.5532 ± 0.0003 |
| exp0.1 | 1.0405 ± 0.0026 | 1.0429 ± 0.0014 | 9.5427 ± 0.0082 | 0.0488 ± 0.0001 | 0.5532 ± 0.0003 |
| exp0.25 | 1.0463 ± 0.0086 | 1.0429 ± 0.0014 | 9.5427 ± 0.0082 | 0.0488 ± 0.0001 | 0.5532 ± 0.0003 |
| exp0.5 ! | 1.0331 ± 0.0501 | 1.0429 ± 0.0014 | 9.5427 ± 0.0082 | 0.0488 ± 0.0001 | 0.5532 ± 0.0003 |
| exp0.75 ! | 1.0139 ± 0.1638 | 1.0429 ± 0.0014 | 9.5427 ± 0.0082 | 0.0488 ± 0.0001 | 0.5532 ± 0.0003 |
| exp1.0 ! | 0.8222 ± 0.0171 | 1.0429 ± 0.0014 | 9.5427 ± 0.0082 | 0.0488 ± 0.0001 | 0.5532 ± 0.0003 |

---

## c1e3_exp1.0

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 14.2790 ± 0.0170 | 1.0407 ± 0.0013 | 14.3231 ± 0.0019 | 0.0330 ± 0.0001 | 0.7115 ± 0.0005 |
| exp0.05 | 14.3158 ± 0.0076 | 1.0407 ± 0.0013 | 14.3231 ± 0.0019 | 0.0330 ± 0.0001 | 0.7115 ± 0.0005 |
| exp0.1 | 14.3181 ± 0.0305 | 1.0407 ± 0.0013 | 14.3231 ± 0.0019 | 0.0330 ± 0.0001 | 0.7115 ± 0.0005 |
| exp0.25 | 14.3326 ± 0.1264 | 1.0407 ± 0.0013 | 14.3231 ± 0.0019 | 0.0330 ± 0.0001 | 0.7115 ± 0.0005 |
| exp0.5 ! | 14.0191 ± 0.5947 | 1.0407 ± 0.0013 | 14.3231 ± 0.0019 | 0.0330 ± 0.0001 | 0.7115 ± 0.0005 |
| exp0.75 ! | 12.7944 ± 0.6394 | 1.0407 ± 0.0013 | 14.3231 ± 0.0019 | 0.0330 ± 0.0001 | 0.7115 ± 0.0005 |
| exp1.0 ! | 11.4590 ± 0.2919 | 1.0407 ± 0.0013 | 14.3231 ± 0.0019 | 0.0330 ± 0.0001 | 0.7115 ± 0.0005 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0379 ± 0.0058 | 1.0407 ± 0.0013 | 14.3231 ± 0.0019 | 0.0330 ± 0.0001 | 0.7115 ± 0.0005 |
| exp0.05 | 1.0406 ± 0.0025 | 1.0407 ± 0.0013 | 14.3231 ± 0.0019 | 0.0330 ± 0.0001 | 0.7115 ± 0.0005 |
| exp0.1 | 1.0411 ± 0.0018 | 1.0407 ± 0.0013 | 14.3231 ± 0.0019 | 0.0330 ± 0.0001 | 0.7115 ± 0.0005 |
| exp0.25 | 1.0407 ± 0.0254 | 1.0407 ± 0.0013 | 14.3231 ± 0.0019 | 0.0330 ± 0.0001 | 0.7115 ± 0.0005 |
| exp0.5 ! | 0.9666 ± 0.0504 | 1.0407 ± 0.0013 | 14.3231 ± 0.0019 | 0.0330 ± 0.0001 | 0.7115 ± 0.0005 |
| exp0.75 ! | 0.8085 ± 0.0523 | 1.0407 ± 0.0013 | 14.3231 ± 0.0019 | 0.0330 ± 0.0001 | 0.7115 ± 0.0005 |
| exp1.0 ! | 0.6786 ± 0.1550 | 1.0407 ± 0.0013 | 14.3231 ± 0.0019 | 0.0330 ± 0.0001 | 0.7115 ± 0.0005 |

---

## c1e4_exp1.0

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 19.0829 ± 0.0436 | 1.0395 ± 0.0017 | 19.1178 ± 0.0169 | 0.0222 ± 0.0000 | 0.8187 ± 0.0003 |
| exp0.05 | 19.1085 ± 0.0203 | 1.0395 ± 0.0017 | 19.1178 ± 0.0169 | 0.0222 ± 0.0000 | 0.8187 ± 0.0003 |
| exp0.1 | 19.1080 ± 0.0341 | 1.0395 ± 0.0017 | 19.1178 ± 0.0169 | 0.0222 ± 0.0000 | 0.8187 ± 0.0003 |
| exp0.25 | 19.0166 ± 0.1526 | 1.0395 ± 0.0017 | 19.1178 ± 0.0169 | 0.0222 ± 0.0000 | 0.8187 ± 0.0003 |
| exp0.5 ! | 18.5086 ± 0.7313 | 1.0395 ± 0.0017 | 19.1178 ± 0.0169 | 0.0222 ± 0.0000 | 0.8187 ± 0.0003 |
| exp0.75 ! | 16.1585 ± 0.0639 | 1.0395 ± 0.0017 | 19.1178 ± 0.0169 | 0.0222 ± 0.0000 | 0.8187 ± 0.0003 |
| exp1.0 ! | 13.5306 ± 0.5856 | 1.0395 ± 0.0017 | 19.1178 ± 0.0169 | 0.0222 ± 0.0000 | 0.8187 ± 0.0003 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.0395 ± 0.0033 | 1.0395 ± 0.0017 | 19.1178 ± 0.0169 | 0.0222 ± 0.0000 | 0.8187 ± 0.0003 |
| exp0.05 | 1.0394 ± 0.0066 | 1.0395 ± 0.0017 | 19.1178 ± 0.0169 | 0.0222 ± 0.0000 | 0.8187 ± 0.0003 |
| exp0.1 | 1.0432 ± 0.0033 | 1.0395 ± 0.0017 | 19.1178 ± 0.0169 | 0.0222 ± 0.0000 | 0.8187 ± 0.0003 |
| exp0.25 | 1.0434 ± 0.0283 | 1.0395 ± 0.0017 | 19.1178 ± 0.0169 | 0.0222 ± 0.0000 | 0.8187 ± 0.0003 |
| exp0.5 ! | 0.9716 ± 0.0479 | 1.0395 ± 0.0017 | 19.1178 ± 0.0169 | 0.0222 ± 0.0000 | 0.8187 ± 0.0003 |
| exp0.75 ! | 0.9040 ± 0.3448 | 1.0395 ± 0.0017 | 19.1178 ± 0.0169 | 0.0222 ± 0.0000 | 0.8187 ± 0.0003 |
| exp1.0 ! | 0.4961 ± 0.2520 | 1.0395 ± 0.0017 | 19.1178 ± 0.0169 | 0.0222 ± 0.0000 | 0.8187 ± 0.0003 |

---

# RESULTS (Dense Table)

---

## naive_ps

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 0.5001 ± 0.0044 | 2.4249 ± 0.0040 |
| exp0.05 | 0.4990 ± 0.0024 | 2.4306 ± 0.0154 |
| exp0.1 | 0.4999 ± 0.0019 | 2.4420 ± 0.0111 |
| exp0.25 | 0.5024 ± 0.0056 | 2.4474 ± 0.0329 |
| exp0.5 ! | 0.4939 ± 0.0094 | 2.3829 ± 0.0363 |
| exp0.75 ! | 0.4859 ± 0.0092 | 2.3110 ± 0.0135 |
| exp1.0 ! | 0.4716 ± 0.0207 | 2.2450 ± 0.1038 |

---

## cmplx_ps

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.6607 ± 0.0059 | 6.7929 ± 0.0216 |
| exp0.05 | 1.6650 ± 0.0023 | 6.8092 ± 0.0145 |
| exp0.1 | 1.6683 ± 0.0020 | 6.8225 ± 0.0115 |
| exp0.25 | 1.6669 ± 0.0067 | 6.8086 ± 0.0394 |
| exp0.5 ! | 1.6519 ± 0.0197 | 6.7264 ± 0.1171 |
| exp0.75 ! | 1.6244 ± 0.0120 | 6.5370 ± 0.1078 |
| exp1.0 ! | 1.6223 ± 0.1060 | 6.4613 ± 0.4541 |

---

## c1e2_exp1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0386 ± 0.0056 | 9.5098 ± 0.0158 |
| exp0.05 | 1.0425 ± 0.0008 | 9.5243 ± 0.0133 |
| exp0.1 | 1.0405 ± 0.0026 | 9.5318 ± 0.0139 |
| exp0.25 | 1.0463 ± 0.0086 | 9.5305 ± 0.0727 |
| exp0.5 ! | 1.0331 ± 0.0501 | 9.3903 ± 0.3537 |
| exp0.75 ! | 1.0139 ± 0.1638 | 9.0730 ± 0.5716 |
| exp1.0 ! | 0.8222 ± 0.0171 | 8.3804 ± 0.3670 |

---

## c1e3_exp1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0379 ± 0.0058 | 14.2790 ± 0.0170 |
| exp0.05 | 1.0406 ± 0.0025 | 14.3158 ± 0.0076 |
| exp0.1 | 1.0411 ± 0.0018 | 14.3181 ± 0.0305 |
| exp0.25 | 1.0407 ± 0.0254 | 14.3326 ± 0.1264 |
| exp0.5 ! | 0.9666 ± 0.0504 | 14.0191 ± 0.5947 |
| exp0.75 ! | 0.8085 ± 0.0523 | 12.7944 ± 0.6394 |
| exp1.0 ! | 0.6786 ± 0.1550 | 11.4590 ± 0.2919 |

---

## c1e4_exp1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.0395 ± 0.0033 | 19.0829 ± 0.0436 |
| exp0.05 | 1.0394 ± 0.0066 | 19.1085 ± 0.0203 |
| exp0.1 | 1.0432 ± 0.0033 | 19.1080 ± 0.0341 |
| exp0.25 | 1.0434 ± 0.0283 | 19.0166 ± 0.1526 |
| exp0.5 ! | 0.9716 ± 0.0479 | 18.5086 ± 0.7313 |
| exp0.75 ! | 0.9040 ± 0.3448 | 16.1585 ± 0.0639 |
| exp1.0 ! | 0.4961 ± 0.2520 | 13.5306 ± 0.5856 |


---

# Insights and conclusions

> Everything above this line is generated by `experiments/report.py init_opt_test`.
> This section is hand-written; `report.py` now carries it across a regeneration
> verbatim (it splits on this heading), so the tables can be rebuilt safely.

The model is the closed-form `OptimalModel`, so it contributes **zero** error.
Every number below is a property of the importance-weighted *estimator*.

`c1e2_exp1.0` / `c1e3_exp1.0` / `c1e4_exp1.0` are the **same** geometric
distribution `p_i ∝ e^-i` truncated at V = 100 / 1000 / 10000. They share one
entropy — the analytic `geometric(e^-1)` value **1.0406518523** — and one
effective support (only ~16 tokens get a nonzero quota in a 4M draw). So any
metric that moves across those three is a function of the **vocabulary**, not of
the distribution being modelled.

Two auxiliary measurements support the sections below. Both are reproducible from
`experiments/init_opt_test/` (the driver scripts are in the session scratchpad):
the per-`t` **first and second moments** of the exact model's loss,
`L1(t) = E[loss | t]` and `L2(t) = E[loss² | t]`, on a 370-point grid out to
`t = 400`, 32768 draws per point. Because

```
E[W] = ∫ L1(t) dt        E[W²] = (1/λ) ∫ L2(t) e^{λt} dt        W = loss/q(t)
```

these give the estimator's exact mean and variance for **every** proposal rate
without assuming anything about the shape of `L(t)`. Validation: the profiles
reproduce `test_nelbo_ref` and `test_ce_ref` to 3–4 digits at every V, and
reproduce `test_wloss_std` to within 0–5% at every rate ≤ 0.1.

---

## 1. The loss path does not leak into the reference path — bit-exactly

Within each of the 15 `(ps, seed)` groups, all 14 `(loss_geometry, rate)` cells
returned **IEEE-754 bit-identical** `wnelbo_ref`, `nelbo_ref`, `wce_ref`,
`ce_ref`, `wnelbo_ref_std` and `wce_ref_std` — a single distinct 64-bit pattern
per field per group, 15/15 groups, across different nodes and GPU models.

Controls: in the same groups `test_wloss` takes 14/14 *distinct* values, and
`wnelbo_ref` takes 3/3 distinct values across seeds — so this is genuine
invariance, not duplicated files. The `salt=0` / `salt=1` split in
`_make_step_generator` is fully decoupled, with no shared generator state.
Reference metrics from runs trained on different objectives at different
proposals are directly comparable. This is the cheapest regression test the repo
has for that split, and it now passes at V = 10 through 10000.

## 2. The polar ELBO is tight at the Bayes optimum — at every V

| ps | V | H(p) | mean `wnelbo_ref` | gap | pooled SE₃ | gap/SE₃ |
|---|---|---|---|---|---|---|
| naive_ps | 10 | 0.500288 | 0.501850 | +0.001562 | 0.000894 | +1.75 |
| cmplx_ps | 10 | 1.666363 | 1.668732 | +0.002369 | 0.001229 | +1.93 |
| c1e2_exp1.0 | 100 | 1.040652 | 1.042943 | +0.002291 | 0.001555 | +1.47 |
| c1e3_exp1.0 | 1000 | 1.040652 | 1.040651 | −0.000001 | 0.001934 | −0.00 |
| c1e4_exp1.0 | 10000 | 1.040652 | 1.039500 | −0.001152 | 0.002514 | −0.46 |

(SE₃ pooled in quadrature over seeds, `sqrt(Σ sdᵢ²/4e6)/3` — *not* the mean of
the per-seed stds, which understates it by 6–26%.)

The ELBO sits at `H(p)` to within ~2σ at every V. The bound has **no constant
slack** at the optimum, so for `init_test` the amount by which a trained run's
`test_wnelbo_ref` exceeds `H(p)` is entirely model error: 0.5003 / 1.6664 /
1.0407 are achievable targets, not unreachable floors.

**The apparent V-trend in that gap column is not real.** Three checks:

- `test_wloss` at `(lg=pp, rate=0.1)` estimates the *same* estimand — same
  geometry, same exp(0.1) proposal, same targets, only a different RNG salt. Its
  gaps are −0.000433 / +0.001967 / −0.000133 / +0.000448 / **+0.002511**. At
  V = 1000 and V = 10000 the two streams disagree in *sign*.
- Direct numerical integration of the measured profile, `∫L1_pp(t) dt`, gives
  0.5004 / 1.6640 / 1.0391 / 1.0442 / 1.0427 — gaps of +0.0001 / −0.0024 /
  −0.0016 / +0.0035 / +0.0020, signs scattered.
- Even within the reference stream alone, V≤100 vs V≥1000 differ by
  +0.002352 ± 0.001666 (z = 1.41, p = 0.16).

So: no measurable V-dependence. What *does* change with V is the **resolving
power**. SE₃ grows 2.8× from V=10 to V=10000, and at V=10000 it is 2.2× larger
than the gap being tested. The smallest violation detectable at 2σ grows from
0.00179 to 0.00503 nats; restoring the V=10 sensitivity would need ~7.9× more
test samples. **At V=10000 a single reference pass can no longer certify the
`>= H(p)` bound in either direction.**

## 3. Three regimes of the importance-weighted estimator

This supersedes the "infinite variance above rate 0.304" framing in `Agent.md`
and `report.py`. Direct measurement of `L2(t)` shows the second-moment integrand
`L2(t)·e^{λt}` **peaks at a finite `t*` and then collapses** — `L1(t)` decays
faster than any exponential (e.g. naive_ps: 1.6e−3 at t=20, 1.9e−19 at t=99,
4.4e−208 at t=400). The variance is therefore **finite at every rate swept**. It
is not infinity that breaks these cells; it is that the variance is astronomical
and a 4M-sample run never sees it.

The controlling quantity is how many test draws land near `t*`:

```
N(>t*) = 4e6 · e^{−rate · t*}          t* = argmax_t  L2(t)·e^{rate·t}
```

| regime | rate | N(>t*) | reported std ÷ true std | error in the mean |
|---|---|---|---|---|
| **trustworthy** | ≤ 0.1 | 3.3e5 – 4.0e6 | 0.96 – 1.05 | ≤ 0.6% |
| **value ok, error bar wrong** | 0.25 | 1.7e−2 – 0.94 | 4.6 – 24 | ≤ 0.7% |
| **broken** | ≥ 0.5 | ≤ 2.2e−7 | 2.9e3 – 5.9e17 | −0.6% to −52% |

The split is identical in all 10 `(ps, geometry)` combinations: rates
{0.01, 0.05, 0.1} have `N(>t*) > 1`, rates {0.25, 0.5, 0.75, 1.0} do not.

Two consequences worth internalising:

- **`test_wloss_std` is not an error bar above rate 0.1.** At
  `c1e4_exp1.0 / pp / rate 1.0` the run reports std ≈ 488 while the true value is
  4.2e17 — understated by 15 orders of magnitude. Any z-score or confidence
  interval computed from the reported std in that regime is meaningless. (This
  is also why the reported std is itself unstable there, ranging up to 9.5×
  across seeds within one cell.)
- **exp(0.25) is a trap.** It sits below the documented 0.304 threshold and its
  *mean* is still accurate to <1%, so it looks fine — but its error bar is
  understated 5–24×, and that gets worse with V (4.6× at V=10, 15.6× at
  V=10000).

## 4. Above the usable range the estimator biases downward

`test_wloss` drifts monotonically down as the rate crosses out of the trustworthy
regime — **30/30 consecutive decreases** (5 ps × 2 geometries × 3 steps from
0.25 → 0.5 → 0.75 → 1.0).

At rate 1.0 with `lg=pp`, against the independently integrated truth `∫L1 dt`:

| ps | V | measured | true (`∫L1 dt`) | error | vs H(p) |
|---|---|---|---|---|---|
| naive_ps | 10 | 0.4716 | 0.5004 | −5.8% | −0.029 nats |
| cmplx_ps | 10 | 1.6223 | 1.6640 | −2.5% | −0.044 nats |
| c1e2_exp1.0 | 100 | 0.8222 | 1.0391 | −20.9% | −0.218 nats |
| c1e3_exp1.0 | 1000 | 0.6786 | 1.0442 | −35.0% | −0.362 nats |
| c1e4_exp1.0 | 10000 | 0.4961 | 1.0427 | −52.4% | −0.545 nats |

Every one of these is *below* `H(p)` — impossible for a true ELBO, and produced
here by a provably exact model. This is the expected signature of a hugely
right-skewed importance-weighted mean: the sample average sits low because the
draws that carry the mass never occur.

The deficits are ordered with V, but treat that ordering as descriptive: the
increments are not individually resolvable (+0.144 ± 0.087 and +0.183 ± 0.195),
and the SEs they would be tested against are themselves invalid in this regime
(§3). The RNG-independent statement is the "error" column above — the deviation
from the directly integrated truth.

**Actionable rule.** The `test_wnelbo_ref >= H(p)` invariant is diagnostic only
when read off the pinned exp(0.1) reference pass. Read off a `test_wloss` from a
cell at rate ≥ 0.5, it reports a spurious violation of up to 52% of `H(p)` for a
model that is exactly correct. Raising `test_size` does not fix this — reaching
`N(>t*) ≈ 1` at rate 1.0 would take e^{61} samples. Lowering the rate does.

## 5. At constant entropy, the ELBO is V-invariant and the weighted CE is not

Across `c1e2` / `c1e3` / `c1e4` — bit-identical distributions, V = 100 / 1000 / 10000:

| metric | V=100 | V=1000 | V=10000 | verdict |
|---|---|---|---|---|
| `wnelbo_ref` | 1.042943 | 1.040651 | 1.039500 | **invariant** (Δ = 3.44e−3 ± 2.96e−3, z=1.16) |
| `wce_ref` | 9.5427 | 14.3231 | 19.1178 | **+4.79 per decade of V** |
| `nelbo_ref` | 0.048786 | 0.032985 | 0.022234 | −54.4% |
| `ce_ref` | 0.553219 | 0.711526 | 0.818693 | +48.0% |
| `wnelbo_ref_std` | 5.378 | 6.700 | 8.705 | +61.9%, ≈ V^0.105 |

The weighted CE follows a strikingly clean law:

```
wce_ref = 2.0792 · ln V − 0.035          R² = 0.999999
```

and the fitted slope is within **1.1σ of 2·H(p) = 2.0813**. Tempting, but the
support is one family: `V=10` does **not** lie on this line (naive_ps −48.6%,
cmplx_ps +43.6%, straddling it at >40 analytic SE), and normalising by entropy
does not rescue it. Treat `slope ≈ 2H(p)` as a conjecture worth one targeted test
(a second `lam`, or `c1e5_exp1.0`), not as an established law.

The mechanism is measured, not assumed: **the ELBO integrand moves to later `t`
as V grows.** The mass-median of `∫L1_pp(t) dt` — the time by which half the ELBO
has accumulated — is 3.5 / 2.8 (V=10) → 7.5 → 12.1 → 16.6. Finer angular packing
(`φ_v` spaced `2π/V` apart) means the bridge must travel further before the
target is resolved. That single fact explains the rest of the table: under the
*fixed* exp(0.1) reference proposal, integrand mass at larger `t` is suppressed by
`e^{−0.1t}`, so the unweighted `nelbo_ref` falls while the weighted `wnelbo_ref`
— which divides that suppression back out — stays put.

**So `wce_ref` cannot compare models across vocabulary sizes**, and neither can
`nelbo_ref` or `ce_ref`: all three move by 48–100% across settings where the
quantity being modelled is bit-identical and the achievable ELBO is unchanged.
Only `wnelbo_ref` is comparable. (`nelbo_ref` and `ce_ref` are `E_q[bridge]`
under `q`, not estimators of any `t`-integral — see `loss.py:278`,
`main.py:166,175`.)

## 6. What to change

1. **`report.py`'s `VARIANCE_CLIFF = 0.304` is the wrong boundary.** It flags
   0.5/0.75/1.0 but passes 0.25, which has a 5–24× understated error bar. The
   measured boundary is between 0.1 and 0.25 at every V. Either lower the
   threshold to ~0.15, or better, use two tiers: `!` for "error bar invalid"
   (> 0.1) and `!!` for "value invalid" (≥ 0.5).
2. **Stop describing the failure as infinite variance.** It is finite but
   unreachable; the useful criterion is `N(>t*) = 4e6·e^{−rate·t*} ≫ 1`, which
   also correctly predicts that the boundary is V-dependent in `t*` (t* = 61 at
   V=10, 93 at V=10000) even though it lands in the same grid gap.
3. **Consider `ref_proposal_exp_rate = 0.05` for large-V work.** The pinned
   exp(0.1) is variance-optimal only at V=10; it costs +6.4% / +23.7% / +49.3%
   in std at V = 100 / 1000 / 10000 (the last ≈ 2.2× more samples for the same
   precision). Changing it breaks comparability with every existing run, so this
   is a decision for the next project, not a retrofit.
4. **`H(p)` for the `c1e*_exp1.0` family is now in `report.py`'s `ENTROPY` map**
   (1.040652 for all of them, including the unswept `c1e5_exp1.0`).
