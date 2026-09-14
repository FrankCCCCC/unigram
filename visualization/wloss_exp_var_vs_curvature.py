#!/usr/bin/env python
"""Expectation and variance of the training objective `wloss` -- or, with
`--metric wnelbo_ref`, of the reference-path ELBO -- vs curvature.

Four figures: {expectation, variance} x {Polar ELBO, cross-entropy}. One line per
loss proposal rate `lambda`, every curvature in the project on the x axis.

  Polar ELBO   wloss = Loss.bridge_loss_elbo_refactor       (the ELBO estimate)
  CE           wloss = Loss.bridge_loss_crossentropy_refactor

`wloss` is a per-sample quantity: the bridge loss at a time `t ~ q_lambda`
reweighted by `1/q_lambda(t)`. Importance sampling is unbiased, so its MEAN
estimates the same integral for every `lambda` -- and its VARIANCE is the price
paid for that estimate. The two figures are the two halves of one story:

  expectation  where the estimator works, every `lambda` lands on the same value
               and the lines collapse onto one flat band. Where it does not, they
               peel off DOWNWARD -- the `1/q(t)` weights are heavy-tailed, the
               tail is never sampled, and the mean silently under-reports.
  variance     the same frontier seen from the other side, and the reason the
               expectation fails: variance blows up before the bias becomes
               visible, so this is the earlier warning.

For the Polar ELBO the integral being estimated is the negative ELBO, which at
the Bayes-optimal model equals `H(p)` -- drawn as a reference line, since it is
the value every honest `lambda` must reproduce. For CE the integral is the
weighted denoising cross-entropy, which has no distribution-only limit: measured
here it scales as `R^2 = 1/|K|` to within 0.8% over four decades, drawn as a
guide.

Both plotted statistics match RESULTS.md's `mean / variance` cells:

  expectation  mean over seeds of `test_wloss`.
  variance     mean over seeds of `test_wloss_std**2`: the point estimate of
               per-sample variance from each run's 4e6 test draws, in nats^2.

Each statistic is averaged separately across the 3 seeds. Variance is never
computed across seed means. Expectation error bars remain the single-run
Monte Carlo standard error, sqrt(averaged per-sample variance / 4e6), rather
than the standard error of the three-seed average.

Curvature enters through the radius `R = 1/sqrt(-K)`: `main_refactor.py` clamps
the heat time at `_radial_t_max(3) * R^2`, and the per-`t` loss decays ~R^2 times
more slowly as K flattens. The ~0.304 variance cliff measured at K=-1 therefore
scales as `1/R^2`, which is why the usable `lambda` range moves with curvature.
Rates above the K=-1 cliff are drawn dashed.

Every curvature present in the project is plotted -- the set is read off the run
directories, not hard-coded, so a sweep that adds curvature cells is picked up
without editing this file. `|K|` carries the x axis on a log scale.

`lambda` is a continuous ordered parameter, so it gets a continuous ramp and a
colorbar rather than a categorical legend. The ramp is viridis truncated to
[0, 0.75]: perceptually uniform and monotone in lightness (so it still reads as
an ordered scale, not a rainbow), but spanning purple -> blue -> teal -> green
rather than one hue, which is what makes seven levels tellable apart. Measured
worst-adjacent separation, OKLab dE x100 on a white surface: one-hue blue ramp
4.7 normal / 4.7 CVD; this ramp 9.3 / 7.4. Truncating LESS is worse, not better
-- the green end bunches up and the worst pair falls back to ~7.

Seven levels on any single ramp still cannot clear the dE 15 floor at which
colour alone is reliable, so identity is carried redundantly by a distinct
marker per `lambda` and a direct end label; the ramp encodes the ordering.

Reads `output/{project}/{run}/test_metrics.json` -- the same files
`experiments/report.py` builds RESULTS.md from -- so the numbers here and the
RESULTS.md tables cannot drift apart. `H(p)` comes from `report.ENTROPY`, so
there is one source of truth for it too.

`--metric wnelbo_ref` plots the headline reference-path ELBO instead of the
trained objective. It changes what `lg` means: `wloss` IS the geometry `lg`
names, but `wnelbo_ref` is always the poincare-polar ELBO measured on the
reference path, so there `lg` only says which objective the model was TRAINED
with. Hence `H(p)` is the right reference for both panels and the CE `R^2`
guide -- a statement about the weighted CE integral -- is not drawn.

The reference proposal is pinned at exp(REF_RATE) in PHYSICAL time while the
bridge is a function of `t/R^2`, so its effective rate is `REF_RATE/|K|`. Those
curvatures are shaded rather than dropped, in report.py's two tiers: light above
REF_EFF_CHECK (consult the mode=opt control at the same (ps, K) -- more factors
identify the target faster, so a 3-factor D=9 product is still sound at an
effective rate of 2 where a D=3 single manifold is already biased) and dark at
or above REF_EFF_SEVERE, where every configuration measured is invalid.

A product-manifold cell tags its factors `x`-joined. What matters is whether they
DIFFER, not whether the tag is joined: `sweep_lib.curvature_tag` collapses equal
factors to the shared scalar (`_k--1.0`), but earlier sweeps spelled them out
(`_k--1.0x-1.0x-1.0`, which is every cell of `prod_manifold_acc_test`). Those are
still one curvature and go on the axis. Only a genuinely MIXED vector
(`_k--0.01x-10.0x-1.0`) has no single Gaussian curvature; rather than crash on
`float()` or silently drop 10% of such a grid, those cells are drawn as unjoined
markers in their own column right of a dotted break, parked on the sharp side
because the sharpest factor is what governs the product (report.k_sort_key).
Their x position carries no curvature meaning.

Outputs:
  <out-dir>/{metric}_mean_{pp,ce}_{ps}.png
  <out-dir>/{metric}_variance_{pp,ce}_{ps}.png

CPU-only, but run it on a compute node.

Example:
  python visualization/wloss_exp_var_vs_curvature.py \
    --project init_opt_test_3d_refactor_new --ps c1e4_exp1.0
"""
import argparse, glob, json, os, re, statistics, sys

