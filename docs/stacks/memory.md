---
title: Memory – Open Source Ai
description: Long-term memory layers for agents and assistants. Open-source memory compared, with install guides – CodesbyFebin Open Source Ai.
---
# Memory

Long-term memory layers for agents and assistants.

*Last checked: 2026-10-20*

## Comparison

| Project | What it does | Approach | Language | Licence |
|---|---|---|---|---|
| Mem0 | Universal memory layer for AI agents | Extract-and-retrieve facts | Python | Apache-2.0 |
| OpenMemory | Local-first memory server (MCP) for AI tools | MCP memory server | Python | Apache-2.0 |
| Letta | Stateful agents with self-editing memory | Agent OS with memory | Python | Apache-2.0 |
| Graphiti | Temporal knowledge-graph memory | Knowledge graph | Python | Apache-2.0 |

## Quick start

```bash
pip install mem0ai
python -c "from mem0 import Memory; m=Memory(); m.add('I like Python', user_id='me'); print(m.search('language?', user_id='me'))"
```
Uses `OPENAI_API_KEY`/`OPENAI_BASE_URL`; point it at your gateway.

## Get the source

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/memory
```

Paths:

- `stacks/memory/mem0`
- `stacks/memory/openmemory`
- `stacks/memory/letta`
- `stacks/memory/graphiti`
