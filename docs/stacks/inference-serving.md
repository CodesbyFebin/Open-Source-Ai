---
title: Inference & Serving – Open Source Ai
description: High-throughput production model serving. Curated open-source inference & serving stacks in CodesbyFebin Open Source Ai.
---
# Inference & Serving

High-throughput production model serving.

## Quick start

On a GPU host: `pip install vllm && vllm serve meta-llama/Llama-3.1-8B-Instruct` exposes `/v1` on port 8000.

## Get the code

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/inference-serving
```

## Stacks

| Project | Path | License |
|---|---|---|
| [vllm](https://github.com/vllm-project/vllm) | `stacks/inference-serving/vllm` | Apache-2.0 |
| [sglang](https://github.com/sgl-project/sglang) | `stacks/inference-serving/sglang` | Apache-2.0 |
| [text-generation-inference](https://github.com/huggingface/text-generation-inference) | `stacks/inference-serving/text-generation-inference` | Apache-2.0 |
| [server](https://github.com/triton-inference-server/server) | `stacks/inference-serving/server` | BSD-3-Clause |
