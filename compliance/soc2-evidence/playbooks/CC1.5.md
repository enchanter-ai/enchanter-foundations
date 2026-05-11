# Playbook — CC1.5 Accountability

- **Control ID:** CC1.5
- **Control description:** The entity holds individuals accountable for their internal control responsibilities in the pursuit of objectives.
- **Evidence-collection mechanism:** Daily `log-tail` event over each repo's `state/precedent-log.md` (self-observed operational failures) plus every plugin's `learnings.md` (F-code-tagged hypothesis/outcome rows). The `override-must-be-logged` contract from root CLAUDE.md is enforced by these logs.
- **Producer (today):** `*/state/precedent-log.md`, `*/prompts/*/learnings.md`.
- **Retention rule:** 1 year.
- **Who reviews:** Repo maintainer weekly; F-code aggregates feed CC4.2.
- **Escalation path:** Three F04 (task drift) in one week → surface to security-closure synthesis. Pattern of unlogged overrides → operator review and conduct module update.
- **Type II evidence shape:** Continuous append-only logs over the 6-month window with traceable F-code accountability entries.
- **External dependency:** None.
