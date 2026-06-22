# Acceptance — 0002 Design

"spec 0002 done" means the following hold simultaneously.

## Artifacts present

- `scripts/voice_lint.py` exists and exits 0 on the current corpus.
- `scripts/validate_decisions.py` exists and exits 0 on the
  `decisions/` directory.
- `signals/2026-W26.yaml` exists and is curated against fresh
  signals (not a copy of 2026-W25).
- `reports/2026-W26/<slug>.md` exists for every repo in the
  registry.
- `reports/2026-W26/_rollup.md` exists and names a forced top-2
  ATTEND and bottom-3 RETIRE.
- `reports/2026-W26/_followthrough.md` exists and is hand-written.
- `data/ledger/2026-W26.jsonl` exists; one row per repo;
  `candidate_verdict` and `final_verdict` both populated.

## Gates pass

```
python -m pytest
python scripts/voice_lint.py
python scripts/validate_schemas.py
python scripts/validate_registry.py
python scripts/validate_rubric.py
python scripts/validate_decisions.py
```

All six exit zero. This matches the v0-acceptance gate list from
spec 0001.

## Manual review

- The 2026-W26 rollup is allowed to differ from 2026-W25 in which
  repos are named, but the mechanic is unchanged: exactly two
  ATTEND, exactly three RETIRE.
- The followthrough memo names at least one ATTEND repo from
  2026-W25 and what (if anything) happened to it. "Nothing" is a
  valid answer.
- The DEC gate refuses a deliberately broken DEC (no front-matter,
  bad id, missing `status`).
- The ledger row shape matches `design.md`. A row with
  `candidate_verdict == final_verdict` is the common case; a row
  where they differ is the load-bearing case the ledger exists to
  audit.
