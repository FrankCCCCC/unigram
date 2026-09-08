import os
from typing import List, Optional, Tuple, Union

import hydra
import lightning as L
import torch
from omegaconf import DictConfig

from dataset import UnigramDataModule, process_ps
from geo_bridge import Coordinate, GeoUtils, HyperbolicHeatKernel
from loss import FlowPath, HyperBridge, Loss, LossGeometry, Proposal
from model import MLPLMRefactor, OptimalModelRefactor
from utils import TaskMgr, save_results
from visualizer import DataMgr
from trainer import BaseTrainer

def resolve_prod_factors(config: DictConfig) -> Tuple[List[int], List[float]]:
    """Read the geometry off the config as plain python lists.

    `prod_factor_dim` / `prod_factor_gaussian_curvature` describe the product
    manifold `H^{d_1}_{K_1} x ... x H^{d_M}_{K_M}`; both null falls back to the
    single factor `[hyper_dim]` at `[gaussian_curvature]`. The conversion out of
    omegaconf is not cosmetic: `HyperbolicModelBase.prod_factors` dispatches on
    `isinstance(x, list)`, and a `ListConfig` is not a `list`.
    """
    dims = config.get("prod_factor_dim", None)
    curvatures = config.get("prod_factor_gaussian_curvature", None)
    if dims is None and curvatures is None:
        return [int(config.hyper_dim)], [float(config.gaussian_curvature)]
    if dims is None or curvatures is None:
        raise ValueError(
            "prod_factor_dim and prod_factor_gaussian_curvature must both be set "
            f"or both be null; got {dims} and {curvatures}."
        )
    return [int(d) for d in dims], [float(k) for k in curvatures]

