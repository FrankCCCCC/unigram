# init_opt_test_3d_refactor_new results

- runs collected: **2268** / 2268 (100%) — run dirs without test_metrics.json: 0
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
  stratified_exp(0.1) and stays valid, but training there is materially noisier.
- `wce_ref` is dominated by rare extremes; treat its spread as indicative only.

---

# Results (Full Table)

---

## naive_ps, K = -0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 62.7888 / 3.817e+05 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.05 | 53.2156 / 1.713e+07 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.1 | 41.7589 / 3.864e+07 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.25 | 23.3729 / 1.708e+07 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.5 ! | 13.3282 / 6.992e+06 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.75 ! | 9.2604 / 3.607e+06 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp1.0 ! | 7.0767 / 2.132e+06 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4973 / 17.14 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.05 | 0.4423 / 3964 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.1 | 0.3552 / 7828 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.25 | 0.1925 / 3064 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.5 ! | 0.1045 / 868.8 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.75 ! | 0.0707 / 379.5 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp1.0 ! | 0.0532 / 205.3 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 21.7140 / 1.265e+06 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.05 | 15.5261 / 7.707e+06 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.1 | 9.7688 / 7.213e+06 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.25 | 3.4393 / 1.087e+06 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.5 ! | 1.4325 / 1.816e+05 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp0.75 ! | 0.8416 / 6.145e+04 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |
| stratified_exp1.0 ! | 0.5785 / 2.768e+04 | 2.3074 / 4.251e+07 | 138.8867 / 9.438e+10 | 0.0035 / n/r | 0.4653 / n/r |

---

## naive_ps, K = -0.05

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 12.6027 / 5112 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.05 | 12.5578 / 1.527e+04 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.1 | 12.3952 / 4.504e+05 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.25 | 10.6431 / 6.85e+05 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.5 ! | 8.3518 / 1.545e+06 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.75 ! | 6.5746 / 1.035e+06 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp1.0 ! | 5.4746 / 8.349e+05 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.5000 / 10.72 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.05 | 0.4973 / 17.14 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.1 | 0.4893 / 378.3 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.25 | 0.4423 / 3964 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.5 ! | 0.3552 / 7828 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.75 ! | 0.2765 / 4880 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp1.0 ! | 0.2287 / 3997 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 22.2116 / 9.545e+05 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.05 | 21.7140 / 1.265e+06 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.1 | 21.4016 / 9.738e+06 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.25 | 15.5261 / 7.707e+06 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.5 ! | 9.7688 / 7.213e+06 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp0.75 ! | 6.3556 / 3.302e+06 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |
| stratified_exp1.0 ! | 4.5865 / 1.976e+06 | 0.4960 / 1231 | 12.6220 / 6.946e+05 | 0.0141 / n/r | 0.3590 / n/r |

---

## naive_ps, K = -0.1

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 6.2885 / 2199 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.05 | 6.3061 / 1161 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.1 | 6.2789 / 3817 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.25 | 6.0090 / 5.163e+04 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.5 ! | 5.3216 / 1.713e+05 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.75 ! | 4.7544 / 4.064e+05 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp1.0 ! | 4.1759 / 3.864e+05 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4995 / 18.67 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.05 | 0.5006 / 7.966 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.1 | 0.4973 / 17.14 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.25 | 0.4764 / 279.5 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.5 ! | 0.4423 / 3964 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.75 ! | 0.4051 / 9167 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp1.0 ! | 0.3552 / 7828 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 22.3576 / 1.205e+06 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.05 | 22.6735 / 1.152e+06 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.1 | 21.7140 / 1.265e+06 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.25 | 19.9900 / 9.536e+06 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.5 ! | 15.5261 / 7.707e+06 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp0.75 ! | 11.9737 / 5.466e+06 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |
| stratified_exp1.0 ! | 9.7688 / 7.213e+06 | 0.5004 / 35.58 | 6.3088 / 9746 | 0.0222 / n/r | 0.2785 / n/r |

---

## naive_ps, K = -0.5

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.2550 / 402.5 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.05 | 1.2577 / 87.96 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.1 | 1.2603 / 51.12 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.25 | 1.2612 / 46.45 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.5 ! | 1.2558 / 152.7 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.75 ! | 1.2461 / 524.5 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp1.0 ! | 1.2395 / 4504 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4963 / 85.27 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.05 | 0.4995 / 18.67 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.1 | 0.5000 / 10.72 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.25 | 0.5006 / 7.966 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.5 ! | 0.4973 / 17.14 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.75 ! | 0.4956 / 155.9 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp1.0 ! | 0.4893 / 378.3 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 22.1982 / 2.46e+06 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.05 | 22.3576 / 1.205e+06 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.1 | 22.2116 / 9.545e+05 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.25 | 22.6735 / 1.152e+06 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.5 ! | 21.7140 / 1.265e+06 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp0.75 ! | 20.6408 / 1.019e+06 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |
| stratified_exp1.0 ! | 21.4016 / 9.738e+06 | 0.5001 / 10.71 | 1.2591 / 51.34 | 0.0400 / n/r | 0.1001 / n/r |

---

## naive_ps, K = -1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.6283 / 199.6 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.05 | 0.6296 / 41.63 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.1 | 0.6288 / 21.99 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.25 | 0.6307 / 11.15 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.5 ! | 0.6306 / 11.61 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.75 ! | 0.6291 / 19.94 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp1.0 ! | 0.6279 / 38.17 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4989 / 171.1 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.05 | 0.4997 / 35.47 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.1 | 0.4995 / 18.67 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.25 | 0.5007 / 9.256 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.5 ! | 0.5006 / 7.966 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.75 ! | 0.4990 / 10.97 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp1.0 ! | 0.4973 / 17.14 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 22.7782 / 1.137e+07 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.05 | 22.8115 / 6.573e+06 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.1 | 22.3576 / 1.205e+06 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.25 | 23.4007 / 6.299e+06 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.5 ! | 22.6735 / 1.152e+06 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp0.75 ! | 21.9860 / 8.815e+05 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |
| stratified_exp1.0 ! | 21.7140 / 1.265e+06 | 0.4990 / 18.69 | 0.6287 / 21.99 | 0.0443 / n/r | 0.0557 / n/r |

---

## naive_ps, K = -2.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.3127 / 98.18 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.05 | 0.3140 / 20.25 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.1 | 0.3148 / 10.41 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.25 | 0.3144 / 4.54 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.5 ! | 0.3153 / 2.788 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.75 ! | 0.3156 / 2.895 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp1.0 ! | 0.3153 / 2.903 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4963 / 337.5 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.05 | 0.4978 / 68.83 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.1 | 0.4997 / 35.47 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.25 | 0.4988 / 15.4 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.5 ! | 0.5007 / 9.256 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.75 ! | 0.5004 / 8.167 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp1.0 ! | 0.5006 / 7.966 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 21.0686 / 3.681e+06 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.05 | 22.6924 / 3.244e+06 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.1 | 22.8115 / 6.573e+06 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.25 | 22.1281 / 8.269e+05 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.5 ! | 23.4007 / 6.299e+06 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp0.75 ! | 22.7801 / 2.103e+06 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |
| stratified_exp1.0 ! | 22.6735 / 1.152e+06 | 0.4997 / 35.31 | 0.3141 / 10.34 | 0.0470 / n/r | 0.0295 / n/r |

---

## naive_ps, K = -3.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.2086 / 65.99 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.05 | 0.2092 / 13.39 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.1 | 0.2094 / 6.804 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.25 | 0.2097 / 2.882 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.5 ! | 0.2098 / 1.613 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.75 ! | 0.2102 / 1.239 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp1.0 ! | 0.2105 / 1.164 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4973 / 512.4 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.05 | 0.4971 / 102.5 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.1 | 0.4988 / 52.14 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.25 | 0.4998 / 22.01 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.5 ! | 0.4992 / 12.21 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.75 ! | 0.5007 / 9.256 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp1.0 ! | 0.5011 / 8.129 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 22.5488 / 2.066e+07 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.05 | 25.5240 / 1.216e+08 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.1 | 22.9247 / 5.152e+06 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.25 | 22.8530 / 1.911e+06 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.5 ! | 22.6523 / 1.068e+06 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp0.75 ! | 23.4007 / 6.299e+06 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |
| stratified_exp1.0 ! | 22.6351 / 9.671e+05 | 0.4987 / 51.97 | 0.2093 / 6.761 | 0.0479 / n/r | 0.0201 / n/r |

---

## naive_ps, K = -4.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.1566 / 49.76 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.05 | 0.1572 / 10.04 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.1 | 0.1570 / 5.063 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.25 | 0.1574 / 2.113 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.5 ! | 0.1572 / 1.135 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.75 ! | 0.1575 / 0.8339 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp1.0 ! | 0.1577 / 0.697 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4988 / 688.9 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.05 | 0.4998 / 137.2 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.1 | 0.4978 / 68.83 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.25 | 0.4998 / 28.75 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.5 ! | 0.4988 / 15.4 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.75 ! | 0.4997 / 11.21 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp1.0 ! | 0.5007 / 9.256 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 20.8536 / 4.739e+06 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.05 | 23.1551 / 4.816e+06 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.1 | 22.6924 / 3.244e+06 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.25 | 22.8382 / 1.87e+06 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.5 ! | 22.1281 / 8.269e+05 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp0.75 ! | 22.2724 / 8.902e+05 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |
| stratified_exp1.0 ! | 23.4007 / 6.299e+06 | 0.5000 / 69.06 | 0.1571 / 5.027 | 0.0485 / n/r | 0.0152 / n/r |

---

## naive_ps, K = -10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.0636 / 20.05 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.05 | 0.0625 / 3.927 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.1 | 0.0628 / 1.996 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.25 | 0.0628 / 0.8101 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.5 ! | 0.0630 / 0.4163 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.75 ! | 0.0629 / 0.2853 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp1.0 ! | 0.0629 / 0.2199 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.5019 / 1710 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.05 | 0.4963 / 337.5 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.1 | 0.4989 / 171.1 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.25 | 0.4978 / 68.83 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.5 ! | 0.4997 / 35.47 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.75 ! | 0.4996 / 24.22 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp1.0 ! | 0.4995 / 18.67 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 21.9570 / 1.778e+07 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.05 | 21.0686 / 3.681e+06 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.1 | 22.7782 / 1.137e+07 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.25 | 22.6924 / 3.244e+06 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.5 ! | 22.8115 / 6.573e+06 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp0.75 ! | 22.1099 / 7.494e+05 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |
| stratified_exp1.0 ! | 22.3576 / 1.205e+06 | 0.5061 / 174 | 0.0633 / 2.011 | 0.0500 / n/r | 0.0063 / n/r |

---

## cmplx_ps, K = -0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 209.4920 / 1.672e+06 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.05 | 184.9835 / 1.381e+08 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.1 | 144.2413 / 1.494e+08 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.25 | 85.1294 / 2.54e+08 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.5 ! | 48.6255 / 9.698e+07 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.75 ! | 33.7021 / 4.566e+07 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp1.0 ! | 25.7289 / 2.579e+07 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6649 / 115.3 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.05 | 1.4645 / 8793 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.1 | 1.1534 / 1.043e+04 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.25 | 0.6450 / 1.169e+04 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.5 ! | 0.3478 / 4111 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.75 ! | 0.2321 / 1604 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp1.0 ! | 0.1734 / 799.1 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 69.1916 / 9.352e+06 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.05 | 49.9948 / 5.068e+07 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.1 | 31.1043 / 2.23e+07 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.25 | 12.1792 / 6.874e+06 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.5 ! | 5.2253 / 1.74e+06 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp0.75 ! | 3.1126 / 8.788e+05 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |
| stratified_exp1.0 ! | 2.1383 / 4.36e+05 | 4.4108 / 6.629e+07 | 389.8795 / 4.765e+11 | 0.0110 / n/r | 1.5563 / n/r |

---

## cmplx_ps, K = -0.05

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 41.9330 / 1.082e+04 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.05 | 41.8984 / 6.69e+04 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.1 | 41.7490 / 2.34e+06 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.25 | 36.9967 / 5.522e+06 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.5 ! | 28.8483 / 5.976e+06 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.75 ! | 23.6920 / 9.061e+06 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp1.0 ! | 19.8960 / 1.118e+07 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6661 / 23.51 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.05 | 1.6649 / 115.3 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.1 | 1.6547 / 2674 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.25 | 1.4645 / 8793 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.5 ! | 1.1534 / 1.043e+04 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.75 ! | 0.9332 / 1.188e+04 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp1.0 ! | 0.7721 / 1.405e+04 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 70.1570 / 8.602e+06 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.05 | 69.1916 / 9.352e+06 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.1 | 65.7711 / 5.927e+07 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.25 | 49.9948 / 5.068e+07 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.5 ! | 31.1043 / 2.23e+07 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp0.75 ! | 21.8270 / 1.472e+07 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |
| stratified_exp1.0 ! | 16.0944 / 1.069e+07 | 1.6536 / 1926 | 42.0887 / 4.186e+06 | 0.0464 / n/r | 1.2013 / n/r |

---

## cmplx_ps, K = -0.1

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 20.9654 / 4841 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.05 | 20.9748 / 2465 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.1 | 20.9492 / 1.672e+04 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.25 | 20.7611 / 1.196e+06 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.5 ! | 18.4983 / 1.381e+06 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.75 ! | 16.2710 / 1.869e+06 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp1.0 ! | 14.4241 / 1.494e+06 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6666 / 41.76 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.05 | 1.6670 / 19.58 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.1 | 1.6649 / 115.3 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.25 | 1.6626 / 1.513e+04 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.5 ! | 1.4645 / 8793 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.75 ! | 1.3189 / 1.817e+04 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp1.0 ! | 1.1534 / 1.043e+04 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 69.1093 / 5.061e+06 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.05 | 69.2097 / 2.235e+06 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.1 | 69.1916 / 9.352e+06 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.25 | 67.6199 / 1.99e+08 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.5 ! | 49.9948 / 5.068e+07 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp0.75 ! | 39.8449 / 8.163e+07 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |
| stratified_exp1.0 ! | 31.1043 / 2.23e+07 | 1.6638 / 84.32 | 20.9806 / 1.795e+04 | 0.0735 / n/r | 0.9307 / n/r |

---

## cmplx_ps, K = -0.5

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 4.1918 / 921 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.05 | 4.1931 / 193.6 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.1 | 4.1933 / 108.2 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.25 | 4.1950 / 98.59 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.5 ! | 4.1898 / 669 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.75 ! | 4.1864 / 6617 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp1.0 ! | 4.1749 / 2.34e+04 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6637 / 195.2 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.05 | 1.6666 / 41.76 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.1 | 1.6661 / 23.51 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.25 | 1.6670 / 19.58 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.5 ! | 1.6649 / 115.3 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.75 ! | 1.6568 / 341.8 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp1.0 ! | 1.6547 / 2674 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 70.7488 / 3.584e+07 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.05 | 69.1093 / 5.061e+06 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.1 | 70.1570 / 8.602e+06 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.25 | 69.2097 / 2.235e+06 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.5 ! | 69.1916 / 9.352e+06 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp0.75 ! | 69.0296 / 5.12e+07 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |
| stratified_exp1.0 ! | 65.7711 / 5.927e+07 | 1.6676 / 23.61 | 4.1934 / 108.5 | 0.1333 / n/r | 0.3339 / n/r |

---

