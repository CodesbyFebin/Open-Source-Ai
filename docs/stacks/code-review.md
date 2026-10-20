---
title: Code Review – Open Source Ai
description: Automated AI code review. Curated open-source code review stacks in CodesbyFebin Open Source Ai.
---
# Code Review

Automated AI code review.

## Quick start

Wire an AI reviewer into CI as a GitHub Action on `pull_request` events, using your gateway key as a secret.

## Get the code

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/code-review
```

## Stacks

| Project | Path | License |
|---|---|---|
| [open-code-review](https://github.com/alibaba/open-code-review) | `stacks/code-review/open-code-review` | Apache-2.0 |
| [pr-agent](https://github.com/qodo-ai/pr-agent) | `stacks/code-review/pr-agent` | MIT |
