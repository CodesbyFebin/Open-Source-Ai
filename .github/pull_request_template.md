## What changed

<!-- e.g. added project X to memory; corrected licence of Y -->

## Review checklist

- [ ] I edited `catalog/*.yaml` / `recipes/*` only, not generated pages (README, docs/stacks, CREDITS)
- [ ] I ran `python scripts/build.py && python scripts/validate.py` and committed the regenerated files
- [ ] Every new or changed licence links to the upstream LICENSE file (evidence URL)
- [ ] Uncertain/custom licences use `state: needs-review`, never a guessed SPDX id
- [ ] Descriptions are original, factual and free of marketing claims
- [ ] Recipe changes: test status updated honestly (`tested` only with a passing smoke test)
- [ ] Added an entry under *Unreleased* in `CHANGELOG.md`