## cmplx_ps, K = -1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 2.1021 / 461.6 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.05 | 2.0980 / 93.76 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.1 | 2.0965 / 48.41 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.25 | 2.0983 / 23.63 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.5 ! | 2.0975 / 24.65 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.75 ! | 2.0974 / 68.4 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp1.0 ! | 2.0949 / 167.2 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6710 / 391.7 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.05 | 1.6675 / 80.12 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.1 | 1.6666 / 41.76 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.25 | 1.6682 / 20.52 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.5 ! | 1.6670 / 19.58 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.75 ! | 1.6678 / 54.1 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp1.0 ! | 1.6649 / 115.3 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 70.5053 / 2.041e+07 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.05 | 68.2121 / 2.215e+06 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.1 | 69.1093 / 5.061e+06 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.25 | 70.4583 / 8.625e+06 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.5 ! | 69.2097 / 2.235e+06 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp0.75 ! | 71.0838 / 2.507e+07 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |
| stratified_exp1.0 ! | 69.1916 / 9.352e+06 | 1.6657 / 41.68 | 2.0964 / 48.48 | 0.1480 / n/r | 0.1857 / n/r |

---

## cmplx_ps, K = -2.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0504 / 229.1 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.05 | 1.0479 / 46.15 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.1 | 1.0490 / 23.44 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.25 | 1.0479 / 9.881 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.5 ! | 1.0492 / 5.907 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.75 ! | 1.0493 / 5.533 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp1.0 ! | 1.0487 / 6.162 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6737 / 778.5 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.05 | 1.6616 / 155.9 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.1 | 1.6675 / 80.12 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.25 | 1.6657 / 34.19 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.5 ! | 1.6682 / 20.52 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.75 ! | 1.6675 / 18.16 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp1.0 ! | 1.6670 / 19.58 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 68.1313 / 1.587e+07 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.05 | 69.4300 / 8.385e+06 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.1 | 68.2121 / 2.215e+06 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.25 | 69.5778 / 2.846e+06 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.5 ! | 70.4583 / 8.625e+06 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp0.75 ! | 69.8615 / 4.203e+06 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |
| stratified_exp1.0 ! | 69.2097 / 2.235e+06 | 1.6630 / 79.47 | 1.0475 / 23.34 | 0.1565 / n/r | 0.0984 / n/r |

---

## cmplx_ps, K = -3.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.6996 / 153.1 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.05 | 0.6988 / 30.67 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.1 | 0.6989 / 15.48 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.25 | 0.6992 / 6.385 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.5 ! | 0.6989 / 3.455 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.75 ! | 0.6994 / 2.625 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp1.0 ! | 0.6995 / 2.338 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6728 / 1168 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.05 | 1.6634 / 233.4 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.1 | 1.6641 / 118.2 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.25 | 1.6684 / 49.49 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.5 ! | 1.6656 / 26.94 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.75 ! | 1.6682 / 20.52 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp1.0 ! | 1.6677 / 18.03 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 73.3296 / 8.53e+07 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.05 | 69.3045 / 9.023e+06 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.1 | 71.4171 / 1.292e+07 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.25 | 70.0327 / 6.142e+06 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.5 ! | 70.2618 / 3.539e+06 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp0.75 ! | 70.4583 / 8.625e+06 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |
| stratified_exp1.0 ! | 69.5264 / 2.802e+06 | 1.6641 / 118.2 | 0.6985 / 15.41 | 0.1597 / n/r | 0.0670 / n/r |

---

## cmplx_ps, K = -4.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.5228 / 114.4 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.05 | 0.5244 / 23 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.1 | 0.5239 / 11.54 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.25 | 0.5246 / 4.725 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.5 ! | 0.5240 / 2.47 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.75 ! | 0.5242 / 1.773 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp1.0 ! | 0.5246 / 1.477 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6661 / 1545 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.05 | 1.6636 / 309.8 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.1 | 1.6616 / 155.9 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.25 | 1.6684 / 64.78 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.5 ! | 1.6657 / 34.19 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.75 ! | 1.6658 / 24.6 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp1.0 ! | 1.6682 / 20.52 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 69.7294 / 9.02e+07 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.05 | 76.9830 / 5.278e+08 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.1 | 69.4300 / 8.385e+06 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.25 | 73.8629 / 2.365e+08 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.5 ! | 69.5778 / 2.846e+06 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp0.75 ! | 70.1135 / 3.535e+06 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |
| stratified_exp1.0 ! | 70.4583 / 8.625e+06 | 1.6674 / 156.9 | 0.5248 / 11.55 | 0.1617 / n/r | 0.0508 / n/r |

---

## cmplx_ps, K = -10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.2097 / 45.96 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.05 | 0.2101 / 9.165 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.1 | 0.2102 / 4.616 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.25 | 0.2096 / 1.846 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.5 ! | 0.2098 / 0.9376 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.75 ! | 0.2099 / 0.636 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp1.0 ! | 0.2097 / 0.4841 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6768 / 3939 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.05 | 1.6737 / 778.5 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.1 | 1.6710 / 391.7 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.25 | 1.6616 / 155.9 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.5 ! | 1.6675 / 80.12 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.75 ! | 1.6688 / 54.55 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp1.0 ! | 1.6666 / 41.76 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 70.2778 / 8.672e+07 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.05 | 68.1313 / 1.587e+07 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.1 | 70.5053 / 2.041e+07 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.25 | 69.4300 / 8.385e+06 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.5 ! | 68.2121 / 2.215e+06 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp0.75 ! | 70.6089 / 6.634e+06 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |
| stratified_exp1.0 ! | 69.1093 / 5.061e+06 | 1.6691 / 390.9 | 0.2105 / 4.626 | 0.1648 / n/r | 0.0208 / n/r |

---

## c1e3_exp1.0, K = -0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 115.1584 / 1.559e+06 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.05 | 100.9162 / 5.77e+07 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.1 | 78.8965 / 4.674e+07 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.25 | 47.2069 / 5.547e+07 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.5 ! | 27.5820 / 2.653e+07 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.75 ! | 19.4163 / 1.37e+07 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp1.0 ! | 14.9542 / 7.852e+06 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0461 / 724.8 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.05 | 0.9232 / 2224 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.1 | 0.7650 / 6059 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.25 | 0.4638 / 5122 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.5 ! | 0.2702 / 2224 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.75 ! | 0.1915 / 1423 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp1.0 ! | 0.1478 / 861.9 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 151.9184 / 5.463e+07 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.05 | 85.1992 / 1.753e+08 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.1 | 41.9377 / 9.729e+07 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.25 | 12.4862 / 2.625e+07 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.5 ! | 4.2794 / 2.464e+06 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.75 ! | 2.3311 / 5.959e+05 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp1.0 ! | 1.5354 / 2.081e+05 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |

---

## c1e3_exp1.0, K = -0.05

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 23.0095 / 6300 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.05 | 23.0317 / 6.238e+04 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.1 | 22.7144 / 3.916e+05 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.25 | 20.1832 / 2.308e+06 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.5 ! | 15.7793 / 1.87e+06 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.75 ! | 12.9840 / 2.542e+06 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp1.0 ! | 10.9744 / 2.578e+06 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0404 / 16.32 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.05 | 1.0461 / 724.8 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.1 | 1.0256 / 632.5 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.25 | 0.9232 / 2224 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.5 ! | 0.7650 / 6059 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.75 ! | 0.6387 / 7904 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp1.0 ! | 0.5408 / 6602 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 158.0541 / 2.209e+07 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.05 | 151.9184 / 5.463e+07 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.1 | 157.1028 / 2.352e+09 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.25 | 85.1992 / 1.753e+08 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.5 ! | 41.9377 / 9.729e+07 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.75 ! | 26.7737 / 1.092e+08 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp1.0 ! | 17.6712 / 5.386e+07 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |

---

## c1e3_exp1.0, K = -0.1

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 11.5034 / 2750 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.05 | 11.5181 / 1386 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.1 | 11.5158 / 1.559e+04 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.25 | 11.3209 / 3.468e+05 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.5 ! | 10.0916 / 5.77e+05 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.75 ! | 8.8539 / 4.199e+05 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp1.0 ! | 7.8896 / 4.674e+05 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0400 / 28.91 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.05 | 1.0413 / 12.83 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.1 | 1.0461 / 724.8 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.25 | 1.0238 / 2381 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.5 ! | 0.9232 / 2224 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.75 ! | 0.8405 / 3624 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp1.0 ! | 0.7650 / 6059 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 156.7821 / 3.324e+07 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.05 | 154.9809 / 1.514e+07 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.1 | 151.9184 / 5.463e+07 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.25 | 178.5507 / 1.869e+10 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.5 ! | 85.1992 / 1.753e+08 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.75 ! | 56.3736 / 9.51e+07 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp1.0 ! | 41.9377 / 9.729e+07 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |

---

## c1e3_exp1.0, K = -0.5

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 2.2991 / 510.2 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.05 | 2.3007 / 110 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.1 | 2.3009 / 63 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.25 | 2.3036 / 55.43 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.5 ! | 2.3032 / 623.8 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.75 ! | 2.2885 / 1805 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp1.0 ! | 2.2714 / 3916 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0364 / 134.1 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.05 | 1.0400 / 28.91 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.1 | 1.0404 / 16.32 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.25 | 1.0413 / 12.83 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.5 ! | 1.0461 / 724.8 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.75 ! | 1.0398 / 789.2 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp1.0 ! | 1.0256 / 632.5 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 158.4930 / 7.616e+07 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.05 | 156.7821 / 3.324e+07 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.1 | 158.0541 / 2.209e+07 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.25 | 154.9809 / 1.514e+07 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.5 ! | 151.9184 / 5.463e+07 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.75 ! | 165.3355 / 2.052e+09 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp1.0 ! | 157.1028 / 2.352e+09 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |

---

## c1e3_exp1.0, K = -1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.1495 / 252.9 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.05 | 1.1498 / 52.27 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.1 | 1.1503 / 27.5 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.25 | 1.1514 / 13.78 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.5 ! | 1.1518 / 13.86 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.75 ! | 1.1514 / 25.92 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp1.0 ! | 1.1516 / 155.9 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0393 / 267.9 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.05 | 1.0381 / 55.1 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.1 | 1.0400 / 28.91 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.25 | 1.0406 / 13.98 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.5 ! | 1.0413 / 12.83 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.75 ! | 1.0408 / 17.88 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp1.0 ! | 1.0461 / 724.8 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 160.8514 / 1.216e+08 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.05 | 159.0159 / 1.885e+08 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.1 | 156.7821 / 3.324e+07 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.25 | 157.7517 / 1.394e+07 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.5 ! | 154.9809 / 1.514e+07 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.75 ! | 156.9669 / 9.63e+07 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp1.0 ! | 151.9184 / 5.463e+07 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |

---

## c1e3_exp1.0, K = -2.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.5765 / 126.2 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.05 | 0.5746 / 25.59 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.1 | 0.5749 / 13.07 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.25 | 0.5752 / 5.655 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.5 ! | 0.5757 / 3.445 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.75 ! | 0.5765 / 3.359 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp1.0 ! | 0.5759 / 3.465 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0399 / 532.3 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.05 | 1.0362 / 107.6 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.1 | 1.0381 / 55.1 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.25 | 1.0409 / 23.79 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.5 ! | 1.0406 / 13.98 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.75 ! | 1.0419 / 12.58 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp1.0 ! | 1.0413 / 12.83 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 160.9252 / 2.454e+08 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.05 | 161.3385 / 2.724e+08 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.1 | 159.0159 / 1.885e+08 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.25 | 157.3720 / 2.09e+07 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.5 ! | 157.7517 / 1.394e+07 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.75 ! | 158.3056 / 1.862e+07 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp1.0 ! | 154.9809 / 1.514e+07 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |

---

## c1e3_exp1.0, K = -3.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.3837 / 83.65 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.05 | 0.3830 / 16.95 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.1 | 0.3830 / 8.569 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.25 | 0.3835 / 3.605 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.5 ! | 0.3835 / 1.997 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.75 ! | 0.3838 / 1.531 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp1.0 ! | 0.3842 / 1.395 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0389 / 798.6 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.05 | 1.0357 / 160.6 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.1 | 1.0370 / 81.4 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.25 | 1.0400 / 34.12 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.5 ! | 1.0407 / 18.7 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.75 ! | 1.0406 / 13.98 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp1.0 ! | 1.0416 / 12.44 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 151.3120 / 1.289e+08 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.05 | 160.4083 / 7.211e+07 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.1 | 157.5153 / 3.366e+07 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.25 | 157.7769 / 2.758e+07 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.5 ! | 155.1359 / 1.181e+07 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.75 ! | 157.7517 / 1.394e+07 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp1.0 ! | 158.2645 / 4.473e+07 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |

---

## c1e3_exp1.0, K = -4.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.2878 / 63.06 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.05 | 0.2869 / 12.6 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.1 | 0.2873 / 6.397 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.25 | 0.2876 / 2.647 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.5 ! | 0.2876 / 1.414 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.75 ! | 0.2876 / 1.027 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp1.0 ! | 0.2879 / 0.8612 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0359 / 1057 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.05 | 1.0349 / 212.7 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.1 | 1.0362 / 107.6 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.25 | 1.0387 / 44.58 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.5 ! | 1.0409 / 23.79 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.75 ! | 1.0404 / 17.03 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp1.0 ! | 1.0406 / 13.98 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 151.4045 / 1.513e+08 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.05 | 155.1774 / 1.372e+08 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.1 | 161.3385 / 2.724e+08 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.25 | 156.0604 / 2.036e+07 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.5 ! | 157.3720 / 2.09e+07 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.75 ! | 158.6151 / 6.522e+07 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp1.0 ! | 157.7517 / 1.394e+07 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |

---

## c1e3_exp1.0, K = -10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.1156 / 25.28 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.05 | 0.1153 / 5.047 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.1 | 0.1149 / 2.529 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.25 | 0.1149 / 1.024 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.5 ! | 0.1150 / 0.5227 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.75 ! | 0.1150 / 0.3569 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp1.0 ! | 0.1150 / 0.275 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0527 / 2721 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.05 | 1.0399 / 532.3 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.1 | 1.0393 / 267.9 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.25 | 1.0362 / 107.6 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.5 ! | 1.0381 / 55.1 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.75 ! | 1.0393 / 37.57 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp1.0 ! | 1.0400 / 28.91 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 151.2545 / 3.927e+08 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.05 | 160.9252 / 2.454e+08 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.1 | 160.8514 / 1.216e+08 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.25 | 161.3385 / 2.724e+08 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.5 ! | 159.0159 / 1.885e+08 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.75 ! | 156.2895 / 4.855e+07 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp1.0 ! | 156.7821 / 3.324e+07 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |

---

## c1e4_exp1.0, K = -0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 115.1584 / 1.559e+06 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.05 | 100.9162 / 5.77e+07 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.1 | 78.8965 / 4.674e+07 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.25 | 47.2069 / 5.547e+07 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.5 ! | 27.5820 / 2.653e+07 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.75 ! | 19.4163 / 1.37e+07 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp1.0 ! | 14.9542 / 7.852e+06 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0461 / 724.8 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.05 | 0.9232 / 2224 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.1 | 0.7650 / 6059 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.25 | 0.4638 / 5122 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.5 ! | 0.2702 / 2224 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.75 ! | 0.1915 / 1423 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp1.0 ! | 0.1478 / 861.9 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 266.6381 / 1.037e+09 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.05 | 111.5275 / 4.302e+08 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.1 | 47.6204 / 1.405e+08 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.25 | 12.9450 / 2.809e+07 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.5 ! | 4.3272 / 2.614e+06 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp0.75 ! | 2.3469 / 6.043e+05 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |
| stratified_exp1.0 ! | 1.5429 / 2.128e+05 | 1.4941 / 3.982e+06 | 192.0419 / 8.322e+10 | 0.0095 / n/r | 0.9459 / n/r |

