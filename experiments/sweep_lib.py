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
# Sized to MEASURED usage, because over-asking here is what actually strands GPUs.
# Over 186 completed cells: MaxRSS 1.46 GiB (worst 1.83), and TotalCPU/Elapsed =
# 1.06 cores -- the work is GPU-bound float64 tensor ops and the dataloader runs
# in-process (num_workers=0). Neither figure grows with the factor count: the
# 256-factor pilots peaked at 1.31 GiB.
#
# The earlier 2 CPU / 16 GB ask was ~10x the real RAM need, and on 2026-09-07 it
# deadlocked the sweep at 5 running jobs against ~14 IDLE GPUs -- other users had
# taken desa-compute-01 down to 11.5 GiB free RAM (7 GPUs idle, no 16 GB slot) and
# kuleshov-compute-02 down to 3 free CPUs (7 GPUs idle, one 2-CPU slot). A job that
# asks for more than it uses cannot run on a node someone else has already
# fragmented, and the GPU sits idle next to it.
CPUS_PER_TASK = 1
MEM = "4G"

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
#
# D = 150 and D = 768 are the 50- and 256-factor products, measured 2026-09-07 on
# desa-compute-01 (2080 Ti) at 50 batches per cell and converted to the Ada rate
# by NODE_SLOWDOWN (scratchpad, not checked in). The horosphere readout loops over
# factors with (batch, V, 3) tensors inside the loop, so the test pass is LINEAR in
# the factor count: fitting `C(V) + n * P(V)` to n = 3 and n = 50 predicted the
# n = 256 / c1e4 cell at 1468 s against 1490 s measured, 1.5% out. These rows are
# the direct measurements, not the fit.
# There is deliberately no SEC_PER_STEP row for them -- both projects are mode=opt
# and Project.gpu_secs never consults it.
TEST_SEC = {(10, 3): 30, (1000, 3): 40, (10000, 3): 60,
            (10, 9): 35, (1000, 9): 50, (10000, 9): 160,
            (10, 150): 240, (1000, 150): 450, (10000, 150): 2540,
            (10, 768): 1260, (1000, 768): 2290, (10000, 768): 12900}
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
# RE-MEASURED 2026-09-10 against 4459 completed cells of this campaign: for every
# (project, ps, geometry) that ran on more than one node, the median Elapsed ratio
# to thickstun-compute-01. Medians over 17-19 configs each came out 1.84 / 1.81 /
# 1.95 -- the old 2.5 / 3.5 / 4.5 were 1.4x, 1.9x and 2.3x too pessimistic, and the
# three non-Ada nodes are in fact within 8% of EACH OTHER, not spread 1.8x apart.
# The values below are the WORST config observed per node, not the median, because
# a time limit has to cover the slow tail: 2.33 / 2.27 / 2.54, rounded up.
#
# Over-estimating here is not free. It inflates time_limit(), and a request far
# longer than the real runtime cannot backfill into a gap -- on 2026-09-10 an
# 08:45:00 limit derived from the bogus 3.5 kept c1e4 ce cells (real runtime 1:58
# on that node) off 7 IDLE A5000s with Reason=ReqNodeNotAvail.
NODE_SLOWDOWN = {"thickstun-compute-01": 1.0, "kuleshov-compute-02": 2.4,
                 "kuleshov-compute-03": 2.3, "desa-compute-01": 2.6}
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
#
# D = 150 / D = 768 are the same 2026-09-07 poll. They are FLAT in the factor
# count -- 5.5 GiB at c1e4 whether the product has 3, 50 or 256 factors -- because
# the readout loops over factors and each iteration's (batch, V, 3) tensors are
# freed before the next. (They are also mode=opt, so nothing is retained for a
# backward pass; the D = 9 row above is a tnb figure and is not comparable.)
# Nothing here is excluded from any node.
PEAK_GB = {(10, 3): 0.9, (1000, 3): 1.7, (10000, 3): 8.0,
           (10, 9): 0.9, (1000, 9): 3.1, (10000, 9): 25.4,
           (10, 150): 0.6, (1000, 150): 0.8, (10000, 150): 5.5,
           (10, 768): 0.6, (1000, 768): 0.8, (10000, 768): 5.6}
