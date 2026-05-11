# SI — System and Information Integrity (NIST SP 800-53r5)

**Family:** SI (System + Information Integrity)
**Baseline:** FedRAMP Moderate
**Date:** 2026-05-05

---

## SI-1 — Policy and Procedures
- **Status:** Partial
- **Evidence:** Conduct modules `verification.md`, `failure-modes.md`, `web-fetch.md`.

## SI-2 — Flaw Remediation
- **Status:** Partial
- **Evidence:**
  - Dependabot auto-PR for npm/PyPI vulnerabilities.
  - `sylph/plugins/pr-lifecycle/` ensures vuln-PR review.
  - F-001-F-024 remediation tracked.
- **Gap:** No SLA for flaw remediation (FedRAMP Moderate: 30 days High, 90 days Moderate).

## SI-2(2) — Automated Flaw Remediation Status
- **Status:** Partial
- **Evidence:** Dependabot status surfaces in PR; vuln-detector logs.

## SI-2(3) — Time to Remediate / Benchmarks
- **Status:** Planned (SLA codification)

## SI-3 — Malicious Code Protection
- **Status:** Partial
- **Evidence:**
  - `hydra/plugins/package-gate/` typosquat detection on new npm/PyPI packages.
  - `hydra/plugins/vuln-detector/` CVE feed.
  - `hydra/plugins/canary/` prompt-injection canary fixtures.
- **Gap:** No traditional AV (no executables run server-side today); hosted deployment will need CSP-inherited malware protection.

## SI-3(8) — Detect Unauthorized Commands
- **Status:** Implemented
- **Evidence:** `hydra/plugins/capability-fence/` + `hydra/plugins/action-guard/` block non-whitelisted / destructive commands.

## SI-4 — System Monitoring
- **Status:** Partial
- **Evidence:**
  - `hydra/plugins/audit-trail/` real-time event capture.
  - `hydra/plugins/canary/` synthetic prompt-injection fixtures fire on every WebFetch.
  - `naga/plugins/naga-observe/` drift detection.
  - `wixie/plugins/inference-engine/` Wald SPRT cross-session pattern detection.
- **Gap:** F-011 pager, F-021/F-024 OTLP.

## SI-4(1) — System-Wide Intrusion Detection System
- **Status:** Partial
- **Evidence:** Canary + capability-fence + secret-scanner are domain-specific IDS analogs.

## SI-4(2) — Automated Tools and Mechanisms for Real-Time Analysis
- **Status:** Partial
- **Evidence:** Hooks run in real-time at PreToolUse/PostToolUse.

## SI-4(4) — Inbound and Outbound Communications Traffic
- **Status:** Partial
- **Evidence:** egress-monitor logs all outbound; deep-research `<untrusted_source>` wrapping treats inbound web content as untrusted.

## SI-4(5) — System-Generated Alerts
- **Status:** Partial
- **Evidence:** audit-trail emits alerts to stderr on HIGH events.
- **Gap:** F-011 pager wiring.

## SI-4(12) — Automated Organization-Generated Alerts
- **Status:** Planned

## SI-4(14) — Wireless Intrusion Detection
- **Status:** Inherited (CSP)

## SI-4(16) — Correlate Monitoring Information
- **Status:** Partial
- **Evidence:** inference-engine cross-session correlation.
- **Gap:** Real-time multi-source correlation depends on OTLP backend (F-021/F-024).

## SI-4(22) — Unauthorized Network Services
- **Status:** Implemented (egress-shield allowlist)

## SI-4(23) — Host-Based Devices
- **Status:** Implemented (per-workstation audit-trail + capability-fence)

## SI-5 — Security Alerts, Advisories, and Directives
- **Status:** Partial
- **Evidence:** Dependabot advisories, GitHub Security Advisories, OSV.dev feed.
- **Gap:** No US-CERT subscription / processing channel — depends on hosted operator org.

## SI-6 — Security and Privacy Function Verification
- **Status:** Partial
- **Evidence:**
  - `hydra/plugins/audit-trail/scripts/verify-chain.sh` validates HMAC chain.
  - Plugin self-tests in `tests/` per repo.
- **Gap:** No scheduled verification run (cron); manual today.

## SI-7 — Software, Firmware, and Information Integrity
- **Status:** Partial
- **Evidence:**
  - HMAC chain on audit-trail.
  - git commit signing (developer-side).
  - `hydra/plugins/sbom-emitter/` CycloneDX SBOM.
- **Gap:** F-002 — no signed-artifact provenance (Sigstore/SLSA L3) on releases.

## SI-7(1) — Integrity Checks
- **Status:** Partial
- **Evidence:** verify-chain.sh; lockfile hash checks via npm/PyPI.

## SI-7(2) — Automated Notifications of Integrity Violations
- **Status:** Planned (depends on F-011 pager)

## SI-7(5) — Automated Response to Integrity Violations
- **Status:** Partial
- **Evidence:** action-guard halts; capability-fence denies on policy mismatch.

## SI-7(7) — Integration of Detection and Response
- **Status:** Partial
- **Evidence:** action-guard + audit-trail + capability-fence are linked at PreToolUse.

## SI-7(15) — Code Authentication
- **Status:** Planned (F-002 Sigstore/SLSA L3)

## SI-8 — Spam Protection
- **Status:** N/A (no email ingress)

## SI-10 — Information Input Validation
- **Status:** Implemented
- **Evidence:**
  - `wixie/plugins/deep-research/` `<untrusted_source>` wrapping for web content.
  - `hydra/plugins/secret-scanner/` validates tool args before egress.
  - Plugin schema validation on settings.json.
- **Gap:** Schema validation per-plugin; no central schema-validator gate.

## SI-11 — Error Handling
- **Status:** Partial
- **Evidence:** Conduct module `tool-use.md` § Error payloads — error messages name what + where; never leak secrets.
- **Gap:** No central error-handling policy doc.

## SI-12 — Information Management and Retention
- **Status:** Partial
- **Evidence:** Per-plugin state directories with documented retention.
- **Gap:** No formal retention schedule; depends on AU-11 / hosted backend.

## SI-16 — Memory Protection
- **Status:** Inherited (host OS / CSP)

---

## Family-level gaps (top 5)

1. **F-002** No signed-artifact provenance — SI-7(15) blocked.
2. **F-011 pager** — SI-4(5), SI-7(2) blocked.
3. **F-021/F-024 OTLP** — SI-4(16) real-time correlation limited.
4. **No SLA for flaw remediation** — SI-2 needs codified timelines.
5. **No central schema-validator gate** — SI-10 per-plugin only.
