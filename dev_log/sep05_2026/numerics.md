# Numerical issues and cautions — Sep 5, 2026

Everything below was measured in-session on `thickstun-compute-01` / `kuleshov-compute-03`
with the shipped proposal (`hyper_dt=0.01`, `hyper_T=1e7`, `exp` rate 0.1) unless stated
otherwise. Numbers are reproducible; the scripts lived in the session scratchpad and are
not checked in.

---

## 0. The one fact behind most of this

**The bridge's angular concentration is `1 - alpha ~ e^{-2u}`**, with `u = kappa*rho` the
dimensionless radius and `alpha = <x, theta>`. float64's machine epsilon is
`2.22e-16 = e^{-36.0}` (`torch.finfo(float64).eps`), so `e^{-2u} < eps` exactly when
**`u > 18.0`**.

Measured (`_angular_boost` at fixed `u`, d=3, 100k draws):

| u | cosh(u) | median 1-alpha | e^{-2u} | true D | ulp(cosh u) |
|---|---|---|---|---|---|
| 10 | 1.1e4 | 4.08e-09 | 2.06e-09 | 9.0e-05 | 2.5e-12 |
| **18** | 3.3e7 | **4.67e-16** | 2.32e-16 | 3.1e-08 | 7.3e-09 |
| 20 | 2.4e8 | 8.49e-18 | 4.25e-18 | 4.1e-09 | **5.4e-08** |
| 50 | 2.6e21 | 7.42e-44 | 3.72e-44 | 3.9e-22 | 5.8e+05 |

The last two columns cross between u=18 and u=20: past there the true `D` sits below the
rounding noise of `cosh(u)`. Under the shipped proposal at d=3, `rho` has **median 7.7,
p99 48.7, max 114.7** — the failure region is not a tail, it is where the bridge lives.

Nothing overflows there. `cosh(50) = 2.6e21` against a float64 ceiling of 1.8e308. The
problem is **cancellation**, not magnitude.

---

## 1. `D_x` must never be evaluated literally

`D_v = cosh(u) - sinh(u)*alpha` is correct algebra and unusable arithmetic. Audit over
200k real bridge samples, d=3:

```
D_literal == 0   -> 1/D^2 = inf   :  9.0965%
D_literal <  0   -> SILENT, finite:  2.4730%
alpha > 1 (rounding)              :  2.1465%
D_stable  <= 0                    :  0.0000%
```

Three distinct failure modes, and the third is the dangerous one:

1. **9.1% become `inf`.** Visible — this is what made `test_wnelbo_ref` come back `nan`.
2. **2.5% go negative.** `D >= e^{-u} > 0` is provable, so a negative value is pure noise.
   It survives `.square()` as a finite number, so nothing flags it.
3. **Silent bias.** Among the survivors, relative error vs the correct value is
   `median 1.0e-11` but `p99 1.6e+14`, `max 1.3e+17`. Dropping the infs and comparing the
   same subset: literal `1.2082e+15` vs correct `1.3608e+31` — **16 orders of magnitude,
   in the optimistic direction**, because the rounding noise of `cosh(u)` is vastly larger
   than the true `e^{-u}`, so `1/D^2` comes out far too small and the reported ELBO looks
   better than it is.

**Use the "Sharp Lower Bound" rearrangement** (slides/aug26_2026, and Invariant 5):

```
D = cosh(u) - sinh(u) alpha = e^{-u} + sinh(u)(1 - alpha) >= e^{-u} > 0
```

All terms positive, so no clamp is needed. Equivalently the half-angle split already used
in `HyperBridge.horosphere_geometry` and `bridge_loss_poincare_disk_polar`:
`D = sin_half_sq * e^{+u} + cos_half_sq * e^{-u}`.

### A clamp is NOT a fix

| form | non-finite | >1% error | >1e-6 error |
|---|---|---|---|
| `cosh - sinh*alpha` | 9.10% | 20.64% | 32.18% |
| `+ .clamp_min(exp(-u))` | 0.00% | 20.53% | 32.17% |
| `exp(-u) + sinh(u)*(1-alpha)` | 0.00% | 0.00% | 0.00% |

Clamping removes the `nan` and leaves 20% of samples wrong by more than 1%. And
`clamp_min(tiny)` is worse still: `1/tiny^2` overflows, so you get `inf` anyway. The only
defensible floor is `e^{-u}`, which *is* the stable form's leading term.

---

## 2. `1 - <x, theta>` is the same trap

