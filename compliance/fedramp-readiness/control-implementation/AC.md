# AC — Access Control (NIST SP 800-53r5)

**Family:** AC (Access Control)
**Baseline:** FedRAMP Moderate
**Document type:** Per-control implementation evidence
**Date:** 2026-05-05
**Status:** Pre-authorization — gaps disclosed honestly

> Implementation column legend: **Implemented** / **Partial** / **Planned** / **N/A** / **Inherited (CSP)** / **Customer**.

---

## AC-1 — Access Control Policy and Procedures
- **Status:** Partial
- **Responsibility:** Shared
- **Evidence:** `agent-foundations/shared/conduct/delegation.md`, `agent-foundations/shared/conduct/skill-authoring.md`, `agent-foundations/compliance/README.md`
- **Gap:** No formal published "Access Control Policy" doc separate from the conduct modules; needs consolidation when hosted control plane is built.

## AC-2 — Account Management
- **Status:** Planned (Customer + Inherited when hosted)
- **Responsibility:** Customer / CSP-inherited
- **Evidence:** Workstation deployment uses local OS accounts. Subagent identity governed by `delegation.md` tool whitelists + capability-fence at runtime.
- **Gap:** No vendor-controlled account lifecycle (no hosted IdP exists). Multi-tenant agency-side accounts blocked on hosted control plane prerequisite. F-013.

## AC-2(1) — Automated System Account Management
- **Status:** Planned
- **Responsibility:** System (when hosted)
- **Evidence:** SCIM provisioning planned with SSO endpoint.
- **Gap:** Hosted control plane prerequisite.

## AC-2(2) — Removal of Temporary / Emergency Accounts
- **Status:** Planned
- **Gap:** Hosted IdP required.

## AC-2(3) — Disable Inactive Accounts
- **Status:** Planned
- **Gap:** Hosted IdP required.

## AC-2(4) — Automated Audit Actions
- **Status:** Implemented (in-system audit trail)
- **Evidence:** `hydra/plugins/audit-trail/scripts/log-event.sh` writes every tool invocation, hook decision, capability check, policy verdict. JSONL with HMAC chain.
- **Gap:** Off-host record copy via OTLP exporter pending (F-021/F-024).

## AC-2(5) — Inactivity Logout
- **Status:** Inherited from host OS / harness
- **Responsibility:** Customer (workstation OS) / CSP (hosted)

## AC-2(7) — Role-based Schemes
- **Status:** Partial
- **Evidence:** Per-plugin SKILL.md `tools:` whitelist constrains by skill role. `delegation.md` defines tier-role-to-tool mappings (investigator: Read/Grep/Glob; red-team: read-only; crafter: Write).
- **Gap:** Role schema is per-plugin, not org-wide.

## AC-2(12) — Account Monitoring for Atypical Usage
- **Status:** Partial
- **Evidence:** `wixie/plugins/inference-engine/` Wald SPRT detects cross-session pattern recurrences. `naga/plugins/naga-observe/` watches for drift.
- **Gap:** No per-account UEBA-style baselining (no accounts in non-hosted form).

## AC-3 — Access Enforcement
- **Status:** Implemented
- **Responsibility:** System
- **Evidence:** `hydra/plugins/capability-fence/hooks/PreToolUse.sh` enforces per-plugin tool whitelists at every tool invocation. `hydra/plugins/action-guard/` gates destructive operations.
- **Gap:** F-010 — escape-hatch CI tests for the sandbox are absent.

## AC-4 — Information Flow Enforcement
- **Status:** Partial
- **Responsibility:** System
- **Evidence:**
  - `hydra/plugins/egress-shield/` allowlist-based outbound URL gating at PreToolUse on WebFetch + Bash (curl/wget).
  - `hydra/plugins/egress-monitor/` observe-mode flow logging.
  - `wixie/plugins/deep-research/` `<untrusted_source>` wrapping for inbound web content.
- **Gap:** F-005 — egress allowlist sparse; not every plugin has explicit entry.

## AC-4(21) — Physical / Logical Separation of Information Flows
- **Status:** Partial
- **Evidence:** Untrusted source isolation in deep-research; capability-fence on every PreToolUse. Sandbox isolation via `lich/plugins/mantis-sandbox`.
- **Gap:** No formal tenant isolation (single-tenant today).

