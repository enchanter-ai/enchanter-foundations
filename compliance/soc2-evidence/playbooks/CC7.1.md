# Playbook — CC7.1 Vulnerability detection

- **Control ID:** CC7.1
- **Control description:** To meet its objectives, the entity uses detection and monitoring procedures to identify (1) changes to configurations that result in new vulnerabilities and (2) susceptibilities to newly discovered vulnerabilities.
- **Evidence-collection mechanism:** Daily tail of `hydra/plugins/vuln-detector/state/audit.jsonl` plus listing of `*/.github/workflows/codeql.yml` workflows.
- **Producer (today):** `hydra/plugins/vuln-detector/`, CodeQL workflows, Dependabot config.
- **Retention rule:** 7 years.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** New high-severity finding → F-009 runbook (OSV-Scanner cron). **GAP:** OSV-Scanner cron not yet wired — addressed before Type II.
- **Type II evidence shape:** Continuous vuln-audit results + CodeQL run history across the window.
- **External dependency:** GitHub-hosted CodeQL and Dependabot (their advisory feeds), OSV.dev advisory feed.
