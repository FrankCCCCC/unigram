#!/usr/bin/env python
"""Shared SLURM submission machinery for the *_refactor_new projects.

The four projects init_{opt_,}test_{3d,3x3d}_refactor_new differ only in
(mode, geometry) -- the grid, the run-name scheme, the cost model and the
scheduling policy are identical -- so they live here once and each project's
``sweep.py`` supplies a :class:`Project` and calls :func:`main`.

ORCHESTRATION ONLY: this submits ``script/train/{ce_redactor,pp_refactor}.sh``;
it never inlines the trainer. Idempotent and resumable -- a cell is skipped when
its ``test_metrics.json`` exists or its job name is already in ``squeue``.

Run from a LOGIN node (compute nodes have no slurm.conf).
"""

from __future__ import annotations

import argparse
import itertools
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from simple_slurm import Slurm

REPO_DIR = Path(__file__).resolve().parents[1]
CONDA_BIN = "/home/sc3379/anaconda3/envs/sfm/bin"

# --- grid shared by all four setup.md files --------------------------------
PS_LIST = ["naive_ps", "cmplx_ps", "c1e3_exp1.0", "c1e4_exp1.0"]
PROPOSALS = ["exp"]
EXP_RATES = ["0.01", "0.05", "0.1", "0.25", "0.5", "0.75", "1.0"]
# abbreviation -> train script. The *_refactor scripts run main_refactor.py,
# which is the only entry point with the product-manifold bridge.
GEOMETRIES = {"ce": "script/train/ce_redactor.sh", "pp": "script/train/pp_refactor.sh"}
SEEDS = [0, 1, 2]
MAX_STEPS = 20000
LR = "0.001"
REF_PROPOSAL = "exp"
REF_RATE = "0.1"
TEST_SIZE = 4_000_000
BATCH_SIZE = 2048

# --- slurm -----------------------------------------------------------------
PARTITION = "thickstun,desa"
# Measured on the pilot: TotalCPU ~= Elapsed, i.e. ~1 core. The work is GPU-bound
# float64 tensor ops and the dataloader runs in-process (num_workers=0). The
# GPU-rich nodes are CPU-poor (desa-compute-01 is 36 CPUs to 8 GPUs), so a larger
# ask strands GPUs.
CPUS_PER_TASK = 2
MEM = "16G"

# Vocabulary size of each ps spec. The horosphere readout materializes several
# (batch, V, D) float64 tensors with D = sum(prod_factor_dim), so V*D drives both
# step time and peak GPU memory.
VOCAB = {"naive_ps": 10, "cmplx_ps": 10, "c1e3_exp1.0": 1000, "c1e4_exp1.0": 10000}

# Measured 2026-09-06 on an RTX 6000 Ada at batch 2048, from a 9-cell pilot
# (200 train steps + 200 test batches per cell; scratchpad, not checked in).
# Keyed by (V, D) with D = sum(prod_factor_dim), because the horosphere readout's
# (batch, V, D) float64 tensors drive both time and memory. SEC_PER_STEP is a
# train step INCLUDING its share of validation (Lightning validates every epoch,
# = every ~9 steps at train_size=20000) and the per-step reference pass.
SEC_PER_STEP = {(10, 3): 0.020, (1000, 3): 0.020, (10000, 3): 0.105,
                (10, 9): 0.040, (1000, 9): 0.045, (10000, 9): 0.290}
# Seconds for the 4M-sample (1954-batch) test pass: two bridge passes per batch,
# no backward.
TEST_SEC = {(10, 3): 30, (1000, 3): 40, (10000, 3): 60,
            (10, 9): 35, (1000, 9): 50, (10000, 9): 160}
# Interpreter + CUDA context + dataset build. Measured ~10 s; budgeted at 60 for
# a cold NFS import.
STARTUP_SEC = 60
# A limit shorter than this buys no backfill worth the risk of losing the cell.
MIN_LIMIT_SEC = 1200
# The rates above are the RTX 6000 Ada's. The other three nodes are slower, and
# the loss is float64-bound (the horosphere geometry and the whole polar loss are
# float64 by Invariant 3), so the spread follows fp64 throughput, not fp32.
# Calibrated against the Ada baseline and confirmed on two 20000-step validation
# cells: a (10, 3) cell on desa-compute-01 ran ~4x the Ada rate, a (10, 9) cell on
# kuleshov-compute-02 ~1.9x. A cell must fit the SLOWEST node it is eligible for,
# so time_limit() takes the max over the nodes excluded_nodes() leaves in play --
# budgeting everything at the 2080 Ti rate would make the c1e4 limits so loose
# they never backfill.
NODE_SLOWDOWN = {"thickstun-compute-01": 1.0, "kuleshov-compute-02": 2.5,
                 "kuleshov-compute-03": 3.5, "desa-compute-01": 4.5}
