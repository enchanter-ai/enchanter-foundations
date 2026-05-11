# Playbook — CC4.2 Communicates control deficiencies

- **Control ID:** CC4.2
- **Control description:** The entity evaluates and communicates internal control deficiencies in a timely manner to those parties responsible for taking corrective action.
- **Evidence-collection mechanism:** Daily `metric` event aggregating F01..F14 code counts across every `wixie/prompts/*/learnings.md` and `state/precedent-log.md`.
- **Producer (today):** F-tagged entries across all plugins.
- **Retention rule:** 1 year.
- **Who reviews:** Repo maintainer weekly; spike investigation immediate.
- **Escalation path:** Any F-code with ≥3 occurrences in one week → surface to security-closure synthesis queue. F08/F09/F10 (action failures) → pause the affected plugin per failure-modes.md.
- **Type II evidence shape:** Continuous F-code time series showing detection-then-remediation lifecycle; counter rules trigger documented per runbook.
- **External dependency:** None.
