# Design — 0002 Cadence

## Shape

Spec 0002 turns the v0.1 calibration into a weekly loop. Three
deliverables:

1. **Voice gate.** `scripts/voice_lint.py` reads markdown under
   `reports/`, `decisions/`, and `docs/`, fails on any banned word.
2. **Decision gate.** `scripts/validate_decisions.py` walks
   `decisions/` and enforces the DEC front-matter shape.
3. **Second weekly row.** `reports/2026-W26/` produced by the CLI
   from `signals/2026-W26.yaml`, plus a `_followthrough.md` memo
   that names what happened to the 2026-W25 ATTEND picks.

## voice_lint.py

The script reuses the same exit-non-zero-on-failure pattern as the
spec 0001 validators. Banned words live in a `BANNED_FAIL` constant
inside the script (not in a YAML the script reads — banned-word
configuration should be guarded by code review, not by data review).

Initial `BANNED_FAIL` set:

- marketing language: `delight`, `seamless`, `cutting-edge`,
  `revolutionary`, `game-changing`, `next-gen`, `world-class`,
  `industry-leading`
- antithetical reversals as a structural device: `not ... but` /
  `it is not X, it is Y` style. (Caught by a small regex, not by
  word-list lookup.)

The script reports the file and line of each violation.

## validate_decisions.py

For each `decisions/DEC-PTP-*.md`:

- Parse YAML front-matter (between leading `---` lines).
- Require keys: `id` (matches `^DEC-PTP-[0-9]+$`), `title`
  (non-empty), `date` (ISO 8601 date), `status`
  (`accepted` or `superseded`), `supersedes` (`null` or a
  string matching the `id` pattern).
- Require the filename to match `<id>-<slug>.md`.

## Weekly cadence

The CLI lands in v0.1 already. Spec 0002 adds the operational habit
of running it weekly:

```
python -m portfolio_thesis_plane generate --week 2026-W26
```

The week-of-year is the only argument that ever changes. The
`signals/<iso-week>.yaml` is curated before each run; everything
else (registry, rubric, scorer, renderer) stays put.

## Followthrough memo

A new file shape — `reports/<iso-week>/_followthrough.md` — that
references last week's ATTEND list and names what happened to each
repo. The memo is hand-written. There is no schema; the
voice_lint.py gate is the only check.

The memo is the input to spec 0004 (cross-week verdict-followthrough
regression). v0.2 ships the memos by hand; the regression spec
turns them into a data set.

## Out of v0.2 scope

- Live signal ingest (spec 0003).
- A web dashboard.
- Automated PR generation per ATTEND pick.
