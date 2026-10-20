---
title: RAG & Vector Databases – Open Source Ai
description: Retrieval frameworks, document pipelines and vector stores. Open-source rag & vector databases compared, with install guides – CodesbyFebin Open Source Ai.
---
# RAG & Vector Databases

Retrieval frameworks, document pipelines and vector stores.

*Last checked: 2026-10-20*

## Comparison

| Project | What it does | Type | Language | Licence |
|---|---|---|---|---|
| LlamaIndex | Data framework for RAG | Framework | Python | MIT |
| Haystack | Production RAG pipelines | Framework | Python | Apache-2.0 |
| RAGFlow | Deep-document-understanding RAG engine | Engine + UI | Python | Apache-2.0 |
| Qdrant | Vector search engine | Vector DB | Rust | Apache-2.0 |
| Chroma | Embedding database | Vector DB (embedded) | Rust/Python | Apache-2.0 |
| Milvus | Cloud-native vector database | Vector DB (scale) | Go | Apache-2.0 |
| Weaviate | Vector DB with hybrid search | Vector DB (hybrid) | Go | BSD-3-Clause (core) |

## Quick start

```bash
docker run -d -p 6333:6333 qdrant/qdrant
pip install llama-index llama-index-vector-stores-qdrant
```
Index documents with LlamaIndex or Haystack into the vector store.

## Get the source

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/rag-vector-db
```

Paths:

- `stacks/rag-vector-db/llama-index`
- `stacks/rag-vector-db/haystack`
- `stacks/rag-vector-db/ragflow`
- `stacks/rag-vector-db/qdrant`
- `stacks/rag-vector-db/chroma`
- `stacks/rag-vector-db/milvus`
- `stacks/rag-vector-db/weaviate`
