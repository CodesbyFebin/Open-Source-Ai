---
title: Evaluation & Observability – Open Source Ai
description: Tracing, evaluations and prompt management. Open-source evaluation & observability compared, with install guides – CodesbyFebin Open Source Ai.
---
# Evaluation & Observability

Tracing, evaluations and prompt management.

*Last checked: 2026-10-20*

## Comparison

| Project | What it does | Focus | Language | Licence |
|---|---|---|---|---|
| Langfuse | LLM tracing, evals and prompt management | Tracing platform | TypeScript | MIT (ee/ dirs separate) |
| Phoenix | AI observability and evaluation | Notebook + server | Python | Elastic-2.0 |
| promptfoo | Prompt testing and red-teaming CLI | CI evals | TypeScript | MIT |
| DeepEval | Unit-test style LLM evaluation | pytest-style | Python | Apache-2.0 |

## Quick start

```bash
npx promptfoo@latest init
npx promptfoo@latest eval
```
For tracing, self-host Langfuse or Phoenix and add their SDK callback.

## Get the source

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/eval-observability
```

Paths:

- `stacks/eval-observability/langfuse`
- `stacks/eval-observability/phoenix`
- `stacks/eval-observability/promptfoo`
- `stacks/eval-observability/deepeval`
