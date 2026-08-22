# Agent.md

Guidance for coding agents working in this repository.

## Coding Rules

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific
instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require
constant clarification.

This repo has no test suite. The de-facto verification is a short training run whose
`test_wnelbo_ref` lands at or above `H(p)` (see **Invariants** below) — use it as the
regression check for any change to the bridge, loss, or proposal.

### 5. Minimalism Implementation

Make sure the codebase is easy-understanding, canonical, and concise.

### 6. RUN MODELS ON COMPUTE NODES

If you're on SLURM and the script needs to load / compute with a model, do it on a compute
node. DO NOT RUN ANY MODEL ON A LOGIN NODE. The runs here are small (a 3-layer MLP, V=10),
but this rule has no exception.

### 7. NO GIT OPERATIONS WITHOUT THE USER'S APPROVAL

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to
overcomplication, and clarifying questions come before implementation rather than after
mistakes.

---

## What This Repo Is

A minimal, single-file-per-concern testbed for a **hyperbolic-boundary bridge language model**
on a **unigram (sequence length 1)** toy distribution. Everything is small on purpose: the
point is to check that the bridge, the loss geometries, and the importance-weighted time
proposal are *numerically correct*, by comparing a trained MLP against a closed-form
Bayes-optimal model and against the analytic entropy `H(p)`.

The generative process: a target word `y` is mapped to a boundary angle `phi_y` on the
Poincaré disk; `HyperBridge.binary_bridge` samples a bridge state `z_t = (rho, theta)` at a
random time `t`; the model must recover `y` from `z_t`. Because `t` runs over an unbounded
range, it is drawn from a proposal `q(t)` and every per-sample loss is reweighted by `1/q(t)`.

## Repository Layout

```
main.py           HyperbolicDLM (LightningModule) + hydra entry point. Owns the
                  train/val/test steps, the per-step RNG seeding, and the "loss vs
                  reference metrics" split.
loss.py           HyperBridge (bridge sampler + horosphere geometry + poincare-polar
                  loss), Loss (cross-entropy loss + importance weighting), Proposal
                  (t samplers and their 1/q weights). LossGeometry / FlowPath are
                  string-tag dataclasses.
model.py          SmallMLP, MLPLM (the trained backbone; its lm_head IS the word
                  embedding), OptimalModel (closed-form Bayes-optimal logits = log p),
                  plus disk/vocab geometry helpers.
dataset.py        UnigramDataset / UnigramDataModule. Resolves the `ps` spec into an
                  exact-count token dataset and pins vocab_size to len(ps).
utils.py          TaskMgr (finished.json idempotency marker), save_results.
visualizer.py     Recorder (in-memory metric series), loss-curve and embedding-
                  concentration plots, DataMgr (writes both to the run folder).
geo_bridge.py     Standalone H^2 / H^d heat-kernel / geodesic library. loss.py
                  imports it for the general-d bridge (sample_radial,
                  _angular_boost, _reflect_to_target). Math is documented in
                  old/hyper_dm.md.
config/config.yaml  The only live config. config/data/unigram0109.yaml is empty and
                  unreferenced (config.yaml has no `defaults:` list).
experiments/      One folder per experiment project (see below). Untracked.
output/           Default hydra run dir; holds stale runs from before the metrics were
                  renamed (test_loss/test_nelbo/test_ce). Gitignored.
old/              Prior single-file iterations and the math notes (hyper_dm.md,
                  hyper_dlm.md). Gitignored; read-only reference, do not extend.
```

Dead-but-present code (do not delete unless asked, do not assume it is wired):
`model.MLPNLM`, `model.get_model`, `model.poisson_posterior_new`,
`HyperBridge.binary_bridge_loss_poincare_disk_polar_horocycle`,
`visualizer.plot_embedding_concentration` (nothing records `emb_*` series), and the
`LossGeometry` tags other than `poincare_polar` / `cross_entropy`.

### Key config knobs (`config/config.yaml`)

