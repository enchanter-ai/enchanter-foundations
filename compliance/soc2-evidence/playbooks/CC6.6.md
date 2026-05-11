# Playbook — CC6.6 External threat protection

- **Control ID:** CC6.6
- **Control description:** The entity implements logical access security measures to protect against threats from sources outside its system boundaries.
- **Evidence-collection mechanism:** Daily tail of `hydra/plugins/canary/state/canary-results.jsonl` (prompt-injection canaries) plus `hydra/plugins/egress-shield` URL-block events. The `<untrusted_source>` wrapping pattern in `wixie/plugins/deep-research/` is documented in the brief artifact.
- **Producer (today):** `hydra/plugins/canary/`, `hydra/plugins/egress-shield/`.
- **Retention rule:** 7 years.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** Canary trigger without remediation → F-004 (CC6.6 partial readiness gap). Tighten and re-run. **GAP:** canary CI-blocking gate not yet wired.
- **Type II evidence shape:** Continuous canary-results log + egress-block log over the window.
- **External dependency:** None.
