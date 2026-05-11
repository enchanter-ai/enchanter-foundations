# Continuous Monitoring (ConMon) Plan — enchanter-ai

**Document type:** FedRAMP ConMon Plan skeleton
**Date:** 2026-05-05
**Cadence baseline:** FedRAMP Rev 5 Moderate ConMon requirements
**Status:** Pre-authorization. ConMon ramps up in earnest once a hosted control plane exists and ATO is in motion.

> Continuous monitoring is the post-authorization heartbeat: monthly vuln scans, quarterly POA&M updates, ongoing inventory + config drift detection. This plan defines what enchanter-ai will operate when authorized; current implementation status is honestly disclosed per row.

---

## 1. ConMon objectives

| Objective | FedRAMP requirement | enchanter-ai mechanism |
|---|---|---|
| Maintain effective security controls | All baseline controls remain implemented | Per-family evidence in `control-implementation/*.md` |
| Detect changes in risk posture | Monthly vuln scan + advisory monitoring | Dependabot + OSV.dev + GHAS CodeQL |
| Maintain inventory accuracy | Weekly inventory delta | SBOM emitter + plugin manifest delta scan |
| Audit-trail integrity | Continuous | HMAC chain + verify-chain.sh + OTLP export (planned) |
| Incident detection + response | Real-time | audit-trail + canary + capability-fence + action-guard |
| POA&M tracking | Monthly update | Gap list in this folder + per-F-code closure tracking |

---

## 2. Monitoring activities + cadence

### 2.1 Real-time (event-driven)

| Activity | Mechanism | Owner plugin | Status |
|---|---|---|---|
| Tool invocation logging | PreToolUse + PostToolUse hooks → JSONL HMAC chain | hydra/audit-trail | **Shipped** |
| Capability-fence enforcement | PreToolUse hook denies non-whitelisted tools | hydra/capability-fence | **Shipped** |
| Egress allowlist enforcement | PreToolUse hook denies non-allowlisted URLs | hydra/egress-shield | **Shipped** (allowlist sparse: F-005) |
| Secret-scanner sweep | PreToolUse hook denies tool args with detected secrets | hydra/secret-scanner | **Shipped** |
| Destructive-op confirmation | PreToolUse hook gates rm/force-push/etc. | hydra/action-guard | **Shipped** |
| Prompt-injection canary | Synthetic fixtures fire on every WebFetch | hydra/canary | **Shipped** (advisory; CI gate pending F-004) |
| Drift watching | PostToolUse + Stop hooks | naga/naga-observe | **Shipped** |
| Audit log to OTLP | OTLP exporter on each event | hydra/audit-trail | **Planned** F-021/F-024 |
| Pager on HIGH+ | Webhook to PagerDuty / Opsgenie | hydra/audit-trail | **Planned** F-011 |

### 2.2 Daily

| Activity | Mechanism | Status |
|---|---|---|
| Dependabot scan | GitHub-native, all repos | **Shipped** — `.github/dependabot.yml` per repo |
| Audit-trail HMAC chain verify | verify-chain.sh cron | **Planned** (manual today) |
| OSV-Scanner cron | scripts/osv-scan.sh | **Planned** F-009 |

### 2.3 Weekly

| Activity | Mechanism | Status |
|---|---|---|
| Inventory delta scan | plugin manifest + SBOM regen | **Planned** (SBOM is per-release today; F-001 default-off) |
| Inference-engine reconcile | Wald SPRT + Beta-Binomial on accumulated artifacts | **Shipped** — `wixie/shared/scripts/inference-engine.py reconcile` |
| Dependabot triage | Maintainer review of open advisories | **Operational** |
| CodeQL alert triage | Maintainer review of open alerts | **Operational** (backlog: F-022) |

### 2.4 Monthly

