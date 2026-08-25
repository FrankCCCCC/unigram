import json, glob, re, collections, statistics as st, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
H = {"naive_ps": 0.500288, "cmplx_ps": 1.666363}
PROJ = [("2", "init_test"), ("3", "init_refactor_3d"), ("9", "init_refactor_9d"), ("16", "init_refactor_16d")]
COL = {"2": "#2a78d6", "3": "#eb6834", "9": "#1baf7a", "16": "#eda100"}
STEPS = [20000, 40000, 100000, 200000]
data = {}
for d, proj in PROJ:
    cells = collections.defaultdict(list)
    for f in glob.glob(f"output/{proj}/ps-*_ps_*/test_metrics.json"):
        n = f.split("/")[-2]; m = json.load(open(f))
        g = re.match(r"ps-(.+?)_lg-(\w+)_q-exp([\d.]+)_.*_st(\d+)_s(\d)", n).groups()
        if float(g[2]) > 0.25: continue
        cells[(g[0], g[1], int(g[3]))].append(m["test_wnelbo_ref"] - H[g[0]])
    data[d] = cells
ink, ink2, grid = "#1f1f1e", "#6b6a63", "#e6e5df"
fig, axes = plt.subplots(2, 2, figsize=(11, 7.2), sharex=True, facecolor="white")
for i, ps in enumerate(("naive_ps", "cmplx_ps")):
    for j, (lg, title) in enumerate((("ce", "cross-entropy-trained"), ("pp", "polar-ELBO-trained"))):
        ax = axes[i][j]; ax.set_facecolor("white")
        ax.axhline(0, color=ink2, lw=1, ls=(0, (4, 3)), zorder=1)
        ends = {}
        for d, _ in PROJ:
            ys = [st.mean(data[d][(ps, lg, s)]) for s in STEPS]
            es = [st.stdev(data[d][(ps, lg, s)]) for s in STEPS]
            ax.errorbar(STEPS, ys, yerr=es, color=COL[d], lw=2, marker="o", ms=5, capsize=2.5, elinewidth=1, zorder=3, label=f"d = {d}")
            ends[d] = ys[-1]
        # direct-label only endpoints that do not collide (>= 6% of the axis span apart); the legend covers the rest
        span = max(ends.values()) - min(ends.values()) + 1e-9
        for d, y in ends.items():
            if all(abs(y - y2) / span >= 0.06 for d2, y2 in ends.items() if d2 != d):
                ax.annotate(f"d={d}", (STEPS[-1], y), xytext=(7, 0), textcoords="offset points", va="center", fontsize=9, color=ink)
        ax.set_xscale("log"); ax.set_xticks(STEPS); ax.set_xticklabels(["20k", "40k", "100k", "200k"])
        ax.set_title(f"{ps}  ·  {title}", fontsize=11, color=ink, loc="left")
        ax.grid(True, axis="y", color=grid, lw=0.8); ax.set_axisbelow(True)
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        for s in ("left", "bottom"): ax.spines[s].set_color(grid)
        ax.tick_params(colors=ink2, labelsize=9)
        ax.set_xlim(16000, 290000)
        if j == 0: ax.set_ylabel("test_wnelbo_ref − H(p)  [nats]", fontsize=9.5, color=ink2)
        if i == 1: ax.set_xlabel("training steps", fontsize=9.5, color=ink2)
        ax.text(0.99, 0.03, "0 = entropy bound H(p)", transform=ax.transAxes, ha="right", fontsize=8, color=ink2)
axes[0][0].legend(frameon=False, fontsize=9, loc="upper left", ncol=4, labelcolor=ink)
fig.suptitle("Reference ELBO above the entropy bound vs. training, by hyperbolic dimension d\n"
             "mean ± std over loss rates exp{0.01, 0.05, 0.1, 0.25} × 3 seeds (12 cells); reference proposal exp(0.1), 4M test samples",
             fontsize=11.5, color=ink, x=0.01, ha="left")
fig.tight_layout(rect=(0, 0, 1, 0.94))
out = f"{sys.argv[1]}/cross_d_wnelbo.png"; fig.savefig(out, dpi=160); print(out)
