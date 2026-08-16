#!/usr/bin/env python
"""Per-cell reproduction check: does a *_refactor project match its reference?

    python experiments/compare_reproduction.py init_opt_test_refactor init_opt_test

Both projects use the same run_name layout, so cells pair 1:1 by directory name.
For every paired cell this loads both test_metrics.json files and reports the
per-metric relative difference, then summarizes: how many cells reproduced
exactly, how many within tolerance, and the worst offenders.

Why relative and not absolute: test_wce_ref runs ~2.4 for naive_ps and ~6.8 for
cmplx_ps, and the *_std columns run to ~38, so a single absolute threshold would
be far too loose on the small metrics and too tight on the large ones.

Exit status is 1 if any paired cell exceeds --tol on any metric, so this can gate
a "reproduction confirmed" claim rather than just printing numbers.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parents[1]

METRICS = [
    "test_wloss",
    "test_wnelbo_ref",
    "test_wce_ref",
    "test_nelbo_ref",
    "test_ce_ref",
    "test_wloss_std",
    "test_wnelbo_ref_std",
    "test_wce_ref_std",
]


def load(project: str) -> dict[str, dict]:
    root = REPO_DIR / "output" / project
    out = {}
    if not root.is_dir():
        return out
    for d in sorted(root.iterdir()):
        f = d / "test_metrics.json"
        if f.is_file():
            try:
                out[d.name] = json.load(open(f))
            except json.JSONDecodeError:
                pass
    return out


def rel(a: float, b: float) -> float:
    """Relative difference, scale-free and safe at zero."""
    if a == b:
        return 0.0
    denom = max(abs(a), abs(b))
    return math.inf if denom == 0 else abs(a - b) / denom


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("refactor", help="project under test, e.g. init_opt_test_refactor")
    ap.add_argument("reference", help="project to reproduce, e.g. init_opt_test")
    ap.add_argument("--tol", type=float, default=1e-9,
                    help="max tolerated relative difference (default: 1e-9, i.e. "
                         "effectively bit-exact)")
    ap.add_argument("--show", type=int, default=10, help="worst cells to list")
    args = ap.parse_args()

    new, ref = load(args.refactor), load(args.reference)
    paired = sorted(set(new) & set(ref))

    print(f"refactor  : output/{args.refactor}/            {len(new):4d} cells with metrics")
    print(f"reference : output/{args.reference}/           {len(ref):4d} cells with metrics")
    print(f"paired    : {len(paired)} cells   (tol = {args.tol:g} relative)")
    only_new, only_ref = sorted(set(new) - set(ref)), sorted(set(ref) - set(new))
    if only_new:
        print(f"  [warn] {len(only_new)} cells only in refactor (no reference to compare)")
    if only_ref:
        print(f"  [note] {len(only_ref)} reference cells not yet reproduced "
              f"(still running, or out of grid)")
    if not paired:
        print("\nNothing to compare yet.")
        raise SystemExit(0)

    # worst relative diff per metric, and per cell
    per_metric = {m: (0.0, None) for m in METRICS}
    per_cell: list[tuple[float, str, str]] = []
    missing_keys = 0
    for name in paired:
        worst, worst_m = 0.0, None
        for m in METRICS:
            if m not in new[name] or m not in ref[name]:
                missing_keys += 1
                continue
            r = rel(new[name][m], ref[name][m])
            if r > per_metric[m][0]:
                per_metric[m] = (r, name)
            if r > worst:
                worst, worst_m = r, m
        per_cell.append((worst, name, worst_m or "-"))

    exact = sum(1 for w, _, _ in per_cell if w == 0.0)
    within = sum(1 for w, _, _ in per_cell if w <= args.tol)
    print(f"\nbit-exact         : {exact}/{len(paired)}")
    print(f"within tol        : {within}/{len(paired)}")
    if missing_keys:
        print(f"  [warn] {missing_keys} metric keys missing on one side")

    print("\nworst relative difference per metric")
    for m in METRICS:
        r, where = per_metric[m]
        flag = "" if r <= args.tol else "   <-- EXCEEDS TOL"
        print(f"  {m:22s} {r:.3e}{flag}")
        if r > args.tol and where:
            print(f"  {'':22s} at {where}")
            print(f"  {'':22s} refactor={new[where][m]!r}")
            print(f"  {'':22s} reference={ref[where][m]!r}")

    bad = sorted((c for c in per_cell if c[0] > args.tol), reverse=True)
    if bad:
        print(f"\n{len(bad)} cells exceed tol; worst {min(args.show, len(bad))}:")
        for w, name, m in bad[:args.show]:
            print(f"  {w:.3e}  {m:20s}  {name}")

    verdict = "REPRODUCED" if not bad else "MISMATCH"
    print(f"\nVERDICT: {verdict}  ({within}/{len(paired)} paired cells within tol)")
    raise SystemExit(0 if not bad else 1)


if __name__ == "__main__":
    main()
