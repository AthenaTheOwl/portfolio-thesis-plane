# System Map — Portfolio Thesis Plane

How the pieces fit together. This is the page to open when something
is confusing and the question is "wait, what reads what?"

## The five surfaces

```
+-------------------+      +---------------------+      +-------------------+
| registry/         |      | signals/<week>.yaml |      | rubric/           |
|   repos.yaml      |      | (per-repo per-factor|      |   thesis-alive    |
|                   |      |  sub-scores 0..4 +  |      |   .yaml           |
| 20 repos w/       |      |  evidence lines)    |      |                   |
| thesis statements |      +----------+----------+      | 5 factors x 5     |
+---------+---------+                 |                 | rules each (0..4) |
          |                           |                 +---------+---------+
          |                           |                           |
          v                           v                           v
       +--+----------------------------------------------------+
       |             src/portfolio_thesis_plane/               |
       |                                                       |
       |  loader.py  -> read registry + rubric + signals       |
       |  score.py   -> factor-score sum, candidate verdict    |
       |  scorer.py  -> (kept; original name for back-compat)  |
       |  report.py  -> render one Markdown card               |
       |  renderer.py-> (kept; original name for back-compat)  |
       |  ledger.py  -> append one JSONL row per (week, repo)  |
       |  cli.py     -> argparse entry, subcommands            |
       |  __main__.py-> `python -m portfolio_thesis_plane ...` |
       +--+----------------------------------+-----------------+
          |                                  |
          v                                  v
+---------+-----------------+    +-----------+-----------------+
| reports/<iso-week>/       |    | data/ledger/<iso-week>.jsonl|
|   <slug>.md   (20)        |    |   one row per (week, repo)  |
|   _rollup.md   (1)        |    |   audit trail, append-only  |
+---------------------------+    +-----------------------------+
```

## Data flow

1. The CLI is invoked: `python -m portfolio_thesis_plane generate
   --week 2026-W25`.
2. `loader.load_registry()` reads `registry/repos.yaml` into a list of
   typed entries.
3. `loader.load_signals(week)` reads `signals/<week>.yaml` into a
   mapping `{repo_slug: {scores: {...}, evidence: {...}}}`.
4. For each repo, `score.score_repo()` (alias of `scorer.score_repo`)
   reduces the per-factor sub-scores into a `Score` dict with a total
   and a candidate verdict.
5. `score.build_rollup()` applies the DEC-PTP-001 forced top-2 /
   bottom-3 mechanic across all repo totals.
6. `report.render_card()` (alias of `renderer.render_card`) emits one
   Markdown card per repo into `reports/<week>/`.
7. `report.render_rollup()` emits `reports/<week>/_rollup.md`.
8. `ledger.append_run()` appends one JSONL row per repo to
   `data/ledger/<week>.jsonl`. The ledger is the
   machine-readable record that survives the next renderer rewrite.

## What revisits what

| Cadence | What revisits | Where it lives |
|---|---|---|
| Weekly | The user runs the CLI, reads the cards, decides | `reports/<week>/` |
| Weekly | The ledger gets one new file per week | `data/ledger/<week>.jsonl` |
| Per-DEC | The rubric, the thresholds, the factor closure | `decisions/DEC-PTP-*.md` |
| Per-spec | The data contracts and the gate set | `specs/000N-*/` |

## Gate set (what `python -m pytest` and the validators guard)

- `python -m pytest` — scorer arithmetic, rollup mechanic, validate
  scripts.
- `python scripts/validate_schemas.py` — all schemas are valid
  JSON Schema draft 2020-12.
- `python scripts/validate_registry.py` — every registry entry
  validates against `schemas/repo-entry.schema.json`; slugs unique.
- `python scripts/validate_rubric.py` — exactly five factors; each
  factor has rules covering scores 0..4.

Deferred to spec 0002:

- `python scripts/voice_lint.py` — banned-word check across `*.md`.
- `python scripts/validate_decisions.py` — DEC front-matter shape.

## Files that hold the load-bearing decisions

- `decisions/DEC-PTP-001-rubric-closure.md` — pins the five-factor
  closure, the verdict thresholds (>=15 ATTEND, 8..14 FREEZE, <=7
  RETIRE), and the forced top-2 / bottom-3 rollup mechanic. Any of
  these change ships as a successor DEC.
- `docs/METHODOLOGY.md` — the prose explanation. The reference the
  user opens when a score feels surprising.
- `STATUS.md` — the current/limits/next snapshot. The
  `## Next feature queue` section is the input to the next factory
  run for this repo.
