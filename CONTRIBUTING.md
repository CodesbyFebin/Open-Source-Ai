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

## Verifying facts

- **Licence:** open the upstream LICENSE file (not just GitHub's badge). Use `state: declared` only for a single standard SPDX licence; otherwise `state: needs-review` with a `review_reason` explaining why (custom terms, multiple licences, source-available, undetected).
- **Repository state:** comes only from `catalog/evidence/`. If validation reports `repo moved`, update `repo:` in `projects.yaml` to the canonical URL.
- **Archived projects** stay in the catalog and are labelled; don't delete them without a CHANGELOG entry.
- **Recipes:** `tested` only when a smoke test passes in CI; say what was tested, versions and environment.

## Tests

```bash
python -m pytest -q tests                      # unit tests
mkdocs build --strict -d _site/Open-Source-Ai
cd tests/browser && npm ci && npx playwright install chromium webkit && npx playwright test
./recipes/local-chat/smoke.sh                  # needs Docker
```

## Maintainer one-time setup (not done automatically)

These settings are documented here and must be applied by a repository admin.

### Branch protection for `main`

Settings → Branches → Add rule for `main`:

- Require a pull request before merging (1 approval)
- Require status checks: `Catalog integrity`, `Docs build + internal links`, `Browser tests (Playwright, desktop + iPhone 13 emulation)`, `Recipe smoke test – local-chat`
- Do **not** require `Upstream links (non-blocking)` or `Recipe – agent-memory-eval` (network-dependent / heavier)
- Do not allow bypass for the bot

### Evidence refresh PRs and CI

PRs created with the default `GITHUB_TOKEN` **do not trigger** other workflows (a GitHub safety rule), so CI will not start on `bot/evidence-refresh` by itself.

**Option A – GitHub App (recommended):**

1. Settings → Developer settings → GitHub Apps → New. Permissions: *Contents: read & write*, *Pull requests: read & write*. No webhook.
2. Install it on this repository only.
3. Add repository variable `OSA_APP_ID` (the App ID) and secret `OSA_APP_PRIVATE_KEY` (the generated private key).
4. The refresh workflow then uses `actions/create-github-app-token` and CI starts automatically on its PRs.

**Option B – manual fallback (no setup):** open the PR, then either close and reopen it, or run *CI* via *Actions → CI → Run workflow* on the `bot/evidence-refresh` branch. Merge only when blocking checks are green.

The refresh job never pushes to `main`, uses no `pull_request_target`, and the collection step runs before any write token is minted.
