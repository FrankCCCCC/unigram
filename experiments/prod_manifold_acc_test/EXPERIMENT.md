# prod_manifold_acc_test

Bayes-optimal (`mode=opt`) reference numbers on the product manifold
`H^3 x H^3 x H^3`, swept over SIX curvature assignments, under the **tensorized**
product-manifold path.

## Hypothesis

1. **Accuracy is unchanged by the acceleration.** The per-factor python loops in
   `poincare_bridge_prod`, `HyperbolicModelBase.horosphere_geometry` and
   `Loss.bridge_loss_elbo_refactor` were replaced by tensor ops over a factor
   axis, and `sample_radial` now takes a per-factor curvature vector. Unit
   checks show the deterministic parts agree with the loops to <= 2e-15 and the
   sampler's law is unchanged, but the *reported statistics* have never been
   compared end to end. The `k-mix` cells here are a byte-for-byte re-run of
   `init_opt_test_3x3d_refactor_new`'s grid, so its published table is the
   control: every metric must agree within Monte-Carlo error
   (`|delta| <~ 3 sqrt(2 var / 4e6)`).
2. **Curvature moves the estimator, not the bound.** `wnelbo_ref` is a *bound on
   the NLL* and is pinned at the exp(0.1) reference proposal, so across the five
   UNIFORM curvatures `{-0.01, -0.05, -1.0, -3.0, -10.0}` it should stay near
   `H(p)` while its per-sample variance changes: curvature rescales the heat
   time (`u = kappa rho`, `max_heat_time ~ _radial_t_max(3) R^2`), so it decides
   which noise levels get training mass, not what the optimum is.
3. **The mixed geometry is dominated by its tightest factor.** `main_refactor`
   clamps `t` to the MINIMUM over factors of `_radial_t_max(3) R_m^2`, so
   `k-mix` = `[-0.01, -10.0, -1.0]` should track the uniform `-10.0` cell rather
   than sitting between the three.

## Design

`mode=opt`, so `trainer.fit` is skipped: `lr`, `max_steps` and
`gradient_clip_val` are inert and only the 4,000,000-sample test pass runs.
`OptimalModelRefactor` is deterministic and parameter-free, so each cell reports
what the EXACT posterior scores on that geometry.

| axis | values | n |
|---|---|---|
| `ps` | `naive_ps`, `cmplx_ps`, `c1e4_exp1.0` | 3 |
| product curvature (`prod_factor_dim=[3,3,3]`) | `mix`=`[-0.01,-10.0,-1.0]`, and uniform `[-x,-x,-x]` for x in `{0.01, 0.05, 1.0, 3.0, 10.0}` | 6 |
| `loss_geometry` | `cross_entropy`, `poincare_polar` | 2 |
| `loss_proposal_exp_rate` | `0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0` | 7 |
| `seed` | `0, 1, 2` | 3 |

**756 cells**, one SLURM job each. Fixed: `loss_proposal_type=exp`,
`ref_proposal_type=exp`, `ref_proposal_exp_rate=0.1`, `test_size=4e6`,
`batch_size=2048`, `lr=1e-3`, `max_steps=20000`, `gradient_clip_val=1.0`.

Only `wloss` varies with `loss_geometry` and `loss_proposal_exp_rate`: the four
reference metrics are drawn from an INDEPENDENT RNG stream (`salt=1`) at the
pinned exp(0.1) proposal, so within one `(ps, curvature, seed)` they are the same
quantity measured 14 times. That redundancy is deliberate -- it is a free
14-fold replication of the reference estimator, and its spread across cells is a
direct read on the estimator's own noise.

## GPU allocation

Submitted to the cluster-wide `gpu` partition rather than `thickstun,desa`: the
latter is fully occupied by `init_test_3x3d_refactor_new` (~460 queued), and
these cells are small enough to run anywhere. `--constraint` gates on the
cluster's `gpu-low/mid/high` features by measured peak memory rather than by
node name, so the wide partition stays safe.

- 1 GPU, 2 CPUs, 16 GB host RAM per cell.
- Seed 0 goes in at `nice=0` and the replicates behind it, so a complete
  single-seed grid lands first (`sweep_lib`'s policy).

## Expected wall clock

MEASURED (grid completed 2026-09-09, 756/756, zero failures):

| dataset | per-cell wall clock | pre-acceleration cost model |
|---|---|---|
| `naive_ps`, `cmplx_ps` (V=10) | 35-62 s | ~250 s |
| `c1e4_exp1.0` (V=10000) | 325-462 s | ~720 s |

Whole grid: ~1 h 40 m wall clock at 8-27 concurrent cells, ~26 GPU-h. All cells
ran on `thickstun-compute-01` / `kuleshov-compute-02,03`; the wider `gpu`
partition sits at PriorityTier 15 against the owner partitions' 20 and never
scheduled, so the extra eligibility only ever helped as a fallback.

## Running it

    cd <repo>
    python experiments/prod_manifold_acc_test/sweep.py --dry-run
    python experiments/prod_manifold_acc_test/sweep.py

Idempotent: a cell is skipped when its `test_metrics.json` exists or its job name
is already in `squeue`. Then

    python experiments/report.py prod_manifold_acc_test