import matplotlib, numpy as np
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.cm import ScalarMappable
from matplotlib.ticker import LogLocator, ScalarFormatter
from matplotlib import colormaps

sys.path.insert(0, os.path.join(
  os.path.dirname(os.path.abspath(__file__)), os.pardir, 'experiments'))
from report import (ENTROPY, REF_RATE, REF_EFF_CHECK,  # noqa: E402
                    REF_EFF_SEVERE)  # one source of truth for H(p) and the tiers

# `_k-<K>` is optional in a run name; this project sweeps it, so it is required
# here. Mirrors experiments/report.py's RUN_RE.
RUN_RE = re.compile(
  r'^ps-(?P<ps>.+?)_k-(?P<k>[^_]+)_lg-(?P<lg>[^_]+)_q-(?P<q>[^_]+?)'
  r'_qref-(?P<qref>[^_]+?)_lr(?P<lr>[^_]+)_st(?P<st>\d+)_s(?P<seed>\d+)$')

GEOMETRIES = {'pp': 'Polar ELBO', 'ce': 'Cross-entropy'}
TEST_SIZE = 4_000_000  # draws behind each run's test_wloss_std
# Loss proposals above this have infinite estimator variance at K = -1
# (measured: L(t) ~ exp(-0.152 t), so the cliff sits at 2*0.152).
VARIANCE_CLIFF = 0.304
# viridis truncated at 0.75: keeps the monotone-lightness ordering while spanning
# four hues, and stops before the pale yellow-green end that would drop a line
# below 2:1 against a white surface (lightest here is 2.10:1).
RAMP = LinearSegmentedColormap.from_list(
  'proposal', colormaps['viridis'](np.linspace(0.0, 0.75, 256)))
# Secondary encoding: seven levels are past what any one ramp separates reliably.
MARKERS = ['o', 's', '^', 'D', 'v', 'P', 'X']
INK, INK_2, INK_3, RULE = '#12161b', '#555e6a', '#868f9b', '#e2dfd8'
REF = '#c8501e'  # the reference/guide line: a status hue, never a series colour


