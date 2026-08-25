# init_refactor_16d results

- runs collected: **36** / 126 (29%) — run dirs without test_metrics.json: 26
- H(naive_ps) = **0.5003** — wnelbo_ref is bounded below by this
- `!` marks loss proposals above the ~0.304 variance cliff, where the
  weighted estimator has infinite variance. The reference pass is pinned at
  exp(0.1) and stays valid, but training there is materially noisier.
- `wce_ref` is dominated by rare extremes; treat its spread as indicative only.

---

# Results (Full Table)

---

## naive_ps, Training Step 20000

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.0121 (n=1) | 0.5268 (n=1) | 0.0092 (n=1) | 0.0512 (n=1) | 0.0009 (n=1) |
| exp0.05 | 0.0094 (n=1) | 0.5189 (n=1) | 0.0089 (n=1) | 0.0506 (n=1) | 0.0009 (n=1) |
| exp0.1 | 0.0089 (n=1) | 0.5238 (n=1) | 0.0089 (n=1) | 0.0513 (n=1) | 0.0009 (n=1) |
| exp0.25 | 0.0085 (n=1) | 0.5237 (n=1) | 0.0088 (n=1) | 0.0512 (n=1) | 0.0009 (n=1) |
| exp0.5 ! | 0.0084 (n=1) | 0.5181 (n=1) | 0.0087 (n=1) | 0.0506 (n=1) | 0.0009 (n=1) |
| exp0.75 ! | 0.0083 (n=1) | 0.5126 (n=1) | 0.0086 (n=1) | 0.0500 (n=1) | 0.0008 (n=1) |
| exp1.0 ! | 0.0083 (n=1) | 0.5149 (n=1) | 0.0086 (n=1) | 0.0503 (n=1) | 0.0008 (n=1) |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.6459 (n=1) | 0.6185 (n=1) | 0.3261 (n=1) | 0.0590 (n=1) | 0.0318 (n=1) |
| exp0.05 | 0.5167 (n=1) | 0.5066 (n=1) | 0.2143 (n=1) | 0.0484 (n=1) | 0.0209 (n=1) |
| exp0.1 | 0.4912 (n=1) | 0.4969 (n=1) | 0.1751 (n=1) | 0.0479 (n=1) | 0.0171 (n=1) |
| exp0.25 | 0.5074 (n=1) | 0.5147 (n=1) | 0.1201 (n=1) | 0.0499 (n=1) | 0.0117 (n=1) |
| exp0.5 ! | 0.5016 (n=1) | 0.5087 (n=1) | 0.0818 (n=1) | 0.0498 (n=1) | 0.0080 (n=1) |
| exp0.75 ! | 0.5030 (n=1) | 0.5247 (n=1) | 0.0704 (n=1) | 0.0514 (n=1) | 0.0069 (n=1) |
| exp1.0 ! | 0.4991 (n=1) | 0.5072 (n=1) | 0.0986 (n=1) | 0.0496 (n=1) | 0.0097 (n=1) |

---

## naive_ps, Training Step 40000

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.0105 (n=1) | 0.5966 (n=1) | 0.0106 (n=1) | 0.0565 (n=1) | 0.0010 (n=1) |
| exp0.05 | 0.0090 (n=1) | 0.5622 (n=1) | 0.0097 (n=1) | 0.0529 (n=1) | 0.0009 (n=1) |
| exp0.1 | 0.0089 (n=1) | 0.5626 (n=1) | 0.0096 (n=1) | 0.0532 (n=1) | 0.0009 (n=1) |
| exp0.25 | 0.0087 (n=1) | 0.5596 (n=1) | 0.0095 (n=1) | 0.0530 (n=1) | 0.0009 (n=1) |
| exp0.5 ! | 0.0085 (n=1) | 0.5527 (n=1) | 0.0093 (n=1) | 0.0525 (n=1) | 0.0009 (n=1) |
| exp0.75 ! | 0.0084 (n=1) | 0.5418 (n=1) | 0.0092 (n=1) | 0.0521 (n=1) | 0.0009 (n=1) |
| exp1.0 ! | 0.0084 (n=1) | 0.5536 (n=1) | 0.0093 (n=1) | 0.0525 (n=1) | 0.0009 (n=1) |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.8003 (n=1) | 0.6674 (n=1) | 0.3090 (n=1) | 0.0634 (n=1) | 0.0298 (n=1) |
| exp0.05 | 0.5394 (n=1) | 0.5312 (n=1) | 0.2653 (n=1) | 0.0504 (n=1) | 0.0257 (n=1) |
| exp0.1 | 0.5045 (n=1) | 0.5479 (n=1) | 0.1966 (n=1) | 0.0487 (n=1) | 0.0189 (n=1) |
| exp0.25 | 0.5038 (n=1) | 0.5105 (n=1) | 0.1896 (n=1) | 0.0489 (n=1) | 0.0184 (n=1) |
| exp0.5 ! | 0.4965 (n=1) | 0.5074 (n=1) | 0.1172 (n=1) | 0.0492 (n=1) | 0.0114 (n=1) |
| exp0.75 ! | 0.5002 (n=1) | 0.4968 (n=1) | 0.1115 (n=1) | 0.0484 (n=1) | 0.0109 (n=1) |
| exp1.0 ! | - | - | - | - | - |

