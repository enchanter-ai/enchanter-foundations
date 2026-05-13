# FedRAMP Engagement Package — Operator Playbook

**Status:** Pre-engagement architectural prerequisite. Not actionable until hosted control plane MVP is committed.
**Owner:** Vis lead + Compliance lead + Eng VP.
**Horizon:** 18–24 months from architectural commit to ATO.
**Last revised:** 2026-05-05.

> **Read this first.** Enchanter-ai today is a workstation-installed CLI + VS Code surface. FedRAMP authorization applies to **cloud service offerings** (SaaS, PaaS, IaaS) consumed by federal agencies. There is no FedRAMP authorization to chase for a binary the customer runs locally. The unlock is the **hosted control plane** — without it, every dollar spent on 3PAO outreach is wasted. Section 1 is therefore the gate; sections 2–10 are conditional on it.

Cross-references:
- `compliance/fedramp-readiness/hosted-control-plane-prerequisite.md` — architectural memo that established this gate.
- `compliance/fedramp-readiness/conmon-plan.md` — partial ConMon baseline already drafted (extended in §7).
- `compliance/fedramp-readiness/control-coverage-matrix.md` — NIST 800-53 Rev 5 control mapping seed.
- `roadmap-2026/MACRO_ROADMAP.md` — parent roadmap.

---

## 1. Hosted Control Plane MVP Design

The hosted control plane is the **minimum cloud-resident surface** required to make FedRAMP authorization both technically meaningful and commercially valuable. Anything less, the agency cannot buy; anything more, the boundary expands and ATO cost balloons.

### 1.1 Minimum hosted surface (boundary inventory)

Six services. Nothing else inside the authorization boundary at MVP. Every additional service inflates the SAR and the annual ConMon burn.

1. **Audit-trail OTLP relay (per-tenant).** Receives OpenTelemetry traces/metrics/logs from workstation agents over mTLS, fans into per-tenant write-isolated buckets. No mutation; relay-only. This is the load-bearing FedRAMP artifact — every action an agent took is queryable by the tenant's compliance officer.
2. **Pager fan-out.** Receives signed alert events from agents (anomaly, policy violation, model-call cost spike), routes to tenant-configured destinations (PagerDuty, Opsgenie, agency SOC). No payload retention beyond 7 days.
3. **Multi-tenant rate-limiter.** Token-bucket per tenant per upstream model provider. Prevents one tenant from exhausting another's quota. Persists usage counters; no agent payloads.
4. **SSO/SCIM.** SAML 2.0 + OIDC + SCIM 2.0. Agency IdP integrations (Okta, Azure AD GCC High, Ping). User/group provisioning, just-in-time access, MFA delegation. No password storage.
5. **Tenant isolation boundary.** The control-plane-wide enforcement layer: every request authenticates a tenant, every storage write is namespaced, every read is filter-gated. Implemented as middleware + storage-layer policy, not application code (defense in depth).
6. **Signed-config distribution.** Workstation agents pull policy bundles (allowed models, denied tools, prompt-injection filters) signed by tenant admin keys. The control plane stores + serves; signing happens client-side. Zero secrets in transit, zero secrets at rest in the control plane.

What is **not** in the boundary at MVP: LLM inference (stays at customer-chosen provider, BAA/DPA managed separately), agent code (workstation-resident), source code (never leaves customer machine), git operations (local-only).

### 1.2 Architecture sketch (text form)