| Activity | FedRAMP cadence | enchanter-ai mechanism | Status |
|---|---|---|---|
| Vulnerability scan + scoring | Monthly | Dependabot + OSV-Scanner + CodeQL aggregated | **Partial** |
| POA&M update | Monthly | Gap list in `control-implementation/*.md` + closure tracker | **Manual** today |
| Egress allowlist review | Monthly | Diff `hydra/plugins/egress-shield/config/allowlist.yaml` | **Manual** |
| PR-lifecycle audit-trail review | Monthly | sylph/pr-lifecycle PR audit + merge metadata | **Manual** |
| Failed-control trend review | Monthly | inference-engine catalog + audit-trail HIGH events | **Partial** |

### 2.5 Quarterly

| Activity | FedRAMP cadence | enchanter-ai mechanism | Status |
|---|---|---|---|
| Self-attestation refresh | Quarterly | This folder + `fedramp-boundary.md` revision | **Operational** |
| SBOM regeneration | Quarterly | hydra/sbom-emitter | **Shipped** (gap F-001) |
| Significant-change review | Quarterly | git log + boundary/SSP diff | **Manual** |
| Vuln-detector audit | Quarterly | hydra/vuln-detector log + remediation rate | **Partial** |
| Quarterly SAR update | Quarterly (post-ATO) | 3PAO engagement | **Pre-authorization** |

### 2.6 Annual

| Activity | FedRAMP cadence | enchanter-ai mechanism | Status |
|---|---|---|---|
| 3PAO assessment + pentest | Annual (post-ATO) | External 3PAO firm | **Pre-authorization** |
| Control reassessment | Annual | Full re-walk of all 325 controls | **Pre-authorization** |
| Risk Assessment refresh | Annual | RA-3 artifact (gap) | **Manual** |
| IR plan review + tabletop | Annual | `incident-response-plan.md` review + simulated event | **Planned** |
| SSP refresh | Annual + on significant change | `ssp-skeleton.md` → full SSP revision | **Skeleton only** |

---

## 3. Vulnerability scanning detail (FedRAMP-specific)

FedRAMP Moderate requires **monthly authenticated** vuln scans of all in-scope assets. enchanter-ai implementation:

| Asset class | Scanner | Auth | Frequency | Output channel |
|---|---|---|---|---|
| npm dependencies | Dependabot | repo-scoped GitHub token | Daily (auto-PR) | GitHub Security Advisories |
| PyPI dependencies | Dependabot | repo-scoped GitHub token | Daily (auto-PR) | GitHub Security Advisories |
| Source code | GHAS CodeQL | repo-scoped | On PR + nightly | GitHub Security tab |
| Combined feed | OSV-Scanner (planned) | n/a | Daily cron | `state/osv-findings.jsonl` |
| Hosted infra (when SaaS) | Inherited from CSP | CSP-managed | Per CSP cadence | CSP Security Hub |
| Container images (when SaaS) | Trivy / Snyk (planned) | registry-scoped | Daily | hub artifact |

**Remediation SLAs** (per FedRAMP Moderate):

| Severity | SLA | enchanter-ai SLA (proposed) |
|---|---|---|
| Critical | 15 days | 7 days |
| High | 30 days | 14 days |
| Moderate | 90 days | 60 days |
| Low | 180 days | 90 days |

SLAs are aspirational pre-authorization; commitment formalized at ATO.

---

## 4. POA&M (Plan of Action and Milestones)

A POA&M is the formal tracker of every accepted gap with a remediation date. enchanter-ai pre-authorization POA&M seed: the **F-001 through F-024 closure list** in `wixie/prompts/security-closure/results/synthesis.md` plus the per-family gap lists in `control-implementation/*.md`.

Top 10 POA&M-shaped gaps (to be formalized at ATO):

