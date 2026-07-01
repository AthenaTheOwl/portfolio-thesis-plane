# portfolio-thesis-plane

Twenty repos go into a weekly report card. This week three of them score above zero. The other seventeen are real repos with no curated signals yet, scoring a flat 0/20, and the tool stamps RETIRE on the bottom three without asking how anyone feels about it.

## What it does

Attention drifts to whatever is loudest that week, and the repos you have quietly stopped believing in keep getting a pass because nobody writes the verdict down. This is a weekly cadence tool that writes the verdict down. Once per ISO week it scores every repo in the portfolio and emits one Markdown card per repo plus a top-of-week roll-up that names the top-two ATTEND repos and the bottom-three RETIRE candidates.

The thesis-alive score is not a model's mood. It is a five-factor checklist, 0 to 20, computed against typed signals: recent model releases that strengthen or invalidate the bet, competing open-source repos that closed the gap, new papers that confirm or undercut the approach, run-evidence in the target repo, and decision-log freshness. The card forces one of ATTEND, FREEZE, or RETIRE. There is no "needs more thought" box to hide in. That is the whole point.

## Try it

One command, no args, no network. It reads the committed registry and the latest signals, scores every repo, and prints the ranked table:

```
python -m portfolio_thesis_plane show
```

```
portfolio thesis plane - 2026-W25
20 repos scored against a 5-factor thesis-alive rubric (0..20).

   #  repo                     score  verdict
  -------------------------------------------
   1  Binding Constraint        11/20  ATTEND
   2  Portfolio Thesis Plane    10/20  ATTEND
   3  Athena Site                2/20  FREEZE
   4  Agent Notary Layer         0/20  FREEZE
   5  Brief Calibration          0/20  FREEZE
   6  Dream Replay CLI           0/20  FREEZE
   7  Eval Forge                 0/20  FREEZE
   8  HBM Supply Tracker         0/20  FREEZE
   9  Interconnect Queue Risk    0/20  FREEZE
  10  MCP Security Lab           0/20  FREEZE
  11  Modelswap Replay           0/20  FREEZE
  12  Oulipo Memory Deck         0/20  FREEZE
  13  Pattern Index              0/20  FREEZE
  14  Pre-Mortem Ledger          0/20  FREEZE
  15  Release Pillar Mapper      0/20  FREEZE
  16  Review Queue               0/20  FREEZE
  17  Source Decay Ledger        0/20  FREEZE
  18  Sports Prediction OS       0/20  RETIRE
  19  Supplier Risk RAG Agent    0/20  RETIRE
  20  Trace-to-Eval Harness      0/20  RETIRE

headline: binding-constraint leads at 11/20; ATTEND forced onto Binding Constraint, Portfolio Thesis Plane. 17 of 20 repos score 0 (dormant), so the bottom-3 RETIRE bucket is Trace-to-Eval Harness, Supplier Risk RAG Agent, Sports Prediction OS.
```

The seventeen zeros are honest. This is the calibration week (`2026-W25`); the rows are real repos from the portfolio with theses already written, but no signals have been curated for them yet, and the rubric scores them exactly as dormant as they are.

## live demo

A Streamlit page (`streamlit_app.py`) renders the same scorecard interactively: the ranked table with per-factor sub-scores, a verdict filter, and the forced-ATTEND headline. It reads the committed registry and latest signals directly — no network, no secrets.

Run it locally:

```
python -m uv run --with streamlit streamlit run streamlit_app.py
# or: pip install -r requirements.txt && streamlit run streamlit_app.py
```

Deploy on Streamlit Community Cloud -> New app -> repo
`AthenaTheOwl/portfolio-thesis-plane`, branch `main`, main file
`streamlit_app.py`.

<!-- live url: (add after first Streamlit Community Cloud deploy) -->

## How it connects

The registry is the portfolio, so every other repo is an input to this one. Two of them score above zero this week and they say what kind of repo earns a verdict:

- [binding-constraint](https://github.com/AthenaTheOwl/binding-constraint) — the week's other forced-attention tool: name the one constraint downstream of most planning waste. It leads the board at 11/20.
- [athena-site](https://github.com/AthenaTheOwl/athena-site) — the public index page the rest of the portfolio cross-links from. The card-extraction pattern this tool runs on was already living there; this repo pulls it into a tool of its own.

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

## Layout

```
portfolio_thesis_plane/   loader, scorer, renderer, report, cli
registry/repos.yaml       the twenty repos and their thesis statements
rubric/thesis-alive.yaml  the five-factor scoring rubric
signals/2026-W25.yaml     typed inputs: model releases, OSS competitors, paper drops
reports/2026-W25/         the week's cards + _rollup.md
schemas/  specs/  decisions/  docs/  tests/
```

## License

MIT. See [LICENSE](LICENSE).
