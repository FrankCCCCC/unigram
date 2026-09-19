#!/usr/bin/env python
"""Spectrum of a run's word-embedding matrix E = lm_head.weight.

E is [V, d] and rectangular, so it has no eigenvalues; the two well-defined
spectral quantities, both plotted here, are

  sigma_i   the d singular values of E
  lambda_i  the d eigenvalues of the Gram matrix E^T E, = sigma_i^2

Codebook variants per run:
  raw                    E exactly as trained (the nn.Linear parameter)
  normalized             every row projected onto the unit sphere
  normalized-mean-shift  normalize, then subtract the mean direction
  mean-shift-normalized  subtract the mean row, then normalize

Checkpoints are the `model.pt` state dicts main_refactor.py writes at the end of
a run. `lm_head.weight` IS the word embedding -- row v is word v's boundary
point (see MLPLMRefactor.word_embedding) -- and is read straight out of the
state dict, so no model is rebuilt and no config is needed.

Outputs, per run and per variant:
  <out-dir>/codebook_eigen_dist_{run}_{variant}[_logx].png
                             2x2 fine histograms; rows = (sigma,
                             lambda), columns = (count, portion), log y
                             throughout (portion = count / d, so the columns
                             differ only by that constant factor). Dashed line
                             = median. The spectrum is heavy-tailed, so the
                             `_logx` pass repeats it with log-spaced bins --
                             read that one to see the bulk.

CPU-only, but run it on a compute node.

Example:
  python visualization/codebook_eign_dist.py \
    --ckpt output/init_opt_3x3d_ada_prod/pre_trained_models/*/model.pt \
    --out-dir experiments/init_opt_3x3d_ada_prod/imgs \
    --variants normalized-mean-shift,normalized
"""
import argparse, os

import matplotlib, numpy as np, torch
matplotlib.use('Agg')
import matplotlib.pyplot as plt

XLABELS = {'sigma': r'singular value $\sigma_i(E)$',
           'lambda': r'eigenvalue $\lambda_i(E^\top E) = \sigma_i^2$'}


@torch.no_grad()
def embedding_matrices(ckpt: str) -> dict:
  """variant -> [V, d] word-embedding matrix, read out of the `model.pt` state dict."""
  W = torch.load(ckpt, map_location='cpu')['lm_head.weight'].double()
  normalized = torch.nn.functional.normalize(W, p=2.0, dim=-1)
  return {'raw': W,
          'normalized': normalized,
          'normalized-mean-shift': normalized - normalized.mean(dim=0),
          'mean-shift-normalized': torch.nn.functional.normalize(
            W - W.mean(dim=0), p=2.0, dim=-1)}


def spectrum(W: torch.Tensor) -> dict:
  """The d singular values of E and the matching Gram eigenvalues sigma^2."""
  sigma = torch.linalg.svdvals(W).numpy()
  return {'sigma': sigma, 'lambda': sigma ** 2}


def plot_histograms(spec: dict, run: str, variant: str, shape, out: str,
                    bins: int, log_x: bool):
  """<out>_{variant}[_logx].png: rows = (sigma, lambda), cols = (count, portion).

  The spectrum is heavy-tailed (a handful of sigma_i are ~20x the bulk), so
  linearly spaced bins put ~99% of the d values in the leftmost few; the log_x
  pass re-bins geometrically to resolve that bulk.
  """
  V, d = shape
  fig, axes = plt.subplots(2, 2, figsize=(11, 8))
  for row, (kind, vals) in enumerate(spec.items()):
    edges = (np.geomspace(vals.min() * 0.98, vals.max() * 1.02, bins + 1)
             if log_x else np.linspace(0.0, vals.max() * 1.02, bins + 1))
    for col, (ylabel, w) in enumerate(
        [('count', None),
         ('portion of spectrum', np.full(vals.size, 1.0 / vals.size))]):
      ax = axes[row, col]
      ax.hist(vals, bins=edges, weights=w, color='C0')
      ax.axvline(np.median(vals), color='r', ls='--', lw=1.2,
                 label=f'median={np.median(vals):.4g}')
      ax.set_yscale('log')
      if log_x:
        ax.set_xscale('log')
      ax.set(xlabel=XLABELS[kind], ylabel=f'log {ylabel}',
             title=f'{kind}: max={vals.max():.4g}, min={vals.min():.4g}')
      ax.grid(alpha=0.3); ax.legend(fontsize=8)
  fig.suptitle(f'{run}\n[{variant}] word-embedding spectrum   '
               f'(V={V}, d={d}, {bins} '
               f'{"log-spaced" if log_x else "linear"} bins)', fontsize=11)
  fig.tight_layout()
  path = f'{out}_{variant}{"_logx" if log_x else ""}.png'
  fig.savefig(path, dpi=150); plt.close(fig)
  print(f'wrote {path}')


def main():
  p = argparse.ArgumentParser(description=__doc__)
  p.add_argument('--ckpt', required=True, nargs='+',
                 help='one or more run checkpoints ({run}/model.pt)')
  p.add_argument('--out-dir', default=None,
                 help='output directory; default experiments/{project}/imgs')
  # The codebook is (V, d) with d = hyper_dim, so the spectrum holds only d
  # values -- 9 for a 3x3d product run. 200 bins (the count that suited a
  # d ~ 1000 transformer codebook) would leave every bar isolated.
  p.add_argument('--bins', type=int, default=20)
  p.add_argument('--variants', default=None,
                 help='comma-separated subset of the variants to plot; '
                      'default: all of them')
  args = p.parse_args()

  for ckpt in args.ckpt:
    run_dir = os.path.dirname(os.path.abspath(ckpt))
    run = os.path.basename(run_dir)
    out_dir = args.out_dir or os.path.join(
      'experiments', os.path.basename(os.path.dirname(run_dir)), 'imgs')
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f'codebook_eigen_dist_{run}')

    mats = embedding_matrices(ckpt)
    if args.variants:
      mats = {k: mats[k] for k in args.variants.split(',')}
    for variant, W in mats.items():
      spec = spectrum(W)
      lam = spec['lambda']
      print(f'{run} [{variant}] E{tuple(W.shape)}  row-norm median='
            f'{W.norm(dim=1).median():.4g}  sigma: max={spec["sigma"].max():.4g} '
            f'min={spec["sigma"].min():.4g}  '
            f'stable rank ||E||_F^2/sigma_max^2={lam.sum() / lam.max():.2f}',
            flush=True)
      for log_x in (False, True):
        plot_histograms(spec, run, variant, tuple(W.shape), out, args.bins,
                        log_x)


if __name__ == '__main__':
  main()
