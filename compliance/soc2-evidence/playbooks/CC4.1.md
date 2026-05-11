# Playbook — CC4.1 Ongoing evaluations

- **Control ID:** CC4.1
- **Control description:** The entity selects, develops, and performs ongoing and/or separate evaluations to ascertain whether the components of internal control are present and functioning.
- **Evidence-collection mechanism:** Daily hash of `wixie/plugins/inference-engine/state/catalog.json` (reconcile output: Wald SPRT + Beta-Binomial posteriors, LLR, verdicts, weights). Quarterly self-attestation files added to `agent-foundations/compliance/`.
- **Producer (today):** `wixie/plugins/inference-engine/` (`reconcile` subcommand).
- **Retention rule:** 7 years.
- **Who reviews:** Repo maintainer weekly; security-closure owner quarterly self-attest.
- **Escalation path:** Reconcile not run in >7 days (catalog hash stale) → flag in dashboard, run reconcile manually.
- **Type II evidence shape:** 6+ months of catalog-hash rotations plus 2 quarterly self-attestations during the window.
- **External dependency:** None — the substrate is internal.
