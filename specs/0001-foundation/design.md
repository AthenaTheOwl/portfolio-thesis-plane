# Design — 0001 Foundation

## Shape

portfolio-thesis-plane is a Python CLI that scores the portfolio's
repos against a five-factor rubric every week and emits Markdown
cards plus a roll-up.

The architecture has four layers:

1. **Registry.** `registry/repos.yaml` lists the repos and their
   thesis statements.
2. **Signals.** `signals/*.yaml` carry the typed inputs that feed
   the rubric. v0 hand-curates these; live ingest is spec 0003.
3. **Scorer.** `src/portfolio_thesis_plane/scorer.py` applies the
   rubric to one repo for one week and emits a `Score` object.
4. **Renderer.** `src/portfolio_thesis_plane/renderer.py` composes
   per-repo cards and the weekly roll-up.

## Data flow

```
registry/repos.yaml
signals/*.yaml
   |
   v
for each repo in registry:
   [scorer.score(repo, week)]  ->  Score
       (sub-scores by factor + evidence ids)
   |
   v
[renderer.card(score)]  ->  reports/<week>/<slug>.md
   |
   v
[renderer.rollup(all_scores)]  ->  reports/<week>/_rollup.md
```

## Rubric scoring

Each factor is scored 0 to 4 by mechanical rules:

- `model-release-impact`: 0 if no model release in the past 30 days
  affects the repo's bet; 4 if a recent release directly strengthens
  or invalidates it.
- `oss-competition`: 0 if no competing OSS repo crossed a threshold
  in the past 30 days; 4 if a competitor shipped a v1 that subsumes
  the repo's scope.
- `paper-drift`: 0 if recent papers do not affect the bet; 4 if a
  paper either nails the approach or refutes it.
- `recent-run-evidence`: 0 if the repo has no factory run, brief, or
  diagnostic in the past 30 days; 4 if it shipped a real artifact
  this week.
- `decision-freshness`: 0 if the latest DEC is older than 90 days;
  4 if a DEC landed this week.

The score is a sum; the verdict bucket is fixed by score range.

## Forced verdict mechanic

The rubric produces candidate ATTEND, FREEZE, and RETIRE buckets.
The roll-up applies the forced top-2 ATTEND and bottom-3 RETIRE on
top of those candidates. If the candidate ATTEND bucket has fewer
than two repos, the roll-up promotes the two highest-scoring repos
regardless. If the candidate RETIRE bucket has fewer than three,
the roll-up demotes the three lowest-scoring repos.

This is the discipline. The mechanic prevents a "nothing changed
this week" cop-out.

## Signal source registry

`signals/sources.yaml` lists the upstream feeds the live-ingest
spec (0003) will consume. v0 hand-fills the typed signal files
directly; the source registry exists to anchor the eventual ingest.

## Out of v0 scope

- Live signal ingest
- Cross-week regression of which past verdicts the user actually
  acted on
- A web dashboard
- Tracking repos outside the AthenaTheOwl portfolio
