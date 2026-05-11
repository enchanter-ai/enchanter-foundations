# Playbook — CC1.3 Management structures and reporting lines

- **Control ID:** CC1.3
- **Control description:** Management establishes, with board oversight, structures, reporting lines, and appropriate authorities and responsibilities.
- **Evidence-collection mechanism:** Daily SHA-256 hash of every `*/CLAUDE.md` (defines tier model: Opus/Sonnet/Haiku) and every `*/plugins/*/.claude-plugin/plugin.json` (defines per-plugin owner).
- **Producer (today):** `wixie/CLAUDE.md`, `hydra/CLAUDE.md`, every plugin `plugin.json` across the ecosystem.
- **Retention rule:** 7 years.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** A CLAUDE.md change that removes the tier model or a plugin.json missing `owner` field → flag in dashboard, open issue tagged `compliance-cc1.3`.
- **Type II evidence shape:** Stable hash trail across 6+ months showing intentional structural changes (each tied to a PR with reviewer sign-off).
- **External dependency:** None.