| key | values | note |
|---|---|---|
| `mode` | `tnb`, `opt` | `tnb` trains `MLPLM`; `opt` skips `trainer.fit` and only tests `OptimalModel` (the analytic reference) |
| `ps` | `naive_ps`, `cmplx_ps`, `cmplx_ps1`, `c1e3_exp1.0`, `c1e4_exp1.0`, `c1e5_exp1.0`, or an explicit list | sets the unigram distribution; `vocab_size` is **overwritten** from `len(ps)` in `main`, so setting it by hand does nothing |
| `loss_geometry` | `cross_entropy`, `poincare_polar` | the trained objective. Other `LossGeometry` tags raise |
| `flow_path` | `hyperbolic_boundary` | only value accepted |
| `loss_proposal_type` / `ref_proposal_type` | `exp`, `unif`, `truncated_exp`, `stratified_exp` | `exp` is the shipped default |
| `loss_proposal_exp_rate` / `ref_proposal_exp_rate` | float > 0 | `0.1` is the shipped default |
| `hyper_dt`, `hyper_T` | `0.01`, `1e7` | together bound `t` to `[0.01, 1e5]` |
| `trainable_word_embedding` | bool | `false` pins `phi_v` to the fixed equally spaced angles; the lm_head still trains as the logit readout |
| `unif_word_embedding` | bool | spread the lm_head rows evenly at init instead of kaiming-uniform |
| `gradient_clip_val` | `1.0` | required: the `1/q(t)` weights are heavy-tailed and `poincare_polar` diverges to NaN without it |
| `train_size` / `val_size` / `test_size` | ints | `test_size=4e6` is the shipped value — the estimator's standard error is what makes the `>= H(p)` check meaningful |

`run_name` and `folder` are interpolated templates; `folder` doubles as `hydra.run.dir`.
Sweeps override `folder` directly.

### Metrics

`_log_losses` writes six scalars per stage (`train_`/`val_`/`test_` prefix):

- `wloss` / `wloss_std` — the **trained** objective (`loss_geometry`, importance-weighted).
  `wloss.mean()` is what `training_step` returns and what the `Recorder` stores as
  `train_loss` / `val_loss` / `test_loss`.
- `wnelbo_ref` — the poincaré-polar ELBO estimate on the *reference* proposal path.
  **This is the headline number**: importance-weighted, so its mean estimates the whole
  integral over `t`.
- `nelbo_ref` — the same integrand **unweighted**. Not an ELBO on its own; it is what the
  per-`t` loss looks like under the proposal. Don't quote it as a bound.
- `wce_ref` / `ce_ref` — the denoising cross-entropy, weighted / unweighted.

The loss path and the reference path use **independent RNG streams** (`salt=0` vs `salt=1`
in `_make_step_generator`), so the reference metrics are comparable across runs trained on
different objectives.

## Invariants

Break any of these and the numbers silently stop meaning what they claim:

1. **Logits are a residual, not a distribution.** The model's posterior is
   `softmax(horosphere_dists + logits)`. Scoring plain `cross_entropy(logits, targets)`
   trains the logits to *be* the posterior, which the poincaré-polar readout then
   double-counts — measured: the reported ELBO inflates 0.4997 → 0.8714 (1.74×) for the
   exact Bayes solution, and the weighted CE becomes a divergent integral.
2. **`test_wnelbo_ref >= H(p)`.** `H(naive_ps) = 0.5003`, `H(cmplx_ps) = 1.6664`,
   `H(cmplx_ps1) = 2.2985` nats. A trained model dipping *below* `H(p)` means a side channel
   leaked — historically, leaving `theta` unwrapped in `binary_rotate_with_target` (it must be
   `remainder(..., 2*pi)`, since the loss only ever sees `theta mod 2*pi`).
3. **Bridge quantities stay float64.** `ts`, `rhos`, `thetas` and the whole horosphere
   computation are float64; only the model input `z` and the logits are cast to float32.
   The polar losses assert this.
