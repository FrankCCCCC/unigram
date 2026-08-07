#!/usr/bin/env python
"""Draw a log-Y companion to every loss_curves.jpg in a project.

    python experiments/plot_logy.py init_test

For each output/{project}/{run}/loss_history.json this writes
{run}/loss_curves_logy.jpg alongside the existing linear-axis figure. The losses
fall by an order of magnitude in the first few hundred steps, so on a linear axis
everything after that is squashed into the bottom of the plot.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parents[1]
# this script lives in experiments/, so sys.path[0] is experiments/ -- the repo
# root has to be added explicitly before importing the project modules.
sys.path.insert(0, str(REPO_DIR))

from visualizer import Recorder, plot_loss_curves  # noqa: E402


def load_recorder(path: Path) -> Recorder:
    recorder = Recorder()
    for name, items in json.load(path.open()).items():
        recorder.history_dict[name] = [
            (int(d["step"]), float(d["value"])) for d in items
        ]
    return recorder


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project")
    ap.add_argument("--name", default="loss_curves_logy.jpg")
    ap.add_argument("--force", action="store_true",
                    help="redraw even if the log-Y figure already exists")
    args = ap.parse_args()

    root = REPO_DIR / "output" / args.project
    done = skipped = failed = 0
    for run in sorted(p for p in root.iterdir() if p.is_dir()):
        src = run / "loss_history.json"
        if not src.exists():
            continue
        dst = run / args.name
        if dst.exists() and not args.force:
            skipped += 1
            continue
        try:
            plot_loss_curves(
                recorder=load_recorder(src),
                output_path=dst,
                title=f"{run.name}\nloss vs steps (log y)",
                log_y=True,
            )
            done += 1
        except Exception as exc:  # noqa: BLE001 - report and keep going
            print(f"  FAILED {run.name}: {exc!r}")
            failed += 1
    print(f"drawn: {done}   already present: {skipped}   failed: {failed}")


if __name__ == "__main__":
    main()
