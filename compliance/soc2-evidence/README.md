# SOC 2 Evidence-Collection Infrastructure

The inline-achievable approximation of SOC 2 Type II preparation: automated daily evidence collection, completeness checking, signed daily bundles, per-criterion playbooks. Designed so that when the 6-month observation period starts, evidence accrues automatically rather than being assembled in a panic before audit field work.

**This is NOT:** a SOC 2 audit, a Type II opinion letter, 6 months of evidence, or a substitute for an independent CPA firm engagement. See `external-engagement-scoping.md` for the explicit boundary.

## Layout

```
soc2-evidence/
├── README.md                          (this file)
├── evidence-collection-plan.md        canonical per-criterion mapping
├── auditor-readiness-dashboard.md     regenerated daily by completeness check
├── external-engagement-scoping.md     what stays external (CPA firm scope)
├── scripts/
│   ├── collect-evidence.py            daily collector (stdlib only)
│   └── evidence-completeness-check.py daily 30d-window check
├── playbooks/                         35 per-criterion files
│   ├── CC1.1.md ... CC9.2.md
│   └── A1.1.md ... A1.3.md
├── collected/                         daily output (gitignored locally; PR'd to soc2-evidence branch)
│   └── YYYY-MM-DD/
│       ├── CC1.1.jsonl ... A1.3.jsonl
│       ├── _summary.json
│       ├── _manifest.sha256           (computed by workflow)
│       └── _manifest.{sig,cert}       (cosign keyless OIDC)
└── .github/workflows/
    └── soc2-evidence-collection.yml   daily cron at 06:17 UTC
```

## Running locally

```bash
# From repo root
python agent-foundations/compliance/soc2-evidence/scripts/collect-evidence.py
python agent-foundations/compliance/soc2-evidence/scripts/evidence-completeness-check.py
```

Both scripts are stdlib-only. Each prints a JSON summary on completion.

## What the CI workflow does

1. Runs the collector — populates `collected/YYYY-MM-DD/`.
2. Runs the completeness check — updates `auditor-readiness-dashboard.md`.
3. Computes SHA-256 manifest over the day's JSONL files.
4. Signs the manifest with cosign (keyless OIDC via GitHub Actions).
5. Opens a PR to the `soc2-evidence` branch; operator merges weekly after dashboard review.
6. Uploads a 90-day GitHub Actions artifact as a redundant retention surface.

## Operator weekly cadence

Every Monday:

1. Open `auditor-readiness-dashboard.md`.
2. Resolve any MISSING criteria via the matching `playbooks/<criterion>.md`.
3. Merge the week's `soc2-evidence` PRs.
4. If coverage <95%, surface to the security-closure synthesis queue.

## Honest disclaimers

- **CC1.2** (board oversight) and **A1.3** (recovery drills) are open gaps. The infrastructure emits explicit `GAP` attestations rather than fabricating evidence — this is per the honest-numbers contract in root `CLAUDE.md`.
- **MUST-SHIP queue** (F-001, F-002, F-004, F-005, F-010, F-013) must close before the Type II observation period begins. Type I is achievable today with documented remediation items.
- **Type II report delivery** earliest realistic: ~9 months from infrastructure start (6mo observation + 3mo field work + report).

See `evidence-collection-plan.md` § 5 and `external-engagement-scoping.md` for the full boundary statement.
