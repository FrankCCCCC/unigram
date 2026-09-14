#!/usr/bin/env python
"""init_opt_test_3x3d_refactor_new sweep: BAYES-OPTIMAL model on the product H^3 x H^3 x H^3.

Grid is exactly experiments/init_opt_test_3x3d_refactor_new/setup.md:

    ps                     {naive_ps, cmplx_ps, c1e3_exp1.0, c1e4_exp1.0}
    loss_proposal_type     {exp}
    loss_proposal_exp_rate {0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0}
    loss_geometry          {cross_entropy, poincare_polar}
    seed                   {0, 1, 2}
    prod_factor_gaussian_curvature
                           {[-0.01,-10.0,-1.0], [-0.01,-0.01,-0.01],
                            [-0.05,-0.05,-0.05], [-0.1,-0.1,-0.1],
                            [-0.5,-0.5,-0.5], [-1.0,-1.0,-1.0], [-2.0,-2.0,-2.0],
                            [-3.0,-3.0,-3.0], [-4.0,-4.0,-4.0], [-10.0,-10.0,-10.0]}
    fixed: mode=opt, prod_factor_dim=[3,3,3],
           lr=1e-3, max_steps=20000, gradient_clip_val=1.0,
           test_size=4e6, batch_size=2048,
           ref_proposal_type=exp, ref_proposal_exp_rate=0.1

4 x 10 x 7 x 2 x 3 = 1680 runs, one SLURM job each.

The swept geometry is the per-factor curvature vector, and it goes in the run
name as `_k-[k1,k2,k3]` -- the same `_k-` slot the single-manifold projects put a
scalar K in, so experiments/report.py parses these runs unchanged. Nine of the
ten vectors are homogeneous, which is what makes them comparable one-for-one
against init_opt_test_3d_refactor_new's nine single-manifold curvatures; the
eighth, [-0.01,-10.0,-1.0], is the MIXED one -- three radii inside one model.

mode=opt skips trainer.fit, so lr / max_steps are inert and only the 4M-sample
test pass runs. OptimalModelRefactor is deterministic and has no parameters, so
this project is the CONTROL for its trained twin init_test_3x3d_refactor_new: it
says what test_wnelbo_ref the exact posterior scores on this product geometry
under the pinned exp(0.1) reference proposal, and where that lands below H(p)
the estimator is at fault, not the model.

It is also the product-manifold counterpart of init_opt_test_3d_refactor_new.
Each factor contributes its own intrinsic radius, and the model input is
(rho_1, rho_2, rho_3) plus the concatenated unit directions, so D = 9.

main_refactor.py clamps the heat time to the MINIMUM over factors of
`_radial_t_max(3) * R_m^2`, so on the mixed vector the K = -10 factor
(R^2 = 0.1, ceiling 9.7) sets the ceiling for the whole product -- much tighter
than the K = -0.01 factor alone would give. On a homogeneous vector the ceiling
is just that curvature's, which is what isolates "three factors" from "three
different radii".

ORCHESTRATION ONLY: submits script/train/{ce_redactor,pp_refactor}.sh; never
inlines the trainer. Idempotent and resumable.

Run this from a LOGIN node (compute nodes have no slurm.conf):
    cd <repo> && python experiments/init_opt_test_3x3d_refactor_new/sweep.py --dry-run
    python experiments/init_opt_test_3x3d_refactor_new/sweep.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sweep_lib import Project, main  # noqa: E402

PROJECT = Project(
    name="init_opt_test_3x3d_refactor_new",
    mode="opt",
    prod_dim="[3,3,3]",
    curvatures=["[-0.01,-10.0,-1.0]", "[-0.01,-0.01,-0.01]", "[-0.05,-0.05,-0.05]",
                "[-0.1,-0.1,-0.1]", "[-0.5,-0.5,-0.5]", "[-1.0,-1.0,-1.0]",
                "[-2.0,-2.0,-2.0]", "[-3.0,-3.0,-3.0]", "[-4.0,-4.0,-4.0]",
                "[-10.0,-10.0,-10.0]"],
)

if __name__ == "__main__":
    main(PROJECT, __doc__)
