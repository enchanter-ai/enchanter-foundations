# Playbook — CC2.1 Quality information for internal control

- **Control ID:** CC2.1
- **Control description:** The entity obtains or generates and uses relevant, quality information to support the functioning of internal control.
- **Evidence-collection mechanism:** Daily `metric` event recording count of `wixie/prompts/*/metadata.json` files (per-prompt provenance: model, tokens, cost, 5-axis scores, 8 SAT assertions, version) and sampled paths.
- **Producer (today):** `wixie/prompts/<name>/metadata.json`, `learnings.md`, `state/precedent-log.md`.
- **Retention rule:** 1 year.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** If prompt count drops without corresponding decommission entries, or metadata.json schema drifts, surface to dashboard.
- **Type II evidence shape:** Growing prompt-count series with stable metadata schema across the window; sampled `metadata.json` files demonstrate honest scoring (no fabrication per CLAUDE.md § Honest numbers).
- **External dependency:** None.