# Overrides for mode=opt at the (V, D) pairs where the modes disagree. The rows
# above are tnb figures, and their comment already says the (10000, 9) one is
# "not comparable" to an opt cell -- but excluded_nodes used to key on (V, D)
# alone, so every opt c1e4 cell inherited 25.4 GiB. That cost it two of the four
# nodes AND +180 nice (NICE_EXCLUDED + one extra node), which is backwards for
# the Bayes-optimal control the trained numbers are read against.
# MEASURED 2026-09-08 on desa-compute-01 (2080 Ti, 11 GB): the worst opt c1e4
# D = 9 cell -- poincare_polar, batch 2048 -- peaked at 4.3 GiB and completed.
# That is consistent with the (10000, 150) / (10000, 768) rows above, which are
# opt polls and flat in factor count; nothing is retained for a backward pass.
PEAK_GB_OPT = {(10000, 9): 4.3}
# Overrides for loss_geometry=cross_entropy. The rows above are the pp figures, as
# the EXPERIMENT.md sizing note says they must be -- but that note was written when
# this table was keyed on (V, D) alone and could not see the geometry. It can now:
# `geom` is in scope at every call site in main(). ce runs the ELBO geometry only on
# the reference pass where pp runs it on the loss pass too, and at c1e4/D=9 that gap
# is 7.5 GiB (17.86 vs 25.34, EXPERIMENT.md's own measured table).
# Sizing ce at the pp figure excluded it from kuleshov-compute-03 for nothing:
# 11 such ce cells had ALREADY completed there in ~1:58 each on 2026-09-06, while
# the 13 pp cells that OOM'd on that node died in 12-18 s. Confirmed 2026-09-09 by
# relaxing the 202 pending ce cells onto it in place.
PEAK_GB_CE = {(10000, 9): 17.86}
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
# mode=opt runs first, as a BAND not a tiebreak: every opt cell outranks every tnb
# cell, because the Bayes-optimal control is what the trained numbers are read
# against -- a trained cell that lands below H(p) means nothing until the exact
# posterior's reading at the same (ps, K) is known. opt cells are also ~40x
# cheaper (no trainer.fit), so the whole control surface lands quickly and the
# expensive trained grid fills in behind it. The offset exceeds the widest
# within-band spread (310) so the bands cannot interleave.
NICE_BY_MODE = {"opt": 0, "tnb": 1000}
PRIMARY_SEED = 0
NICE_REPLICATE = 100
NICE_BY_VOCAB = {10: 0, 1000: 10, 10000: 30}
NICE_EXCLUDED = 150          # base penalty for not fitting every node
NICE_PER_EXCLUDED_NODE = 30  # additional penalty per further excluded node


def curvature_tag(k: str) -> str:
    """Run-name form of a curvature spec: `-1.0`, or `-0.01x-10.0x-1.0`.

    The tag travels inside the `folder=` hydra override, and hydra's override
    grammar reads a bare `[` as the start of a list literal and rejects the run
    -- so the tag must be bracket-free. It must also be underscore-free, since
    experiments/report.py bounds the `_k-` field with `[^_]+`.

    Identical factors collapse to the single shared value. That is what keeps a
    256-factor product's run name inside a filename, and it makes a homogeneous
    product tag compare directly against the single-manifold projects' scalar.
    """
    values = k.strip("[]").split(",")
    return values[0] if len(set(values)) == 1 else "x".join(values)


