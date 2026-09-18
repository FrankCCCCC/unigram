#!/usr/bin/env python
"""init_test_log_vce_3d_refactor_new sweep: the VARIATIONAL CE objective on a
single H^3, across nine curvatures.

Grid is exactly experiments/init_test_log_vce_3d_refactor_new/setup.md:

    ps                     {naive_ps, cmplx_ps, c1e4_exp1.0}
    gaussian_curvature     {-1.0, -2.0, -3.0, -4.0, -10.0, -0.5, -0.1, -0.05, -0.01}
    loss_proposal_type     {stratified_exp}
    loss_proposal_exp_rate {0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0}
    loss_geometry          {var_cross_entropy}
    seed                   {0, 1, 2}
    fixed: mode=tnb, hyper_dim=3, lr=1e-3, max_steps=20000,
           gradient_clip_val=1.0, test_size=4e6, batch_size=2048,
           ref_proposal_type=stratified_exp, ref_proposal_exp_rate=0.1

3 x 9 x 7 x 1 x 3 = 567 runs, one SLURM job each.

`var_cross_entropy` is `Loss.bridge_loss_variational_crossentropy_refactor`: the
denominator-weighted denoising CE that upper-bounds the shared-D_x angular
path-KL, with each factor's denominator taken as `min_v D_{e_v,m}` over the whole
vocabulary. That minimum is what makes the weight a function of `z_t` alone, and
hence what keeps the Bayes posterior the minimiser -- a target-indexed weight
instead optimises the tilted posterior `q*w` and leaves the ELBO ~48% above
`H(p)`. The derivation is in vce_bayes.md; the measurement that motivated it is
in RESULTS.md.

The weight still grows like `e^{2 kappa_m rho_m}` and is UNBOUNDED, unlike the
`poincare_polar` ELBO, so the whole weighted loss is accumulated in log space.
Curvature sets `kappa = sqrt(-K)` and therefore how fast that blow-up happens,
which is why it is the axis this project sweeps.

Both proposals are `stratified_exp`: `Proposal.proposal` gates plain `exp` behind
`allowed_exp` (commit 40e02bd), and one stratum per batch element keeps the batch
mean off the mercy of whichever sample landed at the largest `t`.

The check the project exists for is Invariant 2: `test_wnelbo_ref`, measured on
the independent reference path, must land at or above `H(p)` -- and with the
Bayes-posterior loss it should land CLOSE. init_test_3d_refactor_new runs the
same grid on `cross_entropy` / `poincare_polar` as the baseline.

ORCHESTRATION ONLY: submits script/train/vce_refactor.sh; never inlines the
trainer. Idempotent and resumable.

Run this from a LOGIN node (compute nodes have no slurm.conf):
    cd <repo> && python experiments/init_test_log_vce_3d_refactor_new/sweep.py --dry-run
    python experiments/init_test_log_vce_3d_refactor_new/sweep.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sweep_lib import Project, main  # noqa: E402

PROJECT = Project(
    name="init_test_log_vce_3d_refactor_new",
    mode="tnb",
    ps_list=["naive_ps", "cmplx_ps", "c1e4_exp1.0"],
    geometries=["vce"],
    proposals=["stratified_exp"],
    ref_proposal="stratified_exp",
    hyper_dim=3,
    curvatures=["-1.0", "-2.0", "-3.0", "-4.0", "-10.0",
                "-0.5", "-0.1", "-0.05", "-0.01"],
)

if __name__ == "__main__":
    main(PROJECT, __doc__)
