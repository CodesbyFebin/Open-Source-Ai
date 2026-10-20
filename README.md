<p align="center"><img src="docs/assets/favicon.svg" width="96" alt="Open Source Ai logo"></p>

# Open Source Ai by CodesbyFebin

**All open-source AI agent & LLM stacks in one repository**: LLM gateways and routers, free LLM APIs, chat UIs, local models, inference servers, memory, agent frameworks, coding agents, AI code review, RAG and vector databases, evaluation and observability, backends and app templates.

📖 **Docs:** https://codesbyfebin.github.io/Open-Source-Ai/ · 70 projects · 14 categories · last checked 2026-10-20

| Category | What it covers | Projects |
|---|---|---|
| [Gateways & LLM Routing](docs/stacks/gateways-routing.md) | OpenAI-compatible gateways, routers, guardrail firewalls and free-LLM aggregators. | 6 |
| [Chat UIs](docs/stacks/chat-ui.md) | Self-hosted ChatGPT-style interfaces. | 4 |
| [Local Models & Runtimes](docs/stacks/local-models.md) | Run LLMs on your own laptop or server. | 6 |
| [Inference & Serving](docs/stacks/inference-serving.md) | High-throughput production model serving on GPUs. | 4 |
| [Memory](docs/stacks/memory.md) | Long-term memory layers for agents and assistants. | 4 |
| [Agent Frameworks](docs/stacks/agent-frameworks.md) | Libraries for building single and multi-agent systems. | 7 |
| [Coding Agents](docs/stacks/coding-agents.md) | AI pair programmers and autonomous software agents. | 5 |
| [Code Review](docs/stacks/code-review.md) | Automated AI pull-request review. | 2 |
| [Low-code App Builders](docs/stacks/app-builders.md) | Visual builders for LLM apps, agents and workflows. | 4 |
| [RAG & Vector Databases](docs/stacks/rag-vector-db.md) | Retrieval frameworks, document pipelines and vector stores. | 7 |
| [Evaluation & Observability](docs/stacks/eval-observability.md) | Tracing, evaluations and prompt management. | 4 |
| [Backend & Infra](docs/stacks/backend-infra.md) | Backends, databases and auth for AI products. | 3 |
| [App Templates & Examples](docs/stacks/app-templates.md) | Ready-made AI apps and examples to copy. | 1 |
| [CodesbyFebin Collection](docs/stacks/codesbyfebin-collection.md) | Hand-picked agent tools, MCP servers and experiments. | 13 |

## Quick start

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/code-review   # one category
docker compose -f examples/full-stack/docker-compose.yml up -d   # local AI stack
```

Guides: [Getting Started](docs/guides/getting-started.md) · [Build a Full Stack](docs/guides/full-stack.md) · [Selection Criteria](docs/selection-criteria.md)

## Contributing

Edit `catalog.json`, run `python scripts/build.py` and `python scripts/sync_gitlinks.py`, then open a PR. CI checks catalog, `.gitmodules` and gitlinks agree.

## License

Hub content: [MIT](LICENSE) © CodesbyFebin. Each project under `stacks/` keeps its own licence – see [CREDITS.md](CREDITS.md).
