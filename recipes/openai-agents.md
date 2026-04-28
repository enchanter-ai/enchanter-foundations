# Recipe — OpenAI Agents SDK

How to adopt agent-foundations with the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/).

## What you get

The Agents SDK exposes `instructions` (system prompt), `tools`, and `handoffs` for delegation. Conduct modules slot into instructions; engines slot into tool implementations or post-call validators; the failure taxonomy slots into structured logging.

## Drop-in

```bash
git submodule add https://github.com/enchanter-ai/agent-foundations vendor/foundations
```

In Python:

```python
from pathlib import Path
from agents import Agent, Runner

ROOT = Path(__file__).parent / "vendor" / "foundations"

def load_conduct(*names: str) -> str:
    return "\n\n".join((ROOT / "conduct" / f"{n}.md").read_text() for n in names)

agent = Agent(
    name="MyOrchestrator",
    instructions=(
        "You are a senior backend engineer.\n\n"
        + load_conduct("discipline", "verification", "tool-use", "delegation")
    ),
    model="gpt-5",
    tools=[...],
)
```

## Picking modules by agent role

| Agent role | Modules to load |
|------------|-----------------|
| Top-tier orchestrator | `discipline`, `delegation`, `verification`, `failure-modes` |
| Mid-tier executor | `discipline`, `tool-use`, `formatting`, `failure-modes` |
| Low-tier worker (extraction, summarization) | `tool-use`, `tier-sizing` (so the prompt is mechanical), `web-fetch` (if it fetches) |

The `delegation.md` rules map directly to the SDK's `handoffs` mechanism — every handoff prompt should include the three non-negotiable clauses (structured return, scope fence, context briefing).

## Engines as tools

Engines from `engines/` are language-neutral primitives. Wrap them as SDK tools:

```python
from agents import function_tool

@function_tool
def trust_score(history: list[bool]) -> dict:
    """Beta-Bernoulli trust score over a binary history."""
    alpha, beta_ = 2.0, 2.0
    for ok in history:
        if ok:
            alpha += 1
        else:
            beta_ += 1
    mean = alpha / (alpha + beta_)
    var = (alpha * beta_) / ((alpha + beta_) ** 2 * (alpha + beta_ + 1))
    return {"mean": mean, "variance": var}
```

See [`../engines/trust-scoring.md`](../engines/trust-scoring.md) for the math and [`../engines/README.md`](../engines/README.md) for the catalog.

## Failure logging

Pipe each agent run through a structured logger that writes to a project-local failure log. Tag every entry with one of the [14 codes](../taxonomy/README.md):

```python
import json, time
from pathlib import Path

LOG = Path("state/failure-log.jsonl")

def log_failure(code: str, axis: str | None, hypothesis: str, outcome: str, counter: str):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps({
            "ts": time.time(),
            "code": code,
            "axis": axis,
            "hypothesis": hypothesis,
            "outcome": outcome,
            "counter": counter,
        }) + "\n")
```

Read [`../conduct/failure-modes.md`](../conduct/failure-modes.md) § How to read the log before a new round for the consult-then-act protocol.

## Tier mapping

The SDK doesn't enforce tiers, but the [`../conduct/tier-sizing.md`](../conduct/tier-sizing.md) rubric still applies:

| Tier | OpenAI default |
|------|----------------|
| Top | `gpt-5` |
| Mid | `gpt-4o` |
| Low | `gpt-4o-mini` |

Calibrate prompt verbosity per the rubric — over-decomposed prompts waste budget on top tier; under-decomposed prompts produce silent quality loss on low tier.

## Verifying the adoption

After integration, run a smoke test:

1. Ask the agent to do something it should refuse without confirmation (e.g., `rm -rf`). It should ask first.
2. Ask it a question that triggers context overflow. It should checkpoint.
3. Trigger a known F-code condition (e.g., F02 by asking for a non-existent file). It should ground (Glob/Grep) before claiming.

If any of those fail, the relevant module isn't being loaded — check the `instructions` concatenation.

## What this won't do

- Replace the SDK's tracing / observability — those are runtime; the conduct is design-time.
- Replace your prompt engineering — modules are *defaults*, not the prompt itself.
- Force structured output — pair with the SDK's response schemas / Pydantic models.