def factors(k: str) -> list:
  """Per-factor curvatures of a `_k-` tag; a scalar tag yields one."""
  return [float(v) for v in k.split('x')]


def is_product(k: str) -> bool:
  """True only when the factors actually DIFFER.

  `sweep_lib.curvature_tag` collapses identical factors to the shared scalar
  (`_k--1.0`), but earlier sweeps wrote them out (`_k--1.0x-1.0x-1.0`, all over
  `prod_manifold_acc_test`). A tag like that is still ONE curvature and belongs
  on the axis; only a genuinely mixed vector has no scalar K.
  """
  return len(set(factors(k))) > 1


def sharpest(k: str) -> float:
  """|K| of the sharpest factor -- the scalar a product manifold is governed by.

  Mirrors report.k_sort_key: main_refactor.py clamps the whole product's heat
  time at the `_radial_t_max(d) * R^2` of its sharpest factor, so that factor is
  what sets the ceiling (and the reference proposal's effective rate) for the
  product as a whole.
  """
  return max(abs(v) for v in factors(k))


def collect(project: str, ps: str):
  """((lg, K, rate) -> [metrics/seed], scalar Ks, product Ks, sorted rates).

  A product-manifold run tags its factors `x`-joined (`_k--0.01x-10.0x-1.0`).
  Such a cell has no single Gaussian curvature, so it cannot sit on the log-|K|
  axis; it is returned separately and drawn in its own column past a break.
  """
  cells, ks, rates = {}, set(), set()
  root = os.path.join('output', project)
  for path in sorted(glob.glob(os.path.join(root, '*', 'test_metrics.json'))):
    m = RUN_RE.match(os.path.basename(os.path.dirname(path)))
    if not m or m['ps'] != ps:
      continue
    cells.setdefault((m['lg'], m['k'], m['q']), []).append(json.load(open(path)))
    ks.add(m['k']); rates.add(m['q'])
  if not cells:
    raise SystemExit(f'no runs matched ps={ps!r} under {root}/')
  scalar = sorted((k for k in ks if not is_product(k)),
                  key=lambda k: abs(factors(k)[0]))
  if not scalar:
    raise SystemExit(f'ps={ps!r} under {root}/ has only mixed-curvature cells, '
                     'so there is no curvature axis to plot them against')
  # flattest first: |K| ascending is left-to-right on the log x axis
  return (cells, scalar,
          sorted((k for k in ks if is_product(k)), key=sharpest),
          sorted(rates, key=lambda q: float(q[3:])))


def statistic(runs: list, stat: str, metric: str = 'wloss'):
  """(value, half-error-bar) of `metric` for one cell."""
  if stat == 'mean':
    # Error bar is the estimator's own standard error, not the seed spread:
    # each run averages 4e6 draws, so this is what the mean is worth.
    return (statistic(runs, 'mean_only', metric),
            statistic(runs, 'variance', metric) ** 0.5 / TEST_SIZE ** 0.5)
  if stat == 'mean_only':
    return statistics.mean(r[f'test_{metric}'] for r in runs)
  # test_<metric>_std is the pooled per-sample std over the 4e6-draw test pass.
  return statistics.mean(r[f'test_{metric}_std'] ** 2 for r in runs)