4. **`rho` is capped at `RHO_MAX = 350`.** `cosh` overflows past `ss ~ 710` and both terms of
   the horosphere log underflow past `rho ~ 372`. The cap is statistically a no-op — by then
   the bridge angle already identifies the target to full float64 precision.
5. **Half-angle forms are load-bearing.** `sin_half_sq` / `cos_half_sq` and the
   `atan2(sin a, cos_half_sq·e^-rho − sin_half_sq·e^+rho)` form exist because the direct
   expressions cancel catastrophically at large `rho` and produce `0 * inf = NaN` in the
   backward pass. Don't "simplify" them back.
6. **Eval RNG must depend on `batch_idx` and `stage`.** Lightning does not advance
   `global_step` during validate/test; seeding on `global_step` alone gave 1953/1953
   byte-identical test batches, putting a floor on the standard error that no `test_size`
   could lower.

---

## Cluster Environment 

### Slurm Usage Guide

1. Use ``nice`` to control the priority
2. Ask before canceling any job, you're only allowed to use ``nice`` to prioritize / de-prioritize jobs.

### Unicorn Slurm

Single Cornell CoECIS SLURM cluster; `sc3379` and `ch2263` are two accounts on it.
SLURM binaries live at `/usr/local/slurm/current/bin` (prepend to `PATH`). Partition
`TIMELIMIT` is `infinite`, so a run finishes in one job; resubmitting the same
`OUTPUT_DIR` auto-resumes from `checkpoints/last.ckpt`.

**sc3379@Unicorn** — the account Claude Code sessions run as; submit SLURM directly.

- Interconnection between sc3379 and ch2263: local account here. `sbatch`/`squeue`
  work directly once `/usr/local/slurm/current/bin` is on `PATH`. To reach `ch2263`,
- Interconnection between sc3379@unicorn and shengyenc@arc
  - Use ``tailscale`` to check the IP address of the target login node and then use
  ``ssh -o "ProxyCommand=/home/sc3379/bin/tailscale --socket=/home/sc3379/.tailscale/{target_host_socket} nc %h %p" -i ~/.ssh/unicorn_internal shengyenc@{ip_address}``
  - ``{target_host_socket}`` is the ``tailscaled`` daemon socket of the host you run this from
    (its filename encodes that host — e.g. ``tailscaled-unicorn-login-02.sock``; ``ls
    ~/.tailscale`` may list several, pick the one matching ``hostname`` — only that daemon is on
    the tailnet). ``{ip_address}`` comes from ``tailscale status``; the magicDNS name also works as
    ``%h`` (``tinkercliffs1``/``tinkercliffs2``/``falcon1``/``falcon2-1`` — note falcon2's tailnet
    name is ``falcon2-1``). Use ``unicorn_internal`` (no passphrase) for non-interactive login —
    ``id_rsa`` is also authorized on ARC but passphrase-protected, so it fails under ``BatchMode``.
- identity file: not needed for local use; to SSH into `ch2263` use
  `/home/sc3379/.ssh/unicorn_internal` (public key `.pub` alongside it).
- Partitions: `thickstun,desa` (priority). Add `--exclude=desa-compute-01` — the
  2080 Ti (11 GB) OOMs at seq 1024.
- GPUs:
  - `thickstun-compute-01` — 8× RTX 6000 Ada, 48 GB   (partition `thickstun`)
  - `kuleshov-compute-02`  — 10× RTX A6000, 48 GB      (partition `desa`)
  - `kuleshov-compute-03`  — 10× RTX A5000, 24 GB      (partition `desa`)
  - `desa-compute-01`      — 8× RTX 2080 Ti, 11 GB      (partition `desa`; EXCLUDE)

**ch2263@Unicorn** — borrowed account, reached over SSH from sc3379.