---

## c1e4_exp1.0, K = -0.05

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 23.0095 / 6300 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.05 | 23.0317 / 6.238e+04 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.1 | 22.7144 / 3.916e+05 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.25 | 20.1832 / 2.308e+06 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.5 ! | 15.7793 / 1.87e+06 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.75 ! | 12.9840 / 2.542e+06 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp1.0 ! | 10.9744 / 2.578e+06 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0404 / 16.32 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.05 | 1.0461 / 724.8 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.1 | 1.0256 / 632.5 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.25 | 0.9232 / 2224 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.5 ! | 0.7650 / 6059 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.75 ! | 0.6387 / 7904 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp1.0 ! | 0.5408 / 6602 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 278.6039 / 2.897e+08 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.05 | 266.6381 / 1.037e+09 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.1 | 256.9211 / 7.265e+09 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.25 | 111.5275 / 4.302e+08 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.5 ! | 47.6204 / 1.405e+08 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp0.75 ! | 28.0586 / 1.182e+08 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |
| stratified_exp1.0 ! | 18.4233 / 5.918e+07 | 1.0370 / 926.3 | 23.2620 / 1.611e+06 | 0.0342 / n/r | 0.6988 / n/r |

---

## c1e4_exp1.0, K = -0.1

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 11.5034 / 2750 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.05 | 11.5181 / 1386 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.1 | 11.5158 / 1.559e+04 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.25 | 11.3209 / 3.468e+05 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.5 ! | 10.0916 / 5.77e+05 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.75 ! | 8.8539 / 4.199e+05 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp1.0 ! | 7.8896 / 4.674e+05 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0400 / 28.91 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.05 | 1.0413 / 12.83 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.1 | 1.0461 / 724.8 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.25 | 1.0238 / 2381 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.5 ! | 0.9232 / 2224 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.75 ! | 0.8405 / 3624 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp1.0 ! | 0.7650 / 6059 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 272.0558 / 2.015e+08 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.05 | 265.8855 / 1.556e+08 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.1 | 266.6381 / 1.037e+09 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.25 | 249.7338 / 2.593e+10 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.5 ! | 111.5275 / 4.302e+08 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp0.75 ! | 68.8519 / 2.394e+08 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |
| stratified_exp1.0 ! | 47.6204 / 1.405e+08 | 1.0437 / 115.5 | 11.5216 / 9386 | 0.0510 / n/r | 0.5309 / n/r |

---

## c1e4_exp1.0, K = -0.5

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 2.2991 / 510.2 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.05 | 2.3007 / 110 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.1 | 2.3009 / 63 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.25 | 2.3036 / 55.43 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.5 ! | 2.3032 / 623.8 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.75 ! | 2.2885 / 1805 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp1.0 ! | 2.2714 / 3916 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0364 / 134.1 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.05 | 1.0400 / 28.91 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.1 | 1.0404 / 16.32 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.25 | 1.0413 / 12.83 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.5 ! | 1.0461 / 724.8 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.75 ! | 1.0398 / 789.2 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp1.0 ! | 1.0256 / 632.5 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 283.3289 / 7.695e+08 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.05 | 272.0558 / 2.015e+08 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.1 | 278.6039 / 2.897e+08 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.25 | 265.8855 / 1.556e+08 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.5 ! | 266.6381 / 1.037e+09 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp0.75 ! | 270.9617 / 8.606e+09 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |
| stratified_exp1.0 ! | 256.9211 / 7.265e+09 | 1.0396 / 16.26 | 2.3006 / 63.03 | 0.0854 / n/r | 0.1852 / n/r |

---

## c1e4_exp1.0, K = -1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.1495 / 252.9 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.05 | 1.1498 / 52.27 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.1 | 1.1503 / 27.5 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.25 | 1.1514 / 13.78 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.5 ! | 1.1518 / 13.86 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.75 ! | 1.1514 / 25.92 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp1.0 ! | 1.1516 / 155.9 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0393 / 267.9 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.05 | 1.0381 / 55.1 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.1 | 1.0400 / 28.91 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.25 | 1.0406 / 13.98 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.5 ! | 1.0413 / 12.83 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.75 ! | 1.0408 / 17.88 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp1.0 ! | 1.0461 / 724.8 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 278.7167 / 1.107e+09 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.05 | 283.8702 / 1.409e+09 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.1 | 272.0558 / 2.015e+08 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.25 | 276.8630 / 1.451e+08 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.5 ! | 265.8855 / 1.556e+08 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp0.75 ! | 276.2173 / 7.221e+08 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |
| stratified_exp1.0 ! | 266.6381 / 1.037e+09 | 1.0388 / 28.87 | 1.1500 / 27.5 | 0.0936 / n/r | 0.1025 / n/r |

---

## c1e4_exp1.0, K = -2.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.5765 / 126.2 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.05 | 0.5746 / 25.59 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.1 | 0.5749 / 13.07 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.25 | 0.5752 / 5.655 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.5 ! | 0.5757 / 3.445 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.75 ! | 0.5765 / 3.359 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp1.0 ! | 0.5759 / 3.465 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0399 / 532.3 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.05 | 1.0362 / 107.6 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.1 | 1.0381 / 55.1 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.25 | 1.0409 / 23.79 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.5 ! | 1.0406 / 13.98 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.75 ! | 1.0419 / 12.58 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp1.0 ! | 1.0413 / 12.83 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 282.4690 / 1.945e+09 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.05 | 277.2448 / 4.843e+08 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.1 | 283.8702 / 1.409e+09 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.25 | 268.1124 / 9.228e+07 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.5 ! | 276.8630 / 1.451e+08 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp0.75 ! | 272.1409 / 1.216e+08 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |
| stratified_exp1.0 ! | 265.8855 / 1.556e+08 | 1.0375 / 55.02 | 0.5753 / 13.06 | 0.0983 / n/r | 0.0542 / n/r |

---

## c1e4_exp1.0, K = -3.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.3837 / 83.65 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.05 | 0.3830 / 16.95 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.1 | 0.3830 / 8.569 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.25 | 0.3835 / 3.605 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.5 ! | 0.3835 / 1.997 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.75 ! | 0.3838 / 1.531 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp1.0 ! | 0.3842 / 1.395 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0389 / 798.6 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.05 | 1.0357 / 160.6 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.1 | 1.0370 / 81.4 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.25 | 1.0400 / 34.12 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.5 ! | 1.0407 / 18.7 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.75 ! | 1.0406 / 13.98 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp1.0 ! | 1.0416 / 12.44 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 288.6201 / 1.856e+09 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.05 | 283.1903 / 7.735e+08 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.1 | 271.8444 / 2.138e+08 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.25 | 273.4237 / 2.342e+08 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.5 ! | 284.6160 / 4.299e+08 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp0.75 ! | 276.8630 / 1.451e+08 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |
| stratified_exp1.0 ! | 277.1740 / 1.794e+08 | 1.0350 / 80.92 | 0.3833 / 8.555 | 0.0998 / n/r | 0.0368 / n/r |

---

## c1e4_exp1.0, K = -4.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.2878 / 63.06 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.05 | 0.2869 / 12.6 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.1 | 0.2873 / 6.397 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.25 | 0.2876 / 2.647 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.5 ! | 0.2876 / 1.414 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.75 ! | 0.2876 / 1.027 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp1.0 ! | 0.2879 / 0.8612 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0359 / 1057 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.05 | 1.0349 / 212.7 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.1 | 1.0362 / 107.6 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.25 | 1.0387 / 44.58 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.5 ! | 1.0409 / 23.79 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.75 ! | 1.0404 / 17.03 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp1.0 ! | 1.0406 / 13.98 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 264.0431 / 2.339e+09 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.05 | 274.7786 / 1.204e+09 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.1 | 277.2448 / 4.843e+08 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.25 | 273.7033 / 1.765e+08 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.5 ! | 268.1124 / 9.228e+07 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp0.75 ! | 277.5866 / 1.826e+08 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |
| stratified_exp1.0 ! | 276.8630 / 1.451e+08 | 1.0376 / 107.9 | 0.2879 / 6.383 | 0.1010 / n/r | 0.0279 / n/r |

---

## c1e4_exp1.0, K = -10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.1156 / 25.28 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.05 | 0.1153 / 5.047 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.1 | 0.1149 / 2.529 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.25 | 0.1149 / 1.024 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.5 ! | 0.1150 / 0.5227 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.75 ! | 0.1150 / 0.3569 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp1.0 ! | 0.1150 / 0.275 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0527 / 2721 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.05 | 1.0399 / 532.3 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.1 | 1.0393 / 267.9 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.25 | 1.0362 / 107.6 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.5 ! | 1.0381 / 55.1 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.75 ! | 1.0393 / 37.57 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp1.0 ! | 1.0400 / 28.91 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 270.7324 / 3.943e+09 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.05 | 282.4690 / 1.945e+09 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.1 | 278.7167 / 1.107e+09 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.25 | 277.2448 / 4.843e+08 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.5 ! | 283.8702 / 1.409e+09 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp0.75 ! | 270.9280 / 1.721e+08 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |
| stratified_exp1.0 ! | 272.0558 / 2.015e+08 | 1.0418 / 269.6 | 0.1157 / 2.545 | 0.1030 / n/r | 0.0114 / n/r |

---

# RESULTS (Dense Table)

---

## naive_ps, K = -0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.4973 / 17.14 | 62.7888 / 3.817e+05 | 21.7140 / 1.265e+06 |
| stratified_exp0.05 | 0.4423 / 3964 | 53.2156 / 1.713e+07 | 15.5261 / 7.707e+06 |
| stratified_exp0.1 | 0.3552 / 7828 | 41.7589 / 3.864e+07 | 9.7688 / 7.213e+06 |
| stratified_exp0.25 | 0.1925 / 3064 | 23.3729 / 1.708e+07 | 3.4393 / 1.087e+06 |
| stratified_exp0.5 ! | 0.1045 / 868.8 | 13.3282 / 6.992e+06 | 1.4325 / 1.816e+05 |
| stratified_exp0.75 ! | 0.0707 / 379.5 | 9.2604 / 3.607e+06 | 0.8416 / 6.145e+04 |
| stratified_exp1.0 ! | 0.0532 / 205.3 | 7.0767 / 2.132e+06 | 0.5785 / 2.768e+04 |

---

## naive_ps, K = -0.05

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.5000 / 10.72 | 12.6027 / 5112 | 22.2116 / 9.545e+05 |
| stratified_exp0.05 | 0.4973 / 17.14 | 12.5578 / 1.527e+04 | 21.7140 / 1.265e+06 |
| stratified_exp0.1 | 0.4893 / 378.3 | 12.3952 / 4.504e+05 | 21.4016 / 9.738e+06 |
| stratified_exp0.25 | 0.4423 / 3964 | 10.6431 / 6.85e+05 | 15.5261 / 7.707e+06 |
| stratified_exp0.5 ! | 0.3552 / 7828 | 8.3518 / 1.545e+06 | 9.7688 / 7.213e+06 |
| stratified_exp0.75 ! | 0.2765 / 4880 | 6.5746 / 1.035e+06 | 6.3556 / 3.302e+06 |
| stratified_exp1.0 ! | 0.2287 / 3997 | 5.4746 / 8.349e+05 | 4.5865 / 1.976e+06 |

---

## naive_ps, K = -0.1

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.4995 / 18.67 | 6.2885 / 2199 | 22.3576 / 1.205e+06 |
| stratified_exp0.05 | 0.5006 / 7.966 | 6.3061 / 1161 | 22.6735 / 1.152e+06 |
| stratified_exp0.1 | 0.4973 / 17.14 | 6.2789 / 3817 | 21.7140 / 1.265e+06 |
| stratified_exp0.25 | 0.4764 / 279.5 | 6.0090 / 5.163e+04 | 19.9900 / 9.536e+06 |
| stratified_exp0.5 ! | 0.4423 / 3964 | 5.3216 / 1.713e+05 | 15.5261 / 7.707e+06 |
| stratified_exp0.75 ! | 0.4051 / 9167 | 4.7544 / 4.064e+05 | 11.9737 / 5.466e+06 |
| stratified_exp1.0 ! | 0.3552 / 7828 | 4.1759 / 3.864e+05 | 9.7688 / 7.213e+06 |

---

## naive_ps, K = -0.5

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.4963 / 85.27 | 1.2550 / 402.5 | 22.1982 / 2.46e+06 |
| stratified_exp0.05 | 0.4995 / 18.67 | 1.2577 / 87.96 | 22.3576 / 1.205e+06 |
| stratified_exp0.1 | 0.5000 / 10.72 | 1.2603 / 51.12 | 22.2116 / 9.545e+05 |
| stratified_exp0.25 | 0.5006 / 7.966 | 1.2612 / 46.45 | 22.6735 / 1.152e+06 |
| stratified_exp0.5 ! | 0.4973 / 17.14 | 1.2558 / 152.7 | 21.7140 / 1.265e+06 |
| stratified_exp0.75 ! | 0.4956 / 155.9 | 1.2461 / 524.5 | 20.6408 / 1.019e+06 |
| stratified_exp1.0 ! | 0.4893 / 378.3 | 1.2395 / 4504 | 21.4016 / 9.738e+06 |

---

## naive_ps, K = -1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.4989 / 171.1 | 0.6283 / 199.6 | 22.7782 / 1.137e+07 |
| stratified_exp0.05 | 0.4997 / 35.47 | 0.6296 / 41.63 | 22.8115 / 6.573e+06 |
| stratified_exp0.1 | 0.4995 / 18.67 | 0.6288 / 21.99 | 22.3576 / 1.205e+06 |
| stratified_exp0.25 | 0.5007 / 9.256 | 0.6307 / 11.15 | 23.4007 / 6.299e+06 |
| stratified_exp0.5 ! | 0.5006 / 7.966 | 0.6306 / 11.61 | 22.6735 / 1.152e+06 |
| stratified_exp0.75 ! | 0.4990 / 10.97 | 0.6291 / 19.94 | 21.9860 / 8.815e+05 |
| stratified_exp1.0 ! | 0.4973 / 17.14 | 0.6279 / 38.17 | 21.7140 / 1.265e+06 |

---

## naive_ps, K = -2.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.4963 / 337.5 | 0.3127 / 98.18 | 21.0686 / 3.681e+06 |
| stratified_exp0.05 | 0.4978 / 68.83 | 0.3140 / 20.25 | 22.6924 / 3.244e+06 |
| stratified_exp0.1 | 0.4997 / 35.47 | 0.3148 / 10.41 | 22.8115 / 6.573e+06 |
| stratified_exp0.25 | 0.4988 / 15.4 | 0.3144 / 4.54 | 22.1281 / 8.269e+05 |
| stratified_exp0.5 ! | 0.5007 / 9.256 | 0.3153 / 2.788 | 23.4007 / 6.299e+06 |
| stratified_exp0.75 ! | 0.5004 / 8.167 | 0.3156 / 2.895 | 22.7801 / 2.103e+06 |
| stratified_exp1.0 ! | 0.5006 / 7.966 | 0.3153 / 2.903 | 22.6735 / 1.152e+06 |

---

