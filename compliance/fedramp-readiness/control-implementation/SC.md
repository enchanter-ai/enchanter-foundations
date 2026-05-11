# SC — System and Communications Protection (NIST SP 800-53r5)

**Family:** SC (System + Communications Protection)
**Baseline:** FedRAMP Moderate
**Date:** 2026-05-05

---

## SC-1 — Policy and Procedures
- **Status:** Partial
- **Evidence:** `hydra/plugins/egress-shield/`, `hydra/plugins/egress-monitor/`, conduct module `web-fetch.md`.

## SC-2 — Separation of System and User Functionality
- **Status:** Implemented
- **Evidence:** Plugin hooks (security functions) run separately from user-invocable skills; capability-fence enforces.

## SC-3 — Security Function Isolation
- **Status:** Partial
- **Evidence:** Security plugins (audit-trail, capability-fence, secret-scanner, action-guard, config-shield, egress-shield) run as harness-registered hooks; not user-invocable skills.
- **Gap:** No formal isolation primitive beyond hook-vs-skill split.

## SC-4 — Information in Shared System Resources
- **Status:** Partial
- **Evidence:** Local state directories scoped per-plugin; audit-trail redacts secrets.
- **Gap:** Multi-tenant shared-resource isolation depends on hosted boundary.

## SC-5 — Denial of Service Protection
- **Status:** Partial
- **Evidence:**
  - `pech/plugins/rate-shield/` per-tool rate limits at PreToolUse.
  - `pech/plugins/budget-watcher/` halts on cost budget breach.
- **Gap:** F-013 multi-tenant DoS protection requires hosted rate-limiter backend.

## SC-5(1) — Restrict Ability to Attack Other Systems
- **Status:** Implemented
- **Evidence:** egress-shield allowlist denies outbound to non-allowlisted destinations.

## SC-6 — Resource Availability
- **Status:** Inherited / Customer (workstation) / Planned (hosted)

## SC-7 — Boundary Protection
- **Status:** Implemented (partial coverage)
- **Evidence:**
  - **`hydra/plugins/egress-shield/`** PreToolUse hook gates WebFetch + Bash (curl/wget) against `config/allowlist.yaml`.
  - **`hydra/plugins/egress-monitor/`** observe-mode flow logging.
  - **`hydra/plugins/reach-filter/`** restricts skill discovery surface.
  - **`wixie/plugins/deep-research/`** `<untrusted_source>` wrapping isolates untrusted inbound web content.
- **Canonical connection inventory:** `hydra/plugins/egress-shield/config/allowlist.yaml`.
- **Gap:** F-005 — allowlist sparse; not all plugins have entries.

## SC-7(3) — Access Points
- **Status:** Implemented
- **Evidence:** Egress goes through Bash + WebFetch hook gates (the only two egress paths); both gated by egress-shield.

## SC-7(4) — External Telecommunications Services
- **Status:** Partial
- **Evidence:** Anthropic API + GitHub + npm/PyPI + OTLP (planned) catalogued in boundary doc § 2.3 and SSP § 7.

## SC-7(5) — Deny by Default / Allow by Exception
- **Status:** Implemented
- **Evidence:** egress-shield is allowlist-based; default-deny on unmatched URLs.

## SC-7(7) — Split Tunneling
- **Status:** N/A (no VPN)

## SC-7(8) — Route Traffic to Authenticated Proxy Servers
- **Status:** Planned (hosted egress proxy)

## SC-7(12) — Host-Based Protection
- **Status:** Inherited (host OS firewall) / Customer

## SC-7(13) — Isolation of Security Tools, Mechanisms, Support Components
- **Status:** Partial
- **Evidence:** Security plugins run as hooks; not modifiable by user skills (config-shield protects).

## SC-7(18) — Fail Secure
- **Status:** Implemented
- **Evidence:** egress-shield denies on policy-load failure (fail-closed for egress). Audit-trail fails open per `hooks.md` advisory contract; egress-shield is the exception — fails closed.

## SC-8 — Transmission Confidentiality and Integrity
- **Status:** Implemented
- **Evidence:** All external endpoints use TLS 1.2+ (TLS 1.3 preferred). Egress-shield allowlist scheme requires `https://`.
- **Gap:** TLS pinning planned in enchanter CLI when shipped; not yet.

## SC-8(1) — Cryptographic Protection
- **Status:** Implemented (TLS); FIPS module validation TBD per hosting.

## SC-10 — Network Disconnect
- **Status:** Inherited / Planned (hosted)

## SC-12 — Cryptographic Key Establishment and Management
- **Status:** Partial
- **Evidence:**
  - HMAC key for audit-trail chain — operator-provisioned at install; rotation procedure documented.
  - TLS certs — inherited from host platform.
  - API keys (Anthropic, GitHub) — operator-provisioned; secret-scanner enforces non-logging.
- **Gap:** No vendor-controlled KMS — depends on hosted control plane + CSP KMS (AWS KMS GovCloud / Azure Key Vault Gov).

## SC-12(1) — Availability
- **Status:** Inherited (CSP KMS when hosted)

## SC-12(2) — Symmetric Keys
- **Status:** Planned (CSP KMS-managed)

## SC-12(3) — Asymmetric Keys
- **Status:** Planned (CSP KMS-managed)

## SC-13 — Cryptographic Protection
- **Status:** Partial
- **Evidence:** HMAC-SHA256 (audit-trail), SHA-1 (inference fingerprint dedup only, non-security), TLS 1.2+ (transport).
- **Gap:** FIPS 140-3 module validation TBD per hosting; SHA-1 usage flagged for documentation but acceptable (non-security).

## SC-15 — Collaborative Computing Devices and Applications
- **Status:** N/A

## SC-17 — Public Key Infrastructure Certificates
- **Status:** Inherited (CSP / host)

## SC-18 — Mobile Code
- **Status:** Partial
- **Evidence:** `hydra/plugins/package-gate/` denies non-allowlisted npm/PyPI packages; `hydra/plugins/license-gate/` denies copyleft.
- **Gap:** Runtime executable verification absent.

## SC-20 — Secure Name / Address Resolution Service (Authoritative Source)
- **Status:** Inherited (CSP DNS / host)

## SC-21 — Secure Name / Address Resolution Service (Recursive or Caching Resolver)
- **Status:** Inherited

## SC-22 — Architecture and Provisioning for Name / Address Resolution Service
- **Status:** Inherited

## SC-23 — Session Authenticity
- **Status:** Inherited (TLS) / Planned (hosted session tokens)

## SC-28 — Protection of Information at Rest
- **Status:** Partial
- **Evidence:** audit-trail file permissions; secret-scanner redaction prevents secrets at rest in logs.
- **Gap:** No disk encryption enforcement (customer host responsibility); when hosted, inherit CSP storage encryption.

## SC-28(1) — Cryptographic Protection
- **Status:** Planned (hosted, inherit CSP)

## SC-39 — Process Isolation
- **Status:** Partial
- **Evidence:** `lich/plugins/mantis-sandbox/` provides sandboxed execution.
- **Gap:** Process isolation primitives are OS-level inherited.

## SC-45 — System Time Synchronization
- **Status:** Inherited (host NTP / CSP NTP)

---

## Family-level gaps (top 5)

1. **F-005** Egress allowlist sparse — biggest SC-7 gap.
2. **F-013** Multi-tenant DoS protection requires hosted backend.
3. **No vendor-controlled KMS** — SC-12 depends on hosted control plane + CSP KMS.
4. **FIPS 140-3 validation** TBD per hosting choice.
5. **TLS pinning in enchanter CLI** planned but not shipped.
