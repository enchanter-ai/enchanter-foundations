# AI Risk Register — ISO/IEC 42001 §6.1.2

Per ISO/IEC 42001 clause §6.1.2 (Actions to address risks and opportunities). Each row identifies a risk to the AI Management System or its outcomes, assesses likelihood and impact, names a treatment, and tracks residual risk. Quarterly review per §9.3.

## Risk taxonomy

- **AI-OPS**: operational risks (latency, availability, drift)
- **AI-SEC**: security risks (injection, exfil, tampering)
- **AI-SUP**: supply-chain risks (compromised deps, signing infra)
- **AI-COMP**: compliance risks (regulatory exposure, evidence gaps)
- **AI-DATA**: data risks (poisoning, leakage, retention)
- **AI-ALIGN**: alignment risks (specification gaming, sycophancy)

## Risk entries

| ID | Category | Description | L | I | Score | Treatment | Owner | Residual | Review |
|---|---|---|---|---|---|---|---|---|---|
| R-001 | AI-SEC | Prompt injection via untrusted file content reaches skill body | M | H | High | mitigate — canary + deep-research `<untrusted_source>` wrapping | hydra owner | Med | 2026-08 |
| R-002 | AI-SEC | Indirect injection via WebFetch result | M | H | High | mitigate — canary CI gate (F-004); fixture set 40 → 53 (pentest) | hydra owner | Med | 2026-08 |
| R-003 | AI-SUP | Compromised npm/PyPI maintainer publishes typo-similar package | L | C | High | mitigate — package-gate 6 signals + OSV cron + registry-derived top-10k | hydra owner | Low | 2026-08 |
| R-004 | AI-SUP | Compromised CI runner signs malicious release | L | C | High | mitigate — Sigstore keyless signing + SLSA L3 provenance (F-002 verified) | release owner | Low | 2026-08 |
| R-005 | AI-SEC | Subagent escapes declared tool whitelist | M | H | High | mitigate — capability-fence (observe) + capability-shield (opt-in block) | hydra owner | Med | 2026-08 |
| R-006 | AI-SEC | Audit log tampered post-hoc | L | H | Med | mitigate — HMAC-SHA-256 hash-chain in audit-trail (post pentest F-PT-16 fix) | hydra owner | Low | 2026-08 |
| R-007 | AI-SEC | Egress to attacker-controlled domain exfiltrates secrets | M | C | Critical | mitigate — egress-monitor (observe) + egress-shield (opt-in block) | hydra owner | Med | 2026-08 |
| R-008 | AI-ALIGN | Sycophancy — agent agrees with user's flawed proposal | H | M | High | mitigate — doubt-engine.md conduct module + crow trust-scorer | wixie owner | Med | 2026-08 |
| R-009 | AI-ALIGN | Model invents nonexistent file/function in output | M | M | Med | mitigate — failure-modes.md F02 + verifier pass at end of research | wixie owner | Low | 2026-08 |
| R-010 | AI-OPS | Runaway tool-call loop burns budget | M | M | Med | mitigate — rate-limiter (observe) + rate-shield (opt-in block); pech threshold events | pech owner | Low | 2026-08 |
| R-011 | AI-OPS | Long-context attenuation drops earlier instructions | H | L | Med | mitigate — context.md U-curve placement + checkpoint protocol | wixie owner | Low | 2026-08 |
| R-012 | AI-OPS | State-file race corrupts learning data | M | M | Med | mitigate — locked JSONL append helper (inference-engine + gorgon + naga) | each plugin owner | Low | 2026-08 |
| R-013 | AI-DATA | PII in audit log or learnings.json | L | H | Med | mitigate — secret-scanner masks at write; retention TTL in evidence collection | hydra owner | Low | 2026-08 |
| R-014 | AI-DATA | Training data poisoning of inference-engine ledger | L | M | Low | accept — operator-local, signed cron, audit-trail covers writes | wixie owner | Low | 2026-08 |
| R-015 | AI-COMP | Regulatory exposure under EU AI Act for high-risk uses | L | C | High | mitigate — compliance evidence pkg (NIST AI RMF + ISO 42001 + EU AI Act mapping); pre-deployment risk assessment per AIMS §8.2 | governance | Med | 2026-08 |
| R-016 | AI-COMP | CISA SBOM mandate non-conformance blocks gov procurement | L | H | Med | mitigate — sbom-emitter + CycloneDX emission on release | release owner | Low | 2026-08 |
| R-017 | AI-COMP | EU CRA 2027 cyber-resilience obligations not met | L | H | Med | mitigate — Sigstore + SLSA L3 + Dependabot + CodeQL; vuln-handling SLA in conmon-plan.md | governance | Med | 2026-11 |
| R-018 | AI-SEC | TOCTOU on SKILL.md frontmatter selection (pentest F-PT-14/15/46) | M | C | Critical | mitigate — sign SKILL.md at install; verify mtime+hash before capability-shield eval; **action item, not yet shipped** | hydra owner | High | 2026-06 |
| R-019 | AI-SEC | settings.json + hooks.json unsigned, single Write disables defenses (F-PT-19/49) | M | C | Critical | mitigate — sign config files at install; PreToolUse verify; **action item, not yet shipped** | hydra owner | High | 2026-06 |
| R-020 | AI-SEC | Defense-state files fail-safe-on-malformed inverts under adversarial Write (F-PT-11/12/13/17) | M | C | Critical | mitigate — defense-of-defense layer: meta-canary on state file integrity; **action item, not yet shipped** | hydra owner | High | 2026-06 |
| R-021 | AI-ALIGN | F19 alignment faking — agent appears safe in eval but defects in production | L | C | High | awareness — capability eval protocol per Frontier Safety Framework; no runtime detector | governance | High | 2026-11 |
| R-022 | AI-ALIGN | F20 sandbagging — agent intentionally underperforms in eval | L | M | Med | awareness — blind capability evals; differential probing | governance | Med | 2026-11 |
| R-023 | AI-SUP | Vendor account takeover on enchanter-ai org | L | C | High | mitigate — 2FA mandatory, branch protection, signed commits; operator action required | governance | Med | 2026-08 |
| R-024 | AI-OPS | Hook fails closed silently (regression risk) | L | M | Low | mitigate — advisory contract enforced via hooks.md + conduct-abi.yml | governance | Low | 2026-11 |
| R-025 | AI-SEC | Capability-shield matcher loose-prefix bypass (pentest F-PT-31/32) | M | H | High | mitigate — strict matcher patch shipped 2026-05-11 (drop startswith fallback, require space-star or exact) | hydra owner | Low | 2026-08 |
| R-026 | AI-OPS | OTLP exporter not shipped — observability blind spot | L | M | Low | mitigate — exporter shipped in F-021/F-024; operator wires backend | governance | Low | 2026-08 |
| R-027 | AI-COMP | SOC 2 Type II evidence period not yet started | C | M | High | mitigate — evidence collection infrastructure shipped (compliance/soc2-evidence/); 6mo observation period operator-triggered | governance | High | 2026-11 |
| R-028 | AI-COMP | FedRAMP hosted control plane prerequisite not built | C | M | High | mitigate — pre-authorization pkg shipped; architectural decision required | governance | High | 2026-11 |
| R-029 | AI-OPS | Long-tail false-positive rate unknown (no real customer traffic) | C | L | Med | mitigate — synthetic fire-and-tune harness measures 8 plugins precision/recall; real-traffic gap explicit | governance | Med | 2026-08 |
| R-030 | AI-SUP | External pentest not yet commissioned | C | M | High | mitigate — internal pentest sim shipped (53 fixtures); scoping doc ready for external firm | governance | Med | 2026-08 |

## Likelihood scale
- L (Low): < 5% / year
- M (Med): 5-30% / year
- H (High): 30-70% / year
- C (Certain): > 70% / year

## Impact scale
- L (Low): minor degradation, < 1h response
- M (Med): operational hit, ≤ 1d response
- H (High): trust event, customer-visible, multi-day response
- C (Critical): regulatory / contractual / data breach

## Risk acceptance criteria (per AIMS policy §5.2)

The AIMS owner accepts residual risks at Low and below without escalation. Med residuals require quarterly review per §9.3. High and Critical residuals require explicit board-level acceptance + mitigation roadmap with named owner + due date.

**Current state**: 4 risks (R-018, R-019, R-020, R-027/028) at High residual — pentest follow-up + Tier C external work. Roadmap explicit in TIER_C_HANDOFF.md and `cert-body-engagement-plan.md`.