Replacing `cosh - sinh*alpha` with `e^{-u} + sinh(u)*(1.0 - alphas)` fixes one cancellation
and reintroduces another at the same place. `<x,theta>` is a sum of O(1) products, so its
**absolute** error is ~eps no matter how close to 1 it is; subtracting from 1 keeps that
absolute error. `||x - theta||^2` sums squares of the differences, each accurate in its own
right, so it keeps full **relative** precision down to 1e-300.

Controlled test, `theta = (x + delta*w)/sqrt(1+delta^2)` with `w` unit and orthogonal to
`x`, so the exact `1-alpha = delta^2/(s(s+1))`, `s = sqrt(1+delta^2)`:

| delta | exact 1-alpha | `(x-theta).square().sum()/2` | `1 - <x,theta>` |
|---|---|---|---|
| 1e-2 | 4.999625e-05 | 3.0e-15 | 3.0e-12 |
| 1e-4 | 5.000000e-09 | 3.6e-13 | 2.1e-08 |
| 1e-6 | 5.000000e-13 | 6.3e-11 | **8.9e-05** |

On 200k real bridge samples (d=3):

```
1 - <x,theta> collapsed to exactly 0 : 10.1405%
1 - <x,theta> went negative          :  2.1465%
(x-theta).square().sum()/2 <= 0      :  0.0060%
resulting D_x rel.err                : >1% on 20.27%, max 2.1e+17
```

Since `1-alpha ~ ||delta||^2/2`, the breakdown hits at `||delta|| ~ 1.5e-8` — well inside
where the bridge concentrates. Note this failure does **not** produce `nan`
(`1-alpha = 0` gives `D = e^{-u}`, finite); it is purely the silent kind, biasing `1/D^2`
and the loss **too large** — the opposite direction from §1.

**Always form `1 - alpha` as `(x - theta).square().sum(-1) / 2`.** Same substitution as
`sin_half_sq` in `horosphere_geometry`.

### Corollary for ad-hoc scripts

`alph = theta @ emb.T` overflows 1 by rounding on **2.1%** of samples. A verification
script I wrote did exactly this, `D_v` went negative, and `log` returned `nan` across the
board. If you need `<theta, phi_v>`, take it from `cos_half_sq - sin_half_sq`.

---

## 3. float64 is not optional (Invariant 3)

Same cancellation-free formula, only the precision changed. float32 `eps = 1.2e-7 =
e^{-15.9}`, so `e^{-2u} < eps` at **u > 8.0**:

```
exp(u) overflows       (u > 88.7):  0.021% of samples
e^{-2u} < fp32 eps     (u >  8.0): 48.847%   <-- half the distribution
e^{-2u} < fp32 subnorm (u > 51.7):  0.777%
```

Result, d=3, 150k samples:

```
per-sample loss: non-finite 0.021%, median rel.err 8.9e-02, p99 3.9e+00
weighted ELBO   float64 = 2.262670
                float32 = 2.263153      H(p) = 2.241125
```

The weighted means agree to 0.02% only because the errors cancel in the average — **the
gradient is per-sample and does not get that cancellation**. And Invariant 2's criterion
(Bayes solution lands on `H(p)`, here 0.96% above) is an order of magnitude tighter than
float32's per-sample error, so the invariant would lose all discriminating power.

`RHO_MAX = 350` is a float64 constant. Under float32 it is not even representable through
`exp`.

**The line stays where Invariant 3 puts it:** `ts`, `rhos`, `thetas` and the whole
horosphere/loss computation in float64; only the trunk input and its logits cast to
float32. The geometry is an analytic quantity the loss differentiates and nothing
downstream corrects; the trunk is a learned approximation whose 1e-7 error is far below
its own training noise.

---

## 4. Picking a small `d` does not relax any of this

`1 - alpha ~ 2 e^{-2u}` is **independent of `d`** — `d` enters the Poisson kernel's
exponent `-(d-1)`, not the concentration scale. Measured medians:

| | u=5 | u=10 | u=20 |
|---|---|---|---|
| d=3 | 8.978e-05 | 4.158e-09 | 8.403e-18 |
| d=5 | 8.951e-05 | 4.121e-09 | 8.538e-18 |
| d=9 | 9.037e-05 | 4.092e-09 | 8.455e-18 |
| `e^{-2u}` | 4.540e-05 | 2.061e-09 | 4.248e-18 |

So the float64 requirement, `RHO_MAX = 350`, and the cancellation-free `D_v` are the same
whatever `prod_factor_dim` you choose.

### What `d = 3` does buy

