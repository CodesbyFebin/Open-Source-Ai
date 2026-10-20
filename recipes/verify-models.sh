#!/usr/bin/env bash
# Verify pulled Ollama models match the manifest digests pinned in models.lock.
# Ollama pulls by tag; tags can be re-pointed upstream, so we fail on mismatch.
# Usage: verify-models.sh <compose-dir>   (reads <compose-dir>/models.lock: "<name>:<tag> sha256:<hex>")
set -euo pipefail
dir="$1"; fail=0
while read -r model digest; do
  [ -z "$model" ] || [ "${model:0:1}" = "#" ] && continue
  name="${model%%:*}"; tag="${model#*:}"
  actual="sha256:$(docker compose --project-directory "$dir" exec -T ollama sh -c "sha256sum /root/.ollama/models/manifests/registry.ollama.ai/library/$name/$tag" | cut -c1-64)"
  if [ "$actual" = "$digest" ]; then echo "OK   $model $actual"; else echo "FAIL $model expected $digest got $actual"; fail=1; fi
done < "$dir/models.lock"
exit $fail
