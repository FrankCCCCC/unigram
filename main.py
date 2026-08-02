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

    @staticmethod
    def sample_chi_old(ns,dtype=torch.float64):
        nshape = ns.shape
        ns = ns.reshape(-1)
        M = ns.sum().item()
        x = torch.randn(M, device=ns.device, dtype=dtype).square()
        chi2 = torch.segment_reduce(x,'sum',lengths=ns)
        return chi2.sqrt().reshape(nshape)

    @staticmethod
    def binary_bridge_old(ts):
        ns = torch.poisson(ts/8).to(torch.int64)
        ss = ts.sqrt() * HyperBridge.sample_chi(2*ns+3, ts.dtype)
        vs = torch.rand_like(ts)
        ps = torch.acosh(vs.square() + (1-vs.square())*torch.cosh(ss))
        us = torch.rand_like(ts)
        thetas = 2 * torch.atan((-ps).exp() * torch.tan(torch.pi * (us - 0.5)))
        return (ps,thetas)

    @staticmethod
    def _vocab_angles(
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
    def rotate_with_target(
        thetas: torch.FloatTensor,
        targets: torch.LongTensor,
        vocab_size: int,
        word_embedding: Optional[torch.FloatTensor] = None,
    ):
        # Rotate the spike (at angle 0) onto each target word's boundary angle,
        # using the same word->angle map the loss uses (see _vocab_angles).
        phis = HyperBridge._vocab_angles(
            vocab_size=vocab_size,
            device=thetas.device,
            dtype=thetas.dtype,
            word_embedding=word_embedding,
        )
        return thetas + phis[targets]

    @staticmethod
    def binary_bridge(
        ts,
        targets: torch.LongTensor,
        vocab_size: int,
        word_embedding: Optional[torch.FloatTensor] = None,
    ):
        # Radial sampling
        ns = torch.poisson(ts/8).to(torch.int64)
        ss = ts.sqrt() * HyperBridge.sample_chi(2*ns+3, ts.dtype)
        vs = torch.rand_like(ts)
        ps = torch.acosh(vs.square() + (1-vs.square())*torch.cosh(ss))

        # Free angles
        us = torch.rand_like(ts)
        # Spike angle on 0
        thetas = 2 * torch.atan((-ps).exp() * torch.tan(torch.pi * (us - 0.5)))

        thetas = HyperBridge.rotate_with_target(
            thetas=thetas,
            targets=targets,
            vocab_size=vocab_size,
            word_embedding=word_embedding,
        )
        return ps, thetas

    @staticmethod
    def binary_bridge_loss_poincare_disk_polar(logits, targets, rhos, thetas, word_embedding=None):
        (N,) = targets.shape
        (N,V) = logits.shape
        device = rhos.device
        assert(rhos.shape == (N,))
        assert(thetas.shape == (N,))
        assert(targets.dtype == torch.int64)
        assert(rhos.dtype == torch.float64)
        assert(thetas.dtype == torch.float64)
        assert word_embedding is None or tuple(word_embedding.shape) == (V, 2)
        # phi_v for every vocab word: learnable embedding angles when given,
        # otherwise the equally spaced points used by the *_old variant.
        phis = HyperBridge._vocab_angles(
            vocab_size=V,
            device=device,
            dtype=torch.float64,
            word_embedding=word_embedding,
        )
        # first, we get the horosphere distances
        # print(f"thetas ({thetas.mean().item()}): {torch.isfinite(thetas).all().item()}")
        # print(f"phis ({phis.mean().item()}): {torch.isfinite(phis).all().item()}")
        alphas = thetas[:,None] - phis[None,:]  # angular offsets between z and v
        # print(f"alphas: {torch.isfinite(alphas).all().item()}")
        cos_alphas = alphas.cos()
        sin_alphas = alphas.sin()
        log_two = torch.log(torch.tensor(2.0, device=device, dtype=torch.float64))
        # print(f"cos_alphas ({cos_alphas.mean().item()}): {torch.isfinite(cos_alphas).all().item()}")
        # print(f"sin_alphas ({sin_alphas.mean().item()}): {torch.isfinite(sin_alphas).all().item()}")
        # print(f"1 - cos_alphas ({(1 - cos_alphas).mean().item()}): {torch.isfinite(1 - cos_alphas).all().item()}")
        # print(f"1 + cos_alphas ({(1 + cos_alphas).mean().item()}): {torch.isfinite(1 + cos_alphas).all().item()}")
        horosphere_dists = log_two - torch.logaddexp((1 - cos_alphas).log() + rhos[:,None], (1 + cos_alphas).log() - rhos[:,None])
        # remake mu and subtract the target
        mu = (horosphere_dists + logits.to(torch.float64)).softmax(-1)
        mu = mu - torch.nn.functional.one_hot(targets,V).to(torch.float64)
        # next, we transform the angles alpha after motion by rho
        betas = torch.atan2(sin_alphas, rhos.cosh()[:,None] * cos_alphas - rhos.sinh()[:,None])
        cos_errors = (betas.cos() * mu).sum(-1)
        sin_errors = (betas.sin() * mu).sum(-1)
        return (cos_errors.square() + sin_errors.square())/2

    @staticmethod
    def binary_bridge_loss_poincare_disk_polar_horocycle(logits, targets, rhos, thetas, word_embedding=None):
        (N,) = targets.shape
        (N,V) = logits.shape
        device = rhos.device
        assert(rhos.shape == (N,))
        assert(thetas.shape == (N,))
        assert(targets.dtype == torch.int64)
        assert(rhos.dtype == torch.float64)
        assert(thetas.dtype == torch.float64)
        assert word_embedding is None or tuple(word_embedding.shape) == (V, 2)
        # phi_v for every vocab word: learnable embedding angles when given,
        # otherwise the equally spaced points used by the *_old variant.
        phis = HyperBridge._vocab_angles(
            vocab_size=V,
            device=device,
            dtype=torch.float64,
            word_embedding=word_embedding,
        )
        # first, we get the horosphere distances
        # print(f"thetas ({thetas.mean().item()}): {torch.isfinite(thetas).all().item()}")
        # print(f"phis ({phis.mean().item()}): {torch.isfinite(phis).all().item()}")
        alphas = thetas[:,None] - phis[None,:]  # angular offsets between z and v
        # print(f"alphas: {torch.isfinite(alphas).all().item()}")
        cos_alphas = alphas.cos()
        sin_alphas = alphas.sin()
        # remake mu and subtract the target
        mu = logits.to(torch.float64).softmax(-1)
        mu = mu - torch.nn.functional.one_hot(targets,V).to(torch.float64)
        # next, we transform the angles alpha after motion by rho
        betas = torch.atan2(sin_alphas, rhos.cosh()[:,None] * cos_alphas - rhos.sinh()[:,None])
        cos_errors = (betas.cos() * mu).sum(-1)
        sin_errors = (betas.sin() * mu).sum(-1)
        return (cos_errors.square() + sin_errors.square())/2

    # ---- Cartesian bridge loss ----------------------------------------------
    # Implements the formula directly, term-by-term:
    #   L(theta; y) = (d-1)^2 / 2 * (1 - ||z_t||^2)^2
    #                 * ||  (y - z_t) / ||y - z_t||^2
    #                     - E_{v ~ mu^theta(.|z_t)}[ (v - z_t) / ||v - z_t||^2 ]  ||^2
    # with mu^theta_v(z_t) = softmax_v( (d-1) h(z_t, v) + logits_v ),
    #      h(z_t, v)       = log[ (1 - ||z_t||^2) / ||v - z_t||^2 ].
    # The "_weighted" variant replaces the target (y - z_t)/||y - z_t||^2 with
    # E_{v ~ mu^*(.|z_t)}[(v - z_t)/||v - z_t||^2], where mu^* is the true Bayes
    # posterior softmax((d-1) h + log_ps).

    @staticmethod
    def _poincare_disk_cartesian_geometry(rhos, thetas, V):
        """Returns (z, v, diff, sq, one_minus_zz, h) used by every variant."""
        z = polar_to_cart(rhos, thetas)                                  # (N, 2)
        v = vocab_points(V, rhos.device, rhos.dtype)                     # (V, 2)
        diff = v - z.unsqueeze(-2)                                       # (N, V, 2)
        sq   = diff.square().sum(-1)                                     # (N, V)
        one_minus_zz = 1 - z.square().sum(-1, keepdim=True)              # (N, 1)
        h    = (one_minus_zz / sq).log()                                 # (N, V)
        return z, v, diff, sq, one_minus_zz, h

    @staticmethod
    def _poincare_disk_expected_radial(mu, diff, sq):
        """E_{v ~ mu}[ (v - z) / ||v - z||^2 ]  =  sum_v mu_v (v-z)/||v-z||^2."""
        return (mu / sq).unsqueeze(-1).mul(diff).sum(-2)                 # (N, 2)

    @staticmethod
    def _poincare_disk_cartesian_squared_residual(target, model, one_minus_zz, d=2):
        """L = (d-1)^2 / 2 * (1 - ||z||^2)^2 * ||target - model||^2."""
        residual = target - model                                        # (N, 2)
        return (d - 1) ** 2 / 2 * one_minus_zz.squeeze(-1).square() \
               * residual.square().sum(-1)

    @staticmethod
    def binary_bridge_loss_poincare_disk_cartesian(logits, targets, rhos, thetas):
        V, d = logits.shape[-1], 2
        z, v, diff, sq, one_minus_zz, h = HyperBridge._poincare_disk_cartesian_geometry(rhos, thetas, V)

        # target term: (y - z) / ||y - z||^2
        y_minus_z = v[targets] - z                                       # (N, 2)
        target = y_minus_z / y_minus_z.square().sum(-1, keepdim=True)    # (N, 2)

        # model term: E_{v ~ mu^theta(.|z)}[ (v - z) / ||v - z||^2 ]
        mu = ((d - 1) * h + logits.to(torch.float64)).softmax(-1)        # (N, V)
        model = HyperBridge._poincare_disk_expected_radial(mu, diff, sq)               # (N, 2)

        return HyperBridge._poincare_disk_cartesian_squared_residual(target, model, one_minus_zz, d=d)

    @staticmethod
    def _lorentz_boundary_points(V, device, dtype):
        phis = (torch.arange(V, device=device, dtype=dtype) + 0.5) * (2 * torch.pi / V)
        return torch.stack([torch.ones_like(phis), phis.cos(), phis.sin()], dim=-1)

    @staticmethod
    def _lorentz_inner(x, y):
        return -x[..., 0] * y[..., 0] + (x[..., 1:] * y[..., 1:]).sum(-1)

    @staticmethod
    def _lorentz_geometry(rhos, thetas, V, d):
        z = HyperBridge.polar_to_lorentz(rhos, thetas)                   # (N, d+1)
        xi = HyperBridge._lorentz_boundary_points(V, rhos.device, rhos.dtype)
        inner = HyperBridge._lorentz_inner(z[:, None, :], xi[None, :, :]) # (N, V), negative
        log_poisson = (d - 1) *  (-(-inner).clamp_min(1e-300).log())     # (d - 1) * log 1 / (-<z,xi(y)>)
        directions = xi[None, :, :] / inner[:, :, None]                  # xi(y) / <z,xi(y)>
        return directions, log_poisson

    @staticmethod
    def _lorentz_norm_sq(x):
        return HyperBridge._lorentz_inner(x, x).clamp_min(0)

class Loss:
    @staticmethod
    def binary_bridge_loss_crossentropy(logits, targets, rhos, thetas):
        return torch.nn.functional.cross_entropy(logits, targets, reduction='none')

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
            bridge = HyperBridge.binary_bridge_loss_crossentropy(
                logits=logits,
                targets=targets,
                rhos=rhos,
                thetas=thetas,
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

        ts, proposal_weight = HyperBridge.proposal(
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

class HyperbolicDLM(L.LightningModule):
    def __init__(self, config: DictConfig):
        super().__init__()
        self.config = config

    def get_logits_inputs(
        self,
        batch_size: int,
        targets: torch.LongTensor,
        hyper_dt: float,
        hyper_T: int,
        proposal_type: str,
        proposal_exp_rate: float,
        vocab_size: int,
        word_embedding: Optional[torch.FloatTensor],
        device: torch.device,
        generator: Optional[torch.Generator] = None,
    ):
        ts, proposal_weight = self.bridge.hyper_proposal(
            proposal_type=proposal_type,
            shape=(batch_size,),
            device=device,
            dtype=torch.float64,
            dt=hyper_dt,
            T=hyper_T,
            exp_rate=proposal_exp_rate,
            generator=generator,
        )

        # For calculating posterior
        # Case 1: The word embedding is Equally divided around the circle
        # rhos, thetas = self.bridge.binary_bridge(ts=ts)
        # if self.rotate_emb:
        #     thetas = thetas + (
        #         targets.to(dtype=torch.float64) + 0.5
        #     ) * (2 * torch.pi / int(vocab_size))

        # Case 2: The word embedding is learnable
        if self.config.flow_path == FlowPath.HYPERBOLIC_BOUNDARY:
            rhos, thetas = self.bridge.binary_bridge(
                ts=ts,
                targets=targets,
                vocab_size=vocab_size,
                word_embedding=word_embedding,
            )
        else:
            raise ValueError(f"config.flow_path = {self.config.flow_path} is not supported, only suppport ({FlowPath.HYPERBOLIC_BOUNDARY}).")

        # if "lorentz" in self.loss_geometry:
        #     z = self.bridge.polar_to_lorentz(rhos, thetas).to(dtype=torch.float32)
        # else:
        z = torch.stack([rhos, thetas], dim=-1).to(dtype=torch.float32)
        logits = self.model(z=z, t=ts.to(dtype=torch.float32))
        return logits, ts, rhos, thetas, proposal_weight