## naive_ps, K = -3.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.4973 / 512.4 | 0.2086 / 65.99 | 22.5488 / 2.066e+07 |
| stratified_exp0.05 | 0.4971 / 102.5 | 0.2092 / 13.39 | 25.5240 / 1.216e+08 |
| stratified_exp0.1 | 0.4988 / 52.14 | 0.2094 / 6.804 | 22.9247 / 5.152e+06 |
| stratified_exp0.25 | 0.4998 / 22.01 | 0.2097 / 2.882 | 22.8530 / 1.911e+06 |
| stratified_exp0.5 ! | 0.4992 / 12.21 | 0.2098 / 1.613 | 22.6523 / 1.068e+06 |
| stratified_exp0.75 ! | 0.5007 / 9.256 | 0.2102 / 1.239 | 23.4007 / 6.299e+06 |
| stratified_exp1.0 ! | 0.5011 / 8.129 | 0.2105 / 1.164 | 22.6351 / 9.671e+05 |

---

## naive_ps, K = -4.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.4988 / 688.9 | 0.1566 / 49.76 | 20.8536 / 4.739e+06 |
| stratified_exp0.05 | 0.4998 / 137.2 | 0.1572 / 10.04 | 23.1551 / 4.816e+06 |
| stratified_exp0.1 | 0.4978 / 68.83 | 0.1570 / 5.063 | 22.6924 / 3.244e+06 |
| stratified_exp0.25 | 0.4998 / 28.75 | 0.1574 / 2.113 | 22.8382 / 1.87e+06 |
| stratified_exp0.5 ! | 0.4988 / 15.4 | 0.1572 / 1.135 | 22.1281 / 8.269e+05 |
| stratified_exp0.75 ! | 0.4997 / 11.21 | 0.1575 / 0.8339 | 22.2724 / 8.902e+05 |
| stratified_exp1.0 ! | 0.5007 / 9.256 | 0.1577 / 0.697 | 23.4007 / 6.299e+06 |

---

## naive_ps, K = -10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.5019 / 1710 | 0.0636 / 20.05 | 21.9570 / 1.778e+07 |
| stratified_exp0.05 | 0.4963 / 337.5 | 0.0625 / 3.927 | 21.0686 / 3.681e+06 |
| stratified_exp0.1 | 0.4989 / 171.1 | 0.0628 / 1.996 | 22.7782 / 1.137e+07 |
| stratified_exp0.25 | 0.4978 / 68.83 | 0.0628 / 0.8101 | 22.6924 / 3.244e+06 |
| stratified_exp0.5 ! | 0.4997 / 35.47 | 0.0630 / 0.4163 | 22.8115 / 6.573e+06 |
| stratified_exp0.75 ! | 0.4996 / 24.22 | 0.0629 / 0.2853 | 22.1099 / 7.494e+05 |
| stratified_exp1.0 ! | 0.4995 / 18.67 | 0.0629 / 0.2199 | 22.3576 / 1.205e+06 |

---

## cmplx_ps, K = -0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6649 / 115.3 | 209.4920 / 1.672e+06 | 69.1916 / 9.352e+06 |
| stratified_exp0.05 | 1.4645 / 8793 | 184.9835 / 1.381e+08 | 49.9948 / 5.068e+07 |
| stratified_exp0.1 | 1.1534 / 1.043e+04 | 144.2413 / 1.494e+08 | 31.1043 / 2.23e+07 |
| stratified_exp0.25 | 0.6450 / 1.169e+04 | 85.1294 / 2.54e+08 | 12.1792 / 6.874e+06 |
| stratified_exp0.5 ! | 0.3478 / 4111 | 48.6255 / 9.698e+07 | 5.2253 / 1.74e+06 |
| stratified_exp0.75 ! | 0.2321 / 1604 | 33.7021 / 4.566e+07 | 3.1126 / 8.788e+05 |
| stratified_exp1.0 ! | 0.1734 / 799.1 | 25.7289 / 2.579e+07 | 2.1383 / 4.36e+05 |

---

## cmplx_ps, K = -0.05

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6661 / 23.51 | 41.9330 / 1.082e+04 | 70.1570 / 8.602e+06 |
| stratified_exp0.05 | 1.6649 / 115.3 | 41.8984 / 6.69e+04 | 69.1916 / 9.352e+06 |
| stratified_exp0.1 | 1.6547 / 2674 | 41.7490 / 2.34e+06 | 65.7711 / 5.927e+07 |
| stratified_exp0.25 | 1.4645 / 8793 | 36.9967 / 5.522e+06 | 49.9948 / 5.068e+07 |
| stratified_exp0.5 ! | 1.1534 / 1.043e+04 | 28.8483 / 5.976e+06 | 31.1043 / 2.23e+07 |
| stratified_exp0.75 ! | 0.9332 / 1.188e+04 | 23.6920 / 9.061e+06 | 21.8270 / 1.472e+07 |
| stratified_exp1.0 ! | 0.7721 / 1.405e+04 | 19.8960 / 1.118e+07 | 16.0944 / 1.069e+07 |

---

## cmplx_ps, K = -0.1

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6666 / 41.76 | 20.9654 / 4841 | 69.1093 / 5.061e+06 |
| stratified_exp0.05 | 1.6670 / 19.58 | 20.9748 / 2465 | 69.2097 / 2.235e+06 |
| stratified_exp0.1 | 1.6649 / 115.3 | 20.9492 / 1.672e+04 | 69.1916 / 9.352e+06 |
| stratified_exp0.25 | 1.6626 / 1.513e+04 | 20.7611 / 1.196e+06 | 67.6199 / 1.99e+08 |
| stratified_exp0.5 ! | 1.4645 / 8793 | 18.4983 / 1.381e+06 | 49.9948 / 5.068e+07 |
| stratified_exp0.75 ! | 1.3189 / 1.817e+04 | 16.2710 / 1.869e+06 | 39.8449 / 8.163e+07 |
| stratified_exp1.0 ! | 1.1534 / 1.043e+04 | 14.4241 / 1.494e+06 | 31.1043 / 2.23e+07 |

---

## cmplx_ps, K = -0.5

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6637 / 195.2 | 4.1918 / 921 | 70.7488 / 3.584e+07 |
| stratified_exp0.05 | 1.6666 / 41.76 | 4.1931 / 193.6 | 69.1093 / 5.061e+06 |
| stratified_exp0.1 | 1.6661 / 23.51 | 4.1933 / 108.2 | 70.1570 / 8.602e+06 |
| stratified_exp0.25 | 1.6670 / 19.58 | 4.1950 / 98.59 | 69.2097 / 2.235e+06 |
| stratified_exp0.5 ! | 1.6649 / 115.3 | 4.1898 / 669 | 69.1916 / 9.352e+06 |
| stratified_exp0.75 ! | 1.6568 / 341.8 | 4.1864 / 6617 | 69.0296 / 5.12e+07 |
| stratified_exp1.0 ! | 1.6547 / 2674 | 4.1749 / 2.34e+04 | 65.7711 / 5.927e+07 |

---

## cmplx_ps, K = -1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6710 / 391.7 | 2.1021 / 461.6 | 70.5053 / 2.041e+07 |
| stratified_exp0.05 | 1.6675 / 80.12 | 2.0980 / 93.76 | 68.2121 / 2.215e+06 |
| stratified_exp0.1 | 1.6666 / 41.76 | 2.0965 / 48.41 | 69.1093 / 5.061e+06 |
| stratified_exp0.25 | 1.6682 / 20.52 | 2.0983 / 23.63 | 70.4583 / 8.625e+06 |
| stratified_exp0.5 ! | 1.6670 / 19.58 | 2.0975 / 24.65 | 69.2097 / 2.235e+06 |
| stratified_exp0.75 ! | 1.6678 / 54.1 | 2.0974 / 68.4 | 71.0838 / 2.507e+07 |
| stratified_exp1.0 ! | 1.6649 / 115.3 | 2.0949 / 167.2 | 69.1916 / 9.352e+06 |

---

## cmplx_ps, K = -2.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6737 / 778.5 | 1.0504 / 229.1 | 68.1313 / 1.587e+07 |
| stratified_exp0.05 | 1.6616 / 155.9 | 1.0479 / 46.15 | 69.4300 / 8.385e+06 |
| stratified_exp0.1 | 1.6675 / 80.12 | 1.0490 / 23.44 | 68.2121 / 2.215e+06 |
| stratified_exp0.25 | 1.6657 / 34.19 | 1.0479 / 9.881 | 69.5778 / 2.846e+06 |
| stratified_exp0.5 ! | 1.6682 / 20.52 | 1.0492 / 5.907 | 70.4583 / 8.625e+06 |
| stratified_exp0.75 ! | 1.6675 / 18.16 | 1.0493 / 5.533 | 69.8615 / 4.203e+06 |
| stratified_exp1.0 ! | 1.6670 / 19.58 | 1.0487 / 6.162 | 69.2097 / 2.235e+06 |

---

## cmplx_ps, K = -3.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6728 / 1168 | 0.6996 / 153.1 | 73.3296 / 8.53e+07 |
| stratified_exp0.05 | 1.6634 / 233.4 | 0.6988 / 30.67 | 69.3045 / 9.023e+06 |
| stratified_exp0.1 | 1.6641 / 118.2 | 0.6989 / 15.48 | 71.4171 / 1.292e+07 |
| stratified_exp0.25 | 1.6684 / 49.49 | 0.6992 / 6.385 | 70.0327 / 6.142e+06 |
| stratified_exp0.5 ! | 1.6656 / 26.94 | 0.6989 / 3.455 | 70.2618 / 3.539e+06 |
| stratified_exp0.75 ! | 1.6682 / 20.52 | 0.6994 / 2.625 | 70.4583 / 8.625e+06 |
| stratified_exp1.0 ! | 1.6677 / 18.03 | 0.6995 / 2.338 | 69.5264 / 2.802e+06 |

---

## cmplx_ps, K = -4.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6661 / 1545 | 0.5228 / 114.4 | 69.7294 / 9.02e+07 |
| stratified_exp0.05 | 1.6636 / 309.8 | 0.5244 / 23 | 76.9830 / 5.278e+08 |
| stratified_exp0.1 | 1.6616 / 155.9 | 0.5239 / 11.54 | 69.4300 / 8.385e+06 |
| stratified_exp0.25 | 1.6684 / 64.78 | 0.5246 / 4.725 | 73.8629 / 2.365e+08 |
| stratified_exp0.5 ! | 1.6657 / 34.19 | 0.5240 / 2.47 | 69.5778 / 2.846e+06 |
| stratified_exp0.75 ! | 1.6658 / 24.6 | 0.5242 / 1.773 | 70.1135 / 3.535e+06 |
| stratified_exp1.0 ! | 1.6682 / 20.52 | 0.5246 / 1.477 | 70.4583 / 8.625e+06 |

---

## cmplx_ps, K = -10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6768 / 3939 | 0.2097 / 45.96 | 70.2778 / 8.672e+07 |
| stratified_exp0.05 | 1.6737 / 778.5 | 0.2101 / 9.165 | 68.1313 / 1.587e+07 |
| stratified_exp0.1 | 1.6710 / 391.7 | 0.2102 / 4.616 | 70.5053 / 2.041e+07 |
| stratified_exp0.25 | 1.6616 / 155.9 | 0.2096 / 1.846 | 69.4300 / 8.385e+06 |
| stratified_exp0.5 ! | 1.6675 / 80.12 | 0.2098 / 0.9376 | 68.2121 / 2.215e+06 |
| stratified_exp0.75 ! | 1.6688 / 54.55 | 0.2099 / 0.636 | 70.6089 / 6.634e+06 |
| stratified_exp1.0 ! | 1.6666 / 41.76 | 0.2097 / 0.4841 | 69.1093 / 5.061e+06 |

---

## c1e3_exp1.0, K = -0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0461 / 724.8 | 115.1584 / 1.559e+06 | 151.9184 / 5.463e+07 |
| stratified_exp0.05 | 0.9232 / 2224 | 100.9162 / 5.77e+07 | 85.1992 / 1.753e+08 |
| stratified_exp0.1 | 0.7650 / 6059 | 78.8965 / 4.674e+07 | 41.9377 / 9.729e+07 |
| stratified_exp0.25 | 0.4638 / 5122 | 47.2069 / 5.547e+07 | 12.4862 / 2.625e+07 |
| stratified_exp0.5 ! | 0.2702 / 2224 | 27.5820 / 2.653e+07 | 4.2794 / 2.464e+06 |
| stratified_exp0.75 ! | 0.1915 / 1423 | 19.4163 / 1.37e+07 | 2.3311 / 5.959e+05 |
| stratified_exp1.0 ! | 0.1478 / 861.9 | 14.9542 / 7.852e+06 | 1.5354 / 2.081e+05 |

---

## c1e3_exp1.0, K = -0.05

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0404 / 16.32 | 23.0095 / 6300 | 158.0541 / 2.209e+07 |
| stratified_exp0.05 | 1.0461 / 724.8 | 23.0317 / 6.238e+04 | 151.9184 / 5.463e+07 |
| stratified_exp0.1 | 1.0256 / 632.5 | 22.7144 / 3.916e+05 | 157.1028 / 2.352e+09 |
| stratified_exp0.25 | 0.9232 / 2224 | 20.1832 / 2.308e+06 | 85.1992 / 1.753e+08 |
| stratified_exp0.5 ! | 0.7650 / 6059 | 15.7793 / 1.87e+06 | 41.9377 / 9.729e+07 |
| stratified_exp0.75 ! | 0.6387 / 7904 | 12.9840 / 2.542e+06 | 26.7737 / 1.092e+08 |
| stratified_exp1.0 ! | 0.5408 / 6602 | 10.9744 / 2.578e+06 | 17.6712 / 5.386e+07 |

---

## c1e3_exp1.0, K = -0.1

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0400 / 28.91 | 11.5034 / 2750 | 156.7821 / 3.324e+07 |
| stratified_exp0.05 | 1.0413 / 12.83 | 11.5181 / 1386 | 154.9809 / 1.514e+07 |
| stratified_exp0.1 | 1.0461 / 724.8 | 11.5158 / 1.559e+04 | 151.9184 / 5.463e+07 |
| stratified_exp0.25 | 1.0238 / 2381 | 11.3209 / 3.468e+05 | 178.5507 / 1.869e+10 |
| stratified_exp0.5 ! | 0.9232 / 2224 | 10.0916 / 5.77e+05 | 85.1992 / 1.753e+08 |
| stratified_exp0.75 ! | 0.8405 / 3624 | 8.8539 / 4.199e+05 | 56.3736 / 9.51e+07 |
| stratified_exp1.0 ! | 0.7650 / 6059 | 7.8896 / 4.674e+05 | 41.9377 / 9.729e+07 |

---

## c1e3_exp1.0, K = -0.5

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0364 / 134.1 | 2.2991 / 510.2 | 158.4930 / 7.616e+07 |
| stratified_exp0.05 | 1.0400 / 28.91 | 2.3007 / 110 | 156.7821 / 3.324e+07 |
| stratified_exp0.1 | 1.0404 / 16.32 | 2.3009 / 63 | 158.0541 / 2.209e+07 |
| stratified_exp0.25 | 1.0413 / 12.83 | 2.3036 / 55.43 | 154.9809 / 1.514e+07 |
| stratified_exp0.5 ! | 1.0461 / 724.8 | 2.3032 / 623.8 | 151.9184 / 5.463e+07 |
| stratified_exp0.75 ! | 1.0398 / 789.2 | 2.2885 / 1805 | 165.3355 / 2.052e+09 |
| stratified_exp1.0 ! | 1.0256 / 632.5 | 2.2714 / 3916 | 157.1028 / 2.352e+09 |

---

