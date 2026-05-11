# Hosted Control Plane — Architectural Prerequisite for FedRAMP

**Document type:** Architectural decision / prerequisite statement
**Date:** 2026-05-05
**Status:** **BLOCKING** — FedRAMP authorization cannot begin until this prerequisite is resolved.
**Audience:** Maintainer, prospective federal customers, 3PAO scoping conversations.

---

## 1. The prerequisite, stated plainly

**FedRAMP authorizes hosted cloud services. enchanter-ai today is a developer-workstation install. The two are architecturally incompatible.**

No amount of SSP detail, control evidence, or 3PAO engagement closes this gap. The gap is an architectural fact: FedRAMP authorization is granted to a **system** that an agency consumes from a **vendor's hosted boundary**. A repo installed on a federal developer's laptop is the federal developer's system, not enchanter-ai's. The maintainer cannot authorize what the maintainer does not operate.

This document defines the **shape** of the hosted control plane that would unlock FedRAMP eligibility, and the **rough timeline** to ATO once that shape is built.

---

## 2. Why the current shape doesn't qualify

| FedRAMP requirement | enchanter-ai today | Gap |
|---|---|---|
| Hosted service operated by an authorized vendor | Developer-workstation plugins | Architectural |
| Single authorization boundary the vendor controls | Each developer's workstation is its own boundary | Architectural |
| Continuous monitoring data flowing to vendor | Telemetry stays local (no OTLP exporter, F-021/F-024) | Architectural + control |
| Vendor-controlled identity, audit, key management | Local OS + per-developer | Architectural |
| Customer-tenant isolation | No tenants — single-developer model | Architectural |
| Vendor SLA for availability + incident response | None — no operated service exists | Organizational |

Six independent reasons, any one of which alone would block. The collective effect is unambiguous: enchanter-ai is not authorizable as currently shipped.

---

## 3. What a hosted control plane would look like

This is the proposed architectural unlock. It is **not** a hosted version of the agent itself — user prompts and code stay on the developer's machine. The control plane is a **thin federation layer** that handles the things FedRAMP wants centralized: identity, audit, vendor-controlled crypto, multi-tenant policy.

### 3.1 Components in scope (hosted)

| Component | Purpose | Sourcing |
|---|---|---|
| **OTLP audit collector** | Receive audit-trail HMAC-chained events from each agency endpoint; verify chain; long-term retention | Per F-021/F-024; OpenTelemetry stack on FedRAMP-authorized CSP |
| **Pager / alerting** | Receive HIGH+ events (capability-fence violations, action-guard skips, secret-scanner hits, canary fires) and page the agency security team | Per F-011 |
| **Policy distribution** | Multi-tenant policy bundles (egress allowlist per agency, capability-fence rules per agency) signed by vendor and pulled by endpoints | New component |
| **Multi-tenant rate-limiter** | Cross-developer aggregate rate-limiting per agency tenant (today: per-workstation only) | Per F-013 |
| **SSO / SCIM endpoint** | SAML/OIDC SP + SCIM provisioning for agency-managed identity | New component |
| **License + entitlement service** | Per-tenant license keys, capability tiers, plugin enablement | New component |
| **Inference-substrate publisher** | Curated cross-agency learning feeds (opt-in, sanitized) | Extension of wixie/inference-engine |

### 3.2 Components that stay local (out of hosted boundary)

| Component | Why it stays local |
|---|---|
| LLM API key + prompts | Customer data sovereignty — prompts contain CUI |
| Source code | Customer-owned, never leaves agency |
| Tool outputs (file content, command output) | Customer data sovereignty |
| audit-trail HMAC chain (writer) | Writer stays local; collector receives copies |
| capability-fence enforcement | Enforcement must be local to be tamper-resistant |
| Plugin source | Open-source; mirrored, not centrally served |

The principle: **federated control, local enforcement**. The control plane sets policy and receives evidence; it does not run the agent or see the data.

### 3.3 Tenant model

- **Tenant = federal agency** (or sub-organization within an agency).
- Each tenant gets: a signed policy bundle, an OTLP collector endpoint, an SSO realm, a rate-limit budget, a license key.
- Cross-tenant data isolation by separate OTLP buckets, separate policy bundles, separate rate-limit pools.
- Vendor staff access to tenant data is governed by AC-6 (least privilege), AC-2 (account mgmt), AU-2 (audited).

### 3.4 Hosting target

| Option | Pros | Cons |
|---|---|---|
| AWS GovCloud | FedRAMP High inheritable; mature | Cost; lock-in |
| Azure Government | FedRAMP High inheritable; mature | Cost; lock-in |
| Multi-CSP via FedRAMP-authorized PaaS | Avoid lock-in | Smaller authorized-component selection |

Recommended starting target: **AWS GovCloud** at FedRAMP Moderate, with the option to elevate to High once the hosted footprint is proven. Inherit IaaS + many PaaS controls from the CSP's existing FedRAMP authorization.

---

## 4. Timeline to ATO — explicit

> **Months stated below are *from the moment hosted control plane stand-up begins*, not from today.**

