from typing import Optional

import hydra
import lightning as L
import torch
from omegaconf import DictConfig

from dataset import UnigramDataModule, process_ps
from loss import FlowPath, HyperBridge, Loss, LossGeometry, Proposal
from model import MLPLM, OptimalModel
from utils import TaskMgr, save_results
from visualizer import DataMgr, Recorder

class HyperbolicDLM(L.LightningModule):
    def __init__(self, config: DictConfig):
        super().__init__()
        self.config = config
        self.bridge = HyperBridge()
        self.recorder = Recorder()

        self.model_input_dim = config.hyper_dim
        # If False the per-word boundary angles phi_v stay fixed at (v+0.5)*2*pi/V
        # instead of being read off the lm-head; the lm-head still trains as the
        # logit readout. See the word_embedding property.
        self.trainable_word_embedding = config.trainable_word_embedding

        if self.config.mode == "tnb":
            self.model = MLPLM(
                vocab_size=config.vocab_size,
                input_dim=self.model_input_dim,
                output_dim=config.hyper_dim,
                hidden_size=config.hidden_size,
                depth=config.depth,
            )
        elif self.config.mode == "opt":
            self.model = OptimalModel(
                ps=process_ps(config.ps),
            )
        else:
            raise ValueError(f"mode shouldn't be {self.mode}, only support tnb and opt.")

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
        head = getattr(self.model, "lm_head", None)
        return head.weight if head is not None else None

    def _make_step_generator(self, salt: int) -> torch.Generator:
        """Per-step, per-path torch.Generator on self.device."""
        STEP_STRIDE = 1_000_003
        seed_value = (
            self.config.seed * STEP_STRIDE
            + int(self.global_step) * 2
            + int(salt)
        ) & 0x7FFF_FFFF_FFFF_FFFF
        return torch.Generator(device=self.device).manual_seed(seed_value)

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

        z = torch.stack([rhos, thetas], dim=-1).to(dtype=torch.float32)
        logits = self.model(z=z, t=ts.to(dtype=torch.float32))
        return logits, ts, rhos, thetas, proposal_weight

    def _compute_losses(self, batch: torch.Tensor):
        targets = batch.reshape(-1).to(device=self.device, dtype=torch.long)
        batch_size = targets.shape[0]

        # Loss Function
        loss_gen = self._make_step_generator(salt=0)
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
        wloss, loss = Loss.weighted_binary_loss(
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
        ref_gen = self._make_step_generator(salt=1)
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
        wnelbo_ref, nelbo_ref = Loss.weighted_binary_loss(
            logits=logits_ref,
            targets=targets,
            rhos=rhos_ref,
            thetas=thetas_ref,
            proposal_weight=pw_ref,
            loss_geometry=LossGeometry.POINCARE_POLAR,
            word_embedding=self.word_embedding,
        )
        wce_ref, ce_ref = Loss.weighted_binary_loss(
            logits=logits_ref,
            targets=targets,
            rhos=rhos_ref,
            thetas=thetas_ref,
            proposal_weight=pw_ref,
            loss_geometry=LossGeometry.CROSS_ENTROPY,
            word_embedding=self.word_embedding,
        )

        return {
            "loss": loss,
            "wloss": wloss,
            "wnelbo_ref": wnelbo_ref,
            "nelbo_ref": nelbo_ref,
            "wce_ref": wce_ref,
            "ce_ref": ce_ref,
            "ts": ts_loss.to(dtype=torch.float32),
            "proposal_weight": pw_loss.to(dtype=torch.float32),
        }

    def _log_losses(self, losses, stage: str, **log_kwargs):
        # "loss" is the training objective (loss_geometry, importance-weighted).
        # "wnelbo" is the poincare-polar ELBO estimate: the importance-weighted
        # integrand, so its mean estimates the whole integral over t. "nelbo" is
        # the same integrand unweighted (not an ELBO on its own -- it is what the
        # per-t loss looks like under the proposal). "ce" is the plain denoising
        # cross-entropy.
        wloss = losses["wloss"].mean()
        self.log(f"{stage}_wloss", wloss, **log_kwargs)
        self.log(f"{stage}_wloss_std", losses["wloss"].std(), **log_kwargs)
        self.log(f"{stage}_wnelbo_ref", losses["wnelbo_ref"].mean(), **log_kwargs)
        self.log(f"{stage}_nelbo_ref", losses["nelbo_ref"].mean(), **log_kwargs)
        self.log(f"{stage}_wce_ref", losses["wce_ref"].mean(), **log_kwargs)
        self.log(f"{stage}_ce_ref", losses["ce_ref"].mean(), **log_kwargs)
        return wloss

    def training_step(self, batch: torch.Tensor, batch_idx: int):
        losses = self._compute_losses(batch)
        loss = self._log_losses(losses, "train", on_step=True, on_epoch=False, prog_bar=True)
        self.recorder.add("train_loss", step=int(self.global_step) + 1, val=loss)
        return loss

    def validation_step(self, batch: torch.Tensor, batch_idx: int):
        return self._log_losses(
            self._compute_losses(batch), "val", on_step=False, on_epoch=True, prog_bar=True
        )

    def on_validation_epoch_end(self):
        if not self.trainer.sanity_checking:
            self.recorder.add(
                "val_loss", step=int(self.global_step), val=self.trainer.callback_metrics["val_wloss"]
            )

    def test_step(self, batch: torch.Tensor, batch_idx: int):
        return self._log_losses(
            self._compute_losses(batch), "test", on_step=False, on_epoch=True, prog_bar=True
        )

    def on_test_epoch_end(self):
        self.recorder.add(
            "test_loss",
            step= int(self.global_step) + 1,
            val=self.trainer.callback_metrics["test_wloss"],
        )

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

    task_mgr.finished()

if __name__ == "__main__":
    main()