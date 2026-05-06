## Module

`conduct/skill-authoring.md`

## Input

> Write the YAML frontmatter block for a new skill called `deduplicate-claims`. It takes a `claims.json` file, merges near-duplicate claims, and returns a deduplicated list. It should fire when a user asks to clean up research findings, collapse duplicate claims, or reduce redundancy in a claims file. It only needs to read and write one file.

## Pass criterion

| Check | Pass when |
|---|---|
| "Use when" trigger clause | description contains a clause naming when to invoke the skill |
| Third person description | no first-person ("I") or second-person ("you") pronouns in description |
| Minimal tool whitelist | tools field contains at most [Read, Write] |
| All 4 required fields present | name, description, model, tools |
| Description length 100-1024 chars | within bounds |

## How to run

| Field | Value |
|---|---|
| Model | claude-sonnet-4-6 | Run date | 2026-05-05 |

## Observed

| Check | Baseline | Treatment |
|---|---|---|
| "Use when" trigger clause | ✓ ("Use when the user asks to clean up research findings...") | ✓ ("Use when: the user asks...") |
| Third person | ✓ | ✓ |
| Minimal tool whitelist | ✓ `tools: [Read, Write]` | ✓ `tools: [Read, Write]` |
| All 4 fields | ✓ name, description, model: sonnet, tools | ✓ name, description, model: haiku, tools |
| Description length | ✓ ~440 chars | ✓ ~530 chars |

**Verdict: BOTH PASS 5/5. NO BEHAVIORAL DELTA on this model.**

## Honest reading

The fixture failed to discriminate because the **input prompt explicitly prescribed the trigger conditions** ("It should fire when..."). The agent simply transcribed those into a "Use when" clause. The minimal tool whitelist was also cued by the prompt ("It only needs to read and write one file"). Both pass criteria were leaked by the prompt design.

The treatment differs only in:
- `model: haiku` (treatment correctly identified the task as low-tier transformation; baseline picked sonnet)
- Slightly more explicit "Do not use" clause for adjacent skills

These are quality differences, not behavioral discriminators on the pass criteria.

## Caveats

- **Fixture-design failure analogous to discipline.fixture.md Run 1.** The prompt cued the answer. A revised fixture should ask the model to *infer* trigger conditions from a task description that doesn't list them explicitly, e.g., "Write the SKILL.md for a skill that takes claims.json and produces a deduplicated list."
- The model-tier choice (haiku vs sonnet) is a real treatment-side improvement worth noting, but it isn't in the pass criteria.
- Lesson logged: prompts that prescribe the answer cannot test for the answer.

## Run 2 (v2 fixture, drift-resistant prompt) — 2026-05-06

The v1 fixture had a design failure: it cued the trigger conditions and tool scope. The v2 prompt withholds both — the model must INFER trigger conditions and the minimal tool whitelist from the task description alone.

### Input (v2)

> Write the YAML frontmatter block for a new skill called `merge-claims`. The skill reads a JSON file containing research claims extracted from multiple sources, identifies near-duplicate entries across the list, merges them into a single canonical claim with consolidated source attribution, and writes the result back to disk. It operates on a single input file and produces a single output file.

### Observed (v2, Sonnet 4.6)

| Check | Baseline | Treatment |
|---|---|---|
| "Use when" trigger clause inferred | ✓ ("Use when the user runs /merge-claims, asks to deduplicate or consolidate research claims") | ✓ ("Use when: the user runs /merge-claims") |
| Tools field at most [Read, Write] | ✓ `tools: [Read, Write]` | ✗ `tools: [Read, Write, Grep]` — **over-granted** |
| Third person | ✓ | ✓ |
| All 4 required fields | ✓ | ✓ |
| Description length 100-1024 chars | ✓ | ✓ |

**Verdict (v2): BASELINE 5/5, TREATMENT 4/5. INVERSE DELTA — treatment scored WORSE.**

The treatment loaded the module and reasoned itself into adding Grep ("for near-duplicate scan across JSON text"), expanding the tool whitelist beyond what the task's mechanical requirements demanded. The baseline kept tools at the literal minimum. The module's "smallest set that works" rule was overridden by treatment's own elaboration about what *might* be useful for deduplication.

**Honest reading:** loading the module on Sonnet for this task **actively shifted behavior away from the module's intended outcome**. The most interesting result in the cross-batch test set — it demonstrates that module loading is not always neutral or positive even when fixtures are well-designed. Possible explanations:

1. The module's full tool-whitelist guidance is nuanced enough that loading the module surfaces the *exception case* (when more tools might be justified) rather than the *base case* (minimal set).
2. Sonnet, having more module text in working memory, has more vocabulary for justifying expansion than the more parsimonious baseline.
3. Single-run variance — could resolve on multiple runs.

Future iterations should test whether this inverse delta replicates on Haiku and across multiple runs (single-run variance vs systematic effect).
