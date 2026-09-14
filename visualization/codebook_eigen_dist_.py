#!/usr/bin/env python
"""Spectrum of a run's normalized word-embedding matrix E = lm_head.weight.

E is [V, d] and rectangular, so it has no eigenvalues; the two well-defined
spectral quantities, both plotted here, are

  sigma_i   the d singular values of E
  lambda_i  the d eigenvalues of the Gram matrix E^T E, = sigma_i^2

The codebook is row-normalized first. The bridge and the polar losses only ever
read each row's DIRECTION -- word v's boundary point is e_v / |e_v| on
S^{d-1} (see HyperbolicDLM.word_embedding / HyperBridge._binary_vocab_angles) --
so the unit-row codebook is the one the geometry actually sees. Row norms then
carry no weight and sum_i lambda_i = V exactly, which is the scale to read the
bars against: lambda_i == V/d for a codebook spread isotropically over the
sphere, lambda_1 -> V for one collapsed onto a line.

Checkpoints are the `model.pt` state dicts main.py writes at the end of a `tnb`
run; `lm_head.weight` is read straight out of the state dict rather than by
rebuilding MLPLM, because the vocab_size recorded in .hydra/config.yaml is the
pre-override default (main overwrites cfg.vocab_size from len(ps) after the
config is dumped) and would not match.

Outputs, per run:
  <out-dir>/codebook_eigen_dist_{run}[_logx].png   2x2 fine histograms; rows =
                             (sigma, lambda), columns = (count, portion), log y
                             throughout (portion = count / d, so the columns
                             differ only by that constant factor). Dashed line
                             = median. The spectrum is heavy-tailed, so the
                             `_logx` pass repeats it with log-spaced bins --
                             read that one to see the bulk.

CPU-only, but run it on a compute node.

Example:
  python visualization/codebook_eigen_dist_.py \
    --ckpt output/init_refactor_9d/*/model.pt \
    --out-dir experiments/init_refactor_9d/images
"""
import argparse, os

import matplotlib, numpy as np, torch
matplotlib.use('Agg')
import matplotlib.pyplot as plt

XLABELS = {'sigma': r'singular value $\sigma_i(E)$',
           'lambda': r'eigenvalue $\lambda_i(E^\top E) = \sigma_i^2$'}


@torch.no_grad()
def normalized_embedding(ckpt: str) -> torch.Tensor:
  """[V, d] lm_head.weight with every row rescaled to unit L2 norm."""
  W = torch.load(ckpt, map_location='cpu')['lm_head.weight'].double()
  return torch.nn.functional.normalize(W, p=2.0, dim=-1)


def spectrum(W: torch.Tensor) -> dict:
  """The d singular values of E and the matching Gram eigenvalues sigma^2."""
  sigma = torch.linalg.svdvals(W).numpy()
  return {'sigma': sigma, 'lambda': sigma ** 2}


def plot_histograms(spec: dict, run: str, shape, out: str, bins: int,
                    log_x: bool):
  """<out>[_logx].png: rows = (sigma, lambda), cols = (count, portion).

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
  fig.suptitle(f'{run}\nnormalized word-embedding spectrum   '
               f'(V={V}, d={d}, {bins} '
               f'{"log-spaced" if log_x else "linear"} bins)', fontsize=11)
  fig.tight_layout()
  path = f'{out}{"_logx" if log_x else ""}.png'
  fig.savefig(path, dpi=150); plt.close(fig)
  return path


def main():
  p = argparse.ArgumentParser(description=__doc__)
  p.add_argument('--ckpt', required=True, nargs='+',
                 help='one or more run checkpoints (output/{project}/{run}/model.pt)')
  p.add_argument('--out-dir', default=None,
                 help='output directory; default experiments/{project}/images')
  # The codebook is (V, d) with d = hyper_dim, so the spectrum has only d values
  # -- 9 for init_refactor_9d. 200 bins (the count that suited a d ~ 1000
  # transformer codebook) would leave every bar isolated.
  p.add_argument('--bins', type=int, default=20)
  args = p.parse_args()

  for ckpt in args.ckpt:
    run_dir = os.path.dirname(os.path.abspath(ckpt))
    run = os.path.basename(run_dir)
    out_dir = args.out_dir or os.path.join(
      'experiments', os.path.basename(os.path.dirname(run_dir)), 'images')
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f'codebook_eigen_dist_{run}')

    W = normalized_embedding(ckpt)
    spec = spectrum(W)
    lam = spec['lambda']
    print(f'{run}: E{tuple(W.shape)}  sigma: max={spec["sigma"].max():.4g} '
          f'min={spec["sigma"].min():.4g}  '
          f'stable rank ||E||_F^2/sigma_max^2={lam.sum() / lam.max():.2f}',
          flush=True)
    for log_x in (False, True):
      print(f'  wrote {plot_histograms(spec, run, tuple(W.shape), out, args.bins, log_x)}',
            flush=True)


if __name__ == '__main__':
  main()
