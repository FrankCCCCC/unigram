#!/usr/bin/env python
"""init_test_log_vce_3x3d_refactor_new sweep: the VARIATIONAL CE objective on a
PRODUCT manifold H^3 x H^3 x H^3, across ten curvature vectors.

Grid is exactly experiments/init_test_log_vce_3x3d_refactor_new/setup.md:

    ps                     {naive_ps, cmplx_ps, c1e4_exp1.0}
    prod_factor_dim        [3,3,3]  (fixed)
    prod_factor_gaussian_curvature
        [-0.01,-10.0,-1.0]  (the MIXED vector)
        and the nine uniform vectors [K,K,K] for
        K in {-0.01, -0.05, -0.1, -0.5, -1.0, -2.0, -3.0, -4.0, -10.0}
    loss_proposal_type     {stratified_exp}
    loss_proposal_exp_rate {0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0}
    loss_geometry          {var_cross_entropy}
    seed                   {0, 1, 2}
    fixed: mode=tnb, lr=1e-3, max_steps=20000, gradient_clip_val=1.0,
           test_size=4e6, batch_size=2048,
           ref_proposal_type=stratified_exp, ref_proposal_exp_rate=0.1

3 x 10 x 7 x 1 x 3 = 630 runs, one SLURM job each.

The curvature VECTOR is what is swept, so it goes in the run name as the
`x`-joined tag (`_k--0.01x-10.0x-1.0`) and `Project.prod_curvature_for` rebuilds
the hydra list per cell. report.py's `k_sort_key` already parses that tag.

Why the product is not just "three times the single manifold":

1. **One heat-time ceiling for all three factors.** `main_refactor.py` clamps `t`
   to the MINIMUM over factors of `_radial_t_max(3) * R_m^2`. In the mixed vector
   the K = -10 factor (ceiling 9.7) sets it for the whole product, far tighter
   than the K = -0.01 factor (ceiling 9700) would alone -- so the flat factor is
   sampled only over a sliver of its natural range.
2. **The weight SUMS over factors.** `var_cross_entropy` is
   `CE * sum_m (d_m-1)^2 kappa_m^2 / (min_v D_{e_v,m})^2`, so the sharpest factor
   dominates the weight while the flattest dominates the variance. The `d+2`
   identity of vce_bayes.md is exact only at M = 1; what survives at M > 1 is the
   property that actually matters -- the weight is a function of `z_t` alone, so
   the Bayes posterior is still the minimiser.
3. **D = 9 triples the tensors.** The readout and the min-over-vocabulary weight
   both materialise (batch, V, M, d) float64, which is what drives the cost model
   and node eligibility.

ORCHESTRATION ONLY: submits script/train/vce_refactor.sh; never inlines the
trainer. Idempotent and resumable.

Run this from a LOGIN node (compute nodes have no slurm.conf):
    cd <repo> && python experiments/init_test_log_vce_3x3d_refactor_new/sweep.py --dry-run
    python experiments/init_test_log_vce_3x3d_refactor_new/sweep.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sweep_lib import Project, main  # noqa: E402

UNIFORM = ["-0.01", "-0.05", "-0.1", "-0.5", "-1.0", "-2.0", "-3.0", "-4.0", "-10.0"]

PROJECT = Project(
    name="init_test_log_vce_3x3d_refactor_new",
    mode="tnb",
    ps_list=["naive_ps", "cmplx_ps", "c1e4_exp1.0"],
    geometries=["vce"],
    proposals=["stratified_exp"],
    ref_proposal="stratified_exp",
    prod_dim="[3,3,3]",
    curvatures=["-0.01x-10.0x-1.0"] + [f"{k}x{k}x{k}" for k in UNIFORM],
)

if __name__ == "__main__":
    main(PROJECT, __doc__)
