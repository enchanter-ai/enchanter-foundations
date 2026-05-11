# 3PAO Scoping Package — enchanter-ai

**Document type:** Scoping handoff for a Third-Party Assessment Organization (3PAO)
**Date:** 2026-05-05
**Purpose:** Give a prospective 3PAO firm enough material to scope an engagement, quote effort, and execute kickoff without re-discovery work.
**Status:** Pre-authorization. **A 3PAO assessment cannot conclude until the hosted control plane is stood up.** This package is suitable for scoping conversations and Phase-1-readiness review only.

---

## 1. Why this matters now

A 3PAO firm (FedRAMP-accredited per A2LA) produces two artifacts during assessment:

| Artifact | Purpose | enchanter-ai status |
|---|---|---|
| **SAP** — Security Assessment Plan | Test plan: what's tested, by whom, when, with what tooling | Not authored — depends on engagement |
| **SAR** — Security Assessment Report | Findings + risk ratings + recommendations | Not produced — Phase 4 deliverable |

**This package is the input to SAP authoring.** Give it to the 3PAO; they produce the SAP; you negotiate scope; engagement begins.

> **Critical disclosure for 3PAO scoping conversations:** enchanter-ai is **pre-hosted**. The current deployment is developer-workstation. A full FedRAMP assessment requires a hosted system. Scope conversations should be framed as either (a) **gap analysis** — what would the assessment look like once hosted, or (b) **readiness review** — non-binding evaluation of pre-Phase-1 control implementations. See `hosted-control-plane-prerequisite.md`.

---

## 2. What the 3PAO needs (handoff bundle)

### 2.1 Documentation (this package)

| Artifact | Path |
|---|---|
| FedRAMP boundary | `../fedramp-boundary.md` |
| SSP skeleton | `./ssp-skeleton.md` |
| Hosted control plane prerequisite | `./hosted-control-plane-prerequisite.md` |
| Continuous monitoring plan | `./conmon-plan.md` |
| Incident response plan | `./incident-response-plan.md` |
| Per-family control evidence | `./control-implementation/*.md` (AC, AU, CM, IA, IR, RA, SC, SI, SR) |
| Architecture diagram (Mermaid) | `../../docs/architecture/highlevel.mmd` |
| Security closure synthesis (F-001..F-024) | `../../../wixie/prompts/security-closure/results/synthesis.md` |
| Per-failure-code runbooks | `../../runbooks/F*.md` |
| Conduct modules (behavioral controls) | `../../shared/conduct/*.md` |
| Failure-mode taxonomy | `../../shared/conduct/failure-modes.md` |

### 2.2 Repo access

Read access required for assessment:

| Repo | Path | Notes |
|---|---|---|
| agent-foundations | this repo | Conduct + runbooks + compliance |
| hydra | `<repo-root>/hydra` | 15 defensive-control plugins |
| wixie | `<repo-root>/wixie` | Prompt lifecycle + inference engine |
| pech | `<repo-root>/pech` | Cost + budget controls |
| sylph | `<repo-root>/sylph` | PR + CI lifecycle |
| lich | `<repo-root>/lich` | Code review subagent |
| crow | `<repo-root>/crow` | Decision oversight |
| emu | `<repo-root>/emu` | Context + state |
| gorgon | `<repo-root>/gorgon` | Code analysis |
| naga | `<repo-root>/naga` | Cross-repo + observability |
| djinn | `<repo-root>/djinn` | Drift + intent |

Access mode: GitHub read-only collaborator or org-level read team. Avoid granting write — 3PAO should not modify the system under assessment.

### 2.3 Boundary diagram

Source-of-truth: `agent-foundations/docs/architecture/highlevel.mmd`.

Text rendering for 3PAO non-Mermaid consumers: see `ssp-skeleton.md` § 3.

### 2.4 Test schedule template

The 3PAO will propose this; we supply availability windows. Template for operator response:

```
Available windows for SAP execution:
- Pre-Phase-1 (gap analysis): <dates>
- Phase 1+ (hosted exists): <dates>

Forbidden windows:
- <release cuts>
- <agency demo windows>

Test environment:
- Pre-Phase-1: snapshot of repos + local workstation install demo
- Phase 1+: dedicated test tenant on hosted control plane

Key personnel availability:
- Maintainer: <hours>
- Security Officer (TBD post-hosted): <hours>
- Operator (TBD post-hosted): <hours>
```

### 2.5 Key personnel contacts (template — operator fills)

```
Role                              Name        Email        Phone
--------------------------------- ----------- ------------ ----------
Engagement primary               TBD         TBD          TBD
Technical primary (maintainer)   TBD         TBD          TBD
Security Officer                 TBD         TBD          TBD
Authorizing Official sponsor     TBD         TBD          TBD
Communications Lead              TBD         TBD          TBD
Hosting CSP TAM (when SaaS)      TBD         TBD          TBD
```

---

## 3. Assessment scope shape

### 3.1 Pre-Phase-1 (readiness review — recommended starting point)

Non-binding 3PAO engagement focused on:

