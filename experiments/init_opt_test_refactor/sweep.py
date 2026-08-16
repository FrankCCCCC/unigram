#!/usr/bin/env python
"""init_opt_test_refactor sweep: REPRODUCTION of init_opt_test on the refactored code.

Same grid as experiments/init_opt_test/sweep.py, run against the post-refactor
tree (BaseTrainer extracted into trainer.py, word_embedding pushed into the model
classes). The point is not new science: it is to show that the refactor did not
move any number. Every cell here has a matching cell in output/init_opt_test/,
so the comparison is PER-CELL, not just against the summary table in setup.md.

    ps                     {naive_ps, cmplx_ps,
                            c1e2_exp1.0, c1e3_exp1.0, c1e4_exp1.0}
    loss_proposal_type     {exp}
    loss_proposal_exp_rate {0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0}
    loss_geometry          {cross_entropy, poincare_polar}
    seed                   {0, 1, 2}
    fixed: mode=opt, hyper_dim=2, lr=1e-3, max_steps=20000,
           gradient_clip_val=1.0, test_size=4e6, batch_size=2048,
           ref_proposal_type=exp, ref_proposal_exp_rate=0.1

5 x 7 x 2 x 3 = 210 runs, one SLURM job each.

mode=opt skips trainer.fit, so lr / max_steps are inert and only the 4M-sample
test pass runs. OptimalModel is deterministic and has no parameters, so a
reproduction failure here is unambiguously a bridge / loss / proposal / logging
regression -- there is no training noise to hide behind.

Two free correctness checks to read off the results:
  * test_wnelbo_ref / test_wce_ref are produced by the REFERENCE pass, which is
    pinned to exp(0.1) on its own RNG stream (salt=1) and is independent of the
    swept loss geometry and rate. They must therefore be IDENTICAL across all 14
    (geometry, rate) cells of a given (ps, seed). Verified true in the reference
    outputs.
  * test_wloss is the swept objective. Rates above ~0.304 have infinite
    variance, so those cells legitimately fan out across seeds.

ORCHESTRATION ONLY: submits script/train/{ce,pp}.sh; never inlines the trainer.
Idempotent and resumable -- a cell is skipped when its test_metrics.json exists
or its job name is already in squeue.

Run from a LOGIN node (compute nodes have no slurm.conf):
    cd <repo> && python experiments/init_opt_test_refactor/sweep.py --dry-run
    python experiments/init_opt_test_refactor/sweep.py
"""

from __future__ import annotations

import argparse
import itertools
import os
import subprocess
from pathlib import Path

from simple_slurm import Slurm

PROJECT = "init_opt_test_refactor"
REFERENCE_PROJECT = "init_opt_test"
REPO_DIR = Path(__file__).resolve().parents[2]
OUT_ROOT = Path("output") / PROJECT
LOG_DIR = Path("experiments") / PROJECT / "logs"

CONDA_BIN = "/home/sc3379/anaconda3/envs/sfm/bin"

# --- grid (setup.md; identical to init_opt_test) ---------------------------
PS_LIST = ["naive_ps", "cmplx_ps", "c1e2_exp1.0", "c1e3_exp1.0", "c1e4_exp1.0"]
PROPOSALS = ["exp"]
EXP_RATES = ["0.01", "0.05", "0.1", "0.25", "0.5", "0.75", "1.0"]
# abbreviation -> train script ; abbreviations match the reference run names
GEOMETRIES = {"ce": "script/train/ce.sh", "pp": "script/train/pp.sh"}
SEEDS = [0, 1, 2]

# --- fixed ----------------------------------------------------------------
MODE = "opt"
MAX_STEPS = 20000  # inert under mode=opt (no trainer.fit); kept for the run name
LR = "0.001"
REF_PROPOSAL = "exp"
REF_RATE = "0.1"
TEST_SIZE = 4_000_000
BATCH_SIZE = 2048

# --- slurm ----------------------------------------------------------------
# Both owned partitions, all four nodes. desa-compute-01 (8x 2080 Ti, 11 GB) is
# NOT excluded: Agent.md excludes it because 11 GB OOMs at seq 1024, which does
# not apply to a 3x128 MLP over a <=10-word vocab using well under 1 GB. Its
# sm_75 cards are covered by the env's torch cu128 cubins. init_test/sweep.py
# set the same precedent and ran its whole grid there.
PARTITION = "thickstun,desa"
CPUS_PER_TASK = 4
MEM = "16G"
# The test pass is ~1954 batches and no training runs, so these are minutes each.
# A short limit lets them backfill around the long jobs already on these nodes.
TIME_LIMIT = "01:00:00"

