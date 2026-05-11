# Playbook — CC2.2 Internal communication

- **Control ID:** CC2.2
- **Control description:** The entity internally communicates information necessary to support the functioning of internal control.
- **Evidence-collection mechanism:** Daily SHA-256 hash of every per-plugin briefing in `wixie/plugins/inference-engine/state/briefings/`. Briefings are the cross-session top-of-context surface consumed by every plugin's primary skill at session start.
- **Producer (today):** `wixie/plugins/inference-engine/` (`render-briefing` subcommand).
- **Retention rule:** 1 year.
- **Who reviews:** Repo maintainer weekly; substrate-failure events feed CC4.1.
- **Escalation path:** Briefing absent or empty for a plugin actively in use → reconcile not running. Run `inference-engine.py reconcile` and open issue tagged `compliance-cc2.2`.
- **Type II evidence shape:** 6+ months of briefing-hash rotations tracking SPRT-elevated patterns over time. Stale briefings (no rotation) trigger investigation.
- **External dependency:** None.
