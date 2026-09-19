## ELBO Mean and Variance for Adaptive Product Manifold with 3 Seeds Avg

---

- Project name: ``init_opt_3x3d_ada_prod``
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
- ``mode``: ``opt``
- ``word_embedding``: {output/init_opt_3x3d_ada_prod/pre_trained_models/ps-c1e4_exp1.0_k--0.05_lg-ce_q-exp0.05_qref-exp0.1_lr0.001_st20000_s0, unigram/output/init_opt_3x3d_ada_prod/pre_trained_models/ps-c1e4_exp1.0_k--0.5_lg-ce_q-exp0.05_qref-exp0.1_lr0.001_st20000_s0, unigram/output/init_opt_3x3d_ada_prod/pre_trained_models/ps-c1e4_exp1.0_k--0.1_lg-ce_q-exp0.05_qref-exp0.1_lr0.001_st20000_s0} 
(load pre-trained word embedding and freeze it)

### Ref ELBO & CE
- ``ref_proposal_type``: stratified_exp
- ``ref_proposal_exp_rate``: 0.1

### Result Presentation

- Report point-estimate mean and variance of wloss, wnelbo_ref, wce_ref, nelbo_ref, and ce_ref. Report the average of point-estimate mean and variance across 3 seeds.

---

# TODO

Read Agent.md and Refer to /home/sc3379/workspace/research/unigram-dev/unigram/experiments/init_opt_test_3x3d_refactor_new and /home/sc3379/workspace/research/unigram-dev/unigram/experiments/init_test_3x3d_refactor_new , vary the curvature of every component of  prod_factor_gaussian_curvature to achieve as low test_wloss_ref_std (poincare_polar) variance(std) as possible while tight test_wloss_ref to the training dataset entropy. Do the same thing for 3 different word embeddings. Find the lowest test_wloss_ref_std for each word embedding while tight test_wloss_ref to the training dataset entropy.

Use any GPUs in the cluster, use small GPU like 2080ti etc as many as possible to avoid preempt by priviledged users. If Desa and thickstun partitions have available GPUs, use them.

Refer to /home/sc3379/workspace/research/unigram-dev/unigram/experiments/init_opt_3x3d_ada_prod/imgs, My Intuitition is that since the word embedding concentrates on single or bi-pole, which induce oval geometry, single global curvature might not be the best option for this situation, an adaptive curvature on different direction should yield a oval geometry, suitable to this word embedding.

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
