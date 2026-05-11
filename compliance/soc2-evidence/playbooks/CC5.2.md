# Playbook — CC5.2 Technology controls

- **Control ID:** CC5.2
- **Control description:** The entity also selects and develops general control activities over technology to support the achievement of objectives.
- **Evidence-collection mechanism:** Daily presence-check + state-file listing for each of the 10 hydra defensive plugins: audit-trail, capability-fence, egress-shield, secret-scanner, vuln-detector, package-gate, license-gate, sbom-emitter, action-guard, canary.
- **Producer (today):** `hydra/plugins/*/state/`.
- **Retention rule:** 1 year.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** Any plugin's `state/` missing or empty for >7 days → plugin not running. Restart, open issue tagged `compliance-cc5.2`. F-001/F-002/F-004/F-005/F-010 closure tracked in security-closure synthesis.
- **Type II evidence shape:** Continuous presence of all 10 plugin state dirs with rotating file contents.
- **External dependency:** None.
