# init_test_refactor — does the refactor reproduce `init_test`?

A reproduction run, not new science. The `max_steps=20000` slice of `init_test`'s
grid re-executed against the post-refactor tree.

Companion to `init_opt_test_refactor`. That project holds the model *exact* and so
isolates the bridge / loss / proposal / metric plumbing; this one actually
**trains**, so it additionally exercises `training_step`, `validation_step`, the
optimizer trajectory, gradient clipping, and the recorder series that feed
`loss_curves.jpg`. Read the two together: if `opt` reproduces and this does not,
the divergence is in the training path, not the geometry.

## Hypothesis

**Every cell reproduces its `init_test` counterpart bit-exactly.**

The refactor moved `training_step` / `validation_step` / `test_step`, the per-step
RNG seeding, and the recorder writes into `trainer.py:BaseTrainer`. Those are the
functions this project's numbers flow through, so it is the direct test of that
move. Specifically at risk and checked here:

1. **The RNG stream is unchanged.** `_make_step_generator` now reads `self.seed`
   (set by the subclass) where it previously read `self.config.seed`. Same value,
   but the indirection is new. Any drift in the seed sequence changes every `t`
   draw and every cell moves.
2. **`global_step` / `batch_idx` / `stage` still enter the seed.** Invariant 6:
   Lightning does not advance `global_step` during validate/test, so eval batches
   would become byte-identical to each other if the seed lost `batch_idx`. That
   would not necessarily change the *mean*, but it inflates the standard error —
   so watch `test_wloss_std` as well as `test_wloss`.
3. **The recorder series survived the move.** The refactor briefly renamed them to
   `train_wloss` / `valid_wloss`, which `plot_loss_curves` does not look for. The
   check is that `loss_history.json` again carries `train_loss` (20000 points),
   `val_loss`, and `test_loss`.

Bit-exactness is the bar, not "within noise": everything is seeded, and a prior
parity run of the refactored tree against pre-refactor `HEAD` measured a
run-to-run nondeterminism floor of exactly `0.000e+00` on this hardware, so there
is no noise budget to spend.

`test_wnelbo_ref >= H(p)` (`H(naive_ps) = 0.5003`, `H(cmplx_ps) = 1.6664` nats)
should hold in every trained cell, as it does in the reference.

## Design

Grid from `setup.md` — `init_test`'s grid narrowed to the single
`max_steps=20000` slice — 2 × 2 × 7 × 1 × 3 = **84 runs**, one SLURM job each:

| variable | values |
|---|---|
| `ps` | `naive_ps`, `cmplx_ps` |
| `loss_geometry` | `cross_entropy`, `poincare_polar` |
| `loss_proposal_exp_rate` | 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0 |
| `max_steps` | 20000 |
| `seed` | 0, 1, 2 |

Fixed: `hyper_dim=2`, `lr=1e-3`, `gradient_clip_val=1.0`, `test_size=4e6`,
`batch_size=2048`, `ref_proposal_type=exp`, `ref_proposal_exp_rate=0.1`.

All 84 cells have a matching `init_test` cell (verified by directory listing), and
`run_name` is byte-identical, so the comparison is per-cell with no mapping table.

The reference proposal stays pinned at `exp(0.1)` and untied from the swept
`loss_proposal_exp_rate` — that is what makes `test_wnelbo_ref` / `test_ce_ref`
comparable across rate cells, and `exp(0.1)` sits below the rate ≈ 0.304 cliff
past which the weighted estimator has infinite variance.

`gradient_clip_val=1.0` is load-bearing, not cosmetic: the `1/q(t)` weights are
heavy-tailed and the `poincare_polar` objective diverges to NaN without it.

## GPU allocation

Both owned partitions, all four nodes — `--partition=thickstun,desa`, 1 GPU per
job, 4 CPUs, 16 GB, 1 h limit. `desa-compute-01` is **not** excluded; see
`init_opt_test_refactor/EXPERIMENT.md` for why, and note that `init_test` — the
project this reproduces — ran its entire grid on exactly that node.

Seed 0 is submitted at `--nice=0` and the replicate seeds at `--nice=50`, so a
complete single-seed grid lands first and the replicates fill in behind it. That
way a partial sweep is still a readable result rather than a ragged grid.

## Wall clock (expected)

`init_test` measured ~9 min per cell for train(20k) + test(4M). 84 jobs over the
free slots on the two partitions — roughly 1–3 h wall clock, dominated by
queueing behind the other sweeps already on these nodes.

## Reporting

- `python experiments/report.py init_test_refactor` → `RESULTS.md` in the same
  layout as `init_test`.
- `python experiments/compare_reproduction.py init_test_refactor init_test` → the
  per-cell verdict; exits non-zero if any paired cell exceeds tolerance.
