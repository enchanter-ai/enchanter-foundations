# Playbook — CC6.1 Logical access security

- **Control ID:** CC6.1
- **Control description:** The entity implements logical access security software, infrastructure, and architectures over protected information assets to protect them from security events.
- **Evidence-collection mechanism:** Daily hash of `hydra/plugins/capability-fence/hooks/PreToolUse.sh` (enforces per-subagent tool whitelist) plus tail of `hydra/plugins/action-guard/state/confirmations.jsonl` (destructive-op confirms).
- **Producer (today):** `hydra/plugins/capability-fence/`, `hydra/plugins/action-guard/`.
- **Retention rule:** 7 years.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** PreToolUse.sh modification without security-closure approval → revert. Destructive-op without confirmation event → F10 runbook (action failure). **GAP:** F-010 escape-hatch CI tests not yet wired.
- **Type II evidence shape:** Continuous PreToolUse hash + auditable confirmation log over the window.
- **External dependency:** None.
