---
marp: true
theme: default
paginate: true
# _class: invert
# color: white
size: 4:3
class: lead
style: |
  section.lead h1 {
    text-align: center;
  },
  section.lead h2 {
    text-align: center;
  },
  section.lead h3 {
    text-align: center;
  },
  h1 {
    color: #3d3d3d;
  },
  h2 {
    color: #3d3d3d;
  },
  h3 {
    color: #3d3d3d;
  },
  r {
      color: red;
  },
  y {
      color: yellow;
  },
  b {
      color: blue;
  },
  .g {
      color: green;
  }
---

<style>
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
ng { color: #0072B2; }
rd { color: #D55E00; }
uv { color: #008060; }
hy { color: #7B3FA0; }
table {
  font-size: 0.58em;
  margin: 0.2em auto;
  max-width: 100%;
}
th, td {
  padding: 1px 4px;
  line-height: 1.05;
}
</style>

# Hyperbolic DLM

#### Aug 26, 2026

---

- Normalized word embeddings concentrate on a pole

![alt text](image-4.png)

---

## GenPPL - Entropy Frontier Lines

- Same settings and temperature config as S-FLM paper

![alt text](image-5.png)

---

$$
\mathbb{E}_{x \sim q} \left[ \nabla_{x}\log q_t(z | x) \right]
$$

---

### IS on Sphere (Angles)

Let $\mathbf{\bar{E}} \in \mathbb{R}^{V} \times \mathbb{S}^{d-1}$ is a normalized word embedding matrix with $V$ word and normalized $d$ dimension. $\mathbf{e}_x \in \mathbb{S}^{d-1}$ is the $x$-th row of the $\mathbf{\bar{E}}$.

$z_t \in \mathbb{R}^d$ is an intermediate state at timestep $t$, the forward process is $q_t(z | x) := \mathcal{N}(z; t \mathbf{e}_x, (1 - t)^2 \mathbf{I})$. 

The EFLM loss is

$$
\mathbb{E}_{z_t \sim q_t(\cdot | x)}\left[ \text{CE}(\mathbf{Y}_x  \| \hat{X}_{\Theta}(z_t, t)) \right]
$$

$\mathbf{Y}_x$ is the one-hot encoding of word $x$.

---

### IS on Sphere (Angles)

To do IS on angular space, we can do 

$$
\mathbb{E}_{z_t \sim \bar{q}_t(\cdot | x)}\left[ \frac{q_t(z_t | x)}{\bar{q}_t(z_t | x)} \text{CE}(\mathbf{Y}_x  \| \hat{X}_{\Theta}(z_t, t)) \right]
$$

where $\bar{q}_t(z | x) := \mathcal{N}(z; t \mathbf{e}_x, (1 - t)^2 \frac{\mathbf{\bar{E}}^{\top} \mathbf{\bar{E}}}{Z})$, where $Z$ is a hyperparameter.

---

### Experiment

See if the variance reduces as we use proposal $\bar{q}_t(z | x)$

---

### Pre-conditioned (Adaptive) Angular Steps



---

# Spherical Cauchy Diffusion

---

## Poincare disk Brownian Bridge

Consider sectional curvature $K<0$, let $\kappa:=\sqrt{-K}$, and use $g_K=\kappa^{-2}g_{-1}$ on the unit ball. Recall the Poincare disk brownian bridge

$$
\begin{aligned}
dz_t & = \kappa^2 \left( \frac{d-1}{2} \frac{(1-\|z_t\|^2)^2}{\|x - z_t\|^2} (x - z_t) - \frac{d}{4} (1 - \|z_t\|^2) z_t \right) dt + \kappa\frac{1-\|z_t\|^2}{2} d\bar{W}_t \\
\end{aligned}
$$

$x$ is a target on the boundary and $z_t$ is an intermediate state at timestep $t$

---

## Poincare disk Brownian Bridge in Polar

Denote the $z_t = r_{z_t} \theta_{z_t}$ in polar coordinate $(r_{z_t}, \theta_{z_t})$

$$
\begin{aligned}
z
&=
r_z\theta_z,
&
r_z
&:=
\|z\|
=
\tanh\left(\frac{\kappa\rho_z}{2}\right),
&
\theta_z
&:=
\frac{z}{\|z\|}
\in
\mathbb S^{d-1}.
\end{aligned}
$$

For the polar SDE, define
$$
\alpha_t=\langle x,\theta_{z_t}\rangle,
\qquad
D_t
=
\cosh(\kappa\rho_{z_t})
-
\sinh(\kappa\rho_{z_t})\alpha_t,
$$
and
$$
A_t
:=
\frac{
\cosh(\kappa\rho_{z_t})\alpha_t
-
\sinh(\kappa\rho_{z_t})
}{
D_t
}.
$$

---

## Poincare disk Brownian Bridge in Polar

The disk Brownian bridge can be expressed as the dynamic over radial $d \rho_{z_t}$ and angle $d \theta_{z_t}$

$$
\boxed{
\begin{aligned}
d\rho_{z_t}
&=
dB_t^\rho
+
(d-1)\kappa
\left[
\frac12\coth(\kappa\rho_{z_t})
+
A_t
\right]dt,
\\
d\theta_{z_t}
&=
\frac{\kappa}{\sinh(\kappa\rho_{z_t})}
(I_d-\theta_{z_t}\theta_{z_t}^\top)\,dW_t^{\mathbb S}
\\
&\quad+
\left[
\frac{(d-1)\kappa^2}{\sinh(\kappa\rho_{z_t})D_t}
(x-\alpha_t\theta_{z_t})
-
\frac{(d-1)\kappa^2}{2\sinh^2(\kappa\rho_{z_t})}\theta_{z_t}
\right]dt.
\end{aligned}
}
$$

---

## Radius-as-time spherical Cauchy Posterior

Treats $R$ as an artificial time variable and requires

$$
\theta_{z_R}\sim q_R(\cdot\mid x),
\qquad
z_R=r_{z_R}\theta_{z_R},
\qquad
r_{z_R}=\tanh\left(\frac{\kappa R}{2}\right).
$$

The posterior at radial $\rho = R$ is a hyperbolic Poisson kernel

$$
\boxed{
\begin{aligned}
q_R(\theta_z\mid x) 
& :=
q(\theta_{z_t}=\theta_z\mid \rho_{z_t}=R,Y_\infty=x)
\\
& =
\left(
\frac{1 - \| z_R \|^2}
{\| x - z_{R} \|^2}
\right)^{d-1} \\
& =
\left(
\frac{1-r_{z_R}^2}
{1+r_{z_R}^2-2r_{z_R}\langle x,\theta_z\rangle}
\right)^{d-1} \\
\end{aligned}
}
$$

---

## Radius-as-time spherical Cauchy Probability Flow

The time-homogeneous probability-flow ODE is
$$
\boxed{
\frac{d\theta_{z_R}}{dR}
=
v_x(\theta_{z_R})
:=
\kappa(I_d-\theta_{z_R}\theta_{z_R}^\top)x,
\qquad
\theta_{z_0}\sim\operatorname{Uniform}(\mathbb S^{d-1}).
}
$$

---

## Radius-as-time spherical Cauchy Score

The score and score-corrected drift are
$$
\begin{aligned}
D_x^{(\kappa)}(R,\theta_z)
&:=
\cosh(\kappa R)-\sinh(\kappa R) \langle x,\theta_z \rangle, \\
% &= \frac{e^{\kappa R} + e^{-\kappa R}}{2} - \frac{e^{\kappa R} - e^{-\kappa R}}{2} \langle x,\theta_z \rangle \\
% &= \frac{e^{\kappa R}}{2} (1 - \langle x,\theta_z \rangle) + \frac{e^{- \kappa R}}{2} (1 + \langle x,\theta_z \rangle) \\
\\
s_x(\theta_z,R)
&:=
\nabla_{\mathbb S^{d-1}}\log q_R(\theta_z\mid x)
\\
&=
(d-1)
\frac{\sinh(\kappa R)}{D_x^{(\kappa)}(R,\theta_z)}
(I_d-\theta_z\theta_z^\top)x,
\\
b_x(\theta_z,R)
&:=
v_x(\theta_z)
+
\frac{g(R)^2}{2}s_x(\theta_z,R).
\end{aligned}
$$

The Fokker–Planck equation reduces to the continuity equation:
$$
-\operatorname{div}_{\mathbb S}(q_R b_x)
+\frac{g(R)^2}{2}\Delta_{\mathbb S}q_R
=
-\operatorname{div}_{\mathbb S}(q_R v_x).
$$

---

## Sharp Lower Bound for $D_x^{(\kappa)}(R,\theta_z)$ at Fixed $R$

Because $x,\theta_z\in\mathbb S^{d-1}$, Cauchy–Schwarz gives
$\langle x,\theta_z\rangle\le 1$. For $R\ge0$,

$$
\begin{aligned}
D_x^{(\kappa)}(R,\theta_z)
&=
\cosh(\kappa R)
-\sinh(\kappa R)\langle x,\theta_z\rangle
\\
&=
\frac{e^{\kappa R} + e^{-\kappa R}}{2}
- \frac{e^{\kappa R} - e^{-\kappa R}}{2} \langle x,\theta_z\rangle
\\
&=
e^{-\kappa R}
+\sinh(\kappa R)
\bigl(1-\langle x,\theta_z\rangle\bigr)
\\
&\ge e^{-\kappa R}.
\end{aligned}
$$

Therefore the largest uniform lower bound is
$$
\boxed{
\inf_{\theta_z\in\mathbb S^{d-1}}
D_x^{(\kappa)}(R,\theta_z)
=e^{-\kappa R}.
}
$$

---

## Radius-as-time Spherical Cauchy SDE in Ambient Coordinates

In ambient Itô coordinates, this is
$$
\boxed{
d\theta_{z_R}
=
\left[
b_x(\theta_{z_R},R)
-
\frac{d-1}{2}g(R)^2\theta_{z_R}
\right]dR
+
g(R)(I_d-\theta_{z_R}\theta_{z_R}^\top)dW_R.
}
$$

---

## Radius-as-time Spherical Cauchy ELBO

Continuous-time path-KL term is
$$
\boxed{
\mathcal L_{\mathrm{SC}}(\theta)
=
\frac12
\mathbb E_{x\sim p_{\mathrm{data}}}
\left[
\int_0^{R_{\max}}
\mathbb E_{\theta_{z_R}\sim q_R(\cdot\mid x)}
\left[
\frac{
\|b_x(\theta_{z_R},R)-b_\theta(\theta_{z_R},R)\|^2
}{
g(R)^2
}
\right]dR
\right].
}
$$

---

## Continuous time Poincare Disk Brownian Bridge ELBO

Assume the true and learned bridges share the initial law and the noise. The physical diffusion $g_{\mathrm{PD}}(R)$, target drift $b_x^{\mathrm{PD}}$, and learned drift $b_\theta^{\mathrm{PD}}$ are

$$
g_{\mathrm{PD}}(R) = \frac{\kappa}{\sinh(\kappa R)},
\qquad
b_x^{\mathrm{PD}}(\theta_{z_R},R)
=
\frac{(d-1) \kappa^2}{\sinh(\kappa R) D_x^{(\kappa)}(R,\theta_{z_R})}
(I_d - \theta_{z_R} \theta_{z_R}^\top) x
$$

$$
b_{\theta}^{\mathrm{PD}}(\theta_{z_R},R)
=
\frac{(d-1) \kappa^2}{\sinh(\kappa R) D_x^{(\kappa)}(R,\theta_{z_R})}
(I_d - \theta_{z_R} \theta_{z_R}^\top) \widehat x_\theta(\theta_{z_R}, \kappa R),
\qquad
\widehat x_\theta(\theta_{z_R}, \kappa R) \approx x.
$$

---

## Continuous time Poincare Disk Brownian Bridge ELBO

Conditioning the physical-time path-KL on the radius $R_t=R$ gives
$$
\boxed{
\begin{aligned}
\mathcal L_{\mathrm{PD}}(\theta)
&=
\frac12
\mathbb E_{x\sim p_{\mathrm{data}}}
\left[
\int_0^T\int_0^{R_{\max}}
p_t^{\mathrm{rad},\kappa}(R)
\mathbb E_{\theta_{z_R}\sim q_R^{(\kappa)}(\cdot\mid x)}
\left[
\frac{
\|b_x^{\mathrm{PD}}(\theta_{z_R},R)-b_\theta^{\mathrm{PD}}(\theta_{z_R},R)\|^2
}{
g_{\mathrm{PD}}(R)^2
}
\right]dR\,dt
\right].
\end{aligned}
}
$$

- In physical coordinates, $p_t^{\mathrm{rad},\kappa}$, $q_R^{(\kappa)}$, and the normalized drift error all depend on $\kappa$.
- Taking $R_{\max}=\infty$ and $T=\infty$ gives the full angular path-KL (add the radial term for the total).

---

## Curvature Enters the Conditional KL Rate

Writing $P_{\theta_{z_R}} = I_d - \theta_{z_R} \theta_{z_R}^\top$,
$$
\begin{aligned}
\frac{\| b_x^{\mathrm{PD}}(\theta_{z_R},R) - b_\theta^{\mathrm{PD}}(\theta_{z_R},R) \|^2}
{g_{\mathrm{PD}}(R)^2}
& =
\frac{(d-1)^2\kappa^4}{\sinh(\kappa R)^2D_x^{(\kappa)}(R,\theta_{z_R})^2g_{\mathrm{PD}}(R)^2}
\left\|P_{\theta_{z_R}}\!\left(x-\widehat x_\theta(\theta_{z_R},\kappa R)\right)\right\|^2 \\
& =
\frac{(d-1)^2\kappa^2}{D_x^{(\kappa)}(R,\theta_{z_R})^2}
\left\|P_{\theta_{z_R}}\!\left(x-\widehat x_\theta(\theta_{z_R},\kappa R)\right)\right\|^2 .
\end{aligned}
$$

---

# Decompose Radius and Angles

$$
\begin{aligned}
\mathcal L_{\mathrm{PD}}(\theta)
&=
\frac12
\mathbb E_{x\sim p_{\mathrm{data}}}
\left[
    \int_0^T\int_0^{R_{\max}}
    p_t^{\mathrm{rad},\kappa}(R)
    \mathbb E_{\theta_{z_R}\sim q_R^{(\kappa)}(\cdot\mid x)}
    \left[
        \frac{
        \|b_x^{\mathrm{PD}}(\theta_{z_R},R) - b_\theta^{\mathrm{PD}}(\theta_{z_R},R)\|^2
        }{
        g_{\mathrm{PD}}(R)^2
        }
    \right]dR\,dt
\right] \\
&=
\frac{(d-1)^2 \kappa^4}{2}
\mathbb E_{x\sim p_{\mathrm{data}}}
\left[
    \int_0^T\int_0^{R_{\max}}
    \frac{p_t^{\mathrm{rad},\kappa}(R)}{\sinh(\kappa R)^2g_{\mathrm{PD}}(R)^2}
    \mathbb E_{\theta_{z_R}\sim q_R^{(\kappa)}(\cdot\mid x)}
    \left[
        \frac{\left\|P_{\theta_{z_R}}\!\left(x-\widehat x_\theta(\theta_{z_R},\kappa R)\right)\right\|^2}
        {D_x^{(\kappa)}(R,\theta_{z_R})^2}
    \right]dR\,dt
\right] \\
&=
\frac{(d-1)^2 \kappa^4}{2}
\mathbb E_{x\sim p_{\mathrm{data}}}
\left[
    \int_0^T \int_0^{R_{\max}} \int_{\mathbb S^{d-1}}
    \frac{p_t^{\mathrm{rad},\kappa}(R) q_R^{(\kappa)}(\theta_{z_R} \mid x)}{\sinh(\kappa R)^2D_x^{(\kappa)}(R,\theta_{z_R})^2g_{\mathrm{PD}}(R)^2}
    \left\|P_{\theta_{z_R}}\!\left(x-\widehat x_\theta(\theta_{z_R},\kappa R)\right)\right\|^2
    d\sigma(\theta_{z_R})\, dR\, dt
\right]
\end{aligned}
$$

($\sigma$: uniform probability measure on $\mathbb S^{d-1}$, w.r.t. which $q_R^{(\kappa)}$ is a density; for $d=2$, $d\sigma=d\phi/2\pi$.)

---

## When Is the Hyperbolic ELBO Curvature-Invariant?

Set the dimensionless radius and time to
$$
u=\kappa R,
\qquad
\tau=\kappa^2t.
$$

Metric scaling gives
$$
\begin{aligned}
D_x^{(\kappa)}(R,\theta)&=D_x(u,\theta),
&
q_R^{(\kappa)}(\theta\mid x)&=q_u(\theta\mid x),
\\
p_t^{\mathrm{rad},\kappa}(R)
&= \kappa\, \widetilde p_\tau^{\mathrm{rad}}(u)
&
dt&=\frac{d\tau}{\kappa^2}.
\end{aligned}
$$

---

## Change of Variable on Radius Integral

Since $p_t^{\mathrm{rad},\kappa}$ is a probability density with respect to $dR$
$$
\widetilde p_\tau^{\mathrm{rad}}(u)
:=
\frac{1}{\kappa}
p_{\tau/\kappa^2}^{\mathrm{rad},\kappa}\!\left(\frac{u}{\kappa}\right).
$$

Equivalently,

$$
\begin{aligned}
\int_0^{R_{\max}} p_t^{\mathrm{rad},\kappa}(R) dR
= \int_0^{\kappa R_{\max}} p_{\tau / \kappa^2}^{\mathrm{rad}, \kappa}(\frac{u}{\kappa}) \frac{du}{\kappa}
= \int_0^{\kappa R_{\max}} \widetilde p_\tau^{\mathrm{rad}}(u) du
\end{aligned}
$$

Thus the Jacobian $dR=du/\kappa$ is already absorbed into the transformed density. 

---

## When Is the Hyperbolic ELBO Curvature-Invariant?

With $g_{\mathrm{PD}}(R) = \frac{\kappa}{\sinh(\kappa R)}$ and $p_t^{\mathrm{rad},\kappa}(R)=\kappa\,\widetilde p_\tau^{\mathrm{rad}}(u)$,

$$
\begin{aligned}
\frac{p_t^{\mathrm{rad},\kappa}(R) q_R^{(\kappa)}(\theta_{z_R} \mid x)}{\sinh(\kappa R)^2D_x^{(\kappa)}(R,\theta_{z_R})^2g_{\mathrm{PD}}(R)^2}
\left\|P_{\theta_{z_R}}\!\left(x-\widehat x_\theta(\theta_{z_R},u)\right)\right\|^2
&= \frac{\kappa \widetilde p_\tau^{\mathrm{rad}}(u) q_u(\theta_{z_R} \mid x) \sinh(u)^2}{\sinh(u)^2 \kappa^2}
\frac{\left\|P_{\theta_{z_R}}\!\left(x-\widehat x_\theta(\theta_{z_R},u)\right)\right\|^2}{D_x(u,\theta_{z_R})^2} \\
&= \frac{\widetilde p_\tau^{\mathrm{rad}}(u) q_u(\theta_{z_R} \mid x)}{\kappa}
\frac{\left\|P_{\theta_{z_R}}\!\left(x-\widehat x_\theta(\theta_{z_R},u)\right)\right\|^2}{D_x(u,\theta_{z_R})^2} \\
\end{aligned}
$$

The learned endpoint depends on the dimensionless radius:
$$
\widehat x_\theta(\theta_{z_R},\kappa R)
=
\widehat x_\theta(\theta_{z_R},u).
$$

---

## Scale Equivariance Leaves One $\kappa^2$ Factor

$$
\begin{aligned}
\mathcal L_{\mathrm{PD}}(\theta)
&=
\frac12
\mathbb E_{x\sim p_{\mathrm{data}}}
\left[
    \int_0^T \int_0^{R_{\max}}
    p_t^{\mathrm{rad},\kappa}(R)
    \mathbb E_{\theta_{z_R}\sim q_R^{(\kappa)}(\cdot\mid x)}
    \left[
        \frac{
        \|b_x^{\mathrm{PD}}(\theta_{z_R},R) - b_\theta^{\mathrm{PD}}(\theta_{z_R},R)\|^2
        }{
        g_{\mathrm{PD}}(R)^2
        }
    \right]dR\,dt
\right] \\
&=
\frac{(d-1)^2 \kappa^4}{2}
\mathbb E_{x\sim p_{\mathrm{data}}}
\left[
    \int_0^{\kappa^2 T} \int_0^{\kappa R_{\max}} \int_{\mathbb S^{d-1}}
    \frac{\widetilde p_\tau^{\mathrm{rad}}(u) q_u(\theta_{z_R} \mid x)}{\kappa D_x(u,\theta_{z_R})^2}
    \left\|P_{\theta_{z_R}}\!\left(x-\widehat x_\theta(\theta_{z_R},u)\right)\right\|^2
    d\sigma(\theta_{z_R}) \frac{du}{\kappa} \frac{d\tau}{\kappa^2}
\right] \\
&=
\frac{(d-1)^2}{2}
\mathbb E_{x\sim p_{\mathrm{data}}}
\left[
    \int_0^{\kappa^2 T} \int_0^{\kappa R_{\max}} \int_{\mathbb S^{d-1}}
    \widetilde p_\tau^{\mathrm{rad}}(u) q_u(\theta_{z_R} \mid x)
    \frac{\left\|P_{\theta_{z_R}}\!\left(x-\widehat x_\theta(\theta_{z_R},u)\right)\right\|^2}{D_x(u,\theta_{z_R})^2}
    d\sigma(\theta_{z_R})\, du\, d\tau
\right]
\end{aligned}
$$

The conditional KL rate carries exactly one remaining factor $\kappa^2$:
$$
\frac{\|b_x^{\mathrm{PD}}-b_\theta^{\mathrm{PD}}\|^2}
{g_{\mathrm{PD}}^2}
=
\kappa^2(d-1)^2
\frac{\left\|P_{\theta_{z_R}}\!\left(x-\widehat x_\theta(\theta_{z_R},u)\right)\right\|^2}{D_x(u,\theta_{z_R})^2}.
$$

---

## Curvature Cancels in the Path-KL if Horizon Scales Properly

The $\kappa^2$ KL rate cancels with $dt=d\tau/\kappa^2$, giving
$$
\boxed{
\begin{aligned}
\mathcal L_{\mathrm{PD}}^{(\kappa)}(T,R_{\max})
&=
\frac{(d-1)^2}{2}\mathbb E_x
\left[
\int_0^{\kappa^2T}\!\int_0^{\kappa R_{\max}}
\widetilde p_\tau^{\mathrm{rad}}(u)
\mathbb E_{\theta_u\sim q_u(\cdot\mid x)}
\left[
\frac{\left\|P_{\theta_u}\!\left(x-\widehat x_\theta(\theta_u,u)\right)\right\|^2}{D_x(u,\theta_u)^2}
\right]du\,d\tau
\right].
\end{aligned}
}
$$

Therefore:

- **Fixed physical horizons:** not invariant, because the limits are $\kappa R_{\max}$ and $\kappa^2T$.
- **Infinite-horizon path-KL:** invariant when $T=R_{\max}=\infty$ and the learned predictor is scale-equivariant.

---

# What Curvature Actually Controls

- Curvature only controls the weight, but ELBO is invariant to curvature for infinite time and radius interval
- Curvature therefore controls decoding speed and which noise levels receive training mass.

---

The proposal distribution $p_t^{\mathrm{rad},\kappa}(R)$ over $t\in[0,5]$

![alt text](image.png)

---

Histogram of $p_t^{\mathrm{rad},\kappa}(R)/D_x^{(\kappa)}(R,\theta)$ over $t\in[0,5]$ for $K\in\{-0.01,-0.1,-1,-5,-10\}$, assuming $\langle x,\theta_z\rangle=1$

![alt text](image-3.png)

---

## Unit Embeddings Give a Weighted CE Bound

Let $\mathbf E=[e_1^\top;\ldots;e_V^\top]$ with $\|e_v\|_2=1$. For token $y$
$$
x=e_y=\mathbf E^\top\delta_y,
\qquad
p_\theta=p_\theta(\cdot\mid\theta_u,u),
\qquad
\widehat x_\theta=\mathbf E^\top p_\theta.
$$

Since $P_{\theta_u}$ is an orthogonal projector and $\|\mathbf E^\top a\|_2\leq\|a\|_1$,
$$
\begin{aligned}
\|P_{\theta_u}(x-\widehat x_\theta)\|_2^2
&\leq \|\mathbf E^\top(\delta_y-p_\theta)\|_2^2 \\
&\leq \|\delta_y-p_\theta\|_1^2 \\
&\leq 2\,\mathrm{KL}(\delta_y\|p_\theta)
=2\,\mathrm{CE}(y,p_\theta),
\end{aligned}
$$

---

## Weighted CE Upper-Bounds the Hyperbolic Path-KL

Substituting the embedding bound into the path-KL term gives
$$
\boxed{
\begin{aligned}
\mathcal L_{\mathrm{PD}}(\theta)
&\leq
(d-1)^2\mathbb E_y
\left[
\int_0^{\kappa^2T}\!\int_0^{\kappa R_{\max}}
\widetilde p_\tau^{\mathrm{rad}}(u)
\mathbb E_{\theta_u\sim q_u(\cdot\mid e_y)}
\left[
\frac{\mathrm{CE}(y,p_\theta)}{D_{e_y}(u,\theta_u)^2}
\right]du\,d\tau
\right]
\\
&=: \mathcal L_{\mathrm{CE}}^{\mathrm{hyp}}(\theta).
\end{aligned}
}
$$

---

# Conclusion

- Curvature controls the variance of the ELBO
- Can we make the geometry adaptive to the implied tree structure?

---

## Hyperbolic Product Manifold

Let
$$
\mathcal M
=
\prod_{m=1}^M \mathbb H_{K_m}^{d_m},
\qquad
K_m=-\kappa_m^2<0.
$$

Assume independent noises and a factorized bridge. For factor $m$, let
$$
D_{x_m} (u_m, \theta_{u_m})
=
\cosh(u_m)
-\sinh(u_m) \langle x_m,\theta_{u_m} \rangle,
\qquad
P_{\theta_{u_m}}=I_{d_m}-\theta_{u_m} \theta_{u_m}^\top
\qquad
g_m(R_m) = \frac{\kappa_m}{\sinh(\kappa_m R_m)}.
$$

Using the shared denominator in the true and learned drifts,
$$
\frac{\| b_{x_m, m}^{\mathrm{PD}} - b_{\theta_{u_m}, m}^{\mathrm{PD}} \|^2}{g_m(R_m)^2}
=
(d_m-1)^2\kappa_m^2
\frac{
\|P_{\theta_{u_m}}(x_m-\widehat x_{\theta,m}(\theta_{u_m}, u_m))\|^2
}{D_{x_m} (u_m, \theta_{u_m})^2}.
$$

---

### ELBO of Hyperbolic Product Manifold, Infinite Horizon

Set $u_m=\kappa_mR_m$ and $\tau_m=\kappa_m^2t$. Since

$$
\kappa_m^2p_{m,t}^{\mathrm{rad},\kappa_m}(R_m)dR_mdt
=\widetilde p_{\tau_m}^{\mathrm{rad}}(u_m)du_m d\tau_m
$$

the infinite-horizon ELBO is

$$
\begin{aligned}
\mathcal L_{\mathrm{Prod}}
&=
\sum_{m=1}^{M} \frac{(d_m-1)^2}{2}\mathbb E_x
\left[
\int_0^{\infty}\!\int_0^{\infty}
\widetilde p_{\tau_m}^{\mathrm{rad}}(u_m)
\mathbb E_{\theta_{u_m} \sim q_{u_m}(\cdot \mid x_m)}
\left[
\frac{\left\|P_{\theta_{u_m}}\!\left(x_m - \widehat x_{\theta,m}(\theta_{u_m}, u_m)\right)\right\|^2}{D_{x_m}(u_m, \theta_{u_m})^2}
\right] d u_m d \tau_m
\right].
\end{aligned}
$$

Thus, assuming scale-equivariant predictors and convergent integrals, the product ELBO is invariant to $\boldsymbol\kappa$.

---

# Conclusion

- We can build adaptive noise scheduler, not only temporally, but also spatially
- Incorporate with product manifold, we can achieve adaptive curvature for various directions
- Intuively, adaptive curvature means allocate proper step size and time budget on various depth of trees, which can solve the ill condition problem on word embedding for DLM.

---