```
                ┌─────────────────────────────────────────┐
                │     Agency Workstations (out-of-scope)   │
                │  ┌────────┐  ┌────────┐  ┌────────┐     │
                │  │ Agent  │  │ Agent  │  │ Agent  │ ... │
                │  └────┬───┘  └────┬───┘  └────┬───┘     │
                └───────┼───────────┼───────────┼─────────┘
                        │ mTLS      │ mTLS      │ mTLS
                        ▼           ▼           ▼
        ┌───────────────────────────────────────────────────┐
        │       FedRAMP Authorization Boundary               │
        │  ┌────────────────┐  ┌────────────────────────┐   │
        │  │  Edge / WAF /  │  │  IdP Integration       │   │
        │  │  TLS Termination│  │  (SSO, SCIM)           │   │
        │  └────────┬───────┘  └────────────────────────┘   │
        │           │                                        │
        │  ┌────────▼──────────────────────────────────┐    │
        │  │  Tenant Isolation Middleware              │    │
        │  └────┬─────────────┬─────────────┬──────────┘    │
        │       │             │             │                │
        │  ┌────▼─────┐  ┌────▼─────┐  ┌───▼──────────┐     │
        │  │ OTLP     │  │ Pager    │  │ Rate-limiter │     │
        │  │ Relay    │  │ Fan-out  │  │              │     │
        │  └────┬─────┘  └──────────┘  └──────────────┘     │
        │       │                                            │
        │  ┌────▼──────────────────────────────────┐         │
        │  │ Per-tenant Encrypted Object Storage   │         │
        │  │ + Time-series DB (counters/usage)     │         │
        │  └───────────────────────────────────────┘         │
        │                                                    │
        │  ┌──────────────────────────────────────┐          │
        │  │ Config Distribution (signed bundles) │          │
        │  └──────────────────────────────────────┘          │
        └────────────────────────────────────────────────────┘
```

### 1.3 Tech stack proposal (FedRAMP-eligible base)

Build on a **FedRAMP-authorized substrate**. Inheriting an authorized IaaS removes ~250 of NIST 800-53 controls from our scope. Without inheritance, we re-implement physical security, hypervisor controls, DC personnel screening — economically nonviable for a small team.

| Layer | Choice | Rationale |
|---|---|---|
| IaaS | **AWS GovCloud (US)** — FedRAMP High authorized | Inherits ~250 controls; widest agency familiarity; native KMS, IAM, CloudTrail integrations |
| Compute | EKS on GovCloud + Fargate for serverless tiers | Container isolation, no node-level patching burden on us |
| Storage | S3 (per-tenant prefix + bucket policy + KMS-CMK per tenant) | Cryptographic isolation, FedRAMP-blessed |
| Time-series | Timestream or Managed Prometheus (GovCloud) | Counters/rate-limit state; no agent payload data |
| Edge | CloudFront + WAF (GovCloud regional) | DDoS, OWASP Top 10 baseline |
| IdP | Cognito Federation or PingFederate (FedRAMP High) | SAML/OIDC broker; integrates with agency IdPs |
| Secrets | AWS Secrets Manager + KMS-CMK | FIPS 140-2 validated |
| Logging | CloudTrail + CloudWatch Logs → tenant-isolated S3 export | Auditor-required immutable log retention |
| CI/CD | GovCloud-resident CodePipeline + signed artifacts | Build provenance into the boundary |

**Alternatives considered:**
- *Azure Government* — equivalent FedRAMP posture; viable if the sponsor agency is Azure-standardized (DoD-adjacent, some DHS components).
- *GCP Assured Workloads* — narrower agency footprint, fewer reference customers; rejected at MVP, revisit at scale.

### 1.4 Per-tenant data isolation model

Three concentric layers; each independently sufficient to prevent cross-tenant leak, all three required for defense in depth:

1. **Logical (application).** Every API surface is tenant-scoped via a `tenant_id` claim on the SSO JWT; middleware rejects any request whose claim doesn't match the URL path tenant. Unit-tested, fuzz-tested, red-teamed.
2. **Physical/storage (infrastructure).** Each tenant gets a dedicated S3 prefix + dedicated KMS Customer Managed Key. IAM policies deny cross-tenant decrypt at the KMS API level — even a compromised application can't read another tenant's data without KMS authorization.
3. **Network (boundary).** VPC-level isolation per environment (gov-prod, gov-staging); no shared subnets with non-fed workloads.

**Tenant key model:** one KMS-CMK per tenant, rotated annually, deletable on contract termination (BYOK option available for agencies with internal KMS).

### 1.5 Encryption (rest + transit) + KMS

