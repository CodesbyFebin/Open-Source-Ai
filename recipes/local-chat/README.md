# Local private chat: Ollama + LiteLLM + Open WebUI

**Data flow:** browser → Open WebUI (:3000) → LiteLLM gateway (:4000, OpenAI-compatible) → Ollama (:11434) → local model. Nothing leaves your machine after the first image/model download.

## Requirements

| | Minimum (tested) | For bigger models |
|---|---|---|
| CPU / RAM | 4 vCPU, 8 GB RAM | 16 GB+ RAM, NVIDIA GPU or Apple Silicon |
| Disk | ~8 GB (images + 0.4 GB model) | 25 GB+ |
| Software | Docker 24+ with Compose v2 | – |
| Network | Internet for first pull only | – |

No accounts or paid API keys are needed.

## Run

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai/recipes/local-chat
export LITELLM_MASTER_KEY=sk-$(openssl rand -hex 12)   # never commit real keys
docker compose up -d
docker compose wait model-pull
```

Environment variables: `LITELLM_MASTER_KEY` (gateway key, default is a placeholder), `MODEL` (Ollama model, default `qwen2.5:0.5b`; also change `litellm-config.yaml`).

## Verify

```bash
./smoke.sh     # same test CI runs
# or manually
curl -H "Authorization: Bearer $LITELLM_MASTER_KEY" -H 'Content-Type: application/json' \
  http://localhost:4000/v1/chat/completions \
  -d '{"model":"local-llama","messages":[{"role":"user","content":"Say hi"}]}'
```

Open http://localhost:3000, create the first (admin) account and pick `local-llama`.

## Clean up

```bash
docker compose down        # keep data
docker compose down -v     # also delete models and chats
```

## Known limitations

- `qwen2.5:0.5b` is a tiny model chosen so CI can run on CPU; answers are low quality. Use a 3B–8B model for real use.
- Images use moving tags (`latest`, `main`, `main-stable`); the exact digests tested are in the CI log.
