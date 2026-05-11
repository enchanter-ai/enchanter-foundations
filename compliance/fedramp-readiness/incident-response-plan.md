# Incident Response Plan — enchanter-ai

**Document type:** NIST SP 800-61r2 Incident Response Plan
**Date:** 2026-05-05
**Companion controls:** IR family (`control-implementation/IR.md`)
**Status:** Pre-authorization. Plan is structurally complete; some response channels (pager, US-CERT reporting, hosted SOC) depend on hosted control plane prerequisite.

---

## 1. Plan purpose and scope

This plan governs detection, analysis, containment, eradication, recovery, and post-incident handling for security events within enchanter-ai's authorization boundary (per `fedramp-boundary.md` § 1). It follows the NIST SP 800-61r2 lifecycle.

Out of scope:
- Customer-side incident handling (agency runs its own IR for incidents in their environment).
- Anthropic API / Claude Code harness incidents (OOB; reported to Anthropic).
- CSP-level incidents (inherited from CSP IR when hosted).

---

## 2. Roles

| Role | Responsibilities |
|---|---|
| Incident Owner | First responder; runs containment playbook; updates audit log |
| Security Officer | Validates classification; authorizes containment escalation |
| Communications Lead | Coordinates customer + US-CERT notifications (when applicable) |
| Maintainer (single-org today) | Combines all three roles pre-hosted; will split at ATO time |

Single-maintainer reality is honestly disclosed; FedRAMP authorization requires role separation, which is part of hosted-control-plane operationalization.

---

## 3. Incident classification

### 3.1 Severity rubric

| Severity | Definition | enchanter-ai trigger examples |
|---|---|---|
| **CRITICAL** | Active compromise; confidentiality or integrity loss imminent | Audit-trail HMAC chain break; secret-scanner miss caught externally; capability-fence bypass observed |
| **HIGH** | Likely-compromise indicators; containment urgent | Canary fixture fires positive; egress-shield deny spike from unknown source; HIGH-CVE in direct dep with active exploit |
| **MODERATE** | Anomaly worth investigating; no compromise indicator | Capability-fence denial spike (10x baseline); novel package detected by package-gate; CodeQL HIGH alert |
| **LOW** | Routine drift; logged, no immediate action | Capability-fence denial (single, expected); first occurrence of known F-code in this session |

### 3.2 Mapping to failure-mode codes

Every incident maps to one or more F-codes from `agent-foundations/shared/conduct/failure-modes.md`. Code drives the runbook:

| F-code | Domain | Runbook |
|---|---|---|
| F01 | Sycophancy | `runbooks/F01.md` |
| F02 | Fabrication | `runbooks/F02.md` |
| F03 | Context decay | `runbooks/F03.md` |
| F04 | Task drift | `runbooks/F04.md` |
| F05 | Instruction attenuation | `runbooks/F05.md` |
| F06 | Premature action | `runbooks/F06.md` |
| F07 | Over-helpful substitution | `runbooks/F07.md` |
| F08 | Tool mis-invocation | `runbooks/F08.md` |
| F09 | Parallel race | `runbooks/F09.md` |
| F10 | Destructive without confirmation | `runbooks/F10.md` |
| F11 | Reward hacking | `runbooks/F11.md` |
| F12 | Degeneration loop | `runbooks/F12.md` |
| F13 | Distractor pollution | `runbooks/F13.md` |
| F14 | Version drift | `runbooks/F14.md` |
| F-001..F-024 | Security closure | `wixie/prompts/security-closure/results/synthesis.md` |

(Plus operational F-codes F15-F21 documented in `agent-foundations/runbooks/` as they are minted.)

---

## 4. Lifecycle — NIST SP 800-61r2

### 4.1 Preparation

| Asset | Status |
|---|---|
| Per-failure-code runbooks | **Shipped** (F01-F21) |
| HMAC-chain audit telemetry | **Shipped** (`hydra/plugins/audit-trail/`) |
| Capability-fence + action-guard + secret-scanner | **Shipped** |
| Canary fixtures | **Shipped** (advisory) |
| Pager channel | **Planned** F-011 |
| US-CERT reporting endpoint | **Planned** (hosted org) |
| 24/7 on-call | **No** (small org) |
| Annual IR tabletop | **Planned** |
| Forensic snapshot capacity | **Partial** (git history + audit-trail JSONL + state dirs are the snapshot) |

### 4.2 Detection and analysis

**Detection sources:**

| Source | Latency | Owner |
|---|---|---|
| audit-trail HMAC chain verify | On-demand (manual) / Daily cron (planned) | hydra/audit-trail |
| capability-fence denial events | Real-time | hydra/capability-fence |
| action-guard skip events | Real-time | hydra/action-guard |
| secret-scanner hits | Real-time | hydra/secret-scanner |
| canary fixture fires | Real-time | hydra/canary |
| egress-shield deny spikes | Real-time → log | hydra/egress-shield |
| Dependabot advisory | Daily | GitHub |
| CodeQL alert | On PR + nightly | GitHub |
| inference-engine SPRT elevation | Per-emit + weekly reconcile | wixie/inference-engine |
| External (US-CERT, Anthropic, customer) | Variable | Communications Lead |

