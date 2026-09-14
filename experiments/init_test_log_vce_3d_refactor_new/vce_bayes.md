# Why the ELBO's optimum is the Bayes posterior, and why the variational CE's is not

Companion note to `RESULTS.md`. Part 1 derives where the Bayes posterior enters the
ELBO — it is nowhere in the formula, it is the *argmin*. Part 2 shows exactly which step
of the variational-CE derivation loses it, and what the resulting optimum is instead.

---

## 0. Setup and notation

The generative process (sequence length 1, so one token per example):

| symbol | meaning | in code |
|---|---|---|
| `y ~ p` | target word, `V` of them | `targets`, `ps` |
| `φ_v ∈ S^{d−1}` | word `v`'s boundary direction (unit) | `lm_head.weight` rows, per factor |
| `z_t = (ρ, θ)` | bridge state at heat time `t` | `rhos`, `thetas` |
| `u_m = κ_m ρ_m` | dimensionless radius, `κ_m = √(−K_m)` | `us` |
| `D_v = cosh u − sinh u ⟨φ_v, θ⟩` | Busemann denominator, `= e^{B_v(z)}` | `denoms` |
| `w_v` | `φ_v` transported into the tangent frame at `z`, `‖w_v‖ = 1` | `ws` |
| `p_θ(·|z_t)` | the model's posterior over words | `softmax(logits)` |

Product manifold `H^{d_1}_{K_1} × … × H^{d_M}_{K_M}`; the factors are independent Brownian
motions, so their contributions add. For a single factor (`M = 1`) I drop the `m` index.

Two facts read straight off the code, used throughout:

**(F1) The horosphere readout is the Bayes posterior.** `model.py:327` —
`horosphere_dists[…,v] = Σ_m −(d_m−1) B^m_v(z_m)`, so with `B_v = log D_v`,

```
q(y | z_t)  =  softmax(horosphere_dists + log p)_y  ∝  p_y · Π_m D_{v=y,m}^{−(d_m−1)}
```

This is exactly `OptimalModelRefactor`. The `(d−1)` exponent is the hyperbolic Poisson
kernel's.

**(F2) The bridge drift toward word `v` is `(d_m−1) κ_m w_v^{(m)}`** (`loss.py:126`).

---

## Part 1 — ELBO ⟹ Bayes posterior

### 1.1 The floor is `H(p)`

For any variational bound, `−log p_θ(y) ≤ NELBO_θ(y)`. Take `E_{y∼p}`:

```
H(p)  =  E_p[−log p(y)]  ≤  E_p[−log p_θ(y)]  ≤  E_p[NELBO_θ(y)]
         └ true NLL ┘        └ Gibbs ┘            └ variational gap ┘
```

So `NELBO ≥ H(p)`, with equality iff **both** the model's marginal equals `p` **and** the
variational gap closes. This is Invariant 2, and it is why "tight to the dataset entropy"
and "learned the Bayes posterior" are the same statement.

### 1.2 Girsanov: the KL you can see

Two diffusions differing only in drift have path-KL

```
KL(Q^y ‖ P_θ)  =  E ∫₀^T ½ ‖ b^y(z_t,t) − b_θ(z_t,t) ‖² dt
```

with, by (F2),

```
b^y  = (d−1)κ · w_y(z_t)                 ← true drift; conditioned on y
b_θ  = (d−1)κ · Σ_v p_θ,v(z_t) · w_v(z_t)   ← model drift; a function of z_t only
```

Their difference is `(d−1)κ Σ_v μ_v w_v` with `μ = p_θ − δ_y`, which is precisely
`loss.py:128–131`:

```
(d−1)² κ² / 2 · ‖ Σ_v μ_v w_v ‖²,     μ_v = p_θ(v) − δ_{v,y}
```

**At this point there is no Bayes posterior anywhere.** Only a squared drift mismatch.

### 1.3 Change of measure — this is where it appears

The objective samples `y` first, then `z_t`:

```
L(θ)  =  E_{y∼p} E_{z_t|y} [ ½‖b^y(z_t) − b_θ(z_t)‖² ]
```

But `b_θ` depends only on `z_t`, so to optimize it we must put `z_t` on the outside.
Refactor the joint the other way — this step *is* Bayes' rule:

```
p(y) · q(z_t | y)  =  q(z_t) · q(y | z_t)
```

```
L(θ)  =  E_{z_t} E_{y ∼ q(y|z_t)} [ ½‖b^y(z_t) − b_θ(z_t)‖² ]
                      └──────┬──────┘
                      the Bayes posterior
```

