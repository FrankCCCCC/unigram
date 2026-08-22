import math
from dataclasses import dataclass
from typing import Optional

import torch

from geo_bridge import HyperbolicHeatKernel
from model import uniform_sphere_points

def isnan_or_inf(x):
    return torch.logical_or(torch.isnan(x), torch.isinf(x))

@dataclass
class LossGeometry:
    POINCARE_POLAR: str = "poincare_polar"
    POINCARE_POLAR_HOROCYCLE: str = "poincare_polar_horocycle"
    POINCARE_CARTESIAN: str = "poincare_cartesian"
    LORENTZ_POLAR: str = "lorentz_polar"
    LORENTZ_CARTESIAN: str = "lorentz_cartesian"
    HORO_CROSS_ENTROPY: str = "horo_cross_entropy"
    CROSS_ENTROPY: str = "cross_entropy"

@dataclass
class FlowPath:
    HYPERBOLIC_BOUNDARY: str = "hyperbolic_boundary"
    HYPERBOLIC_RFM: str = "hyperbolic_rfm"

class HyperBridge:
    PROPOSAL_EXP_NAME: str = "exp"
    PROPOSAL_STRATIFIED_EXP_NAME: str = "stratified_exp"
    PROPOSAL_TRUNCATED_EXP_NAME: str = "truncated_exp"
    PROPOSAL_UNIF_NAME: str = "unif"
    PROPOSAL_SIMPSON_NAME: str = "simpson"
    # Largest radial coordinate the bridge emits. Past ~372 both terms of the
    # horosphere log underflow, and cosh overflows outright past ss ~ 710.
    RHO_MAX: float = 350.0

    @staticmethod
    def sample_chi(ns, dtype=torch.float64):
        # chi(n) = sqrt(chi^2(n)), and chi^2(n) ~ Gamma(shape=n/2, scale=2).
        # Sampling Gamma directly avoids allocating sum(ns) standard normals,
        # which blows up when ns is large.
        concentration = ns.to(dtype) / 2
        rate = torch.tensor(0.5, device=ns.device, dtype=dtype)
        chi2 = torch.distributions.Gamma(concentration, rate).sample()
        # print(f"chi2: {isnan_or_inf(chi2).any()}")
        return chi2.sqrt()

    """
    Hyperbolic bridge for binary dimension
    """
    @staticmethod
    def _binary_vocab_angles(
        vocab_size: int,
        device: torch.device,
        dtype: torch.dtype,
        word_embedding: Optional[torch.FloatTensor] = None,
    ):
        # Boundary angle phi_v for every vocabulary word v.
        #   word_embedding given : direction of each word's 2-D embedding. atan2
        #     is scale-invariant, so the L2-normalization is a no-op for the angle
        #     and only guards against overflow.
        #   word_embedding None  : equally spaced points (v + 0.5) * 2*pi / V.
        if word_embedding is None:
            return (
                torch.arange(vocab_size, device=device, dtype=dtype) + 0.5
            ) * (2 * torch.pi / vocab_size)
        e = word_embedding.to(dtype)
        e = e / e.norm(dim=-1, p=2, keepdim=True)
        return torch.atan2(e[..., 1], e[..., 0])

    @staticmethod
    def binary_rotate_with_target(
        thetas: torch.FloatTensor,
        targets: torch.LongTensor,
        vocab_size: int,
        word_embedding: Optional[torch.FloatTensor] = None,
    ):
        # Rotate the spike (at angle 0) onto each target word's boundary angle,
        # using the same word->angle map the loss uses (see _binary_vocab_angles).
        phis = HyperBridge._binary_vocab_angles(
            vocab_size=vocab_size,
            device=thetas.device,
            dtype=thetas.dtype,
            word_embedding=word_embedding,
        )
        # Wrap into [0, 2*pi). The spike lies in (-pi, pi) and phi_v is an
        # arbitrary angle, so the raw sum ranges over (-2*pi, 2*pi) and its
        # UNWRAPPED value reveals which phi_v was added: a word whose
        # theta - phi_v falls outside (-pi, pi) cannot have produced this
        # sample. The loss is pure trigonometry and only ever sees theta mod
        # 2*pi, so it hands those impossible words their 2*pi-image
        # probability. Leaving theta unwrapped therefore feeds the model a
        # side channel the loss does not price in, and the ELBO stops being a
        # bound -- a trained model drops below H(p).
        return torch.remainder(thetas + phis[targets], 2 * torch.pi)

    @staticmethod
    def binary_bridge(
        ts,
        targets: torch.LongTensor,
        vocab_size: int,
        word_embedding: Optional[torch.FloatTensor] = None,
    ):
        # Radial sampling. cosh overflows to +inf for ss > 710, which would make
        # rho = +inf and NaN the whole batch -- reachable with proposal_type=unif
        # at the shipped hyper_T (t up to 1e5 gives ~99% non-finite rho). Capping
        # rho is statistically a no-op: by RHO_MAX the bridge angle already
        # identifies the target to full float64 precision (exp(-2*rho) underflows
        # past ~372), so every larger rho is indistinguishable from RHO_MAX.
        ns = torch.poisson(ts/8).to(torch.int64)
        ss = ts.sqrt() * HyperBridge.sample_chi(2*ns+3, ts.dtype)
        vs = torch.rand_like(ts)
        ps = torch.acosh(vs.square() + (1-vs.square())*torch.cosh(ss.clamp_max(700.0)))
        ps = ps.clamp_max(HyperBridge.RHO_MAX)

        # Free angles
        us = torch.rand_like(ts)
        # Spike angle on 0
        thetas = 2 * torch.atan((-ps).exp() * torch.tan(torch.pi * (us - 0.5)))

        thetas = HyperBridge.binary_rotate_with_target(
            thetas=thetas,
            targets=targets,
            vocab_size=vocab_size,
            word_embedding=word_embedding,
        )
        return ps, thetas

    @staticmethod
    def binary_horosphere_geometry(rhos, thetas, vocab_size, word_embedding=None):
        """Shared geometry: (alphas, sin_half_sq, cos_half_sq, horosphere_dists).

        `horosphere_dists[n, v]` is the log density of the bridge angle at word
        v, up to a v-independent constant, so `softmax(horosphere_dists +
        log p)` is exactly the Bayes posterior q(y | z_t). Every consumer of the
        logits must therefore treat them as a RESIDUAL on top of this term.
        """
        phis = HyperBridge._binary_vocab_angles(
            vocab_size=vocab_size,
            device=rhos.device,
            dtype=torch.float64,
            word_embedding=word_embedding,
        )
        alphas = thetas[:,None] - phis[None,:]  # angular offsets between z and v
        # Everything below is written via the half-angle identities
        # 1 - cos(a) = 2 sin^2(a/2) and 1 + cos(a) = 2 cos^2(a/2). The direct
        # forms cancel catastrophically at large rho, where the bridge angle is
        # absorbed by phi_v and a == 0 exactly: (1 - cos a) is then 0 rather than
        # a^2/2, so its log is -inf and the backward pass evaluates 0 * inf = NaN.
        half_alphas = alphas / 2
        sin_half_sq = half_alphas.sin().square()
        cos_half_sq = half_alphas.cos().square()
        # log2 - log((1 - cos a) e^rho + (1 + cos a) e^-rho), with e^rho pulled
        # out of the log so nothing overflows. clamp_min keeps the log finite
        # once BOTH terms underflow (rho > ~372.6, where sin_half_sq is exactly
        # 0 for the target word); without it horosphere_dists is +inf and the
        # softmax below returns NaN for the whole row.
        horosphere_dists = -rhos[:,None] - (
            sin_half_sq + cos_half_sq * (-2 * rhos[:,None]).exp()
        ).clamp_min(torch.finfo(torch.float64).tiny).log()
        return alphas, sin_half_sq, cos_half_sq, horosphere_dists

    @staticmethod
    def binary_bridge_loss_poincare_disk_polar(logits, targets, rhos, thetas, word_embedding=None):
        (N,) = targets.shape
        (N,V) = logits.shape
        assert(rhos.shape == (N,))
        assert(thetas.shape == (N,))
        assert(targets.dtype == torch.int64)
        assert(rhos.dtype == torch.float64)
        assert(thetas.dtype == torch.float64)
        assert word_embedding is None or tuple(word_embedding.shape) == (V, 2)
        # betas below needs exp(+rho), which overflows past rho ~ 709 and then
        # yields 0 * inf = NaN for the target word. binary_bridge already caps
        # rho, so this only defends against callers passing raw values.
        rhos = rhos.clamp_max(HyperBridge.RHO_MAX)
        alphas, sin_half_sq, cos_half_sq, horosphere_dists = HyperBridge.binary_horosphere_geometry(
            rhos=rhos,
            thetas=thetas,
            vocab_size=V,
            word_embedding=word_embedding,
        )
        sin_alphas = alphas.sin()
        # cos_alphas = alphas.cos()
        # remake mu and subtract the target
        mu = (horosphere_dists + logits.to(torch.float64)).softmax(-1)
        mu = mu - torch.nn.functional.one_hot(targets,V).to(torch.float64)
        # next, we transform the angles alpha after motion by rho.
        # cosh(rho) cos(a) - sinh(rho), again cancellation-free: the direct form
        # collapses to cosh(rho) - sinh(rho), which is 0 in float64 once
        # rho > ~19 even though the true value is e^-rho, and atan2(0, 0) has no
        # gradient.
        betas = torch.atan2(
            sin_alphas,
            cos_half_sq * (-rhos[:,None]).exp() - sin_half_sq * rhos[:,None].exp(),
        )
        # betas = torch.atan2(
        #     sin_alphas,
        #     rhos.cosh()[:,None] * cos_alphas - rhos.sinh()[:,None]
        # )
        cos_errors = (betas.cos() * mu).sum(-1)
        sin_errors = (betas.sin() * mu).sum(-1)
        return (cos_errors.square() + sin_errors.square())/2

    # @staticmethod
    # def binary_bridge_loss_poincare_disk_polar_horocycle(logits, targets, rhos, thetas, word_embedding=None):
    #     (N,) = targets.shape
    #     (N,V) = logits.shape
    #     device = rhos.device
    #     assert(rhos.shape == (N,))
    #     assert(thetas.shape == (N,))
    #     assert(targets.dtype == torch.int64)
    #     assert(rhos.dtype == torch.float64)
    #     assert(thetas.dtype == torch.float64)
    #     assert word_embedding is None or tuple(word_embedding.shape) == (V, 2)
    #     # phi_v for every vocab word: learnable embedding angles when given,
    #     # otherwise the equally spaced points used by the *_old variant.
    #     phis = HyperBridge._binary_vocab_angles(
    #         vocab_size=V,
    #         device=device,
    #         dtype=torch.float64,
    #         word_embedding=word_embedding,
    #     )
    #     # first, we get the horosphere distances
    #     # print(f"thetas ({thetas.mean().item()}): {torch.isfinite(thetas).all().item()}")
    #     # print(f"phis ({phis.mean().item()}): {torch.isfinite(phis).all().item()}")
    #     alphas = thetas[:,None] - phis[None,:]  # angular offsets between z and v
    #     # print(f"alphas: {torch.isfinite(alphas).all().item()}")
    #     cos_alphas = alphas.cos()
    #     sin_alphas = alphas.sin()
    #     # remake mu and subtract the target
    #     mu = logits.to(torch.float64).softmax(-1)
    #     mu = mu - torch.nn.functional.one_hot(targets,V).to(torch.float64)
    #     # next, we transform the angles alpha after motion by rho
    #     betas = torch.atan2(sin_alphas, rhos.cosh()[:,None] * cos_alphas - rhos.sinh()[:,None])
    #     cos_errors = (betas.cos() * mu).sum(-1)
    #     sin_errors = (betas.sin() * mu).sum(-1)
    #     return (cos_errors.square() + sin_errors.square())/2

    """
    Hyperbolic bridge for arbitary dimension
    """
    @staticmethod
    def _vocab_angles(
        vocab_size: Optional[int] = None,
        emb_dim: Optional[int] = None,
        device: Optional[torch.device] = None,
        dtype: torch.dtype = torch.float64,
        word_embedding: Optional[torch.FloatTensor] = None,
    ):
        # Boundary direction phi_v on S^{d-1} for every vocabulary word v -- the
        # d-dimensional analogue of _binary_vocab_angles.
        #   word_embedding given : direction of each word's d-D embedding. The
        #     L2-normalization is a no-op for the direction and only fixes the
        #     scale.
        #   word_embedding None  : uniform_sphere_points(V, d) -- the same fixed
        #     table MLPLM uses for unif_word_embedding (equally spaced angles at
        #     d == 2, seeded Gaussian directions at d > 2), regenerated
        #     deterministically so the bridge and the loss share one
        #     word -> direction map.
        if word_embedding is None:
            return uniform_sphere_points(vocab_size, emb_dim, device=device, dtype=dtype)
        e = word_embedding.to(dtype)
        return e / e.norm(dim=-1, p=2, keepdim=True).clamp_min(torch.finfo(dtype).tiny)

    @staticmethod
    def rotate_with_target(
        thetas: torch.FloatTensor,
        targets: torch.LongTensor,
        vocab_size: Optional[int] = None,
        emb_dim: Optional[int] = None,
        word_embedding: Optional[torch.FloatTensor] = None,
    ):
        # Carry the spike (centred on e_1) onto each target word's boundary
        # direction, using the same word -> direction map the loss uses (see
        # _vocab_angles). The Householder reflection e_1 -> phi_y is an isometry
        # of S^{d-1} and the spike law is rotationally symmetric about e_1, so
        # reflecting instead of rotating leaves the bridge law unchanged. Unlike
        # the scalar-angle path (see binary_rotate_with_target) there is no
        # wrap-around side channel to close: a unit vector carries no winding
        # count for the loss to miss.
        phis = HyperBridge._vocab_angles(
            vocab_size=vocab_size,
            emb_dim=emb_dim,
            device=thetas.device,
            dtype=thetas.dtype,
            word_embedding=word_embedding,
        )
        return HyperbolicHeatKernel._reflect_to_target(thetas, phis[targets])

    @staticmethod
    def _radial_t_max(d: int) -> float:
        # Largest heat time sample_radial can integrate in float64: it forms the
        # marginal sinh^{d-1}(rho) p_H(rho; t) in linear space over a grid
        # reaching rho ~ sqrt(t) (E[chi_d] + 16) + (d-1) t / 2, and its even-d
        # McKean base evaluates cosh a further 8 sqrt(t) + 1 beyond it; both
        # overflow once the exponent passes ~709. Solving
        #   0.5 (d-1) t + (E[chi_d] + 24) sqrt(t) + 1 <= 700 / (d-1)
        # for sqrt(t) keeps the whole grid representable for every d >= 2.
        b = HyperbolicHeatKernel._euclid_mean(d) + 24.0
        c = 700.0 / (d - 1) - 1.0
        half_a = 0.5 * (d - 1)
        s = (math.sqrt(b * b + 4.0 * half_a * c) - b) / (2.0 * half_a)
        return s * s

    @staticmethod
    def bridge(
        ts,
        targets: torch.LongTensor,
        vocab_size: Optional[int] = None,
        emb_dim: Optional[int] = None,
        word_embedding: Optional[torch.FloatTensor] = None,
    ):
        """Sample the H^d bridge state `(rhos, us)` at heat times `ts`.

        d-dimensional analogue of binary_bridge. The bridge toward a boundary
        word factorizes exactly: the radial coordinate keeps the FREE
        heat-kernel marginal (the Poisson kernel is harmonic with unit
        spherical mean, so conditioning on the target does not disturb it) and
        the direction follows the Poisson kernel
        `(cosh rho - sinh rho <u, e_1>)^-(d-1)` centred on e_1, carried onto
        the target word's boundary direction. `d` comes from
        `word_embedding.shape[-1]` when given, else `emb_dim`.

        binary_bridge is the d == 2 special case in closed form (Gruet) and is
        much cheaper; this path prices any d >= 2 through sample_radial's
        numeric inverse-CDF.

        Returns `(rhos, us)`: shapes `(N,)` and `(N, d)`, both `ts.dtype`.
        """
        d = word_embedding.shape[-1] if word_embedding is not None else emb_dim
        # Radial sampling. sample_radial forms the heat-kernel marginal in
        # linear float64, which overflows at large t (reachable with
        # proposal_type=unif at the shipped hyper_T). Clamping t is
        # statistically a no-op for the same reason capping rho is: by
        # _radial_t_max the radial mass sits at rho ~ 700/(d-1), where the
        # direction already identifies the target to full float64 precision
        # (exp(-2*(d-1)*rho) underflows past rho ~ 372/(d-1)), so every larger
        # t is indistinguishable.
        ts = ts.clamp_max(HyperBridge._radial_t_max(d))
        rhos = HyperbolicHeatKernel.sample_radial(ts, d=d, seq_len=1).squeeze(-1)
        rhos = rhos.clamp_max(HyperBridge.RHO_MAX)

        # Spike direction on e_1
        us = HyperbolicHeatKernel._angular_boost(rhos, d=d)

        us = HyperBridge.rotate_with_target(
            thetas=us,
            targets=targets,
            vocab_size=vocab_size,
            emb_dim=emb_dim,
            word_embedding=word_embedding,
        )
        return rhos, us

    @staticmethod
    def horosphere_geometry(rhos, thetas, vocab_size, word_embedding=None):
        """Shared geometry: (phis, sin_half_sq, cos_half_sq, horosphere_dists).

        d-dimensional analogue of binary_horosphere_geometry, with the bridge
        direction `thetas` a unit vector of shape (N, d) instead of a scalar
        angle. `horosphere_dists[n, v] = -(d-1) B_v(z_n)` -- `B_v` the Busemann
        function of word v's boundary point -- is the log density of the bridge
        direction at word v, up to a v-independent constant, so
        `softmax(horosphere_dists + log p)` is exactly the Bayes posterior
        q(y | z_t). Every consumer of the logits must therefore treat them as a
        RESIDUAL on top of this term.
        """
        phis = HyperBridge._vocab_angles(
            vocab_size=vocab_size,
            emb_dim=thetas.shape[-1],
            device=rhos.device,
            dtype=torch.float64,
            word_embedding=word_embedding,
        )
        d = phis.shape[-1]
        # The half-angle identities of the binary path in vector form:
        #   sin^2(a_v/2) = (1 - <u, phi_v>) / 2 = ||u - phi_v||^2 / 4
        #   cos^2(a_v/2) = (1 + <u, phi_v>) / 2 = ||u + phi_v||^2 / 4
        # The difference form is just as cancellation-free: evaluating
        # 1 - <u, phi_v> directly collapses to 0 once the bridge direction is
        # within ~1e-8 of the target word, its log to -inf, and the backward
        # pass to 0 * inf = NaN.
        diffs = thetas[:, None, :] - phis[None, :, :]
        sums = thetas[:, None, :] + phis[None, :, :]
        sin_half_sq = diffs.square().sum(-1) / 4
        cos_half_sq = sums.square().sum(-1) / 4
        # -(d-1) log(cosh rho - sinh rho <u, phi_v>), with e^rho pulled out of
        # the log so nothing overflows. clamp_min keeps the log finite once
        # BOTH terms underflow (rho > ~372.6, where sin_half_sq is exactly 0
        # for the target word); without it horosphere_dists is +inf and the
        # softmax downstream returns NaN for the whole row.
        horosphere_dists = -(d - 1) * (
            rhos[:, None] + (
                sin_half_sq + cos_half_sq * (-2 * rhos[:, None]).exp()
            ).clamp_min(torch.finfo(torch.float64).tiny).log()
        )
        return phis, sin_half_sq, cos_half_sq, horosphere_dists

    @staticmethod
    def bridge_loss_poincare_disk_polar(logits, targets, rhos, thetas, word_embedding=None):
        (N,) = targets.shape
        (N,V) = logits.shape
        d = thetas.shape[-1]
        assert(rhos.shape == (N,))
        assert(thetas.shape == (N, d))
        assert(targets.dtype == torch.int64)
        assert(rhos.dtype == torch.float64)
        assert(thetas.dtype == torch.float64)
        assert word_embedding is None or tuple(word_embedding.shape) == (V, d)
        # ws below needs exp(+rho), which overflows past rho ~ 709 and then
        # yields 0 * inf = NaN for the target word. bridge already caps rho, so
        # this only defends against callers passing raw values.
        rhos = rhos.clamp_max(HyperBridge.RHO_MAX)
        phis, sin_half_sq, cos_half_sq, horosphere_dists = HyperBridge.horosphere_geometry(
            rhos=rhos,
            thetas=thetas,
            vocab_size=V,
            word_embedding=word_embedding,
        )
        # remake mu and subtract the target
        mu = (horosphere_dists + logits.to(torch.float64)).softmax(-1)
        mu = mu - torch.nn.functional.one_hot(targets,V).to(torch.float64)
        # next, we transport each word's boundary direction into the frame at
        # z: the boost carrying z = (rho, u) back to the origin maps phi_v to
        # the unit vector
        #   w_v = [(cos_half_sq e^-rho - sin_half_sq e^+rho) u + p_v] / D_v,
        #   p_v = phi_v - <u, phi_v> u,
        #   D_v = sin_half_sq e^+rho + cos_half_sq e^-rho,
        # the d-dimensional form of the binary
        # betas = atan2(sin a, cos_half_sq e^-rho - sin_half_sq e^+rho): at
        # d == 2, w_v = (cos beta_v, sin beta_v) in the (u, u_perp) basis. As
        # there, the e^{+-rho} split is cancellation-free: the direct
        # cosh(rho) <u, phi_v> - sinh(rho) collapses to 0 in float64 once
        # rho > ~19 even though the true value is e^-rho.
        exp_pos = rhos[:,None].exp()
        exp_neg = (-rhos[:,None]).exp()
        radial_parts = cos_half_sq * exp_neg - sin_half_sq * exp_pos
        # D_v is the Poisson-kernel denominator rescaled by e^-rho; it reaches
        # 0 only past rho ~ 745, which RHO_MAX already rules out, so the clamp
        # is a guard, not a code path.
        denoms = (sin_half_sq * exp_pos + cos_half_sq * exp_neg).clamp_min(
            torch.finfo(torch.float64).tiny
        )
        inners = cos_half_sq - sin_half_sq  # <u, phi_v>, cancellation-free
        perps = phis[None,:,:] - inners[...,None] * thetas[:,None,:]
        ws = (radial_parts[...,None] * thetas[:,None,:] + perps) / denoms[...,None]
        # The bridge drift toward word v is (d-1) w_v (the Doob h-transform of
        # h_v = e^{-(d-1) B_v} under generator Delta/2), so the Girsanov
        # integrand between the model's posterior-mixture drift and the target
        # bridge drift is (d-1)^2/2 ||sum_v mu_v w_v||^2 -- the (d-1)^2 factor
        # is 1 in the binary case.
        errors = (mu[...,None] * ws).sum(-2)
        return (d - 1) ** 2 * errors.square().sum(-1) / 2