# Headroom on top of the slowest-eligible-node estimate. Lower than the 2x the
# earlier sweeps used because NODE_SLOWDOWN now carries the hardware spread
# explicitly instead of hiding it in the margin.
TIME_MARGIN = 1.5

# Peak GPU memory of one step (GiB), from the pilots' nvidia-smi poll, so it
# already includes the CUDA context. Taken at the WORST loss_geometry:
# poincare_polar runs the ELBO geometry on the loss pass AND the reference pass,
# where cross_entropy runs it only on the reference, so pp peaks ~1.3-1.4x higher
# and is what a cell must be sized for. Sizing on the ce measurement is exactly
# the mistake that cost two (10000, 9) cells to OOM on a 24 GB A5000.
#
# (10000, 3) is the one entry that is NOT its poll reading (10.5 GiB under pp on
# a 48 GB card): 11 such cells have since completed on desa-compute-01's 11 GB
# cards, so that poll is the caching allocator's reservation, not the
# requirement, and the ce figure is the honest bound. (10000, 9) is the
# opposite -- a real requirement, confirmed by an OOM at 23.5 GiB.
PEAK_GB = {(10, 3): 0.9, (1000, 3): 1.7, (10000, 3): 8.0,
           (10, 9): 0.9, (1000, 9): 3.1, (10000, 9): 25.4}
PEAK_GB_DEFAULT = 2.5
# Usable GPU memory per node, by the smallest card it offers.
NODE_GPU_GB = {"desa-compute-01": 10.5, "kuleshov-compute-03": 24.0,
               "kuleshov-compute-02": 48.0, "thickstun-compute-01": 48.0}
# Headroom over the measured peak. Only fragmentation: the poll already counted
# the context, and peak memory does not grow with step count. This excludes
# exactly one thing -- c1e4 on the product manifold (17.9 GiB) from the 2080 Ti
# node -- and keeps every other cell eligible for all four nodes.
GPU_MARGIN = 1.15

# Scheduling priority. In SLURM a HIGHER --nice means LOWER priority, so the
# primary seed goes in at nice=0 and the replicates queue behind it: a complete
# single-seed grid lands first and the replicates fill in afterwards. The
# rationale and the measured numbers behind every constant here are in
# experiments/init_refactor_3d/sweep.py; the short version is that a cell which
# does not fit every node must rank BELOW every cell that does, or it
# gate-keeps the small-GPU node it can never run on.
#
# --nice MUST be passed on the sbatch command line, not as a #SBATCH directive:
# its argument is OPTIONAL, so simple_slurm's space-separated "#SBATCH --nice 0"
# parses as --nice followed by a stray token and sbatch rejects the script.
PRIMARY_SEED = 0
NICE_REPLICATE = 100
NICE_BY_VOCAB = {10: 0, 1000: 10, 10000: 30}
NICE_EXCLUDED = 150          # base penalty for not fitting every node
NICE_PER_EXCLUDED_NODE = 30  # additional penalty per further excluded node


