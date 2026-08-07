# ELBO for Training Step, Loss Type and Proposal with 3 Seeds Avg

---

- Project name: ``init_test``

### Dataset
- ``ps``: {``naive_ps``, ``cmplx_ps``, ``c1e2_exp1.0``, ``c1e3_exp1.0``, ``c1e4_exp1.0``}
    - ``naive_ps``: [0.91,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]
    - ``cmplx_ps``: [0.31,0.01,0.2,0.01,0.01,0.3,0.08,0.04,0.03,0.01]
    - ``c1e2_exp1.0``: class=100, $\exp(\lambda=1.0)$
    - ``c1e3_exp1.0``: class=1000, $\exp(\lambda=1.0)$
    - ``c1e4_exp1.0``: class=10000, $\exp(\lambda=1.0)$

### Training
- ``hyper_dim``: 2
- ``loss_proposal_type``: {exp}
- ``loss_proposal_exp_rate``: {0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0}
- ``loss_geometry``: {``cross_entropy``, ``poincare_polar``}
- ``lr``: 0.001
- ``max_steps``: {20000, 40000, 100000, 200000}
- ``gradient_clip_val``: 1.0
- ``test_size``: 4000000
- ``batch_size``: 2048
- ``seed``: {0, 1, 2}

### Ref ELBO & CE
- ``ref_proposal_type``: exp
- ``ref_proposal_exp_rate``: 0.1

---

# Results of naive_ps

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

# Results of cmplx_ps

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

---

# Results of c1e2_exp1.0

---

## c1e2_exp1.0, Training Step 20000

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

---

# Results of c1e3_exp1.0

---

## c1e3_exp1.0, Training Step 20000

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

---

## Results of c1e4_exp1.0

---

## c1e4_exp1.0, Training Step 20000

Each cell: avg & std across seed

**CE**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|

**Polar ELBO**

| loss Proposal | wloss | wnelbo_ref | wce_ref | nelbo_ref | ce_ref | 
|---|---|---|---|---|---|---|