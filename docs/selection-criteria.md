# Selection Criteria

*Last checked: 2026-10-20*

A project is included when it:

1. **Has a licence file** that is OSI-approved open source, or clearly labelled source-available (BUSL, FSL, Elastic, fair-code). Licence notes are shown on every category page and in [Credits](credits.md). Repositories with no licence file are excluded.
2. **Is actively maintained** – commits within roughly the last 12 months, or a stable, widely used release.
3. **Is self-hostable** – runs on your own hardware or cloud without a mandatory vendor account.
4. **Fits a category** in the AI agent / LLM stack, and is useful on its own or alongside the other stacks.
5. **Speaks open interfaces** where possible (OpenAI-compatible API, MCP, standard databases).

Each project is pinned as a git submodule at its upstream default-branch HEAD on the last-checked date. Run `python scripts/sync_gitlinks.py --update` to refresh the pins.
