#!/usr/bin/env python
"""Scan a project's runs and write experiments/{project}/RESULTS.md.

    python experiments/report.py init_test

Reads every output/{project}/{run_name}/test_metrics.json, parses the swept
variables back out of {run_name}, and emits the table layout defined in
experiments/{project}/setup.md: one section per (ps, max_steps), each holding a
CE table and a Polar-ELBO table, one row per loss proposal.

Every setup.md's "Result Presentation" asks for the POINT-ESTIMATE mean and
variance, each averaged across the 3 seeds, so a cell reads "mean / variance":

    mean      avg over seeds of test_<metric>          -- the point estimate
    variance  avg over seeds of test_<metric>_std**2   -- the PER-SAMPLE variance
              of the 4e6-draw test pass, in nats^2

Note this is NOT the across-seed spread the tables used to print: that was a
3-sample std of the mean, smaller by a factor of ~sqrt(4e6) and squared. The two
are related by  across-seed std ~= sqrt(variance / test_size).

The headline metric is wnelbo_ref: the poincare-polar ELBO measured on the
reference pass, whose proposal is pinned to exp(0.1) for every cell, so it is
comparable across cells TRAINED at different loss proposal rates. It is bounded
below by H(p) -- a value under H(p) means the estimator, not the model, is at
fault.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parents[1]

# Analytic entropies of the shipped ps specs; the ELBO cannot beat these.
# The c1e*_exp1.0 specs are the same geometric distribution p_i ∝ e^-i truncated
# at V = 100/1000/10000, so they share one entropy: the analytic
# geometric(q=e^-1) value -log(1-q) + q/(1-q) = 1.0406518523.
ENTROPY = {"naive_ps": 0.500288, "cmplx_ps": 1.666363, "cmplx_ps1": 2.298544,
           "c1e2_exp1.0": 1.040652, "c1e3_exp1.0": 1.040652,
           "c1e4_exp1.0": 1.040652, "c1e5_exp1.0": 1.040652}

# Loss-path proposal rates above this have infinite estimator variance
# (measured: L(t) ~ exp(-0.152 t), so the cliff sits at 2*0.152).
VARIANCE_CLIFF = 0.304

# setup.md column order -> (mean key, per-sample std key or None).
# trainer.BaseTrainer.STD_KEYS records a std for the three WEIGHTED quantities
# only, so the unweighted nelbo_ref / ce_ref have no per-sample variance in any
# existing run. Their variance renders as "n/r" rather than being dropped.
COLUMNS = [
    ("wloss", "test_wloss", "test_wloss_std"),
    ("wnelbo_ref", "test_wnelbo_ref", "test_wnelbo_ref_std"),
    ("wce_ref", "test_wce_ref", "test_wce_ref_std"),
    ("nelbo_ref", "test_nelbo_ref", None),
    ("ce_ref", "test_ce_ref", None),
]
# Draws behind each run's *_std, from setup.md's test_size. Only used to explain
# the relation to the old across-seed spread in the header note.
TEST_SIZE = 4_000_000
NOT_RECORDED = "n/r"
GEOMETRY_TITLE = [("ce", "CE"), ("pp", "Polar ELBO")]
# Dense table: one wloss column per loss_geometry. NELBO and CE are both wloss,
# measured with loss_geometry set to poincare_polar / cross_entropy.
DENSE_COLUMNS = [("NELBO", "pp"), ("CE", "ce")]
DENSE_NOTE = ("NELBO, CE are wloss while setting loss = polar_poincare_disk and "
              "cross_entropy respectively")
# Section order follows setup.md, not the alphabetical directory listing.
PS_ORDER = ["naive_ps", "cmplx_ps", "cmplx_ps1",
            "c1e2_exp1.0", "c1e3_exp1.0", "c1e4_exp1.0", "c1e5_exp1.0"]
# Everything from this heading to the end of an existing RESULTS.md is written by
# hand, not by this script, so it is carried across a regeneration verbatim.
HANDWRITTEN_MARKER = "# Insights and conclusions"

# `_k-<gaussian_curvature>` is optional: projects that sweep curvature put it in
# the run name, projects whose geometry is fixed keep it in the project name.
RUN_RE = re.compile(
    r"^ps-(?P<ps>.+?)(?:_k-(?P<k>[^_]+))?_lg-(?P<lg>[^_]+)_q-(?P<q>[^_]+?)"
    r"_qref-(?P<qref>[^_]+?)_lr(?P<lr>[^_]+)_st(?P<st>\d+)_s(?P<seed>\d+)$"
)


def rate_of(q: str) -> float:
    try:
        return float(q.replace("exp", ""))
    except ValueError:
        return float("nan")


def collect(project: str):
    """(ps, k, steps, lg, q) -> {label: {"mean": [...], "var": [...]}}

    One entry per seed in each list; "var" is empty for metrics whose runs
    recorded no per-sample std.
    """
    root = REPO_DIR / "output" / project
    cells: dict[tuple, dict[str, list[float]]] = {}
    ps_seen, k_seen, steps_seen, missing, unparsed = [], [], set(), 0, []
    for run in sorted(p for p in root.iterdir() if p.is_dir() and p.name != "logs"):
        m = RUN_RE.match(run.name)
        if not m:
            unparsed.append(run.name)
            continue
        f = run / "test_metrics.json"
        if not f.exists():
            missing += 1
            continue
        data = json.load(f.open())
        key = (m["ps"], m["k"], int(m["st"]), m["lg"], m["q"])
        bucket = cells.setdefault(key, {})
        for label, metric_key, std_key in COLUMNS:
            slot = bucket.setdefault(label, {"mean": [], "var": []})
            value = data.get(metric_key)
            if value is not None and math.isfinite(value):
                slot["mean"].append(float(value))
            std = data.get(std_key) if std_key else None
            if std is not None and math.isfinite(std):
                slot["var"].append(float(std) ** 2)
        if m["ps"] not in ps_seen:
            ps_seen.append(m["ps"])
        if m["k"] not in k_seen:
            k_seen.append(m["k"])
        steps_seen.add(int(m["st"]))
    return cells, ps_seen, k_seen, sorted(steps_seen), missing, unparsed


def fmt(slot: dict | None, n_expected: int) -> str:
    """"mean / variance", each averaged across seeds (setup.md)."""
    if not slot or not slot["mean"]:
        return "-"
    means = slot["mean"]
    var = f"{statistics.mean(slot['var']):.4g}" if slot["var"] else NOT_RECORDED
    cell = f"{statistics.mean(means):.4f} / {var}"
    return cell if len(means) >= n_expected else f"{cell} (n={len(means)})"


def table(cells, ps: str, k: str | None, steps: int, lg: str,
          rates: list[str], n_expected: int) -> list[str]:
    header = "| loss Proposal | " + " | ".join(label for label, _, _ in COLUMNS) + " |"
    lines = [header, "|---" * (1 + len(COLUMNS)) + "|"]
    for q in rates:
        bucket = cells.get((ps, k, steps, lg, q))
        flag = " !" if rate_of(q) > VARIANCE_CLIFF else ""
        row = [q + flag] + [
            fmt(bucket.get(label) if bucket else None, n_expected)
            for label, _, _ in COLUMNS
        ]
        lines.append("| " + " | ".join(row) + " |")
    return lines


def dense_table(cells, ps: str, k: str | None, steps: int,
                rates: list[str], n_expected: int) -> list[str]:
    header = "| Proposal | " + " | ".join(label for label, _ in DENSE_COLUMNS) + " |"
    lines = [header, "|---" * (1 + len(DENSE_COLUMNS)) + "|"]
    for q in rates:
        flag = " !" if rate_of(q) > VARIANCE_CLIFF else ""
        row = [q + flag]
        for _, lg in DENSE_COLUMNS:
            bucket = cells.get((ps, k, steps, lg, q))
            row.append(fmt(bucket.get("wloss") if bucket else None, n_expected))
        lines.append("| " + " | ".join(row) + " |")
    return lines


def section_title(ps: str, k: str | None, steps: int, multi_step: bool) -> str:
    title = f"## {ps}" if k is None else f"## {ps}, K = {k}"
    return f"{title}, Training Step {steps}" if multi_step else title


def handwritten_tail(dest: Path) -> list[str]:
    """The hand-written trailer of an existing RESULTS.md, so regenerating the
    tables does not silently delete the analysis someone wrote under them."""
    if not dest.exists():
        return []
    _, marker, tail = dest.read_text().partition(HANDWRITTEN_MARKER)
    return ["", "---", "", marker + tail.rstrip("\n")] if marker else []


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project")
    ap.add_argument("--seeds", type=int, default=3,
                    help="expected seeds per cell; cells with fewer are marked (n=k)")
    args = ap.parse_args()

    cells, ps_list, k_list, steps_list, missing, unparsed = collect(args.project)
    ps_list.sort(key=lambda p: (PS_ORDER.index(p) if p in PS_ORDER else len(PS_ORDER), p))
    # Curvature sections run from flattest to sharpest; None is the single
    # "geometry fixed by the project name" section.
    k_list.sort(key=lambda x: (x is not None, -float(x) if x is not None else 0.0))
    rates = sorted({key[4] for key in cells}, key=rate_of)
    n_runs = sum(len(v["wnelbo_ref"]["mean"]) for v in cells.values()
                 if "wnelbo_ref" in v)
    total = (len(ps_list) * len(k_list) * len(steps_list)
             * len(GEOMETRY_TITLE) * len(rates) * args.seeds)

    out = [
        f"# {args.project} results",
        "",
        f"- runs collected: **{n_runs}** / {total} "
        f"({n_runs / total:.0%}) — run dirs without test_metrics.json: {missing}",
    ]
    for ps in ps_list:
        if ps in ENTROPY:
            out.append(f"- H({ps}) = **{ENTROPY[ps]:.4f}** — wnelbo_ref is bounded below by this")
    out += [
        "- Each cell is **`mean / variance`**, both averaged across the 3 seeds, as",
        "  setup.md's \"Result Presentation\" asks: `mean` is the point estimate",
        "  (avg of `test_<metric>`), `variance` is the PER-SAMPLE variance of the",
        f"  {TEST_SIZE:,}-draw test pass in nats² (avg of `test_<metric>_std**2`).",
        f"- `{NOT_RECORDED}` = not recorded. `trainer.BaseTrainer.STD_KEYS` logs a per-sample",
        "  std for the three WEIGHTED quantities only, so `nelbo_ref` and `ce_ref` have no",
        "  variance in any existing run; filling them needs STD_KEYS extended and a re-run.",
        "- These variances are NOT the `± std` these tables used to print. That was the",
        f"  across-seed spread of the mean, related by `± ≈ sqrt(variance / {TEST_SIZE:,})`.",
        f"- `!` marks loss proposals above the ~{VARIANCE_CLIFF} variance cliff, where the",
        "  weighted estimator has infinite variance. The reference pass is pinned at",
        "  exp(0.1) and stays valid, but training there is materially noisier.",
        "- `wce_ref` is dominated by rare extremes; treat its spread as indicative only.",
    ]
    if unparsed:
        out.append(f"- unparsed run dirs ({len(unparsed)}): {', '.join(unparsed[:3])}")

    multi_step = len(steps_list) > 1
    out += ["", "---", "", "# Results (Full Table)", ""]
    for ps in ps_list:
        for k in k_list:
            for steps in steps_list:
                out += ["---", "", section_title(ps, k, steps, multi_step), "",
                        "Each cell: point-estimate mean / per-sample variance, "
                        "averaged across 3 seeds", ""]
                for lg, title in GEOMETRY_TITLE:
                    out += [f"**{title}**", ""]
                    out += table(cells, ps, k, steps, lg, rates, args.seeds)
                    out += [""]

    out += ["---", "", "# RESULTS (Dense Table)", ""]
    for ps in ps_list:
        for k in k_list:
            for steps in steps_list:
                out += ["---", "", section_title(ps, k, steps, multi_step), "",
                        DENSE_NOTE, ""]
                out += dense_table(cells, ps, k, steps, rates, args.seeds)
                out += [""]

    dest = REPO_DIR / "experiments" / args.project / "RESULTS.md"
    out += handwritten_tail(dest)
    text = "\n".join(out) + "\n"
    dest.write_text(text)
    print(text)
    print(f"written -> {dest}")


if __name__ == "__main__":
    main()