1. **Gap analysis** — does the existing control evidence (this folder) constitute the right shape for a future FedRAMP assessment?
2. **Architecture review** — does the proposed hosted control plane address the prerequisite gaps?
3. **Readiness scoring** — what fraction of NIST 800-53r5 Moderate is plausibly satisfied at Phase-1 cutover?
4. **Roadmap critique** — does the 12-18-month timeline match 3PAO experience with similar shape?

Output: **3PAO Readiness Memo** (not a SAR; not binding). Typical engagement: 4-8 weeks.

### 3.2 Phase 1+ (full SAR engagement)

After hosted control plane is operational:

1. **SAP authoring** — based on this package + hosted environment walkthrough.
2. **Inspection** — read docs, configs, audit logs.
3. **Examination** — verify control implementations via interview + log review.
4. **Testing** — active testing of in-scope controls (capability-fence, egress-shield, secret-scanner, action-guard).
5. **Penetration test** — required by FedRAMP; targets the hosted control plane + plugin interaction.
6. **SAR delivery** — findings + risk ratings + POA&M recommendations.

Typical engagement: 12-24 weeks. Cost (industry typical for Moderate): $200K-$500K depending on scope.

---

## 4. Boundary clarifications the 3PAO will ask

Pre-answering common 3PAO scoping questions:

| Question | Answer |
|---|---|
| Is this a SaaS, PaaS, or IaaS? | Proposed SaaS — agent-substrate-as-a-service. Today: developer-workstation install (out of FedRAMP scope until hosted). |
| What's the hosting CSP? | TBD — AWS GovCloud Moderate is the proposed starting target. |
| What's the FIPS 199 categorization? | **Moderate** proposed (Confidentiality=Mod, Integrity=Mod, Availability=Low). See `ssp-skeleton.md` § 4.2. |
| Where does customer data live? | **At customer-side**, not in the hosted boundary. Hosted control plane handles policy + audit + identity, not user data. See `hosted-control-plane-prerequisite.md` § 3.2. |
| Are there any external systems? | Yes — Anthropic API, GitHub, npm, PyPI, OTLP collector (planned). All inventoried in `ssp-skeleton.md` § 7. |
| Is the LLM in-boundary? | **No.** Anthropic Claude API is OOB. The integration is one of the inventoried external connections. |
| Multi-tenant? | Proposed yes; not today (single-developer install). F-013 gap. |
| FIPS 140-3 modules? | TBD per CSP hosting choice. |
| Federal use today? | None — pre-authorization, no federal customer. |

---

## 5. Phase-by-phase 3PAO involvement

Per `hosted-control-plane-prerequisite.md` § 4:

| Phase | Timing | 3PAO involvement |
|---|---|---|
| 0 — Decision + funding | Months 0-3 | None (gap analysis could begin) |
| 1 — Build hosted control plane MVP | Months 4-9 | Optional readiness review |
| 2 — Close control gaps | Parallel | Optional control-spot-checks |
| 3 — Full SSP authoring | Months 7-12 | SSP review (advisory) |
| 4 — **3PAO engagement + assessment** | Months 10-18 | **Primary engagement: SAP + SAR** |
| 5 — Agency / JAB review + ATO | Months 12-22 | Support agency questions |
| 6 — Annual reassessment | Ongoing | Annual SAR refresh |

---

## 6. Suggested 3PAO selection criteria

Per FedRAMP Marketplace:

- **A2LA accreditation** in scope of FedRAMP.
- **Experience with similar systems** — small SaaS, developer-tool category, AI/LLM-touching systems (relatively new category, fewer firms qualified).
- **Track record at proposed categorization** (Moderate).
- **Cost transparency** in the proposal.
- **Reasonable response on this package's hosted-prerequisite caveat** — firms that brush past it are mis-selling.

We do not endorse specific 3PAOs; the FedRAMP Marketplace is the authoritative directory.

---

## 7. Operator handoff checklist

Before engaging a 3PAO, operator confirms:

- [ ] Read `hosted-control-plane-prerequisite.md` — agree the prerequisite is real, not optional.
- [ ] Decide engagement type — readiness review (Pre-Phase-1) or full SAR (Phase 4+).
- [ ] Identify agency sponsor (or JAB path).
- [ ] Confirm hosting CSP target.
- [ ] Fill in key-personnel contacts (§ 2.5).
- [ ] Set test-schedule windows (§ 2.4).
- [ ] Grant read-only repo access (§ 2.2).
- [ ] Share this bundle with 3PAO candidates.
- [ ] Budget approved.

---

## 8. Cross-references

- `ssp-skeleton.md` — SSP shape for SAP authoring
- `hosted-control-plane-prerequisite.md` — read first
- `conmon-plan.md` — post-ATO ConMon obligations
- `incident-response-plan.md` — IR plan for assessment
- `control-implementation/*.md` — control evidence to walk through
- `../fedramp-boundary.md` — boundary
- FedRAMP Marketplace: https://marketplace.fedramp.gov/
- A2LA accreditation directory for 3PAOs: https://customer.a2la.org/
