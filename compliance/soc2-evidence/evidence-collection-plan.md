# SOC 2 Evidence Collection Plan

**Document version:** 1.0
**Date:** 2026-05-05
**Scope:** CC1-CC9 + A1.x — Trust Services Criteria, enchanter-ai substrate
**Status:** Infrastructure shipped. Type II audit requires 6-month observation period + independent CPA firm engagement (external).

---

## 1. Purpose

Define the source-of-truth mapping from each TSC criterion to (a) the producing plugin/log/script, (b) the evidence artifact format, (c) the retention rule, (d) the landing path. Daily cron (`scripts/collect-evidence.py`) pulls evidence into `collected/YYYY-MM-DD/<criterion>.jsonl` per this plan.

## 2. Evidence shape — normalized JSON event

Every collected event normalizes to:

```json
{
  "ts": "ISO-8601 UTC",
  "criterion": "CC1.1 | CC1.2 | ... | A1.3",
  "plugin": "hydra/audit-trail | wixie/inference-engine | ...",
  "event_type": "attestation | log-tail | screenshot-hash | config-hash | metric | ...",
  "evidence_data": { /* criterion-specific payload */ },
  "hash": "sha256 over (ts + criterion + plugin + event_type + canonical(evidence_data))"
}
```

`hash` provides per-event integrity; the daily commit's cosign signature provides per-day attestation.

## 3. Retention rules (SOC 2 minimums)

| Class | Retention | Examples |
|---|---|---|
| Operational logs | **90 days** rolling | tool-invocation logs, transient hook outputs |
| Control evidence | **1 year** | daily collected JSONL, completeness reports |
| Audit-grade records | **7 years** | signed daily attestations, SBOMs, security incidents, change-management approvals |

Retention floor enforced by: `scripts/collect-evidence.py` writes 1y by default; audit-grade events get `retention: 7y` field; 90d operational pull is by tail-and-drop, not stored in `collected/`.

## 4. Per-criterion mapping

### CC1 — Control Environment

| Crit | Producer | Format | Retention | Landing |
|---|---|---|---|---|
| CC1.1 | `agent-foundations/shared/conduct/` (file-hash + last-modified) | `config-hash` event | 7y | `collected/<d>/CC1.1.jsonl` |
| CC1.2 | **GAP** — single-maintainer; emit `attestation` of org-structure state monthly | `attestation` | 7y | `collected/<d>/CC1.2.jsonl` (sparse) |
| CC1.3 | `*/CLAUDE.md` tier model + `plugins/*/.claude-plugin/plugin.json` owner | `config-hash` | 7y | `collected/<d>/CC1.3.jsonl` |
| CC1.4 | `shared/conduct/skill-authoring.md` + new-skill test gate results | `config-hash` + `metric` | 1y | `collected/<d>/CC1.4.jsonl` |
| CC1.5 | `*/state/precedent-log.md` + plugin `learnings.md` tails | `log-tail` | 1y | `collected/<d>/CC1.5.jsonl` |

### CC2 — Communication & Information

| Crit | Producer | Format | Retention | Landing |
|---|---|---|---|---|
| CC2.1 | per-prompt `metadata.json`, `learnings.md`, `state/precedent-log.md` | `log-tail` | 1y | `collected/<d>/CC2.1.jsonl` |
| CC2.2 | `wixie/plugins/inference-engine/state/briefings/<plugin>.md` hash | `config-hash` | 1y | `collected/<d>/CC2.2.jsonl` |
| CC2.3 | `agent-foundations/compliance/*.md`, repo READMEs | `config-hash` | 1y | `collected/<d>/CC2.3.jsonl` |

### CC3 — Risk Assessment

| Crit | Producer | Format | Retention | Landing |
|---|---|---|---|---|
| CC3.1 | DEPLOY-bar verdict events from `wixie/plugins/convergence-engine/` | `metric` | 1y | `collected/<d>/CC3.1.jsonl` |
| CC3.2 | `wixie/prompts/security-closure/results/synthesis.md` + inference-engine elevated patterns | `attestation` | 7y | `collected/<d>/CC3.2.jsonl` |
| CC3.3 | `hydra/plugins/secret-scanner/state/findings.jsonl` + `hydra/plugins/audit-trail/state/log.jsonl` HMAC chain head | `log-tail` | 7y | `collected/<d>/CC3.3.jsonl` |
| CC3.4 | `wixie/plugins/convergence-engine/` revert events; baseline-snapshot pairs | `log-tail` | 1y | `collected/<d>/CC3.4.jsonl` |

### CC4 — Monitoring Activities

| Crit | Producer | Format | Retention | Landing |
|---|---|---|---|---|
| CC4.1 | `inference-engine.py reconcile` output; quarterly self-attestation files | `attestation` | 7y | `collected/<d>/CC4.1.jsonl` |
| CC4.2 | failure-mode counts (F01..F14) aggregated from `learnings.md` + `precedent-log.md` | `metric` | 1y | `collected/<d>/CC4.2.jsonl` |

### CC5 — Control Activities

| Crit | Producer | Format | Retention | Landing |
|---|---|---|---|---|
| CC5.1 | `shared/conduct/*.md` hashes + `*/plugins/*/SKILL.md` count | `config-hash` | 1y | `collected/<d>/CC5.1.jsonl` |
| CC5.2 | hydra defensive-plugin state heads (audit-trail, capability-fence, egress-shield, secret-scanner, vuln-detector, package-gate, license-gate, sbom-emitter) | `log-tail` | 1y | `collected/<d>/CC5.2.jsonl` |
| CC5.3 | `*/install.sh` hashes + `settings.json` hashes | `config-hash` | 1y | `collected/<d>/CC5.3.jsonl` |

