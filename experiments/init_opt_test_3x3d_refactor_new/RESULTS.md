# init_opt_test_3x3d_refactor_new results

- runs collected: **2520** / 2520 (100%) — run dirs without test_metrics.json: 0
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

## naive_ps, K = -0.01x-0.01x-0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 21.1317 / 9925 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.05 | 20.9839 / 1.1e+05 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.1 | 20.2382 / 1.77e+06 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.25 | 17.1755 / 1.394e+07 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.5 ! | 12.1332 / 1.178e+07 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.75 ! | 8.8439 / 5.77e+06 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp1.0 ! | 6.8846 / 3.187e+06 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4998 / 6.491 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.05 | 0.4973 / 102.5 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.1 | 0.4774 / 1314 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.25 | 0.4262 / 2.055e+04 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.5 ! | 0.2769 / 8422 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.75 ! | 0.1914 / 3590 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp1.0 ! | 0.1444 / 1892 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 11.8486 / 5.768e+04 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.05 | 11.2232 / 3.047e+05 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.1 | 10.2503 / 2.629e+06 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.25 | 7.6639 / 1.508e+07 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.5 ! | 4.3802 / 6.428e+06 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp0.75 ! | 2.5994 / 1.634e+06 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |
| stratified_exp1.0 ! | 1.7672 / 5.423e+05 | 0.4757 / 441.4 | 20.1057 / 4.947e+05 | 0.0087 / n/r | 0.4132 / n/r |

---

## naive_ps, K = -0.01x-10.0x-1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.0628 / 19.73 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.05 | 0.0608 / 3.796 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.1 | 0.0607 / 1.901 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.25 | 0.0606 / 0.7649 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.5 ! | 0.0608 / 0.3941 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.75 ! | 0.0608 / 0.2693 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp1.0 ! | 0.0608 / 0.207 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.5051 / 1802 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.05 | 0.4923 / 346.6 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.1 | 0.4932 / 175.5 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.25 | 0.4959 / 71.81 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.5 ! | 0.4980 / 37 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.75 ! | 0.4981 / 25.36 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp1.0 ! | 0.4986 / 19.58 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 26.8071 / 7.455e+07 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.05 | 23.8245 / 7.961e+06 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.1 | 23.2548 / 2.455e+06 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.25 | 25.1732 / 1.392e+07 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.5 ! | 24.5199 / 1.811e+06 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp0.75 ! | 24.2341 / 8.597e+05 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |
| stratified_exp1.0 ! | 24.4834 / 2.411e+06 | 0.4958 / 177.3 | 0.0605 / 1.881 | 0.0490 / n/r | 0.0060 / n/r |

---

## naive_ps, K = -0.05x-0.05x-0.05

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 4.2232 / 1372 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.05 | 4.2263 / 397 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.1 | 4.2427 / 1018 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.25 | 4.1968 / 4400 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.5 ! | 4.0476 / 7.078e+04 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.75 ! | 3.8100 / 2.282e+05 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp1.0 ! | 3.6114 / 3.976e+05 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4981 / 22.13 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.05 | 0.4998 / 6.491 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.1 | 0.5007 / 9.015 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.25 | 0.4973 / 102.5 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.5 ! | 0.4774 / 1314 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.75 ! | 0.4486 / 5977 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp1.0 ! | 0.4408 / 1.51e+04 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 11.8396 / 6.266e+04 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.05 | 11.8486 / 5.768e+04 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.1 | 11.8974 / 1.393e+05 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.25 | 11.2232 / 3.047e+05 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.5 ! | 10.2503 / 2.629e+06 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp0.75 ! | 8.8354 / 3.845e+06 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |
| stratified_exp1.0 ! | 8.3810 / 1.06e+07 | 0.4999 / 7.201 | 4.2284 / 412.1 | 0.0266 / n/r | 0.2337 / n/r |

---

## naive_ps, K = -0.1x-0.1x-0.1

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 2.1119 / 663.8 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.05 | 2.1109 / 153.1 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.1 | 2.1132 / 99.25 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.25 | 2.1165 / 182.8 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.5 ! | 2.0984 / 1100 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.75 ! | 2.0789 / 1.081e+04 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp1.0 ! | 2.0238 / 1.77e+04 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4984 / 42.8 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.05 | 0.4989 / 9.979 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.1 | 0.4998 / 6.491 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.25 | 0.5000 / 10.15 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.5 ! | 0.4973 / 102.5 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.75 ! | 0.4945 / 850.9 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp1.0 ! | 0.4774 / 1314 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 11.7367 / 6.319e+04 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.05 | 11.9809 / 2.05e+05 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.1 | 11.8486 / 5.768e+04 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.25 | 11.8340 / 2.608e+05 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.5 ! | 11.2232 / 3.047e+05 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp0.75 ! | 11.1589 / 3.843e+06 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |
| stratified_exp1.0 ! | 10.2503 / 2.629e+06 | 0.5001 / 6.517 | 2.1159 / 98.87 | 0.0349 / n/r | 0.1506 / n/r |

---

## naive_ps, K = -0.5x-0.5x-0.5

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4229 / 129.8 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.05 | 0.4224 / 26.55 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.1 | 0.4223 / 13.72 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.25 | 0.4222 / 6.123 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.5 ! | 0.4226 / 3.97 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.75 ! | 0.4232 / 4.176 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp1.0 ! | 0.4243 / 10.18 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4971 / 206.8 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.05 | 0.4984 / 42.8 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.1 | 0.4981 / 22.13 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.25 | 0.4989 / 9.979 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.5 ! | 0.4998 / 6.491 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.75 ! | 0.5004 / 6.665 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp1.0 ! | 0.5007 / 9.015 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 11.8713 / 2.945e+05 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.05 | 11.7367 / 6.319e+04 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.1 | 11.8396 / 6.266e+04 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.25 | 11.9809 / 2.05e+05 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.5 ! | 11.8486 / 5.768e+04 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp0.75 ! | 11.8512 / 5.467e+04 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |
| stratified_exp1.0 ! | 11.8974 / 1.393e+05 | 0.4996 / 22.24 | 0.4227 / 13.71 | 0.0460 / n/r | 0.0391 / n/r |

---

## naive_ps, K = -1.0x-1.0x-1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.2107 / 64.97 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.05 | 0.2112 / 13.1 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.1 | 0.2112 / 6.638 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.25 | 0.2110 / 2.787 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.5 ! | 0.2111 / 1.531 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.75 ! | 0.2111 / 1.143 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp1.0 ! | 0.2113 / 0.9925 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4892 / 405.1 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.05 | 0.4979 / 84.28 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.1 | 0.4984 / 42.8 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.25 | 0.4978 / 18.02 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.5 ! | 0.4989 / 9.979 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.75 ! | 0.4993 / 7.491 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp1.0 ! | 0.4998 / 6.491 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 12.0097 / 1.166e+06 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.05 | 11.9040 / 1.578e+05 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.1 | 11.7367 / 6.319e+04 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.25 | 11.7642 / 3.565e+04 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.5 ! | 11.9809 / 2.05e+05 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp0.75 ! | 11.7750 / 4.212e+04 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |
| stratified_exp1.0 ! | 11.8486 / 5.768e+04 | 0.4998 / 43.08 | 0.2111 / 6.614 | 0.0479 / n/r | 0.0203 / n/r |

---

## naive_ps, K = -2.0x-2.0x-2.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.1063 / 32.96 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.05 | 0.1058 / 6.525 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.1 | 0.1056 / 3.275 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.25 | 0.1056 / 1.339 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.5 ! | 0.1055 / 0.6968 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.75 ! | 0.1055 / 0.4848 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp1.0 ! | 0.1055 / 0.3827 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4947 / 817.5 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.05 | 0.4975 / 166.3 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.1 | 0.4979 / 84.28 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.25 | 0.4982 / 34.51 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.5 ! | 0.4978 / 18.02 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.75 ! | 0.4984 / 12.62 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp1.0 ! | 0.4989 / 9.979 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 12.2148 / 1.478e+06 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.05 | 11.9496 / 3.795e+05 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.1 | 11.9040 / 1.578e+05 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.25 | 11.8656 / 6.598e+04 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.5 ! | 11.7642 / 3.565e+04 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp0.75 ! | 11.7673 / 8.13e+04 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |
| stratified_exp1.0 ! | 11.9809 / 2.05e+05 | 0.4995 / 84.77 | 0.1054 / 3.253 | 0.0489 / n/r | 0.0103 / n/r |

---

## naive_ps, K = -3.0x-3.0x-3.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.0714 / 21.88 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.05 | 0.0703 / 4.313 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.1 | 0.0706 / 2.18 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.25 | 0.0703 / 0.879 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.5 ! | 0.0704 / 0.4522 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.75 ! | 0.0703 / 0.3097 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp1.0 ! | 0.0703 / 0.2388 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4993 / 1234 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.05 | 0.4956 / 246.3 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.1 | 0.4989 / 125.5 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.25 | 0.4978 / 50.99 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.5 ! | 0.4980 / 26.22 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.75 ! | 0.4978 / 18.02 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp1.0 ! | 0.4984 / 13.97 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 11.6082 / 1.012e+06 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.05 | 11.7584 / 3.081e+05 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.1 | 11.9882 / 2.063e+05 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.25 | 11.7441 / 7.448e+04 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.5 ! | 11.7720 / 4.715e+04 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp0.75 ! | 11.7642 / 3.565e+04 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |
| stratified_exp1.0 ! | 11.8978 / 7.479e+04 | 0.4997 / 126.3 | 0.0702 / 2.147 | 0.0493 / n/r | 0.0069 / n/r |

---

## naive_ps, K = -4.0x-4.0x-4.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.0540 / 16.54 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.05 | 0.0525 / 3.228 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.1 | 0.0529 / 1.631 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.25 | 0.0527 / 0.6552 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.5 ! | 0.0528 / 0.3348 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.75 ! | 0.0528 / 0.2278 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp1.0 ! | 0.0528 / 0.1742 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.5019 / 1644 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.05 | 0.4895 / 322.3 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.1 | 0.4975 / 166.3 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.25 | 0.4968 / 67.43 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.5 ! | 0.4982 / 34.51 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.75 ! | 0.4982 / 23.5 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp1.0 ! | 0.4978 / 18.02 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 11.7472 / 1.298e+06 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.05 | 11.6258 / 4.285e+05 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.1 | 11.9496 / 3.795e+05 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.25 | 11.7882 / 9.461e+04 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.5 ! | 11.8656 / 6.598e+04 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp0.75 ! | 11.8515 / 5.13e+04 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |
| stratified_exp1.0 ! | 11.7642 / 3.565e+04 | 0.4980 / 166.9 | 0.0525 / 1.603 | 0.0493 / n/r | 0.0052 / n/r |

---

## naive_ps, K = -10.0x-10.0x-10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.0222 / 6.782 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.05 | 0.0213 / 1.318 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.1 | 0.0211 / 0.6497 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.25 | 0.0212 / 0.261 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.5 ! | 0.0211 / 0.131 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.75 ! | 0.0211 / 0.0877 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp1.0 ! | 0.0211 / 0.06638 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.5160 / 4220 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.05 | 0.4947 / 817.5 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.1 | 0.4892 / 405.1 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.25 | 0.4975 / 166.3 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.5 ! | 0.4979 / 84.28 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.75 ! | 0.4976 / 56.51 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp1.0 ! | 0.4984 / 42.8 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 12.1556 / 3.544e+06 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.05 | 12.2148 / 1.478e+06 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.1 | 12.0097 / 1.166e+06 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.25 | 11.9496 / 3.795e+05 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.5 ! | 11.9040 / 1.578e+05 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp0.75 ! | 11.8031 / 8.986e+04 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |
| stratified_exp1.0 ! | 11.7367 / 6.319e+04 | 0.4910 / 407.1 | 0.0208 / 0.6289 | 0.0489 / n/r | 0.0021 / n/r |

---

## cmplx_ps, K = -0.01x-0.01x-0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 60.6778 / 1.928e+04 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.05 | 60.4242 / 3.285e+05 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.1 | 60.6027 / 6.941e+07 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.25 | 53.6787 / 1.713e+08 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.5 ! | 37.9948 / 6.628e+07 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.75 ! | 28.7552 / 3.888e+07 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp1.0 ! | 22.9859 / 2.495e+07 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6658 / 14.74 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.05 | 1.6573 / 200.8 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.1 | 1.6611 / 4.923e+04 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.25 | 1.4777 / 9.324e+04 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.5 ! | 1.0608 / 4.486e+04 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.75 ! | 0.8198 / 3.682e+04 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp1.0 ! | 0.6657 / 2.691e+04 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 31.3253 / 2.567e+05 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.05 | 30.5181 / 1.321e+06 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.1 | 28.8048 / 3.114e+07 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.25 | 20.8090 / 3.056e+07 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.5 ! | 11.5444 / 9.468e+06 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp0.75 ! | 7.6395 / 4.227e+06 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |
| stratified_exp1.0 ! | 5.5844 / 2.24e+06 | 1.6687 / 2.185e+04 | 60.2528 / 1.64e+07 | 0.0371 / n/r | 1.2954 / n/r |

---