@dataclass(kw_only=True)
class Project:
    """What distinguishes one of the four projects from the others."""

    name: str
    mode: str  # "tnb" (train MLPLMRefactor) | "opt" (Bayes-optimal, no fit)
    # `curvatures` is the swept geometry axis and always lands in the run name.
    # Single manifold H^hyper_dim: a scalar K per run. Product manifold: prod_dim
    # is a hydra list literal ("[3,3,3]") and each curvature is the matching
    # per-factor list ("[-0.01,-10.0,-1.0]").
    hyper_dim: int = 3
    prod_dim: str = "null"
    curvatures: list[str] = field(default_factory=list)

    @property
    def total_dim(self) -> int:
        """D = sum(prod_factor_dim): the width of the (batch, V, D) tensors."""
        if self.prod_dim == "null":
            return self.hyper_dim
        return sum(int(d) for d in self.prod_dim.strip("[]").split(","))

    @property
    def geometry_cells(self) -> list[str]:
        """Curvature values to sweep: scalars, or per-factor list literals."""
        return list(self.curvatures)

    def out_root(self) -> Path:
        return Path("output") / self.name

    def log_dir(self) -> Path:
        return Path("experiments") / self.name / "logs"

    def run_name(self, ps: str, k: str, geom: str, proposal: str,
                 rate: str, seed: int) -> str:
        """Every SEARCHED variable appears here; the fixed dimension does not.

        The reference proposal is pinned by setup.md but is included anyway: if
        it ever changes, results computed under the old one must not silently
        share a directory with the new. experiments/report.py parses this back
        out.
        """
        return (f"ps-{ps}_k-{curvature_tag(k)}_lg-{geom}_q-{proposal}{rate}"
                f"_qref-{REF_PROPOSAL}{REF_RATE}_lr{LR}_st{MAX_STEPS}_s{seed}")

    def job_name(self, run: str) -> str:
        return f"{self.name}_{run}"

    def cost_key(self, ps: str) -> tuple[int, int]:
        return (VOCAB[ps], self.total_dim)

    def steps(self) -> int:
        # mode=opt skips trainer.fit, so only the test pass runs.
        return 0 if self.mode == "opt" else MAX_STEPS

    def gpu_secs(self, ps: str) -> float:
        """Ada-rate GPU seconds for one cell: the fit (if any) plus the test pass.

        `mode=opt` never calls `trainer.fit`, so SEC_PER_STEP is not consulted --
        an opt-only geometry needs no measured train rate to be schedulable.
        """
        key = self.cost_key(ps)
        steps = self.steps()
        return (steps * SEC_PER_STEP[key] if steps else 0.0) + TEST_SEC[key]

    def time_limit(self, ps: str, geom: str = "pp") -> str:
        excluded = set(self.excluded_nodes(ps, geom).split(","))
        slowdown = max(f for node, f in NODE_SLOWDOWN.items() if node not in excluded)
        secs = max(TIME_MARGIN * (STARTUP_SEC + slowdown * self.gpu_secs(ps)),
                   MIN_LIMIT_SEC)
        h, rem = divmod(int(secs), 3600)
        return f"{h:02d}:{rem // 60:02d}:00"

    def peak_gb(self, ps: str, geom: str = "pp") -> float:
        """Measured peak GPU memory (GiB) of one cell.

        `geom` defaults to "pp", the worst geometry, so a caller that does not
        know it still gets the safe figure.
        """
        key = self.cost_key(ps)
        if self.mode == "opt" and key in PEAK_GB_OPT:
            return PEAK_GB_OPT[key]
        if geom == "ce" and key in PEAK_GB_CE:
            return PEAK_GB_CE[key]
        return PEAK_GB.get(key, PEAK_GB_DEFAULT)

    def excluded_nodes(self, ps: str, geom: str = "pp") -> str:
        """Nodes whose GPU cannot hold this cell, comma-joined ('' if none)."""
        need = self.peak_gb(ps, geom) * GPU_MARGIN
        return ",".join(n for n, gb in NODE_GPU_GB.items() if gb < need)

    def job_nice(self, ps: str, seed: int, geom: str = "pp") -> int:
        excl = self.excluded_nodes(ps, geom)
        return (NICE_BY_MODE[self.mode]
                + (0 if seed == PRIMARY_SEED else NICE_REPLICATE)
                + NICE_BY_VOCAB[VOCAB[ps]]
                + (NICE_EXCLUDED + NICE_PER_EXCLUDED_NODE * (len(excl.split(",")) - 1)
                   if excl else 0))

    def job_body(self, script: str, out_dir: Path, ps: str, k: str,
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
CURVATURE={k if self.prod_dim == "null" else "-1.0"} \\
PROD_DIM={self.prod_dim} \\
PROD_CURVATURE={k if self.prod_dim != "null" else "null"} \\
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
            time=project.time_limit(ps, geom),
            output=str(project.log_dir() / f"{name}_%j.log"),
            **({"exclude": excl} if (excl := project.excluded_nodes(ps, geom)) else {}),
        )
        nice = project.job_nice(ps, seed, geom)
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
        STARTUP_SEC + project.gpu_secs(p) for p in args.ps) / 3600
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
