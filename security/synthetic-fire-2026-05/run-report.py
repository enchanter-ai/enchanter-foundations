#!/usr/bin/env python3
"""
run-report.py — consume output/verdicts.jsonl, compute per-plugin TP/FP/TN/FN,
precision/recall, runtime stats. Emit regression-baseline.json and a markdown
summary at output/report.md.

Definitions per event per plugin:
  TP : ground_truth[plugin] == True  and predicted[plugin] == True
  FP : ground_truth[plugin] == False and predicted[plugin] == True
  TN : ground_truth[plugin] == False and predicted[plugin] == False
  FN : ground_truth[plugin] == True  and predicted[plugin] == False

Precision = TP / (TP + FP)   (1.0 if both zero — vacuously correct)
Recall    = TP / (TP + FN)   (1.0 if both zero)

Comparison to previous baseline (if regression-baseline.json exists in dir):
  Flag a regression when current precision OR recall drops by ≥ 5 percentage
  points vs. the stored baseline. Exit code 0 on no regression, 1 otherwise.
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
VERDICTS = OUT / "verdicts.jsonl"
BASELINE = ROOT / "regression-baseline.json"

PLUGINS = [
    "canary", "package-gate", "egress-monitor", "capability-fence",
    "secret-scanner", "vuln-detector", "action-guard", "audit-trail",
]


def load_verdicts():
    with VERDICTS.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def compute():
    """Per-plugin counters."""
    counts = {p: {"TP": 0, "FP": 0, "TN": 0, "FN": 0} for p in PLUGINS}
    rt = {p: [] for p in PLUGINS}
    top_fp = {p: [] for p in PLUGINS}
    top_fn = {p: [] for p in PLUGINS}
    n = 0
    for rec in load_verdicts():
        n += 1
        for p in PLUGINS:
            gt = bool(rec["ground_truth"].get(p, False))
            pr = bool(rec["predicted"].get(p, False))
            if gt and pr:
                counts[p]["TP"] += 1
            elif (not gt) and pr:
                counts[p]["FP"] += 1
                if len(top_fp[p]) < 6:
                    top_fp[p].append({
                        "id": rec["id"], "label": rec["label"],
                        "advisories": rec["advisory_msgs"],
                    })
            elif (not gt) and (not pr):
                counts[p]["TN"] += 1
            else:  # gt and not pr
                counts[p]["FN"] += 1
                if len(top_fn[p]) < 6:
                    top_fn[p].append({
                        "id": rec["id"], "label": rec["label"],
                        "advisories": rec["advisory_msgs"],
                    })
            rt[p].append(rec["runtime_ms"].get(p, 0.0))
    return n, counts, rt, top_fp, top_fn


def precision_recall(c):
    tp, fp, fn = c["TP"], c["FP"], c["FN"]
    prec = tp / (tp + fp) if (tp + fp) else 1.0
    rec = tp / (tp + fn) if (tp + fn) else 1.0
    return prec, rec


def fmt_pct(x):
    return f"{100 * x:.1f}%"


def write_baseline(counts, rt, n):
    base = {
        "generated_at": "2026-05-05",
        "total_events": n,
        "plugins": {},
    }
    for p, c in counts.items():
        prec, rec = precision_recall(c)
        base["plugins"][p] = {
            "TP": c["TP"], "FP": c["FP"], "TN": c["TN"], "FN": c["FN"],
            "precision": round(prec, 4), "recall": round(rec, 4),
            "runtime_ms_avg": round(statistics.fmean(rt[p]), 4) if rt[p] else 0.0,
            "runtime_ms_p99": round(_p99(rt[p]), 4),
        }
    BASELINE.write_text(json.dumps(base, indent=2), encoding="utf-8")


def _p99(xs):
    if not xs:
        return 0.0
    xs = sorted(xs)
    idx = int(0.99 * (len(xs) - 1))
    return xs[idx]


def check_regression(current_counts):
    if not BASELINE.exists():
        return False, ["no baseline to compare against — current run will be saved as baseline"]
    try:
        prev = json.loads(BASELINE.read_text(encoding="utf-8"))
    except Exception:
        return False, ["baseline unreadable; skipping regression check"]
    regressions = []
    for p in PLUGINS:
        prev_p = prev.get("plugins", {}).get(p)
        if not prev_p:
            continue
        cur_prec, cur_rec = precision_recall(current_counts[p])
        d_prec = prev_p["precision"] - cur_prec
        d_rec = prev_p["recall"] - cur_rec
        if d_prec >= 0.05:
            regressions.append(
                f"{p}: precision regressed by {d_prec*100:.1f}pp "
                f"({prev_p['precision']:.3f} -> {cur_prec:.3f})"
            )
        if d_rec >= 0.05:
            regressions.append(
                f"{p}: recall regressed by {d_rec*100:.1f}pp "
                f"({prev_p['recall']:.3f} -> {cur_rec:.3f})"
            )
    return bool(regressions), regressions


def emit_markdown(n, counts, rt, top_fp, top_fn):
    lines = []
    lines.append("# Synthetic Fire Report — 2026-05-05")
    lines.append("")
    lines.append(f"Total events processed: **{n}**")
    lines.append("")
    lines.append("## Per-plugin precision / recall")
    lines.append("")
    lines.append("| Plugin | TP | FP | TN | FN | Precision | Recall | Avg ms | p99 ms |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for p in PLUGINS:
        c = counts[p]
        prec, rec = precision_recall(c)
        avg = statistics.fmean(rt[p]) if rt[p] else 0.0
        p99 = _p99(rt[p])
        lines.append(
            f"| {p} | {c['TP']} | {c['FP']} | {c['TN']} | {c['FN']} | "
            f"{fmt_pct(prec)} | {fmt_pct(rec)} | {avg:.3f} | {p99:.3f} |"
        )
    lines.append("")
    lines.append("## Top false positives (sample)")
    lines.append("")
    for p in PLUGINS:
        if not top_fp[p]:
            continue
        lines.append(f"### {p}")
        for ex in top_fp[p][:3]:
            lines.append(f"- `{ex['id']}` ({ex['label']}): {ex['advisories']}")
        lines.append("")
    lines.append("## Top false negatives (sample)")
    lines.append("")
    for p in PLUGINS:
        if not top_fn[p]:
            continue
        lines.append(f"### {p}")
        for ex in top_fn[p][:3]:
            lines.append(f"- `{ex['id']}` ({ex['label']}): {ex['advisories']}")
        lines.append("")
    (OUT / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    n, counts, rt, top_fp, top_fn = compute()
    write_baseline(counts, rt, n)
    emit_markdown(n, counts, rt, top_fp, top_fn)

    # Summary print
    print(f"events: {n}")
    print(f"{'plugin':<20} {'TP':>4} {'FP':>4} {'TN':>5} {'FN':>4} {'prec':>7} {'recall':>7}")
    for p in PLUGINS:
        c = counts[p]
        prec, rec = precision_recall(c)
        print(f"{p:<20} {c['TP']:>4} {c['FP']:>4} {c['TN']:>5} {c['FN']:>4} "
              f"{prec:>7.3f} {rec:>7.3f}")

    regressed, regs = check_regression(counts)
    if regressed:
        print("REGRESSION DETECTED:")
        for r in regs:
            print(f"  - {r}")
        sys.exit(1)
    print("no regression")


if __name__ == "__main__":
    main()