class HyperbolicDLMRefactor(BaseTrainer):
    def __init__(self, config: DictConfig):
        super().__init__()
        self.config = config
        self.prod_factor_dim, self.prod_factor_gaussian_curvature = resolve_prod_factors(config)
        self.embedding_size = sum(self.prod_factor_dim)
        self.seed = config.seed
        # sample_radial builds the heat-kernel marginal in linear float64, which
        # overflows past _radial_t_max(d) -- stated in UNIT time, so a factor of
        # radius R tolerates R^2 times as much physical time. Clamping t is the
        # same statistical no-op HyperBridge.bridge already relies on: by then
        # the direction identifies the target to full float64 precision.
        self.max_heat_time = min(
            HyperBridge._radial_t_max(factor_dim)
            * GeoUtils._curvature_scale(factor_curvature) ** 2
            for factor_dim, factor_curvature in zip(
                self.prod_factor_dim, self.prod_factor_gaussian_curvature
            )
        )

        if self.config.mode == "tnb":
            self.model = MLPLMRefactor(
                vocab_size=config.vocab_size,
                input_theta_dim=self.embedding_size,
                input_radial_dim=len(self.prod_factor_dim),
                output_theta_dim=self.embedding_size,
                # Nothing consumes a predicted radius: the loss is the ANGULAR
                # path-KL, so the trunk emits boundary features only.
                output_radial_dim=0,
                embedding_size=self.embedding_size,
                hidden_size=config.hidden_size,
                depth=config.depth,
                max_seq_len=1,
                unif_word_embedding=config.unif_word_embedding,
                prod_factor_dim=self.prod_factor_dim,
                prod_factor_gaussian_curvature=self.prod_factor_gaussian_curvature,
            )
            if not config.trainable_word_embedding:
                # Unlike main.py there is no "pinned angles, trainable head"
                # split: lm_head.weight is simultaneously the boundary table the
                # bridge samples toward, the table the loss scores against, and
                # the table the model's own horosphere readout uses. Freezing it
                # freezes all three, which is what keeps them consistent.
                self.model.lm_head.weight.requires_grad_(False)
        elif self.config.mode == "opt":
            self.model = OptimalModelRefactor(
                ps=process_ps(config.ps),
                embedding_size=self.embedding_size,
                prod_factor_dim=self.prod_factor_dim,
                prod_factor_gaussian_curvature=self.prod_factor_gaussian_curvature,
            )
        else:
            raise ValueError(f"mode shouldn't be {self.config.mode}, only support tnb and opt.")

        # Every model on this path owns its boundary table, so the bridge, the
        # loss and the model's horosphere readout all read the same one and
        # nothing has to fabricate a fallback.
        if self.model.word_embedding is None:
            raise ValueError(
                f"{type(self.model).__name__} has no word_embedding; "
                "main_refactor requires every model to own a boundary table."
            )

    def configure_optimizers(self):
        return torch.optim.Adam(
            [p for p in self.parameters() if p.requires_grad], lr=float(self.config.lr)
        )

    @property
    def word_embedding(self) -> torch.Tensor:
        # ONE boundary table for the bridge, the loss and the model: MLPLM
        # Refactor's lm_head.weight, or OptimalModelRefactor's frozen
        # uniform_sphere_points buffer. Never None (checked in __init__).
        return self.model.word_embedding

    def get_logits_inputs(
        self,
        batch_size: int,
        targets: torch.LongTensor,
        hyper_dt: float,
        hyper_T: int,
        proposal_type: str,
        proposal_exp_rate: float,
        word_embedding: torch.FloatTensor,
        device: torch.device,
        generator: Optional[torch.Generator] = None,
    ):
        ts, proposal_weight = Proposal.hyper_proposal(
            proposal_type=proposal_type,
            shape=(batch_size,),
            device=device,
            dtype=torch.float64,
            dt=hyper_dt,
            T=hyper_T,
            exp_rate=proposal_exp_rate,
            generator=generator,
        )

        if self.config.flow_path != FlowPath.HYPERBOLIC_BOUNDARY:
            raise ValueError(
                f"config.flow_path = {self.config.flow_path} is not supported, "
                f"only suppport ({FlowPath.HYPERBOLIC_BOUNDARY})."
            )
        ts = ts.clamp_max(self.max_heat_time)
        # rhos: (B, S, M) one intrinsic radius per factor, thetas: (B, S, sum(d_i))
        # the per-factor unit directions concatenated. ONE heat time per sequence,
        # not per position: sample_radial(ts, d, seq_len, K) draws seq_len
        # independent radii from the same t, which is the bridge's contract.
        rhos, thetas = HyperbolicHeatKernel.poincare_bridge_prod(
            ts=ts,
            targets=targets,
            word_embedding=word_embedding.to(torch.float64),
            output_coord=Coordinate.HYPERBOLIC_POLAR,
            prod_factor_dim=self.prod_factor_dim,
            prod_factor_gaussian_curvature=self.prod_factor_gaussian_curvature,
        )
        # The horosphere readout returns the FULL log-posterior (the geometry is
        # already added), which is what the *_refactor losses consume -- they do
        # not add horosphere_dists again. Axis 1 is the sequence.
        logits = self.model(
            z=None,
            theta=thetas,
            radius=rhos,
            t=None,
            forward_type=self.config.forward_type,
        )
        # proposal_weight is (B,) -- one t per sequence -- while the losses are
        # (B, S), so hand it back with the sequence axis it has to broadcast over.
        return logits, ts, rhos, thetas, proposal_weight[:, None]

    def _compute_losses(self, batch: torch.Tensor, batch_idx: int = 0, stage: int = 0):
        # (B, S). The unigram dataset yields one token per example, so S == 1;
        # reshaping rather than flattening keeps the axis the *_refactor losses
        # and the model both expect.
        targets = batch.reshape(batch.shape[0], -1).to(device=self.device, dtype=torch.long)
        batch_size = targets.shape[0]

        # Loss Function
        loss_gen = self._make_step_generator(salt=0, batch_idx=batch_idx, stage=stage)
        logits_loss, ts_loss, rhos_loss, thetas_loss, pw_loss = self.get_logits_inputs(
            batch_size=batch_size,
            targets=targets,
            hyper_dt=self.config.hyper_dt,
            hyper_T=self.config.hyper_T,
            proposal_type=self.config.loss_proposal_type,
            proposal_exp_rate=self.config.loss_proposal_exp_rate,
            word_embedding=self.word_embedding,
            device=self.device,
            generator=loss_gen,
        )
        wloss, loss = Loss.weighted_loss_refactor(
            logits=logits_loss,
            targets=targets,
            rhos=rhos_loss,
            thetas=thetas_loss,
            proposal_weight=pw_loss,
            loss_geometry=self.config.loss_geometry,
            word_embedding=self.word_embedding,
            prod_factor_dim=self.prod_factor_dim,
            prod_factor_gaussian_curvature=self.prod_factor_gaussian_curvature,
        )

        # Reference CE and ELBO, on an independent RNG stream (salt=1) so they
        # stay comparable across runs trained on different objectives.
        ref_gen = self._make_step_generator(salt=1, batch_idx=batch_idx, stage=stage)
        logits_ref, ts_ref, rhos_ref, thetas_ref, pw_ref = self.get_logits_inputs(
            batch_size=batch_size,
            targets=targets,
            hyper_dt=self.config.hyper_dt,
            hyper_T=self.config.hyper_T,
            proposal_type=self.config.ref_proposal_type,
            proposal_exp_rate=self.config.ref_proposal_exp_rate,
            word_embedding=self.word_embedding,
            device=self.device,
            generator=ref_gen,
        )
        wnelbo_ref, nelbo_ref = Loss.weighted_loss_refactor(
            logits=logits_ref,
            targets=targets,
            rhos=rhos_ref,
            thetas=thetas_ref,
            proposal_weight=pw_ref,
            loss_geometry=LossGeometry.POINCARE_POLAR,
            word_embedding=self.word_embedding,
            prod_factor_dim=self.prod_factor_dim,
            prod_factor_gaussian_curvature=self.prod_factor_gaussian_curvature,
        )
        wce_ref, ce_ref = Loss.weighted_loss_refactor(
            logits=logits_ref,
            targets=targets,
            rhos=rhos_ref,
            thetas=thetas_ref,
            proposal_weight=pw_ref,
            loss_geometry=LossGeometry.CROSS_ENTROPY,
            word_embedding=self.word_embedding,
            prod_factor_dim=self.prod_factor_dim,
            prod_factor_gaussian_curvature=self.prod_factor_gaussian_curvature,
        )

        return {
            self.UNWEIGHTED_LOSS_KEY: loss,
            self.WEIGHTED_LOSS_KEY: wloss,
            self.WEIGHTED_NELBO_REF_KEY: wnelbo_ref,
            self.UNWEIGHTED_NELBO_REF_KEY: nelbo_ref,
            self.WEIGHTED_CE_REF_KEY: wce_ref,
            self.UNWEIGHTED_CE_REF_KEY: ce_ref,
            "ts": ts_loss.to(dtype=torch.float32),
            "proposal_weight": pw_loss.to(dtype=torch.float32),
        }

