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

v0 scaffold; no implementation yet. The specs ledger names the first
set of requirements (R-PTP-001 through R-PTP-010). The first PR
after this scaffold lands the rubric, the repo registry, and one
hand-computed week to calibrate.

## How to run

Placeholder; will land in spec 0002. v0 ships the rubric, the repo
registry (the twenty repos), and one calibration week computed by
hand. No runtime yet.

The eventual CLI shape (target for spec 0003):

```
python -m portfolio_thesis_plane generate --week 2026-W34 --out reports/2026-W34.md
python -m portfolio_thesis_plane score --repo binding-constraint --week 2026-W34
```

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
