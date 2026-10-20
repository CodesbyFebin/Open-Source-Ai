---
title: Gateways & LLM Routing – Open Source Ai
description: Unified OpenAI-compatible gateways, routers and free LLM API aggregators. Curated open-source gateways & llm routing stacks in CodesbyFebin Open Source Ai.
---
# Gateways & LLM Routing

Unified OpenAI-compatible gateways, routers and free LLM API aggregators.

## Quick start

Run a gateway (e.g. LiteLLM: `pip install litellm[proxy] && litellm --model ollama/llama3`) and point any OpenAI SDK at `http://localhost:4000/v1`.

## Get the code

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/gateways-routing
```

## Stacks

| Project | Path | License |
|---|---|---|
| [freellmapi](https://github.com/tashfeenahmed/freellmapi) | `stacks/gateways-routing/freellmapi` | MIT |
| [opencode-free-9router](https://github.com/0xgetz/opencode-free-9router) | `stacks/gateways-routing/opencode-free-9router` | MIT |
| [bifrost](https://github.com/maximhq/bifrost) | `stacks/gateways-routing/bifrost` | Apache-2.0 |
| [gateway](https://github.com/trylonai/gateway) | `stacks/gateways-routing/gateway` | NOASSERTION |
| [litellm](https://github.com/BerriAI/litellm) | `stacks/gateways-routing/litellm` | NOASSERTION |
| [gateway](https://github.com/Portkey-AI/gateway) | `stacks/gateways-routing/gateway` | MIT |
