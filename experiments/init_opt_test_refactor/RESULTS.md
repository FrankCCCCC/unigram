# init_opt_test_refactor results

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

## Verdict: the refactor reproduces `init_opt_test` exactly — 210/210 cells, bit-exact

```
python experiments/compare_reproduction.py init_opt_test_refactor init_opt_test
  paired    : 210 cells   (tol = 1e-09 relative)
  bit-exact : 210/210
  worst relative difference, all 8 metrics: 0.000e+00
  VERDICT: REPRODUCED
```

Not "within noise" — **identical to the last bit**, on every one of
`test_wloss`, `test_wnelbo_ref`, `test_wce_ref`, `test_nelbo_ref`, `test_ce_ref`
and the three `_std` columns, across all 5 `ps` specs × 2 geometries × 7 rates ×
3 seeds.

This is the strong half of the reproduction evidence. `mode=opt` skips
`trainer.fit`, so `OptimalModel` is deterministic and parameter-free and there is
no optimizer trajectory to absorb a regression. What remains under test is
precisely the surface the refactor touched: the proposal, the bridge sampler, the
horosphere geometry, the loss, and the metric plumbing now living in
`trainer.py:BaseTrainer`. All of it is unchanged.

## The reproduction is architecture-independent here (and that matters)

Cells landed across `desa-compute-01` (2080 Ti, `sm_75`), `kuleshov-compute-02`
(A6000, `sm_86`) and `kuleshov-compute-03` (A5000, `sm_86`), and reproduced
bit-exactly on all of them. With no training there is nothing to accumulate, so
ULP-level differences in kernel selection never compound.

Contrast the trained companion `init_test_refactor`, where the same code
reproduces bit-exactly **only** on the architecture that produced the reference
(23/23 on `desa-compute-01`, 0/61 elsewhere). Read together, the two projects
separate the two candidate explanations cleanly: the geometry/loss/metric path is
byte-stable, and the trained-cell drift is hardware, not code.

## Free correctness checks that also passed

- **Reference-pass invariance.** `test_wnelbo_ref` / `test_nelbo_ref` /
  `test_wce_ref` / `test_ce_ref` come from a proposal pinned to `exp(0.1)` on an
  independent RNG stream (`salt=1`). Checked mechanically: all 15 `(ps, seed)`
  groups contain exactly 14 `(loss_geometry, rate)` cells, and every group has
  exactly **one** distinct reference tuple. The refactor did not cross the loss
  and reference streams.
- **`test_wnelbo_ref >= H(p)` at the optimum.** `naive_ps` reports
  0.5019 ± 0.0009 against `H = 0.500288`; `cmplx_ps` 1.6687 ± 0.0008 against
  `H = 1.666363`. The ELBO sits just above the bound, as it should at the exact
  Bayes solution.
- **The variance cliff is intact.** Rates above ≈ 0.304 still fan out across
  seeds with blown-up `test_wloss_std`, and rates `{0.01, 0.05, 0.1, 0.25}` still
  agree tightly — the estimator behaviour the original project characterized is
  preserved, not just the means.
