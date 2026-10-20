---
title: Backend & Infra – Open Source Ai
description: Backends, databases and auth for AI products. Open-source backend & infra compared, with install guides – CodesbyFebin Open Source Ai.
---
# Backend & Infra

Backends, databases and auth for AI products.

*Last checked: 2026-10-20*

## Comparison

| Project | What it does | Type | Language | Licence |
|---|---|---|---|---|
| Butterbase | Open-source backend-as-a-service: Postgres, auth, storage, functions, AI gateway, MCP | BaaS + AI gateway | TypeScript | Apache-2.0 |
| Supabase | Postgres platform with auth, storage, pgvector | BaaS | TypeScript | Apache-2.0 |
| PocketBase | Single-file backend with realtime DB | Embedded BaaS | Go | MIT |

## Quick start

```bash
# single-binary backend
./pocketbase serve
```
Use Postgres + pgvector (Supabase) when you need SQL and vectors together.

## Get the source

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/backend-infra
```

Paths:

- `stacks/backend-infra/butterbase`
- `stacks/backend-infra/supabase`
- `stacks/backend-infra/pocketbase`
