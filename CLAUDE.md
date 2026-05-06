# agent-foundations — Repo Instructions

Audience: Claude (or any agent) editing this repo.

## What this repo is

A standalone framework for building durable AI agents:

- `conduct/` — model-agnostic behavioral modules (discipline, context, verification, delegation, tool-use, etc.)
- `engines/` — generic algorithmic primitives (Aho-Corasick, Beta-Bernoulli, Wald SPRT, Tarjan SCC, etc.)
- `taxonomy/` — failure-mode catalog with one doc per code (F01–F21 + `axes.md` 5-axis hybrid mapping)
- `runbooks/` — incident-response runbooks, one per F-code (Detect / Triage / Rollback / Post-incident)
- `recipes/` — adoption guides per host (Claude Code, OpenAI Agents SDK, Cursor, LangChain, Pydantic-AI, BAML, generic system prompt, eval-harnesses, stupid-agent-review)
- `tests/` — A/B fixtures verifying conduct module impact + `runner.py` reference Python implementation
- `docs/` — ADRs, architecture, `self-test.md` (A/B methodology + per-module inventory)
- `anti-patterns.md`, `glossary.md` — cross-cutting references

## House rules for editing

1. **Model-agnostic.** Examples may name a vendor (Claude / GPT / Gemini), but no module assumes a specific harness, runtime, or product. If a paragraph only makes sense inside one product, it doesn't belong here.
2. **Cross-refs as relative paths.** Inside `conduct/`, sibling refs use `./X.md`. Across folders, use `../engines/X.md` style. Never hardcode absolute paths or org-specific roots.
3. **Granular commits.** One module = one commit. Conventional Commits format: `feat(conduct): add discipline.md`, `feat(engines): add trust-scoring.md`, `docs(recipes): add claude-code.md`, `chore: …`, `fix: …`.
4. **No vendor lock-in in code snippets.** Bash/JSON/Python examples illustrate; they don't depend on a specific tool's runtime.
5. **Marketing register lives in `README.md`.** Module bodies stay technical and tight. The hook/value-prop language goes in the top-level README only.

## Apply the conduct to yourself

Editing this repo means following [`conduct/discipline.md`](conduct/discipline.md), [`conduct/verification.md`](conduct/verification.md), and the rest. The framework is dogfooded — if you find yourself violating it while editing it, that's a signal the module needs to be sharper.

## Self-test posture

When adding or modifying a `conduct/` module, the matching fixture under `tests/<module>.fixture.md` should also be reviewed and re-run. The fixture format is documented in [`docs/self-test.md`](docs/self-test.md); the runtime architecture lives in [`recipes/stupid-agent-review.md`](recipes/stupid-agent-review.md); a reference Python runner is at [`tests/runner.py`](tests/runner.py).

Run a fixture manually with:

```bash
python tests/runner.py tests/<module>.fixture.md          # print results to stdout
python tests/runner.py tests/<module>.fixture.md --apply   # update Observed in-place
```

Honest-numbers principle applies to fixture results: ship the actual outcome (no delta, inverse delta, errored treatment) rather than fabricating a positive verification. The framework's measurement of itself follows the same rule the modules require of agents.

## License

MIT. Contributions are welcome under the same terms — see [LICENSE](LICENSE).
