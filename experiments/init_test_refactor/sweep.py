#!/usr/bin/env python
"""init_test_refactor sweep: REPRODUCTION of init_test on the refactored code.

Grid is experiments/init_test_refactor/setup.md -- init_test's grid narrowed to
the single max_steps=20000 slice:

    ps                     {naive_ps, cmplx_ps}
    loss_proposal_type     {exp}
    loss_proposal_exp_rate {0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0}
    loss_geometry          {cross_entropy, poincare_polar}
    max_steps              {20000}
    seed                   {0, 1, 2}
    fixed: hyper_dim=2, lr=1e-3, gradient_clip_val=1.0,
           test_size=4e6, batch_size=2048,
           ref_proposal_type=exp, ref_proposal_exp_rate=0.1

2 x 7 x 2 x 1 x 3 = 84 runs, one SLURM job each. All 84 have a matching cell in
output/init_test/ (verified), so the comparison is PER-CELL.

Unlike init_opt_test_refactor this one TRAINS, so the model is a function of the
whole optimizer trajectory. Every source of randomness is seeded
(L.seed_everything(workers=True) for init/shuffling, _make_step_generator for the
t draws), so cells should still land on the reference values; residual drift
would come from GPU nondeterminism in the backward pass, not from the refactor.
Read a mismatch here together with init_opt_test_refactor: that project has no
training at all, so if opt reproduces and this does not, the divergence is in the
training path, not the bridge or the loss.

The reference proposal stays PINNED at exp(0.1), deliberately untied from the
swept loss_proposal_exp_rate: that is what makes test_wnelbo_ref / test_ce_ref
comparable across rate cells, and exp(0.1) is below the rate ~0.304 cliff past
which the weighted estimator has infinite variance.

ORCHESTRATION ONLY: submits script/train/{ce,pp}.sh; never inlines the trainer.
Idempotent and resumable -- a cell is skipped when its test_metrics.json exists
or its job name is already in squeue.

Run from a LOGIN node (compute nodes have no slurm.conf):
    cd <repo> && python experiments/init_test_refactor/sweep.py --dry-run
    python experiments/init_test_refactor/sweep.py
"""

from __future__ import annotations

import argparse
import itertools
import os
import subprocess
from pathlib import Path

from simple_slurm import Slurm

PROJECT = "init_test_refactor"
REFERENCE_PROJECT = "init_test"
REPO_DIR = Path(__file__).resolve().parents[2]
OUT_ROOT = Path("output") / PROJECT
LOG_DIR = Path("experiments") / PROJECT / "logs"

CONDA_BIN = "/home/sc3379/anaconda3/envs/sfm/bin"

# --- grid (setup.md) -------------------------------------------------------
PS_LIST = ["naive_ps", "cmplx_ps"]
PROPOSALS = ["exp"]
EXP_RATES = ["0.01", "0.05", "0.1", "0.25", "0.5", "0.75", "1.0"]
GEOMETRIES = {"ce": "script/train/ce.sh", "pp": "script/train/pp.sh"}
MAX_STEPS = [20000]
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
# not apply to a 3x128 MLP over a <=10-word vocab using well under 1 GB.
# init_test/sweep.py -- the project this reproduces -- ran its entire grid there.
PARTITION = "thickstun,desa"
# --nodelist for the REPRODUCTION comparison. 20000 training steps amplify
# ULP-level differences in cuBLAS kernel selection into visible trajectory
# divergence, so a trained cell only reproduces bit-exactly on the architecture
# that produced the reference. Measured on the first full pass of this grid:
#
#   desa-compute-01  (2080 Ti, sm_75)  18/18 bit-exact, max rel diff 0.0e+00
#   kuleshov-compute-02 (A6000, sm_86)  0/17 bit-exact, max rel diff 7.9e-01
#   kuleshov-compute-03 (A5000, sm_86)  0/31 bit-exact, max rel diff 3.5e-01
#
# init_test -- the project this reproduces -- pinned itself to desa-compute-01,
# so --nodelist desa-compute-01 is what makes the comparison a test of the
# refactor rather than a test of the GPU. Leave it unset to use the whole of
# both partitions (faster, but only valid for the no-training opt companion,
# which is architecture-independent because nothing accumulates).
NODELIST = None
CPUS_PER_TASK = 4
MEM = "16G"
# init_test measured ~9 min for train(20k)+test(4M). An hour is generous, and a
# short limit lets these backfill around the long jobs already on these nodes.
TIME_LIMIT = "01:00:00"

