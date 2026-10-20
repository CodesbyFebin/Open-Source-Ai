---
title: Low-code App Builders – Open Source Ai
description: Visual builders for LLM apps, agents and workflows. Open-source low-code app builders compared, with install guides – CodesbyFebin Open Source Ai.
---
# Low-code App Builders

Visual builders for LLM apps, agents and workflows.

*Last checked: 2026-10-20*

## Comparison

| Project | What it does | Licence note | Language | Licence |
|---|---|---|---|---|
| Dify | LLM app and agentic workflow platform | Multi-tenant SaaS restricted | Python | Dify Open Source License (Apache-2.0 + conditions) |
| Flowise | Drag-and-drop agent builder | Core Apache-2.0 | TypeScript | Apache-2.0 (enterprise dir separate) |
| Langflow | Visual flow builder for agents and RAG | Permissive | Python | MIT |
| n8n | Workflow automation with AI nodes | Source-available | TypeScript | Sustainable Use License (fair-code) |

## Quick start

```bash
git submodule update --init --depth 1 stacks/app-builders/dify
cd stacks/app-builders/dify/docker && cp .env.example .env && docker compose up -d
```
Add your gateway as a custom OpenAI-compatible model provider.

## Get the source

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/app-builders
```

Paths:

- `stacks/app-builders/dify`
- `stacks/app-builders/flowise`
- `stacks/app-builders/langflow`
- `stacks/app-builders/n8n`
