# agent-foundations

**The foundations for building durable AI agents — conduct, engines, and the math behind both.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Most agent stacks ship with prompts, tools, and hopes. This repo gives you the missing layer: a model-agnostic framework of behavior rules, algorithmic primitives, a failure-mode taxonomy, and adoption recipes — battle-tested across production agent systems and packaged for drop-in adoption.

---

## Why this exists

Every team building agents rediscovers the same problems:

- *"Why did Claude push to main even though we said not to?"* — instruction attenuation in long contexts.
- *"Why does it keep refactoring code I didn't ask it to touch?"* — task drift, no surgical-changes rule.
- *"Why is this trust score swinging so wildly?"* — Beta-Bernoulli with no prior; one observation flips the verdict.
- *"Why is the same bug recurring across sessions?"* — no precedent log; the agent forgets what failed last week.
- *"Why did our test suite pass but the migration break in prod?"* — self-certification, no independent verification.

The fixes for these are well-known to people who've shipped agents at scale. They're scattered across blog posts, internal docs, and folklore. **agent-foundations consolidates them into a single dependency-free framework.**

---

## What's in the box

```
agent-foundations/
├── conduct/      ← 12 behavior modules: discipline, context, verification,
│                   delegation, tool-use, formatting, skill-authoring,
│                   hooks, precedent, tier-sizing, web-fetch, failure-modes
├── engines/      ← 9 algorithmic primitives: Aho-Corasick, Shannon entropy,
│                   Beta-Bernoulli, Markov drift, Hunt-Szymanski LCS,
│                   Zhang-Shasha tree edit, Tarjan SCC, Wald SPRT,
│                   Jaccard-Cosine boundary segmentation
├── taxonomy/     ← 14 named failure codes (F01–F14), one doc per code,
│                   with signature, counter, examples, escalation
├── recipes/      ← Adoption guides for Claude Code, OpenAI Agents SDK,
│                   Cursor, and generic system prompt
├── docs/         ← Architecture overview + ADRs
├── glossary.md   ← Unified terminology
├── anti-patterns.md  ← Cross-cutting catalog of what not to do
└── CLAUDE.md     ← Repo-level instructions for agents editing this repo
```

---

## Quickstart — 3 minutes

### Claude Code

```bash
git submodule add https://github.com/enchanter-ai/agent-foundations shared/foundations
```

In your project's `CLAUDE.md`:

```markdown
- @shared/foundations/conduct/discipline.md
- @shared/foundations/conduct/verification.md
- @shared/foundations/conduct/tool-use.md
- @shared/foundations/conduct/failure-modes.md
```

Full guide: [`recipes/claude-code.md`](recipes/claude-code.md).

### OpenAI Agents SDK

```python
from pathlib import Path
from agents import Agent

ROOT = Path("vendor/agent-foundations/conduct")
modules = ["discipline", "verification", "tool-use", "delegation"]
instructions = "\n\n".join((ROOT / f"{m}.md").read_text() for m in modules)

agent = Agent(name="MyAgent", instructions=instructions, model="gpt-5", tools=[...])
```

Full guide: [`recipes/openai-agents.md`](recipes/openai-agents.md).

### Cursor

Drop pointer rules into `.cursor/rules/`:

```markdown
---
description: Coding discipline — think-first, simplicity, surgical, goal-driven
globs: ["**/*"]
alwaysApply: true
---

@.cursor/foundations/conduct/discipline.md
```

Full guide: [`recipes/cursor.md`](recipes/cursor.md).

### Anything else (raw API, llama.cpp, Ollama, …)

```python
system_prompt = "\n\n".join(
    (foundations_root / "conduct" / f"{m}.md").read_text()
    for m in ["discipline", "verification", "tool-use"]
)
```

Full guide: [`recipes/system-prompt.md`](recipes/system-prompt.md).

---

## What you actually get

### Behavior rules that survive long contexts

[`conduct/`](conduct/) ships twelve modules. The lightest pull-in is just `discipline.md` (~700 tokens) — four stances (think-first, simplicity, surgical, goal-driven) that catch the majority of unsolicited refactors, premature actions, and over-helpful substitutions.

A heavier pull-in adds `context.md` (U-curve placement, checkpoint protocol), `verification.md` (independent checks, dry-run for destructive ops), and `failure-modes.md` (the 14-code taxonomy). That's the production starter pack.

### Algorithmic primitives, with derivations

[`engines/`](engines/) is the math-grounded layer. Each engine has six required sections: Problem, Formula, Decision rule, Complexity, Implementation pattern, Failure modes. No vibe-coded scoring functions; if it ships in this folder, it has a paper reference and a Big-O.

