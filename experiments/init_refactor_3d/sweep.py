#!/usr/bin/env python
"""init_refactor_3d sweep: init_test's grid on the GENERAL-d bridge at hyper_dim=3.

Grid is exactly experiments/init_refactor_3d/setup.md:

    ps                     {naive_ps, cmplx_ps, c1e3_exp1.0, c1e4_exp1.0}
    loss_proposal_type     {exp}
    loss_proposal_exp_rate {0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0}
    loss_geometry          {cross_entropy, poincare_polar}
    max_steps              {20000, 40000, 100000, 200000}
    seed                   {0, 1, 2}
    fixed: hyper_dim=HYPER_DIM, lr=1e-3, gradient_clip_val=1.0,
           test_size=4e6, batch_size=2048,
           ref_proposal_type=exp, ref_proposal_exp_rate=0.1

4 x 7 x 2 x 4 x 3 = 672 runs, one SLURM job each. The three sibling projects
init_refactor_{3,9,16}d are this file with PROJECT / HYPER_DIM changed.

c1e3_exp1.0 / c1e4_exp1.0 are the same geometric law p_i ~ e^-i truncated at
V = 1000 / 10000, so all four ps specs are compared against a known H(p). They
are FAR more expensive than the V = 10 pair: the horosphere geometry
materializes several (batch, V, d) float64 tensors, so a c1e4 cell costs 8-25x
a naive_ps cell in time and up to 21 GiB of GPU memory. SEC_PER_STEP / PEAK_GB
below carry the measured numbers and size each cell's time limit and node set.

hyper_dim is the dimension d of H^d: the word embedding is (V, d), the bridge
direction is a unit vector on S^{d-1}, and the model input is (rho, u) in
R^{d+1}. It reaches main.py through the train scripts' HYPER_DIM env var.
run_name is byte-identical to init_test's (the dimension lives in the project
name), so experiments/report.py parses these runs unchanged.

The reference proposal is PINNED at exp(0.1) and is deliberately NOT tied to the
swept loss_proposal_exp_rate: that is what makes test_wnelbo_ref / test_ce_ref
comparable across rate cells, and exp(0.1) is below the rate ~0.304 cliff past
which the weighted estimator has infinite variance.

ORCHESTRATION ONLY: this submits script/train/{ce,pp}.sh; it never inlines the
trainer. Idempotent and resumable -- a cell is skipped when its
test_metrics.json already exists or its job name is already in squeue, so
re-running after a partial sweep only fills the gaps.

Run this from a LOGIN node (compute nodes have no slurm.conf):
    cd <repo> && python experiments/init_refactor_3d/sweep.py --dry-run
    python experiments/init_refactor_3d/sweep.py
"""

from __future__ import annotations

import argparse
import itertools
import os
import subprocess
from pathlib import Path

from simple_slurm import Slurm

PROJECT = "init_refactor_3d"
HYPER_DIM = 3
REPO_DIR = Path(__file__).resolve().parents[2]
OUT_ROOT = Path("output") / PROJECT
LOG_DIR = Path("experiments") / PROJECT / "logs"

CONDA_BIN = "/home/sc3379/anaconda3/envs/sfm/bin"

# --- grid (setup.md) -------------------------------------------------------
PS_LIST = ["naive_ps", "cmplx_ps", "c1e3_exp1.0", "c1e4_exp1.0"]
PROPOSALS = ["exp"]
EXP_RATES = ["0.01", "0.05", "0.1", "0.25", "0.5", "0.75", "1.0"]
GEOMETRIES = {"ce": "script/train/ce.sh", "pp": "script/train/pp.sh"}
MAX_STEPS = [20000, 40000, 100000, 200000]
SEEDS = [0, 1, 2]

# --- fixed ----------------------------------------------------------------
LR = "0.001"
REF_PROPOSAL = "exp"
REF_RATE = "0.1"
TEST_SIZE = 4_000_000
BATCH_SIZE = 2048

