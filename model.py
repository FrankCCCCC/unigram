import math
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union

import torch
import torch.nn as nn

from geo_bridge import GeoUtils

class SmallMLP(nn.Module):
    """Tiny time-conditioned MLP that predicts a hyperbolic endpoint."""

    def __init__(
        self,
        input_dim: int,
        hidden_size: int,
        depth: int,
        output_dim: int,
    ):
        super().__init__()
        layers = []
        dim = input_dim
        for _ in range(depth):
            layers.append(nn.Linear(dim, hidden_size))
            layers.append(nn.Tanh())
            dim = hidden_size
        layers.append(nn.Linear(dim, output_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, z: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        """
        Apply the time-conditioned MLP.

        Args:
            z (`torch.Tensor` of shape `(batch_size, io_dim)`):
                Input state in model coordinates.
            t (`torch.Tensor` of shape `(batch_size,)` or `(batch_size, 1)`):
                Per-example time values.

        Returns:
            `torch.Tensor` of shape `(batch_size, output_dim)`:
                Predicted endpoint features.
        """
        if t.ndim == 1:
            t = t[:, None]
        return self.net(torch.cat([z, t], dim=-1))

class HyperbolicModelBase(nn.Module, ABC):
    """Shared readout for models whose state lives on a product of Poincare balls.

    The manifold is `H^{d_1}_{K_1} x ... x H^{d_m}_{K_m}` and the state is the
    `Coordinate.HYPERBOLIC_POLAR` output of
    `HyperbolicHeatKernel.poincare_bridge_prod`: one radial coordinate per factor
    (`radius`, last axis `m`) plus the per-factor unit boundary directions
    concatenated (`theta`, last axis `sum(d_i) == embedding_size`). Both lists
    `None` means the single factor `[embedding_size]` at `[-1.0]`, i.e. plain
    `H^d` -- the same default `poincare_bridge_prod` uses.

    Subclasses supply the trunk (`model_forward`), the boundary table
    (`word_embedding`), and three attributes this class reads: `lm_head`
    (the trunk-features -> vocabulary readout), `output_radial_dim` (how many
    trailing trunk channels are the predicted radius rather than features), and
    the factor spec `prod_factor_dim` / `prod_factor_gaussian_curvature` the
    horosphere readout defaults to. `word_embedding` is required, not optional:
    the horosphere readout has no table of its own to fall back on.

    Two readouts, differing only in who adds the geometry:
      naive       -- returns `lm_head`'s logits untouched. Per Invariant 1 those
                     are a RESIDUAL, so the consumer must add
                     `horosphere_geometry` itself (this is what `loss.py` does).
      horosphere  -- adds `horosphere_geometry` here, so the returned logits are
                     already the full log-posterior and must NOT be corrected a
                     second time.
    """

    def __init__(
        self,
    ):
        super().__init__()

    @property
    @abstractmethod
    def word_embedding(self) -> torch.Tensor:
        pass

    @staticmethod
    def prod_factors(
        prod_factor_dim: Optional[Union[int, List[int]]],
        prod_factor_gaussian_curvature: Optional[Union[float, List[float]]],
        embedding_size: int,
    ):
        """
        Resolve and validate the product-factor split of a boundary of dimension
        `embedding_size`.

        Returns:
            `tuple[List[int], List[float]]`: the per-factor dimensions `d_i >= 2`
                (summing to `embedding_size`) and curvatures `K_i < 0`.
        """
        dims = prod_factor_dim
        curvatures = prod_factor_gaussian_curvature
        if dims is None and curvatures is None:
            return [embedding_size], [-1.0]
        if not (isinstance(dims, list) and isinstance(curvatures, list)):
            raise TypeError(
                "prod_factor_dim and prod_factor_gaussian_curvature must both be "
                f"lists or both be None; got {type(dims)} and {type(curvatures)}."
            )
        if len(dims) != len(curvatures):
            raise ValueError(
                f"prod_factor_dim {dims} and prod_factor_gaussian_curvature "
                f"{curvatures} must have the same length."
            )
        if sum(dims) != embedding_size:
            raise ValueError(
                f"prod_factor_dim {dims} should sum to the embedding size {embedding_size}."
            )
        for factor_dim, factor_curvature in zip(dims, curvatures):
            if factor_dim < 2:
                raise ValueError(f"Each product factor needs dim >= 2, not {factor_dim}.")
            if factor_curvature >= 0.0:
                raise ValueError(f"Hyperbolic curvature should be negative, not {factor_curvature}.")
        return dims, curvatures

    def forward(
        self,
        z: torch.Tensor,
        theta: torch.Tensor,
        radius: torch.Tensor,
        t: Optional[torch.Tensor] = None,
        forward_type: str = "naive",
        return_radial: bool=False,
        prod_factor_dim: Optional[Union[int, List[int]]] = None,
        prod_factor_gaussian_curvature: Optional[Union[float, List[float]]] = None,
    ) -> Tuple[torch.Tensor]:
        """
        Predict vocabulary logits from a time-conditioned state.

        Args:
            z (`torch.Tensor` of shape `(batch_size, max_seq_len, input_theta_dim)`):
                Input state in Cartesian coordinate
            theta (`torch.Tensor` of shape `(batch_size, max_seq_len, input_theta_dim)`):
                Input state in polar coordinate, angles
            radius (`torch.Tensor` of shape `(batch_size, max_seq_len, input_radius_dim)`):
                Input state in polar coordinate, radius, consider product manifold
            t (`torch.Tensor` of shape `(batch_size,)` or `(batch_size, 1)`):
                Per-example time values, optional
            forward_type (`str`, *optional*, defaults to `"naive"`):
                `"naive"` for the residual logits, `"horosphere"` for the
                geometry-corrected ones.
            return_radial (`bool`, *optional*, defaults to `False`):
                Also return the trunk's radial prediction.
            prod_factor_dim (`Union[int, List[int]]`, *optional*):
                Product-factor split, `"horosphere"` only. Both `None` falls
                back to the model's own factors.
            prod_factor_gaussian_curvature (`Union[float, List[float]]`, *optional*):
                Curvature `K_i < 0` of each factor.

        Returns:
            `torch.Tensor` of shape `(batch_size, max_seq_len, vocab_size)`:
                Vocabulary logits.
            `torch.Tensor` of shape `(batch_size, max_seq_len, output_radial_dim)`:
                if return_radial, the predicted radius
        """
        if forward_type == "naive":
            return self.forward_naive(
                z=z,
                theta=theta,
                radius=radius,
                t=t,
                return_radial=return_radial,
            )
        elif forward_type == "horosphere":
            return self.forward_horosphere(
                z=z,
                theta=theta,
                radius=radius,
                prod_factor_dim=prod_factor_dim,
                prod_factor_gaussian_curvature=prod_factor_gaussian_curvature,
                t=t,
                return_radial=return_radial,
            )
        else:
            raise ValueError(f"forward_type, {forward_type}, is not supported.")

    @abstractmethod
    def model_forward(
        self,
        z: torch.Tensor,
        t: torch.Tensor,
    ):
        pass

    def forward_naive(
        self,
        z: torch.Tensor,
        theta: torch.Tensor,
        radius: torch.Tensor,
        t: Optional[torch.Tensor] = None,
        return_radial: bool=False
    ) -> Tuple[torch.Tensor]:
        """
        Predict vocabulary logits from a time-conditioned state.

        The state comes in ONE of the two coordinate systems: either Cartesian
        `z`, or polar `(theta, radius)` -- concatenated on the last axis, so the
        trunk sees `input_theta_dim + input_radius_dim` channels.

        Args:
            z (`torch.Tensor` of shape `(batch_size, max_seq_len, input_theta_dim)`):
                Input state in Cartesian coordinate
            theta (`torch.Tensor` of shape `(batch_size, max_seq_len, input_theta_dim)`):
                Input state in polar coordinate, angles
            radius (`torch.Tensor` of shape `(batch_size, max_seq_len, input_radius_dim)`):
                Input state in polar coordinate, radius, consider product manifold
            t (`torch.Tensor` of shape `(batch_size,)` or `(batch_size, 1)`):
                Per-example time values, optional
            return_radial (`bool`, *optional*, defaults to `False`):
                Also return the trunk's radial prediction.

        Returns:
            `torch.Tensor` of shape `(batch_size, max_seq_len, vocab_size)`:
                Vocabulary logits.
            `torch.Tensor` of shape `(batch_size, max_seq_len, output_radial_dim)`:
                if return_radial, the predicted radius
        """
        if z is not None and (theta is not None or radius is not None):
            raise ValueError(
                "Pass the state either as Cartesian z or as polar (theta, radius), not both."
            )
        if z is None and (theta is None or radius is None):
            raise ValueError(
                "The polar state needs BOTH theta and radius; got "
                f"theta={type(theta)}, radius={type(radius)}."
            )

        input = None
        if z is not None:
            input = z
        else:
            # The TRUNK is fed the dimensionless radius u = kappa*rho, so the
            # predictor is scale-equivariant (the Bayes posterior depends on
            # (theta, u), not on rho). horosphere_geometry below still receives
            # the intrinsic radius and applies kappa itself -- rescaling here
            # only, so the curvature is never applied twice.
            _, curvatures = self.prod_factors(
                prod_factor_dim=self.prod_factor_dim,
                prod_factor_gaussian_curvature=self.prod_factor_gaussian_curvature,
                embedding_size=theta.shape[-1],
            )
            kappas = radius.new_tensor(
                [1.0 / GeoUtils._curvature_scale(k) for k in curvatures]
            )
            input = torch.cat([theta, radius * kappas], dim=-1)

        output = self.model_forward(z=input, t=t)
        # The trunk emits the boundary features first and the radial channels
        # last; splitting by a positive index (rather than -output_radial_dim)
        # keeps output_radial_dim == 0 -- a model that predicts no radius -- from
        # slicing the features away entirely.
        split = output.shape[-1] - self.output_radial_dim
        if return_radial:
            return self.lm_head(output[..., :split]), output[..., split:]
        return self.lm_head(output[..., :split])

    @staticmethod
    def radius_conversion(
        radius: torch.Tensor,
        prod_factor_dim: Union[int, List[int]],
        prod_factor_gaussian_curvature: Union[float, List[float]],
    ):
        """
        Convert to radius on Poincare disk, consider product manifold

        Factor `i` has model radius `R_i = 1/sqrt(|K_i|)` and its intrinsic
        (geodesic) radial coordinate maps to the ball radius
        `R_i tanh(rho_i / 2 R_i)` -- the radial part of
        `GeoUtils.hyperbolic_polar_to_poincare_cartesian`, so the result is
        bounded by that factor's own ball radius. Scalar arguments describe the
        single-factor case.

        Args:
            radius (`torch.Tensor` of shape `(..., num_factors)`):
                Intrinsic radial coordinate of each product factor.
            prod_factor_dim (`int` or `List[int]`):
                Dimension of each factor. Only its length is used here; the
                conversion depends on the curvature alone.
            prod_factor_gaussian_curvature (`float` or `List[float]`):
                Curvature `K_i < 0` of each factor.

        Returns:
            `torch.Tensor` of shape `(..., num_factors)`:
                Poincare-ball radius of each factor.
        """
        if isinstance(prod_factor_dim, list) != isinstance(prod_factor_gaussian_curvature, list):
            raise TypeError(
                "prod_factor_dim and prod_factor_gaussian_curvature must both be "
                f"lists or both be scalars; got {type(prod_factor_dim)} and "
                f"{type(prod_factor_gaussian_curvature)}."
            )
        if not isinstance(prod_factor_dim, list):
            prod_factor_dim = [prod_factor_dim]
            prod_factor_gaussian_curvature = [prod_factor_gaussian_curvature]
        assert len(prod_factor_dim) == len(prod_factor_gaussian_curvature), (
            f"prod_factor_dim {prod_factor_dim} and prod_factor_gaussian_curvature "
            f"{prod_factor_gaussian_curvature} must have the same length."
        )
        assert radius.shape[-1] == len(prod_factor_dim), (
            f"radius must carry one radial coordinate per product factor "
            f"({len(prod_factor_dim)}); got {radius.shape[-1]}."
        )
        model_radius = radius.new_tensor(
            [GeoUtils._curvature_scale(k) for k in prod_factor_gaussian_curvature]
        )
        return model_radius * torch.tanh(radius / (2.0 * model_radius))

    def horosphere_geometry(
        self,
        theta: torch.Tensor,
        radius: torch.Tensor,
        prod_factor_dim: Optional[Union[int, List[int]]] = None,
        prod_factor_gaussian_curvature: Optional[Union[float, List[float]]] = None,
    ):
        """
        Horocycle distance (Poisson kernel) for each word embedding.

        `horosphere_dists[..., v] = sum_i -(d_i - 1) B^i_v(z_i)` -- `B^i_v` the
        Busemann function of word `v`'s boundary point in factor `i`. It is the
        log density of the bridge direction at word `v`, up to a `v`-independent
        constant, so `softmax(horosphere_dists + log p)` is exactly the Bayes
        posterior `q(y | z_t)`; the factors are independent Brownian motions, so
        their Busemann terms simply add. This is the product-manifold form of
        `HyperBridge.horosphere_geometry`, and every consumer of the naive logits
        must treat them as a RESIDUAL on top of this term.

        The half-angle form is the load-bearing one (Invariant 5):
        `cosh s - sinh s <u, phi_v> = e^{+s} sin^2(a_v/2) + e^{-s} cos^2(a_v/2)`,
        with `s = rho_i / R_i` the DIMENSIONLESS radial -- curvature enters only
        here, exactly as in `HyperbolicHeatKernel._angular_boost`. Pulling
        `e^{+s}` out of the log makes it overflow-free, the squared-difference
        forms are cancellation-free, and `clamp_min` keeps the log finite once
        both terms underflow (`s > ~372`, where `sin_half_sq` is exactly 0 for
        the target word). Computed in float64 per Invariant 3.

        Args:
            theta (`torch.Tensor` of shape `(batch_size, max_seq_len, input_theta_dim)`):
                Per-factor unit boundary directions, concatenated.
            radius (`torch.Tensor` of shape `(batch_size, max_seq_len, input_radius_dim)`):
                Intrinsic radial coordinate of each product factor.
            prod_factor_dim (`Union[int, List[int]]`, *optional*):
                Dimension of each factor; they must all be EQUAL here. Both
                lists `None` means the single factor `[embedding_size]` at
                `[-1.0]`.
            prod_factor_gaussian_curvature (`Union[float, List[float]]`, *optional*):
                Curvature `K_i < 0` of each factor, free to differ per factor.

        Returns:
            `torch.Tensor` of shape `(batch_size, max_seq_len, vocab_size)`:
                Horosphere (Busemann) log-densities, float64.
        """
        embedding = self.word_embedding
        if embedding is None:
            raise ValueError(
                f"{type(self).__name__}.word_embedding is None; the horosphere "
                "readout needs the per-word boundary directions. Every model on "
                "this path owns a table -- MLPLMRefactor's lm_head.weight, "
                "OptimalModelRefactor's frozen uniform_sphere_points buffer."
            )
        embedding = embedding.to(torch.float64)
        dims, curvatures = self.prod_factors(
            prod_factor_dim=prod_factor_dim,
            prod_factor_gaussian_curvature=prod_factor_gaussian_curvature,
            embedding_size=embedding.shape[-1],
        )
        if theta.shape[-1] != embedding.shape[-1]:
            raise ValueError(
                f"theta must carry one direction per factor, {embedding.shape[-1]} "
                f"channels in total; got {theta.shape[-1]}."
            )
        if radius.shape[-1] != len(dims):
            raise ValueError(
                f"radius must carry one radial coordinate per product factor "
                f"({len(dims)}); got {radius.shape[-1]}."
            )
        if len(set(dims)) != 1:
            raise ValueError(
                f"horosphere_geometry needs one shared factor dimension; got {dims}."
            )
        theta = theta.to(torch.float64)
        radius = radius.to(torch.float64)
        tiny = torch.finfo(torch.float64).tiny

        # No python loop over factors: one shared factor dimension splits the
        # concatenated boundary axis by a reshape, and the whole formula is
        # elementwise in the resulting factor axis, which the final sum
        # contracts away. Curvature stays per-factor, as the `kappas` vector.
        factor_dim, num_factors = dims[0], len(dims)
        # us: (..., 1, m, d) against phis: (V, m, d) -> (..., V, m, d)
        us = theta.unflatten(-1, (num_factors, factor_dim)).unsqueeze(-3)
        phis = embedding.unflatten(-1, (num_factors, factor_dim))
        phis = phis / phis.norm(dim=-1, p=2, keepdim=True).clamp_min(tiny)
        #   sin^2(a_v/2) = (1 - <u, phi_v>) / 2 = ||u - phi_v||^2 / 4
        #   cos^2(a_v/2) = (1 + <u, phi_v>) / 2 = ||u + phi_v||^2 / 4
        sin_half_sq = (us - phis).square().sum(-1) / 4
        cos_half_sq = (us + phis).square().sum(-1) / 4
        kappas = radius.new_tensor(
            [1.0 / GeoUtils._curvature_scale(k) for k in curvatures]
        )
        ss = (radius * kappas).unsqueeze(-2)
        return -(factor_dim - 1) * (
            ss + (
                sin_half_sq + cos_half_sq * (-2.0 * ss).exp()
            ).clamp_min(tiny).log()
        ).sum(-1)

    def forward_horosphere(
        self,
        z: torch.Tensor,
        theta: torch.Tensor,
        radius: torch.Tensor,
        prod_factor_dim: Optional[Union[int, List[int]]] = None,
        prod_factor_gaussian_curvature: Optional[Union[float, List[float]]] = None,
        t: Optional[torch.Tensor] = None,
        return_radial: bool=False
    ) -> Tuple[torch.Tensor]:
        """
        Predict vocabulary logits from a time-conditioned state.

        The returned logits ALREADY carry the horosphere geometry, i.e. they are
        the log-posterior up to a word-independent constant: `softmax` over them
        is the model's posterior over words. Unlike `forward_naive`'s residual
        logits they must not be corrected a second time (Invariant 1).

        Args:
            z (`torch.Tensor` of shape `(batch_size, max_seq_len, input_theta_dim)`):
                Input state in Cartesian coordinate
            theta (`torch.Tensor` of shape `(batch_size, max_seq_len, input_theta_dim)`):
                Input state in polar coordinate, angles
            radius (`torch.Tensor` of shape `(batch_size, max_seq_len, input_radius_dim)`):
                Input state in polar coordinate, radius on Poincare disk model, consider product manifold
            prod_factor_dim (`Union[int, List[int]]`, *optional*):
                Dimension of each factor. Both `None` falls back to the model's
                own `prod_factor_dim` / `prod_factor_gaussian_curvature`.
            prod_factor_gaussian_curvature (`Union[float, List[float]]`, *optional*):
                Curvature `K_i < 0` of each factor.
            t (`torch.Tensor` of shape `(batch_size,)` or `(batch_size, 1)`):
                Per-example time values, optional
            return_radial (`bool`, *optional*, defaults to `False`):
                Also return the trunk's radial prediction.

        Returns:
            `torch.Tensor` of shape `(batch_size, max_seq_len, vocab_size)`:
                Vocabulary logits, float64.
            `torch.Tensor` of shape `(batch_size, max_seq_len, output_radial_dim)`:
                if return_radial, the predicted radius
        """
        if theta is None or radius is None:
            raise ValueError(
                "The horosphere readout needs the polar state (theta, radius) to "
                "evaluate the Busemann terms."
            )
        pred_radius = None
        if return_radial:
            pred_logit, pred_radius = self.forward_naive(
                z=z, theta=theta, radius=radius, t=t, return_radial=True
            )
        else:
            pred_logit = self.forward_naive(
                z=z, theta=theta, radius=radius, t=t, return_radial=False
            )
        if prod_factor_dim is None and prod_factor_gaussian_curvature is None:
            prod_factor_dim = self.prod_factor_dim
            prod_factor_gaussian_curvature = self.prod_factor_gaussian_curvature
        horo_dist = self.horosphere_geometry(
            theta=theta,
            radius=radius,
            prod_factor_dim=prod_factor_dim,
            prod_factor_gaussian_curvature=prod_factor_gaussian_curvature,
        )
        pred_logit = pred_logit.to(horo_dist.dtype) + horo_dist

        if return_radial:
            return pred_logit, pred_radius
        return pred_logit

class MLPLMRefactor(HyperbolicModelBase):
    """`SmallMLP` backbone reading a product-manifold state.

    The sequence is flattened into one vector (as `MLPNLM` does), and the trunk
    emits `output_theta_dim` boundary features -- read out to vocabulary logits
    by `lm_head`, whose rows ARE the word embedding -- followed by
    `output_radial_dim` radial channels. `input_theta_dim`, `output_theta_dim`
    and `embedding_size` all name the boundary dimension `sum(prod_factor_dim)`,
    and `input_radial_dim` is the number of product factors.
    """

    def __init__(
        self,
        vocab_size: int,
        input_theta_dim: int,
        input_radial_dim: int,
        output_theta_dim: int,
        output_radial_dim: int,
        embedding_size: int,
        hidden_size: int,
        depth: int,
        max_seq_len: int=1,
        unif_word_embedding: bool = False,
        prod_factor_dim: Optional[List[int]] = None,
        prod_factor_gaussian_curvature: Optional[List[float]] = None,
    ):
        super().__init__()
        if not (input_theta_dim == output_theta_dim == embedding_size):
            raise ValueError(
                "input_theta_dim, output_theta_dim and embedding_size all name the "
                f"boundary dimension and must agree; got {input_theta_dim}, "
                f"{output_theta_dim}, {embedding_size}."
            )
        dims, _ = self.prod_factors(
            prod_factor_dim=prod_factor_dim,
            prod_factor_gaussian_curvature=prod_factor_gaussian_curvature,
            embedding_size=embedding_size,
        )
        if input_radial_dim != len(dims):
            raise ValueError(
                f"input_radial_dim must be one radial coordinate per product factor "
                f"({len(dims)}); got {input_radial_dim}."
            )
        self.mlp = SmallMLP(
            # +1: SmallMLP concatenates the scalar time onto its input.
            input_dim=(input_theta_dim + input_radial_dim) * max_seq_len + 1,
            hidden_size=hidden_size,
            depth=depth,
            output_dim=(output_theta_dim + output_radial_dim) * max_seq_len,
        )

        self.vocab_size: int = vocab_size
        self.input_theta_dim: int = input_theta_dim
        self.input_radial_dim: int = input_radial_dim
        self.output_theta_dim: int = output_theta_dim
        self.output_radial_dim: int = output_radial_dim
        self.embedding_size: int = embedding_size
        self.hidden_size: int = hidden_size
        self.depth: int = depth
        self.max_seq_len: int = max_seq_len
        self.unif_word_embedding: bool = unif_word_embedding
        self.prod_factor_dim: Optional[Union[int, List[int]]] = prod_factor_dim
        self.prod_factor_gaussian_curvature: Optional[Union[float, List[float]]] = prod_factor_gaussian_curvature

        self.lm_head = nn.Linear(embedding_size, vocab_size, bias=False)
        if unif_word_embedding:
            # lm_head.weight IS the word embedding the bridge and loss read: each
            # row's direction is that word's boundary angle phi_v = atan2(e_v)
            # (see HyperbolicDLM.word_embedding / HyperBridge._binary_vocab_angles).
            # nn.Linear's default kaiming-uniform init leaves those angles badly
            # clustered, so spread them evenly instead.
            with torch.no_grad():
                self.lm_head.weight.copy_(
                    uniform_sphere_points(vocab_size, embedding_size).to(self.lm_head.weight.dtype)
                )

    @property
    def word_embedding(self) -> torch.Tensor:
        # The lm_head weight IS the boundary embedding: row v is word v's
        # direction, so the shape contract is (vocab_size, output_dim) -- the
        # (V, 2) that _binary_vocab_angles / the polar losses assert.
        return self.lm_head.weight

    def model_forward(
        self,
        z: torch.Tensor,
        t: torch.Tensor,
    ):
        """
        Flatten the sequence, run the trunk, restore the sequence axis.

        Args:
            z (`torch.Tensor` of shape `(batch_size, max_seq_len, input_theta_dim + input_radial_dim)`):
                Input state in the coordinates `forward_naive` assembled.
            t (`torch.Tensor` of shape `(batch_size,)` or `(batch_size, 1)`):
                Per-example time values.

        Returns:
            `torch.Tensor` of shape `(batch_size, max_seq_len, output_theta_dim + output_radial_dim)`:
                Boundary features followed by the radial channels.
        """
        # t is optional: given (theta, u) the Bayes posterior needs no time
        # (OptimalModelRefactor ignores t outright), and conditioning on the
        # physical t would break scale-equivariance. None => constant channel.
        if t is None:
            t = torch.zeros(z.shape[0], dtype=z.dtype, device=z.device)
        if z.ndim != 3 or z.shape[1] != self.max_seq_len:
            raise ValueError(
                f"z must have shape (batch_size, {self.max_seq_len}, channels); "
                f"got {tuple(z.shape)}."
            )
        # The state is float64 (Invariant 3) while the trunk is float32, so the
        # cast happens here, at the boundary between the geometry and the model.
        dtype = self.lm_head.weight.dtype
        output = self.mlp(z=z.flatten(1).to(dtype), t=t.to(dtype))
        return output.reshape(z.shape[0], self.max_seq_len, -1)

class OptimalModelRefactor(HyperbolicModelBase):
    """Bayes-optimal unigram model on a product of Poincare balls.

    Forward returns log-prior logits broadcast over the batch — these are the
    optimal logits for the bridge losses, since
    `softmax(horosphere_dists + log_ps)` recovers the true posterior
    q(y | x_t) ∝ p(y) · prod_i (Poisson kernel)_i. Nothing is trained, so the
    trunk is a constant and `lm_head` is the identity, and the boundary table is
    a frozen `uniform_sphere_points` draw held as a buffer -- not a Parameter,
    so it never takes a gradient, and it is the same table the bridge and the
    loss use for their own reference geometry.
    """

    def __init__(
        self,
        ps,
        embedding_size: int,
        prod_factor_dim: Optional[List[int]] = None,
        prod_factor_gaussian_curvature: Optional[List[float]] = None,
    ):
        super().__init__()
        ps = torch.as_tensor(ps, dtype=torch.float64)
        self.register_buffer("log_ps", (ps / ps.sum()).log())
        self.vocab_size: int = self.log_ps.numel()
        self.embedding_size: int = embedding_size
        # forward_naive's contract: the trunk output IS the logit vector (no
        # projection) and no trailing channel is a predicted radius.
        self.lm_head = nn.Identity()
        self.output_radial_dim: int = 0
        self.prod_factor_dim: Optional[Union[int, List[int]]] = prod_factor_dim
        self.prod_factor_gaussian_curvature: Optional[Union[float, List[float]]] = prod_factor_gaussian_curvature
        self.prod_factors(
            prod_factor_dim=prod_factor_dim,
            prod_factor_gaussian_curvature=prod_factor_gaussian_curvature,
            embedding_size=embedding_size,
        )
        # Frozen boundary table: unit rows spread uniformly over the sphere, the
        # same draw HyperBridge._vocab_angles falls back to, so the reference
        # model's geometry matches the bridge's word -> direction map exactly. A
        # buffer, so .to(device) carries it and no optimizer ever sees it.
        self.register_buffer(
            "_word_embedding",
            uniform_sphere_points(self.vocab_size, embedding_size, dtype=torch.float64),
        )
        print(f"self.ps: {self.log_ps.exp()}")
        print(f"self.log_ps: {self.log_ps}")

    @property
    def word_embedding(self) -> torch.Tensor:
        # (vocab_size, embedding_size), frozen. Same row-per-word contract as
        # MLPLMRefactor's lm_head.weight.
        return self._word_embedding

    def model_forward(
        self,
        z: torch.Tensor,
        t: torch.Tensor,
    ) -> torch.Tensor:
        """
        Evaluate the Bayes-optimal logits.

        Only `z`'s leading shape is used; the coordinates themselves are ignored
        because the optimal logits are just `log p(y)` (the per-`x_t` Poisson
        kernel is supplied by `horosphere_geometry`, or by the loss).

        Args:
            z (`torch.Tensor` of shape `(batch_size, max_seq_len, input_theta_dim)`):
                Input state in Cartesian coordinate
            t (`torch.Tensor` of shape `(batch_size,)` or `(batch_size, 1)`):
                Time values. Ignored.

        Returns:
            `torch.Tensor` of shape `(batch_size, max_seq_len, vocab_size)`:
                Log-prior logits, broadcast to match the leading batch shape.
        """
        del t
        leading_shape = z.shape[:-1]
        return self.log_ps.to(dtype=torch.float32).expand(*leading_shape, -1)

class MLPLM(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        input_dim: int,
        output_dim: int,
        hidden_size: int,
        depth: int,
        unif_word_embedding: bool = False,
    ):
        super().__init__()
        self.mlp = SmallMLP(
            input_dim=input_dim + 1,
            hidden_size=hidden_size,
            depth=depth,
            output_dim=output_dim,
        )

        self.lm_head = nn.Linear(output_dim, vocab_size, bias=False)
        if unif_word_embedding:
            # lm_head.weight IS the word embedding the bridge and loss read: each
            # row's direction is that word's boundary angle phi_v = atan2(e_v)
            # (see HyperbolicDLM.word_embedding / HyperBridge._binary_vocab_angles).
            # nn.Linear's default kaiming-uniform init leaves those angles badly
            # clustered, so spread them evenly instead.
            with torch.no_grad():
                self.lm_head.weight.copy_(
                    uniform_sphere_points(vocab_size, output_dim).to(self.lm_head.weight.dtype)
                )
    @property
    def word_embedding(self) -> torch.Tensor:
        # The lm_head weight IS the boundary embedding: row v is word v's
        # direction, so the shape contract is (vocab_size, output_dim) -- the
        # (V, 2) that _binary_vocab_angles / the polar losses assert.
        return self.lm_head.weight

    def forward(self, z: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        """
        Predict vocabulary logits from a time-conditioned state.

        Args:
            z (`torch.Tensor` of shape `(batch_size, input_dim)`):
                Input state.
            t (`torch.Tensor` of shape `(batch_size,)` or `(batch_size, 1)`):
                Per-example time values.

        Returns:
            `torch.Tensor` of shape `(batch_size, vocab_size)`:
                Vocabulary logits.
        """
        return self.lm_head(self.mlp(z=z, t=t))

class MLPNLM(nn.Module):
    """Tiny time-conditioned MLP language model with a weight-tied embedding table.

    Flattens a fixed-length token sequence into a single vector, passes it through
    one `SmallMLP` conditioned on a scalar time, and reshapes the output back to
    per-position embeddings. Vocabulary logits are produced by projecting through
    the same embedding table used at the input (weight tying), so freezing the
    table freezes the lm-head too.

    Args:
        vocab_size: Vocabulary size.
        embedding_size: Word-embedding dimension.
        max_length: Fixed sequence length consumed by the model.
        hidden_size: Width of each hidden layer in the inner `SmallMLP`.
        depth: Number of hidden layers in the inner `SmallMLP`.
        word_embedding: Optional `(vocab_size, embedding_size)` table used to
            initialize the embedding. Frozen unless `trainable_word_embedding`.
        trainable_word_embedding: If True the embedding table is trainable;
            otherwise it is frozen.

    Returns:
        From `forward`: a tuple `(predicted_embedding, logits)` where
        `predicted_embedding` has shape `(batch, max_length, embedding_size)` and
        `logits` has shape `(batch, max_length, vocab_size)`.
    """

    def __init__(
        self,
        vocab_size: int,
        embedding_size: int,
        max_length: int,
        hidden_size: int,
        depth: int,
        word_embedding: Optional[torch.FloatTensor] = None,
        trainable_word_embedding: bool = False,
        norm_word_embedding: bool = False,
        unif_word_embedding: bool = False,
    ):
        super().__init__()
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        self.max_length = max_length

        if word_embedding is not None:
            if unif_word_embedding:
                raise ValueError(f"unif_word_embedding should be false while word_embedding is provided.")
            if tuple(word_embedding.shape) != (vocab_size, embedding_size):
                raise ValueError(
                    f"word_embedding must have shape ({vocab_size}, {embedding_size}); "
                    f"got {tuple(word_embedding.shape)}"
                )
            self.embedding = nn.Embedding.from_pretrained(word_embedding)
        else:
            if unif_word_embedding:
                # Words spread uniformly over the unit sphere in R^embedding_size.
                unif_embedding = uniform_sphere_points(vocab_size, embedding_size)
                self.embedding = nn.Embedding.from_pretrained(unif_embedding)
            else:
                self.embedding = nn.Embedding(vocab_size, embedding_size)

        if norm_word_embedding:
            self.embedding.weight = torch.norm(self.embedding.weight, p=2, dim=-1)
        if trainable_word_embedding:
            self.embedding.weight.requires_grad = trainable_word_embedding

        self.mlp = SmallMLP(
            input_dim=max_length * embedding_size + 1,
            hidden_size=hidden_size,
            depth=depth,
            output_dim=max_length * embedding_size,
        )

    @property
    def word_embedding(self) -> torch.Tensor:
        # (vocab_size, embedding_size), same row-per-word contract as MLPLM.
        return self.embedding.weight

    def normalize_word_embedding(self) -> torch.Tensor:
        """Return the embedding table with each row rescaled to unit L2-norm.

        Returns:
            `torch.Tensor` of shape `(vocab_size, embedding_size)`.
        """
        w = self.embedding.weight
        return w / w.norm(dim=-1, keepdim=True, p=2).clamp_min(1e-12)

    def forward(
        self,
        ids: torch.LongTensor,
        t: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Predict per-position embeddings and vocabulary logits.

        Args:
            ids (`torch.LongTensor` of shape `(batch, max_length)`):
                Token ids.
            t (`torch.Tensor` of shape `(batch,)` or `(batch, 1)`):
                Per-example time values.

        Returns:
            `tuple[torch.Tensor, torch.Tensor]`:
                `predicted_embedding` of shape `(batch, max_length, embedding_size)`
                and `logits` of shape `(batch, max_length, vocab_size)`.
        """
        if ids.shape[1] != self.max_length:
            raise ValueError(
                f"ids must have shape (batch, {self.max_length}); got {tuple(ids.shape)}"
            )
        batch = ids.shape[0]
        e = self.embedding(ids)
        z = e.reshape(batch, self.max_length * self.embedding_size)
        out = self.mlp(z, t)
        predicted_embedding = out.reshape(batch, self.max_length, self.embedding_size)
        logits = predicted_embedding @ self.embedding.weight.T
        return predicted_embedding, logits

def polar_to_cart(rho: torch.Tensor, theta: torch.Tensor) -> torch.Tensor:
    """
    Map polar disk coordinates to Cartesian disk coordinates.

    Args:
        rho (`torch.Tensor` of shape `(...,)`):
            Radial coordinates.
        theta (`torch.Tensor` of shape `(...,)`):
            Angular coordinates.

    Returns:
        `torch.Tensor` of shape `(..., 2)`:
            Cartesian coordinates. For example, if `rho` and `theta`
            have shape `(256,)`, the output has shape `(256, 2)`.
    """
    r = torch.tanh(rho / 2)
    return torch.stack([r * theta.cos(), r * theta.sin()], dim=-1)

def vocab_points(V: int, device: Union[str, torch.device], dtype) -> torch.Tensor:
    """
    Construct evenly spaced vocabulary anchor points on the unit circle.

    Args:
        V (`int`):
            Vocabulary size.
        device (`str` or `torch.device`):
            Device for the returned tensor.
        dtype:
            Tensor dtype for the returned tensor.

    Returns:
        `torch.Tensor` of shape `(V, 2)`:
            Vocabulary anchor points in Cartesian coordinates. Internally,
            `phi` has shape `(V,)`. For example, when `V = 2`, `phi` has
            shape `(2,)` and the returned tensor has shape `(2, 2)`.
    """
    phi = (torch.arange(V, device=device, dtype=dtype) + 0.5) * (2 * math.pi / V)
    return torch.stack([phi.cos(), phi.sin()], dim=-1)

def uniform_sphere_points(
    V: int,
    d: int,
    device: Union[str, torch.device] = "cpu",
    dtype=torch.float32,
    seed: int = 0,
) -> torch.Tensor:
    """
    Construct `V` unit vectors spread uniformly over the unit sphere in `R^d`.

    For `d == 2` the evenly spread configuration is known in closed form -- the
    equally spaced angles `(v + 0.5) * 2*pi / V` of `vocab_points` -- and is
    used directly, so the 2-D case reproduces the fixed angles the loss falls
    back to (see `HyperBridge._binary_vocab_angles` with `word_embedding=None`). For
    `d > 2` no exact even packing exists for general `V`, so the rows are drawn
    uniformly from the sphere by normalizing isotropic Gaussians: exact in
    distribution, `O(V*d)`, and seeded so the table is reproducible.

    Args:
        V (`int`):
            Number of points (vocabulary size).
        d (`int`):
            Ambient dimension; the points lie on the `(d-1)`-sphere.
        device (`str` or `torch.device`, *optional*, defaults to `"cpu"`):
            Device for the returned tensor.
        dtype (*optional*, defaults to `torch.float32`):
            Dtype for the returned tensor.
        seed (`int`, *optional*, defaults to `0`):
            Seed for the `d > 2` draw. Unused when `d == 2`.

    Returns:
        `torch.Tensor` of shape `(V, d)`:
            Unit-norm rows. For example, `V = 10`, `d = 4` returns shape
            `(10, 4)` with every row satisfying `||x|| = 1`.
    """
    if V < 1:
        raise ValueError(f"V must be >= 1; got {V}")
    if d < 2:
        raise ValueError(f"d must be >= 2; got {d}")
    if d == 2:
        return vocab_points(V, device=device, dtype=dtype)
    generator = torch.Generator().manual_seed(seed)
    x = torch.randn(V, d, generator=generator, dtype=torch.float64)
    x = x / x.norm(dim=-1, keepdim=True).clamp_min(1e-12)
    return x.to(device=device, dtype=dtype)

def poisson_posterior(
    x: torch.Tensor,
    v: torch.Tensor,
    log_ps: torch.Tensor,
    d: int = 2,
) -> torch.Tensor:
    """
    Compute the posterior expectation E_{y|x_t}[(y - x_t) / |y - x_t|^2].

    \mathbb{E}_{y | x_t} \left[ \frac{y - x_t}{||y-x_t ||^2} \right] 
        = \frac{1}{A_{d-1}} \left( 
            \sum_{y \in V} \left( 
                \frac{1 - \|x_t\|^2}{\|x_t - y\|^2} 
            \right)^{d-1} 
                \frac{y - x_t}{||y-x_t ||^2} 
        \right)

    Follow Bayes rule, q(y | x_t) = \frac{q(y) q(x_t | y)}{q(x_t)}
    The posterior is q(y | x_t) propto p(y) * |y - x_t|^{-2(d-1)}; the
    y-independent (1 - |x_t|^2)^{d-1} factor cancels in normalization.

    Args:
        x (`torch.Tensor` of shape `(..., d)`):
            Cartesian disk coordinates for the current state.
        v (`torch.Tensor` of shape `(V, d)`):
            Vocabulary anchor points.
        log_ps (`torch.Tensor` of shape `(V,)`):
            Log prior probabilities over the vocabulary.
        d (`int`, *optional*, defaults to `2`):
            Hyperbolic space dimension parameter in the Poisson kernel.

    Returns:
        `torch.Tensor` of shape `(..., d)`:
            Posterior expectation of (y - x_t) / |y - x_t|^2.
    """
    # x.unsqueeze(-2): (B, 1, d)
    # diff: (B, V, d), Broadcast x along with -2 dimension and compute difference
    diff = v - x.unsqueeze(-2)
    # sq: (B, V)
    sq = diff.square().sum(-1)
    # mu: (B, V)
    mu = (log_ps - (d - 1) * sq.log()).softmax(-1)
    # Weighted sum
    # (mu / sq).unsqueeze(-1): (B, V, 1)
    # (mu / sq).unsqueeze(-1).mul(diff): (B, V, d)
    # (mu / sq).unsqueeze(-1).mul(diff).sum(-2): (B, d)
    return (mu / sq).unsqueeze(-1).mul(diff).sum(-2)

def poisson_posterior_new(
    x: torch.Tensor,
    v: torch.Tensor,
    log_ps: torch.Tensor,
    d: int = 2,
) -> torch.Tensor:
    """
    Alternative Poisson-kernel posterior implementation.

    Args:
        x (`torch.Tensor` of shape `(..., 2)`):
            Cartesian disk coordinates for the current state.
        v (`torch.Tensor` of shape `(V, 2)`):
            Vocabulary anchor points.
        log_ps (`torch.Tensor` of shape `(V,)`):
            Log prior probabilities over the vocabulary.
        d (`int`, *optional*, defaults to `2`):
            Hyperbolic space dimension parameter in the Poisson kernel.

    Returns:
        `torch.Tensor` of shape `(..., V)`:
            Posterior probabilities over the vocabulary. As above,
            `sq = |v - x|^2` has shape `(..., V)`.
    """
    sq = (v - x.unsqueeze(-2)).square().sum(-1)
    return (log_ps - (d - 1) * sq.log()).softmax(-1)

def bridge_drift(
    x: torch.Tensor,
    expectation: torch.Tensor,
    d: int = 2,
) -> torch.Tensor:
    """
    Compute the Bayes-optimal bridge drift field.

    Args:
        x (`torch.Tensor` of shape `(..., d)`):
            Cartesian disk coordinates for the current state.
        expectation (`torch.Tensor` of shape `(..., d)`):
            Posterior expectation E_{y|x_t}[(y - x_t) / |y - x_t|^2], as
            returned by `poisson_posterior`.
        d (`int`, *optional*, defaults to `2`):
            Hyperbolic space dimension parameter.

    Returns:
        `torch.Tensor` of shape `(..., d)`:
            Drift vectors in Cartesian coordinates.
    """
    g2 = 1 - x.square().sum(-1, keepdim=True)
    return (d - 1) / 2 * g2.square() * expectation - d / 4 * g2 * x

class OptimalModel(nn.Module):
    """Bayes-optimal unigram model on D^2.

    Forward returns log-prior logits broadcast over the batch — these are the
    optimal logits for `binary_bridge_loss`, since
    `softmax(horosphere_dists + log_ps)` recovers the true posterior
    q(y | x_t) ∝ p(y) · |y - x_t|^{-2(d-1)} for d=2 (the (1-|x_t|^2) factor
    cancels in normalization). Use `optimal_drift` if you need the
    bridge-drift form instead (e.g., for the visualizer).
    """

    def __init__(self, ps):
        super().__init__()
        ps = torch.as_tensor(ps, dtype=torch.float64)
        self.register_buffer("log_ps", (ps / ps.sum()).log())
        print(f"self.ps: {self.log_ps.exp()}")
        print(f"self.log_ps: {self.log_ps}")

    @property
    def word_embedding(self) -> Optional[torch.Tensor]:
        return None

    def forward(self, z: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        """
        Evaluate the Bayes-optimal logits.

        Args:
            z (`torch.Tensor` of shape `(..., 2)`):
                Polar disk coordinates `(rho, theta)`. Only the leading shape
                is used; coordinates themselves are ignored because the
                optimal logits are just `log p(y)` (the per-`x_t` Poisson
                kernel is supplied by the loss via horosphere distances).
            t (`torch.Tensor`):
                Time values. Ignored.

        Returns:
            `torch.Tensor` of shape `(..., V)`:
                Log-prior logits, broadcast to match the leading batch shape.
        """
        del t
        leading_shape = z.shape[:-1]
        return self.log_ps.to(dtype=torch.float32).expand(*leading_shape, -1)

    def optimal_drift(self, z: torch.Tensor) -> torch.Tensor:
        """
        Closed-form Bayes-optimal bridge drift in Cartesian coordinates.

        Args:
            z (`torch.Tensor` of shape `(..., 2)`):
                Polar disk coordinates `(rho, theta)`.

        Returns:
            `torch.Tensor` of shape `(..., 2)`:
                Bridge drift evaluated under the true posterior.
        """
        z = z.double()
        x = polar_to_cart(z[..., 0], z[..., 1])
        v = vocab_points(self.log_ps.numel(), z.device, z.dtype)
        expectation = poisson_posterior(x, v, self.log_ps)
        return bridge_drift(x, expectation).float()

def get_model(
    model_type: str,
    ps: str = None,
    vocab_size: int = None,
    input_dim: int = None,
    output_dim: int = None,
    hidden_size: int = None,
    depth: int = None,
    unif_word_embedding: bool = True,
):
    if model_type == "opt":
        return OptimalModel(ps=ps)
    elif model_type == "tnb":
        return MLPLM(
            vocab_size=vocab_size,
            input_dim=input_dim,
            output_dim=output_dim,
            hidden_size=hidden_size,
            depth=depth,
            unif_word_embedding=unif_word_embedding,
        )
    else:
        raise ValueError(f"model_type {model_type} is not supported.")