`q(y|z_t)` is not imposed by the objective; it falls out of writing the same expectation in
the order "draw `z_t`, then draw `y`". Nothing has been approximated — this is an identity.

### 1.4 The inner problem is least squares, so its argmin is a conditional expectation

Fix `z_t`. Now `b_θ(z_t)` is a single vector, constant in `y`. Bias–variance:

```
E_{y|z} ‖b^y − b_θ‖²  =  ‖ b_θ − E_{y|z}[b^y] ‖²  +  Var_{y|z}(b^y)
                          └── reducible, sees θ ──┘   └─ irreducible, θ-free ─┘
```

- The second term does not involve `θ`. **This is why the ELBO bottoms out at `H(p)` rather
  than at 0.**
- The first vanishes iff `b_θ(z_t) = E_{y|z_t}[b^y] = Σ_y q(y|z_t) b^y(z_t)`.

This is the same theorem as "the optimal denoiser is `E[x₀ | x_t]`": the minimizer of a
squared error is the conditional expectation, and the conditioning law is the Bayes
posterior.

### 1.5 Back to the parameterization

```
b_θ = (d−1)κ Σ_v p_v w_v        E_{y|z}[b^y] = (d−1)κ Σ_v q_v w_v
```

Equality holds iff `Σ_v p_v w_v = Σ_v q_v w_v`, i.e. **`p = q`** whenever `{w_v}` are
affinely independent. Since the model's `p_θ` is a free softmax over `V` words, the optimum
is attainable, and the ELBO's minimizer is the Bayes posterior. ∎

### 1.6 What the time proposal does — and does not — do

`t` is drawn from a proposal `π(t)` and each sample reweighted by `1/π(t)`. That weight is
**positive and independent of `y`**, so it rescales the inner objective at each `z_t`
without moving its argmin. It changes the *variance* of the estimator, never the optimum.

This is exactly why switching `exp → stratified_exp` moved nothing (`RESULTS.md` §2): it
is a variance intervention against a bias.

---

## Part 2 — The variational CE, and what it actually optimizes

### 2.1 The approximation chain

Start from the exact ELBO integrand of §1.2 and split `w_v = [r_v θ + P_θ^⊥ φ_v] / D_v`,
with `r_v = cos²(a_v/2)e^{−u} − sin²(a_v/2)e^{+u}` (`loss.py`, `radial_parts`/`denoms`).

**Step A (approximation).** Drop the radial component and replace every word's `D_v` by the
*target's* `D_x`, `x := φ_y`. Writing `x̂ = Σ_v p_v φ_v`:

```
Σ_v μ_v w_v   ≈   (1/D_x) · P_θ( x̂ − x )
```

giving the *shared-`D_x` angular surrogate*

```
(d−1)² κ² / (2 D_x²) · ‖ P_θ(x − x̂) ‖²
```

**Step B (bound).** With `x − x̂ = Eᵀ(δ_y − p)` and unit rows, `‖Eᵀa‖₂ ≤ ‖a‖₁`; `P_θ` is an
orthogonal projector; then Pinsker:

```
‖P_θ(x − x̂)‖²  ≤  ‖δ_y − p‖₁²  ≤  2 KL(δ_y ‖ p)  =  2 CE(y, p)
```

Summing the independent factors, `CE` is `m`-free and factors out:

```
VCE(y, p; z_t)  =  CE(y, p) · Σ_m (d_m−1)² κ_m² / D_{x,m}²   =:  CE(y, p) · w(z_t, y)
```

**Only Step A is harmful.** Step B is loose in value but, as §1.4 shows, a `y`-free
multiplier cannot move an argmin. Step A is what makes the multiplier `y`-dependent, by
pulling the target's `D_x` out of the norm.

### 2.2 Exact statement: weighted CE is a proper scoring rule for the *tilted* law

Fix `z_t` and write `q_y = q(y|z_t)`, `w_y = w(z_t, y)`. The conditional objective is

```
L(p)  =  Σ_y q_y w_y ( −log p_y ),        Σ_y p_y = 1
```

Define

```
Z  :=  Σ_y q_y w_y  =  E_q[w]        (positive, y-free)
ν_y :=  q_y w_y / Z                  (the tilted posterior)
```

Then, by direct substitution,

```
L(p)  =  −Σ_y Z ν_y log p_y  =  Z · ( H(ν) + KL(ν ‖ p) )                      (★)
```

So `L` is, up to the positive factor `Z(z_t)`, the cross-entropy **of `ν` against `p`**.
Consequences, all exact:

1. **The unique minimizer is `p* = ν ∝ q · w`**, not `q`. (Matches the Lagrange
   computation: `∂/∂p_y[−Σ q_y w_y log p_y + λΣp_y] = 0 ⟹ p_y ∝ q_y w_y`.)
