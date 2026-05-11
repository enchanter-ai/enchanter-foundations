# Playbook — CC6.4 Physical access

- **Control ID:** CC6.4
- **Control description:** The entity restricts physical access to facilities and protected information assets.
- **Evidence-collection mechanism:** Daily `attestation` event declaring N/A — distributed code repository, no physical infrastructure under enchanter's direct control. Customer-deployed instances of the substrate inherit the customer's physical-access controls.
- **Producer (today):** N/A — synthetic attestation.
- **Retention rule:** 7 years.
- **Who reviews:** Repo maintainer monthly.
- **Escalation path:** If enchanter ever operates physical infrastructure (data center, office hosting production systems), the attestation switches from N/A to physical-access-control evidence and this playbook is rewritten.
- **Type II evidence shape:** N/A attestation persists across the window unless scope changes.
- **External dependency:** Customer-deployed instances' physical-access controls (their evidence, not ours).
