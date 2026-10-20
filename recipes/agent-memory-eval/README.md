# Agent with persistent memory and evaluation: Ollama + Mem0 + Qdrant + promptfoo

**Data flow:** `agent.py remember` → Mem0 → Ollama embeddings → Qdrant · `agent.py ask` → Mem0 search (Qdrant) → Ollama chat with retrieved facts · promptfoo runs `agent.py ask` and asserts on the answers.

## Pinned versions

| Component | Version |
|---|---|
| Ollama | `ollama/ollama:0.40.6` |
| Qdrant | `qdrant/qdrant:v1.19.2` |
| Mem0 | `mem0ai==2.2.1` (see `requirements.txt`) |
| promptfoo | `promptfoo@0.124.1` |
| Models | `qwen2.5:1.5b` (~1 GB), `nomic-embed-text:v1.5` (~0.3 GB) |

Model digests are pinned in `models.lock`; `smoke.sh` runs `../verify-models.sh` after the pull and fails if the tag now points to different weights. To update, pull the new tag, record its digest and say so in CHANGELOG.

## Requirements

- Docker 24+ with Compose v2, Python 3.10+, Node.js 22.22+ (promptfoo 0.124 requirement)
- 4 vCPU, 8 GB RAM, ~6 GB disk; no GPU needed. Cold start ~3–5 minutes (image + model pulls).

## Run

```bash
cd Open-Source-Ai/recipes/agent-memory-eval
python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
./smoke.sh          # full end-to-end test (cleans up on exit; KEEP=1 to keep containers)
```

Or step by step:

```bash
docker compose up -d && docker compose wait model-pull
python agent.py remember "My favourite programming language is Rust."
docker compose restart qdrant              # memory survives the restart
python agent.py recall "favourite language"
python agent.py ask "Which programming language does the user prefer?"
npx promptfoo@0.124.1 eval
```

`remember` stores facts verbatim (`infer=False`) so the test is deterministic; set `INFER=1` to let the LLM extract facts (less reliable with small models).

## Clean up

```bash
docker compose down -v && rm -rf .venv
```

## Known limitations

- Tests memory storage, persistence across a Qdrant restart and a new process, and that answers use stored facts. Does not test Mem0's LLM-based fact extraction, multi-user isolation or tool use.
- Small models can phrase answers unexpectedly; assertions only check for the key word.
