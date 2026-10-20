# How-to: Run a Full Local AI Stack (Ollama + LiteLLM + Open WebUI)

A runnable example lives in [`examples/full-stack/`](https://github.com/CodesbyFebin/Open-Source-Ai/tree/main/examples/full-stack).

## Requirements

| | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB |
| Disk | 10 GB free | 25 GB |
| CPU/GPU | Any x86_64/arm64 CPU (1B model) | NVIDIA GPU or Apple Silicon for 7B+ |
| Software | Docker 24+ with Compose v2 | – |
| Network | Internet access for first image/model pull (~5 GB) | – |

No API keys or accounts are needed.

## Run it

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai/examples/full-stack
export LITELLM_MASTER_KEY=sk-$(openssl rand -hex 12)
docker compose config --quiet      # validate
docker compose up -d
docker compose logs -f model-pull  # wait for "success"
```

## Test it

```bash
curl http://localhost:11434/api/tags                       # Ollama is up
curl -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  http://localhost:4000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"local-llama","messages":[{"role":"user","content":"Say hi"}]}'
```

Open **http://localhost:3000**, create the first (admin) account and choose `local-llama`.

## Extend it

- **Bigger model:** `MODEL=llama3.1:8b docker compose up -d` and update `litellm-config.yaml`.
- **Memory / RAG / agents:** point any tool from the [stacks](../index.md) at `http://localhost:4000/v1` with your master key.
- **Observability:** add a Langfuse callback in `litellm-config.yaml`.

## Stop

```bash
docker compose down        # keep data
docker compose down -v     # also delete models and chats
```
