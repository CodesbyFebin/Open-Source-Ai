#!/usr/bin/env bash
# Smoke test: model -> gateway -> chat UI. Safe for CI (~0.4 GB model, CPU only, no paid APIs).
set -euo pipefail
cd "$(dirname "$0")"
export LITELLM_MASTER_KEY="${LITELLM_MASTER_KEY:-sk-ci-$(date +%s)}"
docker compose config --quiet
docker compose up -d
trap 'docker compose logs --tail 50 || true' ERR
echo "waiting for model pull"; docker compose wait model-pull
for i in $(seq 1 60); do curl -fsS http://localhost:4000/health/liveliness >/dev/null 2>&1 && break; sleep 5; done
resp=$(curl -fsS http://localhost:4000/v1/chat/completions -H "Authorization: Bearer $LITELLM_MASTER_KEY" -H 'Content-Type: application/json' \
  -d '{"model":"local-llama","messages":[{"role":"user","content":"Reply with the word ok"}],"max_tokens":10}')
echo "$resp" | python3 -c 'import json,sys; c=json.load(sys.stdin)["choices"][0]["message"]["content"]; assert c.strip(), "empty"; print("gateway reply:", c)'
for i in $(seq 1 60); do curl -fsS http://localhost:3000/health >/dev/null 2>&1 && break; sleep 5; done
curl -fsS http://localhost:3000/health && echo " open-webui healthy"
docker compose images
echo "SMOKE TEST PASSED"