**Analysis steps:**

1. Receive trigger → assign Incident Owner.
2. Look up F-code → open the runbook.
3. Pull relevant audit-trail rows (HMAC-chained, tamper-evident).
4. Confirm or downgrade severity.
5. If CRITICAL or HIGH → notify Security Officer within SLA.
6. Open incident record (file under `state/incidents/<YYYYMMDD>-<slug>.md` — local today, ticket system when hosted).

### 4.3 Containment

Containment is automated where possible; manual where automation is not yet shipped.

| Containment action | Mechanism | Status |
|---|---|---|
| Halt offending subagent | `hydra/plugins/capability-fence/` revokes tool whitelist | **Shipped** |
| Block egress | `hydra/plugins/egress-shield/` add deny rule | **Shipped** |
| Freeze action-guard for destructive ops | Auto on action-guard trip | **Shipped** |
| Rotate compromised key | Manual procedure in audit-trail README | **Manual** |
| Quarantine session | (planned, depends on hosted) | **Planned** |
| Snapshot state | git tag + audit-trail HMAC checkpoint | **Manual** |

### 4.4 Eradication

| Eradication action | Mechanism |
|---|---|
| Patch vulnerable dep | Dependabot auto-PR + manual merge |
| Remove malicious package | package-gate allowlist tighten + lockfile bump |
| Repair audit log | If HMAC chain broke: identify break point, archive prior chain, start new chain with new key, document gap |
| Revoke compromised secret | Operator-side key rotation |
| Re-issue capability whitelist | Update plugin SKILL.md + capability-fence policy bundle |

### 4.5 Recovery

| Recovery action | Mechanism |
|---|---|
| Re-enable subagent class | Update capability-fence policy after fix verified |
| Re-enable egress endpoint | Update egress-shield allowlist after re-assessed |
| Verify integrity | `hydra/plugins/audit-trail/scripts/verify-chain.sh` |
| Replay canary fixtures | Confirm green |
| Monitor at heightened cadence | 2× normal ConMon frequency for 14 days |

### 4.6 Post-incident

Required artifacts:

1. **Incident record** finalized at `state/incidents/<YYYYMMDD>-<slug>.md`.
2. **Precedent log entry** (per `shared/conduct/precedent.md`) so self-observed failures don't recur.
3. **inference-engine artifact emission** (per `shared/conduct/inference-substrate.md`) if pattern is cross-session relevant.
4. **Runbook update** if the runbook missed steps or led to a suboptimal path.
5. **POA&M update** if a new gap was uncovered (`control-implementation/*.md` + `wixie/prompts/security-closure/results/synthesis.md`).
6. **Lessons-learned review** within 14 days of resolution.

---

## 5. Reporting

### 5.1 Internal

| Trigger | Recipient | Channel | SLA |
|---|---|---|---|
| CRITICAL | Security Officer + Communications Lead | Pager (planned) → email today | < 1h |
| HIGH | Security Officer | Pager → email | < 4h |
| MODERATE | Maintainer | Email / ticket | < 24h |
| LOW | Logged only | audit-trail JSONL | n/a |

### 5.2 External (post-ATO)

| Trigger | Recipient | SLA |
|---|---|---|
| Confirmed incident with federal data exposure | US-CERT | 1h (CRITICAL); 24h (HIGH) |
| Confirmed incident | Agency AO | Per ATO terms |
| Confirmed supply-chain compromise | NVD / CISA | Per CISA timelines |
| Anthropic-side compromise indicator | Anthropic security | Best-effort |

Pre-authorization: external reporting paths are **planned**, not wired. US-CERT registration depends on hosted operator org existing.

---

## 6. Tabletop schedule (planned post-authorization)

| Scenario | Frequency |
|---|---|
| Prompt-injection bypass via untrusted source | Semi-annual |
| Secret-scanner miss + egress | Annual |
| Audit-trail HMAC chain break | Annual |
| Supply-chain compromise of direct dep | Annual |
| Subagent capability escape | Annual |

Each tabletop produces: (1) scenario walkthrough, (2) detected vs. missed signals, (3) runbook gaps, (4) POA&M items.

---

## 7. Gaps (honest disclosure)

1. **F-011 pager** — no automated pager wiring; alerts go to stderr today.
2. **No US-CERT registration** — depends on hosted operator org.
3. **Single-maintainer role aggregation** — IR roles not separated.
4. **F-021/F-024 OTLP** — off-host audit copy not yet shipped.
5. **No formal tabletop schedule** — planned, not yet executed.
6. **Forensic snapshot is local-only** — no off-host evidence preservation.
7. **No 24/7 on-call.**
8. **No incident-ticket system** — incidents tracked in local markdown files.

---

## 8. Cross-references

- `fedramp-boundary.md` § 8 (gap list)
- `ssp-skeleton.md` § 9 (control inheritance)
- `control-implementation/IR.md` (per-control IR evidence)
- `conmon-plan.md` § 7 (escalation thresholds)
- `hosted-control-plane-prerequisite.md` (blocks F-011, US-CERT)
- `agent-foundations/runbooks/F*.md` (per-F-code runbooks)
- `agent-foundations/shared/conduct/failure-modes.md` (taxonomy)
