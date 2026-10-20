---
title: Coding Agents – Open Source Ai
description: AI pair programmers and autonomous software agents. Open-source coding agents compared, with install guides – CodesbyFebin Open Source Ai.
---
# Coding Agents

AI pair programmers and autonomous software agents.

*Last checked: 2026-10-20*

## Comparison

| Project | What it does | Interface | Language | Licence |
|---|---|---|---|---|
| OpenHands | Autonomous software-engineering agent | Web / headless | Python | MIT |
| Continue | IDE assistant for VS Code and JetBrains | IDE extension | TypeScript | Apache-2.0 |
| Aider | Terminal pair programmer working on git repos | CLI | Python | Apache-2.0 |
| OpenCode | Terminal coding agent | TUI | TypeScript | MIT |
| Cline | Autonomous coding agent in VS Code | IDE extension | TypeScript | Apache-2.0 |

## Quick start

```bash
pip install aider-chat
aider --openai-api-base http://localhost:4000/v1 --model openai/llama3.2
```

## Get the source

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/coding-agents
```

Paths:

- `stacks/coding-agents/openhands`
- `stacks/coding-agents/continue`
- `stacks/coding-agents/aider`
- `stacks/coding-agents/opencode`
- `stacks/coding-agents/cline`
