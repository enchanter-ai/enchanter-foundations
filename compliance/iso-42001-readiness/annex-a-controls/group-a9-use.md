# Annex A.9 — Use of AI systems

**Group:** A.9 — Use of AI systems
**Controls:** A.9.2, A.9.3, A.9.4
**Status:** Conformant.

## A.9.2 — Processes for responsible use of AI systems

**Control:** Processes shall be in place for responsible use of AI systems.

**Implementation:**

- `crow/decision-gate` human-in-loop on high-stakes flagged events.
- `hydra/action-guard` dry-run + confirmation for destructive ops.
- Conduct module `shared/conduct/verification.md` § Dry-run for destructive ops mandates plan + explicit user yes before any irreversible operation.
- Conduct module `shared/conduct/delegation.md` § Tool whitelisting per subagent limits scope.

**Evidence:**

- `crow/decision-gate/`
- `hydra/action-guard/`
- `shared/conduct/verification.md`

**Conformance:** Full.

**Gap:** Runtime capability sandbox per subagent (F-010) is roadmap. Subagent escape currently would be RCE primitive. R-003.

---

## A.9.3 — Objectives for responsible use of AI systems

**Control:** Objectives for responsible use shall be defined.

**Implementation:**

- AI principles in `aims-policy.md` §3 articulate the responsible-use frame.
- Conduct modules state behavioral defaults that operationalize the principles.
- DEPLOY bar enforces honest-numbers contract; 7/8 SAT → HOLD verdict (no inflation).

**Evidence:**

- `aims-policy.md` §3
- `shared/conduct/*.md` (all twelve+ modules)
- `wixie/CLAUDE.md` § DEPLOY bar § Behavioral contracts

**Conformance:** Full.

---

## A.9.4 — Intended use of the AI system

**Control:** The intended use of the AI system shall be documented.

**Implementation:**

- Per-skill SKILL.md `description` field includes "Use when..." clause and optional "Do not use for..." clause (per `shared/conduct/skill-authoring.md`).
- Per-plugin README + `plugin.json` describe intended-use scope.
- AIMS scope statement (`aims-policy.md` §2) defines overall intended use.

**Evidence:**

- Per-plugin SKILL.md frontmatter
- `shared/conduct/skill-authoring.md` § Description: both what and when
- `aims-policy.md` §2

**Conformance:** Full.