class Loss:
    """
    Loss of binary dimension Poincare Disk
    """
    @staticmethod
    def binary_bridge_loss_crossentropy(logits, targets, rhos, thetas, word_embedding=None):
        """Denoising cross-entropy of the model's OWN predictive distribution.

        The model's posterior over words is softmax(horosphere_dists + logits):
        the logits are a residual on top of the bridge geometry, not the
        distribution itself. Scoring cross_entropy(logits, targets) instead
        would train the logits to BE the posterior, which the poincare-polar
        readout then double-counts by adding horosphere_dists a second time --
        measured, that inflates the reported ELBO from 0.4997 to 0.8714 (1.74x)
        for the exact Bayes solution. It also makes the importance-weighted CE
        a divergent integral, because CE(t) then tends to H(p) > 0 as t -> inf
        instead of decaying to 0.
        """
        V = logits.shape[-1]
        _, _, _, horosphere_dists = HyperBridge.binary_horosphere_geometry(
            rhos=rhos,
            thetas=thetas,
            vocab_size=V,
            word_embedding=word_embedding,
        )
        return torch.nn.functional.cross_entropy(
            horosphere_dists + logits.to(torch.float64),
            targets,
            reduction='none',
        )

    @staticmethod
    def weighted_binary_loss(logits, targets, rhos, thetas, proposal_weight, word_embedding=None, loss_geometry="poincare_polar"):
        if loss_geometry == LossGeometry.POINCARE_POLAR:
            # print("Use POINCARE_POLAR")
            bridge = HyperBridge.binary_bridge_loss_poincare_disk_polar(
                logits=logits,
                targets=targets,
                rhos=rhos,
                thetas=thetas,
                word_embedding=word_embedding,
            )
        elif loss_geometry == LossGeometry.CROSS_ENTROPY:
            bridge = Loss.binary_bridge_loss_crossentropy(
                logits=logits,
                targets=targets,
                rhos=rhos,
                thetas=thetas,
                word_embedding=word_embedding,
            )
        else:
            raise ValueError(f"Unknown loss_geometry={loss_geometry!r}")
        return bridge * proposal_weight.to(dtype=bridge.dtype), bridge

    """
    Loss of arbitary dimension Poincare Disk
    """
    @staticmethod
    def bridge_loss_crossentropy(logits, targets, rhos, thetas, word_embedding=None):
        """Denoising cross-entropy of the model's OWN predictive distribution.

        The model's posterior over words is softmax(horosphere_dists + logits):
        the logits are a residual on top of the bridge geometry, not the
        distribution itself. Scoring cross_entropy(logits, targets) instead
        would train the logits to BE the posterior, which the poincare-polar
        readout then double-counts by adding horosphere_dists a second time --
        measured, that inflates the reported ELBO from 0.4997 to 0.8714 (1.74x)
        for the exact Bayes solution. It also makes the importance-weighted CE
        a divergent integral, because CE(t) then tends to H(p) > 0 as t -> inf
        instead of decaying to 0.
        """
        V = logits.shape[-1]
        _, _, _, horosphere_dists = HyperBridge.horosphere_geometry(
            rhos=rhos,
            thetas=thetas,
            vocab_size=V,
            word_embedding=word_embedding,
        )
        return torch.nn.functional.cross_entropy(
            horosphere_dists + logits.to(torch.float64),
            targets,
            reduction='none',
        )

    @staticmethod
    def weighted_loss(logits, targets, rhos, thetas, proposal_weight, word_embedding=None, loss_geometry="poincare_polar"):
        if loss_geometry == LossGeometry.POINCARE_POLAR:
            # print("Use POINCARE_POLAR")
            bridge = HyperBridge.bridge_loss_poincare_disk_polar(
                logits=logits,
                targets=targets,
                rhos=rhos,
                thetas=thetas,
                word_embedding=word_embedding,
            )
        elif loss_geometry == LossGeometry.CROSS_ENTROPY:
            bridge = Loss.bridge_loss_crossentropy(
                logits=logits,
                targets=targets,
                rhos=rhos,
                thetas=thetas,
                word_embedding=word_embedding,
            )
        else:
            raise ValueError(f"Unknown loss_geometry={loss_geometry!r}")
        return bridge * proposal_weight.to(dtype=bridge.dtype), bridge

