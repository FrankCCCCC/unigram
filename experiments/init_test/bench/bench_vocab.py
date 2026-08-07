import sys, time, torch
sys.path.insert(0, "/share/desa/nfs02/sc3379/workspace/research/unigram2")
from omegaconf import OmegaConf
from dataset import UnigramDataModule
from loss import HyperBridge, Loss, Proposal
from model import MLPLM

dev = "cuda"
print(f"gpu: {torch.cuda.get_device_name(0)}  total={torch.cuda.get_device_properties(0).total_memory/2**30:.1f} GiB\n")
print(f"{'ps':>14} {'V':>7} {'H(p)':>8} {'peak GiB':>9} {'s/step':>8} {'20k steps':>11}")
for spec in ("naive_ps", "c1e2_exp1.0", "c1e3_exp1.0", "c1e4_exp1.0"):
    dm = UnigramDataModule(config=OmegaConf.create({"ps": spec}))
    ps = torch.tensor(dm.ps, device=dev, dtype=torch.float64)
    V = dm.vocab_size
    H = float(-(ps*ps.log()).sum())
    torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
    try:
        model = MLPLM(vocab_size=V, input_dim=2, output_dim=2, hidden_size=128, depth=3).to(dev)
        opt = torch.optim.Adam(model.parameters(), lr=1e-3)
        N = 2048
        t0 = None
        for i in range(12):
            if i == 2: torch.cuda.synchronize(); t0 = time.time()
            tg = torch.multinomial(ps.float(), N, replacement=True)
            ts, w = Proposal.hyper_proposal("exp", (N,), dev, torch.float64, dt=0.01, T=1e7, exp_rate=0.1)
            emb = model.lm_head.weight
            r, th = HyperBridge.binary_bridge(ts=ts, targets=tg, vocab_size=V, word_embedding=emb)
            lg = model(z=torch.stack([r, th], -1).float(), t=ts.float())
            wl, _ = Loss.weighted_binary_loss(logits=lg, targets=tg, rhos=r, thetas=th,
                proposal_weight=w, word_embedding=emb, loss_geometry="poincare_polar")
            # the reference pass runs every step too (both ELBO and CE readouts)
            wn, _ = Loss.weighted_binary_loss(logits=lg.detach(), targets=tg, rhos=r, thetas=th,
                proposal_weight=w, word_embedding=emb, loss_geometry="poincare_polar")
            wc, _ = Loss.weighted_binary_loss(logits=lg.detach(), targets=tg, rhos=r, thetas=th,
                proposal_weight=w, word_embedding=emb, loss_geometry="cross_entropy")
            opt.zero_grad(); wl.mean().backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step()
        torch.cuda.synchronize()
        sper = (time.time()-t0)/10
        peak = torch.cuda.max_memory_allocated()/2**30
        print(f"{spec:>14} {V:>7} {H:>8.4f} {peak:>9.2f} {sper:>8.4f} {sper*20000/3600:>10.1f}h")
    except torch.cuda.OutOfMemoryError as e:
        print(f"{spec:>14} {V:>7} {H:>8.4f} {'OOM':>9} {'-':>8} {'-':>11}")
    del model, opt
    torch.cuda.empty_cache()