## cmplx_ps, K = -0.01x-10.0x-1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.1703 / 38.77 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.05 | 0.1679 / 7.645 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.1 | 0.1680 / 3.844 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.25 | 0.1677 / 1.542 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.5 ! | 0.1679 / 0.7813 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.75 ! | 0.1680 / 0.5293 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp1.0 ! | 0.1679 / 0.4031 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.7111 / 4566 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.05 | 1.6719 / 880.9 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.1 | 1.6656 / 438 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.25 | 1.6638 / 175.9 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.5 ! | 1.6644 / 89.05 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.75 ! | 1.6655 / 60.27 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp1.0 ! | 1.6659 / 45.98 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 51.1814 / 9.338e+07 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.05 | 49.1785 / 7.733e+06 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.1 | 51.4128 / 2.556e+07 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.25 | 50.8096 / 5.274e+06 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.5 ! | 51.3162 / 5.961e+06 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp0.75 ! | 50.5109 / 1.692e+06 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |
| stratified_exp1.0 ! | 50.5676 / 2.624e+06 | 1.6678 / 437.2 | 0.1680 / 3.831 | 0.1651 / n/r | 0.0166 / n/r |

---

## cmplx_ps, K = -0.05x-0.05x-0.05

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 12.1493 / 2796 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.05 | 12.1356 / 771.4 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.1 | 12.1535 / 1704 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.25 | 12.0848 / 1.314e+04 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.5 ! | 12.1205 / 2.776e+06 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.75 ! | 12.1873 / 1.138e+07 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp1.0 ! | 11.5513 / 9.525e+06 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6663 / 54.74 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.05 | 1.6658 / 14.74 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.1 | 1.6669 / 22.6 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.25 | 1.6573 / 200.8 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.5 ! | 1.6611 / 4.923e+04 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.75 ! | 1.7216 / 3.262e+05 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp1.0 ! | 1.6006 / 1.774e+05 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 31.4751 / 1.877e+05 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.05 | 31.3253 / 2.567e+05 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.1 | 32.4939 / 1.436e+07 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.25 | 30.5181 / 1.321e+06 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.5 ! | 28.8048 / 3.114e+07 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp0.75 ! | 27.2940 / 7.303e+07 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |
| stratified_exp1.0 ! | 24.4535 / 5.779e+07 | 1.6650 / 16.27 | 12.1371 / 888.1 | 0.0970 / n/r | 0.6949 / n/r |

---

## cmplx_ps, K = -0.1x-0.1x-0.1

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 6.0809 / 1375 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.05 | 6.0675 / 298.9 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.1 | 6.0678 / 192.8 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.25 | 6.0756 / 630.9 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.5 ! | 6.0424 / 3285 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.75 ! | 5.9926 / 2.867e+04 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp1.0 ! | 6.0603 / 6.941e+05 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6666 / 107.8 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.05 | 1.6658 / 23.4 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.1 | 1.6658 / 14.74 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.25 | 1.6659 / 28.69 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.5 ! | 1.6573 / 200.8 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.75 ! | 1.6395 / 1309 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp1.0 ! | 1.6611 / 4.923e+04 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 31.2930 / 1.63e+05 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.05 | 31.4391 / 5.588e+05 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.1 | 31.3253 / 2.567e+05 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.25 | 31.4033 / 3.996e+06 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.5 ! | 30.5181 / 1.321e+06 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp0.75 ! | 29.3516 / 4.699e+06 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |
| stratified_exp1.0 ! | 28.8048 / 3.114e+07 | 1.6652 / 14.28 | 6.0681 / 185.5 | 0.1224 / n/r | 0.4412 / n/r |

---

## cmplx_ps, K = -0.5x-0.5x-0.5

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.2158 / 272.1 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.05 | 1.2162 / 54.99 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.1 | 1.2149 / 27.96 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.25 | 1.2135 / 11.96 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.5 ! | 1.2136 / 7.714 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.75 ! | 1.2141 / 8.634 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp1.0 ! | 1.2154 / 17.04 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6673 / 535.1 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.05 | 1.6666 / 107.8 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.1 | 1.6663 / 54.74 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.25 | 1.6658 / 23.4 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.5 ! | 1.6658 / 14.74 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.75 ! | 1.6667 / 15.35 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp1.0 ! | 1.6669 / 22.6 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 31.5428 / 8.634e+05 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.05 | 31.2930 / 1.63e+05 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.1 | 31.4751 / 1.877e+05 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.25 | 31.4391 / 5.588e+05 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.5 ! | 31.3253 / 2.567e+05 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp0.75 ! | 31.1841 / 9.435e+04 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |
| stratified_exp1.0 ! | 32.4939 / 1.436e+07 | 1.6652 / 54.7 | 1.2125 / 27.78 | 0.1552 / n/r | 0.1127 / n/r |

---

## cmplx_ps, K = -1.0x-1.0x-1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.6091 / 136.9 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.05 | 0.6083 / 27.28 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.1 | 0.6081 / 13.75 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.25 | 0.6074 / 5.639 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.5 ! | 0.6068 / 2.989 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.75 ! | 0.6066 / 2.181 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp1.0 ! | 0.6068 / 1.928 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6685 / 1071 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.05 | 1.6683 / 214.3 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.1 | 1.6666 / 107.8 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.25 | 1.6669 / 44.22 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.5 ! | 1.6658 / 23.4 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.75 ! | 1.6658 / 16.94 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp1.0 ! | 1.6658 / 14.74 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 31.0122 / 1.166e+06 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.05 | 31.0798 / 2.623e+05 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.1 | 31.2930 / 1.63e+05 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.25 | 31.3265 / 1.293e+05 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.5 ! | 31.4391 / 5.588e+05 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp0.75 ! | 31.1973 / 7.508e+04 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |
| stratified_exp1.0 ! | 31.3253 / 2.567e+05 | 1.6632 / 107.4 | 0.6058 / 13.65 | 0.1605 / n/r | 0.0584 / n/r |

---

## cmplx_ps, K = -2.0x-2.0x-2.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.3068 / 69.6 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.05 | 0.3040 / 13.58 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.1 | 0.3042 / 6.821 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.25 | 0.3038 / 2.759 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.5 ! | 0.3037 / 1.41 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.75 ! | 0.3034 / 0.9641 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp1.0 ! | 0.3034 / 0.7473 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6839 / 2182 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.05 | 1.6687 / 428.6 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.1 | 1.6683 / 214.3 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.25 | 1.6655 / 86.5 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.5 ! | 1.6669 / 44.22 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.75 ! | 1.6654 / 30.22 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp1.0 ! | 1.6658 / 23.4 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 32.6155 / 5.519e+06 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.05 | 31.4465 / 5.417e+05 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.1 | 31.0798 / 2.623e+05 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.25 | 31.1700 / 1.251e+05 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.5 ! | 31.3265 / 1.293e+05 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp0.75 ! | 31.0981 / 8.154e+04 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |
| stratified_exp1.0 ! | 31.4391 / 5.588e+05 | 1.6638 / 213.8 | 0.3032 / 6.807 | 0.1634 / n/r | 0.0298 / n/r |

---

## cmplx_ps, K = -3.0x-3.0x-3.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.2050 / 46.75 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.05 | 0.2026 / 9.069 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.1 | 0.2028 / 4.534 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.25 | 0.2028 / 1.829 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.5 ! | 0.2025 / 0.9261 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.75 ! | 0.2025 / 0.6265 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp1.0 ! | 0.2024 / 0.4777 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6879 / 3287 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.05 | 1.6670 / 640.9 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.1 | 1.6700 / 321.6 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.25 | 1.6672 / 129.1 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.5 ! | 1.6659 / 65.3 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.75 ! | 1.6669 / 44.22 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp1.0 ! | 1.6663 / 33.73 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 31.7537 / 3.897e+06 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.05 | 31.1451 / 6.731e+05 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.1 | 31.6322 / 5.793e+05 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.25 | 31.2548 / 1.887e+05 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.5 ! | 31.1869 / 1.005e+05 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp0.75 ! | 31.3265 / 1.293e+05 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |
| stratified_exp1.0 ! | 31.2535 / 1.515e+05 | 1.6623 / 319.1 | 0.2021 / 4.526 | 0.1642 / n/r | 0.0200 / n/r |

---

## cmplx_ps, K = -4.0x-4.0x-4.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.1543 / 35.21 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.05 | 0.1521 / 6.825 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.1 | 0.1520 / 3.395 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.25 | 0.1521 / 1.367 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.5 ! | 0.1519 / 0.6897 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.75 ! | 0.1519 / 0.4648 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp1.0 ! | 0.1519 / 0.3524 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.6953 / 4424 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.05 | 1.6677 / 855.1 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.1 | 1.6687 / 428.6 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.25 | 1.6676 / 171.6 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.5 ! | 1.6655 / 86.5 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.75 ! | 1.6662 / 58.26 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp1.0 ! | 1.6669 / 44.22 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 32.2009 / 8.636e+06 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.05 | 31.3262 / 1.395e+06 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.1 | 31.4465 / 5.417e+05 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.25 | 31.2810 / 3.567e+05 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.5 ! | 31.1700 / 1.251e+05 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp0.75 ! | 31.2752 / 1.022e+05 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |
| stratified_exp1.0 ! | 31.3265 / 1.293e+05 | 1.6629 / 426.1 | 0.1516 / 3.396 | 0.1648 / n/r | 0.0150 / n/r |

---

## cmplx_ps, K = -10.0x-10.0x-10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.0621 / 13.92 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.05 | 0.0614 / 2.784 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.1 | 0.0609 / 1.369 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.25 | 0.0608 / 0.5432 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.5 ! | 0.0608 / 0.2728 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.75 ! | 0.0608 / 0.1827 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp1.0 ! | 0.0608 / 0.1375 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.7222 / 1.12e+04 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.05 | 1.6839 / 2182 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.1 | 1.6685 / 1071 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.25 | 1.6687 / 428.6 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.5 ! | 1.6683 / 214.3 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.75 ! | 1.6674 / 143.2 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp1.0 ! | 1.6666 / 107.8 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 31.9188 / 8.521e+06 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.05 | 32.6155 / 5.519e+06 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.1 | 31.0122 / 1.166e+06 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.25 | 31.4465 / 5.417e+05 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.5 ! | 31.0798 / 2.623e+05 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp0.75 ! | 31.2928 / 2.391e+05 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |
| stratified_exp1.0 ! | 31.2930 / 1.63e+05 | 1.6520 / 1050 | 0.0603 / 1.345 | 0.1646 / n/r | 0.0060 / n/r |

---

## c1e3_exp1.0, K = -0.01x-0.01x-0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 41.0422 / 1.291e+04 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.05 | 41.1284 / 4.438e+05 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.1 | 41.9052 / 2.991e+07 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.25 | 35.8110 / 6.603e+07 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.5 ! | 25.2379 / 6.419e+07 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.75 ! | 18.4590 / 2.736e+07 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp1.0 ! | 14.4462 / 1.351e+07 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0401 / 9.297 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.05 | 1.0512 / 906.9 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.1 | 1.0731 / 3.372e+04 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.25 | 0.9079 / 5.517e+04 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.5 ! | 0.6284 / 5.729e+04 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.75 ! | 0.4514 / 2.166e+04 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp1.0 ! | 0.3504 / 1.061e+04 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 54.5363 / 6.349e+05 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.05 | 54.1832 / 2.3e+07 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.1 | 50.7077 / 6.066e+08 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.25 | 30.2960 / 4.621e+08 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.5 ! | 13.3262 / 1.021e+08 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.75 ! | 7.1516 / 1.673e+07 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp1.0 ! | 4.6832 / 4.815e+06 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |

---

## c1e3_exp1.0, K = -0.01x-10.0x-1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.1245 / 24.99 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.05 | 0.1220 / 4.796 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.1 | 0.1221 / 2.416 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.25 | 0.1221 / 0.971 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.5 ! | 0.1223 / 0.4955 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.75 ! | 0.1222 / 0.336 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp1.0 ! | 0.1223 / 0.2575 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0543 / 2692 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.05 | 1.0346 / 529.9 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.1 | 1.0373 / 266.3 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.25 | 1.0381 / 107.4 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.5 ! | 1.0394 / 55.07 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.75 ! | 1.0397 / 37.65 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp1.0 ! | 1.0402 / 28.98 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 174.3016 / 9.401e+08 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.05 | 178.6200 / 3.953e+09 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.1 | 162.9073 / 1.155e+08 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.25 | 164.2966 / 3.033e+07 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.5 ! | 164.1617 / 1.69e+07 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.75 ! | 164.0229 / 1.712e+07 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp1.0 ! | 163.9012 / 1.323e+07 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |

---

## c1e3_exp1.0, K = -0.05x-0.05x-0.05

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 8.2134 / 1797 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.05 | 8.2084 / 516.2 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.1 | 8.2190 / 1439 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.25 | 8.2257 / 1.775e+04 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.5 ! | 8.3810 / 1.196e+06 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.75 ! | 8.0968 / 2.895e+06 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp1.0 ! | 7.6078 / 2.486e+06 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0408 / 32.25 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.05 | 1.0401 / 9.297 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.1 | 1.0409 / 12.91 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.25 | 1.0512 / 906.9 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.5 ! | 1.0731 / 3.372e+04 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.75 ! | 1.0302 / 4.927e+04 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp1.0 ! | 0.9642 / 4.108e+04 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 55.0771 / 8.036e+05 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.05 | 54.5363 / 6.349e+05 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.1 | 55.2744 / 6.193e+06 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.25 | 54.1832 / 2.3e+07 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.5 ! | 50.7077 / 6.066e+08 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.75 ! | 39.3770 / 2.431e+08 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp1.0 ! | 33.7184 / 2.15e+08 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |

---

