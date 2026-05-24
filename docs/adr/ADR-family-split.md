# ADR-0003 — Family-of-plugins layout: split monolithic vis into 7 focused packages

## Status

Accepted, 2026-05-11.

Repo rename effected the same day: `enchanter-ai/vis` → `enchanter-ai/vis`. All 7 packages tagged at v0.6.0; 10 sibling plugins migrated off the vendored tree.

## Context

The monolithic `vis` repo (≈230 tracked files: conduct, engines, taxonomy, runbooks, recipes, tests, docs, compliance, security, operator-wiring) was consumed by 10 sibling plugins via a vendored `shared/vis/` subtree. Three pressures stacked:

1. **Vendor-pattern sync cost.** Every conduct module update required 11 commits (1 canonical + 10 sibling re-vendors). Inter-sibling drift was visible: hydra hardcoded paths through `wixie/shared/vis/...` (see s2.1 audit), and several siblings carried stale copies. The cost-per-update was dominated by mechanical fan-out, not authorship.

2. **t0 empirical PASS on cross-plugin Read.** The s1.0 fixture probe (`tests/cross-plugin-read.fixture`) confirmed Claude Code's CLAUDE.md @-loader resolves file-relative paths across sibling plugin checkouts when the siblings are clones under the same parent directory. This unblocked a refactor that did not require any new runtime mechanism — siblings could @-import from a peer repo as cheaply as from a vendored copy.

3. **s1.0 architectural finding: `${CLAUDE_PLUGIN_ROOT}` is literal.** s1.0 Test B established that CLAUDE.md @-imports do NOT substitute `${CLAUDE_PLUGIN_ROOT}` — the string passes through verbatim. The only portable path shape is file-relative (`@../enchanter-<pkg>/conduct/X.md`). That ruled out marketplace-relative or env-var-relative path strategies, and locked the design around sibling-clone parent-directory conventions.

The s2.0 inventory pass surfaced a further pressure: the monolith bundled unrelated concerns. Conduct rules, algorithmic engines, failure taxonomy, runbooks, host-adoption recipes, compliance evidence, security audit artifacts, and operator-wiring all coexisted in one package. Sibling plugins consumed ~14 conduct modules from a tree of ~230 files. The 16× over-vendoring was waste, but more importantly it conflated "behavioral substrate" (universal) with "compliance evidence" (security-package only) and "engines" (orchestration-only).

## Decision

**Split the monolith into 7 focused packages under a single monorepo, with file-relative `@-imports` and a YAML `.vis-versions` pin file per sibling.**

The five locks:

1. **7 packages by verb.** `enchanter-core`, `enchanter-skills`, `enchanter-web`, `enchanter-memory`, `enchanter-cost`, `enchanter-safety`, `enchanter-orchestration`. Allocation per s2.0 § Decision 1 (exhaustive file-by-file table). `enchanter-core` is universal; `enchanter-safety` is the largest by file count (compliance + security + operator-wiring all folded in); `enchanter-orchestration` owns all 12 engines + `inference-substrate.md`.

2. **Monorepo with `pluginRoot: "./packages"`.** A single git repo `vis`, one `.claude-plugin/marketplace.json` at the repo root, 7 plugin manifests under `packages/<name>/.claude-plugin/plugin.json`. Doc-supported pattern per `plugin-marketplaces` § Walkthrough Step 4. `git mv` preserves per-file history across the cut-over — no `filter-repo` rewrite.

3. **Dep DAG, no cycles.** `core` is the root with no outbound deps. `{skills, web, memory, cost, safety}` each depend on `core`. `orchestration` depends on `core` AND `cost` (the only non-core edge, driven by `packages/orchestration/conduct/multi-turn-negotiation.md` referencing `packages/cost/recipes/eval-harnesses.md`). Verified topologically in s2.0 § Decision 2.

4. **Naming: `enchanter-<concept>` kebab-case; initial version 0.6.0 across all 7.** Continuity with the monolith's v0.6.0 — anyone migrating doesn't see a fresh 0.1.0 and wonder if it's a different product. Subsequent versions diverge per package. Semver policy per s2.0 § Decision 4 (MAJOR = removed/renamed module or tightened "should"→"must" detectable by consumers; MINOR = added module/code/recipe; PATCH = clarification without behavior change).

