# Playbook — CC7.4 Incident response

- **Control ID:** CC7.4
- **Control description:** The entity responds to identified security incidents by executing a defined incident response program to understand, contain, remediate, and communicate security incidents, as appropriate.
- **Evidence-collection mechanism:** Daily tail of `hydra/plugins/action-guard/state/confirmations.jsonl` (destructive-op confirmations recorded). Future: `pager.ts` paging events.
- **Producer (today):** `hydra/plugins/action-guard/`. Future: `pager.ts` (F-011 in progress).
- **Retention rule:** 7 years.
- **Who reviews:** Repo maintainer weekly; incident response immediate.
- **Escalation path:** Destructive op without confirmation → F10 runbook. **GAP:** F-011 pager.ts not yet shipped.
- **Type II evidence shape:** Continuous confirmation log + post-pager incident timeline across the window.
- **External dependency:** Paging service (PagerDuty / Opsgenie / etc.) once pager.ts ships.
