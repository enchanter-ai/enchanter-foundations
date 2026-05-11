# AU — Audit and Accountability (NIST SP 800-53r5)

**Family:** AU (Audit + Accountability)
**Baseline:** FedRAMP Moderate
**Date:** 2026-05-05

---

## AU-1 — Audit and Accountability Policy and Procedures
- **Status:** Partial
- **Evidence:** `hydra/plugins/audit-trail/` README; `agent-foundations/compliance/README.md`; conduct modules.
- **Gap:** No standalone policy document; need consolidation when hosted.

## AU-2 — Event Logging
- **Status:** Implemented
- **Responsibility:** System
- **Evidence:** `hydra/plugins/audit-trail/scripts/log-event.sh` logs:
  - Every PreToolUse + PostToolUse invocation
  - Every hook decision
  - Every capability-fence verdict
  - Every action-guard destructive-op confirmation
  - Every secret-scanner hit
  - Every egress-shield deny / allow
  - Every canary fire
- **Format:** JSONL, one event per line.
- **Integrity:** HMAC-SHA256 chain — each entry's `hmac` field is `HMAC(prev_entry || this_entry)`.

## AU-3 — Content of Audit Records
- **Status:** Implemented
- **Evidence:** Each JSONL entry includes: `timestamp`, `session_id`, `actor` (agent/subagent), `event_type`, `tool`, `args` (redacted by secret-scanner), `outcome`, `policy_verdict`, `prev_hmac`, `hmac`.
- **Gap:** Field set is per-plugin convention; no schema-validation gate yet.

## AU-3(1) — Additional Audit Information
- **Status:** Partial
- **Evidence:** Tool args + outputs captured (truncated > 8KB per plugin convention).
- **Gap:** No structured user-identity field (single-user workstation context); hosted IdP would populate.

## AU-4 — Audit Log Storage Capacity
- **Status:** Partial
- **Evidence:** Local disk; rotation via per-plugin convention.
- **Gap:** No formal capacity-planning doc; OTLP off-host export (F-021/F-024) deferred.

## AU-4(1) — Transfer to Alternate Storage
- **Status:** Planned
- **Gap:** F-021/F-024 OTLP exporter not yet shipped.

## AU-5 — Response to Audit Logging Process Failures
- **Status:** Partial
- **Evidence:** audit-trail hook fails open (per `hooks.md` advisory contract) but emits stderr warning. Verification script flags broken HMAC chains.
- **Gap:** No automated alert on logging failure (depends on F-011 pager wiring).

## AU-6 — Audit Record Review, Analysis, Reporting
- **Status:** Partial
- **Evidence:** Manual via verify-chain.sh; quarterly self-attestation review.
- **Gap:** No real-time analysis; SIEM-style aggregation depends on F-021/F-024.

## AU-6(1) — Automated Process Integration
- **Status:** Planned
- **Gap:** Hosted control plane prerequisite.

## AU-6(3) — Correlate Audit Repositories
- **Status:** Planned
- **Gap:** Cross-tenant correlation depends on hosted multi-tenant model.

## AU-7 — Audit Record Reduction and Report Generation
- **Status:** Partial
- **Evidence:** `wixie/plugins/inference-engine/` reconcile generates per-plugin briefings from audit-trail-derived evidence streams.
- **Gap:** No general-purpose reporting UI.

## AU-7(1) — Automatic Processing
- **Status:** Implemented (inference-engine reconcile)
- **Evidence:** `wixie/shared/scripts/inference-engine.py` runs Wald SPRT + Beta-Binomial.

## AU-8 — Time Stamps
- **Status:** Implemented
- **Evidence:** Each audit entry's `timestamp` is ISO-8601 UTC stamped by audit-trail hook.

## AU-8(1) — Synchronization with Authoritative Time Source
- **Status:** Inherited (host OS / CSP NTP)

## AU-9 — Protection of Audit Information
- **Status:** Implemented
- **Evidence:** HMAC chain detects tampering. Audit log file is append-only by convention; hook never rewrites.
- **Gap:** File-system-level append-only enforcement (chattr +a / equivalent) is opt-in customer configuration; not enforced by plugin.

## AU-9(2) — Store on Separate Physical Systems
- **Status:** Planned
- **Gap:** F-021/F-024.

## AU-9(3) — Cryptographic Protection
- **Status:** Implemented (HMAC chain)
- **Evidence:** HMAC-SHA256 secret per-deployment; rotation procedure documented in audit-trail README.
- **Gap:** Key rotation cadence not enforced; manual today.

## AU-9(4) — Access by Subset of Privileged Users
- **Status:** Inherited (host filesystem perms / hosted IAM)

## AU-10 — Non-Repudiation
- **Status:** Partial
- **Evidence:** HMAC chain + per-actor `session_id` and `actor` field.
- **Gap:** No public-key signature on entries; HMAC is symmetric — verifier shares key with writer.

## AU-11 — Audit Record Retention
- **Status:** Planned
- **Gap:** Retention policy (FedRAMP Moderate: 90 days online + 1 year archived) depends on OTLP backend choice.

## AU-12 — Audit Generation
- **Status:** Implemented
- **Evidence:** audit-trail generates records on every governed event. See AU-2.
- **Gap:** Off-host copy F-021/F-024.

## AU-12(1) — System-Wide / Time-Correlated Audit Trail
- **Status:** Partial
- **Evidence:** Single-workstation HMAC chain provides system-wide ordering.
- **Gap:** Cross-workstation correlation requires hosted OTLP.

## AU-12(3) — Changes by Authorized Individuals
- **Status:** N/A (audit log is append-only; no edits permitted)

---

## Family-level gaps (top 5)

1. **F-021/F-024** OTLP exporter — blocks AU-4(1), AU-6(1), AU-9(2), AU-11, AU-12(1) cross-host.
2. **HMAC key rotation** manual; no scheduled rotation policy enforced.
3. **No real-time alerting** on AU-5 logging-process failures — depends on F-011 pager.
4. **No audit-schema validation gate** — relies on per-plugin convention.
5. **No append-only filesystem enforcement** — relies on customer host config.