| Engine | Use case |
|--------|----------|
| [`pattern-detection.md`](engines/pattern-detection.md) | Multi-pattern text scan in linear time (Aho-Corasick) |
| [`entropy-analysis.md`](engines/entropy-analysis.md) | Detect generated tokens / secrets without a pattern list (Shannon) |
| [`trust-scoring.md`](engines/trust-scoring.md) | Online posterior estimate of a probability (Beta-Bernoulli) |
| [`drift-detection.md`](engines/drift-detection.md) | Catch unproductive loops in event streams (Markov + EMA) |
| [`lcs-alignment.md`](engines/lcs-alignment.md) | Measure how much of an anchor sequence survived (Hunt-Szymanski) |
| [`tree-edit.md`](engines/tree-edit.md) | Quantify structural change between trees (Zhang-Shasha) |
| [`scc.md`](engines/scc.md) | Find dependency cycles in O(V+E) (Tarjan) |
| [`sprt.md`](engines/sprt.md) | Decide between two hypotheses with minimum samples (Wald SPRT) |
| [`boundary-segmentation.md`](engines/boundary-segmentation.md) | Cluster events into tasks (Jaccard + cosine + time-decay) |

### A failure taxonomy that compounds

Free-text learning notes don't compound. Tagged ones do. [`taxonomy/`](taxonomy/) ships 14 canonical codes with precise signatures, testable counters, and escalation rules:

- F01 Sycophancy · F02 Fabrication · F03 Context decay · F04 Task drift · F05 Instruction attenuation
- F06 Premature action · F07 Over-helpful substitution · F08 Tool mis-invocation · F09 Parallel race · F10 Destructive without confirmation
- F11 Reward hacking · F12 Degeneration loop · F13 Distractor pollution · F14 Version drift

Tag every entry in your failure log with one code. Now you can aggregate. Now you can learn.

### Adoption guides, not just docs

[`recipes/`](recipes/) gives you the wiring for the four most common host platforms. No hand-waving — concrete file paths, concrete config, a verification step you can actually run.

---

## Before / after

A small but real example:

**Before** the conduct is loaded — agent context: *"fix the off-by-one in pagination":*

```diff
- function paginate(items, page, perPage) {
-   const start = page * perPage;
-   return items.slice(start, start + perPage);
- }
+ class Paginator {                          // unsolicited refactor (F04)
+   constructor(items) { this.items = items; }
+   /** Returns the requested page of items. */  // unsolicited docs (F04)
+   page(p, n) {
+     const start = (p - 1) * n;            // the actual fix
+     return this.items.slice(start, start + n);
+   }
+ }
```

**After** loading `conduct/discipline.md`:

```diff
  function paginate(items, page, perPage) {
-   const start = page * perPage;
+   const start = (page - 1) * perPage;
    return items.slice(start, start + perPage);
  }
```

Same task. Surgical change. No drift.

---

## Design principles

1. **Model-agnostic.** Examples may name a vendor; modules don't bind to one.
2. **Drop-in or à la carte.** Pick the modules you want; ignore the rest. No required entry point.
3. **Zero runtime dependencies.** Pure prose + math. Loadable into any system that accepts text instructions.
4. **Honest numbers.** Engine docs include failure modes alongside the math. We tell you when the algorithm is the wrong tool.
5. **Layered, not bundled.** Conduct rules don't embed engine math; engines don't make decisions; taxonomy doesn't run code; recipes don't invent rules. The layering is the discipline.

See [`docs/architecture/README.md`](docs/architecture/README.md) for the structure and [`docs/adr/0001-four-layers.md`](docs/adr/0001-four-layers.md) for why.

---

## What this won't do

- **Force the agent to obey.** Memorized rules attenuate over long contexts. For load-bearing rules, pair with a runtime hook.
- **Replace evals.** Conduct shifts default behavior on average; per-task evals still own task quality.
- **Provide reference implementations.** Engines describe the math; runnable code lives in adopter projects.
- **Compete with prompt-engineering tools.** This is a *foundation* — it composes with your prompts, doesn't replace them.

---

## Contributing

Issues and PRs welcome. The contribution bar:

- **New conduct module:** justify why it doesn't fit an existing module.
- **New engine:** include reference, complexity, failure modes.
- **New failure code (F15+):** observed in 3+ independent contexts, testable counter, no overlap with existing codes.
- **New recipe:** concrete adoption steps + a verification check.

See [`CLAUDE.md`](CLAUDE.md) for repo-level editing rules. The framework is dogfooded — contributors are expected to follow the conduct while editing the conduct.

---

## License

MIT. See [LICENSE](LICENSE). Use freely, including commercially. No warranty.

---

## Acknowledgments

Built on the shoulders of well-studied algorithms — Aho & Corasick, Shannon, Tarjan, Wald, Hunt & Szymanski, Zhang & Shasha, Jaccard, Salton — and the operational lessons of every engineer who's debugged an LLM agent in production.

If your team adopts agent-foundations and finds something missing, [open an issue](https://github.com/enchanter-ai/agent-foundations/issues). The framework grows by accumulation of named patterns, not by speculation.