The radial law has a closed form: `pi(rho) ∝ rho sinh(rho) e^{-rho^2/2t}`, equivalently
`rho (1 - e^{-2rho}) e^{-(rho-t)^2/2t}`. It is **not** a chi distribution — chi_d is only
the `t -> 0` limit (measured `rho/sqrt(t)` median for d=3: 1.5405 at t=1e-6 vs chi_3 median
1.5382, rising to 9.5883 at t=90). As `t -> inf` it becomes `N((d-1)t/2, t)`. Exact chi
holds only at `d = 1`, i.e. flat `H^1 = R`.

---

## 5. `RHO_MAX = 350` — two independent reasons

1. `cosh`/`sinh`/`exp(+u)` overflow float64 past `u ~ 710`.
2. The angular-only surrogate's `1/D^2 ~ e^{2u}` reaches `e^{700} ~ 1e304`, just inside the
   float64 ceiling of 1.80e308 (verified: `exp(700) = 1.01e304`). Past `u ~ 355` it
   leaves.

**It caps the DIMENSIONLESS `u = kappa*rho`, not `rho`.** Under curvature `K = -16`,
`kappa = 4`, so `rho = 350` means `u = 1400` and everything overflows. Every clamp site
must apply it after multiplying by `kappa` — see `bridge_loss_elbo_refactor`.

The current full path-KL no longer has the `1/D^2` weight (`||w_v|| == 1` bounds the
integrand by `2(d-1)^2 kappa^2`), so reason 2 applies only if the angular-only surrogate
is ever reinstated. Reason 1 stands regardless.

---

## 6. `_radial_t_max(d)` — who clamps `t` and who does not

`radial_cdf` builds the marginal `sinh^{d-1}(rho) p_H(rho;t)` in **linear** float64, which
overflows past `_radial_t_max(d)`, which falls off fast with `d` because the bound goes
like `700/(d-1)`:

| d | 2 | 3 | 5 | 9 | 16 |
|---|---|---|---|---|---|
| `_radial_t_max` | 394.6 | 97.0 | 23.6 | 5.6 | 1.5 |

