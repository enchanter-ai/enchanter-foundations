# Synthetic Fire & Tune — 2026-05-05

Inline approximation of "≥ 4 weeks customer traffic to measure FP rate."
We can't have real users, but we CAN exercise every advisory plugin
exhaustively with 1300 events of synthetic mixed traffic and measure
FP/FN at simulator level.

## Layout

```
synthetic-fire-2026-05/
├── README.md                          ← this file
├── generate-workloads.py              ← (re)generate 1300 synthetic events
├── harness.py                         ← simulate per-plugin verdict per event
├── run-report.py                      ← FP/FN, precision/recall, regression check
├── workloads/
│   ├── benign/                        ← 1000 events across 5 session shapes
│   ├── adversarial/                   ← 200 events (injection / typosquat /
│   │                                    CVE / exfil / fence violation /
│   │                                    secret / destructive)
│   └── edge/                          ← 100 boundary-condition events
├── output/
│   ├── verdicts.jsonl                 ← per-event verdict from harness.py
│   └── report.md                      ← human-readable rundown
├── regression-baseline.json           ← the per-plugin TP/FP/TN/FN baseline
├── tuning-recommendations-2026-05.md  ← per-plugin tuning advice
└── external-real-traffic-gap.md       ← what synthetic doesn't cover
```

## Run

```bash
python generate-workloads.py   # produces ~1300 events in workloads/
python harness.py              # produces output/verdicts.jsonl
python run-report.py           # produces output/report.md + regression check
```

Exit code from `run-report.py` is non-zero on ≥ 5 pp precision OR recall
regression vs. `regression-baseline.json`. Suitable for CI.

## What this is

A measurable proxy for production-fire on 8 advisory plugins:
canary, package-gate, egress-monitor, capability-fence, secret-scanner,
vuln-detector, action-guard, audit-trail.

## What this is NOT

Real customer traffic. See `external-real-traffic-gap.md` — long-tail
benign behavior, multi-turn attacks, niche tool ecosystems, and hook
behavior under load are not modeled.
