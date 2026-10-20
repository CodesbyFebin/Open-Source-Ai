---
title: Chat UIs – Open Source Ai
description: Self-hosted ChatGPT-style interfaces. Curated open-source chat uis stacks in CodesbyFebin Open Source Ai.
---
# Chat UIs

Self-hosted ChatGPT-style interfaces.

## Quick start

Start a chat UI with Docker, e.g. `docker run -d -p 3000:8080 ghcr.io/open-webui/open-webui:main`, then set the OpenAI base URL to your gateway.

## Get the code

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/chat-ui
```

## Stacks

| Project | Path | License |
|---|---|---|
| [open-webui](https://github.com/open-webui/open-webui) | `stacks/chat-ui/open-webui` | NOASSERTION |
| [lobe-chat](https://github.com/lobehub/lobe-chat) | `stacks/chat-ui/lobe-chat` | NOASSERTION |
| [LibreChat](https://github.com/danny-avila/LibreChat) | `stacks/chat-ui/LibreChat` | MIT |
| [chatbot-ui](https://github.com/mckaywrigley/chatbot-ui) | `stacks/chat-ui/chatbot-ui` | MIT |
