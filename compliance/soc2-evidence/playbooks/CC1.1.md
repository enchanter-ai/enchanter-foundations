# Playbook — CC1.1 Commitment to integrity & ethics

- **Control ID:** CC1.1
- **Control description:** The entity demonstrates a commitment to integrity and ethical values.
- **Evidence-collection mechanism:** Daily SHA-256 hash of every file in `shared/conduct/*.md` (discipline, verification, doubt-engine, delegation, failure-modes, tool-use, formatting, skill-authoring, hooks, precedent, tier-sizing, web-fetch, inference-substrate, context). Emitted as `config-hash` event by `scripts/collect-evidence.py`.
- **Producer (today):** `agent-foundations/shared/conduct/` (read by collector; canonical copies live under `wixie/shared/conduct/`)
- **Retention rule:** 7 years (audit-grade).
- **Who reviews:** Repo maintainer weekly via `auditor-readiness-dashboard.md`.
- **Escalation path:** If a conduct file is deleted or hash-rotates without a corresponding PR, surface to security-closure synthesis queue and open an issue tagged `compliance-drift`.
- **Type II evidence shape:** 6+ months of daily hashes showing controlled change (each rotation traceable to a merged PR).
- **External dependency:** None — fully inline.
