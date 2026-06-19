# Acceptance — 0001 Foundation

"v0 done" means the following hold simultaneously.

## Artifacts present

- `schemas/repo-entry.schema.json` validates
- `schemas/score.schema.json` validates
- `schemas/card.schema.json` and `schemas/rollup.schema.json`
  validate
- `registry/repos.yaml` lists all ~20 portfolio repos with a
  thesis statement each
- `rubric/thesis-alive.yaml` declares the five factors with 0..4
  scoring rules
- `reports/2026-W25/<slug>.md` exists for every repo in the
  registry
- `reports/2026-W25/_rollup.md` exists and names the forced top-2
  ATTEND and bottom-3 RETIRE
- `decisions/DEC-PTP-001-rubric-closure.md` exists

## Gates pass

Run from the repo root:

```
python -m pytest
python scripts/voice_lint.py
python scripts/validate_schemas.py
python scripts/validate_registry.py
python scripts/validate_rubric.py
python scripts/validate_decisions.py
```

All six exit zero.

## Manual review

- The roll-up has exactly two ATTEND repos and exactly three RETIRE
  repos. No "needs more thought" entries.
- Each per-repo card names the five factor sub-scores and the
  total, plus a one-line evidence trail per factor.
- The DEC justifies the closure to five factors and explains the
  forced-verdict mechanic.

## Out of v0 acceptance

- The scorer and renderer modules ship as skeletons. The 2026-W25
  cards are hand-computed; the CLI does not yet reproduce them.
  Auto-reproduction is spec 0003.
- Live signal ingest is spec 0003.
- Cross-week verdict-followthrough regression is spec 0004.