## c1e3_exp1.0, K = -0.1x-0.1x-0.1

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 4.1074 / 875 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.05 | 4.1070 / 199.4 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.1 | 4.1042 / 129.1 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.25 | 4.1069 / 331.5 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.5 ! | 4.1128 / 4438 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.75 ! | 4.1213 / 3.739e+04 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp1.0 ! | 4.1905 / 2.991e+05 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0411 / 62.77 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.05 | 1.0413 / 14.4 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.1 | 1.0401 / 9.297 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.25 | 1.0405 / 22.93 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.5 ! | 1.0512 / 906.9 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.75 ! | 1.0486 / 3695 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp1.0 ! | 1.0731 / 3.372e+04 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 54.2932 / 9.621e+05 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.05 | 54.7856 / 7.973e+05 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.1 | 54.5363 / 6.349e+05 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.25 | 55.7798 / 7.492e+06 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.5 ! | 54.1832 / 2.3e+07 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.75 ! | 53.4978 / 2.482e+08 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp1.0 ! | 50.7077 / 6.066e+08 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |

---

## c1e3_exp1.0, K = -0.5x-0.5x-0.5

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.8188 / 171.6 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.05 | 0.8215 / 35 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.1 | 0.8213 / 17.97 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.25 | 0.8214 / 7.974 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.5 ! | 0.8208 / 5.162 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.75 ! | 0.8210 / 5.125 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp1.0 ! | 0.8219 / 14.39 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0359 / 306.8 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.05 | 1.0411 / 62.77 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.1 | 1.0408 / 32.25 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.25 | 1.0413 / 14.4 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.5 ! | 1.0401 / 9.297 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.75 ! | 1.0405 / 9.109 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp1.0 ! | 1.0409 / 12.91 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 54.4676 / 4.327e+06 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.05 | 54.2932 / 9.621e+05 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.1 | 55.0771 / 8.036e+05 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.25 | 54.7856 / 7.973e+05 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.5 ! | 54.5363 / 6.349e+05 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.75 ! | 54.7637 / 8.215e+05 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp1.0 ! | 55.2744 / 6.193e+06 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |

---

## c1e3_exp1.0, K = -1.0x-1.0x-1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4119 / 87.96 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.05 | 0.4105 / 17.33 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.1 | 0.4107 / 8.75 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.25 | 0.4109 / 3.651 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.5 ! | 0.4107 / 1.994 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.75 ! | 0.4106 / 1.484 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp1.0 ! | 0.4104 / 1.291 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0394 / 623.1 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.05 | 1.0407 / 124.2 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.1 | 1.0411 / 62.77 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.25 | 1.0419 / 26.26 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.5 ! | 1.0413 / 14.4 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.75 ! | 1.0411 / 10.73 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp1.0 ! | 1.0401 / 9.297 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 55.5304 / 1.013e+07 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.05 | 54.5899 / 2.026e+06 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.1 | 54.2932 / 9.621e+05 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.25 | 55.1326 / 1.18e+06 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.5 ! | 54.7856 / 7.973e+05 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.75 ! | 54.6072 / 4.302e+05 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp1.0 ! | 54.5363 / 6.349e+05 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |

---

## c1e3_exp1.0, K = -2.0x-2.0x-2.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.2087 / 44.81 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.05 | 0.2047 / 8.577 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.1 | 0.2052 / 4.332 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.25 | 0.2053 / 1.76 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.5 ! | 0.2054 / 0.9129 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.75 ! | 0.2054 / 0.6345 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp1.0 ! | 0.2054 / 0.4984 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0579 / 1276 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.05 | 1.0366 / 245.5 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.1 | 1.0407 / 124.2 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.25 | 1.0410 / 50.51 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.5 ! | 1.0419 / 26.26 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.75 ! | 1.0419 / 18.29 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp1.0 ! | 1.0413 / 14.4 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 56.8424 / 2.342e+07 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.05 | 54.1177 / 3.037e+06 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.1 | 54.5899 / 2.026e+06 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.25 | 54.4563 / 7.993e+05 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.5 ! | 55.1326 / 1.18e+06 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.75 ! | 54.7343 / 4.317e+05 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp1.0 ! | 54.7856 / 7.973e+05 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |

---

## c1e3_exp1.0, K = -3.0x-3.0x-3.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.1394 / 29.9 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.05 | 0.1364 / 5.724 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.1 | 0.1367 / 2.866 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.25 | 0.1370 / 1.163 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.5 ! | 0.1369 / 0.5929 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.75 ! | 0.1370 / 0.4057 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp1.0 ! | 0.1370 / 0.3127 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0582 / 1896 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.05 | 1.0339 / 367.4 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.1 | 1.0400 / 185 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.25 | 1.0415 / 75.06 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.5 ! | 1.0408 / 38.33 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.75 ! | 1.0419 / 26.26 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp1.0 ! | 1.0422 / 20.28 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 56.8072 / 2.123e+07 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.05 | 54.4747 / 5.909e+06 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.1 | 54.3740 / 2.164e+06 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.25 | 54.7428 / 1.389e+06 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.5 ! | 54.5061 / 6.274e+05 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.75 ! | 55.1326 / 1.18e+06 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp1.0 ! | 55.0902 / 5.611e+05 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |

---

## c1e3_exp1.0, K = -4.0x-4.0x-4.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.1048 / 22.56 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.05 | 0.1026 / 4.342 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.1 | 0.1024 / 2.144 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.25 | 0.1026 / 0.8667 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.5 ! | 0.1027 / 0.44 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.75 ! | 0.1027 / 0.2984 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp1.0 ! | 0.1027 / 0.2282 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0516 / 2504 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.05 | 1.0354 / 493.7 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.1 | 1.0366 / 245.5 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.25 | 1.0406 / 99.54 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.5 ! | 1.0410 / 50.51 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.75 ! | 1.0407 / 34.28 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp1.0 ! | 1.0419 / 26.26 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 62.9961 / 1.516e+08 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.05 | 54.7479 / 7.407e+06 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.1 | 54.1177 / 3.037e+06 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.25 | 54.6063 / 2.519e+06 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.5 ! | 54.4563 / 7.993e+05 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.75 ! | 54.7519 / 6.593e+05 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp1.0 ! | 55.1326 / 1.18e+06 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |

---

## c1e3_exp1.0, K = -10.0x-10.0x-10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.0429 / 9.207 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.05 | 0.0417 / 1.792 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.1 | 0.0412 / 0.8796 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.25 | 0.0409 / 0.3431 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.5 ! | 0.0410 / 0.1733 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.75 ! | 0.0411 / 0.1161 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp1.0 ! | 0.0411 / 0.0875 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0749 / 6447 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.05 | 1.0579 / 1276 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.1 | 1.0394 / 623.1 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.25 | 1.0366 / 245.5 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.5 ! | 1.0407 / 124.2 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.75 ! | 1.0412 / 83.24 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp1.0 ! | 1.0411 / 62.77 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 57.2248 / 6.417e+07 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.05 | 56.8424 / 2.342e+07 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.1 | 55.5304 / 1.013e+07 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.25 | 54.1177 / 3.037e+06 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.5 ! | 54.5899 / 2.026e+06 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.75 ! | 54.6252 / 1.695e+06 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp1.0 ! | 54.2932 / 9.621e+05 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |

---

## c1e4_exp1.0, K = -0.01x-0.01x-0.01

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 41.0422 / 1.291e+04 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.05 | 41.1284 / 4.438e+05 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.1 | 41.9052 / 2.991e+07 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.25 | 35.8110 / 6.603e+07 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.5 ! | 25.2379 / 6.419e+07 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.75 ! | 18.4590 / 2.736e+07 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp1.0 ! | 14.4462 / 1.351e+07 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0401 / 9.297 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.05 | 1.0512 / 906.9 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.1 | 1.0731 / 3.372e+04 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.25 | 0.9079 / 5.517e+04 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.5 ! | 0.6284 / 5.729e+04 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.75 ! | 0.4514 / 2.166e+04 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp1.0 ! | 0.3504 / 1.061e+04 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 65.3062 / 5.816e+06 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.05 | 61.7609 / 3.876e+07 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.1 | 55.2801 / 7.826e+08 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.25 | 31.0488 / 4.948e+08 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.5 ! | 13.4738 / 1.049e+08 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp0.75 ! | 7.2157 / 1.728e+07 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |
| stratified_exp1.0 ! | 4.7028 / 4.844e+06 | 1.0023 / 1991 | 39.4829 / 2.507e+06 | 0.0207 / n/r | 0.8334 / n/r |

---

## c1e4_exp1.0, K = -0.01x-10.0x-1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.1245 / 24.99 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.05 | 0.1220 / 4.796 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.1 | 0.1221 / 2.416 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.25 | 0.1221 / 0.971 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.5 ! | 0.1223 / 0.4955 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.75 ! | 0.1222 / 0.336 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp1.0 ! | 0.1223 / 0.2575 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0543 / 2692 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.05 | 1.0346 / 529.9 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.1 | 1.0373 / 266.3 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.25 | 1.0381 / 107.4 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.5 ! | 1.0394 / 55.07 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.75 ! | 1.0397 / 37.65 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp1.0 ! | 1.0402 / 28.98 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 300.7153 / 5.196e+09 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.05 | 271.1079 / 4.942e+09 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.1 | 266.9461 / 9.766e+08 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.25 | 258.2893 / 1.545e+08 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.5 ! | 268.8989 / 3.38e+08 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp0.75 ! | 266.6036 / 1.332e+08 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |
| stratified_exp1.0 ! | 264.3056 / 1.677e+08 | 1.0327 / 262.6 | 0.1215 / 2.361 | 0.1021 / n/r | 0.0120 / n/r |

---

## c1e4_exp1.0, K = -0.05x-0.05x-0.05

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 8.2134 / 1797 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.05 | 8.2084 / 516.2 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.1 | 8.2190 / 1439 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.25 | 8.2257 / 1.775e+04 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.5 ! | 8.3810 / 1.196e+06 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.75 ! | 8.0968 / 2.895e+06 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp1.0 ! | 7.6078 / 2.486e+06 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0408 / 32.25 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.05 | 1.0401 / 9.297 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.1 | 1.0409 / 12.91 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.25 | 1.0512 / 906.9 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.5 ! | 1.0731 / 3.372e+04 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.75 ! | 1.0302 / 4.927e+04 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp1.0 ! | 0.9642 / 4.108e+04 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 65.0460 / 1.982e+06 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.05 | 65.3062 / 5.816e+06 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.1 | 66.8326 / 8.261e+07 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.25 | 61.7609 / 3.876e+07 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.5 ! | 55.2801 / 7.826e+08 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp0.75 ! | 41.1033 / 2.582e+08 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |
| stratified_exp1.0 ! | 35.3120 / 2.65e+08 | 1.0401 / 11.99 | 8.1960 / 672 | 0.0580 / n/r | 0.4599 / n/r |

---

## c1e4_exp1.0, K = -0.1x-0.1x-0.1

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 4.1074 / 875 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.05 | 4.1070 / 199.4 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.1 | 4.1042 / 129.1 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.25 | 4.1069 / 331.5 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.5 ! | 4.1128 / 4438 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.75 ! | 4.1213 / 3.739e+04 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp1.0 ! | 4.1905 / 2.991e+05 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0411 / 62.77 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.05 | 1.0413 / 14.4 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.1 | 1.0401 / 9.297 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.25 | 1.0405 / 22.93 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.5 ! | 1.0512 / 906.9 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.75 ! | 1.0486 / 3695 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp1.0 ! | 1.0731 / 3.372e+04 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 64.1629 / 2.565e+06 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.05 | 65.0901 / 1.936e+06 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.1 | 65.3062 / 5.816e+06 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.25 | 67.8918 / 3.985e+07 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.5 ! | 61.7609 / 3.876e+07 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp0.75 ! | 60.3452 / 4.564e+08 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |
| stratified_exp1.0 ! | 55.2801 / 7.826e+08 | 1.0396 / 9.315 | 4.0999 / 129.5 | 0.0745 / n/r | 0.2945 / n/r |

---

## c1e4_exp1.0, K = -0.5x-0.5x-0.5

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.8188 / 171.6 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.05 | 0.8215 / 35 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.1 | 0.8213 / 17.97 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.25 | 0.8214 / 7.974 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.5 ! | 0.8208 / 5.162 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.75 ! | 0.8210 / 5.125 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp1.0 ! | 0.8219 / 14.39 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0359 / 306.8 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.05 | 1.0411 / 62.77 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.1 | 1.0408 / 32.25 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.25 | 1.0413 / 14.4 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.5 ! | 1.0401 / 9.297 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.75 ! | 1.0405 / 9.109 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp1.0 ! | 1.0409 / 12.91 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 64.8806 / 1.143e+07 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.05 | 64.1629 / 2.565e+06 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.1 | 65.0460 / 1.982e+06 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.25 | 65.0901 / 1.936e+06 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.5 ! | 65.3062 / 5.816e+06 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp0.75 ! | 64.6816 / 2.455e+06 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |
| stratified_exp1.0 ! | 66.8326 / 8.261e+07 | 1.0401 / 32.24 | 0.8198 / 17.91 | 0.0964 / n/r | 0.0760 / n/r |

---

