# ISO/IEC 42001 Cert-Body Engagement Plan

What we hand to a BSI / DNV / TÜV / SGS auditor when initiating certification. What they bring back. Realistic timeline + cost.

## The engagement model

ISO 42001 certification is a **two-stage external audit** followed by **annual surveillance** + **triennial recertification**. We engage a UKAS- or ANAB-accredited cert body; they assign a lead auditor. Cert body issues the certificate; we do not.

## What we hand the cert body (this package)

Hand the engagement lead a **single tarball** containing:

```
iso-42001-readiness/
├── aims-policy.md                    # §5.1 — AI Management System policy, signed
├── clause-by-clause/
│   ├── clause-4-context.md           # §4 — context, interested parties, scope
│   ├── clause-5-leadership.md        # §5 — commitment, policy, roles
│   ├── clause-6-planning.md          # §6 — risk + objectives + change
│   ├── clause-7-support.md           # §7 — resources, competence, awareness
│   ├── clause-8-operation.md         # §8 — operational planning, AIIA
│   ├── clause-9-evaluation.md        # §9 — monitoring, internal audit, mgmt review
│   └── clause-10-improvement.md      # §10 — nonconformity, corrective action
├── annex-a-controls/
│   ├── SoA.md                         # Statement of Applicability — every Annex A control marked + justified
│   ├── group-a2-policies.md
│   ├── group-a3-internal-organization.md
│   ├── group-a4-resources.md
│   ├── group-a5-impacts.md
│   ├── group-a6-lifecycle.md
│   ├── group-a7-data.md
│   ├── group-a8-information.md
│   ├── group-a9-use.md
│   └── group-a10-third-party.md
├── risk-register.md                   # §6.1.2 — current + with quarterly review evidence
├── management-review-template.md      # §9.3 — template + filled-in reviews
├── internal-audit-checklist.md        # §9.2 — methodology + executed audit reports
└── cert-body-engagement-plan.md       # this document
```

Plus access to:
- `agent-foundations/compliance/soc2-evidence/` (if SOC 2 in scope alongside)
- Repo read access for source code review
- Personnel calendars for interviews

## Cert-body workflow (typical 6-12 months)

### Phase 1 — Pre-audit application (week 0-2)
1. Operator selects cert body. Recommended:
   - **BSI** — UK-based, broad AI portfolio
   - **DNV** — Norway-based, AI + safety
   - **TÜV SÜD** — Germany-based, technical depth
   - **SGS** — global, lower price point
2. Submit application with scope statement (`clause-4-context.md` §4.3)
3. Cert body assigns lead auditor + quotes price (typically $20k-60k for first cycle including Stage 1 + Stage 2)

### Phase 2 — Stage 1 audit (week 4-8)
- **Off-site review** of documented information
- Lead auditor reads the entire package above
- Verifies the AIMS exists, is operational (not just documented), and is auditable
- **Output**: Stage 1 report listing readiness gaps + recommendation: proceed to Stage 2 OR remediate
- **Common Stage 1 findings**: missing management review evidence, incomplete SoA, AIMS policy not actually used
- **Duration**: 2-5 audit-days

### Phase 3 — Gap remediation (week 8-16)
- Close Stage 1 findings (most are minor, 60-day window typical)
- Run another internal audit cycle if Stage 1 surfaced major NC
- Update + re-sign AIMS policy if scope changed

### Phase 4 — Stage 2 audit (week 16-24)
- **On-site** (or hybrid remote) full system audit
- Lead auditor samples evidence per `internal-audit-checklist.md` § Sampling methodology
- Interviews: AIMS owner, AI custodian, security engineer, sample of developers
- Walkthrough of operational evidence: audit-trail logs, release pipeline, incident response drills
- **Output**: Stage 2 report listing any nonconformities (NC) — major or minor
- **Duration**: 5-10 audit-days

### Phase 5 — Closure + certificate (week 24-30)
- Major NCs → 30-day closure window with evidence
- Minor NCs → 60-day closure window OR closed at first surveillance
- Cert body issues **certificate** (typically valid 3 years)
- Surveillance audits annually (smaller scope, 2-3 days each)
- Full recertification audit every 3 years

## Cost estimates (2026 USD)

| Item | Cost range |
|---|---|
| Stage 1 + Stage 2 (first cycle) | $20,000 - $60,000 |
| Annual surveillance audit | $8,000 - $20,000 |
| Recertification (year 3) | $15,000 - $40,000 |
| Internal preparation (consultant hours, if used) | $10,000 - $30,000 |
| **Year-1 total (cert + preparation)** | **$30,000 - $90,000** |

## What the cert body brings back

- **ISO/IEC 42001 certificate** valid 3 years (subject to surveillance)
- **Stage 1 + Stage 2 audit reports** (we keep these for §9.3 management review inputs)
- **Surveillance findings** annually
- **Logo usage rights** for marketing/procurement (per cert body's brand guide)

## Operator action — start here

1. **Week 0**: read this package end-to-end; identify any gaps not yet documented
2. **Week 1**: schedule first management review per `management-review-template.md` — required input to cert-body application
3. **Week 2**: run first internal audit per `internal-audit-checklist.md` — close any major NCs
4. **Week 3-4**: select cert body + submit application
5. **Week 4-6**: receive Stage 1 quote + lead auditor assignment
6. **Week 8+**: Stage 1 audit

**Realistic timeline from today to certificate**: 6-12 months. Faster if the first internal audit is clean.

## What stays open

- The cert body MAY surface findings this readiness pack didn't anticipate (it's not exhaustive)
- Annex A control evidence depth varies by control — some auditors will probe deeper than `group-a*.md` documents
- New AI regulatory developments (EU AI Act implementing acts, NIST AI RMF updates) may require AIMS policy revision before audit
- Surveillance audits in years 2-3 may surface drift that requires corrective action

These are normal and expected. The package above closes the **inline-achievable** portion. The cert body's audit + their certificate is the genuinely external portion.

## Closure status

ISO/IEC 42001 readiness pack: **shipped**. Cert-body engagement: **operator action required** (~6-12 months wall-clock + ~$30k-90k year-1 spend).
