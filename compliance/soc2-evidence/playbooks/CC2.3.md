# Playbook — CC2.3 External communication

- **Control ID:** CC2.3
- **Control description:** The entity communicates with external parties regarding matters affecting the functioning of internal control.
- **Evidence-collection mechanism:** Daily hash of every file in `agent-foundations/compliance/` (soc2.md, nist-ai-rmf.md, iso-42001.md, fedramp-boundary.md, this folder) — the customer-facing control documentation.
- **Producer (today):** `agent-foundations/compliance/*.md`, per-repo `README.md`.
- **Retention rule:** 1 year.
- **Who reviews:** Repo maintainer weekly; quarterly external review by procurement-questionnaire respondent.
- **Escalation path:** Compliance doc changes without a PR review log → flag. Customer questionnaire response inconsistent with documented controls → fix the doc first, then the response.
- **Type II evidence shape:** Versioned hash trail showing intentional updates (each tied to a PR).
- **External dependency:** Customer security-questionnaire responses, contracts referencing this folder — drafted by sales/legal, not produced here.