# In SLURM a HIGHER --nice means LOWER priority. Seed 0 goes in at nice=0 so a
# complete single-seed grid lands first; the replicate seeds fill in behind it.
PRIMARY_SEED = 0
NICE_PRIMARY = 0
NICE_REPLICATE = 50


def job_nice(seed: int) -> int:
    return NICE_PRIMARY if seed == PRIMARY_SEED else NICE_REPLICATE


def run_name(ps: str, geom: str, proposal: str, rate: str, steps: int,
             seed: int) -> str:
    # Byte-identical to init_test's run_name so each cell pairs 1:1 with its
    # reference cell by directory name alone.
    return (f"ps-{ps}_lg-{geom}_q-{proposal}{rate}"
            f"_qref-{REF_PROPOSAL}{REF_RATE}_lr{LR}_st{steps}_s{seed}")


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
             steps: int, seed: int) -> str:
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
    parser.add_argument("--partition", default=PARTITION,
                        help="SLURM partition(s). When pinning with --nodelist, "
                             "this must be a partition that CONTAINS that node: "
                             "SLURM validates the nodelist against the FIRST "
                             "partition listed and rejects the job with "
                             "'Requested nodes not in this partition' otherwise")
    parser.add_argument("--nodelist", default=NODELIST,
                        help="pin every job to this node. Required for a valid "
                             "reproduction comparison: use desa-compute-01, the "
                             "node init_test ran on (see NODELIST above)")
    parser.add_argument("--out-suffix", default="",
                        help="append to the project's output dir so a second pass "
                             "on different hardware does not overwrite the first")
    parser.add_argument("--force", action="store_true",
                        help="resubmit cells whose test_metrics.json already exists")
    args = parser.parse_args()

    out_root = Path(str(OUT_ROOT) + args.out_suffix)
    (REPO_DIR / LOG_DIR).mkdir(parents=True, exist_ok=True)
    queued = squeue_names()

    cells = list(itertools.product(
        args.ps, args.geometries, PROPOSALS, args.rates, args.steps, args.seeds))
    submitted = skipped_done = skipped_queued = 0
    first_body = None
    failed: list[tuple[str, str]] = []

    for ps, geom, proposal, rate, steps, seed in cells:
        name = run_name(ps, geom, proposal, rate, steps, seed)
        out_dir = out_root / name
        if not args.force and (REPO_DIR / out_dir / "test_metrics.json").exists():
            skipped_done += 1
            continue
        if job_name(name) in queued:
            skipped_queued += 1
            continue
        if args.limit is not None and submitted >= args.limit:
            continue

        body = job_body(GEOMETRIES[geom], out_dir, ps, proposal, rate, steps, seed)
        slurm_kwargs = dict(
            job_name=job_name(name),
            partition=args.partition,
            gres="gpu:1",
            ntasks=1,
            cpus_per_task=CPUS_PER_TASK,
            mem=MEM,
            time=TIME_LIMIT,
            output=str(LOG_DIR / f"{name}_%j.log"),
        )
        if args.nodelist:
            slurm_kwargs["nodelist"] = args.nodelist
        slurm = Slurm(**slurm_kwargs)
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
    print(f"partition         : {args.partition}"
          f"{' nodelist=' + args.nodelist if args.nodelist else ' (all nodes)'}")
    if failed:
        print(f"FAILED to submit    : {len(failed)}")
        for name, err in failed[:5]:
            print(f"    {name}\n      {err}")
    print(f"runs      -> {out_root}/")
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