| Surface | Mechanism |
|---|---|
| Transit (agent ↔ control plane) | TLS 1.3 mandatory, mTLS for OTLP and pager fan-out, certificate pinning client-side |
| Transit (control-plane internal) | mTLS via service mesh (App Mesh or Istio), TLS 1.3 only |
| Rest (object storage) | SSE-KMS with per-tenant CMK, FIPS 140-2 Level 2 validated HSMs |
| Rest (databases) | TDE with KMS-CMK, automated backup encryption |
| Rest (logs) | CloudWatch Logs → S3 export with SSE-KMS, immutability via Object Lock (Compliance mode, agency-configurable retention) |
| Secrets | Secrets Manager + KMS-CMK, no plaintext at rest anywhere |
| Key management | AWS KMS in GovCloud (FIPS 140-2 validated); BYOK supported via External Key Store for agencies with internal HSMs |

---

## 2. FedRAMP Path Selection — Baseline

Three baselines (Low / Moderate / High) corresponding to FIPS 199 impact categorization.

| Baseline | Controls | Suited to | Typical SaaS examples |
|---|---|---|---|
| Low | ~125 | Public-facing, no CUI | Marketing sites, public APIs |
| Moderate | ~325 | CUI, non-NSS, most agency adoption | Slack Gov, GitHub Enterprise Cloud Gov, most SaaS |
| High | ~425 | Law enforcement, emergency services, financial | Salesforce Government Cloud Plus, AWS GovCloud itself |

**Recommendation: Moderate baseline.**

Categorization rationale per **NIST SP 800-60 Vol. 2 Rev. 1**:
- *Information types stored:* agent activity logs, usage telemetry, tenant policy bundles, anomaly alerts. No raw source code; no agency mission data; no PII beyond user identifiers.
- *Confidentiality:* Moderate. Agent telemetry, if exposed, could reveal development priorities and tooling configuration — non-trivial but not catastrophic.
- *Integrity:* Moderate. Policy bundle tampering could lead to allowed-tool bypass; tamper-evident signing mitigates but doesn't reduce the categorization.
- *Availability:* Moderate. Control-plane outage degrades agency dev velocity but doesn't halt mission operations (workstation agents continue with cached policy).

Overall categorization: **Moderate (M-M-M)**. High is over-scoped (and roughly 3× more expensive); Low is under-scoped (most agencies reject Low for any system holding agency telemetry).

---

## 3. Authorization Path — JAB P-ATO vs. Agency ATO

Two paths to FedRAMP authorization.

| Path | Authorizer | Reach | Difficulty | Time | Cost |
|---|---|---|---|---|---|
| **JAB P-ATO** | Joint Authorization Board (DOD + DHS + GSA CIOs) | Government-wide reusable | Hardest; ~12 CSPs/year admitted | 18–24mo plus ~6mo queue | +30–50% premium |
| **Agency ATO** | Single sponsoring agency | Reusable but requires per-agency package review | Moderate; gated on sponsor | 12–18mo | Baseline |

**Recommendation: Agency ATO with sponsoring agency identification as a Sales motion.**

Trade-off:
- *JAB P-ATO* gives ecosystem reach (one auth, all agencies inherit) but JAB only admits ~12 CSPs/year via the FedRAMP Connect program; admission itself is competitive and gated on demonstrated demand across multiple agencies. For a pre-revenue government segment, JAB admission is unlikely.
- *Agency ATO* is achievable with one design-partner agency. Other agencies can then reuse the package (a "FedRAMP Authorized" listing in the Marketplace), shortening their internal ATO from 12mo to ~3mo. This is the standard path for small/midcap SaaS.

**Strategy:** pursue Agency ATO with the sponsor identified in §5; once authorized and listed, market the reusable package to subsequent agencies as a 90-day on-ramp.

---

## 4. 3PAO Firm Comparison

Third-Party Assessment Organizations conduct the SAR. They must be FedRAMP-accredited (A2LA) and independent of the CSP.