def _spread_labels(ax, ends, x, side: str = 'right', min_gap_px: float = 12.0) -> None:
  """Place end labels at their line's y, nudged apart to a minimum pixel gap.

  `side` is the end being labelled -- callers pick whichever end the lines fan
  out at, since a label column is only useful where the lines are apart.

  Greedy sweep from the bottom: each label sits at its own value unless that
  would land within `min_gap_px` of the one below, in which case it is pushed
  up. Leaders are drawn wherever a label had to move, so a nudged label still
  points at its own line. Without this the lines converge to within a few pixels
  and the labels stack into an unreadable pile.
  """
  ax.figure.canvas.draw()  # scales and limits must be final to map to pixels
  to_px, to_data = ax.transData.transform, ax.transData.inverted().transform
  rows = sorted(((to_px((x, y))[1], y, col, txt) for y, col, txt in ends))
  placed, prev = [], -float('inf')
  for py, y, col, txt in rows:
    npy = max(py, prev + min_gap_px)
    placed.append((npy, py, y, col, txt))
    prev = npy
  # The sweep only ever pushes UP, so lines converging near the top of the frame
  # stack their labels out through the title. Slide the whole column back down
  # by whatever room is left underneath it.
  lo_px, hi_px = (to_px((x, v))[1] for v in ax.get_ylim())
  overflow = placed[-1][0] - hi_px
  if overflow > 0:
    shift = min(overflow, max(0.0, placed[0][0] - lo_px))
    placed = [(npy - shift, py, y, col, txt) for npy, py, y, col, txt in placed]
  dx, ha = ((9, 'left') if side == 'right' else (-9, 'right'))
  for npy, py, y, col, txt in placed:
    y_lab = to_data((to_px((x, y))[0], npy))[1]
    ax.annotate(txt, (x, y_lab), xytext=(dx, 0), textcoords='offset points',
                va='center', ha=ha, color=col, fontsize=8.5, fontweight='medium',
                annotation_clip=False,
                arrowprops=None if abs(npy - py) < 0.5 else dict(
                  arrowstyle='-', color=col, linewidth=0.8, alpha=0.55,
                  shrinkA=2, shrinkB=1))


