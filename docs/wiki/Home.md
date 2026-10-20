> **Unpublished draft.** The GitHub wiki for this repository has not been initialised (its git remote returns "not found"). To publish: open the repo's **Wiki** tab, click *Create the first page*, paste everything below the line, and save as **Home**.

---

# Open Source Ai – Wiki

**Purpose.** Open Source Ai by CodesbyFebin is a curated, evidence-backed catalog of open-source and source-available projects for building AI agents and LLM apps. It contains metadata, comparisons and recipes – not upstream source code.

- **Search & filter:** https://codesbyfebin.github.io/Open-Source-Ai/catalog/
- **Docs site:** https://codesbyfebin.github.io/Open-Source-Ai/

## Selection criteria

Projects must have a licence file, be maintained or widely used, be self-hostable or usable as a library, and fit a catalog category. Full criteria: https://codesbyfebin.github.io/Open-Source-Ai/selection-criteria/

## Recipes

| Recipe | Status |
|---|---|
| Local private chat (Ollama + LiteLLM + Open WebUI) | tested in CI on every push |
| Agent with memory and evaluation (Ollama + Mem0 + Qdrant + promptfoo) | see https://codesbyfebin.github.io/Open-Source-Ai/recipes/ for current status |

## Contributing

1. Edit `catalog/projects.yaml` (never generated pages).
2. Run `python scripts/build.py && python scripts/validate.py && python -m pytest -q tests`.
3. Open a pull request and complete the checklist. Details: `CONTRIBUTING.md`.

## Licence caveat

The MIT licence covers only this repository's curation, docs and code. Every catalogued project is governed by its own upstream licence. Entries marked **needs review** have custom, multiple, source-available or undetected licences – read the upstream terms before use.

## Freshness

A workflow collects repository state, last commit, latest release and licence detection from the GitHub API every Monday 03:00 UTC and opens a pull request for human review. It is not real-time monitoring. Report: https://codesbyfebin.github.io/Open-Source-Ai/freshness/
