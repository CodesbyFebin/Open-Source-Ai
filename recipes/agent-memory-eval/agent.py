"""Minimal agent with long-term memory. Untested recipe – see README."""
import sys
from mem0 import Memory
from openai import OpenAI

MODEL = "qwen2.5:1.5b"
memory = Memory.from_config({
    "llm": {"provider": "ollama", "config": {"model": MODEL, "ollama_base_url": "http://localhost:11434"}},
    "embedder": {"provider": "ollama", "config": {"model": "nomic-embed-text", "ollama_base_url": "http://localhost:11434"}},
    "vector_store": {"provider": "qdrant", "config": {"host": "localhost", "port": 6333, "embedding_model_dims": 768}},
})
llm = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def chat(user_id: str, text: str) -> str:
    facts = "\n".join(m["memory"] for m in memory.search(text, user_id=user_id).get("results", []))
    reply = llm.chat.completions.create(model=MODEL, messages=[
        {"role": "system", "content": f"Known facts about the user:\n{facts or 'none'}"},
        {"role": "user", "content": text}]).choices[0].message.content
    memory.add([{"role": "user", "content": text}, {"role": "assistant", "content": reply}], user_id=user_id)
    return reply

if __name__ == "__main__":
    print(chat("demo", " ".join(sys.argv[1:]) or "Hi, my favourite language is Python."))
