# Internal Audit Checklist — ISO/IEC 42001 §9.2

Per ISO/IEC 42001 clause §9.2 (Internal audit). The AIMS shall undergo internal audits at planned intervals to determine whether the management system conforms to the organization's own requirements and the standard, and whether it is effectively implemented + maintained.

## Cadence

- **Pre-cert-body** internal audit: ≥ 60 days before first Stage 2 audit (allows time to close findings)
- **Annual** thereafter for the full AIMS scope
- **Targeted** audits triggered by: incident, residual-risk escalation to High, regulatory change

## Auditor independence (§9.2.1.c)

- Internal auditors MUST NOT audit their own work
- The AIMS owner cannot be the sole auditor of their own management system
- For ISO 42001 cert: appoint an external independent auditor OR rotate internal auditors so no person audits their direct deliverables

## Audit scope per clause (§9.2.2.a)

Each internal audit cycle covers all clauses 4-10 unless a documented exception applies.

### Clause 4 — Context of the organization
- [ ] §4.1: External + internal issues documented and current?
- [ ] §4.2: Interested parties + their requirements identified?
- [ ] §4.3: AIMS scope statement exists, signed, current?
- [ ] §4.4: AIMS processes documented per `clause-4-context.md`?

### Clause 5 — Leadership
- [ ] §5.1: Top management commitment evidence (signed AIMS policy, resource allocation records)?
- [ ] §5.2: AI policy (`aims-policy.md`) communicated, current, signed?
- [ ] §5.3: Roles assigned, RACI matrix maintained?

### Clause 6 — Planning
- [ ] §6.1.1: Risk register current per `risk-register.md`?
- [ ] §6.1.2: AI risks assessed + treated per the table?
- [ ] §6.1.3: AI impact assessment (AIIA) records exist for each high-risk AI system?
- [ ] §6.2: AI objectives documented + measurable?
- [ ] §6.3: Changes to AIMS planned + controlled?

### Clause 7 — Support
- [ ] §7.1: Resources adequate (people, tools, budget)?
- [ ] §7.2: Competence requirements defined + met?
- [ ] §7.3: Awareness training delivered, attendance logged?
- [ ] §7.4: Internal + external communications documented?
- [ ] §7.5: Documented information controlled, versioned, accessible?

### Clause 8 — Operation
- [ ] §8.1: Operational planning evidence (release.yml, CI workflows, plugin lifecycle docs)?
- [ ] §8.2: AI risk treatment plan executed + tracked?
- [ ] §8.3: AI system impact assessments performed?
- [ ] §8.4: Data quality + governance (data lineage, retention, deletion)?
- [ ] §8.5: AI lifecycle managed (design, dev, deploy, monitor, decommission)?

### Clause 9 — Performance evaluation
- [ ] §9.1: Monitoring + measurement results recorded?
- [ ] §9.2: Internal audit program executed?
- [ ] §9.3: Management reviews held + minuted per `management-review-template.md`?

### Clause 10 — Improvement
- [ ] §10.1: Nonconformities logged + tracked?
- [ ] §10.2: Corrective actions implemented + verified effective?

## Annex A reference controls (38 controls across 9 groups)

For each Annex A control group (A.2 through A.10), verify:
- [ ] Statement of Applicability (`annex-a-controls/SoA.md`) marks each control as applicable / N/A with justification
- [ ] Each applicable control has evidence-of-implementation cited
- [ ] Each N/A control has documented justification (not just "we don't do that")

Reference: `annex-a-controls/group-a2-*.md` through `group-a10-*.md`.

## Sampling methodology

For evidence-heavy controls (audit logs, signed releases, evidence collection runs):
- **Daily-emitted evidence**: sample 30 random days from prior 12 months
- **Per-release evidence**: sample 5 random releases from prior 12 months OR all if < 5
- **Per-event evidence** (incidents, audit findings): sample 100% (these are rare)

## Audit report shape (§9.2.2.f)

The internal audit report includes:

```
1. Auditor(s) + independence statement
2. Audit scope + dates
3. Sampling methodology
4. Findings per clause (categorized: conformance / minor NC / major NC / observation)
5. Root cause analysis for any NC
6. Corrective action plan per NC (owner, due date, evidence-of-closure criteria)
7. AIMS owner sign-off
8. Distribution: AIMS owner, top management, cert body (when in scope)
```

Reports archived to: `compliance/iso-42001-readiness/internal-audits/YYYY-MM-DD.md`

## Severity definitions

- **Conformance**: clause requirements met
- **Observation (OBS)**: minor concern, no requirement violated; document + monitor
- **Minor nonconformity (MIN-NC)**: requirement met in part; localized; correctable within 60 days
- **Major nonconformity (MAJ-NC)**: requirement not met OR systemic failure; blocks cert; correctable within 30 days OR cycle restart

## Pre-cert audit (first run)

The first internal audit MUST cover the full scope above. Expect to surface several minor NCs and 1-2 major NCs in the first cycle — this is normal and expected. The cert body's Stage 1 audit reviews the internal audit's outputs; arriving with zero findings raises suspicion.

**Common Stage-1 findings (avoid these):**
- Missing management review minutes
- Risk register without quarterly review evidence
- Annex A SoA without justifications for N/A controls
- AIMS policy not signed by top management
- Internal audit by the AIMS owner (independence failure)

## Operator handoff

Per AIMS policy, the operator owns:
1. Scheduling the first internal audit (60 days pre Stage 2)
2. Appointing independent auditor(s)
3. Reviewing this checklist + customizing for repo-specific scope
4. Archiving each audit's outputs
5. Tracking corrective actions to closure before next cycle

## Closure status

This checklist is the **template + methodology**. The actual audit execution (sampling, evidence pulling, interviews, report writing) is the auditor's work, not the document's. **Time to first internal audit**: ~2 weeks of focused work by an independent auditor with this checklist + the compliance evidence pack as inputs.