### CC6 — Logical & Physical Access

| Crit | Producer | Format | Retention | Landing |
|---|---|---|---|---|
| CC6.1 | `hydra/plugins/capability-fence/hooks/PreToolUse.sh` events + `hydra/plugins/action-guard/state/confirmations.jsonl` | `log-tail` | 7y | `collected/<d>/CC6.1.jsonl` |
| CC6.2 | new-skill discovery-test results | `metric` | 1y | `collected/<d>/CC6.2.jsonl` |
| CC6.3 | per-subagent tool-whitelist payloads (sampled from delegation events) | `log-tail` | 1y | `collected/<d>/CC6.3.jsonl` |
| CC6.4 | N/A — distributed code repo, no physical infrastructure | `attestation` (n/a) | 7y | `collected/<d>/CC6.4.jsonl` |
| CC6.5 | N/A | `attestation` (n/a) | 7y | `collected/<d>/CC6.5.jsonl` |
| CC6.6 | `hydra/plugins/canary/state/canary-results.jsonl` + egress-shield URL-block events | `log-tail` | 7y | `collected/<d>/CC6.6.jsonl` |
| CC6.7 | `hydra/plugins/egress-shield/config/allowlist.yaml` hash + block events | `config-hash` + `log-tail` | 1y | `collected/<d>/CC6.7.jsonl` |
| CC6.8 | `hydra/plugins/package-gate/` + `hydra/plugins/vuln-detector/state/audit.jsonl` | `log-tail` | 7y | `collected/<d>/CC6.8.jsonl` |

### CC7 — System Operations

| Crit | Producer | Format | Retention | Landing |
|---|---|---|---|---|
| CC7.1 | `hydra/plugins/vuln-detector/state/audit.jsonl` + `*/.github/workflows/codeql.yml` run summaries | `log-tail` | 7y | `collected/<d>/CC7.1.jsonl` |
| CC7.2 | `hydra/plugins/audit-trail/state/log.jsonl` HMAC head + inference-engine SPRT verdicts | `log-tail` | 7y | `collected/<d>/CC7.2.jsonl` |
| CC7.3 | F-code triage entries from `failure-modes.md`-tagged `learnings.md` rows | `log-tail` | 1y | `collected/<d>/CC7.3.jsonl` |
| CC7.4 | `hydra/plugins/action-guard/state/confirmations.jsonl` (destructive ops gated) | `log-tail` | 7y | `collected/<d>/CC7.4.jsonl` |
| CC7.5 | convergence revert-on-regression events; precedent-log dead-end entries | `log-tail` | 1y | `collected/<d>/CC7.5.jsonl` |

### CC8 — Change Management

| Crit | Producer | Format | Retention | Landing |
|---|---|---|---|---|
| CC8.1 | `sylph/plugins/pr-lifecycle/state/` + `wixie/plugins/prompt-tester/` regression results + convergence DEPLOY verdicts | `log-tail` + `metric` | 7y | `collected/<d>/CC8.1.jsonl` |

### CC9 — Risk Mitigation

| Crit | Producer | Format | Retention | Landing |
|---|---|---|---|---|
| CC9.1 | `wixie/prompts/security-closure/results/synthesis.md` queue snapshots | `attestation` | 7y | `collected/<d>/CC9.1.jsonl` |
| CC9.2 | `hydra/plugins/sbom-emitter/state/sbom.cdx.json` + license-gate + package-gate + vuln-detector heads | `log-tail` | 7y | `collected/<d>/CC9.2.jsonl` |

### A1 — Availability

| Crit | Producer | Format | Retention | Landing |
|---|---|---|---|---|
| A1.1 | `pech/plugins/budget-watcher/` + `pech/plugins/rate-shield/` + `emu/plugins/context-guard/` metric tails | `metric` | 1y | `collected/<d>/A1.1.jsonl` |
| A1.2 | `wixie/plugins/inference-engine/state/artifacts.jsonl` HEAD hash + `state/precedent-log.md` git-commit hash | `config-hash` | 7y | `collected/<d>/A1.2.jsonl` |
| A1.3 | **GAP** — emit `attestation` until formal drill schedule lands | `attestation` (sparse) | 7y | `collected/<d>/A1.3.jsonl` |

## 5. What stays external (NOT in this infrastructure)

- Independent CPA firm engagement & Type II opinion letter.
- Auditor field work, interviews, walkthroughs.
- Management assertion letter (drafted at engagement time).
- Statement of Applicability for FedRAMP overlap (SAR) — if scope expands.
- Findings remediation letters.

This infrastructure produces **input** to those activities; it is not a substitute.

## 6. Completeness contract

`scripts/evidence-completeness-check.py` runs daily and asserts: every CC criterion has at least one event in the last 30 days. Missing criteria flagged to `auditor-readiness-dashboard.md` and forwarded to `hydra/plugins/audit-trail/` as a `soc2-evidence-gap` event.

Coverage target: **100% non-N/A criteria with last-30d count ≥ 1**. Sparse criteria (CC1.2, A1.3) emit at least one `attestation` per month to stay above the floor.
