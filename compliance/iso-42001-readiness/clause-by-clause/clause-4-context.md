# Clause 4 — Context of the organization

**ISO/IEC 42001:2023 §4**
**Status:** Self-attestation, conformant with documented limitations.
**Last reviewed:** 2026-05-05

## §4.1 Understanding the organization and its context

### Requirement

The organization shall determine external and internal issues relevant to its purpose that affect its ability to achieve the intended outcomes of its AIMS.

### Our position

The enchanter-ai project is an open-source agent-substrate effort developing:

- LLM prompt engineering tooling (wixie)
- Runtime guardrails (hydra)
- Skill packaging and discovery (djinn)
- PR automation (sylph)
- Cross-runtime adapters (lich)
- Observability (naga)
- Decision-gating (crow)
- Cost watchdog (pech)
- Shared conduct + compliance (agent-foundations)

### External issues

- Regulatory pressure: EU AI Act phased rollout (2025-2027), EU CRA (2027), US executive orders on AI safety, sector-specific guidance (NIST, FedRAMP).
- Supply-chain risk: typosquatting, malicious dependencies, model deprecations, retired API endpoints.
- Adversarial pressure: prompt-injection corpora growing, MITRE ATLAS taxonomy expansion, public red-team competitions (DARPA AIxCC).
- Vendor velocity: Claude, GPT, Gemini, o-series, Haiku/Sonnet/Opus tier shifts; model IDs retire on weeks-to-months timescales.

### Internal issues

- Small-team scale: management-review formalism scaled down (`aims-policy.md` §1.3).
- Distributed across 9 repositories: cross-repo state coordination is itself a control problem (addressed by inference-engine substrate).
- Open-source default: documentation is public; risk register is public-with-redactions; audit logs are operator-private.

### Evidence

- `agent-foundations/README.md` — project mission.
- Per-repo `README.md` files — local scope statements.
- `wixie/CLAUDE.md` — root-level conduct anchor.
- `aims-policy.md` — formal scope.

### Gap

None at clause level. Lower-clause gaps tracked in `risk-register.md`.

---

## §4.2 Understanding the needs and expectations of interested parties

### Requirement

The organization shall determine interested parties relevant to the AIMS, their relevant requirements, and which of those requirements will be addressed through the AIMS.

### Identified parties

See `aims-policy.md` §2.4 for the canonical list. Summary mapping:

| Party | Requirement | Where addressed |
|---|---|---|
| Developer-users | Predictable agent behavior | conduct modules + SKILL.md frontmatter |
| Downstream agents | Clear contracts | `shared/conduct/delegation.md` |
| Enterprise customers | Vendor risk evidence | this readiness package + sibling compliance maps |
| Certification bodies (future) | Per-clause evidence | this readiness package |
| Regulators | Provenance, accountability | audit-trail + inference-engine |
| Open-source community | Honest framing | self-attestation language throughout |
| Vendors (Claude, GPT, etc.) | Compliance with their TOS | implicit; not separately documented |

### Process for keeping up to date

- Conduct modules are reviewed when a new failure-mode (F15+) is proposed.
- Compliance maps are quarterly self-re-attested.
- Risk register is updated continuously.
- AIMS policy is reviewed annually.

### Evidence

- `aims-policy.md` §2.4
- `risk-register.md`
- `agent-foundations/compliance/` README and sibling maps

### Gap

No formal stakeholder feedback channel beyond GitHub Issues + Security Advisories. Acceptable for current scale; revisit if multi-customer enterprise procurement materializes.

---

## §4.3 Determining the scope of the AIMS

### Requirement

The organization shall determine the boundaries and applicability of the AIMS to establish its scope. The scope shall be available as documented information.

### Scope statement

The AIMS covers:

1. **Authoring lifecycle**: research → craft → refine → converge → test → harden → translate for LLM prompts shipped from wixie.
2. **Runtime governance**: capability checks, egress monitoring, audit trail, action-guard, decision-gate via hydra/crow/naga.
3. **Cross-session learning**: inference-engine substrate.
4. **Conduct modules**: behavioral defaults distributed via `shared/conduct/`.
5. **Compliance evidence production**: this folder and siblings.

The AIMS does **not** cover:

- Models we consume (Claude, OpenAI, Gemini, etc.) — vendor governance.
- Downstream operator agents built atop our skills — downstream AIMS.
- Physical infrastructure — we operate on developer workstations + CI runners.
- Model training / fine-tuning — we orchestrate inference only.

### Boundaries

- Top boundary: AIMS policy `aims-policy.md`.
- Bottom boundary: per-tool invocation in `hydra/audit-trail/state/log.jsonl`.
- Horizontal boundary: nine listed repos; integrations beyond are downstream consumer responsibility.

### Documented information

- `aims-policy.md` §2 — formal scope.
- This file — clause-level affirmation.

### Evidence

- `aims-policy.md`
- `compliance/iso-42001.md` §1.2

### Gap

None at clause level.

---

## §4.4 AI management system

### Requirement

The organization shall establish, implement, maintain, and continually improve an AIMS, including the processes needed and their interactions.

### Our AIMS components

| Component | Implementation |
|---|---|
| Policy | `aims-policy.md` |
| Principles | `aims-policy.md` §3 |
| Risk management | `risk-register.md` + `shared/conduct/failure-modes.md` + inference-engine SPRT |
| Operational lifecycle | wixie prompt-lifecycle skills (`/deep-research` → `/translate-prompt`) |
| Runtime controls | hydra (audit, capability, egress, action-guard), crow (decision-gate), naga (observe) |
| Improvement loop | inference-engine substrate + per-plugin `learnings.md` |
| Performance evaluation | HMAC audit log + SPRT-elevated patterns + DEPLOY-bar self-eval |
| Documented information | `agent-foundations/compliance/` + per-plugin SKILL.md + conduct modules |
| Roles | `aims-policy.md` §5 (Owner, Custodian, Auditor, Coordinator) |

### Process interactions

```
            ┌────────────────────────────┐
            │   AIMS Policy (apex)       │
            └─────────────┬──────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐      ┌─────▼─────┐      ┌────▼────┐
   │ Conduct │      │ Compliance│      │  Risk   │
   │ Modules │      │   Maps    │      │ Register│
   └────┬────┘      └─────┬─────┘      └────┬────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
        ┌─────────────────▼─────────────────┐
        │   Lifecycle skills + runtime      │
        │   guardrails (per-plugin)         │
        └─────────────────┬─────────────────┘
                          │
        ┌─────────────────▼─────────────────┐
        │   Audit trail + Inference engine  │
        │   (durable evidence)              │
        └─────────────────┬─────────────────┘
                          │
        ┌─────────────────▼─────────────────┐
        │   Management review + improvement │
        │   (clause 9, 10)                  │
        └───────────────────────────────────┘
```

### Continual improvement

- Inference-engine substrate: SPRT-elevated patterns become top-of-context briefings at next session.
- Conduct modules versioned via git; new F-codes added through PR review.
- Quarterly self-re-attestation forces refresh of compliance maps.

### Evidence

- This entire readiness package.
- `wixie/plugins/inference-engine/state/briefings/<plugin>.md`
- `agent-foundations/shared/conduct/` (twelve modules).

### Gap

- Management review formalism is documented (template) but not yet exercised at quarterly cadence. Target: first quarterly review by 2026-08-31. Tracked in `risk-register.md` as R-001.
