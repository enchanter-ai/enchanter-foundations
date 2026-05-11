# Playbook — CC3.4 Change-related risk

- **Control ID:** CC3.4
- **Control description:** The entity identifies and assesses changes that could significantly impact the system of internal control.
- **Evidence-collection mechanism:** Daily `log-tail` event recording the convergence-engine no-regression contract status; baseline-snapshot pairs from `verification.md`-driven workflows.
- **Producer (today):** `wixie/plugins/convergence-engine/`, every plugin's baseline-snapshot artifacts.
- **Retention rule:** 1 year.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** F12 (degeneration loop) recurrence → freeze convergence on the affected prompt, open issue tagged `compliance-cc3.4`.
- **Type II evidence shape:** Continuous evidence of revert-on-regression triggers across the window, demonstrating the change-control feedback loop functions.
- **External dependency:** None.
