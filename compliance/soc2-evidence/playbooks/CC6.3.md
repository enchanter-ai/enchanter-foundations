# Playbook — CC6.3 Access provisioning

- **Control ID:** CC6.3
- **Control description:** The entity authorizes, modifies, or removes access to data, software, functions, and other protected information assets based on roles, responsibilities, or the system design and changes.
- **Evidence-collection mechanism:** Daily `log-tail` event recording the per-subagent tool-whitelist contract from `shared/conduct/delegation.md`. Sampled delegation events (when audit-trail captures them) show the whitelist passed to each subagent.
- **Producer (today):** `shared/conduct/delegation.md`; subagent prompts (in conversation logs, not persisted today — gap).
- **Retention rule:** 1 year.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** Subagent observed with broader tool access than its role allows → F08 (tool mis-invocation); revert and tighten the contract.
- **Type II evidence shape:** Delegation-event sampling over the window with per-role whitelist hashes.
- **External dependency:** None.