## c1e4_exp1.0, K = -1.0x-1.0x-1.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.4119 / 87.96 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.05 | 0.4105 / 17.33 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.1 | 0.4107 / 8.75 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.25 | 0.4109 / 3.651 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.5 ! | 0.4107 / 1.994 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.75 ! | 0.4106 / 1.484 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp1.0 ! | 0.4104 / 1.291 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0394 / 623.1 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.05 | 1.0407 / 124.2 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.1 | 1.0411 / 62.77 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.25 | 1.0419 / 26.26 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.5 ! | 1.0413 / 14.4 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.75 ! | 1.0411 / 10.73 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp1.0 ! | 1.0401 / 9.297 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 65.0218 / 2.43e+07 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.05 | 64.4412 / 5.3e+06 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.1 | 64.1629 / 2.565e+06 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.25 | 65.3326 / 2.455e+06 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.5 ! | 65.0901 / 1.936e+06 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp0.75 ! | 64.3148 / 1.226e+06 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |
| stratified_exp1.0 ! | 65.3062 / 5.816e+06 | 1.0360 / 62.19 | 0.4087 / 8.666 | 0.0997 / n/r | 0.0393 / n/r |

---

## c1e4_exp1.0, K = -2.0x-2.0x-2.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.2087 / 44.81 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.05 | 0.2047 / 8.577 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.1 | 0.2052 / 4.332 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.25 | 0.2053 / 1.76 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.5 ! | 0.2054 / 0.9129 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.75 ! | 0.2054 / 0.6345 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp1.0 ! | 0.2054 / 0.4984 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0579 / 1276 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.05 | 1.0366 / 245.5 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.1 | 1.0407 / 124.2 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.25 | 1.0410 / 50.51 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.5 ! | 1.0419 / 26.26 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.75 ! | 1.0419 / 18.29 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp1.0 ! | 1.0413 / 14.4 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 68.6324 / 6.228e+07 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.05 | 63.5311 / 7.053e+06 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.1 | 64.4412 / 5.3e+06 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.25 | 64.6906 / 2.438e+06 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.5 ! | 65.3326 / 2.455e+06 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp0.75 ! | 65.8578 / 2.861e+06 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |
| stratified_exp1.0 ! | 65.0901 / 1.936e+06 | 1.0356 / 123 | 0.2043 / 4.292 | 0.1016 / n/r | 0.0200 / n/r |

---

## c1e4_exp1.0, K = -3.0x-3.0x-3.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.1394 / 29.9 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.05 | 0.1364 / 5.724 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.1 | 0.1367 / 2.866 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.25 | 0.1370 / 1.163 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.5 ! | 0.1369 / 0.5929 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.75 ! | 0.1370 / 0.4057 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp1.0 ! | 0.1370 / 0.3127 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0582 / 1896 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.05 | 1.0339 / 367.4 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.1 | 1.0400 / 185 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.25 | 1.0415 / 75.06 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.5 ! | 1.0408 / 38.33 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.75 ! | 1.0419 / 26.26 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp1.0 ! | 1.0422 / 20.28 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 67.7377 / 5.969e+07 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.05 | 64.4570 / 1.241e+07 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.1 | 64.0581 / 5.23e+06 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.25 | 64.6988 / 4.045e+06 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.5 ! | 64.4442 / 1.645e+06 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp0.75 ! | 65.3326 / 2.455e+06 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |
| stratified_exp1.0 ! | 65.5344 / 1.73e+06 | 1.0326 / 182.8 | 0.1358 / 2.835 | 0.1019 / n/r | 0.0134 / n/r |

---

## c1e4_exp1.0, K = -4.0x-4.0x-4.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.1048 / 22.56 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.05 | 0.1026 / 4.342 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.1 | 0.1024 / 2.144 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.25 | 0.1026 / 0.8667 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.5 ! | 0.1027 / 0.44 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.75 ! | 0.1027 / 0.2984 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp1.0 ! | 0.1027 / 0.2282 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0516 / 2504 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.05 | 1.0354 / 493.7 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.1 | 1.0366 / 245.5 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.25 | 1.0406 / 99.54 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.5 ! | 1.0410 / 50.51 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.75 ! | 1.0407 / 34.28 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp1.0 ! | 1.0419 / 26.26 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 73.1289 / 1.992e+08 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.05 | 64.1049 / 1.55e+07 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.1 | 63.5311 / 7.053e+06 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.25 | 64.7189 / 6.335e+06 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.5 ! | 64.6906 / 2.438e+06 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp0.75 ! | 64.8578 / 1.874e+06 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |
| stratified_exp1.0 ! | 65.3326 / 2.455e+06 | 1.0316 / 242.8 | 0.1018 / 2.114 | 0.1021 / n/r | 0.0101 / n/r |

---

## c1e4_exp1.0, K = -10.0x-10.0x-10.0

Each cell: point-estimate mean / per-sample variance, averaged across 3 seeds

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 0.0429 / 9.207 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.05 | 0.0417 / 1.792 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.1 | 0.0412 / 0.8796 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.25 | 0.0409 / 0.3431 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.5 ! | 0.0410 / 0.1733 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.75 ! | 0.0411 / 0.1161 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp1.0 ! | 0.0411 / 0.0875 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 1.0749 / 6447 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.05 | 1.0579 / 1276 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.1 | 1.0394 / 623.1 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.25 | 1.0366 / 245.5 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.5 ! | 1.0407 / 124.2 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.75 ! | 1.0412 / 83.24 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp1.0 ! | 1.0411 / 62.77 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |

**Variational CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| stratified_exp0.01 | 66.3860 / 1.15e+08 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.05 | 68.6324 / 6.228e+07 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.1 | 65.0218 / 2.43e+07 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.25 | 63.5311 / 7.053e+06 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.5 ! | 64.4412 / 5.3e+06 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp0.75 ! | 65.2787 / 6.139e+06 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |
| stratified_exp1.0 ! | 64.1629 / 2.565e+06 | 1.0216 / 593.3 | 0.0404 / 0.8255 | 0.1018 / n/r | 0.0040 / n/r |

---

# RESULTS (Dense Table)

---

## naive_ps, K = -0.01x-0.01x-0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.4998 / 6.491 | 21.1317 / 9925 | 11.8486 / 5.768e+04 |
| stratified_exp0.05 | 0.4973 / 102.5 | 20.9839 / 1.1e+05 | 11.2232 / 3.047e+05 |
| stratified_exp0.1 | 0.4774 / 1314 | 20.2382 / 1.77e+06 | 10.2503 / 2.629e+06 |
| stratified_exp0.25 | 0.4262 / 2.055e+04 | 17.1755 / 1.394e+07 | 7.6639 / 1.508e+07 |
| stratified_exp0.5 ! | 0.2769 / 8422 | 12.1332 / 1.178e+07 | 4.3802 / 6.428e+06 |
| stratified_exp0.75 ! | 0.1914 / 3590 | 8.8439 / 5.77e+06 | 2.5994 / 1.634e+06 |
| stratified_exp1.0 ! | 0.1444 / 1892 | 6.8846 / 3.187e+06 | 1.7672 / 5.423e+05 |

---

## naive_ps, K = -0.01x-10.0x-1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.5051 / 1802 | 0.0628 / 19.73 | 26.8071 / 7.455e+07 |
| stratified_exp0.05 | 0.4923 / 346.6 | 0.0608 / 3.796 | 23.8245 / 7.961e+06 |
| stratified_exp0.1 | 0.4932 / 175.5 | 0.0607 / 1.901 | 23.2548 / 2.455e+06 |
| stratified_exp0.25 | 0.4959 / 71.81 | 0.0606 / 0.7649 | 25.1732 / 1.392e+07 |
| stratified_exp0.5 ! | 0.4980 / 37 | 0.0608 / 0.3941 | 24.5199 / 1.811e+06 |
| stratified_exp0.75 ! | 0.4981 / 25.36 | 0.0608 / 0.2693 | 24.2341 / 8.597e+05 |
| stratified_exp1.0 ! | 0.4986 / 19.58 | 0.0608 / 0.207 | 24.4834 / 2.411e+06 |

---

## naive_ps, K = -0.05x-0.05x-0.05

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.4981 / 22.13 | 4.2232 / 1372 | 11.8396 / 6.266e+04 |
| stratified_exp0.05 | 0.4998 / 6.491 | 4.2263 / 397 | 11.8486 / 5.768e+04 |
| stratified_exp0.1 | 0.5007 / 9.015 | 4.2427 / 1018 | 11.8974 / 1.393e+05 |
| stratified_exp0.25 | 0.4973 / 102.5 | 4.1968 / 4400 | 11.2232 / 3.047e+05 |
| stratified_exp0.5 ! | 0.4774 / 1314 | 4.0476 / 7.078e+04 | 10.2503 / 2.629e+06 |
| stratified_exp0.75 ! | 0.4486 / 5977 | 3.8100 / 2.282e+05 | 8.8354 / 3.845e+06 |
| stratified_exp1.0 ! | 0.4408 / 1.51e+04 | 3.6114 / 3.976e+05 | 8.3810 / 1.06e+07 |

---

## naive_ps, K = -0.1x-0.1x-0.1

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.4984 / 42.8 | 2.1119 / 663.8 | 11.7367 / 6.319e+04 |
| stratified_exp0.05 | 0.4989 / 9.979 | 2.1109 / 153.1 | 11.9809 / 2.05e+05 |
| stratified_exp0.1 | 0.4998 / 6.491 | 2.1132 / 99.25 | 11.8486 / 5.768e+04 |
| stratified_exp0.25 | 0.5000 / 10.15 | 2.1165 / 182.8 | 11.8340 / 2.608e+05 |
| stratified_exp0.5 ! | 0.4973 / 102.5 | 2.0984 / 1100 | 11.2232 / 3.047e+05 |
| stratified_exp0.75 ! | 0.4945 / 850.9 | 2.0789 / 1.081e+04 | 11.1589 / 3.843e+06 |
| stratified_exp1.0 ! | 0.4774 / 1314 | 2.0238 / 1.77e+04 | 10.2503 / 2.629e+06 |

---

## naive_ps, K = -0.5x-0.5x-0.5

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.4971 / 206.8 | 0.4229 / 129.8 | 11.8713 / 2.945e+05 |
| stratified_exp0.05 | 0.4984 / 42.8 | 0.4224 / 26.55 | 11.7367 / 6.319e+04 |
| stratified_exp0.1 | 0.4981 / 22.13 | 0.4223 / 13.72 | 11.8396 / 6.266e+04 |
| stratified_exp0.25 | 0.4989 / 9.979 | 0.4222 / 6.123 | 11.9809 / 2.05e+05 |
| stratified_exp0.5 ! | 0.4998 / 6.491 | 0.4226 / 3.97 | 11.8486 / 5.768e+04 |
| stratified_exp0.75 ! | 0.5004 / 6.665 | 0.4232 / 4.176 | 11.8512 / 5.467e+04 |
| stratified_exp1.0 ! | 0.5007 / 9.015 | 0.4243 / 10.18 | 11.8974 / 1.393e+05 |

---

## naive_ps, K = -1.0x-1.0x-1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.4892 / 405.1 | 0.2107 / 64.97 | 12.0097 / 1.166e+06 |
| stratified_exp0.05 | 0.4979 / 84.28 | 0.2112 / 13.1 | 11.9040 / 1.578e+05 |
| stratified_exp0.1 | 0.4984 / 42.8 | 0.2112 / 6.638 | 11.7367 / 6.319e+04 |
| stratified_exp0.25 | 0.4978 / 18.02 | 0.2110 / 2.787 | 11.7642 / 3.565e+04 |
| stratified_exp0.5 ! | 0.4989 / 9.979 | 0.2111 / 1.531 | 11.9809 / 2.05e+05 |
| stratified_exp0.75 ! | 0.4993 / 7.491 | 0.2111 / 1.143 | 11.7750 / 4.212e+04 |
| stratified_exp1.0 ! | 0.4998 / 6.491 | 0.2113 / 0.9925 | 11.8486 / 5.768e+04 |

---

## naive_ps, K = -2.0x-2.0x-2.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.4947 / 817.5 | 0.1063 / 32.96 | 12.2148 / 1.478e+06 |
| stratified_exp0.05 | 0.4975 / 166.3 | 0.1058 / 6.525 | 11.9496 / 3.795e+05 |
| stratified_exp0.1 | 0.4979 / 84.28 | 0.1056 / 3.275 | 11.9040 / 1.578e+05 |
| stratified_exp0.25 | 0.4982 / 34.51 | 0.1056 / 1.339 | 11.8656 / 6.598e+04 |
| stratified_exp0.5 ! | 0.4978 / 18.02 | 0.1055 / 0.6968 | 11.7642 / 3.565e+04 |
| stratified_exp0.75 ! | 0.4984 / 12.62 | 0.1055 / 0.4848 | 11.7673 / 8.13e+04 |
| stratified_exp1.0 ! | 0.4989 / 9.979 | 0.1055 / 0.3827 | 11.9809 / 2.05e+05 |

---

## naive_ps, K = -3.0x-3.0x-3.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.4993 / 1234 | 0.0714 / 21.88 | 11.6082 / 1.012e+06 |
| stratified_exp0.05 | 0.4956 / 246.3 | 0.0703 / 4.313 | 11.7584 / 3.081e+05 |
| stratified_exp0.1 | 0.4989 / 125.5 | 0.0706 / 2.18 | 11.9882 / 2.063e+05 |
| stratified_exp0.25 | 0.4978 / 50.99 | 0.0703 / 0.879 | 11.7441 / 7.448e+04 |
| stratified_exp0.5 ! | 0.4980 / 26.22 | 0.0704 / 0.4522 | 11.7720 / 4.715e+04 |
| stratified_exp0.75 ! | 0.4978 / 18.02 | 0.0703 / 0.3097 | 11.7642 / 3.565e+04 |
| stratified_exp1.0 ! | 0.4984 / 13.97 | 0.0703 / 0.2388 | 11.8978 / 7.479e+04 |

