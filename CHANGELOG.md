# Changelog

Catalog changes are recorded here. Evidence refreshes are listed by their pull request.

## Unreleased

- Upstream link check moved to its own workflow: checks all 140 unique upstream repo/licence/setup URLs plus docs links with a GitHub token, publishes a report artifact, and opens/updates an issue on scheduled failures (still non-blocking).
- Ollama models pinned by manifest digest (`recipes/*/models.lock`), verified after pull; all GitHub Actions pinned to commit SHAs.
- Added Licence Review Worksheet (`docs/licence-review.md`) for the 15 needs-review entries.

- Licences: 15 projects now `needs-review`, each with a recorded `review_reason` (adds Phoenix, Trylon Gateway, llamafile and three AgentDomains repos: source-available or undetected). OpenMemory and PR-Agent re-verified as MIT from their LICENSE files.
- Collector: failed / rate-limited lookups are reported as failed and keep previous evidence; records `moved` and `fetch_status`. Validator: moved repo and GitHub licence mismatch are errors; zone-aware date checks.
- Unit tests (collector, validator, build) and Playwright browser tests (Chromium + WebKit, desktop and iPhone 13 emulation, axe-core).
- Search page: URL state (reload/back/forward), clear button, no-results message, archived badge, focus styles.
- Recipes: pinned images; local-chat smoke test now proves the reply came from the model; agent-memory-eval end-to-end CI workflow.
- Refresh workflow: optional GitHub App token, minimal permissions.

- Merged first evidence refresh (PR #1): 70 projects collected, 2 archived upstream (Flowise, Text Generation Inference).
- Corrected licences from upstream LICENSE files: OpenMemory Apache-2.0 → MIT, PR-Agent AGPL-3.0 → MIT.

## 2026-10-21 – Catalog-first release

- Converted the repository from git submodules to a catalog: removed `.gitmodules` and all 70 gitlinks; upstream code is no longer referenced as bundled.
- New single source of truth `catalog/projects.yaml` with JSON Schema validation; README, category pages, credits and search data are generated.
- Updated canonical URLs for 7 moved repositories (LibreChat, llamafile, Lobe Chat, OpenCode, OpenHands, PR-Agent, Text Generation WebUI).
- Licences: 9 custom/multi-licence projects marked *needs review* instead of a single SPDX id.
- Added weekly evidence refresh (pull-request based), freshness report, search & filter page, two recipes (one CI-tested), issue forms and PR checklist.

## 2026-10-20 – Initial hub

- 14 categories, 70 projects.