# In SLURM a HIGHER --nice means LOWER priority. Seed 0 goes in at nice=0 so a
# complete single-seed grid lands first; the replicate seeds fill in behind it.
PRIMARY_SEED = 0
NICE_PRIMARY = 0
NICE_REPLICATE = 50


def job_nice(seed: int) -> int:
    return NICE_PRIMARY if seed == PRIMARY_SEED else NICE_REPLICATE


def run_name(ps: str, geom: str, proposal: str, rate: str, seed: int) -> str:
    # Byte-identical to init_opt_test's run_name so each cell pairs 1:1 with its
    # reference cell by directory name alone.
    return (f"ps-{ps}_lg-{geom}_q-{proposal}{rate}"
            f"_qref-{REF_PROPOSAL}{REF_RATE}_lr{LR}_st{MAX_STEPS}_s{seed}")


def job_name(name: str) -> str:
    return f"{PROJECT}_{name}"


def squeue_names() -> set[str]:
    """Job names already queued/running for this user (idempotency guard)."""
    try:
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
             seed: int) -> str:
    return f"""
export TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1
export SLURM_JOB_NAME=bash
export NCCL_P2P_DISABLE=1 NCCL_IB_DISABLE=1
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PATH={CONDA_BIN}:$PATH
cd {REPO_DIR}
OUTPUT_DIR={out_dir} \\
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
EXTRA="mode={MODE}" \\
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
    parser.add_argument("--seeds", nargs="+", type=int, default=SEEDS)
    parser.add_argument("--force", action="store_true",
                        help="resubmit cells whose test_metrics.json already exists")
    args = parser.parse_args()

    (REPO_DIR / LOG_DIR).mkdir(parents=True, exist_ok=True)
    queued = squeue_names()

    cells = list(itertools.product(
        args.ps, args.geometries, PROPOSALS, args.rates, args.seeds))
    submitted = skipped_done = skipped_queued = 0
    first_body = None
    failed: list[tuple[str, str]] = []

    for ps, geom, proposal, rate, seed in cells:
        name = run_name(ps, geom, proposal, rate, seed)
        out_dir = OUT_ROOT / name
        if not args.force and (REPO_DIR / out_dir / "test_metrics.json").exists():
            skipped_done += 1
            continue
        if job_name(name) in queued:
            skipped_queued += 1
            continue
        if args.limit is not None and submitted >= args.limit:
            continue

        body = job_body(GEOMETRIES[geom], out_dir, ps, proposal, rate, seed)
        slurm = Slurm(
            job_name=job_name(name),
            partition=PARTITION,
            gres="gpu:1",
            ntasks=1,
            cpus_per_task=CPUS_PER_TASK,
            mem=MEM,
            time=TIME_LIMIT,
            output=str(LOG_DIR / f"{name}_%j.log"),
        )
        if first_body is None:
            first_body = (name, slurm, body)
        if not args.dry_run:
            try:
                # --nice on the command line, not as a #SBATCH directive: its
                # argument is OPTIONAL, so simple_slurm's space-separated
                # "#SBATCH --nice   0" parses as --nice plus a stray token and
                # sbatch rejects the script.
                slurm.sbatch(body, verbose=False,
                             sbatch_cmd=f"sbatch --nice={job_nice(seed)}")
            except Exception as exc:  # noqa: BLE001 - report and keep going
                failed.append((name, repr(exc)[:200]))
                continue
        submitted += 1

    print(f"grid cells        : {len(cells)}")
    print(f"already finished  : {skipped_done}")
    print(f"already in squeue : {skipped_queued}")
    print(f"{'would submit' if args.dry_run else 'submitted'}      : {submitted}")
    print(f"partition         : {PARTITION} (all nodes)")
    if failed:
        print(f"FAILED to submit    : {len(failed)}")
        for name, err in failed[:5]:
            print(f"    {name}\n      {err}")
    print(f"runs      -> {OUT_ROOT}/")
    print(f"logs      -> {LOG_DIR}/")
    print(f"reference -> output/{REFERENCE_PROJECT}/  (same run names)")
    if args.dry_run and first_body is not None:
        name, slurm, body = first_body
        print(f"\n--- example submission: {job_name(name)} ---")
        print("$ sbatch << EOF")
        print(f"{slurm}\n{body}")
        print("EOF")


if __name__ == "__main__":
    main()