| Firm | 3PAO-Accredited | AI/Dev-Tools Experience | Initial Assessment | Annual ConMon | Lead Time | Notable References |
|---|---|---|---|---|---|---|
| **A-LIGN** | Y | Strong — GitHub, Snowflake (commercial), several MLOps SaaS | $350–500k | $80–150k | 6–9mo | Largest 3PAO by volume; thorough but slower scheduling |
| **Coalfire** | Y | Strong — many cloud-native SaaS, some AI tooling | $300–450k | $70–130k | 4–8mo | Best-known FedRAMP brand; mature ConMon practice |
| **Schellman** | Y | Moderate — broad SaaS, less dev-tooling specific | $275–425k | $60–120k | 4–7mo | Aggressive pricing; SOC 2 + FedRAMP bundled discount possible |
| **BAI Security** | Y | Moderate — boutique, more agency-side relationships | $200–350k | $50–100k | 3–6mo | Smaller, faster, less brand weight with skeptical sponsors |
| **Kratos** | Y | Light on commercial SaaS; strong defense/intel | $325–475k | $75–140k | 5–8mo | Good for defense-adjacent sponsors (DoD components) |
| **Aprio** | Y | Light — generalist; new entrant to FedRAMP | $225–375k | $55–110k | 3–6mo | Lowest cost; reference base thin; risk on first FedRAMP assessment |

**Shortlist for RFP:** A-LIGN, Coalfire, Schellman. Issue parallel RFPs (see §4.1) with identical statement of work; select on price + earliest available kickoff + reference-call results.

### 4.1 3PAO RFP — Statement of Work outline

1. **System scope.** Hosted control plane MVP per §1, FedRAMP Moderate baseline, AWS GovCloud substrate.
2. **Deliverables.** SAP, SAR, Readiness Assessment Report (RAR) optional pre-engagement, ConMon attestation framework.
3. **Timeline.** Kickoff within 60 days of award; SAP within 30 days of kickoff; SAR within 90 days of testing start.
4. **Pricing structure.** Fixed-fee initial + per-month ConMon retainer; not T&M.
5. **Independence.** No advisory engagement with us in the preceding 24 months (FedRAMP-required separation).
6. **References.** Minimum 3 FedRAMP Moderate SaaS authorizations completed in prior 36 months.
7. **AI workload familiarity.** Question on the firm's experience assessing systems with LLM-augmented agents — pricing variance often signals comfort level.

---

## 5. Sponsoring Agency Identification

Agency ATO requires a federal agency willing to issue the authorization. The agency carries assessment-package liability and gets first-mover access to the tool. This is a **Sales motion**, not a compliance motion — treat it as such.

### 5.1 Target agencies

| Agency | AI Tooling Adoption Posture | Entry Point | Why a fit |
|---|---|---|---|
| **DHS** | Active — DHS AI Task Force; Silicon Valley Innovation Program (SVIP) funds early-stage tools | DHS S&T SVIP solicitations; CISA secure-dev initiatives | Mission alignment with secure software development; existing SaaS authorization pipeline |
| **GSA** | Active — TTS (10x, Centers of Excellence) explicitly funds gov-software-modernization tools | TTS 10x program; GSA's AI Center of Excellence | TTS authorizes its own tools and shares packages with sister agencies; lowest-friction sponsor |
| **DOE** | Moderate — national labs adopt AI dev tools aggressively (ORNL, LLNL); HQ slower | Lab CIO offices; DOE Office of the CIO | Labs run their own ATO boundaries; can sponsor for HQ if lab adoption demonstrates value |
| **DOT** | Light — limited AI dev-tooling adoption to date | Volpe Center; FAA AI initiatives | Lower priority; revisit after first sponsor |

**Recommended primary:** **GSA TTS**. Lowest friction; TTS routinely sponsors small SaaS for internal use, then makes the package available; well-understood ATO workflow.

**Recommended secondary (parallel pursuit):** **DHS SVIP**. Funding + sponsor potential combined; explicitly targets early-stage tools.

### 5.2 Outreach playbook

