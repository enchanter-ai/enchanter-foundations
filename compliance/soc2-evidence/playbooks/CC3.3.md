# Playbook — CC3.3 Fraud risk

- **Control ID:** CC3.3
- **Control description:** The entity considers the potential for fraud in assessing risks to the achievement of objectives.
- **Evidence-collection mechanism:** Daily tail of `hydra/plugins/secret-scanner/state/findings.jsonl` (committed secrets) and `hydra/plugins/audit-trail/state/log.jsonl` (HMAC-chained tamper-evident log).
- **Producer (today):** `hydra/plugins/secret-scanner/`, `hydra/plugins/audit-trail/`.
- **Retention rule:** 7 years.
- **Who reviews:** Repo maintainer weekly; HMAC chain integrity verified per audit-trail's own verification mechanism.
- **Escalation path:** HMAC chain break → tamper investigation, freeze writes, surface to security-closure. New secret finding → rotate credential per F-006 runbook.
- **Type II evidence shape:** Continuous HMAC-chained log over the window with auditable chain head; secret-scan findings showing remediation lifecycle.
- **External dependency:** None.
