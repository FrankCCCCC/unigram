#!/usr/bin/env python
"""init_opt_test sweep: ELBO of the BAYES-OPTIMAL model vs loss type and proposal.

Grid is exactly experiments/init_opt_test/setup.md:

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

The three `c1e*_exp1.0` specs are the SAME geometric distribution p_i ∝ e^-i
truncated at V = 100 / 1000 / 10000, so all three have H(p) = 1.040652 nats (the
analytic geometric(e^-1) entropy) and only ~16 tokens ever appear in a 4M-sample
draw. They vary the vocabulary -- i.e. the packing of the boundary angles
phi_v = (v+0.5)*2*pi/V -- at constant entropy.

This is init_test with the model replaced by the closed-form Bayes-optimal one
(`mode=opt`, passed through the train scripts' EXTRA hook): trainer.fit is
skipped, so lr / max_steps are inert and only the 4M-sample test pass runs. What
is left is a pure ESTIMATOR study -- the model is exact, so every cell-to-cell
difference in test_wloss is the importance-weighted estimator, not learning.

Two things to read off the results:
  * test_wloss  -- headline. The exact model's objective under the swept
    (loss_geometry, loss_proposal_exp_rate). Rates above ~0.304 have infinite
    variance, so those cells should fan out across seeds.
  * test_wnelbo_ref / test_wce_ref -- the reference pass is pinned to exp(0.1)
    and is fed by an independent RNG stream, and OptimalModel is deterministic,
    so these must come out (near-)IDENTICAL for all 14 (geometry, rate) cells of
    a given (ps, seed). That invariance is a free correctness check on the
    loss/reference split.

ORCHESTRATION ONLY: this submits script/train/{ce,pp}.sh; it never inlines the
trainer. Idempotent and resumable -- a cell is skipped when its
test_metrics.json already exists or its job name is already in squeue, so
re-running after a partial sweep only fills the gaps.

Run this from a LOGIN node (compute nodes have no slurm.conf):
    ssh unicorn-login-02
    cd <repo> && python experiments/init_opt_test/sweep.py --dry-run
    python experiments/init_opt_test/sweep.py
"""

from __future__ import annotations

import argparse
import itertools
import os
import subprocess
from pathlib import Path

from simple_slurm import Slurm

PROJECT = "init_opt_test"
REPO_DIR = Path(__file__).resolve().parents[2]
OUT_ROOT = Path("output") / PROJECT
LOG_DIR = Path("experiments") / PROJECT / "logs"

CONDA_BIN = "/home/sc3379/anaconda3/envs/sfm/bin"

# --- grid (setup.md) -------------------------------------------------------
PS_LIST = ["naive_ps", "cmplx_ps", "c1e2_exp1.0", "c1e3_exp1.0", "c1e4_exp1.0"]
PROPOSALS = ["exp"]
EXP_RATES = ["0.01", "0.05", "0.1", "0.25", "0.5", "0.75", "1.0"]
# abbreviation -> (train script, hydra loss_geometry) ; abbreviations match name_ext
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
# The `desa` and `thickstun` partitions are deliberately avoided: the init_test
# sweep already has its full grid queued there. `gpu` is the cluster-wide
# community pool (PriorityTier 15 vs 20 for the owned partitions, PreemptMode
# REQUEUE) -- these jobs are a few minutes each and TaskMgr makes them
# idempotent, so being preempted costs nothing. The four nodes owned by desa /
# thickstun are excluded so the sweep stays entirely off them.
PARTITION = "gpu"
# yu-compute-01 is excluded for a different reason: the desa NFS export is
# permission-denied there, so slurmd cannot even chdir into the submit dir or
# create the --output file. Jobs land in /tmp and die in <15s with no log
# (measured: 9 cells, all on that node, ExitCode 0:53).
EXCLUDE_NODES = ("desa-compute-01,kuleshov-compute-02,kuleshov-compute-03,"
                 "thickstun-compute-01,yu-compute-01")
# The community pool also holds pre-Turing cards (GTX 1080 Ti / Titan X / Titan
# Xp / V100). The env's torch 2.7.0+cu128 ships cubins for sm_75/80/86/90/100/120
# only, so those nodes hard-fail at the first kernel launch -- measured on
# snavely-compute-09 (GTX TITAN X, sm_52). Constraining to the arch features the
# cluster tags (there is no `turing` tag, so 2080 Ti nodes drop out too) leaves
# 90 of 143 nodes, all sm_80+.
CONSTRAINT = "ampere|ada|hopper|blackwell"
CPUS_PER_TASK = 4
MEM = "16G"
# The test pass is ~1954 batches; init_test's train+test runs took ~9 min, so an
# hour is generous. A short limit lets these backfill on the busy community pool.
TIME_LIMIT = "01:00:00"


def run_name(ps: str, geom: str, proposal: str, rate: str, seed: int) -> str:
    # Same layout as init_test so experiments/report.py parses it unchanged.
    # mode is not encoded: it is fixed for the whole project (the project name
    # carries it), and only searched variables belong in the run name.
    return (f"ps-{ps}_lg-{geom}_q-{proposal}{rate}"
            f"_qref-{REF_PROPOSAL}{REF_RATE}_lr{LR}_st{MAX_STEPS}_s{seed}")


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
            exclude=EXCLUDE_NODES,
            constraint=CONSTRAINT,
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
            # One rejected cell must not abandon the remaining dozens.
            try:
                slurm.sbatch(body, verbose=False)
            except Exception as exc:  # noqa: BLE001 - report and keep going
                failed.append((name, repr(exc)[:200]))
                continue
        submitted += 1

    print(f"grid cells        : {len(cells)}")
    print(f"already finished  : {skipped_done}")
    print(f"already in squeue : {skipped_queued}")
    print(f"{'would submit' if args.dry_run else 'submitted'}      : {submitted}")
    print(f"partition         : {PARTITION} -C '{CONSTRAINT}' (exclude {EXCLUDE_NODES})")
    if failed:
        print(f"FAILED to submit    : {len(failed)}")
        for name, err in failed[:5]:
            print(f"    {name}\n      {err}")
    print(f"runs   -> {OUT_ROOT}/")
    print(f"logs   -> {LOG_DIR}/")
    if args.dry_run and first_body is not None:
        name, slurm, body = first_body
        print(f"\n--- example submission: {job_name(name)} ---")
        print("$ sbatch << EOF")
        print(f"{slurm}\n{body}")
        print("EOF")


if __name__ == "__main__":
    main()
