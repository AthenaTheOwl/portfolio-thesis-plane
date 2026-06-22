# Product Brief — Portfolio Thesis Plane

A monthly-to-quarterly control plane that scores, calibrates, and audits
the verdict each repo in the AthenaTheOwl portfolio earns this week.
The brief here is the one-page answer to "what is this thing for and how
do I know it is working?"

## The problem

Attention is the scarce resource. With ~20 repos in the portfolio, the
user (Vignesh) cannot keep every bet alive in working memory. The
default failure mode is that the loudest repo of the week gets all the
attention and the quiet ones drift — until a quiet one ships a paper
that invalidates the bet six months too late.

The user is the only operator. There is no team. The control plane
has to be cheap enough to run weekly *and* honest enough to surface
the repo the user has been avoiding thinking about.

## What this ships

A weekly run that consumes:

- `registry/repos.yaml` — the twenty bets being tracked
- `rubric/thesis-alive.yaml` — the five-factor scoring rubric
- `signals/<iso-week>.yaml` — hand-curated or ingested evidence

…and produces:

- `reports/<iso-week>/<slug>.md` — one typed verdict card per repo
- `reports/<iso-week>/_rollup.md` — the forced top-2 ATTEND and
  bottom-3 RETIRE
- `data/ledger/<iso-week>.jsonl` — one machine-readable row per repo,
  appended forever, so cross-week regressions are queryable

The verdict is forced: every repo gets `ATTEND`, `FREEZE`, or `RETIRE`.
There is no "needs more thought" escape hatch.

## Who uses it

The user (Vignesh), weekly. The output is the input to the next week's
planning. The cadence is the discipline; the typed card is the
artifact. No other consumers, no SLA, no API. The audit trail is
checked into git so the user can read it cold six months later.

## What "working" looks like

- Every ISO week has a `reports/<week>/` directory and a corresponding
  ledger row.
- The forced top-2 / bottom-3 mechanic is applied every week,
  including weeks where every repo scored low — the mechanic is the
  point.
- Every rubric change ships as a DEC. The rubric is closed at five
  factors until a successor DEC opens it.
- The CLI is one command:
  `python -m portfolio_thesis_plane generate --week <iso-week>`.

## What this deliberately is not

- Not an LLM judge. The rubric arithmetic is mechanical. An LLM may
  classify signals into the typed YAML inputs (spec 0003), but the
  score sum is fixed and reproducible.
- Not a recommender. The forced verdict is a discipline mechanic, not
  a prediction.
- Not a dashboard. The artifact is the Markdown card. If the user
  wants a graph it gets built off the ledger.
- Not a service. There is no daemon. The CLI is invoked by hand once
  a week.

## v0.1 scope (what is checked in)

- The data contracts: `schemas/*.json`.
- The inputs: `registry/repos.yaml`, `rubric/thesis-alive.yaml`,
  `signals/2026-W25.yaml`.
- The founding governance decision: `DEC-PTP-001-rubric-closure.md`.
- Three validate-* gate scripts.
- The first calibration run: `reports/2026-W25/` and one ledger row
  at `data/ledger/2026-W25.jsonl`.
- A runnable CLI: `python -m portfolio_thesis_plane generate --week
  2026-W25` reproduces the cards from `signals/2026-W25.yaml`.

The deferred work — voice lint, decision-front-matter validator,
signal ingest, cross-week followthrough — is named in
`STATUS.md` under **Next feature queue**.