## c1e3_exp1.0, K = -1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0393 / 267.9 | 1.1495 / 252.9 | 160.8514 / 1.216e+08 |
| stratified_exp0.05 | 1.0381 / 55.1 | 1.1498 / 52.27 | 159.0159 / 1.885e+08 |
| stratified_exp0.1 | 1.0400 / 28.91 | 1.1503 / 27.5 | 156.7821 / 3.324e+07 |
| stratified_exp0.25 | 1.0406 / 13.98 | 1.1514 / 13.78 | 157.7517 / 1.394e+07 |
| stratified_exp0.5 ! | 1.0413 / 12.83 | 1.1518 / 13.86 | 154.9809 / 1.514e+07 |
| stratified_exp0.75 ! | 1.0408 / 17.88 | 1.1514 / 25.92 | 156.9669 / 9.63e+07 |
| stratified_exp1.0 ! | 1.0461 / 724.8 | 1.1516 / 155.9 | 151.9184 / 5.463e+07 |

---

## c1e3_exp1.0, K = -2.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0399 / 532.3 | 0.5765 / 126.2 | 160.9252 / 2.454e+08 |
| stratified_exp0.05 | 1.0362 / 107.6 | 0.5746 / 25.59 | 161.3385 / 2.724e+08 |
| stratified_exp0.1 | 1.0381 / 55.1 | 0.5749 / 13.07 | 159.0159 / 1.885e+08 |
| stratified_exp0.25 | 1.0409 / 23.79 | 0.5752 / 5.655 | 157.3720 / 2.09e+07 |
| stratified_exp0.5 ! | 1.0406 / 13.98 | 0.5757 / 3.445 | 157.7517 / 1.394e+07 |
| stratified_exp0.75 ! | 1.0419 / 12.58 | 0.5765 / 3.359 | 158.3056 / 1.862e+07 |
| stratified_exp1.0 ! | 1.0413 / 12.83 | 0.5759 / 3.465 | 154.9809 / 1.514e+07 |

---

## c1e3_exp1.0, K = -3.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0389 / 798.6 | 0.3837 / 83.65 | 151.3120 / 1.289e+08 |
| stratified_exp0.05 | 1.0357 / 160.6 | 0.3830 / 16.95 | 160.4083 / 7.211e+07 |
| stratified_exp0.1 | 1.0370 / 81.4 | 0.3830 / 8.569 | 157.5153 / 3.366e+07 |
| stratified_exp0.25 | 1.0400 / 34.12 | 0.3835 / 3.605 | 157.7769 / 2.758e+07 |
| stratified_exp0.5 ! | 1.0407 / 18.7 | 0.3835 / 1.997 | 155.1359 / 1.181e+07 |
| stratified_exp0.75 ! | 1.0406 / 13.98 | 0.3838 / 1.531 | 157.7517 / 1.394e+07 |
| stratified_exp1.0 ! | 1.0416 / 12.44 | 0.3842 / 1.395 | 158.2645 / 4.473e+07 |

---

## c1e3_exp1.0, K = -4.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0359 / 1057 | 0.2878 / 63.06 | 151.4045 / 1.513e+08 |
| stratified_exp0.05 | 1.0349 / 212.7 | 0.2869 / 12.6 | 155.1774 / 1.372e+08 |
| stratified_exp0.1 | 1.0362 / 107.6 | 0.2873 / 6.397 | 161.3385 / 2.724e+08 |
| stratified_exp0.25 | 1.0387 / 44.58 | 0.2876 / 2.647 | 156.0604 / 2.036e+07 |
| stratified_exp0.5 ! | 1.0409 / 23.79 | 0.2876 / 1.414 | 157.3720 / 2.09e+07 |
| stratified_exp0.75 ! | 1.0404 / 17.03 | 0.2876 / 1.027 | 158.6151 / 6.522e+07 |
| stratified_exp1.0 ! | 1.0406 / 13.98 | 0.2879 / 0.8612 | 157.7517 / 1.394e+07 |

---

## c1e3_exp1.0, K = -10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0527 / 2721 | 0.1156 / 25.28 | 151.2545 / 3.927e+08 |
| stratified_exp0.05 | 1.0399 / 532.3 | 0.1153 / 5.047 | 160.9252 / 2.454e+08 |
| stratified_exp0.1 | 1.0393 / 267.9 | 0.1149 / 2.529 | 160.8514 / 1.216e+08 |
| stratified_exp0.25 | 1.0362 / 107.6 | 0.1149 / 1.024 | 161.3385 / 2.724e+08 |
| stratified_exp0.5 ! | 1.0381 / 55.1 | 0.1150 / 0.5227 | 159.0159 / 1.885e+08 |
| stratified_exp0.75 ! | 1.0393 / 37.57 | 0.1150 / 0.3569 | 156.2895 / 4.855e+07 |
| stratified_exp1.0 ! | 1.0400 / 28.91 | 0.1150 / 0.275 | 156.7821 / 3.324e+07 |

---

## c1e4_exp1.0, K = -0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0461 / 724.8 | 115.1584 / 1.559e+06 | 266.6381 / 1.037e+09 |
| stratified_exp0.05 | 0.9232 / 2224 | 100.9162 / 5.77e+07 | 111.5275 / 4.302e+08 |
| stratified_exp0.1 | 0.7650 / 6059 | 78.8965 / 4.674e+07 | 47.6204 / 1.405e+08 |
| stratified_exp0.25 | 0.4638 / 5122 | 47.2069 / 5.547e+07 | 12.9450 / 2.809e+07 |
| stratified_exp0.5 ! | 0.2702 / 2224 | 27.5820 / 2.653e+07 | 4.3272 / 2.614e+06 |
| stratified_exp0.75 ! | 0.1915 / 1423 | 19.4163 / 1.37e+07 | 2.3469 / 6.043e+05 |
| stratified_exp1.0 ! | 0.1478 / 861.9 | 14.9542 / 7.852e+06 | 1.5429 / 2.128e+05 |

---

## c1e4_exp1.0, K = -0.05

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0404 / 16.32 | 23.0095 / 6300 | 278.6039 / 2.897e+08 |
| stratified_exp0.05 | 1.0461 / 724.8 | 23.0317 / 6.238e+04 | 266.6381 / 1.037e+09 |
| stratified_exp0.1 | 1.0256 / 632.5 | 22.7144 / 3.916e+05 | 256.9211 / 7.265e+09 |
| stratified_exp0.25 | 0.9232 / 2224 | 20.1832 / 2.308e+06 | 111.5275 / 4.302e+08 |
| stratified_exp0.5 ! | 0.7650 / 6059 | 15.7793 / 1.87e+06 | 47.6204 / 1.405e+08 |
| stratified_exp0.75 ! | 0.6387 / 7904 | 12.9840 / 2.542e+06 | 28.0586 / 1.182e+08 |
| stratified_exp1.0 ! | 0.5408 / 6602 | 10.9744 / 2.578e+06 | 18.4233 / 5.918e+07 |

---

## c1e4_exp1.0, K = -0.1

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0400 / 28.91 | 11.5034 / 2750 | 272.0558 / 2.015e+08 |
| stratified_exp0.05 | 1.0413 / 12.83 | 11.5181 / 1386 | 265.8855 / 1.556e+08 |
| stratified_exp0.1 | 1.0461 / 724.8 | 11.5158 / 1.559e+04 | 266.6381 / 1.037e+09 |
| stratified_exp0.25 | 1.0238 / 2381 | 11.3209 / 3.468e+05 | 249.7338 / 2.593e+10 |
| stratified_exp0.5 ! | 0.9232 / 2224 | 10.0916 / 5.77e+05 | 111.5275 / 4.302e+08 |
| stratified_exp0.75 ! | 0.8405 / 3624 | 8.8539 / 4.199e+05 | 68.8519 / 2.394e+08 |
| stratified_exp1.0 ! | 0.7650 / 6059 | 7.8896 / 4.674e+05 | 47.6204 / 1.405e+08 |

---

## c1e4_exp1.0, K = -0.5

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0364 / 134.1 | 2.2991 / 510.2 | 283.3289 / 7.695e+08 |
| stratified_exp0.05 | 1.0400 / 28.91 | 2.3007 / 110 | 272.0558 / 2.015e+08 |
| stratified_exp0.1 | 1.0404 / 16.32 | 2.3009 / 63 | 278.6039 / 2.897e+08 |
| stratified_exp0.25 | 1.0413 / 12.83 | 2.3036 / 55.43 | 265.8855 / 1.556e+08 |
| stratified_exp0.5 ! | 1.0461 / 724.8 | 2.3032 / 623.8 | 266.6381 / 1.037e+09 |
| stratified_exp0.75 ! | 1.0398 / 789.2 | 2.2885 / 1805 | 270.9617 / 8.606e+09 |
| stratified_exp1.0 ! | 1.0256 / 632.5 | 2.2714 / 3916 | 256.9211 / 7.265e+09 |

---

## c1e4_exp1.0, K = -1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0393 / 267.9 | 1.1495 / 252.9 | 278.7167 / 1.107e+09 |
| stratified_exp0.05 | 1.0381 / 55.1 | 1.1498 / 52.27 | 283.8702 / 1.409e+09 |
| stratified_exp0.1 | 1.0400 / 28.91 | 1.1503 / 27.5 | 272.0558 / 2.015e+08 |
| stratified_exp0.25 | 1.0406 / 13.98 | 1.1514 / 13.78 | 276.8630 / 1.451e+08 |
| stratified_exp0.5 ! | 1.0413 / 12.83 | 1.1518 / 13.86 | 265.8855 / 1.556e+08 |
| stratified_exp0.75 ! | 1.0408 / 17.88 | 1.1514 / 25.92 | 276.2173 / 7.221e+08 |
| stratified_exp1.0 ! | 1.0461 / 724.8 | 1.1516 / 155.9 | 266.6381 / 1.037e+09 |

---

## c1e4_exp1.0, K = -2.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0399 / 532.3 | 0.5765 / 126.2 | 282.4690 / 1.945e+09 |
| stratified_exp0.05 | 1.0362 / 107.6 | 0.5746 / 25.59 | 277.2448 / 4.843e+08 |
| stratified_exp0.1 | 1.0381 / 55.1 | 0.5749 / 13.07 | 283.8702 / 1.409e+09 |
| stratified_exp0.25 | 1.0409 / 23.79 | 0.5752 / 5.655 | 268.1124 / 9.228e+07 |
| stratified_exp0.5 ! | 1.0406 / 13.98 | 0.5757 / 3.445 | 276.8630 / 1.451e+08 |
| stratified_exp0.75 ! | 1.0419 / 12.58 | 0.5765 / 3.359 | 272.1409 / 1.216e+08 |
| stratified_exp1.0 ! | 1.0413 / 12.83 | 0.5759 / 3.465 | 265.8855 / 1.556e+08 |

---

## c1e4_exp1.0, K = -3.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0389 / 798.6 | 0.3837 / 83.65 | 288.6201 / 1.856e+09 |
| stratified_exp0.05 | 1.0357 / 160.6 | 0.3830 / 16.95 | 283.1903 / 7.735e+08 |
| stratified_exp0.1 | 1.0370 / 81.4 | 0.3830 / 8.569 | 271.8444 / 2.138e+08 |
| stratified_exp0.25 | 1.0400 / 34.12 | 0.3835 / 3.605 | 273.4237 / 2.342e+08 |
| stratified_exp0.5 ! | 1.0407 / 18.7 | 0.3835 / 1.997 | 284.6160 / 4.299e+08 |
| stratified_exp0.75 ! | 1.0406 / 13.98 | 0.3838 / 1.531 | 276.8630 / 1.451e+08 |
| stratified_exp1.0 ! | 1.0416 / 12.44 | 0.3842 / 1.395 | 277.1740 / 1.794e+08 |

---

## c1e4_exp1.0, K = -4.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0359 / 1057 | 0.2878 / 63.06 | 264.0431 / 2.339e+09 |
| stratified_exp0.05 | 1.0349 / 212.7 | 0.2869 / 12.6 | 274.7786 / 1.204e+09 |
| stratified_exp0.1 | 1.0362 / 107.6 | 0.2873 / 6.397 | 277.2448 / 4.843e+08 |
| stratified_exp0.25 | 1.0387 / 44.58 | 0.2876 / 2.647 | 273.7033 / 1.765e+08 |
| stratified_exp0.5 ! | 1.0409 / 23.79 | 0.2876 / 1.414 | 268.1124 / 9.228e+07 |
| stratified_exp0.75 ! | 1.0404 / 17.03 | 0.2876 / 1.027 | 277.5866 / 1.826e+08 |
| stratified_exp1.0 ! | 1.0406 / 13.98 | 0.2879 / 0.8612 | 276.8630 / 1.451e+08 |

---

## c1e4_exp1.0, K = -10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0527 / 2721 | 0.1156 / 25.28 | 270.7324 / 3.943e+09 |
| stratified_exp0.05 | 1.0399 / 532.3 | 0.1153 / 5.047 | 282.4690 / 1.945e+09 |
| stratified_exp0.1 | 1.0393 / 267.9 | 0.1149 / 2.529 | 278.7167 / 1.107e+09 |
| stratified_exp0.25 | 1.0362 / 107.6 | 0.1149 / 1.024 | 277.2448 / 4.843e+08 |
| stratified_exp0.5 ! | 1.0381 / 55.1 | 0.1150 / 0.5227 | 283.8702 / 1.409e+09 |
| stratified_exp0.75 ! | 1.0393 / 37.57 | 0.1150 / 0.3569 | 270.9280 / 1.721e+08 |
| stratified_exp1.0 ! | 1.0400 / 28.91 | 0.1150 / 0.275 | 272.0558 / 2.015e+08 |


---

# Insights and conclusions

**All 2268 runs completed (2268/2268). There were zero failures and zero non-finite values**: none in any numeric column of the collected CSV, and no NaN or Infinity token in any `test_metrics.json`. With `mode=opt` the model is the exact Bayes posterior (`OptimalModelRefactor`). So every number here measures the importance-weighted **estimator** at a given `(ps, K, λ)`, not a model.

Two structural facts decide how to read everything below.
- **The reference pass is one number per `(ps, K, seed)`** (§1).
- **The loss pass depends on `(K, λ)` only through `lamR2 = λ/|K| = λR²`** (§2).

Together they mean the grid holds far fewer independent measurements than cells. The 3 seeds are its only independent replication.

## 1. The reference pass is invariant, and `c1e3 = c1e4` except under VCE

**Hypothesis 3 passes, to float64 precision.** The check covers 108 `(ps, K, seed)` groups of 21 `(lg, λ)` cells each:

| metric | groups bitwise identical | max relative spread |
|---|---|---|
| `wce_ref`, `ce_ref`, `wce_ref_std` | 108 / 108 | 0 |
| `wnelbo_ref`, `nelbo_ref` | 103 / 108 each | 2.14e-16 (1 ulp) |
| `wnelbo_ref_std` | 99 / 108 | 4.9e-16 (≤ 3 ulp) |

- **Only c1e4, and only at the ulp level.** All 19 non-bitwise (group, metric) pairs are `c1e4_exp1.0` (15 groups), and none has more than 2 distinct values. The minority value is scattered across `ce`, `pp` and `vce` and across rates, so it does not follow lg or λ.
- **The split follows hardware.** Where it was traced, it follows the machine the job ran on:
  - in all 19 pairs, the odd value comes from the runs whose SLURM log names no GPU;
  - in 4 groups mapped with `sacct`, those are exactly the runs on `desa-compute-01`.
  
  This is repeatable per-hardware rounding, not an RNG leak. A leak that depended on lg or λ would move a mean by about `std/sqrt(N)` (≈ 3.7e-3 for c1e4, `K = -2`, seed 0), roughly 13 orders of magnitude more.
- **The hypothesis's premise is only half true.** `salt=1` seeds only the generator that draws `t`. The bridge draws come from the global RNG seeded by `L.seed_everything(seed)`: `torch.rand` in `sample_radial` and `torch.randn` in `_free_direction`. The reference pass reads that stream right after the loss pass. The invariance holds because the loss pass consumes a fixed-shape number of global draws in every cell. So what this check proves is "same RNG consumption in every cell", not "separate bridge streams".

