## ELBO Mean and Variance for Adaptive Product Manifold with 3 Seeds Avg

---

- Project name: ``init_3x3d_ada_prod``
- Use ``main_refactor.py`` and scripts ``script/train/ce_redactor.sh`` and ``script/train/pp_refactor.sh``

### Dataset
- ``ps``: {``naive_ps``, ``cmplx_ps``, ``c1e4_exp1.0``}
    - ``naive_ps``: [0.91,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]
    - ``cmplx_ps``: [0.31,0.01,0.2,0.01,0.01,0.3,0.08,0.04,0.03,0.01]
    - ``c1e4_exp1.0``: exp_decay_ps(n=10000, lam=1.0)

### Training
- ``loss_proposal_type``: {stratified_exp}
- ``loss_proposal_exp_rate``: {0.05}
- ``loss_geometry``: {``poincare_polar``}
- Product Manifold: prod_factor_dim: [3,3,3], prod_factor_gaussian_curvature: [-0.05, -0.05, -0.05]
- ``lr``: 0.001
- ``max_steps``: {20000}
- ``gradient_clip_val``: 1.0
- ``test_size``: 4000000
- ``batch_size``: 2048
- ``seed``: {0, 1, 2}
- ``mode``: ``tnb``

### Ref ELBO & CE
- ``ref_proposal_type``: stratified_exp
- ``ref_proposal_exp_rate``: 0.1

### Result Presentation

- Report point-estimate mean and variance of wloss, wnelbo_ref, wce_ref, nelbo_ref, and ce_ref. Report the average of point-estimate mean and variance across 3 seeds.

---

# TODO

Read Agent.md and Refer to /home/sc3379/workspace/research/unigram-dev/unigram/experiments/init_opt_test_3x3d_refactor_new and /home/sc3379/workspace/research/unigram-dev/unigram/experiments/init_test_3x3d_refactor_new , vary the curvature of every component of  prod_factor_gaussian_curvature to achieve as low test_wnelbo_ref_std (poincare_polar) variance(std) as possible while tight test_wnelbo_ref to the training dataset entropy.

---

# Results

---

## naive_ps, Training Step 20000

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

---

# Results

---

## cmplx_ps, Training Step 20000

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

---

# Results

---

## c1e4_exp1.0, Training Step 20000

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|
