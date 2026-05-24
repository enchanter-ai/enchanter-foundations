# Macro roadmap — enchanter-ai security posture to audit-grade 100/100

Generated 2026-05-11. Replaces the abstract Tier C handoff with phased deliverables, dependencies, named owners, and explicit go/no-go gates.

## Three buckets, one phased plan

| Bucket | Items | Achievable by | Inline today |
|---|---|---|---|
| **B1** Inline-fixable critical residuals | R-018, R-019, R-020 | code + commit | YES (this session) |
| **B2** External time/personnel/capital | pentest, SOC 2, ISO 42001, FedRAMP, real traffic, operator wiring, CodeQL FP | external auditors / customer time / operator creds | NO (calendar-bound) |
| **B3** Research-frontier | R-021 alignment faking, R-022 sandbagging | published detection mechanism (none yet) | NO (no known fix) |

## Phase timeline

```
Phase 0   ┃ ≤ 1 week     ┃ inline critical fixes + operator wiring + CodeQL FP suppression
Phase 1   ┃ months 1-3   ┃ external pentest engagement + SOC 2 evidence collection starts + ISO 42001 cert body selection
Phase 2   ┃ months 3-9   ┃ SOC 2 observation period running + ISO Stage 1+2 audit + production fire-and-tune pilot
Phase 3   ┃ months 9-18  ┃ SOC 2 Type II report + ISO certificate + FedRAMP hosted control plane MVP + 3PAO engagement
Phase 4   ┃ months 18-24+┃ FedRAMP ATO + surveillance audits + alignment research integration
```

## Dependency graph

```
                         R-018/19/20 (B1, Phase 0)
                                │
                                ▼
       ┌────────────────────────┴────────────────────────┐
       ▼                                                 ▼
External pentest engagement                  SOC 2 evidence collection (autonomous, starts Phase 0)
       │                                                 │
       ▼                                                 ▼
Pentest report (Phase 1-2)                  SOC 2 Type II observation (6mo, Phase 1-3)
       │                                                 │
       └──────────────┐                                  ▼
                      ▼                       SOC 2 audit (Phase 3, ~3mo field work)
            ISO 42001 cert body Stage 1                  │
            (Phase 2, ~2mo)                              │
                      │                                  │
                      ▼                                  │
            ISO 42001 Stage 2 (Phase 2-3)                │
                      │                                  │
                      ▼                                  │
            ISO 42001 certificate (Phase 3)              │
                                                          │
                                                          ▼
                              FedRAMP hosted control plane MVP (Phase 3)
                                          │
                                          ▼
                              FedRAMP 3PAO engagement (Phase 3-4)
                                          │
                                          ▼
                              FedRAMP ATO (Phase 4)
```

## Phase 0 — immediate (≤ 1 week, ~80h dev work + 1d operator)

| Item | Owner | Effort | Deliverable |
|---|---|---|---|
| R-018 SKILL.md signing + verify | hydra owner | 30h | cosign-signed SKILL.md at install; capability-shield verifies sig before evaluating frontmatter |
| R-019 settings/hooks.json signing | hydra owner | 20h | cosign-signed config; PreToolUse hook rejects on sig mismatch |
| R-020 Defense-of-defense state layer | hydra owner | 30h | meta-canary on state file integrity; signed state files OR separate write-only audit channel |
| Operator wiring (Datadog/Sentry/PagerDuty/Slack/Splunk) | operator | 1d total | env vars set + verify-all.sh green |
| Hydra CodeQL `py/clear-text-logging-sensitive-data` FP suppression | operator | 5min | GitHub Security UI suppress with documented justification |
| Tag + verify another release post-fixes | release owner | 30min | `v0.2.0-rc.1` fires; Sigstore + SLSA verify clean |

**Phase 0 exit criteria**: all 3 pentest residuals fixed + operator integrations live + no open critical findings.

## Phase 1 — kickoff (months 1-3)

| Item | Owner | Cost | Deliverable |
|---|---|---|---|
| External pentest firm selection + RFP | governance | $25k-100k | signed SOW with Bishop Fox / NCC Group / Trail of Bits |
| Pentest field work | firm | n/a | full pentest report + remediation timeline |
| SOC 2 auditor selection + engagement letter | governance | $15k-30k year 1 | signed with A-LIGN / Schellman / Vanta partner |
| SOC 2 evidence collection going live | AIMS owner | 0 (already shipped) | daily cron commits to `soc2-evidence` branch; weekly operator review |
| ISO 42001 cert body selection + Stage 1 application | governance | $5k application | submitted to BSI / DNV / TÜV |
| Internal audit cycle #1 | AIMS owner + appointee | 2 weeks | pre-Stage-1 internal audit report; close any majors |
| First management review held + minuted | top management | 1 day | first §9.3 review per template |
| Production fire-and-tune pilot recruitment | operator | n/a | 3-5 design-partner customers signed up |

