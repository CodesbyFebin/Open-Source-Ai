---
title: Chat UIs – Open Source Ai
description: Self-hosted ChatGPT-style interfaces. Open-source chat uis compared, with install guides – CodesbyFebin Open Source Ai.
---
# Chat UIs

Self-hosted ChatGPT-style interfaces.

*Last checked: 2026-10-20*

## Comparison

| Project | What it does | Highlights | Language | Licence |
|---|---|---|---|---|
| Open WebUI | Feature-rich web UI for Ollama and OpenAI-compatible APIs | RAG, multi-user, plugins | Python/Svelte | Open WebUI License (BSD-3 + branding clause) |
| Lobe Chat | Modern multi-provider chat and agent workspace | Agents marketplace | TypeScript | LobeHub Community License (Apache-2.0 based) |
| LibreChat | Multi-provider chat with agents, auth and plugins | Enterprise auth | TypeScript | MIT |
| Chatbot UI | Minimal open-source chat front end | Simple, hackable | TypeScript | MIT |

## Quick start

```bash
docker run -d -p 3000:8080 -v open-webui:/app/backend/data ghcr.io/open-webui/open-webui:main
```
Open http://localhost:3000 and add your gateway as an OpenAI-compatible connection.

## Get the source

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/chat-ui
```

Paths:

- `stacks/chat-ui/open-webui`
- `stacks/chat-ui/lobe-chat`
- `stacks/chat-ui/librechat`
- `stacks/chat-ui/chatbot-ui`