## AC-5 — Separation of Duties
- **Status:** Implemented
- **Evidence:**
  - Authoring agent ≠ review agent (lich/mantis-core).
  - PR author ≠ PR merger (sylph/pr-lifecycle + branch protection).
  - Audit-log writer ≠ verifier (HMAC chain).

## AC-6 — Least Privilege
- **Status:** Implemented
- **Evidence:**
  - `delegation.md` § Tool whitelisting — investigator/red-team/crafter/translator/validator role bundles.
  - `skill-authoring.md` mandates minimum tool whitelist in SKILL.md frontmatter.
  - `hydra/plugins/capability-fence/` runtime enforcement.
  - `hydra/plugins/action-guard/` destructive-op dry-run + confirmation gate.

## AC-6(1) — Authorize Access to Security Functions
- **Status:** Partial
- **Evidence:** Security-relevant plugins (audit-trail, capability-fence, secret-scanner) cannot be invoked by user-level skills; they run as hooks owned by the harness configuration.
- **Gap:** No explicit "security function" registry; relies on convention.

## AC-6(2) — Non-Privileged Access for Nonsecurity Functions
- **Status:** Inherited / Customer
- **Responsibility:** Operator policy

## AC-6(5) — Privileged Accounts
- **Status:** Planned (hosted)
- **Gap:** Hosted control plane required.

## AC-6(7) — Review of User Privileges
- **Status:** Planned (hosted)

## AC-6(9) — Log Use of Privileged Functions
- **Status:** Implemented
- **Evidence:** Every action-guard confirmation, every destructive-op dry-run, every capability override is logged to `hydra/plugins/audit-trail/state/log.jsonl` with HMAC chain.

## AC-6(10) — Prohibit Non-Privileged Users from Executing Privileged Functions
- **Status:** Implemented (in-system)
- **Evidence:** Capability whitelist per subagent role; action-guard PreToolUse hook denies destructive ops absent confirmation.

## AC-7 — Unsuccessful Logon Attempts
- **Status:** Inherited (host OS / hosted IdP when built)

## AC-8 — System Use Notification
- **Status:** Planned (hosted SSO banner)

## AC-10 — Concurrent Session Control
- **Status:** Inherited / Planned (hosted)

## AC-11 — Device Lock
- **Status:** Inherited (host OS)

## AC-12 — Session Termination
- **Status:** Inherited / Planned (hosted)

## AC-14 — Permitted Actions Without Identification or Authentication
- **Status:** Implemented (none permitted in hosted form)

## AC-17 — Remote Access
- **Status:** Planned (hosted) / Customer (workstation)
- **Evidence:** TLS to all external endpoints; egress-shield allowlist; API key isolation by secret-scanner.

## AC-17(1) — Monitoring / Control
- **Status:** Partial
- **Evidence:** `hydra/plugins/egress-monitor/` flow logging.

## AC-17(2) — Protection of Confidentiality / Integrity Using Encryption
- **Status:** Implemented
- **Evidence:** TLS 1.2+ on every external endpoint; HMAC chain on local audit telemetry.

## AC-17(3) — Managed Access Control Points
- **Status:** Planned (hosted)

## AC-17(4) — Privileged Commands / Access
- **Status:** Planned (hosted)

## AC-18 — Wireless Access
- **Status:** Inherited (CSP / host)

## AC-19 — Access Control for Mobile Devices
- **Status:** Customer / Inherited

## AC-20 — Use of External Information Systems
- **Status:** Partial
- **Evidence:** Anthropic API, GitHub, npm, PyPI inventoried in `fedramp-boundary.md` § 2.3 and `ssp-skeleton.md` § 7. All gated by egress-shield.
- **Gap:** No formal customer agreements with external systems beyond standard ToS.

## AC-20(1) — Limits on Use
- **Status:** Implemented (allowlist)

## AC-21 — Information Sharing
- **Status:** N/A (single-tenant today) / Planned (hosted)

## AC-22 — Publicly Accessible Content
- **Status:** N/A (no public-facing system; source on GitHub is project repo, not customer-data system)

---

## Family-level gaps (top 5)

1. **F-013** No multi-tenant identity boundaries — blocked on hosted control plane.
2. **F-010** No escape-hatch CI tests for capability-fence sandbox.
3. **F-005** Egress allowlist sparse.
4. **AC-2 lifecycle** entirely depends on a hosted IdP that does not exist.
5. **No documented Access Control Policy** as a standalone artifact — currently distributed across conduct modules.
