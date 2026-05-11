# System Security Plan (SSP) — enchanter-ai

**Document type:** SSP skeleton (FedRAMP Rev 5 SSP template-shaped)
**Document version:** 0.1 (DRAFT — pre-authorization, advisory)
**Date:** 2026-05-05
**Baseline proposed:** FedRAMP Moderate
**Status:** **Pre-authorization.** This is not a submitted SSP. It is an architectural skeleton that maps enchanter-ai onto FedRAMP's SSP template so a 3PAO and an agency sponsor can begin scoping conversations.

> **Critical pre-requisite:** enchanter-ai is currently a **developer-workstation install**, not a hosted SaaS. FedRAMP authorizes hosted services. The boundary described below assumes a hosted control plane that does not yet exist. See `hosted-control-plane-prerequisite.md` for the architectural gap.

---

## 1. System identification

| Field | Value |
|---|---|
| System name | enchanter-ai |
| Short name | enchanter |
| Version | 0.x (pre-1.0; per-plugin versions in `<repo>/plugins/<plugin>/manifest.json`) |
| Unique identifier | TBD (assigned at FedRAMP package submission) |
| System owner | enchanter-ai maintainer (TBD organization) |
| Authorizing official | TBD (post-hosted-deployment) |
| System security officer | TBD |
| Vendor | enchanter-ai project |
| Service model | SaaS (proposed — see prerequisite doc) |
| Deployment model | Public cloud (proposed) |
| Authorization path | JAB P-ATO or agency ATO (TBD) |
| Categorization | FIPS 199 **Moderate** (proposed) |

---

## 2. System description

### 2.1 Purpose

enchanter-ai is an **agent substrate** — a coordinated set of plugins, hooks, skills, conduct modules, and runbooks that govern the runtime behavior of Anthropic's Claude Code agent. The substrate enforces operational discipline (audit, capability fencing, egress allowlisting, supply-chain validation, drift detection, cost governance, PR lifecycle, code-review gating) so AI-assisted development at federal-customer sites runs under documented controls.

### 2.2 What enchanter-ai is not

- It is **not** an LLM. The underlying model is Anthropic Claude (out-of-boundary external system).
- It is **not** a code editor. It operates inside the Claude Code harness (also OOB — Anthropic product).
- It is **not** a workflow orchestrator in the Airflow/Temporal sense. It is a behavioral overlay on a single-process agent runtime.

### 2.3 Users

| Role | Description | Authentication |
|---|---|---|
| Developer / operator | Person invoking Claude Code with enchanter-ai installed | Local OS account (workstation today); SSO + MFA when SaaS (proposed) |
| Plugin maintainer | Contributor with write access to a repo | GitHub OAuth + branch protection |
| Compliance reviewer | Reader of `compliance/` artifacts | Read-only repo access |
| Auditor (future) | 3PAO assessor | TBD per SaaS auth model |
| Subagent (machine identity) | Spawned Agent-tool instance scoped by `delegation.md` | Inherited from harness; capability whitelist enforced |

---

## 3. System boundary

### 3.1 Authorization boundary

See `fedramp-boundary.md` § 3 for the canonical diagram. Text rendering retained inline for SSP self-containment.

```
+============================================================+
|                AUTHORIZATION BOUNDARY                      |
|   (proposed hosted control plane — not yet deployed)       |
|                                                            |
|  Claude Code harness (Anthropic, OOB)                      |
|       <--+ enchanter-ai plugins (11 repos, ~73 plugins)    |
|            - hydra (defensive controls, 15)                |
|            - wixie (prompt lifecycle + inference, 9)       |
|            - pech  (cost + budget, 7)                      |
|            - sylph (PR + branch + CI, 9)                   |
|            - lich  (code-review subagent mantis, 8)        |
|            - crow  (decision oversight, 4)                 |
|            - emu   (context + state, 3)                    |
|            - gorgon (code analysis, 6)                     |
|            - naga  (cross-repo + observability, 6)         |
|            - djinn (drift + intent, 6)                     |
|            - agent-foundations (conduct + runbooks)        |
|                                                            |
|       Local state: audit-trail HMAC chain,                 |
|                    inference-engine catalog, precedent     |
+============================================================+
   |             |             |               |
   v             v             v               v
 Anthropic    GitHub        npm/PyPI         OTLP collector
 API (OOB)    API (OOB)     (OOB)            (OOB, planned)
```

