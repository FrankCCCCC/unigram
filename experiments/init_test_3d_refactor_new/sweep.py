#!/usr/bin/env python
"""init_test_3d_refactor_new sweep: TRAINED model on a single H^3 at three curvatures.

Grid is exactly experiments/init_test_3d_refactor_new/setup.md:

    ps                     {naive_ps, cmplx_ps, c1e3_exp1.0, c1e4_exp1.0}
    gaussian_curvature     {-1.0, -10.0, -0.01}
    loss_proposal_type     {exp}
    loss_proposal_exp_rate {0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0}
    loss_geometry          {cross_entropy, poincare_polar}
    seed                   {0, 1, 2}
    fixed: mode=tnb, hyper_dim=3, lr=1e-3, max_steps=20000,
           gradient_clip_val=1.0, test_size=4e6, batch_size=2048,
           ref_proposal_type=exp, ref_proposal_exp_rate=0.1

4 x 3 x 7 x 2 x 3 = 504 runs, one SLURM job each.

Curvature is the new axis relative to init_refactor_3d, and it is not a cosmetic
rescaling: K fixes the radius R = 1/sqrt(-K), and the heat-time ceiling
main_refactor.py clamps to is `_radial_t_max(3) * R^2` = 97 * R^2 -- 9.7 at
K = -10 and 9700 at K = -0.01. The per-t loss therefore decays ~R^2 times more
slowly at K = -0.01, while the reference proposal stays pinned at exp(0.1), so
the weighted estimator's variance is a function of curvature. The matching
init_opt_test_3d_refactor_new project runs the SAME grid on the Bayes-optimal
model, which is what separates "the model is bad here" from "the estimator is".

ORCHESTRATION ONLY: submits script/train/{ce_redactor,pp_refactor}.sh; never
inlines the trainer. Idempotent and resumable.

Run this from a LOGIN node (compute nodes have no slurm.conf):
    cd <repo> && python experiments/init_test_3d_refactor_new/sweep.py --dry-run
    python experiments/init_test_3d_refactor_new/sweep.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sweep_lib import Project, main  # noqa: E402

PROJECT = Project(
    name="init_test_3d_refactor_new",
    mode="tnb",
    hyper_dim=3,
    curvatures=["-1.0", "-10.0", "-0.01"],
)

if __name__ == "__main__":
    main(PROJECT, __doc__)
