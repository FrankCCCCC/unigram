class HyperbolicDLM(L.LightningModule):
    def __init__(self, config: DictConfig):
        super().__init__()
        self.config = config
        self.bridge = HyperBridge()
        self.recorder = Recorder()

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

    def _compute_losses(self, batch: torch.Tensor):
        targets = batch.reshape(-1).to(device=self.device, dtype=torch.long)
        batch_size = targets.shape[0]

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
        wloss, loss = self.bridge.weighted_binary_loss(
            logits=loss_logits,
            targets=targets,
            rhos=rhos_loss,
            thetas=thetas_loss,
            proposal_weight=pw_loss,
            loss_geometry=self.loss_geometry,
            word_embedding=self.word_embedding,
        )
        ce = torch.nn.functional.cross_entropy(loss_logits, targets, reduction="none")

        if (self.config.nelbo_proposal_type == self.config.loss_proposal_type
              and self.config.nelbo_proposal_exp_rate == self.config.loss_proposal_exp_rate
              and self.config.nelbo_geometry == self.loss_geometry
              and self.config.loss_geometry not in {LossGeometry.CROSS_ENTROPY, LossGeometry.HORO_CROSS_ENTROPY}):
            # Identical configs — reuse the loss-path computation.
            wnelbo = wloss
            nelbo = loss
            ts_nelbo = ts_loss
            pw_nelbo = pw_loss
        else:
            nelbo_gen = self._make_step_generator(salt=1)
            nelbo_logits, ts_nelbo, rhos_nelbo, thetas_nelbo, pw_nelbo = self.get_logits_inputs(
                batch_size=batch_size,
                targets=targets,
                hyper_dt=self.config.hyper_dt,
                hyper_T=self.config.hyper_T,
                proposal_type=self.config.nelbo_proposal_type,
                proposal_exp_rate=self.config.nelbo_proposal_exp_rate,
                vocab_size=self.config.vocab_size,
                word_embedding=self.word_embedding,
                device=self.device,
                generator=nelbo_gen,
            )
            wnelbo, nelbo = self.bridge.weighted_binary_nelbo(
                logits=nelbo_logits,
                targets=targets,
                rhos=rhos_nelbo,
                thetas=thetas_nelbo,
                proposal_weight=pw_nelbo,
                loss_geometry=self.config.nelbo_geometry,
                word_embedding=self.word_embedding,
            )

        return {
            "loss": wloss,
            "wnelbo_loss": wnelbo,
            "nelbo_loss": nelbo,
            "ce": ce,
            "ts": ts_nelbo.to(dtype=torch.float32),
            "proposal_weight": pw_nelbo.to(dtype=torch.float32),
        }

    def training_step(self, batch: torch.Tensor, batch_idx: int):
        losses = self._compute_losses(batch)
        loss = losses["loss"].mean()
        loss_std = losses["loss"].std()

        return loss

    def validation_step(self, batch: torch.Tensor, batch_idx: int):
        losses = self._compute_losses(batch)
        loss = losses["loss"].mean()
        loss_values = losses["loss"].detach().to(dtype=torch.float64)

        return loss

    def test_step(self, batch: torch.Tensor, batch_idx: int):
        losses = self._compute_losses(batch)
        loss = losses["loss"].mean()
        loss_values = losses["loss"].detach().to(dtype=torch.float64)

        return loss

@hydra.main(version_base=None)
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