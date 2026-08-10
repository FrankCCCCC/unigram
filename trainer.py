from abc import abstractmethod

import lightning as L
import torch
from visualizer import Recorder

class BaseTrainer(L.LightningModule):
    # Train / Valid / Test Keys. These double as the metric-name prefixes, so
    # they are the strings that land in test_metrics.json and in the sweep
    # result tables -- "val", not "valid".
    TRAIN_KEY: str = "train"
    VALID_KEY: str = "val"
    TEST_KEY: str = "test"

    # Loss and NELBO keys
    UNWEIGHTED_LOSS_KEY: str = "loss"
    WEIGHTED_LOSS_KEY: str = "wloss"
    UNWEIGHTED_NELBO_REF_KEY: str = "nelbo_ref"
    WEIGHTED_NELBO_REF_KEY: str = "wnelbo_ref"
    UNWEIGHTED_CE_REF_KEY: str = "ce_ref"
    WEIGHTED_CE_REF_KEY: str = "wce_ref"

    # Recorder series name: "{stage}_loss" is what visualizer.plot_loss_curves
    # plots by default. The value stored is the weighted-loss mean.
    RECORD_LOSS_KEY: str = UNWEIGHTED_LOSS_KEY

    # Quantities that also get a standard deviation reported.
    STD_KEYS = (WEIGHTED_LOSS_KEY, WEIGHTED_NELBO_REF_KEY, WEIGHTED_CE_REF_KEY)

    def __init__(self):
        super().__init__()
        self.recorder = Recorder()
        self.seed: int = 0

    def _make_step_generator(self, salt: int, batch_idx: int = 0, stage: int = 0) -> torch.Generator:
        """Per-step, per-batch, per-path torch.Generator on self.device.

        batch_idx and stage must be part of the seed: Lightning does not advance
        global_step during validate/test, so seeding on global_step alone gives
        every eval batch the identical t vector (measured: 1953/1953 test batches
        byte-identical). The estimator stays unbiased but its standard error hits
        a floor that raising test_size cannot lower -- ~2x wider than it looks.
        """
        seed_value = (
            self.seed * 1_000_003
            + int(self.global_step) * 7_919
            + int(batch_idx) * 104_729
            + int(stage) * 15_485_863
            + int(salt)
        ) & 0x7FFF_FFFF_FFFF_FFFF
        return torch.Generator(device=self.device).manual_seed(seed_value)

    @abstractmethod
    def _compute_losses(self, batch: torch.Tensor, batch_idx: int = 0, stage: int = 0) -> dict:
        """Return per-sample loss tensors keyed by the *_KEY constants above."""
        raise NotImplementedError

    def _log_losses(self, losses, stage: str, **log_kwargs):
        # "loss" is the training objective (loss_geometry, importance-weighted).
        # "wnelbo" is the poincare-polar ELBO estimate: the importance-weighted
        # integrand, so its mean estimates the whole integral over t. "nelbo" is
        # the same integrand unweighted (not an ELBO on its own -- it is what the
        # per-t loss looks like under the proposal). "ce" is the plain denoising
        # cross-entropy.
        wloss = losses[self.WEIGHTED_LOSS_KEY].mean()
        self.log(f"{stage}_{self.WEIGHTED_LOSS_KEY}", wloss, **log_kwargs)
        self.log(f"{stage}_{self.WEIGHTED_NELBO_REF_KEY}", losses[self.WEIGHTED_NELBO_REF_KEY].mean(), **log_kwargs)
        self.log(f"{stage}_{self.UNWEIGHTED_NELBO_REF_KEY}", losses[self.UNWEIGHTED_NELBO_REF_KEY].mean(), **log_kwargs)
        self.log(f"{stage}_{self.WEIGHTED_CE_REF_KEY}", losses[self.WEIGHTED_CE_REF_KEY].mean(), **log_kwargs)
        self.log(f"{stage}_{self.UNWEIGHTED_CE_REF_KEY}", losses[self.UNWEIGHTED_CE_REF_KEY].mean(), **log_kwargs)
        if log_kwargs.get("on_epoch"):
            # Epoch-aggregated std must come from pooled sums, not from
            # self.log(...).std(): Lightning would average the PER-BATCH stds,
            # and one 2048-sample batch rarely contains the tail of these
            # heavy-tailed integrands, so that underestimates by ~7%.
            self._accumulate_std(losses)
        else:
            for key in self.STD_KEYS:
                self.log(f"{stage}_{key}_std", losses[key].std(), **log_kwargs)
        return wloss

    def _reset_std_accum(self) -> None:
        # per key: [sum, sum of squares, count]
        self._std_accum = {key: [0.0, 0.0, 0] for key in self.STD_KEYS}

    def _accumulate_std(self, losses) -> None:
        for key in self.STD_KEYS:
            values = losses[key].detach().to(dtype=torch.float64)
            acc = self._std_accum[key]
            acc[0] += float(values.sum().cpu())
            acc[1] += float(values.square().sum().cpu())
            acc[2] += int(values.numel())

    @staticmethod
    def _std_from_sums(total: float, sq_total: float, count: int) -> float:
        if count <= 1:
            return 0.0
        return (max(sq_total - total * total / count, 0.0) / (count - 1)) ** 0.5

    def _log_std_accum(self, stage: str) -> None:
        for key, (total, sq_total, count) in self._std_accum.items():
            self.log(
                f"{stage}_{key}_std",
                torch.tensor(
                    self._std_from_sums(total, sq_total, count),
                    device=self.device,
                    dtype=torch.float64,
                ),
            )

    def training_step(self, batch: torch.Tensor, batch_idx: int):
        losses = self._compute_losses(batch, batch_idx=batch_idx, stage=0)
        loss = self._log_losses(losses, self.TRAIN_KEY, on_step=True, on_epoch=False, prog_bar=True)
        self.recorder.add(f"{self.TRAIN_KEY}_{self.RECORD_LOSS_KEY}", step=int(self.global_step) + 1, val=loss)
        return loss

    def validation_step(self, batch: torch.Tensor, batch_idx: int):
        return self._log_losses(
            self._compute_losses(batch, batch_idx=batch_idx, stage=1),
            self.VALID_KEY, on_step=False, on_epoch=True, prog_bar=True
        )

    def on_validation_epoch_start(self):
        self._reset_std_accum()

    def on_validation_epoch_end(self):
        if not self.trainer.sanity_checking:
            self._log_std_accum(self.VALID_KEY)
            self.recorder.add(
                f"{self.VALID_KEY}_{self.RECORD_LOSS_KEY}",
                step=int(self.global_step),
                val=self.trainer.callback_metrics[f"{self.VALID_KEY}_{self.WEIGHTED_LOSS_KEY}"],
            )

    def test_step(self, batch: torch.Tensor, batch_idx: int):
        return self._log_losses(
            self._compute_losses(batch, batch_idx=batch_idx, stage=2),
            self.TEST_KEY, on_step=False, on_epoch=True, prog_bar=True
        )

    def on_test_epoch_start(self):
        self._reset_std_accum()

    def on_test_epoch_end(self):
        self._log_std_accum(self.TEST_KEY)
        self.recorder.add(
            f"{self.TEST_KEY}_{self.RECORD_LOSS_KEY}",
            step=int(self.global_step) + 1,
            val=self.trainer.callback_metrics[f"{self.TEST_KEY}_{self.WEIGHTED_LOSS_KEY}"],
        )
