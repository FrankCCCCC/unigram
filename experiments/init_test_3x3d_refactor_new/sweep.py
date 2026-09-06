#!/usr/bin/env python
"""init_test_3x3d_refactor_new sweep: TRAINED model on the product H^3 x H^3 x H^3.

Grid is exactly experiments/init_test_3x3d_refactor_new/setup.md:

    ps                     {naive_ps, cmplx_ps, c1e3_exp1.0, c1e4_exp1.0}
    loss_proposal_type     {exp}
    loss_proposal_exp_rate {0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0}
    loss_geometry          {cross_entropy, poincare_polar}
    seed                   {0, 1, 2}
    fixed: mode=tnb, prod_factor_dim=[3,3,3],
           prod_factor_gaussian_curvature=[-0.01,-10.0,-1.0],
           lr=1e-3, max_steps=20000, gradient_clip_val=1.0,
           test_size=4e6, batch_size=2048,
           ref_proposal_type=exp, ref_proposal_exp_rate=0.1

4 x 7 x 2 x 3 = 168 runs, one SLURM job each.

The geometry is FIXED and lives in the project name, so run_name is
byte-identical to init_refactor_3d's and experiments/report.py parses these runs
unchanged. This is the product-manifold counterpart of
init_test_3d_refactor_new: the same three curvatures {-0.01, -10.0, -1.0}, but
carried by three simultaneous factors of one model instead of three separate
models. Each factor contributes its own intrinsic radius, and the model input is
(rho_1, rho_2, rho_3) plus the concatenated unit directions, so D = 9.

main_refactor.py clamps the heat time to the MINIMUM over factors of
`_radial_t_max(3) * R_m^2`, so the K = -10 factor (R^2 = 0.1, ceiling 9.7) sets
the ceiling for the whole product -- much tighter than the K = -0.01 factor
alone would give.

ORCHESTRATION ONLY: submits script/train/{ce_redactor,pp_refactor}.sh; never
inlines the trainer. Idempotent and resumable.

Run this from a LOGIN node (compute nodes have no slurm.conf):
    cd <repo> && python experiments/init_test_3x3d_refactor_new/sweep.py --dry-run
    python experiments/init_test_3x3d_refactor_new/sweep.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sweep_lib import Project, main  # noqa: E402

PROJECT = Project(
    name="init_test_3x3d_refactor_new",
    mode="tnb",
    prod_dim="[3,3,3]",
    prod_curvature="[-0.01,-10.0,-1.0]",
)

if __name__ == "__main__":
    main(PROJECT, __doc__)