@hydra.main(version_base=None, config_path="config", config_name="config_refactor")
def main(cfg: DictConfig) -> None:
    datamodule = UnigramDataModule(config=cfg)
    cfg.ps = datamodule.ps
    cfg.vocab_size = datamodule.vocab_size

    task_mgr = TaskMgr(work_dir=cfg.folder)
    if task_mgr.check_finished():
        return

    L.seed_everything(int(cfg.seed), workers=True)
    model = HyperbolicDLMRefactor(config=cfg)
    print(
        f"Geometry: prod_factor_dim={model.prod_factor_dim} "
        f"prod_factor_gaussian_curvature={model.prod_factor_gaussian_curvature}"
    )
    trainer = L.Trainer(
        accelerator="auto",
        devices=1,
        max_steps=int(cfg.max_steps),
        gradient_clip_val=cfg.gradient_clip_val,
        logger=False,
        enable_checkpointing=False,
        enable_model_summary=False,
        enable_progress_bar=True,
        log_every_n_steps=1,
        num_sanity_val_steps=0,
    )
    if cfg.mode == "tnb":
        trainer.fit(model, datamodule=datamodule)
    test_metrics = trainer.test(model, datamodule=datamodule, verbose=False)
    data_mgr = DataMgr(cfg.folder)
    saved = data_mgr.save(
        recorder=model.recorder,
        data_file=cfg.loss_data_path,
        fig_file=cfg.loss_plot_path,
        moving_average_window=cfg.loss_plot_ma_window,
    )
    print(f"Saved loss data to: {saved['data_path']}")
    print(f"Saved loss plot to: {saved['figure_path']}")

    if test_metrics:
        print("Test metrics:")
        for name, value in test_metrics[0].items():
            print(f"  {name}: {value:.6f}")

    metrics_path = save_results(test_metrics, cfg.folder)
    print(f"Saved test metrics to: {metrics_path}")
    if cfg.mode == "tnb":
        torch.save(model.model.state_dict(), os.path.join(cfg.folder, "model.pt"))

    task_mgr.finished()

if __name__ == "__main__":
    main()