5. **`.vis-versions` YAML pin file per sibling.** Multi-package version pinning lives in a sibling-root YAML file (per s2.0 § Decision 5). CLAUDE.md @-imports name only paths (`@../enchanter-core/conduct/discipline.md`), never versions. `install.sh --bootstrap-vis` reads the pin file to checkout matching tags in the sibling-clone parent dir.

## Consequences

### Good

- **Per-update flow goes from 11 commits to 1.** A canonical commit in `vis/packages/<name>/` is the single source of truth. Siblings auto-resolve on next pull via `.vis-versions` semver range; no fan-out re-vendoring.
- **Per-sibling version pinning.** Each sibling pins each consumed package independently. `crow` can stay on `enchanter-core@~0.6.0` while `wixie` moves to `~0.7.0` without coordination.
- **Smaller per-sibling footprint.** Vendored `shared/vis/` deletion removed ~128 files per sibling (typical) — for a fleet of 10 siblings that's ~1280 redundant tracked files across the org.
- **Atomic cross-package edits stay atomic.** A change touching both `core` and `skills` ships as one PR, one commit, one release within the monorepo — multi-repo would have split this into a coordinated 2-PR dance.
- **Cross-cutting `docs/` survives at one location.** ADRs and architecture docs live at monorepo root; multi-repo would have forced them to fragment or pick a home package arbitrarily.

### Bad

- **Developer workflow now requires `vis/` as a sibling clone.** Fresh-clone developers need both their target sibling repo AND `vis` under the same parent dir for @-imports to resolve. Bootstrap script TBD (open question below).
- **3 of 7 packages have zero current consumers.** The s2.1 audit revealed `enchanter-memory`, `enchanter-cost`, and `enchanter-safety` have ZERO external consumers across the fleet of 10 siblings. Even nominally-adjacent siblings — `pech` (cost-themed) and `hydra` (security-themed) — self-implement rather than @-importing the matching vis modules. From s2.1 § Single-consumer / no-consumer packages:

  > "Of the 7 packages, only **core, skills, web** are universally consumed; **orchestration** has 3 consumers; **memory, cost, safety** have ZERO external consumers in the current fleet."

  This is shelf content, not architectural waste — the modules exist as the canonical home for their respective concerns and can be adopted later. But it signals a separate v0.7+ product question: should the fleet adopt nominally-applicable modules, or are these packages serving external (non-fleet) consumers only? See Open Questions.

- **Monorepo's single `marketplace.json` becomes load-bearing.** If Claude Code ever requires per-plugin marketplace files (schema regression), all 7 packages would need re-wiring. Tracked as a v0.6 risk (s2.0 risk register, new — open).

### Neutral

- **Tag-push per package is 7 release operations.** `claude plugin tag --push packages/<name>` × 7 succeeded in s2.2; the operational ceiling for a future v0.7 release of all 7 is the same. If only some packages bump, only those tag-pushes fire.
- **`orchestration → cost` is the only non-core edge.** Acceptable in a DAG. Driven by one cross-ref (`packages/orchestration/conduct/multi-turn-negotiation.md` → `packages/cost/recipes/eval-harnesses.md`). Could be eliminated in v0.7 by inlining a one-paragraph summary; deferred.
- **`operator-wiring-2026-05/` folded into `enchanter-safety`.** 17 files of paging/observability content — closest semantic match was safety, but if safety's audience splits (security-engineer vs. SRE) a v0.7 `enchanter-ops` package becomes a candidate.

## Alternatives considered