# --- slurm ----------------------------------------------------------------
# Both owned partitions. Every cell is eligible for all four nodes; only the
# ones whose measured peak memory does not fit a node's GPU are steered away
# from it (see excluded_nodes), so desa-compute-01's 8x 2080 Ti stay in play for
# everything they can hold. Agent.md excludes that node for seq-1024 work, which
# does not apply to a 3x128 MLP.
PARTITION = "thickstun,desa"
# Measured, not guessed: finished cells report TotalCPU ~= Elapsed (13:25 elapsed vs
# 13:18 CPU), i.e. ~1 core. The work is GPU-bound float64 tensor ops and the dataloader
# runs in-process (num_workers=0), so 2 leaves 100% headroom. It matters because the
# GPU-rich nodes are CPU-poor -- desa-compute-01 is 36 CPUs to 8 GPUs -- so a 4-CPU ask
# strands GPUs whenever other jobs hold CPUs on the same node.
CPUS_PER_TASK = 2
MEM = "16G"

# Vocabulary size of each ps spec. The horosphere geometry materializes several
# (batch, V, d) float64 tensors, so V*d drives both a cell's step time and its
# peak GPU memory.
VOCAB = {"naive_ps": 10, "cmplx_ps": 10, "c1e3_exp1.0": 1000, "c1e4_exp1.0": 10000}

# Per-cell wall-clock budget, keyed by (vocabulary size, hyper_dim) and doubled
# by time_limit() for headroom. SEC_PER_STEP covers train + the per-step reference
# pass; TEST_SEC covers the 4M-sample test pass. V = 10 keeps the 2080 Ti pilot's
# flat figures, so the finished naive_ps / cmplx_ps cells are budgeted exactly as
# they were; V = 1000 / 10000 are measured at batch 2048 on an RTX A6000 and
# rounded up ~25%.
#
# Keyed by d, not just V, because the scheduler is sched/backfill: a limit 7x the
# real cost (what a single V-keyed worst-d row gives d = 3) almost never fits a
# backfill window, so the cell waits for a full drain instead. Fairshare here
# charges actual usage, not the request, so the only cost of a loose limit is
# that lost backfill -- and the only cost of a tight one is losing the cell.
SEC_PER_STEP = {(10, 3): 0.05, (10, 9): 0.05, (10, 16): 0.05,
                (1000, 3): 0.035, (1000, 9): 0.07, (1000, 16): 0.08,
                (10000, 3): 0.22, (10000, 9): 0.47, (10000, 16): 0.70}
TEST_SEC = {10: 300, 1000: 300, 10000: 900}

# Peak GPU memory of a training step, measured at batch 2048 on an RTX A6000.
# Only the V = 10000 cells come close to a card's capacity; everything else fits
# in under 2.5 GiB. Keyed by (vocab size, hyper_dim) because the (batch, V, d)
# tensors scale with d as well.
PEAK_GB = {(10000, 3): 5.1, (10000, 9): 12.4, (10000, 16): 20.9}
PEAK_GB_DEFAULT = 2.5
# Usable GPU memory per node, by the smallest card it offers.
NODE_GPU_GB = {"desa-compute-01": 10.5, "kuleshov-compute-03": 24.0,
               "kuleshov-compute-02": 48.0, "thickstun-compute-01": 48.0}
# Headroom over the measured peak: fragmentation plus the CUDA context.
GPU_MARGIN = 1.25


def time_limit(ps: str, steps: int) -> str:
    v = VOCAB[ps]
    secs = 2 * (steps * SEC_PER_STEP[(v, HYPER_DIM)] + TEST_SEC[v])
    h, rem = divmod(int(secs), 3600)
    return f"{h:02d}:{rem // 60:02d}:00"


def excluded_nodes(ps: str) -> str:
    """Nodes whose GPU cannot hold this cell, comma-joined ('' if none)."""
    need = PEAK_GB.get((VOCAB[ps], HYPER_DIM), PEAK_GB_DEFAULT) * GPU_MARGIN
    return ",".join(n for n, gb in NODE_GPU_GB.items() if gb < need)


