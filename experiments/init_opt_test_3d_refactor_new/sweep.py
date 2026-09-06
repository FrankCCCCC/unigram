#!/usr/bin/env python
"""init_opt_test_3d_refactor_new sweep: BAYES-OPTIMAL model on H^3 at three curvatures.

Grid is exactly experiments/init_opt_test_3d_refactor_new/setup.md:

    ps                     {naive_ps, cmplx_ps, c1e3_exp1.0, c1e4_exp1.0}
    gaussian_curvature     {-1.0, -10.0, -0.01}
    loss_proposal_type     {exp}
    loss_proposal_exp_rate {0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0}
    loss_geometry          {cross_entropy, poincare_polar}
    seed                   {0, 1, 2}
    fixed: mode=opt, hyper_dim=3, lr=1e-3, max_steps=20000,
           gradient_clip_val=1.0, test_size=4e6, batch_size=2048,
           ref_proposal_type=exp, ref_proposal_exp_rate=0.1

4 x 3 x 7 x 2 x 3 = 504 runs, one SLURM job each.

mode=opt skips trainer.fit, so lr / max_steps are inert and only the 4M-sample
test pass runs. OptimalModelRefactor is deterministic and has no parameters, so
this project is the CONTROL for its trained twin init_test_3d_refactor_new: at
each curvature it says what test_wnelbo_ref the exact posterior scores under the
pinned exp(0.1) reference proposal. Where that lands below H(p) the estimator is
at fault, not the model -- and curvature is expected to move it, because the
heat-time ceiling main_refactor.py clamps to is `_radial_t_max(3) * R^2` with
R = 1/sqrt(-K), i.e. 9.7 at K = -10 and 9700 at K = -0.01, so the per-t loss
decays ~R^2 times more slowly while the proposal stays pinned.

Two free correctness checks to read off the results:
  * test_wnelbo_ref / test_wce_ref come from the REFERENCE pass, pinned to
    exp(0.1) on its own RNG stream (salt=1) and independent of the swept loss
    geometry and rate. They must be IDENTICAL across all 14 (geometry, rate)
    cells of a given (ps, K, seed).
  * test_wloss is the swept objective. Rates above ~0.304 have infinite variance
    at K = -1, so those cells legitimately fan out across seeds.

ORCHESTRATION ONLY: submits script/train/{ce_redactor,pp_refactor}.sh; never
inlines the trainer. Idempotent and resumable.

Run this from a LOGIN node (compute nodes have no slurm.conf):
    cd <repo> && python experiments/init_opt_test_3d_refactor_new/sweep.py --dry-run
    python experiments/init_opt_test_3d_refactor_new/sweep.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sweep_lib import Project, main  # noqa: E402

PROJECT = Project(
    name="init_opt_test_3d_refactor_new",
    mode="opt",
    hyper_dim=3,
    curvatures=["-1.0", "-10.0", "-0.01"],
)

if __name__ == "__main__":
    main(PROJECT, __doc__)
