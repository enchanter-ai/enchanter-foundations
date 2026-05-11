# Playbook — CC6.7 Restricts data movement

- **Control ID:** CC6.7
- **Control description:** The entity restricts the transmission, movement, and removal of information to authorized internal and external users and processes.
- **Evidence-collection mechanism:** Daily hash of `hydra/plugins/egress-shield/config/allowlist.yaml` plus tail of egress-shield block events.
- **Producer (today):** `hydra/plugins/egress-shield/`.
- **Retention rule:** 1 year.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** Allowlist change without security-closure approval → revert. **GAP:** F-005 — current allowlist sparse, needs density expansion before Type II.
- **Type II evidence shape:** Stable allowlist hash with documented change history; continuous block-event log over the window.
- **External dependency:** None.