2. **The objective's preference for the tilt over the truth is exactly**

   ```
   L(q) − L(ν)  =  Z · KL(ν ‖ q)  ≥  0
   ```

   with equality iff `w` is `q`-a.s. constant in `y`. So "the weight depends on the target"
   and "the truth is not optimal" are the *same* condition, and `Z·KL(ν‖q)` measures the
   damage.
3. Weighted CE is a proper scoring rule — just for `ν`. It is proper for `q` iff `w ⟂ y`.

### 2.3 Identifying the tilt: `ν` is the Bayes posterior of dimension `d + 2`

For a single factor, combine (F1) with the weight's `D^{-2}`:

```
q_y ∝ p_y · D_y^{−(d−1)}          w_y ∝ D_y^{−2}
ν_y ∝ q_y w_y ∝ p_y · D_y^{−(d+1)}
```

A Bayes posterior in dimension `d'` carries exponent `−(d'−1)`. Setting `d'−1 = d+1`:

```
d' = d + 2
```

**The variational CE's optimum is the exact Bayes posterior of the same problem in two more
dimensions** — a sharper Poisson kernel, hence a systematically over-confident posterior.
Over-confidence raises the expected CE under the true law, so the reference ELBO sits above
`H(p)`. (For `M > 1` the weight is a *sum* over factors rather than a product, so this clean
identity is exact only at `M = 1` — which is the `H^3` case measured here.)

### 2.4 What was measured

`naive_ps`, `K = −1`, `d = 3`, 50 000 draws (`diag_vce_minimizer.py`; `RESULTS.md` §3):

| posterior handed to the loss | `VCE` | reference ELBO |
|---|---|---|
| Bayes `q` | 0.644 | 0.507 ( `H(p)` = 0.5003 ) |
| tilted `ν ∝ q·w` | **0.318** | **0.828** |

The tilt scores the objective 2.07× *better* while denoising *worse* — the empirical form of
(★) and of `L(q) − L(ν) = Z·KL(ν‖q) > 0`. `log w` spans 40.7 nats across words at rate 0.1
and 124.8 at rate 0.01. Trained models landed at 0.73–0.76, between `q` (0.507) and `ν`
(0.828), i.e. partially converged toward `ν`.

### 2.5 The fix, and why it is the minimal one

Any `y`-free weight restores the argmin, because in (★) a `y`-free `w` makes `ν = q`. It
must still dominate the target's term to keep Step B a bound. Two candidates:

| weight | valid bound | `y`-free | usable |
|---|---|---|---|
| `e^{2u}` (since `D_x ≥ e^{−u}`) | ✓ | ✓ | ✗ — log-weights reach 212; the sample mean is dominated by single draws |
| **`min_v D_v` in place of `D_x`** | ✓ (termwise per factor) | ✓ | ✓ — costs 0.1015 nats, identical to `w` on 92.5% of draws |

The second is `LossGeometry.VAR_CROSS_ENTROPY_TF`. It is minimal in a precise sense: Step A
collapsed `{D_v}_v` onto one representative, and the defect was only that the representative
was chosen *by the target*. Choosing it by `min_v` instead keeps the collapse, keeps the
bound direction (`min_v D_v ≤ D_x ⟹ weight only grows`), and removes the `y` dependence.

Measured (20 000 steps, 4M-sample test, `naive_ps`, `K = −1`, seed 0):

| loss proposal | `var_cross_entropy` | `var_cross_entropy_tf` | `H(p)` |
|---|---|---|---|
| stratified_exp 0.05 | 0.7002 | **0.5084** | 0.5003 |
| stratified_exp 0.1 | 0.7505 | **0.5042** | 0.5003 |
| stratified_exp 0.25 | 0.7602 | **0.5039** | 0.5003 |

---

## Summary

| | minimizer | why |
|---|---|---|
| ELBO (`poincare_polar`) | `q` — Bayes posterior | squared drift error; argmin of `‖·‖²` is the conditional expectation under `q` (§1.4) |
| plain CE (`cross_entropy`) | `q` | proper scoring rule |
| VCE (`var_cross_entropy`) | `ν ∝ q·w` = Bayes posterior at `d+2` | weight is target-indexed; (★) makes it proper for `ν`, not `q` |
| VCE-TF (`var_cross_entropy_tf`) | `q` | weight is a function of `z_t` alone, so `ν = q` |

The time proposal `π(t)` and its `1/π(t)` weight are `y`-free throughout, so they affect
only estimator variance — never which posterior is optimal.