# Scheduling priority. In SLURM a HIGHER --nice means LOWER priority, so the
# primary seed goes in at nice=0 and the replicate seeds queue behind it: a full
# single-seed grid completes first and the replicates fill in afterwards.
#
# --nice MUST be passed on the sbatch command line, not as a #SBATCH directive:
# its argument is OPTIONAL, so simple_slurm's space-separated
# "#SBATCH --nice   0" parses as --nice followed by a stray token, and sbatch
# rejects it with "Invalid directive found in batch script: 0".
PRIMARY_SEED = 0
NICE_REPLICATE = 100
# Within a seed the queue is ordered by cost, so a complete coarse picture lands
# early and the expensive cells fill in behind it: small vocabulary before
# large, short runs before long. Both terms stay well under NICE_REPLICATE, so
# every seed-0 cell still outranks every replicate.
NICE_BY_VOCAB = {10: 0, 1000: 10, 10000: 30}
NICE_BY_STEPS = {20000: 0, 40000: 2, 100000: 5, 200000: 9}
# A cell that does not fit every node must rank BELOW cells that do. SLURM's main
# scheduler gate-keeps a partition on the highest-priority job it cannot place, so
# a c1e4 cell waiting for a >=24 GB GPU sits at the head of the queue and strands
# desa-compute-01's 8x 11 GB cards -- which can ONLY ever run the small cells.
# Measured 2026-08-26: that left the node at 0/8 GPUs for hours with 780 cells
# queued; re-ranking refilled it to 7/8 within 25 s. This term must exceed
# NICE_REPLICATE **plus the vocab/steps spread** (100 + 39) so a fits-everywhere
# REPLICATE still outranks an excluded PRIMARY seed -- ordering by cost alone is what
# caused the stall, and a value of 90 (< NICE_REPLICATE) was not enough: it left
# desa-compute-01 idle again once the capable seed-0 cells drained.
# Scaled by HOW restricted the cell is, not just whether it is restricted: a cell that
# fits three nodes must outrank one that fits only two, or the less portable cell
# gate-keeps hardware it cannot use. Measured 2026-08-27: 16d c1e4 (>=48 GB, 2 nodes) and
# 9d c1e4 (>=24 GB, 3 nodes) carried equal nice, and a 16d cell at the head stranded
# kuleshov-compute-03's idle A5000s from the 9d cells that fit them.
NICE_EXCLUDED = 150          # base penalty for not fitting every node
NICE_PER_EXCLUDED_NODE = 30  # additional penalty per further excluded node


def job_nice(ps: str, steps: int, seed: int) -> int:
    return ((0 if seed == PRIMARY_SEED else NICE_REPLICATE)
            + NICE_BY_VOCAB[VOCAB[ps]] + NICE_BY_STEPS[steps]
            + (NICE_EXCLUDED + NICE_PER_EXCLUDED_NODE * (len(excl.split(",")) - 1)
               if (excl := excluded_nodes(ps)) else 0))


def run_name(ps: str, geom: str, proposal: str, rate: str, steps: int, seed: int) -> str:
    # Every swept variable must appear here. The reference proposal is fixed by
    # setup.md but is included anyway: if it is ever changed, results computed
    # under the old one must not silently share a directory with the new.
    return (f"ps-{ps}_lg-{geom}_q-{proposal}{rate}"
            f"_qref-{REF_PROPOSAL}{REF_RATE}_lr{LR}_st{steps}_s{seed}")


def job_name(name: str) -> str:
    return f"{PROJECT}_{name}"


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