- Interconnection between sc3379 and ch2263:
  `ssh -i /home/sc3379/.ssh/unicorn_internal ch2263@unicorn-login-02.coecis.cornell.edu`.
  SLURM needs a **login shell** — wrap remote commands as `ssh ... 'bash -lc "<cmd>"'`
  (`sbatch`/`squeue` are not on the non-login `PATH`).
- identity file: `/home/sc3379/.ssh/unicorn_internal` (its `.pub` is in ch2263's
  `~/.ssh/authorized_keys`).
- conda: `source ~/miniconda3/etc/profile.d/conda.sh; conda activate hodlr`.
  s-flm requires Python ≥3.10 (`dataclass(kw_only=)`); `hodlr` is py3.11 with
  torch 2.9/cu128 + lightning/hydra/transformers/datasets — leaf deps added:
  `wandb simple_slurm matplotlib scipy scikit-learn`.
- Partitions: `nlplarge`, `nlplarge-claire-highpri` (both map to one node,
  `nlplarge-compute-01`).
- GPUs:
  - `nlplarge-compute-01` — 8× A100-SXM4-80GB, 80 GB   (partitions `nlplarge`, `nlplarge-claire-highpri`)
- Storage:
  - Use ``/scratch/ch2263`` to save checkpoints and dataset. But the storage is only available on compute nodes

### ARC Slurm

Virginia Tech ARC — two relevant clusters, each with its own login nodes. ARC `/home`
and `/projects` are shared across clusters. Jobs require an allocation
(`--account=<allocation>`); GPU queues follow the `<gpu>_normal_q` / `<gpu>_preemptable_q`
naming (preemptable = lower priority, can be killed). Request GPUs with
`--partition=<queue> --gres=gpu:<n>`. (Exact submission flags: see the docs.)

Login Nodes
- tinkercliffs1, tinkercliffs2 — TinkerCliffs cluster
- falcon1, falcon2 — Falcon cluster

- Interconnection between login nodes: 
  - identity file ``~/.ssh/id_rsa``
- Interconnection between Unicorn and Arc:
  - Use ``tailscale`` to check the IP address of the target login node and then use
  ``ssh -o "ProxyCommand=/home/shengyenc/bin/tailscale --socket=/home/shengyenc/.tailscale/{target_host_socket} nc %h %p" -i ~/.ssh/id_rsa sc3379@{ip_address}``
  - ``{target_host_socket}`` is the ``tailscaled`` daemon socket of the ARC node you run this from
    (its filename encodes that node; see ``ls ~/.tailscale``). This reverse direction is not yet
    verified from this repo.
- Storage:
  - Use ``/scratch/shengyenc`` to save checkpoints and dataset. But the storage is only available on compute nodes

