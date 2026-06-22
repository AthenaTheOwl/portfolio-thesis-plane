# Methodology — Portfolio Thesis Plane

How the weekly scorecard is computed. This document is the reference
the user reads when a rubric score feels surprising and the
follow-up question is "wait, what does this actually mean?"

## Cadence

One run per ISO week. The reference Monday for any week is the
literal Monday of that ISO week. All lookback windows
(`past 30 days`, `past 90 days`) are anchored to that Monday so a
run that lands on a Wednesday does not get a different answer than
one that lands on a Friday.

A run produces exactly three artifact families:

1. `reports/<iso-week>/<slug>.md` — one card per repo in
   `registry/repos.yaml`.
2. `reports/<iso-week>/_rollup.md` — exactly one rollup naming the
   forced top-2 ATTEND and forced bottom-3 RETIRE.
3. `data/ledger/<iso-week>.jsonl` — one machine-readable row per
   repo per week. The ledger is append-only; the renderer can be
   rewritten without losing history.

## The five-factor rubric

Closure to exactly five factors is pinned by DEC-PTP-001 and is not
revisable without a successor DEC.

| Factor | Reads | 0 means | 4 means |
|---|---|---|---|
| `model-release-impact` | Foundation-model release log | No relevant release in 30d | Release directly strengthens or invalidates the bet |
| `oss-competition` | OSS competitor watchlist | No threshold crossed in 30d | A competitor shipped a v1 that subsumes the scope |
| `paper-drift` | Recent literature scan | No relevant papers in 30d | A paper nails or refutes the method with real evidence |
| `recent-run-evidence` | The target repo's commit/run log | Dormant in 30d | A real artifact shipped this week |
| `decision-freshness` | The target repo's `decisions/` dir | Latest DEC > 90d old | A DEC landed this week |

The intermediate scores 1, 2, 3 are spelled out per-factor in
`rubric/thesis-alive.yaml`. The rubric closes to five factors and
not three because three lets a single noisy factor flip a verdict;
it closes to five and not seven because each added factor degrades
the cadence (the user stops writing cards). DEC-PTP-001 lists
factors considered and rejected.

## Score arithmetic and the verdict map

```
total = sum(factor_scores.values())  # 0..20
verdict = ATTEND  if total >= 15
verdict = FREEZE  if 8 <= total <= 14
verdict = RETIRE  if total <= 7
```

The thresholds are part of DEC-PTP-001. Adjusting them requires a
successor DEC.

## The forced verdict mechanic

The candidate buckets above are not the rollup. The rollup overrides
candidate verdicts to force exactly two ATTEND repos and exactly
three RETIRE repos every week:

1. Sort all repos by total descending. The top two go to ATTEND.
2. From the remaining repos, sort by total ascending. The bottom
   three go to RETIRE.
3. Everything in between goes to FREEZE.

**Tie rule.** Among repos tied on total, the alphabetically earlier
slug gets the *better* outcome. For ATTEND (a good outcome) that
means the earlier slug wins the spot. For RETIRE (a bad outcome)
the earlier slug *escapes* and the alphabetically later slug falls
into RETIRE.

The mechanic is the load-bearing decision. Without it, a quiet
week scores zero ATTENDs and zero RETIREs and the report has cost
nothing to write. The point is to force a written attention
allocation, not to score it on its own terms.

## What this method deliberately does not do

- **No LLM scoring.** The rubric is mechanical. An LLM may classify
  signals into the typed YAML inputs (spec 0003), but the score
  arithmetic is fixed and reproducible.
- **No weighted sums.** All five factors weigh equally (0..4 each,
  max 20). Weights would themselves drift and become a hidden
  re-rank surface.
- **No "needs more thought" verdict.** Every repo gets `ATTEND`,
  `FREEZE`, or `RETIRE`. Hedging is the failure mode this tool
  exists to defeat.
- **No carryover.** Each week is computed fresh against current
  signals. A repo that was ATTEND last week starts this week at
  the same score everyone else does. Followthrough regression is
  spec 0004.

## Calibration

v0 ships one fully-computed calibration week
(`reports/2026-W25/` + `data/ledger/2026-W25.jsonl`). The signals
were hand-curated against the rubric and the cards reflect the
resulting scores. This is the anchor against which the spec 0002
weekly cadence is measured — the first automated run should produce
a 2026-W26 rollup that the user finds defensible without manual
override.

## What revisits this

The methodology document is not static. The following triggers a
revisit and (if anything changes) a new DEC:

- **Per-DEC.** Every rubric edit (factor add, factor remove, factor
  rename) ships as a successor to DEC-PTP-001. The methodology table
  above is regenerated from the new DEC.
- **Per-quarter.** The user opens this file and the latest rollup
  side by side and asks: did the forced top-2 / bottom-3 mechanic
  surface the repos that actually mattered, or did it just sort
  noise? If the mechanic produced six wrong-feeling weeks in a row,
  that is itself a DEC.
- **After a surprise.** If a score feels surprising in either
  direction (a quiet repo scored high, a hot repo scored low), the
  user reads this file before changing the rubric. Most "surprises"
  are the rubric working — that is what mechanical scoring is for.
- **When the ledger gets queried for the first time.** The ledger
  format at `data/ledger/<week>.jsonl` is described in
  `SYSTEM_MAP.md`. Any change to the row shape is a DEC.

## Maintenance contract

- Every rubric edit ships as a DEC.
- Every threshold edit ships as a DEC.
- Every factor add / remove / rename ships as a DEC.
- Every change to the ledger row shape ships as a DEC.
- Registry edits (slug additions, slug removals, thesis-statement
  rewrites) do not require a DEC. They are content updates.
