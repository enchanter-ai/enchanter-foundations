# IR — Incident Response (NIST SP 800-53r5)

**Family:** IR (Incident Response)
**Baseline:** FedRAMP Moderate
**Date:** 2026-05-05
**Companion artifact:** `../incident-response-plan.md`

---

## IR-1 — Incident Response Policy and Procedures
- **Status:** Implemented (per-failure-code runbooks)
- **Evidence:** `agent-foundations/runbooks/F0*.md` — F01 through F21 documented runbooks covering each named failure mode from `agent-foundations/shared/conduct/failure-modes.md`.
- **Gap:** No single "IR Policy" cover doc; runbooks are per-code. Consolidated in `../incident-response-plan.md`.

## IR-2 — Incident Response Training
- **Status:** Partial
- **Evidence:** Conduct modules are the training material — every contributor reads `agent-foundations/shared/conduct/*.md`. `failure-modes.md` is the named-taxonomy training.
- **Gap:** No formal training-completion attestation.

## IR-2(1) — Simulated Events
- **Status:** Partial
- **Evidence:** `hydra/plugins/canary/` fires synthetic prompt-injection fixtures on WebFetch — a continuous tabletop for SI-4 / IR-4.
- **Gap:** No scheduled IR tabletop exercise.

## IR-2(2) — Automated Training Environments
- **Status:** N/A (small org)

## IR-3 — Incident Response Testing
- **Status:** Partial
- **Evidence:** Canary fixtures fire in production-equivalent path; runbooks include test commands.
- **Gap:** No annual IR test plan execution.

## IR-3(2) — Coordination with Related Plans
- **Status:** Partial
- **Evidence:** IR plan cross-references SI (canary), SC (egress), AC (capability-fence), AU (audit-trail).

## IR-4 — Incident Handling
- **Status:** Implemented
- **Evidence:**
  - **Preparation:** Conduct modules + runbooks + plugin defenses pre-deployed.
  - **Detection + analysis:** audit-trail HMAC chain, canary fires, secret-scanner hits, capability-fence denials, action-guard skips.
  - **Containment:** action-guard halts destructive ops; capability-fence denies further tool use by offending subagent.
  - **Eradication:** Per-F-code runbook actions.
  - **Recovery:** git revert + audit-trail re-verification.
  - **Post-incident:** Emit precedent log entry + `wixie/plugins/inference-engine/` artifact for cross-session learning.
- **Gap:** F-011 — no automated pager on HIGH+ severity events.

## IR-4(1) — Automated Incident Handling Processes
- **Status:** Partial
- **Evidence:** action-guard auto-halts; capability-fence auto-denies; canary auto-alerts.
- **Gap:** Pager wiring + auto-quarantine of offending session pending.

## IR-4(4) — Information Correlation
- **Status:** Partial
- **Evidence:** `wixie/plugins/inference-engine/` Wald SPRT correlates patterns across sessions.
- **Gap:** Real-time multi-source correlation needs OTLP aggregation (F-021/F-024).

## IR-5 — Incident Monitoring
- **Status:** Implemented (in-system)
- **Evidence:** audit-trail JSONL captures every event; `naga/plugins/naga-observe/` watches drift.
- **Gap:** Off-host monitoring pending (F-021/F-024).

## IR-5(1) — Automated Tracking / Data Collection / Analysis
- **Status:** Partial
- **Evidence:** Inference-engine reconcile.

## IR-6 — Incident Reporting
- **Status:** Planned
- **Evidence:** Runbooks specify "report to operator" but no formal report channel.
- **Gap:** US-CERT / agency-reporting endpoint depends on hosted operator org.

## IR-6(1) — Automated Reporting
- **Status:** Planned
- **Gap:** Depends on F-011 + F-021 + hosted operator.

## IR-7 — Incident Response Assistance
- **Status:** Partial
- **Evidence:** Runbook chain is the assistance; maintainer reachable via GitHub Issues.
- **Gap:** No 24/7 support model — depends on hosted operator org.

## IR-7(1) — Automation Support
- **Status:** Partial
- **Evidence:** Runbooks include automated triage steps.

## IR-8 — Incident Response Plan
- **Status:** Implemented (this folder)
- **Evidence:** `../incident-response-plan.md`
- **Gap:** Plan is preparatory; needs version control + annual review cadence once authorized.

## IR-9 — Information Spillage Response
- **Status:** Partial
- **Evidence:**
  - `hydra/plugins/secret-scanner/` PreToolUse blocks secrets in tool args before they reach external systems.
  - audit-trail redaction excludes detected secrets from logs.
  - egress-shield denies unallowed outbound destinations.
- **Gap:** No formal spillage drill; depends on hosted reporting channel.

## IR-9(2) — Training
- **Status:** Implemented (conduct modules + runbooks)

## IR-9(3) — Post-Spill Operations
- **Status:** Partial
- **Evidence:** Runbook F-021 (audit-trail tampering) + F-009 (vuln-detector hits) cover related scenarios.

## IR-9(4) — Exposure to Unauthorized Personnel
- **Status:** Planned (hosted operator)

---

## Family-level gaps (top 5)

1. **F-011** No automated pager — IR-4(1), IR-6(1) blocked.
2. **No formal IR tabletop schedule** — IR-3 partial.
3. **No hosted operator org** — IR-6, IR-7, IR-9 reporting endpoints undefined.
4. **F-021/F-024** OTLP — cross-session correlation limited.
5. **No US-CERT registration** — federal incident reporting endpoint undefined.