---

## naive_ps, Training Step 100000

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.0126 (n=1) | 0.4916 (n=1) | 0.0086 (n=1) | 0.0488 (n=1) | 0.0009 (n=1) |
| exp0.05 | 0.0088 (n=1) | 0.4949 (n=1) | 0.0084 (n=1) | 0.0492 (n=1) | 0.0008 (n=1) |
| exp0.1 | 0.0087 (n=1) | 0.4879 (n=1) | 0.0084 (n=1) | 0.0484 (n=1) | 0.0008 (n=1) |
| exp0.25 | 0.0087 (n=1) | 0.5000 (n=1) | 0.0084 (n=1) | 0.0491 (n=1) | 0.0008 (n=1) |
| exp0.5 ! | 0.0084 (n=1) | 0.4859 (n=1) | 0.0083 (n=1) | 0.0482 (n=1) | 0.0008 (n=1) |
| exp0.75 ! | 0.0085 (n=1) | 0.4958 (n=1) | 0.0084 (n=1) | 0.0492 (n=1) | 0.0008 (n=1) |
| exp1.0 ! | - | - | - | - | - |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.7528 (n=1) | 0.6748 (n=1) | 0.3449 (n=1) | 0.0636 (n=1) | 0.0331 (n=1) |
| exp0.05 | 0.5155 (n=1) | 0.5153 (n=1) | 0.2568 (n=1) | 0.0489 (n=1) | 0.0248 (n=1) |
| exp0.1 | 0.5321 (n=1) | 0.4976 (n=1) | 0.2283 (n=1) | 0.0474 (n=1) | 0.0221 (n=1) |
| exp0.25 | - | - | - | - | - |
| exp0.5 ! | - | - | - | - | - |
| exp0.75 ! | - | - | - | - | - |
| exp1.0 ! | - | - | - | - | - |

---

# RESULTS (Dense Table)

---

## naive_ps, Training Step 20000

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 0.6459 (n=1) | 0.0121 (n=1) |
| exp0.05 | 0.5167 (n=1) | 0.0094 (n=1) |
| exp0.1 | 0.4912 (n=1) | 0.0089 (n=1) |
| exp0.25 | 0.5074 (n=1) | 0.0085 (n=1) |
| exp0.5 ! | 0.5016 (n=1) | 0.0084 (n=1) |
| exp0.75 ! | 0.5030 (n=1) | 0.0083 (n=1) |
| exp1.0 ! | 0.4991 (n=1) | 0.0083 (n=1) |

---

## naive_ps, Training Step 40000

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 0.8003 (n=1) | 0.0105 (n=1) |
| exp0.05 | 0.5394 (n=1) | 0.0090 (n=1) |
| exp0.1 | 0.5045 (n=1) | 0.0089 (n=1) |
| exp0.25 | 0.5038 (n=1) | 0.0087 (n=1) |
| exp0.5 ! | 0.4965 (n=1) | 0.0085 (n=1) |
| exp0.75 ! | 0.5002 (n=1) | 0.0084 (n=1) |
| exp1.0 ! | - | 0.0084 (n=1) |

---

## naive_ps, Training Step 100000

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 0.7528 (n=1) | 0.0126 (n=1) |
| exp0.05 | 0.5155 (n=1) | 0.0088 (n=1) |
| exp0.1 | 0.5321 (n=1) | 0.0087 (n=1) |
| exp0.25 | - | 0.0087 (n=1) |
| exp0.5 ! | - | 0.0084 (n=1) |
| exp0.75 ! | - | 0.0085 (n=1) |
| exp1.0 ! | - | - |

