# Contributing to Open Source Ai

Thanks for helping keep the catalog accurate.

## Source of truth

| File | Edited by | Purpose |
|---|---|---|
| `catalog/projects.yaml` | humans | curated project data (schema: `catalog/schema.json`) |
| `catalog/categories.yaml` | humans | categories |
| `catalog/quickstarts.json` | humans | per-category quick start |
| `catalog/evidence/*.json` | bot (weekly PR) | facts collected from the GitHub API |
| `recipes/*` | humans | composed stacks with test status |
| `README.md`, `CREDITS.md`, `docs/stacks`, `docs/recipes`, `docs/freshness.md`, `docs/assets/catalog.json`, `mkdocs.yml` nav | **generated** | do not edit by hand |

## Add or correct a project

```bash
pip install -r requirements.txt
# edit catalog/projects.yaml
python scripts/build.py
python scripts/validate.py
mkdocs serve   # preview at http://127.0.0.1:8000
```

Then open a pull request and complete the checklist. New projects need an evidence file: run `GITHUB_TOKEN=... python scripts/collect.py` or let the weekly refresh add it (validation will tell you).

## Licences

Upstream licences are authoritative. Use an SPDX id with `state: declared` only when the upstream LICENSE file is a single standard licence. Otherwise use `state: needs-review` and describe the terms in `label`. Report licence errors with the *Wrong metadata or licence* issue form.

## Evidence refresh

`.github/workflows/refresh.yml` runs weekly (Monday 03:00 UTC) and on demand. It only updates `catalog/evidence/` and regenerated pages, and always opens a pull request for review – it never pushes to `main`. Pull requests opened by the bot do not trigger CI automatically; a maintainer should run `python scripts/validate.py` on the branch (or re-run CI) before merging.