### 3.2 Reference

`agent-foundations/docs/architecture/highlevel.mmd` is the source-of-truth Mermaid diagram. The text rendering above is the FedRAMP-consumable form.

### 3.3 Boundary delineation rationale

- **In-boundary:** anything that processes federal-customer prompts, tool invocations, tool outputs, or audit telemetry.
- **OOB:** the Claude Code harness binary (Anthropic), the LLM API (Anthropic), GitHub source-control APIs, package registries.
- **Connections to OOB:** every external endpoint is gated by `hydra/egress-shield/config/allowlist.yaml` — that file is the canonical connection inventory for SC-7.

---

## 4. Information types and categorization

### 4.1 Information types (NIST SP 800-60v2 mappings)

| Information type | NIST 800-60 ID | Sensitivity | Where it flows | Where it rests |
|---|---|---|---|---|
| Developer / user prompts | C.3.5.1 (System Development) | **Moderate** (may include CUI in federal deployment) | User → harness → Anthropic API | hydra/audit-trail log; wixie/prompts/<name>/ |
| Tool invocations + arguments | C.3.5.1 | Moderate | Harness → plugin hooks → audit log | hydra/audit-trail/state/log.jsonl |
| Tool outputs (file content, web content, API responses) | Variable | Moderate (may include CUI) | Tool → harness → audit log | hydra/audit-trail/state/log.jsonl |
| Source code | C.3.5.2 | Customer IP — Moderate | Git ↔ harness ↔ editor | Customer git repo (boundary edge) |
| Secrets (API keys, tokens) | C.2.6.1 (Access Control Information) | High; detected and redacted | Never logged | Excluded by hydra/secret-scanner |
| Audit telemetry | C.3.5.1 (System and Network Monitoring) | Moderate (integrity-critical) | Plugin → audit-trail → OTLP (planned) | HMAC chain; external collector |
| Cross-session learning artifacts | C.3.5.1 | Internal evidence; Low-Moderate | Plugin → inference-engine | wixie/plugins/inference-engine/state/* |
| SBOM artifacts | C.3.5.1 | Publicly disclosable | Release pipeline | hydra/sbom-emitter state; release asset |

### 4.2 FIPS 199 categorization

| Objective | Impact | Rationale |
|---|---|---|
| Confidentiality | **Moderate** | Prompts and tool outputs may carry CUI from federal customer workloads |
| Integrity | **Moderate** | Tampered audit logs or capability-fence configs would undermine all controls; HMAC chain mitigates |
| Availability | **Low** | Workstation tool; agent unavailability is inconvenience, not mission-critical |

**Overall categorization:** Moderate (highest of the three).

---

## 5. System inventory

### 5.1 Software inventory (plugins, in-boundary)

The full plugin inventory is in `fedramp-boundary.md` § 2.1. Summary:

| Repo | Plugins | Role |
|---|---|---|
| agent-foundations | n/a (shared conduct + runbooks) | Behavioral defaults, taxonomy |
| hydra | 15 | Defensive controls |
| wixie | 9 | Prompt lifecycle + inference engine |
| pech | 7 | Cost + budget |
| sylph | 9 | PR + branch + CI |
| lich | 8 | Code-review subagent (mantis) |
| crow | 4 | Decision oversight |
| emu | 3 | Context + state |
| gorgon | 6 | Code analysis |
| naga | 6 | Cross-repo + observability |
| djinn | 6 | Drift + intent |
| **Total** | **~73 plugins** | |

Each plugin has a manifest at `<repo>/plugins/<plugin>/manifest.json` and a SKILL.md per skill with `name`, `description`, `model`, `tools` frontmatter.

### 5.2 External dependencies (supply chain, in-boundary)

| Component | Type | Risk control plugin |
|---|---|---|
| Node.js + npm registry packages | Runtime + tooling | hydra/package-gate, hydra/license-gate, hydra/vuln-detector, hydra/sbom-emitter |
| Python + PyPI packages | Tooling (inference-engine, scripts) | Same |
| Git + GitHub Actions | CI/CD | sylph/pr-lifecycle; CodeQL workflow; Dependabot |
| Anthropic Claude API | LLM provider | hydra/egress-shield allowlist |

### 5.3 External systems (OOB; connections inventoried)

| System | Direction | Data classification | Connection control |
|---|---|---|---|
| Anthropic Claude API | Outbound | Up to CUI | hydra/egress-shield; API-key isolation |
| GitHub | Bi | Source + configs | OAuth token; sylph/pr-lifecycle |
| npm + PyPI | Inbound (fetch) | Public package metadata | hydra/package-gate |
| Web (deep-research fetches) | Outbound | Public web content | hydra/egress-shield; `<untrusted_source>` wrapping |
| OTLP collector (planned) | Outbound | Audit telemetry | TLS + auth token |

### 5.4 Hardware inventory

Workstation today (out of scope for FedRAMP since not hosted). When hosted: cloud IaaS components inherit from the underlying CSP's FedRAMP authorization (e.g., AWS GovCloud, Azure Government). enchanter-ai itself is the application layer above the IaaS authorization boundary.

---

## 6. User roles and access

### 6.1 Role definitions

| Role | Privileges | Authentication (proposed SaaS) |
|---|---|---|
| Developer / agency end-user | Invoke skills, run agents on own data | SSO (SAML/OIDC) + MFA |
| Plugin maintainer | Edit plugin source, merge PRs | GitHub OAuth + branch protection + signed commits |
| Operator / SRE | Operate hosted control plane, view telemetry | SSO + MFA + privileged-access workstation |
| Compliance reviewer | Read compliance artifacts, audit logs | SSO + MFA, read-only |
| 3PAO assessor | Read access to source, configs, audit logs | Time-bounded SSO grant |
| Authorizing official | Sign ATO; read assessment artifacts | SSO + MFA |

### 6.2 Authentication

Workstation today: local OS account. Proposed SaaS: SAML/OIDC SSO with MFA; SCIM provisioning for agency-managed identity. See AC family in `control-implementation/AC.md`.

### 6.3 Separation of duties

- Plugin author ≠ plugin reviewer (sylph/pr-lifecycle).
- Code authoring agent ≠ code review subagent (lich/mantis).
- Audit log writers ≠ audit log readers (HMAC chain prevents writer tampering; readers verify).

---

## 7. Network connections

The **canonical connection inventory** is `hydra/plugins/egress-shield/config/allowlist.yaml` (gap F-005: currently sparse). For SSP purposes, the inventory below is authoritative as of 2026-05-05.

| # | Endpoint | Direction | Purpose | Owner plugin | Authentication |
|---|---|---|---|---|---|
| 1 | https://api.anthropic.com/* | Outbound | LLM API | wixie, lich, crow, any LLM consumer | API key (per-deployment) |
| 2 | https://api.github.com/* | Outbound | gh CLI git ops | sylph | OAuth token |
| 3 | https://github.com/* | Outbound | git fetches | sylph | OAuth or SSH key |
| 4 | https://registry.npmjs.org/* | Outbound | npm metadata | hydra/package-gate, hydra/sbom-emitter | none (public) |
| 5 | https://pypi.org/* | Outbound | PyPI metadata | hydra/package-gate, hydra/vuln-detector | none |
| 6 | https://api.osv.dev/* | Outbound (planned) | Vuln feed | hydra/vuln-detector | none |
| 7 | https://spdx.org/*, https://*.fsf.org | Outbound | License metadata | hydra/license-gate | none |
| 8 | Web fetches (per-task) | Outbound | Research | wixie/deep-research (Haiku fetcher) | none; allowlist + budget |
| 9 | OTLP collector (planned) | Outbound | Telemetry | hydra/audit-trail | TLS + bearer token |

All connections use TLS 1.2+ (SC-8, SC-12 — see `control-implementation/SC.md`). Connection #1 (Anthropic API) carries the most sensitive data flow; key isolation is enforced by hydra/secret-scanner pre-egress sweep.

---

## 8. Cryptographic protections (summary)

| Use case | Algorithm | Implementation |
|---|---|---|
| Audit-log integrity | HMAC-SHA256 chain | hydra/plugins/audit-trail/scripts/log-event.sh |
| Inference-engine fingerprint | SHA-1 (non-security; deduplication only) | wixie/shared/scripts/inference-engine.py |
| TLS to external systems | TLS 1.2+ (1.3 preferred) | Host platform |
| Code signing (planned, F-002) | Sigstore / SLSA L3 | Release pipeline |
| Secret detection | Regex + entropy (gitleaks-style) | hydra/plugins/secret-scanner |

FIPS 140-3 validated module status: TBD per host platform when SaaS deployed. The audit-log HMAC implementation today uses OS-provided OpenSSL; FIPS-mode operation must be validated as part of the hosted-deployment work (gap; tracked in `hosted-control-plane-prerequisite.md`).

---

## 9. Control summary and inheritance

Detailed per-control evidence: `control-implementation/<family>.md`. Inheritance summary:

| Family | In-system | Inherited from CSP | Customer responsibility |
|---|---|---|---|
| AC | Capability-fence, scope-fence (delegation), action-guard | IAM, MFA, SSO (when on cloud CSP) | Per-user role assignment |
| AU | audit-trail HMAC, OTLP exporter (planned) | CloudTrail / Azure Monitor / GCP Cloud Logging | Log retention policy |
| CM | config-shield, action-guard, package-gate, version pins | CSP config management for IaaS | Change-approval workflow |
| IA | Subagent identity via capability whitelist | **Mostly inherited** — SSO/MFA from CSP | Identity store population |
| IR | Runbooks F01-F21; audit-trail evidence | CSP incident-response infra | Customer-side comms |
| RA | vuln-detector, secret-scanner, canary, inference-engine | CSP threat intel feeds | Acceptance of residual risk |
| SC | egress-shield, egress-monitor, TLS via host | CSP boundary protection (VPC, WAF, DDoS) | DNS, customer VPN if any |
| SI | canary, HMAC chain, deep-research sanitization, sbom-emitter | CSP malware / IDS | Patching policy |
| SR | package-gate, sbom-emitter, license-gate, SLSA L3 (planned) | CSP vendor-management inheritance | Customer's own SBOM consumption |

---

## 10. SSP maintenance

This skeleton is updated on a **quarterly** cadence by the enchanter-ai maintainer. Triggers for off-cycle update:

- New plugin shipped that adds an external connection.
- Change to authorization boundary (e.g., the hosted control plane stand-up).
- Significant change to a security-relevant control implementation.
- New gap discovered by 3PAO scoping conversation, vuln scan, or audit-trail review.

Drafts are reviewed by sylph/pr-lifecycle. Final versions are tagged in git so prior SSP states are auditable.

---

## 11. References

- `fedramp-boundary.md` — boundary document (peer artifact)
- `control-implementation/*.md` — per-family control evidence
- `conmon-plan.md` — continuous monitoring plan
- `incident-response-plan.md` — IR plan
- `3pao-scoping-package.md` — 3PAO handoff
- `hosted-control-plane-prerequisite.md` — architectural prerequisite (READ FIRST)
- `agent-foundations/docs/architecture/highlevel.mmd` — architecture diagram

---

## 12. Pre-authorization disclaimer

This SSP skeleton is **NOT** a FedRAMP submission. It is preparatory material. FedRAMP authorization requires:

1. A hosted SaaS deployment (today: workstation only — gap).
2. A complete SSP, ~200+ pages, expanded from this skeleton.
3. A 3PAO-executed Security Assessment Plan (SAP) and resulting Security Assessment Report (SAR).
4. A Plan of Action and Milestones (POA&M) with remediation timelines.
5. An Authorization to Operate (ATO) signed by an agency authorizing official, or a Joint Authorization Board P-ATO.
6. Continuous monitoring evidence over time (typically 12+ months pre-authorization data).

Realistic timeline from architectural prerequisite (hosted control plane stand-up) to ATO: **12-18 months minimum** — see `hosted-control-plane-prerequisite.md` § Timeline.
