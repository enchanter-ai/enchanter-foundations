# Playbook — CC7.3 Security event evaluation

- **Control ID:** CC7.3
- **Control description:** The entity evaluates security events to determine whether they could or have resulted in a failure of the entity to meet its objectives (security incidents) and, if so, takes actions to prevent or address such failures.
- **Evidence-collection mechanism:** Daily `log-tail` event referencing F-code triage entries per `shared/conduct/failure-modes.md` and the F01-F21 runbooks under `agent-foundations/runbooks/`.
- **Producer (today):** F-tagged entries across all plugins; runbooks library.
- **Retention rule:** 1 year.
- **Who reviews:** Repo maintainer weekly; incident triage immediate.
- **Escalation path:** F08/F09/F10 (action failures) clusters → pause the affected plugin and run the matching runbook.
- **Type II evidence shape:** Continuous F-code triage log with linked runbook executions across the window.
- **External dependency:** None.