| Phase | Duration | Output | Cumulative |
|---|---|---|---|
| Phase 0 — Decision + funding | 1-3 months | Funded program; vendor org legal entity; FedRAMP point-of-contact registered | 1-3 |
| Phase 1 — Build hosted control plane MVP | 4-6 months | OTLP collector, pager, SSO, multi-tenant rate-limiter, signed policy distribution all running on GovCloud | 5-9 |
| Phase 2 — Close enchanter-ai control gaps | Parallel to Phase 1 | F-001 (SBOM default-on), F-002 (Sigstore/SLSA L3), F-005 (egress allowlist complete), F-010 (sandbox-escape CI), F-011 (pager wiring), F-013 (multi-tenant rate-limit), F-021/F-024 (OTLP exporter) all closed | merged into 5-9 |
| Phase 3 — SSP authoring + agency sponsor outreach | 2-3 months | Full ~200-page SSP; agency sponsor signed engagement | 7-12 |
| Phase 4 — 3PAO engagement + assessment | 3-6 months | SAP executed; SAR delivered; POA&M drafted | 10-18 |
| Phase 5 — Agency / JAB review + ATO issuance | 2-4 months | Signed ATO | **12-22 months** |
| Phase 6 — Continuous monitoring + annual re-assessment | Indefinite | Monthly ConMon, annual 3PAO | ongoing |

**Realistic minimum from "decision to pursue FedRAMP" to "ATO signed": 12-18 months.** Aggressive case (well-funded, agency sponsor early, no major SAR findings): 12. Realistic case (typical sponsor + 3PAO scheduling): 15-18. Slip case (significant SAR findings, sponsor change, CSP elevation): 22+.

This is consistent with FedRAMP Marketplace median timelines: agency ATO median ~16 months, JAB P-ATO median ~24 months, "in process" listings averaging 12-18 months active assessment.

---

## 5. What can be done **before** the control plane exists

Most of FedRAMP readiness is policy, documentation, and control implementation in code. enchanter-ai can complete a large fraction pre-architectural-unlock:

| Workstream | Doable now? | Notes |
|---|---|---|
| Per-family control implementation (this folder, `control-implementation/`) | Yes | Documents the in-system controls regardless of hosting |
| ConMon plan + IR plan + 3PAO scoping package | Yes | Done in this folder |
| Close shippable control gaps (F-001, F-002, F-005, F-010) | Yes | Independent of hosting |
| HMAC chain hardening, capability-fence regression tests | Yes | In-system code |
| Egress allowlist completeness | Yes | Per-plugin config |
| Pager wiring, OTLP exporter (F-011, F-021, F-024) | **No** — requires hosted endpoint | Built when control plane exists |
| Multi-tenant rate-limiter (F-013) | **No** — requires hosted backend | Built when control plane exists |
| SSO + SCIM | **No** — requires hosted IdP | Built when control plane exists |
| 3PAO engagement | **No** — 3PAO needs hosted system to assess | Phase 4 |
| ATO | **No** | Phase 5 |

**The honest signal:** roughly 60-70% of the readiness work is doable pre-architectural-unlock. The remaining 30-40% is genuinely blocked by the absence of the hosted control plane.

---

## 6. Anti-patterns to avoid

- **Calling this readiness package an SSP.** It is a skeleton. A real SSP is ~200 pages, deployment-specific, and signed.
- **Claiming "FedRAMP-aligned" without disclosing the prerequisite.** The hosted gap is the central fact. Bury it and you mislead the customer.
- **Spending 3PAO budget pre-architectural-unlock.** The 3PAO will produce findings dominated by "no hosted system to assess." Wait until Phase 1 is done.
- **Treating the workstation install as the system.** It isn't. The hosted control plane is.
- **Aspirational timelines.** 6-month ATOs are extreme outliers; 12-18 is realistic.

---

## 7. Decision points for the maintainer

This document does not commit enchanter-ai to a FedRAMP path. It defines what that path would require. Decision points the maintainer faces:

1. **Pursue FedRAMP at all?** Cost: $500K-$2M+ over 12-18 months for a small org. Justified only by a specific agency demand-signal.
2. **Hosted control plane funding?** Without operational hosting, no path forward.
3. **CSP target?** GovCloud Moderate is the lowest-friction start.
4. **Sponsor model — JAB or agency?** Agency sponsor is typically faster; JAB has wider downstream re-use.
5. **3PAO selection?** Material to phase 4 cost and timeline. Choose accredited 3PAO from FedRAMP marketplace.

This document's job: ensure none of these decisions are made under the illusion that today's enchanter-ai is FedRAMP-eligible. It isn't. The unlock is the hosted control plane.

---

## 8. Cross-references

- `ssp-skeleton.md` — SSP authored against this assumed architecture
- `fedramp-boundary.md` — current boundary (workstation reality)
- `control-implementation/` — per-family evidence (mostly portable to hosted form)
- `conmon-plan.md` — ConMon design (some components blocked by this prerequisite)
- `3pao-scoping-package.md` — 3PAO handoff (Phase 4 input)
