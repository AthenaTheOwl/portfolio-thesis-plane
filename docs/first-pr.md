# First PR

The literal first PR after this scaffold. The goal is the registry,
the rubric, and the schemas — no scoring runtime, no signal ingest,
no hand-computed week yet.

## Files this PR adds

- `schemas/repo-entry.schema.json`
  - JSON Schema draft 2020-12
  - Required: `slug`, `name`, `thesis_statement`, `created_at`,
    `current_verdict`
  - `current_verdict` enum: `ATTEND`, `FREEZE`, `RETIRE`,
    `unscored`
- `schemas/score.schema.json`
  - Required: `repo_slug`, `iso_week`, `factor_scores`, `total`,
    `verdict`
  - `factor_scores` is an object with one key per rubric factor,
    each value 0..4
- `schemas/card.schema.json`
  - Wrapper schema for the per-repo card's front-matter
- `schemas/rollup.schema.json`
  - Front-matter schema for the weekly roll-up; enforces exactly
    2 ATTEND and exactly 3 RETIRE
- `registry/repos.yaml`
  - One entry per portfolio repo (the ~20 in the active set)
  - `current_verdict: unscored` for every entry; the calibration
    week will fill these in
- `rubric/thesis-alive.yaml`
  - Five factors: `model-release-impact`, `oss-competition`,
    `paper-drift`, `recent-run-evidence`, `decision-freshness`
  - Per-factor `rules`: an array of `{ score: 0..4, condition: ... }`
- `decisions/DEC-PTP-001-rubric-closure.md`
  - Justifies the five-factor closure
  - Names the forced-verdict mechanic and why it is the point
  - Lists factors considered and deferred (e.g., revenue, user
    interest)
- `scripts/validate_schemas.py`
- `scripts/validate_registry.py`
- `scripts/validate_rubric.py`

## Verification

```
python -m pytest        # no tests yet; runner exits clean
python scripts/validate_schemas.py
python scripts/validate_registry.py
python scripts/validate_rubric.py
```

All four exit zero. The registry validates. The rubric validates.

## What this PR does not do

- No hand-computed week. PR 2 lands the 2026-W25 calibration.
- No scorer or renderer code. PR 3 lands the skeletons.
- No CLI entry point.
- No voice-lint script. That lands in PR 2.
