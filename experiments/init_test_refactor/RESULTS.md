# init_test_refactor results

- runs collected: **84** / 84 (100%) — run dirs without test_metrics.json: 0
- H(naive_ps) = **0.5003** — wnelbo_ref is bounded below by this
- H(cmplx_ps) = **1.6664** — wnelbo_ref is bounded below by this
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
| exp0.01 | 2.2600 ± 0.0140 | 0.5026 ± 0.0028 | 2.2490 ± 0.0163 | 0.0352 ± 0.0002 | 0.1510 ± 0.0012 |
| exp0.05 | 2.2434 ± 0.0047 | 0.5004 ± 0.0006 | 2.2359 ± 0.0028 | 0.0350 ± 0.0000 | 0.1502 ± 0.0002 |
| exp0.1 | 2.2350 ± 0.0035 | 0.5004 ± 0.0011 | 2.2340 ± 0.0025 | 0.0350 ± 0.0001 | 0.1501 ± 0.0001 |
| exp0.25 | 2.2379 ± 0.0266 | 0.5002 ± 0.0004 | 2.2348 ± 0.0023 | 0.0350 ± 0.0000 | 0.1501 ± 0.0002 |
| exp0.5 ! | 2.2466 ± 0.1452 | 0.5024 ± 0.0019 | 2.2570 ± 0.0127 | 0.0350 ± 0.0001 | 0.1506 ± 0.0002 |
| exp0.75 ! | 2.2219 ± 0.2080 | 0.5130 ± 0.0084 | 2.3216 ± 0.0509 | 0.0353 ± 0.0003 | 0.1521 ± 0.0013 |
| exp1.0 ! | 2.2446 ± 0.3141 | 0.5228 ± 0.0177 | 2.3982 ± 0.0896 | 0.0356 ± 0.0004 | 0.1548 ± 0.0021 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 0.5186 ± 0.0075 | 0.5152 ± 0.0074 | 11.2374 ± 7.1007 | 0.0323 ± 0.0015 | 0.7541 ± 0.4818 |
| exp0.05 | 0.5073 ± 0.0046 | 0.5062 ± 0.0030 | 8.0725 ± 8.6962 | 0.0322 ± 0.0015 | 0.5393 ± 0.5920 |
| exp0.1 | 0.5067 ± 0.0042 | 0.5051 ± 0.0026 | 12.0630 ± 8.5795 | 0.0323 ± 0.0018 | 0.8028 ± 0.5727 |
| exp0.25 | 0.5220 ± 0.0275 | 0.5085 ± 0.0015 | 14.3620 ± 9.2576 | 0.0312 ± 0.0012 | 0.9299 ± 0.6075 |
| exp0.5 ! | 0.5109 ± 0.0603 | 0.5610 ± 0.0819 | 12.3092 ± 12.4384 | 0.0273 ± 0.0057 | 0.6835 ± 0.6931 |
| exp0.75 ! | 0.4599 ± 0.0777 | 0.6572 ± 0.1594 | 25.8109 ± 17.1879 | 0.0294 ± 0.0025 | 1.3353 ± 0.8605 |
| exp1.0 ! | 0.3859 ± 0.2104 | 0.7969 ± 0.2571 | 21.9983 ± 20.3273 | 0.0282 ± 0.0097 | 1.1012 ± 1.0438 |

---