**Phase 1 exit criteria**: pentest report received + SOC 2 evidence period started (clock running) + ISO Stage 1 application submitted + first design-partner customer running enchanter-ai in production.

## Phase 2 — observation period (months 3-9)

| Item | Owner | Deliverable |
|---|---|---|
| Pentest remediation | hydra owner | every finding either fixed or risk-accepted with documentation |
| SOC 2 observation continues | AIMS owner | monthly auditor check-ins; evidence completeness >95% |
| ISO 42001 Stage 1 audit | cert body | readiness report; close any majors within 60d |
| ISO 42001 Stage 2 audit | cert body | full system audit; close any majors within 30d |
| Production fire-and-tune | design partners | ≥4 weeks each; FP/FN rates measured; tunings shipped |
| Quarterly management review #2 | top management | minuted; risk register quarterly review |
| Quarterly management review #3 | top management | minuted |

**Phase 2 exit criteria**: pentest closed + SOC 2 6mo observation window complete + ISO 42001 Stage 2 done + production FP/FN within acceptable band.

## Phase 3 — certifications + FedRAMP unlock (months 9-18)

| Item | Owner | Deliverable |
|---|---|---|
| SOC 2 auditor field work | auditor | sample evidence; interview personnel; SAR drafted |
| SOC 2 Type II opinion letter | auditor | unqualified opinion preferred |
| ISO 42001 certificate issued | cert body | 3-year certificate |
| FedRAMP hosted control plane MVP | engineering | optional cloud relay for audit-trail OTLP + pager; multi-tenant rate-limiter; SSO/SCIM; per `hosted-control-plane-prerequisite.md` |
| FedRAMP 3PAO selection + SAP | governance | signed engagement, $200k-500k year 1 |
| 3PAO assessment | 3PAO | SAR + POAM produced |
| Quarterly management reviews #4-#6 | top management | minuted |

**Phase 3 exit criteria**: SOC 2 Type II opinion in hand + ISO certificate in hand + 3PAO SAR submitted to JAB/agency.

## Phase 4 — ATO + ongoing posture (months 18-24+)

| Item | Owner | Deliverable |
|---|---|---|
| FedRAMP ATO | sponsoring agency / JAB | formal Authority To Operate |
| Continuous monitoring | AIMS owner | monthly POAM updates; quarterly SAR updates |
| SOC 2 surveillance | auditor | annual mini-audit |
| ISO 42001 surveillance | cert body | annual surveillance audit (lighter scope) |
| Alignment research integration | governance + AIMS owner | blind capability eval protocol when published detector emerges |

**Phase 4 exit criteria**: ATO granted; ongoing posture sustained.

## Total cost + time envelope

| Frame | Lower | Typical | Slip case |
|---|---|---|---|
| Time to SOC 2 Type II | 9mo | 12mo | 18mo |
| Time to ISO 42001 certificate | 6mo | 9mo | 18mo |
| Time to FedRAMP ATO (from architectural unlock) | 12mo | 18mo | 24mo+ |
| Year-1 cash spend (pentest + SOC 2 + ISO) | $70k | $150k | $250k |
| Year-1 + FedRAMP year-1 spend | $270k | $650k | $1.0M |

## Documents shipped with this roadmap

Each external item has its own micro-roadmap shipped to `roadmap-2026/`:

- `pentest-engagement-package.md` (vendor comparison + RFP + kickoff)
- `soc2-engagement-package.md` (CPA firm comparison + observation start checklist)
- `iso-42001-engagement-package.md` (cert body comparison + Stage 1 prep)
- `fedramp-engagement-package.md` (hosted control plane MVP + 3PAO RFP)
- `production-fire-and-tune-launch.md` (design-partner recruitment + tuning playbook)
- `operator-wiring-kickoff.md` (Day-1 walkthrough + verify-all checklist)
- `alignment-research-watch.md` (literature survey + blind-eval methodology)

Each inline-fixable critical residual has shipped code:

- R-018 SKILL.md signing → `hydra/plugins/capability-shield/` extension
- R-019 settings/hooks signing → `hydra/plugins/config-shield/` extension
- R-020 defense-of-defense → new plugin `hydra/plugins/state-integrity/`

## Open vs closed accounting

- **Bucket 1 (B1)**: target 3/3 closed inline this session (Phase 0)
- **Bucket 2 (B2)**: 7/7 packaged with operator-handoff micro-roadmaps; execution is operator-driven
- **Bucket 3 (B3)**: 2/2 documented as research-frontier; literature watch ongoing

This roadmap is the contract. Updates flow through quarterly management reviews per ISO 42001 §9.3.
