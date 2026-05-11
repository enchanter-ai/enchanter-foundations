# Annex A.5 — Assessing impacts of AI systems

**Group:** A.5 — Assessing impacts of AI systems
**Controls:** A.5.2, A.5.3, A.5.4, A.5.5
**Status:** Conformant with image-pipeline gap.

## A.5.2 — AI system impact assessment process

**Objective:** To define and implement a process for AI system impact assessment.

**Control:** The organization shall establish a process to assess the potential consequences for individuals, groups, society from development, deployment, and use of AI systems.

**Implementation:**

Per `clause-by-clause/clause-8-operation.md` §8.4:

- `/harden` 12-attack red-team for misuse + adversarial + bias.
- `crow/decision-gate` human-in-loop for high-stakes runtime actions.
- `hydra/action-guard` dry-run + confirmation for destructive ops.
- `<untrusted_source>` wrapping prevents indirect prompt-injection escalation.
- Inference-engine substrate accumulates cross-session evidence of recurring impact patterns.

**Evidence:**

- `wixie/prompt-harden/`
- `crow/decision-gate/`
- `hydra/action-guard/`

**Conformance:** Full for text-prompt pathway.

**Gap:** Image-prompt 12-attack coverage thinner. R-008.

---

## A.5.3 — Documentation of impact assessments

**Objective:** To record impact assessments.

**Control:** Impact assessments shall be documented and retained.

**Implementation:**

- Per-prompt `audit.json` (12-attack red-team output).
- Per-prompt `metadata.json` (5-axis scores + 8 assertions).
- `learnings.md` records hypothesis + outcome per iteration.
- `wixie/plugins/inference-engine/state/artifacts.jsonl` for cross-session-relevant impact patterns.

**Evidence:**

- `wixie/prompts/*/audit.json`
- `wixie/prompts/*/metadata.json`
- `wixie/prompts/*/learnings.md`

**Conformance:** Full.

---

## A.5.4 — Assessing AI system impact on individuals or groups

**Objective:** To consider impacts on individuals, groups, and society in impact assessments.

**Control:** Impact on individuals or groups of individuals shall be assessed.

**Implementation:**

- Reviewer scoring rubric includes fairness/bias axis when prompt touches user-facing content.
- Cite hygiene `source_type` field prevents single-vendor bias.
- `/harden` includes bias / stereotype attacks.

**Evidence:**

- `wixie/convergence-engine/` rubric
- `shared/conduct/web-fetch.md` § cite hygiene
- `wixie/prompt-harden/` attack categories

**Conformance:** Conformant for explicit-user-facing prompts; ambient impact on non-target groups less systematically assessed.

**Gap:** No standalone bias-eval harness across the full prompt portfolio. R-014.

---

## A.5.5 — Assessing societal impacts of AI systems

**Objective:** To consider societal impacts in impact assessments.

**Control:** Impact on society of AI systems shall be assessed.

**Implementation:**

- AI principles in `aims-policy.md` §3 (fairness, accountability, transparency, safety, privacy, robustness, sustainability) define societal-impact frame.
- Conduct modules operationalize the principles.
- Cross-references to EU AI Act, NIST AI RMF, FedRAMP AI provide societal-impact regulatory framing.
- Self-imposed responsible-disclosure norm: public advisory within 30 days of Critical cross-tenant confirmation.

**Evidence:**

- `aims-policy.md` §3
- `agent-foundations/compliance/` (sibling regulatory maps)
- `aims-policy.md` §10.3 (advisory commitment)

**Conformance:** Conformant at policy level; quantitative societal-impact metrics not produced.

**Gap:** Societal-impact metrics qualitative only. Acceptable for current scale; revisit at scale-up.
