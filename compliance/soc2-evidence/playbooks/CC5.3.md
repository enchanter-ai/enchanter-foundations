# Playbook — CC5.3 Deployment via policies and procedures

- **Control ID:** CC5.3
- **Control description:** The entity deploys control activities through policies that establish what is expected and procedures that put policies into action.
- **Evidence-collection mechanism:** Daily SHA-256 hash of every `*/install.sh` plus relevant `settings.json` files (wires hooks, permissions, env vars per `shared/conduct/hooks.md`).
- **Producer (today):** Each repo's `install.sh`, `.claude/settings.json`.
- **Retention rule:** 1 year.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** install.sh change without corresponding documentation update → flag. settings.json drift from documented baseline → investigate.
- **Type II evidence shape:** Versioned install/settings hashes showing controlled deployment evolution.
- **External dependency:** None.