**`c1e3` and `c1e4` are one validation, not two.** Over the 189 paired runs per lg, these all agree to ≤ 5.9e-16 relative:
- all six reference fields;
- `ce` and `pp` `test_wloss` and `test_wloss_std`.

Only `vce` differs (§6). Do not quote the two specs as corroborating each other for CE or ELBO.

## 2. The loss pass sees `(K, λ)` only through `lamR2 = λ/|K|`

**Measured.** Within each `(ps, seed)`, cells with equal `lamR2` repeat the same computation up to floating-point rounding. There are 156 multi-cell groups per lg (12 `(ps, seed)` × 13 shared `lamR2` values).

| lg | invariant quantity | max rel. spread, mean | max rel. spread, per-sample std |
|---|---|---|---|
| `pp` | `wloss` | 7.3e-16 | 6.6e-15 |
| `vce` | `wloss` | 5.4e-14 | 5.3e-13 |
| `ce` | `wloss / R^2` | 4.4e-15 | 7.2e-15 |

Examples:
- **pp:** `naive_ps` seed 1 at `lamR2 = 10` gives 0.306001132586367, 0.3060011325863668 and 0.3060011325863669 at `(K, λ)` = (−0.01, 0.1), (−0.05, 0.5) and (−0.1, 1.0).
- **ce:** raw `ce` is not invariant; it scales by the R² ratio. `c1e3` seed 1 at `lamR2 = 1` reads 114.74780383348018 at `K = -0.01` and 1.1474780383348007 at `K = -1`.

**Why, from the code.** Four facts combine:
- **Same random numbers in every cell of a seed.** The stratified `u` comes from a per-step generator whose seed has no `ps`, `K`, `lg` or `λ` term. The bridge's global-RNG draws have fixed shapes, and the targets come from their own generator (`seed+2`).
- **The proposal is scale-free.** `t|K| = -ln(u)/lamR2` and the weight is `1/(λu) = R²/(lamR2·u)`. The heat-time clamp `96.96 R^2` is a fixed 96.96 in unit time.
- **The sampler and readout are dimensionless.** The sampler returns `rho = R·rho_1(t/R^2)`. The boost, the horosphere logits and the losses read only `kappa·rho`.
- **The loss prefactors decide the R² scaling.** `pp` and `vce` carry an explicit `kappa^2 = |K|`, which cancels the R² in the weight. `ce` (plain `F.cross_entropy`) has no such factor, so it keeps the R².

**Consequences.**
- **Duplicate cells.** The 63 `(K, λ)` cells hold only **37 distinct `lamR2`** values (0.001 to 100). Thirteen values are shared by 2–5 cells (39 cells). The other 24 cells have no partner, so for them the collapse follows from the code, not from data.
- **Distinct values.** Counting `c1e3 = c1e4` for ce and pp, the 2268 runs contain **1110 numerically distinct loss-pass values** (ce 333, pp 333, vce 444) and **81 distinct reference values**.
- **Correlated values.** The distinct values are still not independent. Within a seed, every `ps`, `K`, `λ` and `lg` reuses the same uniforms. Seed residuals correlate about 0.7 at adjacent `lamR2` (ratio ≤ 1.34) and fall to about 0 beyond a ratio of 2.6 for `lamR2 ≤ 1`. For `lamR2 ≥ 1` a correlation of 0.3–0.5 persists. Counts like "n/9 below H" across `ps` or across `lamR2` cannot be multiplied into a significance level.
- **No separate K effect.** The loss pass cannot separate a curvature effect from a rate effect. Any trend "along K at fixed λ" is a `lamR2` trend. The old §4 ("the integral moves, the proposal does not") was describing this.
- **The old grid agrees.** Its tables show the same identity. All 52 multi-member `pp` classes print identical strings; for example, `naive_ps` `pp` at `lamR2 = 1` reads `0.4995 / 22.48` in all 5 cells. The `ce` classes agree after dividing the mean by R² and the variance by R⁴, within print rounding.
- **vce's larger spread.** The `vce` spread (a few hundred ulp) is still rounding. Hypothesis, not tested: its `1/min_v D^2` weight amplifies ulp differences in `t/R^2`.

**The reference pass is the same estimator at `lamR2_ref = 0.1/|K|`, on a different stream.** It is the same `get_logits_inputs` plus `weighted_loss_refactor` at rate 0.1. The difference is its `t` stream (`salt=1`) and its bridge draws (a later stretch of the global RNG); it shares the target tokens. So it is an effectively independent replicate of the loss cell `(K, 0.1)`, not a copy.

For `K ∈ [-10, -0.05]`:
- **Ratios.** The 3-seed ratio of `wnelbo_ref` to `pp` `wloss(K, 0.1)` lies in **[0.9973, 1.0145]**. The ratio of `wce_ref` to `ce` `wloss(K, 0.1)` lies in **[0.9979, 1.0241]**.
- **z-scores.** Per-seed z lies in [−1.21, +1.70] using `std/sqrt(N)`, or [−1.78, +2.50] with the calibrated SE of §5.

That is consistent with one shared distribution, at a precision of about 0.5–1.5%.

## 3. Soundness is a function of `lamR2`