1. **Week 0–4:** Compile capability brief (2-pager): what Enchanter does, why it matters for federal dev velocity + security, hosted-MVP architecture summary, FedRAMP roadmap commitment.
2. **Week 4–8:** Warm intros via existing federal-adjacent network (Coalition for Sensible Safeguards, federal-contractor advisory firms, ex-USDS network). Cold outreach via SAM.gov + agency innovation-lab public contacts.
3. **Week 8–16:** Discovery calls. Demonstrate workstation agent + describe hosted control plane on the roadmap. Ask: would your office sponsor an Agency ATO if MVP ships by [date]?
4. **Week 16–24:** MOU or LOI with sponsor. Co-define use case + pilot terms. Sponsor agrees to issue ATO conditional on SAR clearance.
5. **Week 24+:** Begin 3PAO engagement (§4) with sponsor named in the SAP.

### 5.3 Sample pitch (capability-brief lead paragraph)

> Enchanter is an vis platform that lets federal development teams use AI coding assistants without source code, prompts, or developer activity ever leaving the workstation. The hosted control plane — currently in design for FedRAMP Moderate authorization on AWS GovCloud — provides agency CIOs the audit trail, tenant isolation, and policy enforcement they require, while keeping the LLM-inference surface at the developer's provider of choice. We are seeking a sponsoring agency for our Agency ATO pursuit and offer pilot access in exchange for sponsorship.

---

## 6. SAP / SAR / POAM Cycle

The three documents that move a FedRAMP package from "in assessment" to "Authorized".

| Doc | Produced by | Purpose | Typical length |
|---|---|---|---|
| **SAP** (Security Assessment Plan) | 3PAO | Scope, methodology, testing schedule, sample sizes for control testing | 50–80 pages |
| **SAR** (Security Assessment Report) | 3PAO | Findings from executing the SAP; per-control pass/fail/risk-accepted | 200–400 pages |
| **POAM** (Plan of Action & Milestones) | CSP (us) | Tracking of every SAR finding to remediation or risk-acceptance | Living spreadsheet/JSON |

**Cadence (mature state):**
- SAP: revisited annually as part of ConMon annual assessment.
- SAR: produced once at initial ATO; full re-test annually under ConMon (a subset re-tested each year on a rotating schedule).
- POAM: updated **monthly** with remediation progress. Submitted to authorizing agency monthly. New findings (from ConMon scans, incident response, etc.) appended within 30 days of discovery.

**Sample POAM entry shape:**

```yaml
poam_id: POAM-2027-014
control: AC-2(7)  # Account Management - Role-Based Schemes
finding: SCIM provisioning does not auto-deprovision on agency IdP user disable within 4 hours
severity: Moderate
discovered: 2027-03-14
discovered_by: 3PAO annual assessment
remediation_plan: Implement SCIM event listener with 1h reconciliation window
milestones:
  - 2027-04-15: Design complete
  - 2027-05-15: Implementation complete
  - 2027-06-01: Re-test by 3PAO
status: in-progress
risk_accepted: false
```

---

## 7. Continuous Monitoring (ConMon)

ConMon makes FedRAMP authorization a continuous obligation, not a point-in-time check. The baseline lives in `compliance/fedramp-readiness/conmon-plan.md`; extensions specific to the hosted control plane:

### 7.1 Hosted-control-plane-specific monitors

| Monitor | Frequency | Source | Alert destination |
|---|---|---|---|
| Per-tenant OTLP relay throughput + error rate | Real-time | CloudWatch metrics on OTLP endpoints | Pager fan-out + monthly POAM |
| Cross-tenant access attempts (denied) | Real-time | Application audit log → SIEM | SOC + immediate POAM entry if > 0 |
| KMS decrypt-denial events | Real-time | CloudTrail | SOC + POAM if > threshold |
| Tenant isolation middleware test suite | Daily CI | Automated red-team fuzzing | Eng + monthly POAM rollup |
| Vulnerability scans (containers + dependencies) | Weekly | ECR scan + Snyk/Trivy | Eng + monthly POAM |
| Penetration test | Annual | Independent firm (not the 3PAO) | Full POAM entry per finding |
| Configuration drift | Daily | AWS Config + custom Conftest policies | Eng + monthly POAM |
| Anomaly detection on usage patterns | Real-time | ML-based outlier detection on rate-limiter counters | Pager fan-out for confirmed anomalies |