@dataclass(kw_only=True)
class Project:
    """What distinguishes one of the four projects from the others."""

    name: str
    mode: str  # "tnb" (train MLPLMRefactor) | "opt" (Bayes-optimal, no fit)
    # Single manifold H^hyper_dim: one run per swept curvature, and the
    # curvature goes in the run name. Product manifold: prod_dim / prod_curvature
    # are hydra list literals, the geometry is fixed and lives in the project
    # name, and curvatures is empty.
    hyper_dim: int = 3
    curvatures: list[str] = field(default_factory=list)
    prod_dim: str = "null"
    prod_curvature: str = "null"

    @property
    def total_dim(self) -> int:
        """D = sum(prod_factor_dim): the width of the (batch, V, D) tensors."""
        if self.prod_dim == "null":
            return self.hyper_dim
        return sum(int(d) for d in self.prod_dim.strip("[]").split(","))

    @property
    def geometry_cells(self) -> list[str | None]:
        """Curvature values to sweep, or [None] for the fixed product geometry."""
        return list(self.curvatures) if self.curvatures else [None]

    def out_root(self) -> Path:
        return Path("output") / self.name

    def log_dir(self) -> Path:
        return Path("experiments") / self.name / "logs"

    def run_name(self, ps: str, k: str | None, geom: str, proposal: str,
                 rate: str, seed: int) -> str:
        """Every SEARCHED variable appears here; the fixed geometry does not.

        The reference proposal is pinned by setup.md but is included anyway: if
        it ever changes, results computed under the old one must not silently
        share a directory with the new. experiments/report.py parses this back
        out, with `_k-<K>` optional.
        """
        k_tag = f"_k-{k}" if k is not None else ""
        return (f"ps-{ps}{k_tag}_lg-{geom}_q-{proposal}{rate}"
                f"_qref-{REF_PROPOSAL}{REF_RATE}_lr{LR}_st{MAX_STEPS}_s{seed}")

    def job_name(self, run: str) -> str:
        return f"{self.name}_{run}"

    def cost_key(self, ps: str) -> tuple[int, int]:
        return (VOCAB[ps], self.total_dim)

    def steps(self) -> int:
        # mode=opt skips trainer.fit, so only the test pass runs.
        return 0 if self.mode == "opt" else MAX_STEPS

    def time_limit(self, ps: str) -> str:
        key = self.cost_key(ps)
        excluded = set(self.excluded_nodes(ps).split(","))
        slowdown = max(f for node, f in NODE_SLOWDOWN.items() if node not in excluded)
        gpu_secs = slowdown * (self.steps() * SEC_PER_STEP[key] + TEST_SEC[key])
        secs = max(TIME_MARGIN * (STARTUP_SEC + gpu_secs), MIN_LIMIT_SEC)
        h, rem = divmod(int(secs), 3600)
        return f"{h:02d}:{rem // 60:02d}:00"

    def excluded_nodes(self, ps: str) -> str:
        """Nodes whose GPU cannot hold this cell, comma-joined ('' if none)."""
        need = PEAK_GB.get(self.cost_key(ps), PEAK_GB_DEFAULT) * GPU_MARGIN
        return ",".join(n for n, gb in NODE_GPU_GB.items() if gb < need)

    def job_nice(self, ps: str, seed: int) -> int:
        excl = self.excluded_nodes(ps)
        return ((0 if seed == PRIMARY_SEED else NICE_REPLICATE)
                + NICE_BY_VOCAB[VOCAB[ps]]
                + (NICE_EXCLUDED + NICE_PER_EXCLUDED_NODE * (len(excl.split(",")) - 1)
                   if excl else 0))

    def job_body(self, script: str, out_dir: Path, ps: str, k: str | None,
                 proposal: str, rate: str, seed: int) -> str:
        return f"""
export TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1
export SLURM_JOB_NAME=bash
export NCCL_P2P_DISABLE=1 NCCL_IB_DISABLE=1
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PATH={CONDA_BIN}:$PATH
cd {REPO_DIR}
OUTPUT_DIR={out_dir} \\
HYPER_DIM={self.hyper_dim} \\
CURVATURE={k if k is not None else "-1.0"} \\
PROD_DIM={self.prod_dim} \\
PROD_CURVATURE={self.prod_curvature} \\
PS={ps} \\
PROPOSAL={proposal} \\
EXP_RATE={rate} \\
REF_PROPOSAL={REF_PROPOSAL} \\
REF_RATE={REF_RATE} \\
MAX_STEPS={MAX_STEPS} \\
SEED={seed} \\
LR={LR} \\
TEST_SIZE={TEST_SIZE} \\
PER_GPU_BS={BATCH_SIZE} \\
EXTRA="mode={self.mode}" \\
    bash {script}
""".strip()


def squeue_names() -> set[str]:
    """Job names already queued/running for this user (idempotency guard)."""
    try:
        # timeout: with no slurm.conf reachable, squeue retries internally for
        # ~60s before giving up, which would stall every invocation.
        out = subprocess.run(
            ["squeue", "-h", "-u", os.environ.get("USER", ""), "-o", "%j"],
            capture_output=True, text=True, check=True, timeout=15,
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError,
            subprocess.TimeoutExpired) as exc:
        print(f"  [warn] squeue unavailable ({exc}); cannot skip in-flight jobs")
        return set()
    return {line.strip() for line in out.splitlines() if line.strip()}


