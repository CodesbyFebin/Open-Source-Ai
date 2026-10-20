---
title: Code Review – Open Source Ai
description: Automated AI pull-request review. Open-source code review compared, with install guides – CodesbyFebin Open Source Ai.
---
# Code Review

Automated AI pull-request review.

*Last checked: 2026-10-20*

## Comparison

| Project | What it does | Runs as | Language | Licence |
|---|---|---|---|---|
| Open Code Review | Hybrid deterministic + LLM agent code reviewer with line-level comments | CLI / CI | Go | Apache-2.0 |
| PR-Agent | PR review, describe and improve commands | GitHub Action / app | Python | AGPL-3.0 |

## Quick start

Run a reviewer in CI on `pull_request` events, storing your gateway key as a repository secret. Each project's README shows the GitHub Action snippet.

## Get the source

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/code-review
```

Paths:

- `stacks/code-review/open-code-review`
- `stacks/code-review/pr-agent`
