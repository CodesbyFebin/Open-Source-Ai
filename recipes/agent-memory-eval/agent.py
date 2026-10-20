"""Minimal agent with long-term memory (Mem0 + Qdrant) on a local Ollama model.

Usage:
  python agent.py remember "<fact>"   # store a fact for user 'demo'
  python agent.py recall "<query>"     # print stored memories matching the query
  python agent.py ask "<question>"     # answer using retrieved memories
"""
import os, sys
from mem0 import Memory
from openai import OpenAI

CHAT = os.environ.get("CHAT_MODEL", "qwen2.5:1.5b")
EMBED = os.environ.get("EMBED_MODEL", "nomic-embed-text:v1.5")
OLLAMA = os.environ.get("OLLAMA_URL", "http://localhost:11434")
USER = "demo"

memory = Memory.from_config({
    "llm": {"provider": "ollama", "config": {"model": CHAT, "ollama_base_url": OLLAMA, "temperature": 0}},
    "embedder": {"provider": "ollama", "config": {"model": EMBED, "ollama_base_url": OLLAMA}},
    "vector_store": {"provider": "qdrant", "config": {"host": "localhost", "port": 6333, "collection_name": "osa_demo", "embedding_model_dims": 768}},
})


def hits(q):
    r = memory.search(q, user_id=USER)
    return [m["memory"] for m in (r.get("results", r) if isinstance(r, dict) else r)]


def ask(q):
    facts = "\n".join(hits(q)) or "none"
    llm = OpenAI(base_url=OLLAMA + "/v1", api_key="ollama")
    return llm.chat.completions.create(model=CHAT, temperature=0, messages=[
        {"role": "system", "content": "Answer in one short sentence using only these facts about the user:\n" + facts},
        {"role": "user", "content": q}]).choices[0].message.content


if __name__ == "__main__":
    cmd, text = sys.argv[1], " ".join(sys.argv[2:])
    if cmd == "remember":
        # infer=False stores the fact verbatim (deterministic); infer=True lets the LLM extract facts
        print(memory.add([{"role": "user", "content": text}], user_id=USER, infer=os.environ.get("INFER", "0") == "1"))
    elif cmd == "recall":
        print("\n".join(hits(text)))
    elif cmd == "ask":
        print(ask(text))
