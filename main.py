import os
from typing import Optional

import hydra
import lightning as L
import torch
from omegaconf import DictConfig

from dataset import UnigramDataModule, process_ps
from loss import FlowPath, HyperBridge, Loss, LossGeometry, Proposal
from model import MLPLM, OptimalModel
from utils import TaskMgr, save_results
from visualizer import DataMgr
from trainer import BaseTrainer

class HyperbolicDLM(BaseTrainer):
    def __init__(self, config: DictConfig):
        super().__init__()
        self.config = config
        self.bridge = HyperBridge()

        # Model input z = (rho, u): the bridge radius plus its direction, a unit
        # vector in R^hyper_dim (the boundary of H^hyper_dim is S^{hyper_dim-1}).
        self.model_input_dim = config.hyper_dim + 1
        # If False the per-word boundary angles phi_v stay fixed at (v+0.5)*2*pi/V
        # instead of being read off the lm-head; the lm-head still trains as the
        # logit readout. See the word_embedding property.
        self.trainable_word_embedding = config.trainable_word_embedding
        self.seed = config.seed

        if self.config.mode == "tnb":
            self.model = MLPLM(
                vocab_size=config.vocab_size,
                input_dim=self.model_input_dim,
                output_dim=config.hyper_dim,
                hidden_size=config.hidden_size,
                depth=config.depth,
                unif_word_embedding=config.unif_word_embedding,
            )
        elif self.config.mode == "opt":
            self.model = OptimalModel(
                ps=process_ps(config.ps),
            )
        else:
            raise ValueError(f"mode shouldn't be {self.config.mode}, only support tnb and opt.")

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=float(self.config.lr))

    @property
    def word_embedding(self) -> Optional[torch.Tensor]:
        # Learnable boundary embedding (lm-head weights, shape (V, hyper_dim)) used to
        # define each word's boundary angle phi_v = atan2(e_v). Returns None — so the
        # bridge and loss fall back to fixed equally-spaced angles — when the backbone
        # has no such table (e.g. OptimalModel) OR when trainable_word_embedding is
        # False.
        if not self.trainable_word_embedding:
            return None
        return self.model.word_embedding

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

        # For calculating posterior
        # Case 1: The word embedding is Equally divided around the circle
        # rhos, thetas = self.bridge.bridge(ts=ts)
        # if self.rotate_emb:
        #     thetas = thetas + (
        #         targets.to(dtype=torch.float64) + 0.5
        #     ) * (2 * torch.pi / int(vocab_size))

        # Case 2: The word embedding is learnable
        if self.config.flow_path == FlowPath.HYPERBOLIC_BOUNDARY:
            rhos, thetas = self.bridge.bridge(
                ts=ts,
                targets=targets,
                vocab_size=vocab_size,
                emb_dim=self.config.hyper_dim,
                word_embedding=word_embedding,
            )
        else:
            raise ValueError(f"config.flow_path = {self.config.flow_path} is not supported, only suppport ({FlowPath.HYPERBOLIC_BOUNDARY}).")

        # rhos: (N,), thetas: (N, hyper_dim) unit directions -> z: (N, hyper_dim + 1)
        z = torch.cat([rhos[:, None], thetas], dim=-1).to(dtype=torch.float32)
        logits = self.model(z=z, t=ts.to(dtype=torch.float32))
        return logits, ts, rhos, thetas, proposal_weight

    def _compute_losses(self, batch: torch.Tensor, batch_idx: int = 0, stage: int = 0):
        targets = batch.reshape(-1).to(device=self.device, dtype=torch.long)
        batch_size = targets.shape[0]

        # Loss Function
        loss_gen = self._make_step_generator(salt=0, batch_idx=batch_idx, stage=stage)
        loss_logits, ts_loss, rhos_loss, thetas_loss, pw_loss = self.get_logits_inputs(
            batch_size=batch_size,
            targets=targets,
            hyper_dt=self.config.hyper_dt,
            hyper_T=self.config.hyper_T,
            proposal_type=self.config.loss_proposal_type,
            proposal_exp_rate=self.config.loss_proposal_exp_rate,
            vocab_size=self.config.vocab_size,
            word_embedding=self.word_embedding,
            device=self.device,
            generator=loss_gen,
        )
        wloss, loss = Loss.weighted_loss(
            logits=loss_logits,
            targets=targets,
            rhos=rhos_loss,
            thetas=thetas_loss,
            proposal_weight=pw_loss,
            loss_geometry=self.config.loss_geometry,
            word_embedding=self.word_embedding,
        )
        # ce = torch.nn.functional.cross_entropy(loss_logits, targets, reduction="none")

        # Reference CE and ELBO
        ref_gen = self._make_step_generator(salt=1, batch_idx=batch_idx, stage=stage)
        logits_ref, ts_ref, rhos_ref, thetas_ref, pw_ref = self.get_logits_inputs(
            batch_size=batch_size,
            targets=targets,
            hyper_dt=self.config.hyper_dt,
            hyper_T=self.config.hyper_T,
            proposal_type=self.config.ref_proposal_type,
            proposal_exp_rate=self.config.ref_proposal_exp_rate,
            vocab_size=self.config.vocab_size,
            word_embedding=self.word_embedding,
            device=self.device,
            generator=ref_gen,
        )
        wnelbo_ref, nelbo_ref = Loss.weighted_loss(
            logits=logits_ref,
            targets=targets,
            rhos=rhos_ref,
            thetas=thetas_ref,
            proposal_weight=pw_ref,
            loss_geometry=LossGeometry.POINCARE_POLAR,
            word_embedding=self.word_embedding,
        )
        wce_ref, ce_ref = Loss.weighted_loss(
            logits=logits_ref,
            targets=targets,
            rhos=rhos_ref,
            thetas=thetas_ref,
            proposal_weight=pw_ref,
            loss_geometry=LossGeometry.CROSS_ENTROPY,
            word_embedding=self.word_embedding,
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

@hydra.main(version_base=None, config_path="config", config_name="config")
def main(cfg: DictConfig) -> None:
    datamodule = UnigramDataModule(config=cfg)
    cfg.ps = datamodule.ps
    cfg.vocab_size = datamodule.vocab_size

    task_mgr = TaskMgr(work_dir=cfg.folder)
    if task_mgr.check_finished():
        return

    L.seed_everything(int(cfg.seed), workers=True)
    model = HyperbolicDLM(config=cfg)
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
        # Final weights (a few KB): the lm_head rows are the learned boundary
        # embedding, so a finished run can be re-evaluated and its phi inspected.
        torch.save(model.model.state_dict(), os.path.join(cfg.folder, "model.pt"))

    task_mgr.finished()

if __name__ == "__main__":
    main()