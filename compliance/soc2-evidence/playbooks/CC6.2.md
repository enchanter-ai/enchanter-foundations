# Playbook — CC6.2 Access authorization

- **Control ID:** CC6.2
- **Control description:** Prior to issuing system credentials and granting system access, the entity registers and authorizes new internal and external users whose access is administered by the entity.
- **Evidence-collection mechanism:** Daily `metric` event recording skill-discovery-test results (9/10 dispatches correct, per `shared/conduct/skill-authoring.md`). Per-plugin `settings.json` permissions hash.
- **Producer (today):** `shared/conduct/skill-authoring.md`, each plugin's `.claude/settings.json`.
- **Retention rule:** 1 year.
- **Who reviews:** Repo maintainer weekly; new-skill PRs include the discovery-test result.
- **Escalation path:** Skill failing the 9/10 discovery test attempted to merge → block, request rework.
- **Type II evidence shape:** Per-new-skill discovery-test attestations across the window.
- **External dependency:** None.
