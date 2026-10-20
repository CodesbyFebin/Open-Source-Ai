# How-to: Connect Any Tool to a Gateway
Every stack here speaks the OpenAI API. Set:
```bash
export OPENAI_BASE_URL=http://localhost:4000/v1
export OPENAI_API_KEY=<your gateway key>
```
In UIs (Open WebUI, Dify, Flowise) add a custom *OpenAI-compatible* provider with the same URL.