### 7.2 Monthly POAM update process

1. Aggregate findings from all monitors above for the prior month.
2. Classify: new / in-progress / resolved / risk-accepted.
3. Compute remediation aging: any High open > 30 days, any Moderate > 90 days, any Low > 180 days requires explicit risk-acceptance signature from CSO + sponsoring agency AO.
4. Submit POAM update by 5th business day of following month to sponsoring agency.

---

## 8. Cost + Time Envelope

Be honest. FedRAMP is expensive and slow. The numbers below are realistic for a small/midcap SaaS; under-budgeting here is the most common cause of mid-engagement abandonment.

| Phase | Duration | Spend Range | Major line items |
|---|---|---|---|
| **Year 0** — Architectural commit + sponsor pursuit | 6–9 months | **$300–500k** | Hosted MVP design + early build (eng), compliance lead hire (FTE or fractional), sponsor outreach travel + capability briefs, FedRAMP advisor retainer (~$15k/mo × 6mo), readiness gap assessment (optional RAR from 3PAO ~$50k) |
| **Year 1** — Hosted build + 3PAO engagement | 12 months | **$400–800k** | 3PAO initial assessment ($300–500k), continued hosted-MVP eng (~$200k incremental), GovCloud infra ($30–80k/yr), penetration test ($50–80k), security tools (SIEM, vuln scanning) ($50–100k/yr) |
| **Year 2** — ATO finalization + ConMon ramp | 12 months | **$200–400k** | 3PAO ConMon retainer ($60–150k/yr), GovCloud infra growth, FedRAMP PMO fees (~$5k/yr), compliance FTE fully loaded, remediation eng for SAR findings |
| **Year 3+** — Steady state | annual | **$250–500k/yr** | Annual ConMon assessment, infra, compliance team, penetration test, remediation eng |

**Realistic time-to-ATO:**
- *Best case:* 18 months from architectural commit, if sponsor is identified by month 6, hosted MVP ships by month 12, 3PAO kickoff at month 12, no major SAR findings.
- *Typical:* **24 months.** SAR finds ≥ 30 items requiring remediation; remediation + retest pushes ATO 6+ months.
- *Slip case:* 30+ months. Sponsor agency turnover, 3PAO schedule slip, significant architectural rework post-SAR.

**Three-year ATO cost envelope:** **$900k–$1.7M** before steady-state ConMon. Most small SaaS underestimate by ~40%.

---

## 9. Pre-3PAO Checklist

3PAO engagement is rational **only when all of the following hold**. Engaging earlier wastes 3PAO fees on a system that isn't assessable yet.

- [ ] Hosted control plane MVP (§1) deployed to GovCloud in a dedicated `gov-prod` account with at least one design-partner tenant onboarded.
- [ ] Sponsoring agency (§5) has issued an LOI or MOU naming us as the system under assessment.
- [ ] FIPS 199 categorization document signed by CSO and sponsor AO designee (Moderate per §2).
- [ ] System Security Plan (SSP) drafted to 80%+ — every control in the NIST 800-53 Rev 5 Moderate baseline addressed, even if "planned" rather than "implemented" for some.
- [ ] Compliance lead in place (FTE or fractional with ≥ 5 prior FedRAMP authorizations).
- [ ] FedRAMP advisor retainer in place (independent of the chosen 3PAO).
- [ ] Year-1 budget approved by board / executive sponsor; not contingent on funding round.
- [ ] Penetration test completed by an independent firm in the prior 6 months; findings remediated or risk-accepted.
- [ ] ConMon tooling (SIEM, vuln scan, config drift) operational and producing signal for ≥ 90 days.
- [ ] All inheritable controls from AWS GovCloud documented in the SSP with the CSP-customer responsibility matrix.
- [ ] Tabletop incident-response exercise completed; IR runbook reviewed by sponsor.

