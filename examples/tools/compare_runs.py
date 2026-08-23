#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
#
# REFERENCE IMPLEMENTATION. Taken verbatim from the project it was written for, and
# tied to that project's report schema. It is here to be read, not to be dropped into
# another tree: what transfers is the list of things it refuses to do. See
# examples/tools/README.md and MEASUREMENT.md of the standard.
#
# Compares two configurations from benchmark reports, and refuses to produce a
# verdict when the measurement method cannot support one.
#
# This exists because two of the project's rules were declarations with nothing
# behind them (MEASUREMENT.md of the standard):
#
#   - "sweep in both directions" — whichever configuration runs first is measured on
#     a cooler SoC, so a one-directional A -> B comparison flatters B. Reversing the
#     order must not change the verdict; this tool refuses to give one unless both
#     directions are present.
#   - the significance threshold — it was a constant, 1.3%, derived from a single
#     lucky run whose p50 spread was 0.42%. The same scene on the same build the same
#     day also produced 0.84%. The threshold is now computed from the spreads of the
#     runs actually being compared, so a noisy session cannot certify a small win.
#
#   python tools/compare_runs.py --a before1.json before2.json \
#                                --b after1.json after2.json
#
# Exit codes: 0 a comparison was produced, 2 refused (method insufficient), 1 error.

import argparse
import json
import os
import re
import statistics
import sys

# A difference counts only if it clears the noise by this factor. Three times the
# worst observed spread, not a number carried over from a previous session.
SIGNIFICANCE_FACTOR = 3.0


def started_at(data):
    """When this report's runs began.

    sweep_order is the harness's own record of the order its runs happened in, so it
    is the primary key; a hand-curated baseline records no per-run times and falls
    back to its capture date. Ordering used to come from timestamp_utc alone, which
    made sweep_order a field nothing read and locked curated baselines out of being
    used as a comparison arm at all.
    """
    order = data.get("sweep_order")
    if isinstance(order, list) and order and isinstance(order[0], str) \
            and re.match(r"\d{4}-\d{2}-\d{2}", order[0]):
        return order[0]
    return data.get("timestamp_utc") or data.get("captured") or ""


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    p50 = (data.get("summary") or {}).get("ft_p50_ms")
    if p50 is None:
        # A curated baseline keeps its percentiles under "summary"; a raw report from
        # bench.py keeps per-run entries. Fall back to the median of the runs.
        runs = [r.get("ft_p50_ms") for r in data.get("runs", []) if r.get("ft_p50_ms")]
        p50 = statistics.median(runs) if runs else None
    if p50 is None:
        sys.exit(f"error: {path} has no ft_p50_ms to compare.")
    n_runs = (data.get("config") or {}).get("runs")
    if n_runs is None:
        n_runs = len(data.get("runs") or [])
    return {
        "path": path,
        "p50": p50,
        "spread": data.get("p50_spread_pct"),
        "runs": n_runs,
        "when": started_at(data),
        "scene": data.get("scene_id"),
        "commit": (data.get("armsx2_base_commit") or "")[:8],
    }


def check_spreads(reports):
    """Every report must carry a spread that was actually observed.

    A single run has nothing to vary against, so bench.py records a spread of 0.0 —
    and a threshold of three times zero certifies any difference at all as
    significant. That defeats the whole point of deriving the threshold from the data,
    so the tool refuses rather than inventing a floor.
    """
    bad = [r for r in reports if not r["runs"] or r["runs"] < 2 or r["spread"] is None]
    return bad


def check_sweep(order):
    """Both directions must appear in the execution order."""
    transitions = {(order[i], order[i + 1]) for i in range(len(order) - 1)}
    return ("A", "B") in transitions and ("B", "A") in transitions


def main():
    ap = argparse.ArgumentParser(
        description="Compare two configurations, enforcing the sweep and threshold rules.")
    ap.add_argument("--a", nargs="+", required=True, metavar="JSON",
                    help="Reports for configuration A (the baseline side).")
    ap.add_argument("--b", nargs="+", required=True, metavar="JSON",
                    help="Reports for configuration B (the change under test).")
    ap.add_argument("--metric", default="ft_p50_ms",
                    help="Informational: which metric is being compared (default ft_p50_ms).")
    args = ap.parse_args()

    a = [load(p) for p in args.a]
    b = [load(p) for p in args.b]
    for r in a:
        r["arm"] = "A"
    for r in b:
        r["arm"] = "B"

    scenes = {r["scene"] for r in a + b}
    if len(scenes) > 1:
        sys.exit(f"error: reports span more than one scene: {sorted(map(str, scenes))}.\n"
                 f"       A comparison is only meaningful within one registered scene.")
    scene = scenes.pop() or "(unregistered)"

    ordered = sorted(a + b, key=lambda r: r["when"])
    order = [r["arm"] for r in ordered]

    print(f"scene:  {scene}")
    print(f"metric: {args.metric}")
    print(f"order:  {' -> '.join(order)}")
    for r in ordered:
        spread = "n/a" if r["spread"] is None else f"{r['spread']:.2f}%"
        print(f"        {r['arm']}  {r['p50']:>8.2f}  spread {spread}  "
              f"({r['runs']} run(s))  {os.path.basename(r['path'])}")

    weak = check_spreads(a + b)
    if weak:
        print("\nREFUSED: a threshold cannot be derived from these reports.")
        for r in weak:
            print(f"  {os.path.basename(r['path'])}: {r['runs']} run(s), "
                  f"spread {r['spread']}")
        print("The threshold is three times the worst spread actually observed, and a")
        print("single run observes none - three times zero would certify any difference")
        print("at all. Re-run with at least two runs per report.")
        sys.exit(2)

    if not check_sweep(order):
        print("\nREFUSED: the sweep is one-directional.")
        print("A run measured later sits on a warmer SoC, so whichever configuration")
        print("went first is flattered. Run the sweep both ways (A, B, then B, A) and")
        print("compare again. See gotchas G09.")
        sys.exit(2)

    median_a = statistics.median(r["p50"] for r in a)
    median_b = statistics.median(r["p50"] for r in b)
    delta_pct = (median_b - median_a) / median_a * 100.0
    worst_spread = max(r["spread"] for r in a + b)
    threshold = worst_spread * SIGNIFICANCE_FACTOR

    print(f"\nA median: {median_a:.2f}    B median: {median_b:.2f}")
    print(f"delta:    {delta_pct:+.2f}%")
    print(f"threshold {threshold:.2f}%  ({SIGNIFICANCE_FACTOR:g}x the worst observed "
          f"spread, {worst_spread:.2f}%)")

    if abs(delta_pct) < threshold:
        outcome = "inconclusive - the difference does not clear the noise"
    elif delta_pct < 0:
        outcome = "significant improvement (lower frametime)"
    else:
        outcome = "significant regression (higher frametime)"
    print(f"\n{outcome}")

    print("\nFor the Result block of the E## entry:")
    print(f"- {scene}: {args.metric} {delta_pct:+.2f}% "
          f"(threshold {threshold:.2f}%) -> `{os.path.basename(b[0]['path'])}`")
    print("\nThe verdict word - confirmed, refuted or inconclusive - is yours: it")
    print("depends on what the prediction said, which this tool does not know.")
    sys.exit(0)


if __name__ == "__main__":
    main()
