# Annex A.2 — Policies related to AI

**Group:** A.2 — Policies related to AI
**Controls:** A.2.2, A.2.3
**Status:** Conformant.

## A.2.2 — AI policy

**Objective:** To provide management direction and support for AI in accordance with business requirements and applicable requirements.

**Control:** The organization shall document a policy for the development or use of AI systems.

**Implementation:**

- `agent-foundations/compliance/iso-42001-readiness/aims-policy.md` — apex AIMS policy.
- `agent-foundations/shared/conduct/` — twelve+ behavioral modules constituting operational policy.

**Evidence:**

- `aims-policy.md` §3 (AI principles)
- `aims-policy.md` §5 (roles)
- `shared/conduct/*.md` (operational defaults)

**Conformance:** Full.

**Gap:** None.

---

## A.2.3 — Alignment with other organizational policies

**Objective:** To ensure that the AI policy is aligned with other organizational policies.

**Control:** The organization shall determine where other policies could be affected by or apply to AI use and ensure alignment.

**Implementation:**

- Cross-references from `aims-policy.md` to:
  - NIST AI RMF (`nist-ai-rmf.md`)
  - SOC 2 (`soc2.md`)
  - FedRAMP boundary (`fedramp-boundary.md`)
- Conduct module `shared/conduct/inference-substrate.md` references substrate behavior governed by `wixie/plugins/inference-engine/`.
- `aims-policy.md` §6 establishes precedence rules between AIMS policy, conduct modules, and plugin-local instructions.

**Evidence:**

- `agent-foundations/compliance/` (sibling maps)
- `aims-policy.md` §6 (precedence rules)
- `wixie/CLAUDE.md` (plugin-vs-policy precedence)

**Conformance:** Full.

**Gap:** None.