class Proposal:
    @staticmethod
    def proposal(
        proposal_type: str,
        shape,
        device,
        dtype,
        unif_min: float,
        unif_max: float,
        exp_rate: float,
        generator: Optional[torch.Generator] = None,
    ):
        proposal_type = proposal_type.lower()
        interval = float(unif_max - unif_min)
        if interval < 0:
            raise ValueError("proposal requires unif_max >= unif_min")

        if proposal_type == HyperBridge.PROPOSAL_UNIF_NAME:
            ts = unif_min + interval * torch.rand(shape, device=device, dtype=dtype, generator=generator)
            weights = torch.full_like(ts, interval)
            return ts, weights
        elif proposal_type == HyperBridge.PROPOSAL_TRUNCATED_EXP_NAME:
            if exp_rate <= 0:
                raise ValueError("proposal_exp_rate must be > 0")
            if interval == 0:
                ts = torch.full(shape, unif_min, device=device, dtype=dtype)
                return ts, torch.zeros_like(ts)
            u = torch.rand(shape, device=device, dtype=dtype, generator=generator).clamp(
                min=1e-12,
                max=1 - 1e-12,
            )
            normalizer = 1 - torch.exp(
                torch.tensor(-exp_rate * interval, device=device, dtype=dtype)
            )
            ts = unif_min - torch.log1p(-u * normalizer) / exp_rate
            density = exp_rate * torch.exp(-exp_rate * (ts - unif_min)) / normalizer
            return ts, density.reciprocal()
        elif proposal_type == HyperBridge.PROPOSAL_EXP_NAME:
            if exp_rate <= 0:
                raise ValueError("proposal_exp_rate must be > 0")
            if interval == 0:
                ts = torch.zeros(shape, device=device, dtype=dtype)
                return ts, torch.zeros_like(ts)
            u = torch.rand(shape, device=device, dtype=dtype, generator=generator).clamp(
                min=1e-12,
                max=1 - 1e-12,
            )
            # Use torch.log(-u) is also correct, but torch.log1p(-u) is more numerically stable because it can handle u close to 0
            ts = - torch.log1p(-u) / exp_rate
            density = exp_rate * torch.exp(-exp_rate * ts)
            return ts, density.reciprocal()
        elif proposal_type == HyperBridge.PROPOSAL_STRATIFIED_EXP_NAME:
            if exp_rate <= 0:
                raise ValueError("proposal_exp_rate must be > 0")
            numel = 1
            for dim in shape:
                numel *= int(dim)
            u = (
                torch.arange(numel, device=device, dtype=dtype)
                + torch.rand(numel, device=device, dtype=dtype, generator=generator)
            ) / numel
            u = u.view(-1)[torch.randperm(u.numel(), device=device, generator=generator)].view(u.shape)
            u = u.clamp(min=1e-12, max=1 - 1e-12).reshape(shape)
            # The same ts sampling as: ts = - torch.log(u) / exp_rate
            # ts = - torch.log1p(-u) / exp_rate
            ts = - torch.log(u) / exp_rate
            # The same equation as: weights = (exp_rate * ts).exp() / exp_rate
            weights = 1.0 / (exp_rate * u)
            # weights = (exp_rate * ts).exp() / exp_rate
            return ts, weights
        else:
            raise NotImplementedError(f"proposal_type={proposal_type} is not implemented.")

    @staticmethod
    def hyper_proposal(
        proposal_type: str,
        shape,
        device,
        dtype,
        dt: float = 0.01,
        T: int = 1000,
        exp_rate: float = 1.0,
        generator: Optional[torch.Generator] = None,
    ):
        if dt is None or T is None or dt <= 0.0 or T <= 0:
            raise ValueError("dt and T must be positive for hyper_proposal.")

        total_time = dt * T
        unif_min = float(max(dt, 1e-8))
        unif_max = float(max(total_time, unif_min))

        ts, proposal_weight = Proposal.proposal(
            proposal_type=proposal_type,
            shape=shape,
            device=device,
            dtype=dtype,
            unif_min=unif_min,
            unif_max=unif_max,
            exp_rate=exp_rate,
            generator=generator,
        )
        return ts, proposal_weight