def main(project: Project, doc: str | None = None) -> None:
    parser = argparse.ArgumentParser(description=doc)
    parser.add_argument("--dry-run", action="store_true",
                        help="print the plan and one sbatch script; submit nothing")
    parser.add_argument("--limit", type=int, default=None,
                        help="submit at most this many jobs (for a pilot)")
    parser.add_argument("--ps", nargs="+", default=PS_LIST)
    parser.add_argument("--curvatures", nargs="+", default=None,
                        help="subset of the swept curvatures (single-manifold projects)")
    parser.add_argument("--rates", nargs="+", default=EXP_RATES)
    parser.add_argument("--geometries", nargs="+", default=list(GEOMETRIES))
    parser.add_argument("--seeds", nargs="+", type=int, default=SEEDS)
    parser.add_argument("--partition", default=PARTITION)
    parser.add_argument("--force", action="store_true",
                        help="resubmit cells whose test_metrics.json already exists")
    args = parser.parse_args()

    (REPO_DIR / project.log_dir()).mkdir(parents=True, exist_ok=True)
    queued = squeue_names()

    ks = args.curvatures if args.curvatures is not None else project.geometry_cells
    cells = list(itertools.product(
        args.ps, ks, args.geometries, PROPOSALS, args.rates, args.seeds))
    submitted = skipped_done = skipped_queued = 0
    first_body = None
    failed: list[tuple[str, str]] = []
    nice_counts: dict[int, int] = {}

    for ps, k, geom, proposal, rate, seed in cells:
        name = project.run_name(ps, k, geom, proposal, rate, seed)
        out_dir = project.out_root() / name
        if not args.force and (REPO_DIR / out_dir / "test_metrics.json").exists():
            skipped_done += 1
            continue
        if project.job_name(name) in queued:
            skipped_queued += 1
            continue
        if args.limit is not None and submitted >= args.limit:
            continue

        body = project.job_body(GEOMETRIES[geom], out_dir, ps, k, proposal, rate, seed)
        slurm = Slurm(
            job_name=project.job_name(name),
            partition=args.partition,
            gres="gpu:1",
            ntasks=1,
            cpus_per_task=CPUS_PER_TASK,
            mem=MEM,
            time=project.time_limit(ps),
            output=str(project.log_dir() / f"{name}_%j.log"),
            **({"exclude": excl} if (excl := project.excluded_nodes(ps)) else {}),
        )
        nice = project.job_nice(ps, seed)
        sbatch_cmd = f"sbatch --nice={nice}"
        if first_body is None:
            first_body = (name, slurm, body, sbatch_cmd)
        nice_counts[(nice, seed != PRIMARY_SEED)] = (
            nice_counts.get((nice, seed != PRIMARY_SEED), 0) + 1)
        if not args.dry_run:
            # One rejected cell must not abandon the remaining hundreds.
            try:
                slurm.sbatch(body, sbatch_cmd=sbatch_cmd, verbose=False)
            except Exception as exc:  # noqa: BLE001 - report and keep going
                failed.append((name, repr(exc)[:200]))
                continue
        submitted += 1

    print(f"project           : {project.name} (mode={project.mode}, D={project.total_dim})")
    print(f"grid cells        : {len(cells)}")
    print(f"already finished  : {skipped_done}")
    print(f"already in squeue : {skipped_queued}")
    print(f"{'would submit' if args.dry_run else 'submitted'}      : {submitted}")
    n_cols = len(ks) * len(args.geometries) * len(PROPOSALS) * len(args.rates) * len(args.seeds)
    gpu_h = n_cols * sum(
        STARTUP_SEC + project.steps() * SEC_PER_STEP[project.cost_key(p)]
        + TEST_SEC[project.cost_key(p)] for p in args.ps) / 3600
    print(f"estimated compute : ~{gpu_h:.0f} GPU-h for the FULL grid at the budgeted rate")
    if failed:
        print(f"FAILED to submit    : {len(failed)}")
        for name, err in failed[:5]:
            print(f"    {name}\n      {err}")
    for (nice, replicate), count in sorted(nice_counts.items()):
        tag = "replicate seeds" if replicate else f"seed {PRIMARY_SEED} (runs first)"
        print(f"  nice={nice:<3} {count:>5} jobs   {tag}")
    print(f"runs   -> {project.out_root()}/")
    print(f"logs   -> {project.log_dir()}/")
    if args.dry_run and first_body is not None:
        name, slurm, body, sbatch_cmd = first_body
        print(f"\n--- example submission: {project.job_name(name)} ---")
        print(f"$ {sbatch_cmd} << EOF")
        print(f"{slurm}\n{body}")
        print("EOF")