## cmplx_ps

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 6.7444 ± 0.0054 | 1.6682 ± 0.0020 | 6.7369 ± 0.0017 | 0.1206 ± 0.0001 | 0.4618 ± 0.0005 |
| exp0.05 | 6.7391 ± 0.0039 | 1.6667 ± 0.0019 | 6.7250 ± 0.0068 | 0.1206 ± 0.0001 | 0.4612 ± 0.0003 |
| exp0.1 | 6.8029 ± 0.1142 | 1.6727 ± 0.0092 | 6.7975 ± 0.1273 | 0.1210 ± 0.0006 | 0.4663 ± 0.0088 |
| exp0.25 | 6.8592 ± 0.2158 | 1.6755 ± 0.0158 | 6.8685 ± 0.2518 | 0.1207 ± 0.0002 | 0.4689 ± 0.0137 |
| exp0.5 ! | 6.7446 ± 0.0534 | 1.6773 ± 0.0148 | 6.7849 ± 0.0773 | 0.1212 ± 0.0009 | 0.4646 ± 0.0054 |
| exp0.75 ! | 6.5645 ± 0.0288 | 1.6707 ± 0.0016 | 6.7500 ± 0.0163 | 0.1207 ± 0.0001 | 0.4623 ± 0.0004 |
| exp1.0 ! | 6.2728 ± 0.0412 | 1.6755 ± 0.0008 | 6.7829 ± 0.0201 | 0.1208 ± 0.0001 | 0.4627 ± 0.0004 |

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref |
|---|---|---|---|---|---|
| exp0.01 | 1.6741 ± 0.0097 | 1.6755 ± 0.0063 | 9.5300 ± 2.0449 | 0.1129 ± 0.0073 | 0.6249 ± 0.1180 |
| exp0.05 | 1.6760 ± 0.0107 | 1.6731 ± 0.0105 | 9.8652 ± 2.1592 | 0.1118 ± 0.0085 | 0.6471 ± 0.1290 |
| exp0.1 | 1.6741 ± 0.0052 | 1.6741 ± 0.0034 | 11.1912 ± 0.5429 | 0.1055 ± 0.0101 | 0.7101 ± 0.0021 |
| exp0.25 | 1.6732 ± 0.0140 | 1.6736 ± 0.0022 | 11.3863 ± 1.9101 | 0.1031 ± 0.0109 | 0.7008 ± 0.0838 |
| exp0.5 ! | 1.6615 ± 0.0293 | 1.6790 ± 0.0041 | 15.3509 ± 1.3271 | 0.0912 ± 0.0071 | 0.8495 ± 0.0650 |
| exp0.75 ! | 1.4715 ± 0.1611 | 1.7131 ± 0.0366 | 16.1898 ± 3.6653 | 0.0923 ± 0.0198 | 0.9006 ± 0.1433 |
| exp1.0 ! | 1.2362 ± 0.0596 | 1.7165 ± 0.0136 | 20.1226 ± 4.3718 | 0.0787 ± 0.0202 | 1.0152 ± 0.1438 |

---

# RESULTS (Dense Table)

---

## naive_ps

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 0.5186 ± 0.0075 | 2.2600 ± 0.0140 |
| exp0.05 | 0.5073 ± 0.0046 | 2.2434 ± 0.0047 |
| exp0.1 | 0.5067 ± 0.0042 | 2.2350 ± 0.0035 |
| exp0.25 | 0.5220 ± 0.0275 | 2.2379 ± 0.0266 |
| exp0.5 ! | 0.5109 ± 0.0603 | 2.2466 ± 0.1452 |
| exp0.75 ! | 0.4599 ± 0.0777 | 2.2219 ± 0.2080 |
| exp1.0 ! | 0.3859 ± 0.2104 | 2.2446 ± 0.3141 |

---

## cmplx_ps

NELBO, CE are wloss while setting loss = polar_poincare_disk and cross_entropy respectively

| Proposal | NELBO | CE |
|---|---|---|
| exp0.01 | 1.6741 ± 0.0097 | 6.7444 ± 0.0054 |
| exp0.05 | 1.6760 ± 0.0107 | 6.7391 ± 0.0039 |
| exp0.1 | 1.6741 ± 0.0052 | 6.8029 ± 0.1142 |
| exp0.25 | 1.6732 ± 0.0140 | 6.8592 ± 0.2158 |
| exp0.5 ! | 1.6615 ± 0.0293 | 6.7446 ± 0.0534 |
| exp0.75 ! | 1.4715 ± 0.1611 | 6.5645 ± 0.0288 |
| exp1.0 ! | 1.2362 ± 0.0596 | 6.2728 ± 0.0412 |


---

# Insights and conclusions

## Verdict: the refactor reproduces `init_test` exactly — 84/84 cells, bit-exact

```
python experiments/compare_reproduction.py init_test_refactor init_test
  paired    : 84 cells   (tol = 1e-09 relative)
  bit-exact : 84/84
  worst relative difference, all 8 metrics: 0.000e+00
  VERDICT: REPRODUCED
```

The tables above are generated from runs pinned to `desa-compute-01` — the node
`init_test` itself ran on. That pinning is not a detail; see below.

