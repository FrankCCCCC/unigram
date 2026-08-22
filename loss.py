from dataclasses import dataclass
from typing import Optional

import torch

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
        vocab_size: int = None,
        emb_dim: int = None,
        word_embedding: Optional[torch.FloatTensor] = None,
    ):
        """
        word_embedding: torch.FloatTensor : [V, d]
        return: 
            if word_embedding is None:
                Return uniformly distributed spherical word embedding
                return [V, d], \in \mathbb{S}^{d-1}
            else:
                Rotate the uniformly distribution with direction of word_embedding
                return [V, d], \in \mathbb{S}^{d-1}
        """
        if word_embedding is None:
            if vocab_size is not None and emb_dim is not None:
                word_embedding = torch.randn(vocab_size, emb_dim)
        e = word_embedding
        e = e / e.norm(dim=-1, p=2, keepdim=True)
        return e

    @staticmethod
    def rotate_with_target(
        thetas: torch.FloatTensor,
        targets: torch.LongTensor,
        vocab_size: int = None,
        emb_dim: int = None,
        word_embedding: Optional[torch.FloatTensor] = None,
    ):
        """

        """
        # Rotate the spike (at angle 0) onto each target word's boundary angle,
        # using the same word->angle map the loss uses (see _vocab_angles).
        phis = HyperBridge._vocab_angles(
            vocab_size=vocab_size,
            emb_dim=emb_dim,
            word_embedding=word_embedding,
        )
        # TODO: Implement the rotation for arbitary dim

    @staticmethod
    def bridge(
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
        return ps, thetas

    @staticmethod
    def horosphere_geometry(rhos, thetas, vocab_size, word_embedding=None):
        """Shared geometry: (alphas, sin_half_sq, cos_half_sq, horosphere_dists).

        `horosphere_dists[n, v]` is the log density of the bridge angle at word
        v, up to a v-independent constant, so `softmax(horosphere_dists +
        log p)` is exactly the Bayes posterior q(y | z_t). Every consumer of the
        logits must therefore treat them as a RESIDUAL on top of this term.
        """
        phis = HyperBridge._vocab_angles(
            vocab_size=vocab_size,
            device=rhos.device,
            dtype=torch.float64,
            word_embedding=word_embedding,
        )
        # TODO: arbiarty dim horosphere geo

    @staticmethod
    def bridge_loss_poincare_disk_polar(logits, targets, rhos, thetas, word_embedding=None):
        # (N,) = targets.shape
        # (N,V) = logits.shape
        # assert(rhos.shape == (N,))
        # assert(thetas.shape == (N,))
        # assert(targets.dtype == torch.int64)
        # assert(rhos.dtype == torch.float64)
        # assert(thetas.dtype == torch.float64)
        # assert word_embedding is None or tuple(word_embedding.shape) == (V, 2)
        # betas below needs exp(+rho), which overflows past rho ~ 709 and then
        # yields 0 * inf = NaN for the target word. binary_bridge already caps
        # rho, so this only defends against callers passing raw values.
        rhos = rhos.clamp_max(HyperBridge.RHO_MAX)
        alphas, sin_half_sq, cos_half_sq, horosphere_dists = HyperBridge.horosphere_geometry(
            rhos=rhos,
            thetas=thetas,
            vocab_size=V,
            word_embedding=word_embedding,
        )
        # TODO: Implement Polar Poincare Disk ELBO for arbitrary dim

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