| # | ID | Description | Owner | Target |
|---|---|---|---|---|
| 1 | F-001 | SBOM emitter default-off — flip on | hydra/sbom-emitter maintainer | Pre-Phase-3 |
| 2 | F-002 | No Sigstore/SLSA L3 release pipeline | release maintainer | Pre-Phase-3 |
| 3 | F-005 | Egress allowlist sparse | hydra/egress-shield maintainer | Pre-Phase-4 |
| 4 | F-009 | OSV-Scanner cron not shipped | hydra/vuln-detector maintainer | Pre-Phase-3 |
| 5 | F-010 | Capability-sandbox escape-hatch CI tests absent | hydra/capability-fence maintainer | Pre-Phase-4 |
| 6 | F-011 | No pager on HIGH+ events | hosted-control-plane | Phase 1 |
| 7 | F-013 | No multi-tenant rate-limiter | hosted-control-plane | Phase 1 |
| 8 | F-021/F-024 | OTLP exporter not shipped | hydra/audit-trail + hosted | Phase 1 |
| 9 | F-022 | CodeQL alert triage backlog | all repos | Pre-Phase-3 |
| 10 | (new) | No FIPS 140-3 module validation | host platform / CSP choice | Phase 1 |

Phase numbers reference `hosted-control-plane-prerequisite.md` § 4.

---

## 5. Significant-change definition

Triggers off-cycle ConMon update (and may trigger 3PAO re-assessment):

- New external connection added to egress allowlist.
- New plugin shipped that touches CUI flows.
- Change to audit-trail HMAC algorithm or key-rotation procedure.
- Change to capability-fence enforcement semantics.
- Change to FIPS-validated cryptographic module.
- Migration between CSPs (when hosted).
- Material change to subagent identity model.

Per FedRAMP guidance: significant change requires SSP update within 30 days and may trigger Significant Change Request to the AO.

---

## 6. Reporting cadence (post-ATO)

| Report | Recipient | Cadence |
|---|---|---|
| Monthly ConMon deliverables | AO + 3PAO | Monthly |
| POA&M update | AO | Monthly |
| Significant change request | AO | As needed |
| Annual assessment package | AO + 3PAO | Annual |
| Incident report | AO + US-CERT | Per US-CERT timelines (1h for HIGH+) |

**Pre-authorization:** none of these reports are submitted. Cadence + format is documented for readiness.

---

## 7. Escalation thresholds

| Trigger | Channel | SLA |
|---|---|---|
| Audit-trail HMAC chain break | Maintainer pager (F-011 planned) | < 1h |
| Capability-fence denial spike (> 10x baseline) | Maintainer pager | < 1h |
| Canary fixture fire | Pager + manual review | < 4h |
| Critical CVE in direct dep | Auto-PR + maintainer alert | < 24h |
| Egress-shield deny spike | Maintainer alert | < 24h |
| OTLP exporter failure | Maintainer alert | < 4h |

Pager wiring depends on F-011 — pre-authorization, escalation is stderr → email convention.

---

## 8. ConMon tooling inventory

| Tool | Use | Status |
|---|---|---|
| Dependabot | Daily dep scan | **Shipped** |
| GHAS CodeQL | Static analysis | **Shipped** |
| OSV-Scanner | Vuln cron | **Planned** F-009 |
| hydra/audit-trail | Event logging + HMAC chain | **Shipped** |
| hydra/canary | Prompt-injection fixtures | **Shipped** (advisory) |
| hydra/sbom-emitter | Release SBOM | **Shipped** (gap F-001) |
| OTLP collector | Off-host audit | **Planned** F-021/F-024 |
| PagerDuty / Opsgenie | HIGH+ events | **Planned** F-011 |
| inference-engine | Cross-session learning | **Shipped** |

---

## 9. Cross-references

- `ssp-skeleton.md`
- `control-implementation/*.md` per-family evidence
- `incident-response-plan.md`
- `hosted-control-plane-prerequisite.md`
- `fedramp-boundary.md` § 7 (current ConMon story)
- `wixie/prompts/security-closure/results/synthesis.md` (F-code closure)
