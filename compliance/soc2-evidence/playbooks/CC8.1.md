# Playbook — CC8.1 Change management

- **Control ID:** CC8.1
- **Control description:** The entity authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes to infrastructure, data, software, and procedures to meet its objectives.
- **Evidence-collection mechanism:** Daily presence-check of `sylph/plugins/pr-lifecycle/state/` plus count of `wixie/prompts/*/tests.json` (regression suites ≥3 tests, ≥1 edge-case per CLAUDE.md § DEPLOY bar).
- **Producer (today):** `sylph/plugins/pr-lifecycle/`, `sylph/plugins/weaver-gate/`, `wixie/plugins/prompt-tester/`, `wixie/plugins/convergence-engine/`.
- **Retention rule:** 7 years.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** PR merged without weaver-gate approval → F-002 lane; revert and re-review. tests.json regression count dropping → investigate.
- **Type II evidence shape:** Continuous PR-lifecycle records + DEPLOY-verdict log across the window.
- **External dependency:** GitHub PR workflow (their audit log of PR approvals).
