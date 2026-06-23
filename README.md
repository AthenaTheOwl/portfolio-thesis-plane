# Portfolio Thesis Plane

Weekly machine-generated report card across the ~20 repos in the AthenaTheOwl portfolio. Each repo gets a thesis-still-alive score, a last-run-evidence date, an eval-coverage delta, and a decision-log staleness count, with a forced ATTEND / FREEZE / RETIRE verdict per repo.

## What this is

A weekly cadence tool. The output is one Markdown card per repo per
ISO week, plus a top-of-week roll-up that names the top-two ATTEND
repos and the bottom-three RETIRE candidates.

The thesis-alive score is not LLM vibes. It is a five-factor checklist
computed against typed signals:

1. Recent model releases that strengthen or invalidate the repo's bet
2. Competing open-source repos that closed the gap
3. New papers that confirm or undercut the approach
4. Recent run-evidence in the target repo (factory runs, briefs,
   diagnostics)
5. Decision-log freshness in the target repo

The card forces a verdict: ATTEND, FREEZE, or RETIRE. No "needs more
thought" escape hatch. That is the point.

## Who uses it

The user (Vignesh), weekly. The portfolio is the input; the verdicts
are the input to the next week's planning. The cadence is the
discipline; the typed card is the artifact.

## Why now

Attention drifts to whatever is emotionally salient. A typed weekly
report card forces a written verdict on each repo, including the ones
the user has been avoiding thinking about. The pattern that makes
this work in athena-site is already present; this repo extracts it
into a focused tool.

## Status

v0.1 shipped — runnable, minimal. The CLI scores the twenty registry
repos against the five-factor rubric using hand-curated signals, applies
the forced top-2 / bottom-3 mechanic, and writes weekly cards plus a
roll-up. One calibration week (`2026-W25`) is committed. The next passes
deepen it: replace the seventeen placeholder rows with real repos, and
compute a second week so the week-over-week factors exercise a diff. See
`STATUS.md` for the next-feature queue.

## How to run

```
# ranked, readable scorecard from the latest committed week (no args)
python -m portfolio_thesis_plane show

# regenerate the cards + roll-up for a week
python -m portfolio_thesis_plane generate --week 2026-W25

# one repo's score as JSON
python -m portfolio_thesis_plane score --repo binding-constraint --week 2026-W25

# validate the committed registry, rubric, and schemas
python -m portfolio_thesis_plane validate
```

`show` is read-only and offline: it reads `registry/repos.yaml` and the
latest `signals/*.yaml`, scores every repo, and prints a ranked table
plus a one-line headline.

## live demo

A Streamlit page (`streamlit_app.py`) renders the same scorecard
interactively: a ranked table with per-factor sub-scores, a verdict
filter, and the forced-ATTEND headline. It reads the committed registry
and latest signals directly — no network, no secrets.

Run it locally:

```
python -m uv run --with streamlit streamlit run streamlit_app.py
# or: pip install -r requirements.txt && streamlit run streamlit_app.py
```

Deploy on Streamlit Community Cloud -> New app -> repo
`AthenaTheOwl/portfolio-thesis-plane`, branch `main`, main file
`streamlit_app.py`.

<!-- live url: (add after first Streamlit Community Cloud deploy) -->

## Layout

```
portfolio-thesis-plane/
  README.md
  LICENSE
  AGENTS.md
  .gitignore
  specs/
    0001-foundation/
      requirements.md
      design.md
      tasks.md
      acceptance.md
  docs/
    first-pr.md
```

Future directories (named in specs, not created yet):

- `src/portfolio_thesis_plane/` — runtime
- `registry/repos.yaml` — the twenty repos and their thesis statements
- `rubric/thesis-alive.yaml` — the five-factor scoring rubric
- `reports/` — weekly cards and roll-ups
- `signals/` — typed inputs (model-release log, OSS competitor log,
  paper-drop log)

## License

MIT. See [LICENSE](LICENSE).
