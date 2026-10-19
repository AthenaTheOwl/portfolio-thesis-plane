# portfolio-thesis-plane

Twenty repos enter the W26 scorecard. Dream Replay CLI and Eval Forge lead at 8/20;
HBM Supply Tracker and Interconnect Queue Risk are the only zeros. The tool still
forces a bottom-three RETIRE bucket, so low evidence cannot hide behind a quiet week.

## What it does

Attention drifts to whatever is loudest that week, and the repos you have quietly stopped believing in keep getting a pass because nobody writes the verdict down. This is a weekly cadence tool that writes the verdict down. Once per ISO week it scores every repo in the portfolio and emits one Markdown card per repo plus a top-of-week roll-up that names the top-two ATTEND repos and the bottom-three RETIRE candidates.

The thesis-alive score is not a model's mood. It is a five-factor checklist, 0 to 20, computed against typed signals: recent model releases that strengthen or invalidate the bet, competing open-source repos that closed the gap, new papers that confirm or undercut the approach, run-evidence in the target repo, and decision-log freshness. The card forces one of ATTEND, FREEZE, or RETIRE. There is no "needs more thought" box to hide in. That is the whole point.

## Try it

One command, no args, no network. It reads the committed registry and the latest signals, scores every repo, and prints the ranked table:

```
python -m portfolio_thesis_plane show
```

```
portfolio thesis plane - 2026-W26
20 repos scored against a 5-factor thesis-alive rubric (0..20).

   #  repo                     score  verdict
  -------------------------------------------
   1  Dream Replay CLI           8/20  ATTEND
   2  Eval Forge                 8/20  ATTEND
   3  Pattern Index              8/20  FREEZE
   4  Portfolio Thesis Plane     8/20  FREEZE
   5  Pre-Mortem Ledger          8/20  FREEZE
   6  Review Queue               8/20  FREEZE
   7  Athena Site                7/20  FREEZE
   8  Brief Calibration          7/20  FREEZE
   9  Source Decay Ledger        7/20  FREEZE
  10  MCP Security Lab           6/20  FREEZE
  11  Supplier Risk RAG Agent    6/20  FREEZE
  12  Trace-to-Eval Harness      6/20  FREEZE
  13  Modelswap Replay           4/20  FREEZE
  14  Oulipo Memory Deck         4/20  FREEZE
  15  Release Pillar Mapper      4/20  FREEZE
  16  Agent Notary Layer         3/20  FREEZE
  17  Binding Constraint         3/20  FREEZE
  18  Sports Prediction OS       3/20  RETIRE
  19  HBM Supply Tracker         0/20  RETIRE
  20  Interconnect Queue Risk    0/20  RETIRE

headline: dream-replay-cli leads at 8/20; ATTEND forced onto Dream Replay CLI, Eval Forge. 2 of 20 repos score 0 (dormant), so the bottom-3 RETIRE bucket is Interconnect Queue Risk, HBM Supply Tracker, Sports Prediction OS.
```

The two zeros are honest. HBM Supply Tracker and Interconnect Queue Risk have
registered theses but no W26 signals, so the rubric leaves them at zero. The result is
a curation queue. Underlying project value sits outside this weekly evidence score.

## Live demo

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

The registry is the portfolio, so every other repo is an input. W26 puts two evidence
workflows at the top:

- [dream-replay-cli](https://github.com/AthenaTheOwl/dream-replay-cli) turns a
  retrospective into a replayable artifact rather than a loose note.
- [eval-forge](https://github.com/AthenaTheOwl/eval-forge) packages evaluation cases
  and verdicts into a repeatable gate.

## How to run

```
# ranked, readable scorecard from the latest committed week (no args)
python -m portfolio_thesis_plane show

# regenerate the cards + roll-up for a week
python -m portfolio_thesis_plane generate --week 2026-W26

# one repo's score as JSON
python -m portfolio_thesis_plane score --repo dream-replay-cli --week 2026-W26

# validate the committed registry, rubric, and schemas
python -m portfolio_thesis_plane validate
```

## Layout

```
portfolio_thesis_plane/   loader, scorer, renderer, report, cli
registry/repos.yaml       the twenty repos and their thesis statements
rubric/thesis-alive.yaml  the five-factor scoring rubric
signals/2026-W26.yaml     typed inputs: model releases, OSS competitors, paper drops
reports/2026-W26/         the week's cards + _rollup.md
schemas/  specs/  decisions/  docs/  tests/
```

## License

MIT. See [LICENSE](LICENSE).

## Method update

[October method update: A forced attention ranking still needs a coverage label](docs/attention-under-missing-evidence.md).