---

## naive_ps, K = -4.0x-4.0x-4.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.5019 / 1644 | 0.0540 / 16.54 | 11.7472 / 1.298e+06 |
| stratified_exp0.05 | 0.4895 / 322.3 | 0.0525 / 3.228 | 11.6258 / 4.285e+05 |
| stratified_exp0.1 | 0.4975 / 166.3 | 0.0529 / 1.631 | 11.9496 / 3.795e+05 |
| stratified_exp0.25 | 0.4968 / 67.43 | 0.0527 / 0.6552 | 11.7882 / 9.461e+04 |
| stratified_exp0.5 ! | 0.4982 / 34.51 | 0.0528 / 0.3348 | 11.8656 / 6.598e+04 |
| stratified_exp0.75 ! | 0.4982 / 23.5 | 0.0528 / 0.2278 | 11.8515 / 5.13e+04 |
| stratified_exp1.0 ! | 0.4978 / 18.02 | 0.0528 / 0.1742 | 11.7642 / 3.565e+04 |

---

## naive_ps, K = -10.0x-10.0x-10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 0.5160 / 4220 | 0.0222 / 6.782 | 12.1556 / 3.544e+06 |
| stratified_exp0.05 | 0.4947 / 817.5 | 0.0213 / 1.318 | 12.2148 / 1.478e+06 |
| stratified_exp0.1 | 0.4892 / 405.1 | 0.0211 / 0.6497 | 12.0097 / 1.166e+06 |
| stratified_exp0.25 | 0.4975 / 166.3 | 0.0212 / 0.261 | 11.9496 / 3.795e+05 |
| stratified_exp0.5 ! | 0.4979 / 84.28 | 0.0211 / 0.131 | 11.9040 / 1.578e+05 |
| stratified_exp0.75 ! | 0.4976 / 56.51 | 0.0211 / 0.0877 | 11.8031 / 8.986e+04 |
| stratified_exp1.0 ! | 0.4984 / 42.8 | 0.0211 / 0.06638 | 11.7367 / 6.319e+04 |

---

## cmplx_ps, K = -0.01x-0.01x-0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6658 / 14.74 | 60.6778 / 1.928e+04 | 31.3253 / 2.567e+05 |
| stratified_exp0.05 | 1.6573 / 200.8 | 60.4242 / 3.285e+05 | 30.5181 / 1.321e+06 |
| stratified_exp0.1 | 1.6611 / 4.923e+04 | 60.6027 / 6.941e+07 | 28.8048 / 3.114e+07 |
| stratified_exp0.25 | 1.4777 / 9.324e+04 | 53.6787 / 1.713e+08 | 20.8090 / 3.056e+07 |
| stratified_exp0.5 ! | 1.0608 / 4.486e+04 | 37.9948 / 6.628e+07 | 11.5444 / 9.468e+06 |
| stratified_exp0.75 ! | 0.8198 / 3.682e+04 | 28.7552 / 3.888e+07 | 7.6395 / 4.227e+06 |
| stratified_exp1.0 ! | 0.6657 / 2.691e+04 | 22.9859 / 2.495e+07 | 5.5844 / 2.24e+06 |

---

## cmplx_ps, K = -0.01x-10.0x-1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.7111 / 4566 | 0.1703 / 38.77 | 51.1814 / 9.338e+07 |
| stratified_exp0.05 | 1.6719 / 880.9 | 0.1679 / 7.645 | 49.1785 / 7.733e+06 |
| stratified_exp0.1 | 1.6656 / 438 | 0.1680 / 3.844 | 51.4128 / 2.556e+07 |
| stratified_exp0.25 | 1.6638 / 175.9 | 0.1677 / 1.542 | 50.8096 / 5.274e+06 |
| stratified_exp0.5 ! | 1.6644 / 89.05 | 0.1679 / 0.7813 | 51.3162 / 5.961e+06 |
| stratified_exp0.75 ! | 1.6655 / 60.27 | 0.1680 / 0.5293 | 50.5109 / 1.692e+06 |
| stratified_exp1.0 ! | 1.6659 / 45.98 | 0.1679 / 0.4031 | 50.5676 / 2.624e+06 |

---

## cmplx_ps, K = -0.05x-0.05x-0.05

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6663 / 54.74 | 12.1493 / 2796 | 31.4751 / 1.877e+05 |
| stratified_exp0.05 | 1.6658 / 14.74 | 12.1356 / 771.4 | 31.3253 / 2.567e+05 |
| stratified_exp0.1 | 1.6669 / 22.6 | 12.1535 / 1704 | 32.4939 / 1.436e+07 |
| stratified_exp0.25 | 1.6573 / 200.8 | 12.0848 / 1.314e+04 | 30.5181 / 1.321e+06 |
| stratified_exp0.5 ! | 1.6611 / 4.923e+04 | 12.1205 / 2.776e+06 | 28.8048 / 3.114e+07 |
| stratified_exp0.75 ! | 1.7216 / 3.262e+05 | 12.1873 / 1.138e+07 | 27.2940 / 7.303e+07 |
| stratified_exp1.0 ! | 1.6006 / 1.774e+05 | 11.5513 / 9.525e+06 | 24.4535 / 5.779e+07 |

---

## cmplx_ps, K = -0.1x-0.1x-0.1

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6666 / 107.8 | 6.0809 / 1375 | 31.2930 / 1.63e+05 |
| stratified_exp0.05 | 1.6658 / 23.4 | 6.0675 / 298.9 | 31.4391 / 5.588e+05 |
| stratified_exp0.1 | 1.6658 / 14.74 | 6.0678 / 192.8 | 31.3253 / 2.567e+05 |
| stratified_exp0.25 | 1.6659 / 28.69 | 6.0756 / 630.9 | 31.4033 / 3.996e+06 |
| stratified_exp0.5 ! | 1.6573 / 200.8 | 6.0424 / 3285 | 30.5181 / 1.321e+06 |
| stratified_exp0.75 ! | 1.6395 / 1309 | 5.9926 / 2.867e+04 | 29.3516 / 4.699e+06 |
| stratified_exp1.0 ! | 1.6611 / 4.923e+04 | 6.0603 / 6.941e+05 | 28.8048 / 3.114e+07 |

---

## cmplx_ps, K = -0.5x-0.5x-0.5

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6673 / 535.1 | 1.2158 / 272.1 | 31.5428 / 8.634e+05 |
| stratified_exp0.05 | 1.6666 / 107.8 | 1.2162 / 54.99 | 31.2930 / 1.63e+05 |
| stratified_exp0.1 | 1.6663 / 54.74 | 1.2149 / 27.96 | 31.4751 / 1.877e+05 |
| stratified_exp0.25 | 1.6658 / 23.4 | 1.2135 / 11.96 | 31.4391 / 5.588e+05 |
| stratified_exp0.5 ! | 1.6658 / 14.74 | 1.2136 / 7.714 | 31.3253 / 2.567e+05 |
| stratified_exp0.75 ! | 1.6667 / 15.35 | 1.2141 / 8.634 | 31.1841 / 9.435e+04 |
| stratified_exp1.0 ! | 1.6669 / 22.6 | 1.2154 / 17.04 | 32.4939 / 1.436e+07 |

---

## cmplx_ps, K = -1.0x-1.0x-1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6685 / 1071 | 0.6091 / 136.9 | 31.0122 / 1.166e+06 |
| stratified_exp0.05 | 1.6683 / 214.3 | 0.6083 / 27.28 | 31.0798 / 2.623e+05 |
| stratified_exp0.1 | 1.6666 / 107.8 | 0.6081 / 13.75 | 31.2930 / 1.63e+05 |
| stratified_exp0.25 | 1.6669 / 44.22 | 0.6074 / 5.639 | 31.3265 / 1.293e+05 |
| stratified_exp0.5 ! | 1.6658 / 23.4 | 0.6068 / 2.989 | 31.4391 / 5.588e+05 |
| stratified_exp0.75 ! | 1.6658 / 16.94 | 0.6066 / 2.181 | 31.1973 / 7.508e+04 |
| stratified_exp1.0 ! | 1.6658 / 14.74 | 0.6068 / 1.928 | 31.3253 / 2.567e+05 |

---

## cmplx_ps, K = -2.0x-2.0x-2.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6839 / 2182 | 0.3068 / 69.6 | 32.6155 / 5.519e+06 |
| stratified_exp0.05 | 1.6687 / 428.6 | 0.3040 / 13.58 | 31.4465 / 5.417e+05 |
| stratified_exp0.1 | 1.6683 / 214.3 | 0.3042 / 6.821 | 31.0798 / 2.623e+05 |
| stratified_exp0.25 | 1.6655 / 86.5 | 0.3038 / 2.759 | 31.1700 / 1.251e+05 |
| stratified_exp0.5 ! | 1.6669 / 44.22 | 0.3037 / 1.41 | 31.3265 / 1.293e+05 |
| stratified_exp0.75 ! | 1.6654 / 30.22 | 0.3034 / 0.9641 | 31.0981 / 8.154e+04 |
| stratified_exp1.0 ! | 1.6658 / 23.4 | 0.3034 / 0.7473 | 31.4391 / 5.588e+05 |

---

## cmplx_ps, K = -3.0x-3.0x-3.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6879 / 3287 | 0.2050 / 46.75 | 31.7537 / 3.897e+06 |
| stratified_exp0.05 | 1.6670 / 640.9 | 0.2026 / 9.069 | 31.1451 / 6.731e+05 |
| stratified_exp0.1 | 1.6700 / 321.6 | 0.2028 / 4.534 | 31.6322 / 5.793e+05 |
| stratified_exp0.25 | 1.6672 / 129.1 | 0.2028 / 1.829 | 31.2548 / 1.887e+05 |
| stratified_exp0.5 ! | 1.6659 / 65.3 | 0.2025 / 0.9261 | 31.1869 / 1.005e+05 |
| stratified_exp0.75 ! | 1.6669 / 44.22 | 0.2025 / 0.6265 | 31.3265 / 1.293e+05 |
| stratified_exp1.0 ! | 1.6663 / 33.73 | 0.2024 / 0.4777 | 31.2535 / 1.515e+05 |

---

## cmplx_ps, K = -4.0x-4.0x-4.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.6953 / 4424 | 0.1543 / 35.21 | 32.2009 / 8.636e+06 |
| stratified_exp0.05 | 1.6677 / 855.1 | 0.1521 / 6.825 | 31.3262 / 1.395e+06 |
| stratified_exp0.1 | 1.6687 / 428.6 | 0.1520 / 3.395 | 31.4465 / 5.417e+05 |
| stratified_exp0.25 | 1.6676 / 171.6 | 0.1521 / 1.367 | 31.2810 / 3.567e+05 |
| stratified_exp0.5 ! | 1.6655 / 86.5 | 0.1519 / 0.6897 | 31.1700 / 1.251e+05 |
| stratified_exp0.75 ! | 1.6662 / 58.26 | 0.1519 / 0.4648 | 31.2752 / 1.022e+05 |
| stratified_exp1.0 ! | 1.6669 / 44.22 | 0.1519 / 0.3524 | 31.3265 / 1.293e+05 |

---

## cmplx_ps, K = -10.0x-10.0x-10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.7222 / 1.12e+04 | 0.0621 / 13.92 | 31.9188 / 8.521e+06 |
| stratified_exp0.05 | 1.6839 / 2182 | 0.0614 / 2.784 | 32.6155 / 5.519e+06 |
| stratified_exp0.1 | 1.6685 / 1071 | 0.0609 / 1.369 | 31.0122 / 1.166e+06 |
| stratified_exp0.25 | 1.6687 / 428.6 | 0.0608 / 0.5432 | 31.4465 / 5.417e+05 |
| stratified_exp0.5 ! | 1.6683 / 214.3 | 0.0608 / 0.2728 | 31.0798 / 2.623e+05 |
| stratified_exp0.75 ! | 1.6674 / 143.2 | 0.0608 / 0.1827 | 31.2928 / 2.391e+05 |
| stratified_exp1.0 ! | 1.6666 / 107.8 | 0.0608 / 0.1375 | 31.2930 / 1.63e+05 |

---

## c1e3_exp1.0, K = -0.01x-0.01x-0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0401 / 9.297 | 41.0422 / 1.291e+04 | 54.5363 / 6.349e+05 |
| stratified_exp0.05 | 1.0512 / 906.9 | 41.1284 / 4.438e+05 | 54.1832 / 2.3e+07 |
| stratified_exp0.1 | 1.0731 / 3.372e+04 | 41.9052 / 2.991e+07 | 50.7077 / 6.066e+08 |
| stratified_exp0.25 | 0.9079 / 5.517e+04 | 35.8110 / 6.603e+07 | 30.2960 / 4.621e+08 |
| stratified_exp0.5 ! | 0.6284 / 5.729e+04 | 25.2379 / 6.419e+07 | 13.3262 / 1.021e+08 |
| stratified_exp0.75 ! | 0.4514 / 2.166e+04 | 18.4590 / 2.736e+07 | 7.1516 / 1.673e+07 |
| stratified_exp1.0 ! | 0.3504 / 1.061e+04 | 14.4462 / 1.351e+07 | 4.6832 / 4.815e+06 |

---