Together with `init_opt_test_refactor` (210/210 bit-exact) that is **294 of 294
cells reproduced bit-exactly**, covering both the no-training and the trained
paths.

Stronger than the eight test scalars: the **entire optimization trajectory** is
identical. Comparing `loss_history.json` point-by-point across all 84 runs --
20000 `train_loss` points plus 2000 `val_loss` points each, **1,848,084 points
total** -- gives 84/84 runs with byte-identical curves, worst relative difference
`0.000e+00`. Matching endpoints alone would leave room for two different
trajectories coincidentally landing near each other; matching every step does not.
The post-refactor model is not merely equivalent to the pre-refactor one, it is
the same model.

Beyond the eight scalars, the recorder output matches too: all 84 runs emit
`{train_loss: 20000, val_loss: 2000, test_loss: 1}`, the same series shape as the
reference's `st20000` runs, and all 84 `loss_curves.jpg` render. That specifically
retires the one refactor defect that produced no error at all — the recorder
series had been renamed to `train_wloss` / `valid_wloss`, which
`plot_loss_curves` does not look for, silently emptying the train and validation
curves.

## Trained-cell reproduction is architecture-bound; the no-training companion is not

The first pass of this grid deliberately used every desa + thickstun GPU. It came
back **23/84 bit-exact**, which reads like a refactor bug until you group by node:

| node | arch | bit-exact | max rel diff |
|---|---|---|---|
| `desa-compute-01` | 2080 Ti, `sm_75` | **23 / 23** | 0.000e+00 |
| `kuleshov-compute-02` | A6000, `sm_86` | 0 / 26 | 8.859e-01 |
| `kuleshov-compute-03` | A5000, `sm_86` | 0 / 35 | 7.866e-01 |

Perfectly separated, no exceptions in either direction: every cell that ran on the
reference's own architecture reproduced bit-exactly, and no cell on any other
architecture did. 20000 optimizer steps amplify ULP-level differences in cuBLAS
kernel selection and reduction order into visibly different trajectories, and the
`poincare_polar` objective — heavy-tailed `1/q(t)` weights, `gradient_clip_val`
load-bearing against NaN — amplifies hardest, which is why it dominated the
worst-offender list even though `cross_entropy` drifted just as often (21 ce vs
17 pp non-exact).

The companion project settles it. `init_opt_test_refactor` runs the same code with
`mode=opt`, so `trainer.fit` is skipped and nothing accumulates — and it
reproduced bit-exactly on **all three** architectures, 210/210. Same code, same
metric plumbing, same bridge and loss; the only difference is whether 20000
gradient steps ran. So the drift is hardware, not the refactor.

That first pass is preserved at `output/init_test_refactor_allgpu/` rather than
discarded — it is the evidence for this section, and it is a standing caution:
**cross-architecture comparison of trained cells in this repo is not meaningful at
better than ~1e-1 relative.** Any future reproduction or A/B of a *trained* result
must pin `--nodelist`, which `sweep.py` now supports. Note that SLURM validates
`--nodelist` against the FIRST partition listed, so `--partition desa` must
accompany `--nodelist desa-compute-01`; `--partition thickstun,desa` is rejected
outright with "Requested nodes not in this partition".

## Other checks that passed

- **`test_wnelbo_ref >= H(p)`** in every trained cell modulo estimator noise
  (`H(naive_ps) = 0.500288`, `H(cmplx_ps) = 1.666363`). The trained model sits
  essentially at the Bayes optimum: `naive_ps` reaches 0.5002–0.5228 depending on
  loss proposal rate. The marginal sub-`H` readings at the tight rates are
  estimator, not model, and are present identically in the reference.
- **The variance cliff is intact.** `wloss` std widens sharply for rates above
  ≈ 0.304 (`exp0.5` 0.1452, `exp0.75` 0.2080, `exp1.0` 0.3141 for `naive_ps` CE)
  while `{0.01, 0.05, 0.1, 0.25}` stay tight — the same estimator behaviour the
  original project characterized.
- **The RNG seam survived.** `_make_step_generator` now reads `self.seed` (set by
  the subclass) where it previously read `self.config.seed`. Bit-exact `wloss` and
  `wloss_std` across all 84 cells means the seed sequence, and therefore every `t`
  draw, is unchanged.
