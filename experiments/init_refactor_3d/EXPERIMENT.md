# init_refactor_3d — `init_test`'s grid on the general-d bridge, `hyper_dim = 3`

First run of the arbitrary-dimension bridge (`HyperBridge.bridge` /
`Loss.weighted_loss`, the `claude/init-refactor-nd` branch) at a dimension the
binary code path cannot reach. One of three sibling projects — `init_refactor_3d`,
`init_refactor_9d`, `init_refactor_16d` — that differ only in `hyper_dim`.

## Hypothesis

1. **The general-d path is a valid ELBO at d = 3.** `test_wnelbo_ref >= H(p)` in
   every trained cell (`H(naive_ps) = 0.5003`, `H(cmplx_ps) = 1.6664` nats), and the
   best cells land on it from above, as the d = 2 `init_test` cells do. Pre-check
   (Bayes-optimal model, `mode=opt`, `cmplx_ps`, 1M test samples, 2080 Ti):
   `wnelbo_ref = 1.6712 ± 0.0065` — on `H(p)`.
2. **The d = 2 findings carry over**: `cross_entropy` and `poincare_polar` training
   both reach `H(p)`, the `exp` rate sweet spot stays at or below the ~0.304
   variance cliff, and more steps help the `poincare_polar` cells more than the CE
   cells.
3. **Across the siblings** (3 → 9 → 16), the bridge identifies the word sooner in
   `t` (drift `(d-1)/2`), so `wce_ref` shrinks with d while the ELBO stays pinned
   at `H(p)`; the importance-weighted estimator's standard deviation grows with d
   (measured at the Bayes model: `wnelbo_ref_std` 6.5 → 23 → 29 for d = 3 → 9 → 11).

## What changed in the code to run this

- `main.py`: the model input is `z = (rho, u)` with `u` the bridge direction, a
  unit vector in `R^hyper_dim` — so `MLPLM.input_dim = hyper_dim + 1` and `z` is a
  `cat`, not the binary `stack([rho, theta])`. `bridge()` is handed
  `emb_dim=hyper_dim` for the `word_embedding is None` fallback.
- `script/train/{ce,pp}.sh`: `hyper_dim` comes from a `HYPER_DIM` env var
  (default 2, so `init_test` is unchanged).
- `word_embedding` is the trained `lm_head` weight `(V, hyper_dim)`, as at d = 2
  (`trainable_word_embedding=true`, `unif_word_embedding=false` — config defaults).

## Design

Grid from `setup.md` — identical to `init_test` except `hyper_dim`:
2 × 2 × 7 × 4 × 3 = **336 runs**, one SLURM job each.

| variable | values |
|---|---|
| `ps` | `naive_ps`, `cmplx_ps` |
| `loss_geometry` | `cross_entropy`, `poincare_polar` |
| `loss_proposal_exp_rate` | 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0 |
| `max_steps` | 20000, 40000, 100000, 200000 |
| `seed` | 0, 1, 2 |

Fixed: `hyper_dim=3`, `lr=1e-3`, `gradient_clip_val=1.0`, `test_size=4e6`,
`batch_size=2048`, `ref_proposal_type=exp`, `ref_proposal_exp_rate=0.1`.

`run_name` is byte-identical to `init_test`'s (the dimension is carried by the
project name), so `experiments/report.py init_refactor_3d` works unchanged and the
cells pair 1:1 with `init_test` for a d = 2 vs d = 3 comparison.

Note on the bridge at d > 2: `bridge()` clamps `t` at `_radial_t_max(d)` (97 at
d = 3, 5.6 at d = 9, 1.5 at d = 16) because the radial marginal is formed in linear
float64. Past that `t` the direction already identifies the word to full precision,
so the loss there is 0 regardless — statistically a no-op, but it means most of
the `exp(0.1)` mass at d = 9 / 16 sits on the clamp.

## GPU allocation

Both owned partitions, all four nodes — `--partition=thickstun,desa`, 1 GPU, 4
CPUs, 16 GB per job; `desa-compute-01` included (the model uses well under 1 GB).
Per-cell `--time` scales with `max_steps` (2× the 2080 Ti pilot rate of ~0.05
s/step + 5 min test): 43 min / 1 h 10 / 3 h 10 / 5 h 50.

Seed 0 at `--nice=0`, replicates at `--nice=50`, so a complete single-seed grid
lands first.

## Wall clock (expected)

Pilot on the 2080 Ti (the slowest node): ~0.04 s/step for d = 3 (the odd-d radial
sampler costs ~5 ms per `bridge()` call), 4M-sample test ≈ 80 s. Per
(ps, rate, geometry, seed) column: 360k steps ≈ 4.5 h → **~390 GPU-h** per
project. With the ~10 GPUs free at submission (the rest hold the user's `simpflm`
jobs and other users' work) that is ~1.5–2 days per project; faster as GPUs free up.

## Reporting

- `python experiments/report.py init_refactor_3d` → `RESULTS.md`.
- Cross-dimension comparison: the same command for `_9d` / `_16d`, plus
  `experiments/init_test/RESULTS.md` for d = 2.

## Grid extension (2026-08-23)

Added on request: the `init_test` `c1e4_exp1.0` slice at d = 3 —
`ps=c1e4_exp1.0` (V = 10^4 geometric, H = 1.0407), `max_steps=20000`, both
geometries × 7 rates × 3 seeds = 42 runs. Same run-name scheme, same output root,
so `report.py` picks it up as its own section. ~38 min/cell at d = 2 on the
2080 Ti; similar at d = 3 (the V = 10^4 loss matrices dominate, not the sampler).