## c1e3_exp1.0, K = -0.01x-10.0x-1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0543 / 2692 | 0.1245 / 24.99 | 174.3016 / 9.401e+08 |
| stratified_exp0.05 | 1.0346 / 529.9 | 0.1220 / 4.796 | 178.6200 / 3.953e+09 |
| stratified_exp0.1 | 1.0373 / 266.3 | 0.1221 / 2.416 | 162.9073 / 1.155e+08 |
| stratified_exp0.25 | 1.0381 / 107.4 | 0.1221 / 0.971 | 164.2966 / 3.033e+07 |
| stratified_exp0.5 ! | 1.0394 / 55.07 | 0.1223 / 0.4955 | 164.1617 / 1.69e+07 |
| stratified_exp0.75 ! | 1.0397 / 37.65 | 0.1222 / 0.336 | 164.0229 / 1.712e+07 |
| stratified_exp1.0 ! | 1.0402 / 28.98 | 0.1223 / 0.2575 | 163.9012 / 1.323e+07 |

---

## c1e3_exp1.0, K = -0.05x-0.05x-0.05

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0408 / 32.25 | 8.2134 / 1797 | 55.0771 / 8.036e+05 |
| stratified_exp0.05 | 1.0401 / 9.297 | 8.2084 / 516.2 | 54.5363 / 6.349e+05 |
| stratified_exp0.1 | 1.0409 / 12.91 | 8.2190 / 1439 | 55.2744 / 6.193e+06 |
| stratified_exp0.25 | 1.0512 / 906.9 | 8.2257 / 1.775e+04 | 54.1832 / 2.3e+07 |
| stratified_exp0.5 ! | 1.0731 / 3.372e+04 | 8.3810 / 1.196e+06 | 50.7077 / 6.066e+08 |
| stratified_exp0.75 ! | 1.0302 / 4.927e+04 | 8.0968 / 2.895e+06 | 39.3770 / 2.431e+08 |
| stratified_exp1.0 ! | 0.9642 / 4.108e+04 | 7.6078 / 2.486e+06 | 33.7184 / 2.15e+08 |

---

## c1e3_exp1.0, K = -0.1x-0.1x-0.1

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0411 / 62.77 | 4.1074 / 875 | 54.2932 / 9.621e+05 |
| stratified_exp0.05 | 1.0413 / 14.4 | 4.1070 / 199.4 | 54.7856 / 7.973e+05 |
| stratified_exp0.1 | 1.0401 / 9.297 | 4.1042 / 129.1 | 54.5363 / 6.349e+05 |
| stratified_exp0.25 | 1.0405 / 22.93 | 4.1069 / 331.5 | 55.7798 / 7.492e+06 |
| stratified_exp0.5 ! | 1.0512 / 906.9 | 4.1128 / 4438 | 54.1832 / 2.3e+07 |
| stratified_exp0.75 ! | 1.0486 / 3695 | 4.1213 / 3.739e+04 | 53.4978 / 2.482e+08 |
| stratified_exp1.0 ! | 1.0731 / 3.372e+04 | 4.1905 / 2.991e+05 | 50.7077 / 6.066e+08 |

---

## c1e3_exp1.0, K = -0.5x-0.5x-0.5

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0359 / 306.8 | 0.8188 / 171.6 | 54.4676 / 4.327e+06 |
| stratified_exp0.05 | 1.0411 / 62.77 | 0.8215 / 35 | 54.2932 / 9.621e+05 |
| stratified_exp0.1 | 1.0408 / 32.25 | 0.8213 / 17.97 | 55.0771 / 8.036e+05 |
| stratified_exp0.25 | 1.0413 / 14.4 | 0.8214 / 7.974 | 54.7856 / 7.973e+05 |
| stratified_exp0.5 ! | 1.0401 / 9.297 | 0.8208 / 5.162 | 54.5363 / 6.349e+05 |
| stratified_exp0.75 ! | 1.0405 / 9.109 | 0.8210 / 5.125 | 54.7637 / 8.215e+05 |
| stratified_exp1.0 ! | 1.0409 / 12.91 | 0.8219 / 14.39 | 55.2744 / 6.193e+06 |

---

## c1e3_exp1.0, K = -1.0x-1.0x-1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0394 / 623.1 | 0.4119 / 87.96 | 55.5304 / 1.013e+07 |
| stratified_exp0.05 | 1.0407 / 124.2 | 0.4105 / 17.33 | 54.5899 / 2.026e+06 |
| stratified_exp0.1 | 1.0411 / 62.77 | 0.4107 / 8.75 | 54.2932 / 9.621e+05 |
| stratified_exp0.25 | 1.0419 / 26.26 | 0.4109 / 3.651 | 55.1326 / 1.18e+06 |
| stratified_exp0.5 ! | 1.0413 / 14.4 | 0.4107 / 1.994 | 54.7856 / 7.973e+05 |
| stratified_exp0.75 ! | 1.0411 / 10.73 | 0.4106 / 1.484 | 54.6072 / 4.302e+05 |
| stratified_exp1.0 ! | 1.0401 / 9.297 | 0.4104 / 1.291 | 54.5363 / 6.349e+05 |

---

## c1e3_exp1.0, K = -2.0x-2.0x-2.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0579 / 1276 | 0.2087 / 44.81 | 56.8424 / 2.342e+07 |
| stratified_exp0.05 | 1.0366 / 245.5 | 0.2047 / 8.577 | 54.1177 / 3.037e+06 |
| stratified_exp0.1 | 1.0407 / 124.2 | 0.2052 / 4.332 | 54.5899 / 2.026e+06 |
| stratified_exp0.25 | 1.0410 / 50.51 | 0.2053 / 1.76 | 54.4563 / 7.993e+05 |
| stratified_exp0.5 ! | 1.0419 / 26.26 | 0.2054 / 0.9129 | 55.1326 / 1.18e+06 |
| stratified_exp0.75 ! | 1.0419 / 18.29 | 0.2054 / 0.6345 | 54.7343 / 4.317e+05 |
| stratified_exp1.0 ! | 1.0413 / 14.4 | 0.2054 / 0.4984 | 54.7856 / 7.973e+05 |

---

## c1e3_exp1.0, K = -3.0x-3.0x-3.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0582 / 1896 | 0.1394 / 29.9 | 56.8072 / 2.123e+07 |
| stratified_exp0.05 | 1.0339 / 367.4 | 0.1364 / 5.724 | 54.4747 / 5.909e+06 |
| stratified_exp0.1 | 1.0400 / 185 | 0.1367 / 2.866 | 54.3740 / 2.164e+06 |
| stratified_exp0.25 | 1.0415 / 75.06 | 0.1370 / 1.163 | 54.7428 / 1.389e+06 |
| stratified_exp0.5 ! | 1.0408 / 38.33 | 0.1369 / 0.5929 | 54.5061 / 6.274e+05 |
| stratified_exp0.75 ! | 1.0419 / 26.26 | 0.1370 / 0.4057 | 55.1326 / 1.18e+06 |
| stratified_exp1.0 ! | 1.0422 / 20.28 | 0.1370 / 0.3127 | 55.0902 / 5.611e+05 |

---

## c1e3_exp1.0, K = -4.0x-4.0x-4.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0516 / 2504 | 0.1048 / 22.56 | 62.9961 / 1.516e+08 |
| stratified_exp0.05 | 1.0354 / 493.7 | 0.1026 / 4.342 | 54.7479 / 7.407e+06 |
| stratified_exp0.1 | 1.0366 / 245.5 | 0.1024 / 2.144 | 54.1177 / 3.037e+06 |
| stratified_exp0.25 | 1.0406 / 99.54 | 0.1026 / 0.8667 | 54.6063 / 2.519e+06 |
| stratified_exp0.5 ! | 1.0410 / 50.51 | 0.1027 / 0.44 | 54.4563 / 7.993e+05 |
| stratified_exp0.75 ! | 1.0407 / 34.28 | 0.1027 / 0.2984 | 54.7519 / 6.593e+05 |
| stratified_exp1.0 ! | 1.0419 / 26.26 | 0.1027 / 0.2282 | 55.1326 / 1.18e+06 |

---

## c1e3_exp1.0, K = -10.0x-10.0x-10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0749 / 6447 | 0.0429 / 9.207 | 57.2248 / 6.417e+07 |
| stratified_exp0.05 | 1.0579 / 1276 | 0.0417 / 1.792 | 56.8424 / 2.342e+07 |
| stratified_exp0.1 | 1.0394 / 623.1 | 0.0412 / 0.8796 | 55.5304 / 1.013e+07 |
| stratified_exp0.25 | 1.0366 / 245.5 | 0.0409 / 0.3431 | 54.1177 / 3.037e+06 |
| stratified_exp0.5 ! | 1.0407 / 124.2 | 0.0410 / 0.1733 | 54.5899 / 2.026e+06 |
| stratified_exp0.75 ! | 1.0412 / 83.24 | 0.0411 / 0.1161 | 54.6252 / 1.695e+06 |
| stratified_exp1.0 ! | 1.0411 / 62.77 | 0.0411 / 0.0875 | 54.2932 / 9.621e+05 |

---

## c1e4_exp1.0, K = -0.01x-0.01x-0.01

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0401 / 9.297 | 41.0422 / 1.291e+04 | 65.3062 / 5.816e+06 |
| stratified_exp0.05 | 1.0512 / 906.9 | 41.1284 / 4.438e+05 | 61.7609 / 3.876e+07 |
| stratified_exp0.1 | 1.0731 / 3.372e+04 | 41.9052 / 2.991e+07 | 55.2801 / 7.826e+08 |
| stratified_exp0.25 | 0.9079 / 5.517e+04 | 35.8110 / 6.603e+07 | 31.0488 / 4.948e+08 |
| stratified_exp0.5 ! | 0.6284 / 5.729e+04 | 25.2379 / 6.419e+07 | 13.4738 / 1.049e+08 |
| stratified_exp0.75 ! | 0.4514 / 2.166e+04 | 18.4590 / 2.736e+07 | 7.2157 / 1.728e+07 |
| stratified_exp1.0 ! | 0.3504 / 1.061e+04 | 14.4462 / 1.351e+07 | 4.7028 / 4.844e+06 |

---

## c1e4_exp1.0, K = -0.01x-10.0x-1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0543 / 2692 | 0.1245 / 24.99 | 300.7153 / 5.196e+09 |
| stratified_exp0.05 | 1.0346 / 529.9 | 0.1220 / 4.796 | 271.1079 / 4.942e+09 |
| stratified_exp0.1 | 1.0373 / 266.3 | 0.1221 / 2.416 | 266.9461 / 9.766e+08 |
| stratified_exp0.25 | 1.0381 / 107.4 | 0.1221 / 0.971 | 258.2893 / 1.545e+08 |
| stratified_exp0.5 ! | 1.0394 / 55.07 | 0.1223 / 0.4955 | 268.8989 / 3.38e+08 |
| stratified_exp0.75 ! | 1.0397 / 37.65 | 0.1222 / 0.336 | 266.6036 / 1.332e+08 |
| stratified_exp1.0 ! | 1.0402 / 28.98 | 0.1223 / 0.2575 | 264.3056 / 1.677e+08 |

---

## c1e4_exp1.0, K = -0.05x-0.05x-0.05

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0408 / 32.25 | 8.2134 / 1797 | 65.0460 / 1.982e+06 |
| stratified_exp0.05 | 1.0401 / 9.297 | 8.2084 / 516.2 | 65.3062 / 5.816e+06 |
| stratified_exp0.1 | 1.0409 / 12.91 | 8.2190 / 1439 | 66.8326 / 8.261e+07 |
| stratified_exp0.25 | 1.0512 / 906.9 | 8.2257 / 1.775e+04 | 61.7609 / 3.876e+07 |
| stratified_exp0.5 ! | 1.0731 / 3.372e+04 | 8.3810 / 1.196e+06 | 55.2801 / 7.826e+08 |
| stratified_exp0.75 ! | 1.0302 / 4.927e+04 | 8.0968 / 2.895e+06 | 41.1033 / 2.582e+08 |
| stratified_exp1.0 ! | 0.9642 / 4.108e+04 | 7.6078 / 2.486e+06 | 35.3120 / 2.65e+08 |

---

## c1e4_exp1.0, K = -0.1x-0.1x-0.1

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0411 / 62.77 | 4.1074 / 875 | 64.1629 / 2.565e+06 |
| stratified_exp0.05 | 1.0413 / 14.4 | 4.1070 / 199.4 | 65.0901 / 1.936e+06 |
| stratified_exp0.1 | 1.0401 / 9.297 | 4.1042 / 129.1 | 65.3062 / 5.816e+06 |
| stratified_exp0.25 | 1.0405 / 22.93 | 4.1069 / 331.5 | 67.8918 / 3.985e+07 |
| stratified_exp0.5 ! | 1.0512 / 906.9 | 4.1128 / 4438 | 61.7609 / 3.876e+07 |
| stratified_exp0.75 ! | 1.0486 / 3695 | 4.1213 / 3.739e+04 | 60.3452 / 4.564e+08 |
| stratified_exp1.0 ! | 1.0731 / 3.372e+04 | 4.1905 / 2.991e+05 | 55.2801 / 7.826e+08 |

---

## c1e4_exp1.0, K = -0.5x-0.5x-0.5

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0359 / 306.8 | 0.8188 / 171.6 | 64.8806 / 1.143e+07 |
| stratified_exp0.05 | 1.0411 / 62.77 | 0.8215 / 35 | 64.1629 / 2.565e+06 |
| stratified_exp0.1 | 1.0408 / 32.25 | 0.8213 / 17.97 | 65.0460 / 1.982e+06 |
| stratified_exp0.25 | 1.0413 / 14.4 | 0.8214 / 7.974 | 65.0901 / 1.936e+06 |
| stratified_exp0.5 ! | 1.0401 / 9.297 | 0.8208 / 5.162 | 65.3062 / 5.816e+06 |
| stratified_exp0.75 ! | 1.0405 / 9.109 | 0.8210 / 5.125 | 64.6816 / 2.455e+06 |
| stratified_exp1.0 ! | 1.0409 / 12.91 | 0.8219 / 14.39 | 66.8326 / 8.261e+07 |