| caller | clamps `t`? |
|---|---|
| `HyperBridge.bridge` | **yes** |
| `HyperBridge.sample_radial_tabulated` | yes (via the table's `t_max`) |
| `HyperbolicHeatKernel.sample_radial` (raw) | **no** — returns `nan` past it |
| `HyperbolicHeatKernel.poincare_bridge_prod` | **no** |

`main_refactor.py` therefore clamps `ts` itself (`self.max_heat_time`), using
`_radial_t_max(d_m) * R_m^2` per factor and taking the min — the bound is stated in
**unit** time, so a factor of radius `R` tolerates `R^2` times as much physical time. The
shipped `hyper_T` reaches `t = 1e5` against a limit of ~97, so without that clamp every
run is garbage.

**Caution:** any new call site that reaches `sample_radial` or `poincare_bridge_prod`
directly inherits the un-clamped behaviour.

---

## 7. Even `d` is ~1000x more expensive, and the cost is per-sample

`radial_cdf` for even `d` needs the McKean integral `_mckean_base`, a `(B, 2000, 1024)`
float64 quadrature (hence `_RADIAL_BCHUNK = 16`). Odd `d` has a closed-form base and needs
only `k = (d-1)/2` finite differences.

```
sample_radial d=2, B= 2048:  1.749 s   (1.749 s per 2048)
sample_radial d=2, B= 4096:  3.500 s   (1.750 s per 2048)
sample_radial d=2, B= 8192:  7.007 s   (1.752 s per 2048)
sample_radial d=3, B= 2048:  0.0014 s
```

**Perfectly linear in B** — the cost is real per-sample work (each of the B samples has its
own `t`, so it builds B separate CDFs), not launch overhead. Consequences:

- **`torch.vmap` over the factor axis buys nothing.** Merging M factor calls into one is
  break-even by the table above. It is also not expressible: `d` is a python int selecting
  the odd/even branch and the recursion depth, not a tensor axis.
- **A padded `(N, M, d_max)` layout buys nothing either.** It vectorises the angular side
  (already ~2% of the cost) and leaves the radial side untouched — different `d_i` are
  genuinely different distributions and different code paths.
- **The fix is the tabulated quantile**, already in `loss.py`
  (`_radial_quantile_table` / `sample_radial_tabulated`): `1.749 s -> 0.0003 s`, **6162x**.
  It works because the radial law depends only on `(t, d)` and curvature is a pure
  rescaling `rho = R * rho_1(t/R^2)`, so one table per `d` serves all curvatures.

`poincare_bridge_prod` does **not** use the table, so `main_refactor.py` at `hyper_dim=2`
pays ~5.5 s/step (~30 h for 20k steps) where `main.py` does not. `hyper_dim=3` is ~5.9 ms.

### Tabulating odd `d` too: measurable, not worth it

| d | quadrature | table | speedup | build | table size |
|---|---|---|---|---|---|
| 3 | 1.465 ms | 0.245 ms | 6.0x | 0.01 s | 56.1 MiB |
| 5 | 2.374 ms | 0.236 ms | 10.1x | 0.01 s | 53.6 MiB |
| 9 | 3.129 ms | 0.236 ms | 13.3x | 0.01 s | 51.1 MiB |
| 15 | 4.383 ms | 0.237 ms | 18.5x | 0.01 s | 49.1 MiB |

At d=3 the radial sampler is 83% of the bridge and ~50% of a 5.9 ms training step, so the
table would give ~1.7x end-to-end — **48 seconds over a 20k-step run**, in exchange for a
resident 56 MiB and an extra interpolation layer. Accuracy against the analytic d=3 law is
essentially identical (quadrature 1.77e-3 / 1.73e-3 / 1.40e-3 / 5.98e-4 at t = 0.05 / 1 /
5 / 50; table 1.77e-3 / 1.75e-3 / 1.44e-3 / 6.38e-4). Only worth doing for code uniformity.

---

## 8. `exact_d3` — exact, unbounded in `t`, and slower at our batch size

`sample_radial(..., exact_d3=True)` inverts the closed-form CDF

```
F(rho) = Phi(a) - Phi(-b) + (phi(b) - phi(a)) / sqrt(t),
a = (rho - t)/sqrt(t),  b = (rho + t)/sqrt(t)
```

by 48 bisections on `[0, t + 14 sqrt(t)]`. Use `Phi(a) - Phi(-b)`, not the algebraically
equal `Phi(b) - Phi(-a)`: `-b < a` always, so the subtracted term is the small one.

Validated deterministically against a 4M-point integral of the density, `max |F_closed -
F_numeric| = 2.7e-6` flat over `t` in `[1e-6, 1e4]` (that residual is the trapezoid's own
error). `F(samples)` is uniform to 1-2e-3 against a KS scale of 2.2e-3 at N=400k.

**It is the more accurate of the two** (both vs the analytic law):

| t | exact_d3 | grid |
|---|---|---|
| 1e-2 | 9.6e-04 | 2.4e-03 |
| 1 | 3.6e-03 | 5.3e-03 |
| 10 | 6.5e-04 | 4.4e-03 |

**No `_radial_t_max` ceiling**: `mean/t` = 1.0016 / 1.0003 / 1.00001 at t = 500 / 5000 /
1e6, where the grid path returns non-finite.

**But it is flat in B and the grid path is linear**, so at our batch size it loses:

| B | exact_d3 | grid | ratio |
|---|---|---|---|
| 2048 | 7.03 ms | 1.41 ms | **5.0x slower** |
| 32768 | 7.02 ms | 35.7 ms | 0.20x |
| 262144 | 6.92 ms | 285 ms | 0.02x |

Crossover ~B=8k. Off by default is right. Not currently reachable from `main_refactor.py`
(`poincare_bridge_prod` does not take the flag). If the 5x matters, replacing the tail of
the bisection with 3 Newton steps (density `(rho/t^{3/2}) phi(a) (1 - e^{-2rho})`,
cancellation-free) should reach ~2 ms.

---

## 9. Square the ratio, not the numerator and denominator separately

Where a `1/D` weight appears, compute `(||num|| / D)` first and square that.
`||num||^2 / D^2` overflows at reachable radii while `(||num||/D)^2` does not: `||num||`
is bounded by 2 while `D` reaches `e^{-350}`, so the intermediate `D^2 = 1e-304` underflows
where the ratio does not.

---

## 10. Applying curvature twice

`HyperbolicModelBase.horosphere_geometry` takes the **intrinsic** `rho` and forms
`ss = radius / _curvature_scale(K)` itself. Feeding it a pre-scaled `u = kappa*rho`
double-applies `kappa` and is **invisible at `K = -1`** (kappa = 1). Measured
`test_wnelbo_ref` for the Bayes-optimal model, `H(naive_ps) = 0.5003`:

| K | double-scaled | correct |
|---|---|---|
| -1 | 0.500761 | 0.500761 |
| -16 | 1.061358 | **0.500761** |
| -0.25 | 0.795903 | **0.500761** |
| product `[3,3]`, `[-1,-0.25]` | 0.535781 | **0.504522** |

**Convention: `radius` means the intrinsic `rho` at every public boundary.** The
dimensionless `u` is formed inside — in `forward_naive` for the trunk (so the predictor is
scale-equivariant) and in `bridge_loss_elbo_refactor` / `horosphere_geometry` for the
geometry. Anything that pre-scales at a call site will be silently wrong on every run at
`K = -1`, which is the default.

---

## 11. `_std_from_sums` in `trainer.py`

```python
(max(sq_total - total * total / count, 0.0) / (count - 1)) ** 0.5
```

Correct — the standard sum-of-squares identity for the unbiased sample variance, matching
`torch.std`'s default `correction=1` (agrees to 6.3e-16 / 3.9e-16 / 0.0 on uniform,
wloss-like and lognormal data). It exists because Lightning's `on_epoch=True` averages
**per-batch** stds, which on heavy-tailed integrands underestimates badly — measured
**80.9% low** on 1000 lognormal^3 batches, against a pooled estimate that reproduces the
two-pass answer exactly.

