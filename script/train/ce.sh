#!/usr/bin/env bash
# ONE training run of the unigram model on the CROSS-ENTROPY objective.
#
# No sweeps or loops here: experiments/init_test/sweep.py builds the grid and
# submits one SLURM job per cell, parameterizing this script via env vars.
#
# Knobs (env vars, all optional):
#   OUTPUT_DIR  run directory (= hydra.run.dir, holds metrics + logs)
#   PYTHON PS PROPOSAL EXP_RATE MAX_STEPS SEED LR TEST_SIZE PER_GPU_BS EXTRA
#
# The reference pass (which reports test_wnelbo_ref / test_ce_ref) uses its OWN
# proposal, pinned to exp(0.1) by experiments/init_test/setup.md, INDEPENDENT of
# the loss proposal. That is what makes the reference metrics comparable across
# cells with different loss_proposal_exp_rate -- and exp(0.1) sits below the
# rate ~0.304 cliff past which the weighted estimator has infinite variance.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_DIR}"

PYTHON="${PYTHON:-/home/sc3379/anaconda3/envs/sfm/bin/python}"
PS="${PS:-naive_ps}"
PROPOSAL="${PROPOSAL:-exp}"
EXP_RATE="${EXP_RATE:-0.1}"
REF_PROPOSAL="${REF_PROPOSAL:-exp}"
REF_RATE="${REF_RATE:-0.1}"
MAX_STEPS="${MAX_STEPS:-20000}"
SEED="${SEED:-1}"
LR="${LR:-0.001}"
TEST_SIZE="${TEST_SIZE:-4000000}"
PER_GPU_BS="${PER_GPU_BS:-2048}"
OUTPUT_DIR="${OUTPUT_DIR:-output/init_test/ps-${PS}_lg-ce_q-${PROPOSAL}${EXP_RATE}_qref-${REF_PROPOSAL}${REF_RATE}_lr${LR}_st${MAX_STEPS}_s${SEED}}"
EXTRA="${EXTRA:-}"

# shellcheck disable=SC2086  # EXTRA is intentionally word-split
exec "${PYTHON}" -u main.py \
    loss_geometry=cross_entropy \
    ps="${PS}" \
    lr="${LR}" \
    max_steps="${MAX_STEPS}" \
    test_size="${TEST_SIZE}" \
    batch_size="${PER_GPU_BS}" \
    seed="${SEED}" \
    hyper_dim=2 \
    gradient_clip_val=1.0 \
    loss_proposal_type="${PROPOSAL}" \
    loss_proposal_exp_rate="${EXP_RATE}" \
    ref_proposal_type="${REF_PROPOSAL}" \
    ref_proposal_exp_rate="${REF_RATE}" \
    folder="${OUTPUT_DIR}" \
    ${EXTRA}