If any item is "in progress" rather than "complete," delay 3PAO kickoff. The cost of a 60-day delay is ~$25k; the cost of failing initial SAR is ~$150–300k in remediation + retest.

---

## 10. Decision Matrix — Pursue FedRAMP Only If

FedRAMP is a strategic commitment, not an opportunistic one. Pursue **only if all four** are true. Any "no" → defer; revisit in 6 months.

| Gate | Required state | Source of truth |
|---|---|---|
| **(a) Government design partner** | ≥ 1 federal agency has expressed concrete intent to use Enchanter in a hosted-control-plane configuration, ideally with LOI | Sponsor outreach log per §5 |
| **(b) Hosted MVP roadmap commitment** | §1 hosted control plane on the engineering roadmap with quarterly milestones and named tech lead | `roadmap-2026/MACRO_ROADMAP.md` |
| **(c) Year-1 budget approval** | ≥ $400k allocated in year-1 budget specifically for hosted build + 3PAO; not fungible with other lines | CFO sign-off in budget doc |
| **(d) C-suite mandate** | CEO + CTO + CSO have all signed off on the 24-month commitment in writing | Board memo or signed strategy doc |

**If 4/4 → green-light, execute §1 → §5 → §4 → §6 in order.**
**If 3/4 → fix the gap before any 3PAO spend. Sponsor outreach (§5) and architectural work (§1) are no-regret; 3PAO RFP (§4) is regret-heavy if any gate is unmet.**
**If ≤ 2/4 → defer. Park this package; revisit quarterly.**

---

## Appendix A — Glossary

- **ATO** — Authority to Operate. The authorization a federal agency issues a system before agency users may operate it.
- **AO** — Authorizing Official. The agency executive who signs the ATO.
- **CSP** — Cloud Service Provider. Us, in this context.
- **ConMon** — Continuous Monitoring. The ongoing security posture maintenance required post-ATO.
- **CUI** — Controlled Unclassified Information. Information requiring safeguarding under federal law but not classified.
- **JAB** — Joint Authorization Board. DOD + DHS + GSA CIOs; issues P-ATOs reusable across agencies.
- **P-ATO** — Provisional ATO. JAB-issued; agencies still issue their own ATO citing the P-ATO but with lower friction.
- **POAM** — Plan of Action & Milestones. Tracking of remediation work for SAR findings.
- **3PAO** — Third-Party Assessment Organization. A2LA-accredited firm that performs the SAR.
- **SAP** — Security Assessment Plan. 3PAO's testing plan.
- **SAR** — Security Assessment Report. 3PAO's findings.
- **SSP** — System Security Plan. CSP-authored description of the system + how each control is met.
- **SVIP** — Silicon Valley Innovation Program. DHS S&T's startup engagement vehicle.
- **TTS** — Technology Transformation Services. GSA's modern-dev arm; runs 10x and the COEs.

## Appendix B — Document Inheritance

This package depends on, and extends, these compliance artifacts:

- `compliance/fedramp-readiness/hosted-control-plane-prerequisite.md` — establishes the §1 gate.
- `compliance/fedramp-readiness/conmon-plan.md` — extended by §7.
- `compliance/fedramp-readiness/control-coverage-matrix.md` — NIST 800-53 Rev 5 mapping seed; expanded into the SSP.
- `roadmap-2026/MACRO_ROADMAP.md` — must reflect the hosted-MVP commitment for §10(b) to evaluate true.

## Appendix C — Honest Disclosures

1. **This is hard.** Most pre-revenue SaaS that start FedRAMP pursuit do not finish. The dropout point is usually month 14–18, mid-3PAO, when the SAR comes back with 60+ findings and the cap table revisits whether the federal segment is worth the burn.
2. **The sponsor is the unlock.** No sponsor → no agency ATO → no marketplace listing → no other agency reuses → zero ROI on the spend. §5 outranks §4 in sequencing risk.
3. **The hosted MVP is the bigger unlock.** Without it there is no system to assess. §1 outranks §5 in technical risk.
4. **Estimates assume favorable execution.** A real engagement adds 20–40% to numbers above for unforeseen remediation. Plan accordingly.