**But it is the textbook catastrophic-cancellation formula**; the `max(..., 0.0)` exists
only to stop a negative radicand becoming `nan`. It fails when `variance << mean^2`:

| mean (sigma = 1e-3) | pooled | two-pass | rel.err |
|---|---|---|---|
| 1 | 1.00220470e-03 | 1.00220470e-03 | 7.7e-11 |
| 1e3 | 1.00095060e-03 | 1.00095712e-03 | 6.5e-06 |
| 1e6 | **0.0** (clamp fired) | 1.00403036e-03 | 1.00 |
| 1e9 | **12.95** | 1.00339646e-03 | 1.3e+04 |

We are safely in the opposite regime — `var/mean^2` is 24.2 (`wloss`), 74.5
(`wnelbo_ref`), 27.4 (`wce_ref`) — so there is nothing to cancel. **Caution if a future
metric has a large mean and small spread** (an accuracy, a probability, a normalised
score): it will return 0 or garbage without warning. Welford would remove the hazard at the
cost of carrying a running mean in `_std_accum`.

---

## 12. Memory

Both radial paths materialise large intermediates and OOM'd twice during this session:

- `radial_cdf`: `(B, 2000)` float64 per tensor, several live at once. `B = 400k` tried to
  allocate 5.96 GiB per tensor and died on a 48 GB card.
- `_mckean_base`: `(B, 2000, 1024)`, chunked at `_RADIAL_BCHUNK = 16`.

Keep verification scripts at `B <= 150k` for odd `d`, less for even. Also: `torch.tensor(
python_list)` builds a **CPU float32** tensor — against CUDA float64 state that is a device
error, and where it silently promotes it costs precision. Use `x.new_tensor(...)`.

---

## Appendix: adjacent (non-numerical) cautions found alongside

1. **`test_wnelbo_ref` is only comparable to `H(p)` for the FULL path-KL.** The slides'
   angular-only, shared-`D_x` surrogate omits the radial drift term and sits **below** the
   entropy, so it cannot be an ELBO on the NLL. Measured at the Bayes optimum:
   full `2.251384` = radial `0.672263` + angular `1.579121`; shared-`D_x` `1.522009`;
   `H(p) = 2.241125`. So `full/H = 1.0046` (tight) and `angular/H = 0.6791`.
   The radial term is nonzero because `E[A_t | rho] = 0` (which is why the radial marginal
   is target-independent and the bridge factorises) does **not** imply `E[A_t^2] = 0` — and
   the KL rate is a mean square. Measured `E[A_y] = -2.8e-02`, `E[A_y^2] = 3.5e-01`.

2. **`forward_type: naive` changes what the loss means.** The `*_refactor` losses take
   `logits` as the complete log-posterior. Under `naive` the model returns the residual, so
   `mode=opt` emits the plain prior and stops being Bayes-optimal:
   `test_wnelbo_ref` 0.500761 (horosphere) vs **14.93** (naive).

3. **`run_name` collides for every product-manifold config.** It interpolates
   `${hyper_dim}` and `${gaussian_curvature}`, both ignored when `prod_factor_dim` is set,
   so `[3,3] K=[-1,-0.25]` and `[2,4] K=[-1,-1]` produce the identical folder. With
   `TaskMgr.check_finished()` the second run of a sweep is silently **skipped**.

4. **`GeoUtils._curvature_scale`'s list and tensor branches skip the `K != 0` check** the
   scalar branch has. `prod_factors` validates `K < 0` upstream, so nothing reaches it
   today.