---

## c1e4_exp1.0, K = -1.0x-1.0x-1.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0394 / 623.1 | 0.4119 / 87.96 | 65.0218 / 2.43e+07 |
| stratified_exp0.05 | 1.0407 / 124.2 | 0.4105 / 17.33 | 64.4412 / 5.3e+06 |
| stratified_exp0.1 | 1.0411 / 62.77 | 0.4107 / 8.75 | 64.1629 / 2.565e+06 |
| stratified_exp0.25 | 1.0419 / 26.26 | 0.4109 / 3.651 | 65.3326 / 2.455e+06 |
| stratified_exp0.5 ! | 1.0413 / 14.4 | 0.4107 / 1.994 | 65.0901 / 1.936e+06 |
| stratified_exp0.75 ! | 1.0411 / 10.73 | 0.4106 / 1.484 | 64.3148 / 1.226e+06 |
| stratified_exp1.0 ! | 1.0401 / 9.297 | 0.4104 / 1.291 | 65.3062 / 5.816e+06 |

---

## c1e4_exp1.0, K = -2.0x-2.0x-2.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0579 / 1276 | 0.2087 / 44.81 | 68.6324 / 6.228e+07 |
| stratified_exp0.05 | 1.0366 / 245.5 | 0.2047 / 8.577 | 63.5311 / 7.053e+06 |
| stratified_exp0.1 | 1.0407 / 124.2 | 0.2052 / 4.332 | 64.4412 / 5.3e+06 |
| stratified_exp0.25 | 1.0410 / 50.51 | 0.2053 / 1.76 | 64.6906 / 2.438e+06 |
| stratified_exp0.5 ! | 1.0419 / 26.26 | 0.2054 / 0.9129 | 65.3326 / 2.455e+06 |
| stratified_exp0.75 ! | 1.0419 / 18.29 | 0.2054 / 0.6345 | 65.8578 / 2.861e+06 |
| stratified_exp1.0 ! | 1.0413 / 14.4 | 0.2054 / 0.4984 | 65.0901 / 1.936e+06 |

---

## c1e4_exp1.0, K = -3.0x-3.0x-3.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0582 / 1896 | 0.1394 / 29.9 | 67.7377 / 5.969e+07 |
| stratified_exp0.05 | 1.0339 / 367.4 | 0.1364 / 5.724 | 64.4570 / 1.241e+07 |
| stratified_exp0.1 | 1.0400 / 185 | 0.1367 / 2.866 | 64.0581 / 5.23e+06 |
| stratified_exp0.25 | 1.0415 / 75.06 | 0.1370 / 1.163 | 64.6988 / 4.045e+06 |
| stratified_exp0.5 ! | 1.0408 / 38.33 | 0.1369 / 0.5929 | 64.4442 / 1.645e+06 |
| stratified_exp0.75 ! | 1.0419 / 26.26 | 0.1370 / 0.4057 | 65.3326 / 2.455e+06 |
| stratified_exp1.0 ! | 1.0422 / 20.28 | 0.1370 / 0.3127 | 65.5344 / 1.73e+06 |

---

## c1e4_exp1.0, K = -4.0x-4.0x-4.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0516 / 2504 | 0.1048 / 22.56 | 73.1289 / 1.992e+08 |
| stratified_exp0.05 | 1.0354 / 493.7 | 0.1026 / 4.342 | 64.1049 / 1.55e+07 |
| stratified_exp0.1 | 1.0366 / 245.5 | 0.1024 / 2.144 | 63.5311 / 7.053e+06 |
| stratified_exp0.25 | 1.0406 / 99.54 | 0.1026 / 0.8667 | 64.7189 / 6.335e+06 |
| stratified_exp0.5 ! | 1.0410 / 50.51 | 0.1027 / 0.44 | 64.6906 / 2.438e+06 |
| stratified_exp0.75 ! | 1.0407 / 34.28 | 0.1027 / 0.2984 | 64.8578 / 1.874e+06 |
| stratified_exp1.0 ! | 1.0419 / 26.26 | 0.1027 / 0.2282 | 65.3326 / 2.455e+06 |

---

## c1e4_exp1.0, K = -10.0x-10.0x-10.0

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE | VCE |
|---|---|---|---|
| stratified_exp0.01 | 1.0749 / 6447 | 0.0429 / 9.207 | 66.3860 / 1.15e+08 |
| stratified_exp0.05 | 1.0579 / 1276 | 0.0417 / 1.792 | 68.6324 / 6.228e+07 |
| stratified_exp0.1 | 1.0394 / 623.1 | 0.0412 / 0.8796 | 65.0218 / 2.43e+07 |
| stratified_exp0.25 | 1.0366 / 245.5 | 0.0409 / 0.3431 | 63.5311 / 7.053e+06 |
| stratified_exp0.5 ! | 1.0407 / 124.2 | 0.0410 / 0.1733 | 64.4412 / 5.3e+06 |
| stratified_exp0.75 ! | 1.0412 / 83.24 | 0.0411 / 0.1161 | 65.2787 / 6.139e+06 |
| stratified_exp1.0 ! | 1.0411 / 62.77 | 0.0411 / 0.0875 | 64.1629 / 2.565e+06 |


---

# Insights and conclusions

**All 2520 runs completed (2520/2520). Zero failures, zero non-finite values.** With `mode=opt` the
model is the exact Bayes posterior (`OptimalModelRefactor`), so every number below measures the
importance-weighted **estimator** on a product geometry, not a model. No figures are produced for
this project: `visualization/wloss_exp_var_vs_curvature.py` puts a scalar curvature on its x axis,
and this grid's geometry is a vector.

Read this against the single-manifold control `init_opt_test_3d_refactor_new`, whose verified
section establishes the machinery this one reuses: the reference-pass invariance, the
`lamR2 = lambda/|K|` collapse, and the heavy-tail behaviour of the pinned `stratified_exp(0.1)`
reference. Claims below that duplicate it are stated once and cited, not re-derived.

*Provenance.* Sections 1–5 come from claims that passed a three-lens adversarial check (numbers,
statistics, mechanism). Sections 6–7 come from claims whose checkers were cut off by an account
usage limit; every number in them was instead re-derived directly from the per-run
`test_metrics.json` data before being written here. The distinction is marked where it matters.

## 1. The reference pass is bitwise invariant, and `c1e3 = c1e4` except under VCE

**Hypothesis 4 passes, bitwise.** In all 120 `(ps, vector, seed)` groups of 21 `(lg, lambda)` cells,
each of the six reference fields — `wnelbo_ref`, `wnelbo_ref_std`, `wce_ref`, `wce_ref_std`,
`nelbo_ref`, `ce_ref` — takes exactly one value. Max relative spread 0, in the CSV and in all 2520
raw `test_metrics.json`.

- **This is stronger than the control, for a hardware reason, not a statistical one.** The control
  was bitwise in 103/108 groups for `wnelbo_ref`/`nelbo_ref` and 99/108 for `wnelbo_ref_std`; its 19
  split pairs were all `c1e4` and each minority value came from that group's runs on
  `desa-compute-01` (RTX 2080 Ti). Here no `c1e4` run could land there: `sweep_lib` sizes
  `(V=10000, D=9)` at 25.4 GiB × 1.15, so all 630 ran on the 48-GB cards (310 A6000, 320 RTX 6000
  Ada), and 29 of 30 `c1e4` groups still mix both models. `naive`/`cmplx`/`c1e3` did run on the 2080
  Ti and are bitwise too.
- **The hypothesis's premise is only half right.** `salt=1` seeds the `t` proposal only; the bridge
  draws come from the global RNG after the loss pass. The invariance holds because the loss pass
  consumes a fixed number of global draws in every cell — shapes are fixed, with no rejection
  sampling — so what is shown is equal RNG consumption, not separate bridge streams.

**`c1e3` and `c1e4` are one validation, not two.** Over the 630 paired runs the reference fields
differ by at most 7.2e-16 (1–4 ulp) and `ce`/`pp` `wloss` by at most 1.1e-15. `c1e3`'s boundary table
is the first 998 rows of `c1e4`'s, and `ce`/`pp` see the extra rows only through a posterior where
`p = 1e-30`. Only `vce`, which reads every row through `min_v D`, separates them (§7).

## 2. On uniform vectors the loss pass sees only `lamR2`; the mixed vector has no such axis

The 63 `(K, lambda)` cells over the nine uniform vectors hold **37 distinct `lamR2`** values
(0.001–100); 13 of them are shared by 39 cells. Within each `(ps, seed, lamR2)` group the cells agree
to rounding:

| lg | invariant quantity | max relative spread |
|---|---|---|
| `pp` | `wloss` | 6.4e-16 |
| `vce` | `wloss` | 4.3e-15 |
| `ce` | `wloss / R^2` | 5.1e-15 |

Raw `ce` is not invariant: at `lamR2 = 1` it runs from 41.07 at `[-0.01]^3` to 0.4107 at `[-1]^3`,
the R² ratio. Counting `c1e3 = c1e4` for `ce`/`pp`, the 2520 runs hold 1320 distinct loss-pass values
and 90 distinct reference values. The mechanism is the control's, factor by factor: one heat time,
dimensionless `t/R^2`, and `kappa^2` prefactors in `pp`/`vce` but not `ce`.

**The mixed vector `[-0.01,-10,-1]` has no duplicates at all.** Its factors run at
`lamR2_m = lambda * (100, 0.1, 1)`, so no single `lamR2` exists. Its 7 rates differ pairwise by at
least 7.4e-5 (pp) and no mixed cell matches any uniform cell (closest 1.8e-6 relative, ~10 orders
above ulp and far inside the estimator scatter). Its 21 cells per `(ps, seed)` are still **not
independent**: they reuse one `u`-stream, one target sequence and one set of bridge draws.

## 3. The mixed vector lands on H(p) and tracks its sharpest factor (hypothesis 1)

| ps | `wnelbo_ref` (3-seed) | dev vs H | per-sample std | across-seed t (2 dof) |
|---|---|---|---|---|
| naive_ps | 0.49581 | −0.89% | 13.31 | −1.36 |
| cmplx_ps | 1.66782 | +0.09% | 20.91 | +2.76 |
| c1e3 = c1e4 | 1.03270 | −0.76% | 16.21 | −1.90 |

All are inside `t_crit(2 dof) = 4.30`, so **part (a) passes**. Per-*seed* deviations reach −2.19%
(naive seed 0), so on a single seed the exact posterior's own reading sets a **~2% resolution floor**
for the `test_wnelbo_ref >= H(p)` check.

**Part (b) holds on the CE family.** Against the single-manifold `K = -10` control (3-seed ratios,
naive / cmplx / c1e3):

| metric | mixed / single K=−10 | `[-10]^3` / single K=−10 |
|---|---|---|
| `ce_ref` | 0.956 / 0.800 / 1.051 | 0.331 / 0.289 / 0.352 |
| `wce_ref` | 0.955 / 0.798 / 1.050 | 0.328 / 0.287 / 0.349 |
| `wnelbo_ref_std` | 1.01 / 1.06 / 0.99 | 1.53 / 1.64 / 1.48 |

The ELBO metrics do not discriminate (0.97–1.00 for both), as expected: `wnelbo_ref` targets H(p) at
every geometry. So the mixed vector reproduces **single `K = -10`**, not `[-10]^3` — with a
reproducible ps-dependent residual (cmplx CE sits ~20% low), and the caveat that this is a
cross-project comparison with different boundary tables.

**The loss pass is flat in rate.** `pp wloss` stays within −1.59%…+2.69% of H across the 21
`(ps, rate)` cells, every deviation inside the Monte-Carlo noise floor (|z| ≤ 2.30), and shrinks to
−0.33%…−0.05% at `lambda = 1`. The ceiling (9.696, set by the `K = -10` factor, identical for single
`K = -10` and `[-10]^3`) clamps 37.9% of reference draws, but it is **not** what separates these
geometries: the `pp` std separation (mixed 0.995–1.077× single `K=-10`, `[-10]^3` 1.47–1.69×) is as
large at `lambda = 1`, where 6.2e-5 of draws are clamped, as at `lambda = 0.01`, where 90.8% are.

**Versus the old `exp` grid** (mixed vector only): per-sample std and CE metrics are unchanged to
~1% (std 13.32 vs 13.31, 20.91 vs 20.88, 16.21 vs 16.35). `wnelbo_ref` moved −0.0018 / +0.0029 /
−0.0099, i.e. 1–2 SE. Both proposals have the same marginal law for `t` and the same weights, so
these are estimator variance, not a proposal effect.

## 4. Soundness on the uniform vectors (hypothesis 2, mostly supported)

**Reference pass.** For `[-4]^3` through `[-0.1]^3` every reading is within **0.87%** of H(p) for all
four ps — the same order as the single manifold, slightly worse (max |dev| 0.87% vs 0.54%). At
`[-10]^3` it reads **0.86–1.86% low** (naive −1.86, cmplx −0.86, c1e3 −1.83) where the single
manifold reads +0.11…+1.16%.