- GPUs / Partitions (source: https://www.docs.arc.vt.edu/resources/gpu.html):
  - TinkerCliffs (login: tinkercliffs1/2)
    - A100-80GB  — 112 GPUs (14 nodes × 8) | `a100_normal_q`, `a100_preemptable_q`
    - H200-141GB —  56 GPUs ( 7 nodes × 8) | `h200_normal_q`, `h200_preemptable_q`
  - Falcon (login: falcon1/2)
    - L40S-48GB — 80 GPUs  (20 nodes × 4) | `l40s_normal_q`, `l40s_preemptable_q`
    - A30-24GB  — 128 GPUs (32 nodes × 4) | `a30_normal_q`, `a30_preemptable_q`
    - V100-16GB — 80 GPUs  (40 nodes × 2) | `v100_normal_q`, `v100_preemptable_q`
    - T4-16GB   — 18 GPUs  (18 nodes × 1) | `t4_normal_q`, `t4_preemptable_q`

(ARC also exposes A100-80GB on the CUI and Biomed clusters via their own `a100_*_q`
queues — see the docs page above.)

---

## Experimental Scripts Write Up

For each experiment, create a project folder under ``experiments`` with ``{project_name}`` and store the checkpoints and results of each run under ``experiments/{project_name}/{run_name}``.

### Anaconda Environment

Follow ``README.md``: ``conda create -n sfm python=3.12`` then ``pip install -r requirements.txt``.
Python **≥3.10** is required (the code uses ``dataclass(kw_only=)``); 3.12 is the reference.

- ``torch`` / ``numpy`` are intentionally **not** pinned in ``requirements.txt`` (the NGC base
  image provides them) — install a ``torch`` build matching the node CUDA yourself
  (cu128 for the A100 / RTX-6000-Ada nodes).
- ``simple-slurm==0.3.6`` (for the sweeps) is now pinned in ``requirements.txt``, so
  ``pip install -r requirements.txt`` covers it.
- Export ``TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1`` when loading checkpoints — torch's
  ``weights_only`` default rejects the pickled Lightning ckpts.
- Reusing an existing ``sfm`` env instead of building ``sfm``, if there is no env named ``sfm``, build it via

```bash
conda create -n sfm python=3.12
conda activate sfm
pip install -r requirements.txt
```

### Training & Sampling Run Setup

- Create functions / classes in ``experiment.py`` to set up the soft link of the checkpoint for training and sampling run (if needed)
- If use ``ch2263@Unicorn``, save the checkpoints at ``/scratch/ch2263/syc_workspace/sfm_output/{project_name}/{run_name}/checkpoints`` and create a soft link at ``${OUTPUT_DIR}/checkpoints`` to link the actual checkpoint path ``/scratch/ch2263/syc_workspace/sfm_output/{project_name}/{run_name}/checkpoints`` before the training starts. This should be handle in ``experiment.py``
- If use ``shengyenc@ARC``, save the checkpoints at ``/scratch/shengyenc/syc_workspace/sfm_output/{project_name}/{run_name}/checkpoints`` and create a soft link at ``${OUTPUT_DIR}/checkpoints`` to link the actual checkpoint path ``/scratch/shengyenc/syc_workspace/sfm_output/{project_name}/{run_name}/checkpoints`` before the training starts. This should be handle in ``experiment.py``
- The sweep.py of each experiment should use setup method in ``experiment.py`` to handle the storage of ch2263@unicorn and shengyenc@ARC

### Training Script

Under ``scripts/train/{dataset_name}``, 

one bash file per method ``{method}.sh`` — **one training run per script** (no sweeps or
loops inside; the sweep parameterizes it via env vars).

### Sweep Script

1. Under ``experiments/{project_name}``
2. One experiment project script for one project
3. Use python and ``simple_slurm`` to submit jobs to slurm
4. Don't assign ``nice`` in the sweep script. The sweep script only submit the jobs

One folder per project under `experiments/{project_name}/`, containing:

- `sweep.sh` (or `sweep.py`) — **orchestration only**. It loops over the grid and calls
  `python -u main.py <overrides> folder=experiments/{project}/{run_name}`; it never inlines
  model code. Knobs come in as env vars with defaults (see `experiments/init_test/sweep.sh`
  as the reference), plus an `EXTRA` passthrough for ad-hoc hydra overrides.
- `EXPERIMENT.md` — hypothesis, design, GPU allocation, expected wall-clock.
- `RESULTS.md` — numerical table + insights and conclusions.
- `{run_name}/` — one folder per run, written by hydra.

`{run_name}` is semantic and encodes only the *searched* variables, abbreviated:
`{var1abbr}-{val1}_{var2abbr}-{val2}_...` (e.g. `lg-cross_entropy_q-exp0.1_lr0.001_st20000_s42`).

**Orchestration only** — the sweep CALLS the train + sample scripts; it never inlines
``python -m main``. It builds the parameter grid, submits one SLURM job per cell (train
then eval), and is idempotent/resumable: skip a cell whose ``finished.json`` exists or
whose job name is already in ``squeue``.

Unique and semanticful name for each slurm job, ex ``{project_name}_{var1}-{var1_value}_{var2}-{var2_value}...``, use abbr for each variable nam ``var1``, followed by a parameter value ``var1_value``. Only record the searched parameters in the project

### SLURM Env Setup

The sweep submits one SLURM job per run with `simple_slurm`; each job activates the
conda env (see `## Cluster Environment`), then runs the train script followed by the
sample/eval script. Boilerplate every job body needs:

```bash
# simple_slurm resources: partition=<cluster queue>, gres=gpu:<N>, ntasks=1,
#   cpus_per_task=16, mem=128G, time=..., output=experiments/<project>/logs/<run>_%j.log
export TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1
export SLURM_JOB_NAME=bash                      # Lightning uses its own DDP launcher, not srun
export NCCL_P2P_DISABLE=1 NCCL_IB_DISABLE=1     # avoid NCCL hangs on single-/multi-GPU
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PATH=<conda-env>/bin:$PATH               # sc3379: .../envs/sfm ; ch2263: .../envs/hodlr
cd <REPO>
OUTPUT_DIR=... DEVICES=<N> PER_GPU_BS=<b> MAX_STEPS=... [MODEL=... SEQ_LEN=... GLOBAL_BATCH=...] \
    bash scripts/train/<dataset>/<method>.sh
CKPT_PATH=<out>/checkpoints/last.ckpt OUTPUT_DIR=<out>/eval DEVICES=1 \
    bash scripts/sample/<dataset>/<method>.sh
```

- **Gradient accumulation** is derived by the config, not set by hand:
  `accumulate_grad_batches = global_batch_size / (devices × per_gpu_batch × num_nodes)`.
  Pick `GLOBAL_BATCH`/`DEVICES`/`PER_GPU_BS` so it divides evenly — the dataloader
  asserts `global_batch == per_gpu_batch × num_nodes × num_gpus × accum`.
- **Eval on one GPU** (`DEVICES=1`; the sample scripts set `CUDA_VISIBLE_DEVICES=0`) so
  `torch.cuda.device_count()` matches `trainer.devices` and the assert holds.
- **Idempotent + resumable**: skip a cell if its `eval/ppl.json` exists or its job name
  is already in `squeue`; resubmitting the same `OUTPUT_DIR` auto-resumes from `last.ckpt`.

### Training and Sampling Outputs

All checkpoints and generated text go under ``outputs/{project_name}`` (same name as the
experiment folder under ``experiments/``), one subfolder per run:

Each run folder holds:

```
experiments/{project}/{run_name}/
├── .hydra/{config,hydra,overrides}.yaml   # exact resolved config
├── main.log                               # hydra job log
├── loss_history.json                      # Recorder series: train_loss/val_loss/test_loss
├── loss_curves.jpg                        # plot of the above
├── test_metrics.json                      # the six test_* scalars
└── finished.json                          # TaskMgr marker
```

**Idempotency:** `TaskMgr.check_finished()` reads `finished.json` and returns immediately if
the run already completed, so re-running a sweep is safe and only fills gaps. To force a redo,
delete `finished.json` (or the whole run folder).

Sweeps that submit to SLURM should use `simple_slurm`, one job per grid cell, with a unique
job name matching `{run_name}`, and should skip a cell whose `finished.json` exists or whose
job name is already in `squeue`. Don't set `nice` inside a sweep script — the sweep only
submits.

- ``{run_name}`` = the semantic SLURM job name (e.g. ``{var}-{val}_...``).
- ``experiments/report.py {project_name}`` scans every ``{run_name}/eval/`` and writes a
  summary table to ``experiments/{project_name}/RESULTS.md``.

### Reports and Experiment

- For each experimental project, create a experimental arch file called ``experiments/{project_name}/EXPERIMENT.md`` to record the experimental design, hypothesis, GPU allocation, and expected wall clock time
- For each experimental project, create a experimental report, called ``experiments/{project_name}/RESULTS.md`` to record the numerical and qualitative results of each experiment. Provide table for the numerical results and inisights and conclusions of the experiment.