#!/usr/bin/env bash
# End-to-end: services up -> store memories (session 1) -> restart Qdrant -> new process
# recalls them (session 2) -> promptfoo asserts the agent's answers use the memories.
set -euo pipefail
cd "$(dirname "$0")"
cleanup() { status=$?; [ $status -ne 0 ] && docker compose logs --tail 60 || true; [ "${KEEP:-0}" = 1 ] || docker compose down -v >/dev/null 2>&1 || true; exit $status; }
trap cleanup EXIT
start=$(date +%s)
docker compose config --quiet
docker compose up -d
docker compose wait model-pull
../verify-models.sh .
for i in $(seq 1 30); do curl -fsS http://localhost:6333/readyz >/dev/null 2>&1 && break; sleep 2; done
python agent.py remember "My favourite programming language is Rust."
python agent.py remember "I live in Lisbon, Portugal."
echo "--- restarting qdrant to prove persistence"
docker compose restart qdrant
for i in $(seq 1 30); do curl -fsS http://localhost:6333/readyz >/dev/null 2>&1 && break; sleep 2; done
out=$(python agent.py recall "favourite programming language")
echo "session 2 recall: $out"
echo "$out" | grep -qi rust || { echo "memory not recalled after restart"; exit 1; }
npx --yes promptfoo@0.124.1 eval --no-cache --no-progress-bar -o /tmp/promptfoo.json
python3 -c 'import json;r=json.load(open("/tmp/promptfoo.json"))["results"]["stats"];print("promptfoo", r);assert r["failures"]==0 and r["successes"]>=2'
docker compose images
echo "elapsed $(( $(date +%s) - start ))s"
echo "SMOKE TEST PASSED"