**Loss pass, `pp` `wloss / H(p)`.** Values are 3-seed means; `c1e3` equals `c1e4` for pp. The last column is the c1e4 per-sample variance (the tables' "/" half) with its seed max/min in brackets.

| `lamR2` | naive_ps | cmplx_ps | c1e3 = c1e4 | c1e4 per-sample var (seed max/min) |
|---|---|---|---|---|
| 0.001 | 1.0032 | 1.0062 | 1.0116 | 2721 (1.10) |
| 0.01 | 0.9972 | 1.0028 | 0.9987 | 267.9 (1.01) |
| 0.1 | 0.9984 | 1.0001 | 0.9994 | 28.9 (1.01) |
| 0.25 | 1.0009 | 1.0011 | 0.9999 | 14.0 (1.00) |
| 0.5 | 1.0007 | 1.0004 | 1.0006 | 12.8 (1.07) |
| 0.75 | 0.9974 | 1.0009 | 1.0001 | 17.9 (1.06) |
| 1 | 0.9941 | 0.9991 | 1.0052 | 724.8 (82.2) |
| 1.5 | 0.9906 | 0.9943 | 0.9991 | 789.2 (16.2) |
| 2 | 0.9780 | 0.9930 | 0.9855 | 632.5 (6.84) |
| 2.5 | 0.9523 | 0.9977 | 0.9838 | 2381 (12.0) |
| 5 | 0.8841 | 0.8789 | 0.8871 | 2224 (1.44) |
| 10 | 0.7101 | 0.6922 | 0.7351 | 6059 (3.58) |
| 25 | 0.3848 | 0.3871 | 0.4457 | 5122 (3.79) |
| 100 | 0.1063 | 0.1040 | 0.1421 | 862 (3.34) |

The pooled readings below use naive, cmplx and c1e3 × 3 seeds.

- **`lamR2 ∈ [0.01, 1]`: sound.**
  - All 189 per-seed readings lie within **[−1.50%, +2.46%]** of H(p), and every pooled per-`lamR2` mean lies within [−0.46%, +0.11%].
  - For `lamR2 ∈ [0.001, 0.005]` readings lie within [−1.83%, +2.58%]. They are noisier because the per-sample std grows like `lamR2^-1/2` (18–63).
  - This does not demonstrate zero bias. A small low offset of about −0.1% to −0.5% at `lamR2` ≈ 0.01–0.2 is not excluded (seed-level t about −3 to −3.5 with df = 2).
- **`lamR2 = 1` is the edge.**
  - One c1e3 seed, with per-sample std 46 against 5.1 and 5.7 for the others, reads +2.46%.
  - The pp per-sample std agrees across seeds (max/min ≤ 1.08) only up to `lamR2 = 0.5`.
- **`lamR2` 1.5–2.5: onset, not pinned down.** Typical readings start to fall below H. Seed-level t is −2.2 / −4.1 / −2.2 (df = 2) at 1.5 / 2 / 2.5.
- **`lamR2 ≥ 5`: every one of the 81 loss-pass readings is below H.** Pooled means are −11.7% at 5, −28.8% at 10 and −88.3% at 100, and each `(ps, seed)` falls monotonically.

**What the low readings are, and are not.**
- **Not a bias from the proposal weight or the t clamp.**
  - The `stratified_exp` weight is exactly `1/q(t)`.
  - The t clamp cannot bind for `lamR2 > 0.285`. Where it does bind, it replaces the tail beyond `s = t|K| = 96.96` with a term `f(96.96)·(27.63/lamR2 − 96.96)`. That term depends on `lamR2`, but it is ≥ 0 (the pp integrand is ≥ 0 and the weight is unclamped), so it can only add mass. The expectation is therefore only approximately independent of `lamR2`, and the `lamR2`-dependent part is never negative.
  - So the deficit is either a finite-sample shortfall of a heavy-tailed estimator, or, at large `lamR2`, truncation of the expectation by the `u ≥ 1e-12` clamp. That clamp removes `s > 27.6/lamR2`, so at `lamR2 = 100` it caps `s` at 0.276. Both effects scale as `1/lamR2`, and the data cannot separate them.
- **Hypothesis: limited reach.** A 4e6-draw pass reaches about `s ≈ 15.2/lamR2`, and mass beyond that shows up only as rare huge weights. Consistent with this, within each ps, runs with larger std read higher (Spearman +0.62 to +0.93 for `lamR2` 0.75–5).
- §4 shows the other face of the same tail.

**Reference pass, `wnelbo_ref` 3-seed mean (deviation from H(p)).**

| K | `lamR2_ref` | naive_ps | cmplx_ps | c1e3 = c1e4 | old `exp` grid (naive / cmplx / c1e3) |
|---|---|---|---|---|---|
| −10 | 0.01 | 0.5061 (+1.2%) | 1.6691 (+0.2%) | 1.0418 (+0.1%) | −0.6 / −0.4 / −0.1% |
| −4 | 0.025 | 0.5000 (−0.1%) | 1.6674 (+0.1%) | 1.0376 (−0.3%) | −0.2 / −0.0 / −0.0% |
| −3 | 0.033 | 0.4987 (−0.3%) | 1.6641 (−0.1%) | 1.0350 (−0.5%) | +0.2 / +0.2 / −0.3% |
| −2 | 0.05 | 0.4997 (−0.1%) | 1.6630 (−0.2%) | 1.0375 (−0.3%) | +0.1 / +0.2 / −0.2% |
| −1 | 0.1 | 0.4990 (−0.3%) | 1.6657 (−0.0%) | 1.0388 (−0.2%) | +0.2 / +0.2 / +0.0% |
| −0.5 | 0.2 | 0.5001 (−0.0%) | 1.6676 (+0.1%) | 1.0396 (−0.1%) | +0.2 / +0.2 / +0.1% |
| −0.1 | 1 | 0.5004 (+0.0%) | 1.6638 (−0.2%) | 1.0437 (+0.3%) | +1.0 / −0.4 / +0.1% |
| **−0.05** | 2 | 0.4960 (−0.9%) | 1.6536 (−0.8%) | 1.0370 (−0.3%) | −2.2 / −1.7 / −0.8% |
| **−0.01** | 10 | **2.3074 (+361%)** | **4.4108 (+165%)** | **1.4941 (+44%)** | −28.2 / −25.4 / −26.3% |

- **`K ∈ [-10, -0.1]`.** All 63 per-seed readings lie within **[−0.72%, +1.65%]**. Max |z| is 1.67 on `std/sqrt(N)`. With the calibrated SE of §5, max |z| is about 2.3 and 5 of 63 exceed 2, which is unremarkable.
- **`K = -0.05`.** Readings lie in [−2.79%, +2.48%], median −1.16%, with 6/9 below H.
- **`K = -0.01`.** See §4.
- **The old usable range restated.** The old report's range `-10 <= K <= -0.1` ("usable to 3.3× the cliff") is the statement `lamR2_ref ≤ 1`. The flat-curvature failure belongs to the proposal at large `lamR2`, not to K. At `K = -0.01` itself, the loss pass at `λ = 0.01` (`lamR2 = 1`) reads **0.990–1.025 H on all 9 distinct runs**:
  - naive 0.9917 / 1.0003 / 0.9904;
  - cmplx 1.0000 / 0.9982 / 0.9991;
  - c1e3 1.0246 / 0.9958 / 0.9952.
- **Prediction, from the code but untested (no run exists).** A reference rate of `0.1·|K|` would make `wnelbo_ref` at every K the `K = -1`, rate-0.1 estimator, per seed. `wce_ref` would scale as R².

**`c1e3`: a small offset across the sound range is possible, and the dip at `K ∈ [-4, -2]` is unexplained.** Each cell uses 6 streams: 3 seeds × {reference pass, loss pass `pp` at λ = 0.1}.

| K (`lamR2`) | 6-stream mean vs H | nats | nominal `t_5` | p |
|---|---|---|---|---|
| −10 (0.01) | −0.010% | — | — | 0.97 |
| −4 (0.025) | −0.360% | −0.0038 | −5.08 | 0.004 |
| −3 (0.033) | −0.447% | −0.0047 | −4.74 | 0.005 |
| −2 (0.05) | −0.275% | −0.0029 | −5.73 | 0.002 |
| −1 (0.1) | −0.119% | — | — | 0.16 |

- **Per-cell tests.** Correcting over 21 tests leaves only `K = -2`.
- **Per-stream test over the pre-registered range.** Averaged per stream over `K ∈ [-10, -0.1]`, all 6 c1e3 streams read low (stream-mean z −0.53 / −0.10 / −0.66 / −0.88 / −0.25 / −0.58; `t_5` = −4.35, p ≈ 0.007, ≈ 0.02 across 3 ps; mean offset −0.12%). A constant offset of that size is not excluded by the `lamR2` 0.125–0.5 readings of the same salt-0 streams (3-seed means −0.02% to +0.12%, SE 0.10–0.135%). The post-hoc window `K ∈ [-4, -1]` gives `t_5` = −7.93, p = 5e-4.
- **Only the `lamR2`-localized 0.3–0.45% dip conflicts with an unbiased estimator.**

Reasons not to read the dip as a c1e3-specific bias:
- **The window was chosen after seeing the data.**
- **The rows are not independent.** The same 6 streams are reused at every K, and the 6-reading spread is only 0.33–0.53× the SE.
- **The expectation cannot be lower at small `lamR2`.** Across these `lamR2` it can differ only through the ≥ 0 t-clamp term, and that term is larger at smaller `lamR2` (see above). The same salt-0 streams read within ±0.12% of H at `lamR2` 0.125–0.75.
- **It is not specific to c1e3.** naive_ps and cmplx_ps also read lower in that window on the same seeds.
- **Other deviations have no power either way.** naive_ps at `K = -3` (−0.311%, `t_5` = −1.87, p = 0.12) is consistent with zero and equally with a c1e3-sized offset. The 84/126 sound-region readings below H is not a binomial result.
- **Scale.** Each deficit is about one per-run `std/sqrt(N)` (0.0052 / 0.0045 / 0.0037 nats at `K = -4 / -3 / -2`).

## 4. The heavy tail at flat curvature (`K = -0.01`, `lamR2_ref = 10`)

**Same estimator, two streams.** Per-seed values for seeds 0 / 1 / 2, divided by H(p). Bold marks readings above H.

| ps | reference (salt 1): `wnelbo_ref / H` | reference per-sample std | loss pass `pp` (salt 0), `(K=-0.01, λ=0.1)`: `wloss / H` |
|---|---|---|---|
| naive_ps | 0.997 / **12.04** / 0.796 | 272 / 11289 / 139 | 0.851 / 0.612 / 0.667 |
| cmplx_ps | 0.757 / **4.32** / **2.87** | 183 / 12181 / 7103 | 0.691 / 0.693 / 0.693 |
| c1e3 = c1e4 | 0.952 / 0.966 / **2.39** | 363 / 407 / 3413 | 0.779 / 0.712 / 0.715 |

- **The four readings above H are single-draw events.**
  - **Share bounds.** Every weighted pp sample is ≥ 0, so mean and std bound the largest draw's share of the mean: naive s1 [87.8%, 93.7%], cmplx s1 [71.6%, 84.6%], cmplx s2 [55.3%, 74.4%], c1e3 s2 [47.1%, 68.6%].
  - **Without the draw.** Subtracting that excess (about `std/sqrt(N)`) puts all nine reference readings 22–34% below H, the old grid's band.
  - **The five readings below H** have a lower bound of only 0.5–7.5% and an upper bound of 7–27%. No dominant draw is forced there, but none is ruled out either.
- **About two tail events, not four.** The salt-1 `u` stream is shared across ps.
  - **Seed 1** blows up naive and cmplx. Its `wce_ref` also has one draw carrying ≥ 72.1% / 64.4% / 52.9% of the total for naive / cmplx / c1e3.
  - **Seed 2** blows up cmplx and c1e3.
  - Whether a shared huge weight becomes an ELBO hit depends on the ps. For example, c1e3 s1 has a CE hit but no ELBO hit.
- **Where the hits sit, from a code bound.**
  - The pp integrand is ≤ `2(d-1)^2|K| = 0.08`. So the hits need `u` ≤ 3.8e-8 / 3.9e-8 / 7.6e-8 / 1.7e-7, i.e. `t` ≥ 171 / 171 / 164 / 156.
  - That is inside the proposal's support (`t ≤ 276`) and deeper than a typical pass's smallest draw (`u ≈ 2.5e-7`, `t ≈ 152`).
  - On the same `u` stream at `K = -0.05` and `-0.1`, that `t` becomes `s = t|K|` ≥ 8.5 and ≥ 17, where the integrand is ≤ 2e-4. The means there stay within −2.79%..+2.48% and ±0.92% of H.
- **The salt-0 loss pass caught no such draw.**
  - All 9 readings sit at 0.612–0.851 H, with per-sample std 24–145 and a largest-draw share ≤ 17%.
  - These 9 values repeat bit-for-bit at `(K=-0.05, λ=0.5)` and `(K=-0.1, λ=1.0)`.
- **The old grid is the mirror image.**
  - Its reference read 25–28% low (std 91 / 258 / 110).
  - Its salt-0 loss pass at `exp0.1`, `K = -0.01`, read 0.5783 (+15.6%), 1.3615 (−18.3%) and 0.8509 (−18.2%), with std 829 / 687 / 305.
  - Each grid had one tight low stream and one heavy-tailed stream. Only which salt was which swapped.
- **z-scores carry no information here.** When one draw X dominates, `mean ≈ X/N` and `std ≈ X/sqrt(N)`, so z ≈ 1 by construction (observed 0.97–1.06).
- **The unweighted metrics are reproducible.** Seed spread of `nelbo_ref` and `ce_ref` is ≤ 0.15%. naive gives 0.003473 / 0.003473 / 0.003474 and 0.4653 / 0.4652 / 0.4654.

**Verdict on hypothesis 2.**
- **`K = -0.05`: partly supported.** The reference gives −0.9 / −0.8 / −0.3%, 6/9 below H, which is not significant alone. The loss pass at `lamR2 = 2` gives −2.2 / −0.7 / −1.5%, 8/9 below.
- **`K = -0.01`: refuted as stated.**
  - The 3-seed means are +361 / +165 / +44%.
  - "~25% low" is the *typical hit-free reading*, not a stable property: the loss pass gives −29.0 / −30.8 / −26.5% (range −38.8% to −14.9%).
  - The reach argument was not falsified, since the typical deficit did not shrink. Its literal form ("cannot reach `t` the proposal never draws") fails: the overshooting runs drew `t ≳ 156–171` and found mass there.
  - What the data support is a heavy-tailed estimator whose typical reading sits well below its mean.
  - Whether that mean equals H at rate 0.1 is not established, because the `u` clamp caps `t ≤ 276`.
  - Hypothesis, not shown: the variance is effectively infinite for `lamR2` of about 1–2 and above.
- **The old correction numbers have no support.** Across six `(salt, seed)` streams, single readings run from 0.61 H to 12 H. With 2 of 6 streams hit, P(three hit-free old streams) could lie anywhere from about 0.01 to 0.9.

## 5. What stratification did and did not change

| | `EXPERIMENT.md` prediction | measured |
|---|---|---|
| per-sample variance | unchanged | new/old ratio of pooled std: `wnelbo_ref` 0.995–1.014 (18 `(ps, K)` cells, `K ∈ [-10, -0.5]`); `pp` `wloss` 0.996–1.028 (median 1.001) and `ce` `wloss` 0.991–1.010 over 57 unique `(ps, lamR2 ≤ 0.2)` cells; `pp` stays 0.973–1.035 up to `lamR2 = 0.5` |
| across-seed spread | smaller; `std/sqrt(N)` overstates the SE | `pp` ELBO scatter ≈ **0.65×** `std/sqrt(4e6)` (`K ∈ [-10, -0.5]`, 6 streams; 95% t-interval 0.54–0.73; a stream-clustered estimate gives 0.74 [0.64, 0.83]); `ce` ≈ 0.50; `vce` ≈ 0.93 (no clear shrink) |
| reach | unchanged | analytic: P(min `u` > 2.5e-7) = 0.3678 vs 0.3679 iid; P(min `u` > 1e-6) = 0.0182 vs 0.0183 |

- **Unchanged per-sample variance is nearly a code identity.** Every draw has the same marginal `(t, weight)`, and `*_std` is pooled over all 4e6 draws. The agreement is a check on the implementation, not a discovery.
  - **Where it scatters.** The ratio scatters from `lamR2` of about 0.75–1 (`pp` 0.70–4.13; the 4.13 is one c1e3 seed with std 46.0 against 5.1 / 5.7).
  - **At `K = -0.01`.** The reference seed-RMS std is 18–71× the old grid's; per seed it ranges 0.7× to 124×, median 3.7×. The §4 single draws drive this, not stratification.
- **The spread shrink.**
  - **Token counts explain little.** The exact-count test set (`counts_from_ps`) keeps between-token variance out of the scatter. That is about 3% of `pp` per-sample variance on average, an SD factor of about 0.98.
  - **Stratification remains a hypothesis.** Most of the `pp` shrink is consistent with `u` stratification, but this grid has no iid-proposal control. For `ce` the split between causes is not established.
- **"Smaller than the `exp` grid had" cannot be measured directly.** The old grid kept only 3-seed means.
  - The RMS z of the 3-seed mean about H over `K ∈ [-10, -0.5]` is 0.99 new vs 0.92 old, and both include offsets.
  - A paired loss-minus-reference statistic gives RMS 1.09 old vs 0.62 new. The old excess is one shared offset, so this is directional only.
- **Practical rule for error bars.**
  - For `pp` at `lamR2 ≲ 0.5`, the `std/sqrt(N)` error bar is about 1.5× too wide, so z-scores built on it are conservative.
  - At `lamR2 ≳ 1`, no std-based error bar is valid.
- **Reach, more generally.** Below any `u < 1/2048` (`t > 76` at rate 0.1), the tail count is a fixed 1954 draws against about Poisson(1953) for iid. The far tail is statistically unchanged, so the §4 change at `K = -0.01` is not a stratification reach effect. This assumes the old grid drew independent `t` per test batch. That was not confirmed from code; the old grid's within-noise readings at `K ≤ -0.1` argue for it.

## 6. VCE and CE

**Finite, but not necessarily precise.**
- **Range.** `vce` `wloss` runs from 0.546 (naive_ps, `K = -0.01`, λ = 1, seed 1) to 326.6 (c1e4, `K = -0.1`, λ = 0.25, seed 0).
- **Precision.** The maximum cell has per-sample std 2.58e5, so its nominal SE is about 129, roughly 40% of its mean.
- **Log space.** The data do not show that log-space accumulation was needed: every per-sample value stays at or below about 5.2e8.

**CE scales exactly as R².** The integrand depends on `t` only through `t/R^2`, so `dt = R² ds`. Raw `ce` `wloss` can only be compared across K after dividing by R². For example, naive at `lamR2 = 0.1` reads 0.06288 at `K = -10`, 0.6288 at `K = -1` and 6.288 at `K = -0.1`.

| ps | `ce wloss / R^2`, plateau (`lamR2 ≤ 1`) | × H(p) | `wce_ref / R^2` (K in [−10, −0.1]) | at `lamR2 = 100`, share of plateau (pp share of H) |
|---|---|---|---|---|
| naive_ps | 0.6291 | 1.257 | 0.6296 | 11.2% (10.6%) |
| cmplx_ps | 2.0973 | 1.259 | 2.0979 | 12.3% (10.4%) |
| c1e3 = c1e4 | 1.1508 | 1.106 | 1.1517 | 13.0% (14.2%) |

The CE integral has no H(p) target: its ratio to H depends on ps and on the time-unit convention. The plateau holds to `lamR2` of about 1.5–2 and then truncates at about the same rate as pp.

**The VCE mean shows a plateau, then a drop-off.**

| `lamR2` | naive | cmplx | c1e3 | c1e4 | `pp / H` (naive / cmplx / c1e3=c1e4) |
|---|---|---|---|---|---|
| plateau ≤ 1 (absolute) | 22.52 | 70.44 | 156.88 | 275.71 | ≈ 1 |
| 2.5 (÷ plateau) | 0.887 | 0.960 | 1.138 | 0.906 | 0.952 / 0.998 / 0.984 |
| 5 | 0.689 | 0.710 | 0.543 | 0.405 | 0.884 / 0.879 / 0.887 |
| 10 | 0.434 | 0.442 | 0.267 | 0.173 | 0.710 / 0.692 / 0.735 |
| 100 | 0.026 | 0.030 | 0.0098 | 0.0056 | 0.106 / 0.104 / 0.142 |

- **No drift detected for `lamR2 ≤ 1`.** Over the 25 distinct values, OLS slopes are +0.44 / −0.69 / +0.38 / −0.62% per decade (t = 0.44 / −1.03 / 0.80 / −1.06).
  - A drift up to about 2% per decade is not excluded.
  - cmplx's per-seed slopes are all negative (t = 3.7 on 2 dof). That is borderline and driven by one outlier.
  - Single-seed outliers reach +13% (naive at `lamR2 = 0.0167`: 31.51 / 22.98 / 22.08).
  - The c1e3 value at `lamR2 = 2.5` is one noisy cell.
- **Scope of that test.** The t clamp binds for `lamR2 ≲ 0.157`, which is 16 of the 25 plateau values; at 0.001, 91% of draws sit on the cap. The effective reach is therefore only `t/R^2` ≈ 15–97. Hypothesis 4's non-convergence is untested beyond that.
- **The drop-off.** VCE falls much faster than pp. Hypothesis: VCE's integrand mass sits at larger `t/R^2` than the ELBO's, and more so for c1e4. That fits c1e3 and c1e4 coinciding at large `lamR2` (1.535 vs 1.543 at 100).

**The VCE per-sample variance is far above pp's.**
- **Raw std ratio.** At matched `(ps, K, λ, seed)`, `vce` std exceeds `pp` std in 756/756 runs (444 distinct values). The median ratio is **355×** (per ps 190 / 235 / 738 / 2183×), the minimum 8×, and the minimum on the plateau 75×.
- **Most of it is scale.** Plateau medians of the mean ratio are 44.8 / 41.6 / 150 / 263. After dividing by the mean, the coefficient of variation is still higher for vce in every plateau run: medians **5.4 / 6.7 / 5.9 / 9.9×**, minimum 1.24. For `lamR2 ≥ 5` the medians fall to 1.3 / 1.6 / 2.2 / 2.4×.
- **Quote medians only.** vce's own std varies across seeds by a median 1.9× and up to 19.7×, against 1.01× for pp.

**VCE separates `c1e3` from `c1e4`.**
- **Direction and size.** `c1e4 > c1e3` in 189/189 runs (111 distinct). The gap has median 41.5% of c1e4 (range 0.35–52.4%), and c1e4's std is larger in 189/189 (median 2.4×, up to 9.7×).
- **The ratio depends on `lamR2`:**

| `lamR2` | ≤ 1 | 1.5–2 | 2.5 | 5 | 10 | 25 | 100 |
|---|---|---|---|---|---|---|---|
| c1e4 / c1e3, per seed | 1.62–2.10 (mean 1.758) | 1.50–1.85 | 1.34–1.54 | 1.28–1.33 | 1.07–1.20 | 1.03–1.04 | 1.004–1.006 |

- **Why the sign is near-structural, not a significance result.**
  - The vce weight takes `min_v D` over every table row, including zero-probability words.
  - c1e3's boundary table equals the first 994 rows of c1e4's (same seed-0 `randn`).
  - The two specs share the random draws and have identical CE.
  - The median nearest-neighbour `sin^2(a/2)` drops from 7.1e-4 to 7.2e-5 with the larger table.
  - From `lamR2 = 7.5` up, each difference is within 2 unpaired SEs.
- **Not a converged constant.** Nothing shows 1.76 is the population ratio. The high end of the plateau range comes with 6–10× std blow-ups.

**Cross-project: this VCE value is not a floor for the trained twin.** `init_test_log_vce_3d_refactor_new` is compared on the plateau, 46 cells per ps.

| ps | cells where twin < opt (3-seed mean) | every twin seed < every opt seed | twin/opt median | example `K=-1, λ=0.1` (twin vs opt) |
|---|---|---|---|---|
| naive_ps | 42 / 46 | 41 / 46 | 0.637 | 14.56 vs 22.36 |
| cmplx_ps | 46 / 46 | 46 / 46 | 0.498 | 34.51 vs 69.11 |
| c1e4_exp1.0 | 0 / 46 | — | 41.9 (single-seed dominated) | — |

- **naive exceptions.** The 4 naive cells not below opt are all rate 0.01: 1.556, 1.716, 1.316 and 1.009.
- **c1e4 is unstable, not bounded below.** Its 3-seed means are dominated by blown-up single seeds. 28/138 individual twin seeds read below the opt mean, as do 6/46 cell medians.
- **Effective sample.** The cells cover about 25 independent `lamR2` comparisons, and nominal z-scores are not valid significance levels for this estimator.
- **It refutes the pre-registered expectation.** `EXPERIMENT.md` expected a floor the twin "can only approach from above". The Bayes posterior minimises `E[W(z_t)·CE]` only for `OptimalModelRefactor`'s frozen `uniform_sphere_points` table.
- **The twin solves a different problem.** It runs with `trainable_word_embedding: true` and `unif_word_embedding: false`. One learned `lm_head.weight` sets the bridge target, `min_v D` and the readout. The twin also beats the Bayes posterior on the unweighted `ce_ref` in 41/46 (naive) and 45/46 (cmplx) cells; for example, naive `K = -1`, λ = 0.1 gives 0.0486 / 0.0493 / 0.0487 against 0.0556 / 0.0558 / 0.0556. So it samples a different `(y, z_t)` joint.
- **Hypothesis: the learned table causes the gap.** Its geometry clearly differs: naive's dominant token is pushed about 98–116° from its nearest neighbour.
- **Code provenance.** The `min_v D` weight was committed in `6e7b6c9` (2026-09-13 22:17), after the twin's runs wrote their metrics (09-11 15:59 to 09-12 03:36). The twin's `vce_bayes.md` (09-11 15:15), `EXPERIMENT.md` and `RESULTS.md` already describe the `min_v D` form and report the superseded target-indexed weight separately, so the twin almost certainly ran this weight uncommitted, but git cannot prove it. This grid ran the committed code: `loss.py`'s mtime is 2026-09-15 00:13, but its content is identical to HEAD (`git diff HEAD -- loss.py` is empty).

## 7. Hypothesis scorecard

| # | pre-registered hypothesis | verdict | evidence |
|---|---|---|---|
| 1 | `wnelbo_ref = H(p)` within noise for `K ∈ [-10, -0.1]`, smaller across-seed spread | **Partly** | Location: 63 per-seed readings in [−0.72%, +1.65%], seed means −0.54%..+1.16%. "Within noise" holds only on the conservative SE. Per stream over `K ∈ [-10, -0.1]`, all 6 c1e3 streams read low (`t_5` = −4.35, p ≈ 0.007; ≈ 0.02 across 3 ps; −0.12%). The `lamR2` 0.125–0.5 readings (SE 0.10–0.135%) do not exclude a constant offset that small. Only the `lamR2`-localized 0.3–0.45% dip at `K ∈ [-4, -2]` conflicts with an unbiased estimator, and it is unexplained (§3). Spread: `pp` scatter ≈ 0.65× `std/sqrt(N)`, but there is no direct old-vs-new measurement (§5). |
| 2 | `K = -0.05` stays 1–2% low; `K = -0.01` stays ~25% low | **Partly at −0.05; refuted as stated at −0.01** | Reference −0.9 / −0.8 / −0.3% at −0.05. At −0.01, seed means are +361 / +165 / +44% from about 2 single-draw events; the same estimator on salt 0 reads −29.0 / −30.8 / −26.5%. Reach not falsified, literal form unsupported (§4). |
| 3 | reference metrics identical across all 21 `(lg, λ)` cells | **Confirmed** (to 1 ulp) | Max relative spread 2.14e-16; the 1-ulp splits are c1e4-only and track hardware. The premise "own RNG stream" holds only for `t` (§1). |
| 4 | VCE finite; per-sample variance far above pp; mean drifts with rate where the integral diverges | **Partly** | Finite in 756/756 runs. std median 355× pp, CV 5–10× on the plateau. No drift detected for `lamR2 ≤ 1` (≤ ~2%/decade not excluded; reach only to `t/R^2 ≈ 97`). Log-space accumulation not shown to be needed (§6). |
| 5 | VCE breaks the c1e3 / c1e4 degeneracy | **Confirmed** | `c1e4 > c1e3` in 189/189, median gap 41.5%, plateau ratio ≈ 1.76 falling to 1.004 at `lamR2 = 100`; ce, pp and all reference metrics agree to ≤ 5.9e-16. The sign is near-structural (§6). |

## 8. What this licenses the trained projects to claim

**`init_test_3d_refactor_new` (`ce`, `pp`; all nine `K` ∈ {−10, −4, −3, −2, −1, −0.5, −0.1, −0.05, −0.01}; plain `exp` loss and reference proposals).**
- **Coverage.** Its output has `test_metrics.json` for all 9 curvatures (168/168 at each K). Only its `RESULTS.md` is stale: it still has just the `K` = −10 / −1 / −0.01 sections.
- **Its reference pass used plain `exp(0.1)`, so comparisons with this grid are qualitative.** Per-draw marginals and reach are the same (§5), so the estimator has the same expectation and per-sample variance. Batch-mean noise and per-seed values differ. The previous `exp` grid's numbers remain its like-for-like prior.
- **Grouped by `lamR2_ref = 0.1/|K|`:**
  - **`K ∈ [-10, -0.5]` (`lamR2_ref` 0.01–0.2): sound.**
    - Exact-model 3-seed means read −0.54% to +1.16% of H(p), and per-seed readings −0.72% to +1.65%. The old `exp` grid's seed means read −0.6% to +0.2%.
    - A trained `test_wnelbo_ref` above that band measures the model's own gap. One clearly below it is a leak or bug signal, since the estimator is sound here. Deviations of a few tenths of a percent either way cannot be attributed to the model.
  - **`K = -0.1` (`lamR2_ref = 1`): the edge.** Exact-model per-seed readings stay within ±1% ([−0.42%, +0.92%]; old `exp` seed means +1.0 / −0.4 / +0.1%). But agreement of the std across seeds is lost past `lamR2` ≈ 0.5: the reference per-sample std seed max/min here is 1.64 / 1.46 / 2.24 for naive / cmplx / c1e3.
  - **`K = -0.05` (`lamR2_ref = 2`): unresolved.** Exact-model per-seed readings span −2.79%..+2.48% (old `exp` seed means −2.2 / −1.7 / −0.8%). A trained deficit of a few percent there cannot be attributed to the model.
  - **`K = -0.01` (`lamR2_ref = 10`): neither a floor nor a correction number is licensed.**
    - The old guidance "compare to 0.3594 / 1.2439 / 0.7667" is withdrawn. Those were typical hit-free readings.
    - The same plain-exp estimator on the old salt-0 stream read +15.6% for naive.
    - A trained cell below H there is expected and is not a leak. A cell far above H may be one draw: check whether `std ≈ (reading − typical)·sqrt(N)`.
- **Loss-pass `wloss`.**
  - Read it through `lamR2`, and divide `ce` by R² before comparing across K.
  - `pp ≥ H` is a meaningful check only for `lamR2 ≲ 1`. At `lamR2 = 5 / 10 / 100` the exact model itself reads 0.818–0.992 / 0.612–0.851 / 0.096–0.149 H per seed.
- **To measure the ELBO at flat K, use `lamR2_ref ≲ 0.5`, i.e. a reference rate ≲ 0.5·|K| (0.005 at `K = -0.01`).**
  - §3 puts the edge at `lamR2 = 1`. At that value one c1e3 seed has std 46 against 5.1 / 5.7 and reads +2.46%; two naive seeds sit at z = −2.0 / −2.45; the c1e4 variance seed max/min is 82; and the pp std agrees across seeds only up to `lamR2 = 0.5`.
  - Rate 0.01 at `K = -0.01` (`lamR2 = 1`) reads 0.990–1.025 H on all 9 distinct runs here, but that setting is already at the edge, with one heavy-tailed seed.
  - This is a change to `setup.md`, flagged here rather than made.

**`init_test_log_vce_3d_refactor_new` (`vce`; same `stratified_exp(0.1)` reference).**
- **Reference readings.** Its `wnelbo_ref` / `wce_ref` are draws of the §3 estimator and should be compared in distribution; per-seed identity has not been checked.
  - `K ∈ [-10, -0.5]` is sound, and `K = -0.1` is the edge (per-seed readings within ±1%, but std agreement across seeds is lost).
  - At `K = -0.05`, per-seed readings of the exact model already span ±3%.
  - `K = -0.01` is not resolvable at this rate.
  - For `pp` at `K ∈ [-10, -0.5]`, `std/sqrt(N)` overstates the SE by about 1.5×.
- **Its VCE `test_wloss` is not bounded below by this project's VCE `wloss` as configured.** Twin/opt plateau medians are 0.637 (naive) and 0.498 (cmplx). It cannot claim to "approach the Bayes floor from above"; any such comparison needs a matched boundary table. Its c1e4 cells are single-seed dominated, so quote medians.
- **Compare VCE numbers at matched `lamR2`, preferably on the plateau (`lamR2 ≤ 1`).**
  - At `lamR2 = 5` the exact model already reads only 0.40–0.71 of its plateau.
  - The VCE per-sample std is not a usable error bar: seed-to-seed it varies 1.9× in the median, up to 19.7×.
- **c1e3 and c1e4 are different VCE problems** (plateau ratio ≈ 1.76), though they are identical for CE and the ELBO.

## 9. Reading the figures in `imgs/`

`visualization/wloss_exp_var_vs_curvature.py --ps c1e4_exp1.0` writes six panels, `wloss_{mean,variance}_{pp,ce,vce}_c1e4_exp1.0.png`. They were written at 05:02, after the last `test_metrics.json` (04:34:42), and they match the tables:

    mean panel y      ==  the number before "/" in the c1e4_exp1.0 wloss column  (seed mean of test_wloss)
    variance panel y  ==  the number after "/"                                    (seed mean of test_wloss_std**2)
    mean error bar    ==  sqrt(variance / 4e6)    single-run MC SE, not the SE of the 3-seed mean

**Rule illustration.** c1e4 `pp`, `K = -1`, `λ = 0.01` reads `1.0393 / 267.9` in the table (old grid `1.0351 / 266.2`). Its bar is `sqrt(267.9/4e6) = 0.0082`.

**Read-offs checked against the data:**

| panel | cell | plotted | data |
|---|---|---|---|
| pp mean | `K=-0.01, λ=0.1` | ~0.765 ± ~0.04 | 0.76495 ± 0.0389 |
| pp mean | `K=-0.05, λ=1` | ~0.54 | 0.54081 ± 0.0406 |
| vce mean | `K=-0.01, λ=0.05` | just above 10² | 111.53 ± 10.37 |
| vce mean | `K=-0.01, λ=1` | ~1.5 | 1.5429 ± 0.2306 |
| pp variance | `K=-10, λ=0.01` | ~2700 | 2720.7 |
| vce variance | `K=-0.1, λ=0.25` | ~2.6e10 | 2.593e10 |

**How to read the panels.**
- **Each panel is one curve.** The x axis is log |K| with one line per λ. By §2, each `pp` / `vce` line is a single master curve in `lamR2`, shifted horizontally by `log10 λ` at the 9 markers. The `ce` mean lines are additionally multiplied by `1/λ` (R² scaling), and the variance lines by `1/λ²`.
- **Few independent estimates.** A 63-point panel holds 37 distinct estimates, and the flat-K columns resample the same `lamR2` curve.
- **Axes and bars.** The `pp` mean panel has a linear y axis; the others are log. The bars match the seed scatter for pp at `K=-0.01, λ=0.1` (seed SD 0.0392). They do not for vce at `K=-0.01, λ=1` (seed SD 0.103 against a bar of 0.231).

**What each panel shows:**
- **pp mean.** Lines sit on H(p) = 1.0407 for `K ∈ [-10, -0.5]`, within −1.45% to +1.16% (all within 1.2 bars). They fan down at flat K; at `K = -0.01` they read 1.0461, 0.9232, 0.7650, 0.4638, 0.2702, 0.1915, 0.1478 for λ = 0.01..1.
- **ce mean.** Lines follow the ∝R² guide (anchor 0.11559 at `K=-10, λ=0.01`). `ce/R^2` stays within 1.1476–1.1559 for `lamR2 ≤ 1`, then reads 1.144 / 1.136 / 1.132 at 1.5 / 2 / 2.5 and 1.009 at 5. The panel spans 0.1149 (`K=-10, λ=0.25`) to 115.16 (`K=-0.01, λ=0.01`). At `K = -0.01` the λ = 1 line peels furthest below the ∝R² guide, to 14.95 (against 115.2 for λ = 0.01).
- **vce mean.** Plateau of 249.7–288.6 for `lamR2 ≤ 2.5`; the low end is the noisy `K=-0.1, λ=0.25` cell with a bar of ±80.5. It drops to 111.5 at 5 and 1.543 at 100.
- **pp variance.** Not a V. It falls roughly as `2.7/lamR2` to a floor of 12.4–17.9 on `lamR2` ≈ 0.19–0.75, where seeds agree within 1.11×.
  - Seed agreement breaks between 0.75 and 1: the 724.8 at `lamR2 = 1` is seeds 2116 / 26 / 33.
  - It then forms a hump peaking at 7904 at `lamR2 = 15` (seeds 16455 / 3632 / 3625) and falls back to 862 at 100.
- **ce variance.** Spans 0.275 (`K=-10, λ=1`) to 5.77e7 (`K=-0.01, λ=0.05`).
- **vce variance.** Falls from 3.9e9 at `lamR2 = 0.001` to about 1e8–4e8, trendless, on roughly 0.06–0.5. It peaks at 2.59e10 at 2.5 (seeds 6.65e10 / 9.45e9 / 1.85e9), then falls strictly to 2.13e5 at 100.
- **Dashed lines and footer.** Dashing and the footer's "~0.304 cliff" follow raw λ, not `lamR2`; see §10.

## 10. Caveat on the `!` flags and the dashed lines

**The flag uses raw λ, but the loss pass depends on `lamR2`.**
- **Code.** `experiments/report.py` sets `VARIANCE_CLIFF = 0.304` (line 50) and flags `rate > VARIANCE_CLIFF` (lines 154, 168). The figure script dashes `lam > VARIANCE_CLIFF` (line 193).
- **Result.** λ ∈ {0.5, 0.75, 1.0} is flagged at every K: 432 rows in the tables above, 144 per rate.
- **The flag contradicts itself.** Since the loss pass depends on `(K, λ)` only through `lamR2` (§2), any rate threshold must be written as `λ/|K|`. The flagged `K=-10, λ=1.0` cell and the unflagged `K=-1, λ=0.1` cell are the same computation (naive pp std 4.3173 / 4.3258 / 4.3204 in both).
- **How much it misclassifies.** Read as `lamR2 > 0.304`, the rule would flag 29 of the 63 `(K, λ)` cells, against 27 flagged now; the two rules disagree on 20.
  - **Flagged but `lamR2 ≤ 0.304`:** `K=-2` at 0.5; `K=-3` at 0.5 and 0.75; `K=-4` and `K=-10` at 0.5, 0.75 and 1.
  - **Unflagged but `lamR2 > 0.304`:** `K=-0.5` at 0.25; `K=-0.1` and `K=-0.05` at 0.05–0.25; `K=-0.01` at 0.01–0.25.
  - **In the figures.** On the pp variance panel, the `!` lines at `K = -10` (λ = 0.5 / 0.75 / 1) have the *lowest* variance at that K (55.1 / 37.6 / 28.9, against 2721 for λ = 0.01). On the pp mean panel, the solid λ = 0.25 line reads 0.4638 (−55.4%) at `K = -0.01`.

**The 0.304 value itself is not validated for this grid.**
- It comes from the `d = 2`, plain-`exp` `init_opt_test` project. That project's own `RESULTS.md` later withdrew the infinite-variance framing.
- In this code `u` is clamped at `1e-12`, so the implemented estimator's variance is strictly finite. The header note's "infinite variance" is literally false.
- **What the data show instead** (pp, c1e4):
  - The first heavy-tail symptom is the seed spread of the per-sample variance. It is ≤ 1.5% for `lamR2` in [0.005, 0.25]; it is 4.5–9% at `lamR2 ≤ 0.0025` (and 2.8% at 0.0033), where the variance grows as `lamR2^-1`; and it rises to 5–10% at 0.333–0.75. That is weakly consistent with an onset somewhere in 0.25–0.33 (n = 3; the std stays within 1.08× across seeds up to 0.5).
  - One seed of three blows up at `lamR2 = 1`.
  - The mean falls clearly below H, on all seeds, only between `lamR2` 2.5 and 5. naive_ps breaks earlier (1.5–2) and cmplx_ps later (5).

**No reported number depends on the flags.** They annotate only. The flag is shared code across the `*_refactor_new` projects, so the fix (flag on `λ/|K|`, and for pp only unless `ce` / `vce` thresholds are measured) is flagged here rather than made unilaterally.
