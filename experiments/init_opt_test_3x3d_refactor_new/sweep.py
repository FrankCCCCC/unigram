#!/usr/bin/env python
"""init_opt_test_3x3d_refactor_new sweep: BAYES-OPTIMAL model on the PRODUCT
manifold H^3 x H^3 x H^3, across ten curvature vectors.

Grid is exactly experiments/init_opt_test_3x3d_refactor_new/setup.md:

    ps                     {naive_ps, cmplx_ps, c1e3_exp1.0, c1e4_exp1.0}
    prod_factor_dim        [3,3,3]  (fixed)
    prod_factor_gaussian_curvature
        [-0.01,-10.0,-1.0]  (the MIXED vector)
        and the nine uniform vectors [K,K,K] for
        K in {-0.01, -0.05, -0.1, -0.5, -1.0, -2.0, -3.0, -4.0, -10.0}
    loss_proposal_type     {stratified_exp}
    loss_proposal_exp_rate {0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0}
    loss_geometry          {cross_entropy, poincare_polar, var_cross_entropy}
    seed                   {0, 1, 2}
    fixed: mode=opt, lr=1e-3, max_steps=20000, gradient_clip_val=1.0,
           test_size=4e6, batch_size=2048,
           ref_proposal_type=stratified_exp, ref_proposal_exp_rate=0.1

4 x 10 x 7 x 3 x 3 = 2520 runs, one SLURM job each.

The curvature VECTOR is swept, so it goes in the run name as the `x`-joined tag
(`_k--0.01x-10.0x-1.0`) and `Project.prod_curvature_for` rebuilds the hydra list
per cell; report.py's `k_sort_key` parses that tag. Both proposals are
`stratified_exp`: `Proposal.proposal` gates plain `exp` behind `allowed_exp`
(commit 40e02bd), which `hyper_proposal` never passes.

mode=opt skips trainer.fit, so lr / max_steps are inert and only the 4M-sample
test pass runs. OptimalModelRefactor is deterministic and has no parameters, so
this project is the CONTROL for its trained twins init_test_3x3d_refactor_new and
init_test_log_vce_3x3d_refactor_new: it says what test_wnelbo_ref the exact
posterior scores on each product geometry under the pinned stratified_exp(0.1)
reference proposal, and where that lands below H(p) the estimator is at fault,
not the model.

main_refactor.py clamps the heat time to the MINIMUM over factors of
`_radial_t_max(3) * R_m^2`. In the mixed vector the K = -10 factor (R^2 = 0.1,
ceiling 9.7) sets the ceiling for the whole product; a uniform vector has no
sharper factor to bind it, so [-0.01,-0.01,-0.01] keeps the flat ceiling (9700)
and is the control for that mechanism.

The reference metrics must be IDENTICAL across all 21 (geometry, rate) cells of
a given (ps, K, seed): the reference pass runs on its own RNG stream (salt=1).

ORCHESTRATION ONLY: submits script/train/{ce,pp,vce}_refactor.sh; never inlines
the trainer. Idempotent and resumable.

Run this from a LOGIN node (compute nodes have no slurm.conf):
    cd <repo> && python experiments/init_opt_test_3x3d_refactor_new/sweep.py --dry-run
    python experiments/init_opt_test_3x3d_refactor_new/sweep.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sweep_lib import Project, main  # noqa: E402

UNIFORM = ["-0.01", "-0.05", "-0.1", "-0.5", "-1.0", "-2.0", "-3.0", "-4.0", "-10.0"]

PROJECT = Project(
    name="init_opt_test_3x3d_refactor_new",
    mode="opt",
    geometries=["ce", "pp", "vce"],
    proposals=["stratified_exp"],
    ref_proposal="stratified_exp",
    prod_dim="[3,3,3]",
    curvatures=["-0.01x-10.0x-1.0"] + [f"{k}x{k}x{k}" for k in UNIFORM],
)

if __name__ == "__main__":
    main(PROJECT, __doc__)
