# Recipe — Claude Code

How to adopt agent-foundations in a [Claude Code](https://github.com/anthropics/claude-code) project.

## What you get

Claude Code reads `CLAUDE.md` files at every level of the project tree on session start. Its agent dispatcher reads skill descriptions from `.claude/skills/`. Its hooks fire on tool events declared in `.claude/settings.json`. All four are first-class entry points for this framework.

## Drop-in (3 minutes)

From your project root:

```bash
git submodule add https://github.com/enchanter-ai/agent-foundations shared/foundations
```

Or, for a vendored copy:

```bash
mkdir -p shared
git clone https://github.com/enchanter-ai/agent-foundations.git shared/foundations
rm -rf shared/foundations/.git
```

Then in your project's `CLAUDE.md`, reference what you want loaded into context:

```markdown
## Shared behavioral modules

These apply to every skill in this project.

- @shared/foundations/conduct/discipline.md — coding conduct
- @shared/foundations/conduct/context.md — attention-budget hygiene
- @shared/foundations/conduct/verification.md — independent checks
- @shared/foundations/conduct/delegation.md — subagent contracts
- @shared/foundations/conduct/tool-use.md — tool invocation hygiene
- @shared/foundations/conduct/precedent.md — log self-observed failures
- @shared/foundations/conduct/failure-modes.md — 14-code taxonomy
```

The `@path/to/file.md` syntax tells Claude Code to inline the file at session start. Only reference the modules you want loaded; loading all twelve is overkill for most projects.

## Picking modules by project type

| Project type | Recommended modules |
|--------------|---------------------|
| Anything (always load) | `discipline.md`, `verification.md`, `tool-use.md` |
| Long agent loops (convergence, iteration) | + `context.md`, `failure-modes.md` |
| Multi-subagent workflows | + `delegation.md`, `tier-sizing.md` |
| Skills + hooks heavy | + `skill-authoring.md`, `hooks.md` |
| Web research / fetching | + `web-fetch.md` |
| Cross-session memory | + `precedent.md` |
| Multi-target prompt engineering | + `formatting.md` |

## Hooks (optional)

If you want runtime guards instead of memorized rules, the hook contract from [`../conduct/hooks.md`](../conduct/hooks.md) drops into `.claude/settings.json`:

```jsonc
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "shared/foundations/scripts/lint-after-edit.sh" }]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [{ "type": "command", "command": "shared/foundations/scripts/inject-checkpoint.sh" }]
      }
    ]
  }
}
```

(The `scripts/` referenced are placeholders — agent-foundations ships docs and references; runnable scripts live in the adopting project.)

## Skills (optional)

Skills authored against the framework follow [`../conduct/skill-authoring.md`](../conduct/skill-authoring.md). At minimum, frontmatter:

```yaml
---
name: my-workflow
description: >
  Does X. Use when the user asks for Y or runs /my-workflow.
  Do not use for Z (see /other-workflow).
model: sonnet
tools: [Read, Edit, Write, Bash, Grep, Glob]
---
```

The body is a runbook (see § Body structure of the linked module).

## Memory + precedent

Claude Code ships an auto-memory system at `~/.claude/projects/<project>/memory/` for cross-session user-taught feedback. Pair it with a project-local precedent log per [`../conduct/precedent.md`](../conduct/precedent.md):

```bash
mkdir -p state
touch state/precedent-log.md
git add state/precedent-log.md && git commit -m "chore: seed precedent log"
```

Reference both in your `CLAUDE.md`:

```markdown
## Persistence

- Cross-session user feedback → auto-memory (managed by Claude Code).
- Self-observed failures → `state/precedent-log.md` (committed; team asset).
```

## Verifying the adoption

1. Open the project in Claude Code.
2. Ask: *"What modules are you loading from agent-foundations?"*
3. Claude Code should list the modules referenced in your `CLAUDE.md`.

If a referenced module isn't being read, check the path — `@` syntax is relative to the project root.

## What this won't do

- Force the agent to obey the conduct. Memorized rules attenuate (see [F05](../taxonomy/f05-instruction-attenuation.md)). For load-bearing rules, write a hook.
- Prevent destructive ops by itself. Pair `verification.md` with explicit Claude Code permissions and confirmation prompts.
- Replace per-project context. The conduct is *general*; your `CLAUDE.md` still owns project-specific rules (style, branch naming, deployment).
