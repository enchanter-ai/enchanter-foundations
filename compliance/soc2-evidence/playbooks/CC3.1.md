# Playbook — CC3.1 Suitable objectives

- **Control ID:** CC3.1
- **Control description:** The entity specifies objectives with sufficient clarity to enable the identification and assessment of risks relating to objectives.
- **Evidence-collection mechanism:** Daily `metric` event recording the DEPLOY bar (σ<0.45, overall≥9.0, all axes≥7.0, 8/8 SAT assertions) as canonical from `wixie/CLAUDE.md` § DEPLOY bar. Future enhancement: tail of convergence-engine verdicts.
- **Producer (today):** `wixie/CLAUDE.md`; future: `wixie/plugins/convergence-engine/state/verdicts.jsonl`.
- **Retention rule:** 1 year.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** DEPLOY bar changes without security-closure approval → flag and block. Inflated scores in metadata.json (CLAUDE.md § Honest numbers violation) → open F11 (reward hacking) entry.
- **Type II evidence shape:** Stable DEPLOY-bar constants with traceable verdict distribution across the window.
- **External dependency:** None.
