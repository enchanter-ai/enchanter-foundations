# IA — Identification and Authentication (NIST SP 800-53r5)

**Family:** IA (Identification + Authentication)
**Baseline:** FedRAMP Moderate
**Date:** 2026-05-05

> **Family-level note:** Nearly all IA controls are **inherited from the host platform** in the workstation-install reality, and **deferred to the hosted SSO/SCIM endpoint** in the proposed hosted control plane. enchanter-ai itself does not directly implement user authentication — it consumes identity from the harness environment.

---

## IA-1 — Identification and Authentication Policy and Procedures
- **Status:** Partial
- **Evidence:** `delegation.md` (subagent identity), `skill-authoring.md` (tool whitelist as machine identity)
- **Gap:** No standalone IA policy.

## IA-2 — Identification and Authentication (Organizational Users)
- **Status:** Inherited (host OS today) / Planned (hosted SSO when deployed)
- **Responsibility:** Customer / CSP-inherited
- **Evidence:** Workstation: local OS account. Hosted: SAML/OIDC SSO.
- **Gap:** Hosted control plane prerequisite for vendor-enforced authentication.

## IA-2(1) — MFA to Privileged Accounts
- **Status:** Planned (hosted SSO + enforced MFA)
- **Gap:** Hosted IdP required.

## IA-2(2) — MFA to Non-Privileged Accounts
- **Status:** Planned (hosted)
- **Gap:** Same.

## IA-2(8) — Access to Accounts — Replay Resistant
- **Status:** Planned (hosted) / Inherited (CSP)
- **Evidence:** When hosted, SAML/OIDC + short-lived tokens.

## IA-2(12) — Acceptance of PIV Credentials
- **Status:** Planned (federal-tenant requirement)
- **Gap:** Hosted SSO must accept PIV for federal agency users.

## IA-3 — Device Identification and Authentication
- **Status:** Customer / Planned (hosted)
- **Evidence:** Per-developer workstation today.

## IA-4 — Identifier Management
- **Status:** Planned (hosted SCIM lifecycle)
- **Gap:** No vendor-managed identifier store yet.

## IA-4(4) — Identify User Status
- **Status:** Planned (hosted)

## IA-5 — Authenticator Management
- **Status:** Inherited / Planned (hosted)
- **Evidence:** API keys for external services (Anthropic, GitHub) governed by `hydra/plugins/secret-scanner/` — never logged, never echoed; rotation procedure in operator runbook.

## IA-5(1) — Password-Based Authentication
- **Status:** N/A (no password-based auth in-system) / Planned (hosted SSO)

## IA-5(2) — Public-Key-Based Authentication
- **Status:** Customer (GitHub SSH keys; OS SSH agent)

## IA-5(6) — Protection of Authenticators
- **Status:** Implemented (in-system secret handling)
- **Evidence:** `hydra/plugins/secret-scanner/` regex + entropy detection; PreToolUse hook denies tool args containing detected secrets; audit-trail redacts.
- **Gap:** No vendor-controlled secret-vault integration.

## IA-5(7) — No Embedded Unencrypted Static Authenticators
- **Status:** Implemented
- **Evidence:** secret-scanner CI gate; pre-commit checks via `sylph/pr-lifecycle/`.

## IA-5(11) — Hardware Token-Based Authentication
- **Status:** Planned (hosted SSO supports hardware tokens)

## IA-6 — Authentication Feedback
- **Status:** Inherited (host OS / hosted SSO when built)

## IA-7 — Cryptographic Module Authentication
- **Status:** Inherited (host OS / CSP FIPS-validated modules when hosted)
- **Gap:** FIPS 140-3 module validation TBD per hosting choice.

## IA-8 — Identification and Authentication (Non-Organizational Users)
- **Status:** N/A (no non-org-user direct access in-system) / Planned (federated identity, hosted)

## IA-8(1) — Acceptance of PIV Credentials from Other Agencies
- **Status:** Planned (hosted)

## IA-8(2) — Acceptance of External Authenticators
- **Status:** Planned (hosted SSO federation)

## IA-8(4) — Use of Defined Profiles
- **Status:** Planned (hosted)

## IA-11 — Re-Authentication
- **Status:** Inherited (host OS / hosted)

## IA-12 — Identity Proofing
- **Status:** Customer / Planned (hosted, per NIST SP 800-63-3 IAL2 for federal users)

---

## Subagent identity (system-internal)

Although IA-2 through IA-12 are largely inherited or planned, enchanter-ai does manage **subagent identity** internally:

- Every spawned Agent-tool invocation receives an explicit tool whitelist per `delegation.md`.
- The `hydra/plugins/capability-fence/` PreToolUse hook validates each subagent's tool call against its declared whitelist.
- Subagent invocations are tagged in `hydra/plugins/audit-trail/state/log.jsonl` with a `session_id` + `actor` field so cross-subagent action attribution survives.

This is **machine-identity scoping**, not a substitute for organizational user authentication. It is documented here for completeness but does not satisfy IA-2 et al.

---

## Family-level gaps (top 5)

1. **Hosted control plane prerequisite** — IA-2 through IA-12 nearly all depend on hosted SSO/SCIM that does not exist.
2. **No vendor-controlled secret vault** — IA-5(6) relies on host secret storage.
3. **PIV credential acceptance** (IA-2(12), IA-8(1)) — federal requirement, hosted-only.
4. **FIPS 140-3 module validation** — TBD per CSP hosting choice.
5. **No identity proofing** path defined for federal end-users (IA-12).