1. **Keep the monolith + vendor pattern.** Rejected — fails on the 11-commit-per-update tax. The vendoring mechanism doesn't scale past ~10 siblings, and inter-sibling drift was already observable (hydra hardcoding through wixie's tree).
2. **Git submodules.** Rejected — fragile developer experience (`git submodule update --recursive` failures are a known pain point), and submodule SHAs would force every sibling to bump on every vis change, defeating the per-sibling pinning goal.
3. **MCP resources.** Rejected — runtime resource-fetch indirection adds latency to every @-import resolution, and the MCP resource spec doesn't model the path-relative cross-plugin reading pattern that t0 confirmed works in Claude Code today.
4. **Custom tool / loader.** Rejected — would replace a tested Claude Code mechanism (CLAUDE.md @-loader with file-relative paths) with a bespoke layer requiring its own test suite and version compatibility matrix.
5. **Multi-repo (Option R).** Rejected in favor of monorepo. Would have required 7 separate `git filter-repo --subdirectory-filter` runs producing new repos with rewritten SHAs; 7 PR queues, 7 release pipelines, 7 CI configs; and `docs/` (ADRs spanning all packages) would have had to fragment or pick a home arbitrarily. Operational overhead higher by an order of magnitude for current team size.

## Open questions / future work

- **Why pech / hydra don't adopt nominally-applicable vis modules.** s2.1 Issue 2: pech (cost-themed) doesn't @-import `cost-accounting.md`; hydra (security-themed) doesn't @-import `refusal-and-recovery.md` or `compliance/*`. Is the vis content too generic for sibling-specific needs, or is this an adoption-gap question? Investigate in v0.7+ and either iterate the modules toward what siblings actually need or document them as external-adopter-only.
- **Bootstrap script for fresh-clone developer experience.** Currently a new developer cloning any sibling must also `git clone enchanter-ai/vis` into the same parent dir for @-imports to resolve. Write a one-line bootstrap (read `.vis-versions`, clone-or-pull `vis`, checkout matching tags) and document it in each sibling's README.
- **Dev-mode `--plugin-dir` behavior.** s1.0 Test A surfaced: `claude --plugin-dir` doesn't auto-resolve cross-plugin dependencies the way `claude plugin marketplace add` does. Documented as known; v0.7 candidate to either patch the dev-mode resolver or write a `bootstrap-dev.sh` workaround.
- **`${CLAUDE_PLUGIN_ROOT}` in CLAUDE.md.** s1.0 Test B: literal, not substituted. Locked path pattern via file-relative `@-imports`. If Claude Code adds substitution in a future release, file-relative paths still work (no churn), but the alternative shape becomes available.
- **Sibling skills directly consuming vis packages.** Today only sibling repo-root `CLAUDE.md` consumes vis packages. Per s2.0 reframing, sub-plugin skills (sibling-internal SKILL.md files) can adopt the cross-plugin-Read pattern from t0 PASS — would let individual skills declare narrower dep sets than the repo as a whole. v0.7+ candidate.
- **`enchanter-ops` package.** Operator-wiring content (paging, observability) currently folded into `enchanter-safety`. If safety's audience pulls apart (security-engineer vs. SRE), split as 8th package. Tracked.
- **Honest-numbers contract for adoption metrics.** Schedule D+30 review (2026-06-10) to count actual adoption of memory/cost/safety vs. baseline. If still 0 consumers, revisit whether shelf content has a non-fleet audience or should fold back into core.

## References

- s2.0 design lock — `wixie/state/roadmaps/2026-05-11-share-resources/s2-family-split/s2.0-design.md` (5 decisions, exhaustive content-allocation table, DAG verification)
- s2.1 audit aggregate — `s2.1-summary.md` + per-sibling `s2.1-audit/<sibling>.md` × 10 (Issue 2: zero-consumer packages)
- s2.2 build summary — `s2.2-summary.md` (7 packages tagged, marketplace landed, commit `d0d0f9c`)
- s2.3 sibling migrations — `s2.3-migrate/<sibling>.md` × 10 (vendored tree deleted, @-imports rewritten, pin files added)
- s1.0 design — `wixie/state/roadmaps/.../s1.0-design.md` (path-resolution Tests A, B, C; t0 cross-plugin-Read PASS)
- Plugin-marketplaces doc — `pluginRoot`, `./<path>` source pattern, kebab-case naming rule
- Plugins-reference doc — `dependencies` field with semver constraints
- ADR-0001 — Four-Layer Structure (the conduct + engines + taxonomy + recipes layering this split preserves within `enchanter-core` and across packages)
- ADR-0002 — Taxonomy expansion (the F01–F21 catalog now split: F01–F14 in core, F15–F21 in safety)
