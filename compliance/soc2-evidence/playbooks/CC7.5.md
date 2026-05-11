# Playbook — CC7.5 Incident recovery

- **Control ID:** CC7.5
- **Control description:** The entity identifies, develops, and implements activities to recover from identified security incidents.
- **Evidence-collection mechanism:** Daily `log-tail` event recording the convergence-engine revert-on-regression contract status; precedent-log dead-end entries.
- **Producer (today):** `wixie/plugins/convergence-engine/`, `*/state/precedent-log.md`.
- **Retention rule:** 1 year.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** Recovery failure (revert didn't restore baseline) → freeze, investigate, surface to security-closure.
- **Type II evidence shape:** Continuous revert-event log + precedent-log dead-end entries across the window.
- **External dependency:** None.