**Loss pass, keyed by `lamR2`.** The seed mean stays within 1% of H(p) over `lamR2 ∈ [0.0167, 2.5]`
for every ps, and the 1%-window's upper end sits 1.7–3.3× further out than the single manifold's:

| `lamR2` | product (naive / cmplx / c1e3) | single manifold |
|---|---|---|
| 5 | −0.59 / −0.54 / +1.01% | −11.59 / −12.11 / −11.29% |
| 10 | −4.57 / −0.32 / +3.12% | −28.99 / −30.78 / −26.49% |
| 25 | −14.81 / −11.32 / −12.75% | −61.52 / −61.29 / −55.43% |
| 100 | −71.14 / −60.05 / −66.33% | −89.37 / −89.60 / −85.79% |

At small `lamR2` the product is the noisier of the two: per-sample std 1.41–1.69× the single's for
`lamR2 ≤ 0.2`, following `1/sqrt(lamR2)` to within 5%.

**The `[-10]^3` deficit is unexplained, and is not the heat-time ceiling.** By code, only `t` is
clamped and never the weight, and the `pp` integrand is non-negative, so the clamp can only *raise* a
reading; by data, the `lamR2 = 0.001` cell (90.8% clamped) reads **high** (+3.1…+3.4%), and the
shortfall is already present in the unweighted `nelbo_ref`. The independent `salt=0` stream at the
same `lamR2 = 0.01` reproduces the deficit only for naive (−2.21%), reading +0.13% (cmplx) and
−0.12% (c1e3). Treat `[-10]^3` as carrying ~2% estimator uncertainty rather than a demonstrated bias.

**Caveat on counting.** All 21 product reference means for `K ∈ [-10, -0.1]` are negative (single:
14/21), but within a seed those cells share every random input across `K` and ps. That is three
independent seeds, not 21 confirmations.

## 5. The flat vectors do not collapse (hypothesis 3, refuted as registered)

| vector | `wnelbo_ref` dev vs H (naive / cmplx / c1e3) | per-sample std | largest single draw |
|---|---|---|---|
| `[-0.05]^3` | −0.07 / −0.08 / −0.05% | 2.6–4.1 | ≤ 0.27% of the sum |
| `[-0.01]^3` | −4.91 / +0.14 / −3.69% | 19–53 (cmplx s0: 247) | ≤ 2.6% (6.9% cmplx s0) |
| single `K = -0.01` | +361 / +165 / +44% | 139–12181 | 47–94% in 4 of 9 runs |

- **`[-0.05]^3` reads on H(p)**, each within 0.8 across-seed SE, where the single manifold at
  `K = -0.05` spans −2.8%…+2.5% with std 8.9–65.2.
- **`[-0.01]^3` shows no single-draw dominance at all** — the pathology that made the single
  manifold's `K = -0.01` reference unusable. Like-for-like on the `salt=0` loss pass at the same
  `lamR2 = 10`, the product reads −4.57 / −0.32 / +3.12% against the single manifold's
  −28.99 / −30.78 / −26.49%.
- **The registered ~25% collapse does not happen**, and the registered mechanism is inert: at
  `K = -0.01` the ceiling is 9696 while the `u ≥ 1e-12` clamp caps `t` at 276, so it never binds in
  either project, on either pass.
- **The residual low reading is robust only for naive_ps** (−4.91% reference and −4.57% loss pass,
  two independent streams, pooled t = −3.3). The c1e3 −3.69% is contradicted by +3.12% on the other
  stream; cmplx reads on H(p).

*Hypothesis, not demonstrated:* with three factors the ELBO integrand decays faster in `t/R^2`, so
the same rare huge weights land where the integrand is already negligible, and hit-free runs miss
less tail mass. §6 gives the measured version of that compression.

## 6. Product versus single manifold: CE is ~1/3, the ELBO agrees, time runs ~3× faster

*(Numbers in this section and §7 were re-derived by the orchestrator from the run data, not checked
by the adversarial panel.)*

At matched `(ps, K, seed)`, 3-seed means, product / single:

| K | `wnelbo_ref` | `wnelbo_ref_std` | `wce_ref` | `ce_ref` |
|---|---|---|---|---|
| −10 | 0.970 / 0.990 / 0.981 | 1.53 / 1.64 / 1.48 | 0.328 / 0.287 / 0.349 | 0.331 / 0.289 / 0.352 |
| −4 … −0.5 | 0.994 – 1.002 | 1.41 – 1.65 | 0.334 – 0.336 / 0.289 / 0.354 – 0.356 | 0.29 – 0.41 (ps-dependent) |
| −0.1 | 0.999 / 1.001 / 0.996 | 0.44 / 0.42 / 0.31 | 0.335 / 0.289 / 0.356 | 0.541 / 0.474 / 0.555 |
| −0.05 | 1.008 / 1.007 / 1.003 | 0.10 / 0.10 / 0.12 | 0.335 / 0.288 / 0.352 | 0.651 / 0.578 / 0.658 |
| −0.01 | 0.206 / 0.378 / 0.671 | 0.01 / 0.02 / 0.03 | 0.145 / 0.155 / 0.206 | 0.888 / 0.832 / 0.881 |

- **The ELBO agrees** (0.994–1.008) wherever both estimators work, as it must: both target H(p).
- **The weighted CE integral is ~1/3 of the single manifold's**, stably across `K ∈ [-10, -0.05]` and
  ps-dependent (naive 0.33, cmplx 0.29, c1e3 0.35). The same factor appears in the loss pass:
  `ce wloss / R^2` on the plateau is 0.2116 / 0.6086 / 0.4116, i.e. 0.336 / 0.290 / 0.358× the
  single's.
- **The std ratio flips.** The product is 1.4–1.7× noisier where both are well behaved, and 3–100×
  *quieter* at flat curvature, where the single manifold's heavy tail takes over.
- **The `K = -0.01` column is not a product-vs-single statement**: the single-manifold reference there
  is tail-hit (§5), so the ratio measures its explosion.

**Time compression.** Pairing the product at `lamR2` with the single manifold at `lamR2 / 3` removes
almost all of the divergence:

| `lamR2` | product/single, matched | product(λR²)/single(λR²/3) |
|---|---|---|
| 1 | 1.005 / 1.001 / 0.994 | 0.998 / 0.999 / 0.999 |
| 7.5 | 1.246 / 1.244 / 1.249 | 1.038 / 0.987 / 1.024 |
| 15 | 1.639 / 1.848 / 1.615 | 1.023 / 1.180 / 1.116 |
| 75 | 2.694 / 3.530 / 2.349 | 0.995 / 1.271 / 0.970 |

*Hypothesis, partly structural:* the product's integrand works on a ~2.4–4.5× shorter dimensionless
time scale because three factors carry independent evidence. Part of this is forced rather than
discovered — `bridge_loss_elbo_refactor` sums three per-factor terms, so at `tau = 0` the product
integrand is ~3× the single's while both integrate to H(p), which bounds the ratio between 1 and ~3
by construction. The independent evidence that the posterior really does resolve faster is `ce_ref`,
which is not so constrained.

## 7. VCE and CE

- **Finite everywhere.** All 840 `vce` runs have finite `wloss` and `wloss_std`, spanning 1.32
  (naive, `[-0.01]^3`, λ=1) to 342.76 (c1e4, mixed vector, λ=0.01).
- **Plateau (`lamR2 ≤ 1`, uniform vectors):** 11.86 / 31.40 / 55.05 / 65.22 for
  naive / cmplx / c1e3 / c1e4, against the single manifold's 22.49 / 69.95 / 156.87 / 274.65. At
  matched `(ps, seed, lamR2)` the median ratio is **0.528 / 0.448 / 0.350 / 0.236** — the product's
  VCE is *smaller*, not ~3× larger, while `pp` is 1.00× and `ce` is 0.29–0.36×.
- **The mixed vector again tracks single `K = -10`**: median VCE ratio 1.098 / 0.731 / 1.046 / 0.949,
  and 1.6–4.1× `[-10]^3`.
- **Heavy tails confirmed (hypothesis 5, part one).** `vce` per-sample std exceeds `pp`'s in **840/840**
  runs (median 110.6×, min 6.9×), and its coefficient of variation is larger in 834/840 (median
  2.64×). The `vce` std is not a usable error bar.
- **VCE separates `c1e3` from `c1e4` (hypothesis 5, part two).** `c1e4 > c1e3` in **210/210** runs,
  median gap **15.5%** of `c1e4` — smaller than the single manifold's 41.5%, and shrinking with
  `lamR2` (0.4% at `lamR2 = 100`). The sign is near-structural: the weight takes `min_v D` over the
  whole table, and `c1e3`'s rows are a near-subset of `c1e4`'s, so this is not 210 independent tests.
- **Cross-project: the opt VCE value is not a floor for the trained twin.** On the 46 uniform
  plateau cells per ps, `init_test_log_vce_3x3d_refactor_new` reads below this project's VCE in
  41/46 (naive) and 45/46 (cmplx) cells, with every twin seed below every opt seed in 38 and 44 of
  them; twin/opt medians 0.612 and 0.658. Example, `[-1]^3` at λ=0.1: naive 7.00 / 7.06 / 7.34 vs
  11.56 / 11.79 / 11.86. Its `c1e4` is unstable rather than bounded (28/46). This reproduces the
  single-manifold finding and has the same explanation there: the twin trains its own boundary
  table, so it is not minimising the same functional.

## 8. Hypothesis scorecard

| # | pre-registered hypothesis | verdict | evidence |
|---|---|---|---|
| 1 | mixed vector lands on H(p); reproduces single `K=-10`, not `[-10]^3` | **Confirmed** | −0.89 / +0.09 / −0.76% of H, all within `t_crit(2 dof)`; `ce_ref` ratio 0.96 / 0.80 / 1.05 vs `[-10]^3`'s 0.33 / 0.29 / 0.35 (§3) |
| 2 | uniform `[K,K,K]`, `K ∈ [-10, -0.1]`, lands on H(p) | **Mostly** | within 0.87% for `[-4]^3`…`[-0.1]^3`; `[-10]^3` reads 0.86–1.86% low, not ceiling-driven, reproduced by the second stream only for naive (§4) |
| 3 | `[-0.05]^3` slightly low; `[-0.01]^3` collapses ~25% | **Refuted as registered** | `[-0.05]^3` within 0.09% of H; `[-0.01]^3` reads −4.9 / +0.1 / −3.7% with no single-draw dominance, against −26…−31% for the single manifold at the same `lamR2` (§5) |
| 4 | reference metrics identical across all 21 `(lg, λ)` cells | **Confirmed** | bitwise in all 120 groups, spread exactly 0; premise about the RNG stream corrected (§1) |
| 5 | VCE finite, heavier tails than `pp`, weight sums over factors | **Confirmed** | finite in 840/840; std > `pp` in 840/840 (median 110.6×); `c1e4 > c1e3` in 210/210, median gap 15.5% (§7) |

## 9. What this licenses the trained projects to claim

**`init_test_3x3d_refactor_new`** (`ce`/`pp`, `mode=tnb`, 1680 runs, plain `exp` loss and reference
proposals). Its run names tag uniform vectors with a scalar, but its hydra overrides confirm the
geometry is the product one (`prod_factor_gaussian_curvature=[-1.0,-1.0,-1.0]` and so on), covering
the same ten geometries. Because its reference used plain `exp(0.1)`, comparisons with this grid are
**qualitative**: the two proposals share the marginal law of `t` and the per-sample variance, but not
per-seed values.

- **`[-4]^3` … `[-0.1]^3` and the mixed vector: sound.** Read a trained `test_wnelbo_ref` against
  H(p) with about **1%** estimator resolution (2% at `[-10]^3`, and ~2% on a single seed for the
  mixed vector). A trained reading materially above that band is the model's own gap; one below it,
  where the estimator is sound, is a leak or bug signal.
- **`[-0.05]^3` and `[-0.01]^3` are usable here** — unlike single `K = -0.01`, where no correction
  number is licensed at all. At `[-0.01]^3` allow for the exact model's own −5%…0% spread.
- **Read `pp` by `lamR2 = lambda/|K|`, not by `K` or `lambda` separately**, and divide `ce` by `R^2`
  before comparing across curvature. `pp >= H(p)` is a meaningful check for `lamR2 ≲ 2.5`; beyond
  that the exact model itself reads low.
- **Do not compare product and single-manifold CE magnitudes directly**: the product's weighted CE
  integral is ~1/3 of the single manifold's at the same `K` (§6).

**`init_test_log_vce_3x3d_refactor_new`** (`vce`, 630 runs, same pinned `stratified_exp(0.1)`
reference). Its reference readings are draws of the §4 estimator and can be read against the bands
above directly. Its `test_wloss` is **not** bounded below by this project's VCE (§7), so it cannot
claim to approach a Bayes floor from above without a matched boundary table; compare at matched
`lamR2` on the plateau, quote medians rather than 3-seed means for `c1e4`, and do not use the VCE
per-sample std as an error bar.

## 10. Caveat on the `!` flags

`experiments/report.py` flags loss proposals by raw `lambda > 0.304`, and the same fixed threshold
appears in the figure script. As the single-manifold report's section 10 sets out in full, the loss
pass depends on `(K, lambda)` only through `lamR2`, so any such threshold has to be written as
`lambda/|K|`; on the uniform vectors here the flagged and correct rules disagree in the same way.
The flags annotate only — no number reported above depends on them — and the code is shared across
the `*_refactor_new` projects, so the fix is flagged here rather than made unilaterally. The mixed
vector has no `lamR2` at all (§2), so for that vector the flag has no correct scalar form.