def plot(cells, ks, rates, lg, ps, stat, out, metric, model_label,
         prod_ks=()) -> str:
  fig, ax = plt.subplots(figsize=(9.4, 5.8))
  fig.patch.set_facecolor('white'); ax.set_facecolor('white')
  xs = [abs(factors(k)[0]) for k in ks]
  # Product manifolds have no scalar K, so they get their own column past a
  # break instead of a place on the continuous |K| scale. Parked on the SHARP
  # side because the sharpest factor is what governs the product.
  pxs = [max(xs) * 4.0 * 2.2 ** i for i in range(len(prod_ks))]
  lams = [float(q[3:]) for q in rates]
  norm = LogNorm(vmin=min(lams), vmax=max(lams))
  # `wloss` IS the geometry `lg` names; `wnelbo_ref` is the poincare-polar ELBO
  # on the reference path whatever the model was trained with. So H(p) is the
  # right target for both panels once the metric is wnelbo_ref.
  measures_elbo = (metric == 'wnelbo_ref' or lg == 'pp')
  # The ELBO's expectation has an exact target; every other panel spans decades.
  # wnelbo_ref on a TRAINED grid spans decades too (diverged cells reach ~25 nats
  # while the truncation-biased flat-K end reaches ~1e-9), so it stays log.
  linear_y = (stat == 'mean' and lg == 'pp' and metric == 'wloss')

  ends, all_y = [], []
  for i, (q, lam) in enumerate(zip(rates, lams)):
    got = [(x, statistic(cells[(lg, k, q)], stat, metric))
           for x, k in zip(xs, ks) if (lg, k, q) in cells]
    if not got:
      continue
    col = RAMP(norm(lam))
    past_cliff = lam > VARIANCE_CLIFF
    style = dict(color=col, marker=MARKERS[i % len(MARKERS)], markersize=5.5,
                 linewidth=1.9, linestyle='--' if past_cliff else '-',
                 markeredgecolor='white', markeredgewidth=0.8, zorder=3)
    if stat == 'mean':
      x_v, ye = zip(*got)
      y_v, err = zip(*ye)
      ax.errorbar(x_v, y_v, yerr=err, elinewidth=1.2, capsize=2.5,
                  ecolor=col, **style)
    else:
      x_v, y_v = zip(*got)
      ax.plot(x_v, y_v, **style)
    ends.append((y_v[0], y_v[-1], col, f'{lam:g}' + ('!' if past_cliff else '')))
    all_y.extend(y_v)

    # Same colour and marker, but never joined by a line: these are not a
    # continuation of the curvature sweep, they are separate geometries.
    got_p = [(x, statistic(cells[(lg, k, q)], stat, metric))
             for x, k in zip(pxs, prod_ks) if (lg, k, q) in cells]
    if got_p:
      px_v, pye = zip(*got_p)
      if stat == 'mean':
        py_v, perr = zip(*pye)
        ax.errorbar(px_v, py_v, yerr=perr, elinewidth=1.2, capsize=2.5,
                    ecolor=col, **dict(style, linestyle='none'))
      else:
        py_v = pye
        ax.plot(px_v, py_v, **dict(style, linestyle='none'))
      all_y.extend(py_v)

  ax.set_xscale('log')
  if not linear_y:
    ax.set_yscale('log')

  # Reference: what an unbiased estimator must return.
  if stat == 'mean' and measures_elbo and ps in ENTROPY:
    ax.axhline(ENTROPY[ps], color=REF, linewidth=1.5, linestyle=(0, (5, 4)),
               zorder=2)
    # Every honest lambda converges ON H(p), so on the wnelbo_ref panels this
    # label lands exactly where the lines bunch up. Back it so it stays readable.
    over = dict(zorder=4, bbox=dict(facecolor='white', edgecolor='none',
                                    alpha=0.82, pad=1.5))
    ax.annotate(f'H(p) = {ENTROPY[ps]:.4f}', (xs[0], ENTROPY[ps]),
                xytext=(2, 7), textcoords='offset points', color=REF,
                fontsize=9.5, fontweight='medium',
                **(over if metric == 'wnelbo_ref' else {}))
  if stat == 'mean' and metric == 'wloss' and lg == 'ce':
    # Measured: the weighted CE integral is proportional to R^2 = 1/|K|.
    anchor = statistic(cells[(lg, ks[-1], rates[0])], 'mean_only')
    ax.plot(xs, [anchor * xs[-1] / x for x in xs], color=REF, linewidth=1.5,
            linestyle=(0, (5, 4)), zorder=2)
    ax.annotate('$\\propto R^2 = 1/|K|$', (xs[0], anchor * xs[-1] / xs[0]),
                xytext=(4, 6), textcoords='offset points', color=REF,
                fontsize=9.5, fontweight='medium')

  # Inside the shaded band below, the estimator standard error is the size of the
  # value itself, so a symmetric error bar reaches <= 0 -- meaningless on a log
  # axis, and it stretches the frame until the real signal occupies a sliver of
  # it. Scale the frame to the MEANS (and to H(p), which must stay visible) and
  # let those whiskers run off the top and bottom.
  if stat == 'mean' and metric == 'wnelbo_ref' and all_y:
    span = all_y + ([ENTROPY[ps]] if ps in ENTROPY else [])
    ax.set_ylim(min(span) / 1.6, max(span) * 1.6)

  ax.set_xlim(min(xs) * 0.6, pxs[-1] * 1.7 if pxs else max(xs) * 2.6)
  if pxs:
    # Break rule: everything right of it is off the curvature scale.
    ax.axvline((max(xs) * pxs[0]) ** 0.5, color=INK_3, linewidth=1.0,
               linestyle=(0, (2, 3)), zorder=1)
  # The reference proposal is pinned in physical time, so it runs at an effective
  # dimensionless rate of REF_RATE/|K|. report.py grades that in two tiers, and
  # the tiers are NOT interchangeable: its measured table shows a 3-factor D=9
  # product still SOUND at effective rate 2 where a D=3 single manifold is
  # already biased -- more factors identify the target faster. So the milder band
  # says "check against the mode=opt control", not "invalid".
  # Shown as shading only; explained in the footnote, because every corner of
  # these bands is occupied by collapsing lines, end labels or H(p).
  if metric == 'wnelbo_ref':
    severe, check = REF_RATE / REF_EFF_SEVERE, REF_RATE / REF_EFF_CHECK
    left = ax.get_xlim()[0]
    if min(xs) < check:
      ax.axvspan(max(left, severe), check, color=REF, alpha=0.06, zorder=0)
    if min(xs) <= severe:
      ax.axvspan(left, severe, color=REF, alpha=0.15, zorder=0)
  ax.set_xticks(xs + pxs)
  ax.set_xticklabels([f'{factors(k)[0]:g}' for k in ks]
                     + ['×'.join(f'{v:g}' for v in factors(k))
                        for k in prod_ks])
  ax.tick_params(axis='x', length=0, pad=6, labelsize=9.5, colors=INK_2)
  for lab in ax.get_xticklabels()[len(xs):]:
    lab.set_fontsize(8.5); lab.set_color(INK_3)
  ax.tick_params(axis='y', labelsize=9, colors=INK_2)
  ax.minorticks_off()
  # A log axis spanning under a decade carries a single major tick, which reads
  # as an unlabelled axis. There, label the decade subdivisions instead, in plain
  # numbers -- 0.4 / 0.6 / 1 beats a lone 10^0.
  if not linear_y:
    y_lo, y_hi = ax.get_ylim()
    if y_hi / y_lo < 25:
      ax.yaxis.set_minor_locator(LogLocator(subs=tuple(range(2, 10))))
      ax.yaxis.set_minor_formatter(ScalarFormatter())
      ax.yaxis.set_major_formatter(ScalarFormatter())
      ax.tick_params(axis='y', which='minor', labelsize=8.5, colors=INK_2)
      ax.grid(axis='y', which='minor', color=RULE, linewidth=0.5, zorder=0)

  if stat == 'mean':
    # Kept short: with four footnote lines the axes shrink until a longer
    # rotated label overruns them. The title already says "reference ELBO".
    what = ('reference ELBO' if metric == 'wnelbo_ref' else
            'negative ELBO estimate' if lg == 'pp' else 'weighted CE integral')
    ylab = f'E[{metric}]   ({what}, nats)' + ('' if linear_y else '   (log scale)')
  else:
    # Kept short for wnelbo_ref: the longer name plus the extra footnote line
    # squeezes the axes until the rotated label clips off the canvas.
    ylab = (f'per-sample variance of {metric}, seed-averaged   (log scale)'
            if metric == 'wnelbo_ref' else
            'per-sample variance of wloss (averaged across seeds)   (log scale)')
  ax.set_ylabel(ylab, fontsize=11, color=INK)
  ax.set_xlabel('Gaussian curvature $K$   '
                '(flatter, $R^2=1/|K|$ large $\\leftarrow$   $\\rightarrow$ sharper)',
                fontsize=11, color=INK, labelpad=9)
  head = ('expectation' if stat == 'mean' else 'estimator variance')
  lead = (f'{GEOMETRIES[lg]}: {head}' if metric == 'wloss' else
          f'{GEOMETRIES[lg]}-trained: reference ELBO {head}')
  ax.set_title(f'{lead} vs curvature\n'
               f'{ps} · {model_label} · {len(ks)} curvatures'
               + (f' + {len(prod_ks)} product' if prod_ks else '')
               + f' × {len(rates)} proposal rates',
               fontsize=12.5, color=INK, loc='left', pad=14)

  ax.grid(axis='y', color=RULE, linewidth=0.8, zorder=0)
  ax.set_axisbelow(True)
  for side in ('top', 'right'):
    ax.spines[side].set_visible(False)
  for side in ('left', 'bottom'):
    ax.spines[side].set_color(RULE)

  # Label the end where the lines are actually separated. On the ELBO
  # expectation panel every lambda converges on H(p) at sharp curvature and fans
  # out at flat curvature, so the useful column is the left one.
  def _spread(vals):
    lo, hi = min(vals), max(vals)
    return (hi / lo if (not linear_y and lo > 0) else hi - lo)
  left_first = _spread([e[0] for e in ends]) > _spread([e[1] for e in ends])
  _spread_labels(ax, [(e[0] if left_first else e[1], e[2], e[3]) for e in ends],
                 xs[0] if left_first else xs[-1],
                 side='left' if left_first else 'right')

  cb = fig.colorbar(ScalarMappable(norm=norm, cmap=RAMP), ax=ax, pad=0.055,
                    fraction=0.04)
  cb.set_label('proposal rate $\\lambda$   (exp proposal, log scale)',
               fontsize=10, color=INK_2)
  cb.set_ticks(lams)
  cb.set_ticklabels([f'{l:g}' for l in lams])
  cb.ax.tick_params(labelsize=8.5, colors=INK_2, length=2)
  cb.outline.set_edgecolor(RULE)

  tail = (f'\nError bars are the estimator standard error over {TEST_SIZE:.0e} '
          'draws.' if stat == 'mean' else '')
  band = (f'\nShaded: pinned exp({REF_RATE:g}) reference, effective rate '
          f'${REF_RATE:g}/|K|$ — light $> {REF_EFF_CHECK:g}$ (check vs the '
          f'mode=opt control), dark $\\geq {REF_EFF_SEVERE:g}$ (invalid).'
          if metric == 'wnelbo_ref' else '')
  prod = ('\nRight of the dotted rule: product manifolds — no scalar $K$, off the '
          'curvature scale, drawn unjoined; governed by their sharpest factor.'
          if prod_ks else '')
  fig.text(0.01, 0.015,
           f'Dashed / "!" = $\\lambda$ above the ~{VARIANCE_CLIFF} variance cliff '
           'measured at $K=-1$; it scales as $1/R^2$, so it moves with '
           f'curvature.{tail}{band}{prod}',
           fontsize=8.5, color=INK_3, va='bottom', linespacing=1.5)
  # 8.5pt at linespacing 1.5 is ~0.030 of the 5.8in canvas per extra line; at
  # 0.023 a fourth line runs into the x label and the rotated y label.
  fig.tight_layout(rect=(0, (0.055 if stat == 'mean' else 0.035)
                         + (0.030 if band else 0) + (0.030 if prod else 0), 1, 1))
  fig.savefig(out, dpi=150, facecolor='white')
  plt.close(fig)
  return out


