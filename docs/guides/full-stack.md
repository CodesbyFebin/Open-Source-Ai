# How-to: Build a Full Open-Source AI Stack
1. **Model** – `ollama run llama3.2` (local) or `vllm serve <model>` (GPU).
2. **Gateway** – run LiteLLM / Bifrost / FreeLLMAPI and register the model; one OpenAI-compatible endpoint for everything.
3. **Chat UI** – Open WebUI or LibreChat pointed at the gateway.
4. **Memory** – mem0 / OpenMemory for persistent user memory.
5. **RAG** – Qdrant or Chroma + LlamaIndex for your documents.
6. **Agents** – CrewAI / LangGraph / smolagents using the gateway URL.
7. **Observability** – Langfuse or Phoenix tracing every call.
8. **Coding** – Aider / Continue / OpenHands on the same gateway.

```bash
export OPENAI_BASE_URL=http://localhost:4000/v1
export OPENAI_API_KEY=sk-local
```
