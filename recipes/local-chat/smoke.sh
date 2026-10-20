#!/usr/bin/env bash
# Smoke test: model -> gateway -> chat UI. CPU only, ~0.4 GB model, no paid APIs.
# Proves the reply came from the local model: arithmetic answer, token usage, model
# reported by the gateway, and Ollama's own log/ps showing the request and loaded model.
set -euo pipefail
cd "$(dirname "$0")"
export LITELLM_MASTER_KEY="${LITELLM_MASTER_KEY:-sk-ci-$RANDOM$RANDOM}"
cleanup() { status=$?; [ $status -ne 0 ] && docker compose logs --tail 80 || true; [ "${KEEP:-0}" = 1 ] || docker compose down -v >/dev/null 2>&1 || true; exit $status; }
trap cleanup EXIT
start=$(date +%s)
docker compose config --quiet
docker compose up -d
docker compose wait model-pull
../verify-models.sh .
for i in $(seq 1 60); do curl -fsS http://localhost:4000/health/liveliness >/dev/null 2>&1 && break; sleep 5; done
resp=$(curl -fsS http://localhost:4000/v1/chat/completions -H "Authorization: Bearer $LITELLM_MASTER_KEY" -H 'Content-Type: application/json' \
  -d '{"model":"local-llama","temperature":0,"messages":[{"role":"user","content":"What is 17 plus 25? Answer with the number only."}],"max_tokens":20}')
echo "$resp" | python3 -c '
import json,sys
r=json.load(sys.stdin); c=r["choices"][0]["message"]["content"]; u=r.get("usage") or {}
print("gateway model:", r.get("model"), "| reply:", repr(c), "| usage:", u)
assert "42" in c, "model did not answer 17+25"
assert u.get("completion_tokens",0)>0, "no completion tokens reported"
assert "qwen2.5" in (r.get("model") or "") or r.get("model")=="local-llama", "unexpected model"'
docker compose exec -T ollama ollama ps | tee /tmp/ollama-ps.txt
grep -q "qwen2.5:0.5b" /tmp/ollama-ps.txt || { echo "model not loaded in Ollama"; exit 1; }
docker compose logs ollama 2>&1 | grep -E 'POST +"/api/chat"|POST +"/v1/chat/completions"|POST +"/api/generate"' | tail -2 | tee /tmp/ollama-req.txt
[ -s /tmp/ollama-req.txt ] || { echo "no chat request in Ollama logs"; exit 1; }
for i in $(seq 1 60); do curl -fsS http://localhost:3000/health >/dev/null 2>&1 && break; sleep 5; done
curl -fsS http://localhost:3000/health && echo " open-webui healthy"
docker compose images
docker compose exec -T ollama ollama list
echo "elapsed $(( $(date +%s) - start ))s"
echo "SMOKE TEST PASSED"
