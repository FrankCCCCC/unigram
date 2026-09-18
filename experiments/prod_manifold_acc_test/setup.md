# # ELBO for Training Step, Loss Type and Proposal with 3 Seeds Avg

---

- Project name: ``prod_manifold_acc_test``
- Use ``main_refactor.py`` and scripts ``script/train/ce_redactor.sh`` and ``script/train/pp_refactor.sh``

### Dataset
- ``ps``: {``naive_ps``, ``cmplx_ps``, ``c1e4_exp1.0``}
    - ``naive_ps``: [0.91,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]
    - ``cmplx_ps``: [0.31,0.01,0.2,0.01,0.01,0.3,0.08,0.04,0.03,0.01]
    - ``c1e4_exp1.0``: exp_decay_ps(n=10000, lam=1.0)

### Training
- ``loss_proposal_type``: {exp}
- ``loss_proposal_exp_rate``: {0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0}
- ``loss_geometry``: {``cross_entropy``, ``poincare_polar``}
- Product Manifold:
    - (prod_factor_dim: [3,3,3], prod_factor_gaussian_curvature: [-0.01, -10.0, -1.0])
    - (prod_factor_dim: [3,3,3], prod_factor_gaussian_curvature: [-0.01, -0.01, -0.01])
    - (prod_factor_dim: [3,3,3], prod_factor_gaussian_curvature: [-0.05, -0.05, -0.05])
    - (prod_factor_dim: [3,3,3], prod_factor_gaussian_curvature: [-1.0, -1.0, -1.0])
    - (prod_factor_dim: [3,3,3], prod_factor_gaussian_curvature: [-3.0, -3.0, -3.0])
    - (prod_factor_dim: [3,3,3], prod_factor_gaussian_curvature: [-10.0, -10.0, -10.0])
- ``lr``: 0.001
- ``max_steps``: {20000}
- ``gradient_clip_val``: 1.0
- ``test_size``: 4000000
- ``batch_size``: 2048
- ``seed``: {0, 1, 2}
- ``mode``: ``opt``

### Ref ELBO & CE
- ``ref_proposal_type``: exp
- ``ref_proposal_exp_rate``: 0.1

### Result Presentation

- Report point-estimate mean and variance of wloss, wnelbo_ref, wce_ref, nelbo_ref, and ce_ref. Report the average of point-estimate mean and variance across 3 seeds.

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

## naive_ps, Training Step 40000

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

---

## naive_ps, Training Step 100000

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

---

## naive_ps, Training Step 200000

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

## cmplx_ps, Training Step 40000

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

---

## cmplx_ps, Training Step 100000

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

---

## cmplx_ps, Training Step 200000

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|
