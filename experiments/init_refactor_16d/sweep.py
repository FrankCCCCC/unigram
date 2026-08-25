#!/usr/bin/env python
"""init_refactor_16d sweep: init_test's grid on the GENERAL-d bridge at hyper_dim=16.

Grid is exactly experiments/init_refactor_16d/setup.md:

    ps                     {naive_ps, cmplx_ps}
    loss_proposal_type     {exp}
    loss_proposal_exp_rate {0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0}
    loss_geometry          {cross_entropy, poincare_polar}
    max_steps              {20000, 40000, 100000, 200000}
    seed                   {0, 1, 2}
    fixed: hyper_dim=HYPER_DIM, lr=1e-3, gradient_clip_val=1.0,
           test_size=4e6, batch_size=2048,
           ref_proposal_type=exp, ref_proposal_exp_rate=0.1

2 x 7 x 2 x 4 x 3 = 336 runs, one SLURM job each. The three sibling projects
init_refactor_{3,9,16}d are this file with PROJECT / HYPER_DIM changed.

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
    cd <repo> && python experiments/init_refactor_16d/sweep.py --dry-run
    python experiments/init_refactor_16d/sweep.py
"""

from __future__ import annotations

import argparse
import itertools
import os
import subprocess
from pathlib import Path

from simple_slurm import Slurm

PROJECT = "init_refactor_16d"
HYPER_DIM = 16
REPO_DIR = Path(__file__).resolve().parents[2]
OUT_ROOT = Path("output") / PROJECT
LOG_DIR = Path("experiments") / PROJECT / "logs"

CONDA_BIN = "/home/sc3379/anaconda3/envs/sfm/bin"

# --- grid (setup.md) -------------------------------------------------------
PS_LIST = ["naive_ps", "cmplx_ps"]
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
# Both owned partitions, all four nodes. desa-compute-01 (8x 2080 Ti, 11 GB) is
# NOT excluded: Agent.md excludes it because 11 GB OOMs at seq 1024, which does
# not apply to a 3x128 MLP over a 10-word vocab using well under 1 GB. This is
# new science, not a reproduction, so there is no reason to pin a node.
PARTITION = "thickstun,desa"
CPUS_PER_TASK = 4
MEM = "16G"
# Per-cell wall-clock budget. Measured on the 2080 Ti pilot (the slowest node):
# SEC_PER_STEP covers train + the per-step reference pass; TEST_SEC covers the
# 4M-sample test pass. Both doubled for headroom -- an expired limit costs the
# whole cell, a loose one costs nothing on an `infinite`-TIMELIMIT partition.
SEC_PER_STEP = 0.05
TEST_SEC = 300


def time_limit(steps: int) -> str:
    secs = 2 * (steps * SEC_PER_STEP + TEST_SEC)
    h, rem = divmod(int(secs), 3600)
    return f"{h:02d}:{rem // 60:02d}:00"


# Scheduling priority. In SLURM a HIGHER --nice means LOWER priority, so the
# primary seed goes in at nice=0 and the replicate seeds queue behind it: a full
# single-seed grid completes first and the replicates fill in afterwards.
#
# --nice MUST be passed on the sbatch command line, not as a #SBATCH directive:
# its argument is OPTIONAL, so simple_slurm's space-separated
# "#SBATCH --nice   0" parses as --nice followed by a stray token, and sbatch
# rejects it with "Invalid directive found in batch script: 0".
PRIMARY_SEED = 0
NICE_PRIMARY = 0
NICE_REPLICATE = 50


def job_nice(seed: int) -> int:
    return NICE_PRIMARY if seed == PRIMARY_SEED else NICE_REPLICATE


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
            time=time_limit(steps),
            output=str(LOG_DIR / f"{name}_%j.log"),
        )
        sbatch_cmd = f"sbatch --nice={job_nice(seed)}"
        if first_body is None:
            first_body = (name, slurm, body, sbatch_cmd)
        nice_counts[job_nice(seed)] = nice_counts.get(job_nice(seed), 0) + 1
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
    n_cols = len(args.ps) * len(args.geometries) * len(PROPOSALS) * len(args.rates) * len(args.seeds)
    gpu_h = n_cols * sum(s * SEC_PER_STEP + TEST_SEC for s in args.steps) / 3600
    print(f"estimated compute : ~{gpu_h:.0f} GPU-h at the pilot's 2080 Ti rate")
    if failed:
        print(f"FAILED to submit    : {len(failed)}")
        for name, err in failed[:5]:
            print(f"    {name}\n      {err}")
    for nice in sorted(nice_counts):
        tag = "seed 0 (runs first)" if nice == NICE_PRIMARY else "replicate seeds"
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
