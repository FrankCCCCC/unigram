#!/usr/bin/env python
"""prod_manifold_acc_test sweep: BAYES-OPTIMAL model on H^3 x H^3 x H^3, six curvature assignments.

Grid is exactly experiments/prod_manifold_acc_test/setup.md:

    ps                     {naive_ps, cmplx_ps, c1e4_exp1.0}
    prod_factor_gaussian_curvature
                           [-0.01,-10.0,-1.0]      (mixed)
                           [-x,-x,-x] for x in {0.01, 0.05, 1.0, 3.0, 10.0}
    loss_proposal_type     {exp}
    loss_proposal_exp_rate {0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0}
    loss_geometry          {cross_entropy, poincare_polar}
    seed                   {0, 1, 2}
    fixed: mode=opt, prod_factor_dim=[3,3,3], lr=1e-3, max_steps=20000,
           gradient_clip_val=1.0, test_size=4e6, batch_size=2048,
           ref_proposal_type=exp, ref_proposal_exp_rate=0.1

3 x 6 x 2 x 7 x 3 = 756 runs, one SLURM job each.

Unlike the four init_* projects, the swept axis here is the product CURVATURE
VECTOR, not a single-manifold curvature, so `k` is the vector's `x`-joined tag
(`-0.01x-10.0x-1.0`) -- the same tag the earlier product runs in
output/init_opt_test_3x3d_refactor_new/ already carry, so experiments/report.py
parses these unchanged.

WHY: this is the acceptance test for the tensorized product-manifold path. The
per-factor python loops in poincare_bridge_prod, horosphere_geometry and
bridge_loss_elbo_refactor became tensor ops over a factor axis, and sample_radial
now takes a per-factor curvature vector. Unit checks pin the deterministic parts
to <= 2e-15 against the loops, but the reported STATISTICS have never been
compared end to end. The `-0.01x-10.0x-1.0` cells re-run
init_opt_test_3x3d_refactor_new's published grid, so its table is the control.

mode=opt skips trainer.fit, so lr / max_steps are inert and only the 4M-sample
test pass runs; OptimalModelRefactor is deterministic and parameter-free, so each
cell reports what the EXACT posterior scores on that geometry.

Submitted to the cluster-wide `gpu` partition: thickstun,desa is saturated by
init_test_3x3d_refactor_new. That partition is heterogeneous, so cells are gated
by the cluster's gpu-low/mid/high FEATURES (--constraint) instead of by the
node-name exclusions sweep_lib uses for the four known nodes.

ORCHESTRATION ONLY: submits script/train/{ce_redactor,pp_refactor}.sh; never
inlines the trainer. Idempotent and resumable.

Run this from a LOGIN node (compute nodes have no slurm.conf):
    cd <repo> && python experiments/prod_manifold_acc_test/sweep.py --dry-run
    python experiments/prod_manifold_acc_test/sweep.py
"""

import dataclasses
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sweep_lib import Project, main  # noqa: E402

# setup.md's six product geometries, keyed by the `x`-joined run-name tag.
PROD_CURVATURES = [
    "[-0.01,-10.0,-1.0]",
    "[-0.01,-0.01,-0.01]",
    "[-0.05,-0.05,-0.05]",
    "[-1.0,-1.0,-1.0]",
    "[-3.0,-3.0,-3.0]",
    "[-10.0,-10.0,-10.0]",
]
BY_TAG = {"x".join(lit.strip("[]").split(",")): lit for lit in PROD_CURVATURES}

# GPU features on the wide `gpu` partition, by smallest card the feature admits:
# gpu-low ~ 11 GB (2080 Ti / 1080 Ti / Titan X), gpu-mid ~ 24 GB (3090 / A5000),
# gpu-high ~ 48 GB and up (A6000 / 6000 Ada / A100 / H200 / B200).
SMALL_VOCAB_CONSTRAINT = "gpu-low|gpu-mid|gpu-high"
LARGE_VOCAB_CONSTRAINT = "gpu-mid|gpu-high"
LARGE_VOCAB = {"c1e3_exp1.0", "c1e4_exp1.0"}


@dataclass(kw_only=True)
class ProductCurvatureProject(Project):
    """A project whose swept cell IS the product curvature vector.

    `Project` sweeps `curvatures` into the single-manifold `CURVATURE` env var
    and keeps `prod_curvature` fixed; here the sweep runs the other way round.
    """

    @property
    def geometry_cells(self) -> list[str]:
        return list(BY_TAG)

    def job_body(self, script, out_dir, ps, k, proposal, rate, seed):
        # `k` is the tag; the cell's geometry is the vector it names. CURVATURE
        # stays at its default and is inert -- main_refactor ignores hyper_dim /
        # gaussian_curvature once both product lists are set.
        cell = dataclasses.replace(self, prod_curvature=BY_TAG[k])
        return Project.job_body(cell, script, out_dir, ps, None, proposal, rate, seed)

    def constraint(self, ps: str) -> str:
        return LARGE_VOCAB_CONSTRAINT if ps in LARGE_VOCAB else SMALL_VOCAB_CONSTRAINT

    def time_limit(self, ps: str) -> str:
        # sweep_lib's model is calibrated on the four thickstun/desa nodes; the
        # wide partition reaches much slower fp64 cards (3090 / A5000 are 1/64
        # rate), and these are opt-mode cells where a generous wall limit costs
        # only backfill priority, never compute. A timeout would cost the whole
        # 4M-sample pass.
        return "01:30:00" if ps in LARGE_VOCAB else "00:30:00"

    def excluded_nodes(self, ps: str) -> str:
        # Superseded by `constraint`: the feature gate covers every node on the
        # wide partition, where the NODE_GPU_GB name list covers only four.
        return ""


PROJECT = ProductCurvatureProject(
    name="prod_manifold_acc_test",
    mode="opt",
    ps_list=["naive_ps", "cmplx_ps", "c1e4_exp1.0"],
    partition="gpu",
    prod_dim="[3,3,3]",
)

if __name__ == "__main__":
    main(PROJECT, __doc__)