def main():
  p = argparse.ArgumentParser(description=__doc__,
                              formatter_class=argparse.RawDescriptionHelpFormatter)
  p.add_argument('--project', default='init_opt_test_3d_refactor_new')
  p.add_argument('--ps', default='c1e4_exp1.0')
  p.add_argument('--stat', choices=['mean', 'variance', 'both'], default='both')
  p.add_argument('--metric', choices=['wloss', 'wnelbo_ref'], default='wloss',
                 help='wloss = the trained objective; wnelbo_ref = the '
                      'reference-path ELBO, measured the same way for both lg')
  p.add_argument('--model-label', default='Bayes-optimal model',
                 help='subtitle text; pass e.g. "trained MLP" for a mode=tnb '
                      'project')
  p.add_argument('--out-dir', default=None,
                 help='default experiments/{project}/imgs')
  args = p.parse_args()

  out_dir = args.out_dir or os.path.join('experiments', args.project, 'imgs')
  os.makedirs(out_dir, exist_ok=True)
  cells, ks, prod_ks, rates = collect(args.project, args.ps)
  print(f'{args.ps}: {len(ks)} curvatures {[factors(k)[0] for k in ks]}, '
        f'{len(rates)} rates {[float(q[3:]) for q in rates]}')
  if prod_ks:
    print(f'  + {len(prod_ks)} product manifold(s), off the curvature scale: '
          f'{prod_ks} (sharpest factor |K| = '
          f'{[sharpest(k) for k in prod_ks]})')

  stats = ['mean', 'variance'] if args.stat == 'both' else [args.stat]
  for stat in stats:
    for lg in GEOMETRIES:
      if not any(key[0] == lg for key in cells):
        print(f'  [skip] no {lg} runs for ps={args.ps}')
        continue
      out = os.path.join(out_dir, f'{args.metric}_{stat}_{lg}_{args.ps}.png')
      print(f'wrote {plot(cells, ks, rates, lg, args.ps, stat, out, args.metric, args.model_label, prod_ks)}')


if __name__ == '__main__':
  main()
