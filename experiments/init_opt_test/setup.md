# ELBO for Optimal Model, Loss Type and Proposal with 3 Seeds Avg

---

- Project name: ``init_opt_test``

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
- ``max_steps``: 20000
- ``gradient_clip_val``: 1.0
- ``test_size``: 4000000
- ``batch_size``: 2048
- ``seed``: {0, 1, 2}

### Ref ELBO & CE
- ``ref_proposal_type``: exp
- ``ref_proposal_exp_rate``: 0.1

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