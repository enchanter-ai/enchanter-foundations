# Playbook — CC3.2 Risk identification and analysis

- **Control ID:** CC3.2
- **Control description:** The entity identifies risks to the achievement of its objectives across the entity and analyzes risks as a basis for determining how the risks should be managed.
- **Evidence-collection mechanism:** Daily SHA-256 hash of `wixie/prompts/security-closure/results/synthesis.md` (F-001..F-030 closure audit) plus inference-engine elevated patterns (SPRT verdict ≥2.89 LLR).
- **Producer (today):** `wixie/prompts/security-closure/results/synthesis.md`, `wixie/plugins/inference-engine/state/catalog.json`.
- **Retention rule:** 7 years.
- **Who reviews:** Repo maintainer weekly; security-closure owner quarterly.
- **Escalation path:** Synthesis hash unchanged for >30 days while new F-codes accumulate → re-run security-closure audit.
- **Type II evidence shape:** Versioned synthesis snapshots showing risk-register evolution; SPRT walks demonstrating risk-analysis rigor.
- **External dependency:** None.
