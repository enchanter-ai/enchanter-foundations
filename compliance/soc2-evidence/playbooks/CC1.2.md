# Playbook — CC1.2 Board oversight

- **Control ID:** CC1.2
- **Control description:** The board of directors demonstrates independence from management and exercises oversight of the development and performance of internal control.
- **Evidence-collection mechanism:** Monthly `attestation` event emitted by `collect-evidence.py` declaring current org structure (`single-maintainer`, `board: none`). When org formalizes, the attestation switches to board-meeting minutes hash + member list.
- **Producer (today):** `org-structure` (synthetic — no plugin produces this).
- **Retention rule:** 7 years.
- **Who reviews:** Repo maintainer monthly.
- **Escalation path:** **GAP per soc2.md CC1.2** — deferred until org formalizes. Procurement-questionnaire response: cite the gap honestly; do not claim board oversight.
- **Type II evidence shape:** N/A while single-maintainer. Post-formalization: 12 monthly board-minutes hashes + attestation of independence.
- **External dependency:** Board formation, board charter, member onboarding — all external to this infrastructure.
