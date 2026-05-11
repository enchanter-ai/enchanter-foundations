# Playbook — CC6.8 Malicious software prevention/detection

- **Control ID:** CC6.8
- **Control description:** The entity implements controls to prevent or detect and act upon the introduction of unauthorized or malicious software to meet the entity's objectives.
- **Evidence-collection mechanism:** Daily tail of `hydra/plugins/vuln-detector/state/audit.jsonl` (npm audit + pip-audit results) plus hash of `hydra/plugins/package-gate/scripts/check-package.sh` (typosquat + age + maintainer checks).
- **Producer (today):** `hydra/plugins/vuln-detector/`, `hydra/plugins/package-gate/`.
- **Retention rule:** 7 years.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** New vuln finding → triage per F-009 runbook. Package-gate block bypassed → F08 (action failure). **GAP:** F-023 typosquat seed list not registry-derived.
- **Type II evidence shape:** Continuous vuln-audit log + package-gate script integrity across the window.
- **External dependency:** Upstream advisory databases (npm advisory, pip-audit OSV feed) — fed via the plugins, not part of our infrastructure.