def job_body(script: str, out_dir: Path, ps: str, proposal: str, rate: str,
             steps: int, seed: int) -> str:
    return f"""
export TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1
export SLURM_JOB_NAME=bash
export NCCL_P2P_DISABLE=1 NCCL_IB_DISABLE=1
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PATH={CONDA_BIN}:$PATH
cd {REPO_DIR}
OUTPUT_DIR={out_dir} \\
HYPER_DIM={HYPER_DIM} \\
PS={ps} \\
PROPOSAL={proposal} \\
EXP_RATE={rate} \\
REF_PROPOSAL={REF_PROPOSAL} \\
REF_RATE={REF_RATE} \\
MAX_STEPS={steps} \\
SEED={seed} \\
LR={LR} \\
TEST_SIZE={TEST_SIZE} \\
PER_GPU_BS={BATCH_SIZE} \\
    bash {script}
""".strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="print the plan and one sbatch script; submit nothing")
    parser.add_argument("--limit", type=int, default=None,
                        help="submit at most this many jobs (for a pilot)")
    parser.add_argument("--ps", nargs="+", default=PS_LIST)
    parser.add_argument("--rates", nargs="+", default=EXP_RATES)
    parser.add_argument("--geometries", nargs="+", default=list(GEOMETRIES))
    parser.add_argument("--steps", nargs="+", type=int, default=MAX_STEPS)
    parser.add_argument("--seeds", nargs="+", type=int, default=SEEDS)
    parser.add_argument("--partition", default=PARTITION)
    parser.add_argument("--force", action="store_true",
                        help="resubmit cells whose test_metrics.json already exists")
    args = parser.parse_args()

    (REPO_DIR / LOG_DIR).mkdir(parents=True, exist_ok=True)
    queued = squeue_names()

    cells = list(itertools.product(
        args.ps, args.geometries, PROPOSALS, args.rates, args.steps, args.seeds))
    submitted = skipped_done = skipped_queued = 0
    first_body = None
    failed: list[tuple[str, str]] = []
    nice_counts: dict[int, int] = {}

    for ps, geom, proposal, rate, steps, seed in cells:
        name = run_name(ps, geom, proposal, rate, steps, seed)
        out_dir = OUT_ROOT / name
        if not args.force and (REPO_DIR / out_dir / "test_metrics.json").exists():
            skipped_done += 1
            continue
        if job_name(name) in queued:
            skipped_queued += 1
            continue
        if args.limit is not None and submitted >= args.limit:
            continue

        body = job_body(GEOMETRIES[geom], out_dir, ps, proposal, rate, steps, seed)
        slurm = Slurm(
            job_name=job_name(name),
            partition=args.partition,
            gres="gpu:1",
            ntasks=1,
            cpus_per_task=CPUS_PER_TASK,
            mem=MEM,
            time=time_limit(ps, steps),
            output=str(LOG_DIR / f"{name}_%j.log"),
            **({"exclude": excl} if (excl := excluded_nodes(ps)) else {}),
        )
        sbatch_cmd = f"sbatch --nice={job_nice(ps, steps, seed)}"
        if first_body is None:
            first_body = (name, slurm, body, sbatch_cmd)
        nice = job_nice(ps, steps, seed)
        nice_counts[nice] = nice_counts.get(nice, 0) + 1
        if not args.dry_run:
            # One rejected cell must not abandon the remaining hundreds.
            try:
                slurm.sbatch(body, sbatch_cmd=sbatch_cmd, verbose=False)
            except Exception as exc:  # noqa: BLE001 - report and keep going
                failed.append((name, repr(exc)[:200]))
                continue
        submitted += 1

    print(f"project           : {PROJECT} (hyper_dim={HYPER_DIM})")
    print(f"grid cells        : {len(cells)}")
    print(f"already finished  : {skipped_done}")
    print(f"already in squeue : {skipped_queued}")
    print(f"{'would submit' if args.dry_run else 'submitted'}      : {submitted}")
    n_cols = len(args.geometries) * len(PROPOSALS) * len(args.rates) * len(args.seeds)
    gpu_h = n_cols * sum(
        s * SEC_PER_STEP[(VOCAB[p], HYPER_DIM)] + TEST_SEC[VOCAB[p]]
        for p in args.ps for s in args.steps) / 3600
    print(f"estimated compute : ~{gpu_h:.0f} GPU-h for the FULL grid at the budgeted rate")
    if failed:
        print(f"FAILED to submit    : {len(failed)}")
        for name, err in failed[:5]:
            print(f"    {name}\n      {err}")
    for nice in sorted(nice_counts):
        tag = "seed 0 (runs first)" if nice < NICE_REPLICATE else "replicate seeds"
        print(f"  nice={nice:<3} {nice_counts[nice]:>5} jobs   {tag}")
    print(f"runs   -> {OUT_ROOT}/")
    print(f"logs   -> {LOG_DIR}/")
    if args.dry_run and first_body is not None:
        name, slurm, body, sbatch_cmd = first_body
        print(f"\n--- example submission: {job_name(name)} ---")
        print(f"$ {sbatch_cmd} << EOF")
        print(f"{slurm}\n{body}")
        print("EOF")


if __name__ == "__main__":
    main()
