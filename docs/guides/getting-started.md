# Getting Started

Open Source Ai is a catalog: it links to upstream projects instead of bundling them.

1. **Find projects** – use [Search & Filter](../catalog.md) or browse a category in the navigation.
2. **Check fit** – each project's detail section lists deployment, hardware, licence (with evidence link) and activity.
3. **Install from upstream** – follow the project's linked setup docs, or clone only what you need:
   ```bash
   git clone --depth 1 https://github.com/ollama/ollama
   ```
4. **Compose a stack** – start from a [recipe](../recipes/index.md):
   ```bash
   git clone https://github.com/CodesbyFebin/Open-Source-Ai-Full-Stack
   cd Open-Source-Ai-Full-Stack/recipes/local-chat && docker compose up -d
   ```
