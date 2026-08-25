# Tabulated even-d radial sampler vs the exact sample_radial (and, at d=2, the
# closed-form Gruet sampler): KS distance over a sweep of t, plus bridge() timing.
# Run on a GPU node:  python experiments/init_refactor_16d/validate_table.py
import time, math, torch, sys
sys.path.insert(0, "/share/thickstun/sychou/workspace/research/unigram-dev/unigram")
from loss import HyperBridge, Proposal
from geo_bridge import HyperbolicHeatKernel as HK
dev = torch.device("cuda"); torch.manual_seed(0)
print(torch.cuda.get_device_name())

def ks(a, b):
    a, _ = a.sort(); b, _ = b.sort()
    allv = torch.cat([a, b]).sort().values
    Fa = torch.searchsorted(a, allv, right=True) / a.numel()
    Fb = torch.searchsorted(b, allv, right=True) / b.numel()
    return (Fa - Fb).abs().max().item()

N = 1 << 15
for d in (2, 16):
    t0 = time.time(); HyperBridge._radial_quantile_table(d, dev); torch.cuda.synchronize()
    log_t, xq = HyperBridge._radial_tables[(d, str(dev))]
    print(f"\n== d={d}: table {tuple(xq.shape)} built in {time.time()-t0:.1f}s, t_max={HyperBridge._radial_t_max(d):.3f}")
    tmax = HyperBridge._radial_t_max(d)
    for t in [1e-6, 1e-3, 0.01, 0.03, 0.1, 0.3, 1.0, min(3.0, tmax), min(10.0, tmax), min(50.0, tmax), tmax]:
        ts = torch.full((N,), t, dtype=torch.float64, device=dev)
        exact = HK.sample_radial(ts[:4096].repeat(16), d=d, seq_len=1).squeeze(-1) if d % 2 == 0 else None
        # exact: 16 x 4096 rows (chunked so the McKean quadrature fits); same distribution
        exact = HK.sample_radial(ts, d=d, seq_len=1).squeeze(-1) if N <= 4096 else torch.cat(
            [HK.sample_radial(ts[:4096], d=d, seq_len=1).squeeze(-1) for _ in range(N // 4096)])
        tab = HyperBridge.sample_radial_tabulated(ts, d=d)
        line = (f"t={t:9.3g}  exact mean={exact.mean():8.4f} std={exact.std():7.4f} | "
                f"table mean={tab.mean():8.4f} std={tab.std():7.4f} | KS={ks(exact, tab):.4f}")
        if d == 2:
            ns = torch.poisson(ts / 8).to(torch.int64)
            ss = ts.sqrt() * HyperBridge.sample_chi(2 * ns + 3, ts.dtype)
            vs = torch.rand_like(ts)
            gruet = torch.acosh(vs.square() + (1 - vs.square()) * torch.cosh(ss.clamp_max(700.0)))
            line += f" | Gruet mean={gruet.mean():8.4f} KS(tab,Gruet)={ks(gruet, tab):.4f} KS(exact,Gruet)={ks(exact, gruet):.4f}"
        print(line)
    # random t from the exp(0.1) proposal, mixed batch (the real use)
    ts, _ = Proposal.hyper_proposal("exp", (4096,), dev, torch.float64, dt=0.01, T=10_000_000, exp_rate=0.1)
    ts = ts.clamp_max(tmax)
    ex = torch.cat([HK.sample_radial(ts, d=d, seq_len=1).squeeze(-1) for _ in range(8)])
    tb = torch.cat([HyperBridge.sample_radial_tabulated(ts, d=d) for _ in range(8)])
    print(f"exp(0.1) batch: exact mean={ex.mean():.4f} std={ex.std():.4f} | table mean={tb.mean():.4f} std={tb.std():.4f} | KS={ks(ex, tb):.4f}")
    # timing
    ts, _ = Proposal.hyper_proposal("exp", (2048,), dev, torch.float64, dt=0.01, T=10_000_000, exp_rate=0.1)
    tg = torch.randint(0, 10, (2048,), device=dev)
    HyperBridge.bridge(ts, tg, vocab_size=10, emb_dim=d); torch.cuda.synchronize(); t0 = time.time()
    for _ in range(10): HyperBridge.bridge(ts, tg, vocab_size=10, emb_dim=d)
    torch.cuda.synchronize(); print(f"bridge() d={d}: {(time.time()-t0)/10*1000:.1f} ms")
