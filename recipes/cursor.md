# Recipe — Cursor

How to adopt agent-foundations in [Cursor](https://cursor.com).

## What you get

Cursor reads `.cursor/rules/` (or legacy `.cursorrules`) at the workspace root for project-wide AI behavior. Conduct modules drop in as rule files. Cursor's chat and inline editing both pick them up.

## Drop-in

```bash
git submodule add https://github.com/enchanter-ai/agent-foundations .cursor/foundations
mkdir -p .cursor/rules
```

For each conduct module you want active, create a thin pointer rule. Example `.cursor/rules/01-discipline.mdc`:

```markdown
---
description: Coding discipline — think-first, simplicity, surgical, goal-driven
globs: ["**/*"]
alwaysApply: true
---

@.cursor/foundations/conduct/discipline.md
```

The frontmatter says when the rule applies; the body inlines the module via `@` syntax. Cursor's recent rules format (`.mdc`) supports both globs and conditional application.

## Recommended starter set

```
.cursor/rules/
├── 01-discipline.mdc
├── 02-context.mdc
├── 03-verification.mdc
├── 04-tool-use.mdc
└── 05-failure-modes.mdc
```

Five rules cover ~80% of the value. Add more as project complexity grows.

Sample `02-context.mdc`:

```markdown
---
description: Context budget hygiene — U-curve placement, checkpoint protocol
globs: ["**/*"]
alwaysApply: true
---

@.cursor/foundations/conduct/context.md
```

## Per-language scopes

Cursor rules support `globs` for selective application. Use this to load tier-sizing only for prompt files, formatting only for prompt-engineering folders, etc.:

```markdown
---
description: Tier-sizing for prompt files
globs: ["prompts/**/*.md", "agents/**/*.md"]
alwaysApply: false
---

@.cursor/foundations/conduct/tier-sizing.md
```

This avoids loading every module on every file edit — Cursor's effective context is finite.

## Engines as inline references

Engines are math-grounded primitives, not behavior rules — they don't belong in always-apply rules. Reference them on demand:

- In chat: *"Build a trust score for these N observations using @.cursor/foundations/engines/trust-scoring.md"*
- In a rule scoped to relevant files: e.g., scope `pattern-detection.md` to security-scanning code paths.

## Composer-mode considerations

Cursor's Composer mode generates multi-file changes. For composer:

- **Always-apply rules:** discipline, verification, tool-use, surgical-changes — these prevent unsolicited refactors across files.
- **Scoped rules:** delegation (only matters when composer dispatches to multiple parallel agents), formatting (only matters in prompt files).

## Failure logging

Cursor doesn't ship a structured failure log; add one to the project:

```bash
mkdir -p state
touch state/precedent-log.md
```

Reference the precedent protocol in your rules:

`.cursor/rules/06-precedent.mdc`:
```markdown
---
description: Self-observed failure log; consult before risky steps
globs: ["**/*"]
alwaysApply: true
---

@.cursor/foundations/conduct/precedent.md

Project precedent log: `state/precedent-log.md`. Grep before non-trivial Bash; append after unexpected failures.
```

## Verifying the adoption

1. Open Cursor's chat in the project.
2. Ask: *"What rules are currently active?"*
3. Cursor should list the rules you added.

If a rule isn't applying, check `globs` — `["**/*"]` matches everything; narrower patterns require an open file matching the pattern.

## What this won't do

- Cursor's selector is heuristic — many rules in the same scope can compete for attention. Keep rule descriptions sharp (see [`../conduct/skill-authoring.md`](../conduct/skill-authoring.md) for the description discipline that makes selectors work).
- Replace per-language linters / type checkers. Conduct + engines are about *how the agent behaves*, not *whether the code compiles*.
