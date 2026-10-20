---
title: Agent Frameworks – Open Source Ai
description: Libraries for building single and multi-agent systems. Open-source agent frameworks compared, with install guides – CodesbyFebin Open Source Ai.
---
# Agent Frameworks

Libraries for building single and multi-agent systems.

*Last checked: 2026-10-20*

## Comparison

| Project | What it does | Style | Language | Licence |
|---|---|---|---|---|
| LangChain | Composable LLM application framework | Broad integrations | Python | MIT |
| LangGraph | Graph-based stateful agent orchestration | Controllable workflows | Python | MIT |
| CrewAI | Role-based multi-agent crews | Multi-agent teams | Python | MIT |
| AutoGen | Conversational multi-agent framework | Agent conversations | Python | CC-BY-4.0 (docs) / MIT (code) |
| smolagents | Minimal code-writing agents | Lightweight | Python | Apache-2.0 |
| Agno | Fast agent framework with memory and tools | Performance | Python | Apache-2.0 |
| OpenHuman | Lightweight agent harness that runs hundreds of agents on a small VPS | - | Rust | GPL-3.0 |

## Quick start

```bash
pip install smolagents
export OPENAI_BASE_URL=http://localhost:4000/v1 OPENAI_API_KEY=sk-local
```
Then create an agent with an OpenAI-compatible model class from your chosen framework.

## Get the source

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/agent-frameworks
```

Paths:

- `stacks/agent-frameworks/langchain`
- `stacks/agent-frameworks/langgraph`
- `stacks/agent-frameworks/crewai`
- `stacks/agent-frameworks/autogen`
- `stacks/agent-frameworks/smolagents`
- `stacks/agent-frameworks/agno`
- `stacks/agent-frameworks/openhuman`
