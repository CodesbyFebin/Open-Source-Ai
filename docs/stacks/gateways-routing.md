---
title: Gateways & LLM Routing – Open Source Ai
description: OpenAI-compatible gateways, routers, guardrail firewalls and free-LLM aggregators. Open-source gateways & llm routing compared, with install guides – CodesbyFebin Open Source Ai.
---
# Gateways & LLM Routing

OpenAI-compatible gateways, routers, guardrail firewalls and free-LLM aggregators.

*Last checked: 2026-10-20*

## Comparison

| Project | What it does | Focus | Language | Licence |
|---|---|---|---|---|
| FreeLLMAPI | Aggregates free LLM providers behind one /v1 endpoint with failover | Free-tier aggregation | TypeScript | MIT |
| OpenCode Free Router | Routes coding-agent traffic to free model endpoints | Free routing for coding agents | JavaScript | MIT |
| Bifrost | High-performance AI gateway with load balancing and fallbacks | Low-latency gateway | Go | Apache-2.0 |
| Trylon Gateway | Self-hosted LLM firewall with guardrails | Guardrails / security | Python | BUSL-1.1 |
| LiteLLM | Proxy + SDK for 100+ LLM APIs in OpenAI format, cost tracking | Broadest provider coverage | Python | MIT (enterprise/ dir separate) |
| Portkey Gateway | Fast AI gateway with routing, retries and caching | Edge-friendly gateway | TypeScript | MIT |

## Quick start

```bash
pip install 'litellm[proxy]'
litellm --model ollama/llama3.2 --port 4000
curl http://localhost:4000/v1/models
```
Point any OpenAI SDK at `http://localhost:4000/v1`.

## Get the source

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/gateways-routing
```

Paths:

- `stacks/gateways-routing/freellmapi`
- `stacks/gateways-routing/opencode-free-9router`
- `stacks/gateways-routing/bifrost`
- `stacks/gateways-routing/trylon-gateway`
- `stacks/gateways-routing/litellm`
- `stacks/gateways-routing/portkey-gateway`
