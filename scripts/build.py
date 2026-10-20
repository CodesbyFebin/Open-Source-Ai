"""Regenerate .gitmodules, docs/stacks/*, README.md and CREDITS.md from catalog.json."""
import json,os
c=json.load(open("catalog.json"));D=c["last_checked"];SITE="https://codesbyfebin.github.io/Open-Source-Ai/"
cats=c["categories"]
with open(".gitmodules","w") as g:
  for cat in cats:
    for it in cat["items"]:
      p=f"stacks/{cat['id']}/{it[1]}"
      g.write(f'[submodule "{p}"]\n\tpath = {p}\n\turl = https://github.com/{it[0]}.git\n\tshallow = true\n')
GUIDE=json.load(open("scripts/quickstarts.json"))
os.makedirs("docs/stacks",exist_ok=True)
for f in os.listdir("docs/stacks"): os.remove("docs/stacks/"+f)
for cat in cats:
  k=cat["id"];c1,c2=cat["cols"]
  rows="\n".join(f"| {it[2]} | {it[3]} | {it[5]} | {it[6]} | {it[4]} |" for it in cat["items"])
  paths="\n".join(f"- `stacks/{k}/{it[1]}`" for it in cat["items"])
  open(f"docs/stacks/{k}.md","w").write(f"""---
title: {cat['title']} – Open Source Ai
description: {cat['desc']} Open-source {cat['title'].lower()} compared, with install guides – CodesbyFebin Open Source Ai.
---
# {cat['title']}

{cat['desc']}

*Last checked: {D}*

## Comparison

| Project | What it does | {c1} | {c2} | Licence |
|---|---|---|---|---|
{rows}

## Quick start

{GUIDE[k]}

## Get the source

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/{k}
```

Paths:

{paths}
""")
  os.makedirs(f"stacks/{k}",exist_ok=True)
  open(f"stacks/{k}/README.md","w").write(f"# {cat['title']}\n\n{cat['desc']}\n\nDocs: {SITE}stacks/{k}/\n\nFetch: `git submodule update --init --depth 1 stacks/{k}`\n")
total=sum(len(x["items"]) for x in cats)
tbl="\n".join(f"| [{x['title']}](stacks/{x['id']}.md) | {x['desc']} | {len(x['items'])} |" for x in cats)
open("docs/index.md","w").write(f"""---
title: Open Source Ai – All Open-Source AI Agent & LLM Stacks in One Repo
description: CodesbyFebin Open Source Ai is a free, categorised hub of {total} open-source LLM gateways, chat UIs, local models, agents, RAG, memory and observability stacks.
---
# Open Source Ai

**One repo. Every open-source stack for AI agents and LLMs.** Curated and categorised by **CodesbyFebin**.

*{total} projects in {len(cats)} categories · last checked {D}*

| Category | What it covers | Projects |
|---|---|---|
{tbl}

- New here? [Getting Started](guides/getting-started.md)
- Want a working stack in 10 minutes? [Build a Full Stack](guides/full-stack.md)
- How projects are chosen: [Selection Criteria](selection-criteria.md)
""")
rtbl="\n".join(f"| [{x['title']}](docs/stacks/{x['id']}.md) | {x['desc']} | {len(x['items'])} |" for x in cats)
open("README.md","w").write(f"""<p align="center"><img src="docs/assets/favicon.svg" width="96" alt="Open Source Ai logo"></p>

# Open Source Ai by CodesbyFebin

**All open-source AI agent & LLM stacks in one repository**: LLM gateways and routers, free LLM APIs, chat UIs, local models, inference servers, memory, agent frameworks, coding agents, AI code review, RAG and vector databases, evaluation and observability, backends and app templates.

📖 **Docs:** {SITE} · {total} projects · {len(cats)} categories · last checked {D}

| Category | What it covers | Projects |
|---|---|---|
{rtbl}

## Quick start

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
git submodule update --init --depth 1 stacks/code-review   # one category
docker compose -f examples/full-stack/docker-compose.yml up -d   # local AI stack
```

Guides: [Getting Started](docs/guides/getting-started.md) · [Build a Full Stack](docs/guides/full-stack.md) · [Selection Criteria](docs/selection-criteria.md)

## Contributing

Edit `catalog.json`, run `python scripts/build.py` and `python scripts/sync_gitlinks.py`, then open a PR. CI checks catalog, `.gitmodules` and gitlinks agree.

## License

Hub content: [MIT](LICENSE) © CodesbyFebin. Each project under `stacks/` keeps its own licence – see [CREDITS.md](CREDITS.md).
""")
cr=f"# Credits & Licences\n\nOpen Source Ai's own content (docs, scripts, curation) is MIT-licensed © CodesbyFebin. Each project under `stacks/` is a git submodule pointing at its original repository, unmodified, under its own licence. Licences were read from each upstream LICENSE file on {D}; always check upstream before use.\n\n| Project | Upstream | Licence |\n|---|---|---|\n"+"\n".join(f"| {it[2]} | https://github.com/{it[0]} | {it[4]} |" for x in cats for it in x["items"])+"\n"
open("CREDITS.md","w").write(cr);open("docs/credits.md","w").write(cr)
nav="\n".join(f"      - {x['title']}: stacks/{x['id']}.md" for x in cats)
m=open("mkdocs.yml").read().split("nav:")[0]
open("mkdocs.yml","w").write(m+f"""nav:
  - Home: index.md
  - Guides:
      - Getting Started: guides/getting-started.md
      - Build a Full Stack: guides/full-stack.md
      - Connect to a Gateway: guides/connect-gateway.md
  - Selection Criteria: selection-criteria.md
  - Stacks:
{nav}
  - Credits & Licences: credits.md
""")
print("built",total)
