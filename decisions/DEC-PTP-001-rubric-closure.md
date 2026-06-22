---
id: DEC-PTP-001
title: Five-factor rubric closure and forced verdict mechanic
date: 2026-06-22
status: accepted
supersedes: null
---

# DEC-PTP-001 — Five-factor rubric closure and forced verdict mechanic

## Context

The thesis-alive rubric exists to force a written verdict on every
portfolio repo every week. Without a fixed factor list and a forced
verdict mechanic, the rubric drifts: a new factor gets bolted on
whenever a repo feels uncomfortable, an extra "needs more thought"
verdict appears, and the weekly report stops costing anything to write.

This decision pins both the closure and the mechanic in writing so
later edits land as successor DECs rather than as silent rubric
re-balancing.

## Decision

The thesis-alive rubric closes to exactly five factors:

1. `model-release-impact`
2. `oss-competition`
3. `paper-drift`
4. `recent-run-evidence`
5. `decision-freshness`

Each factor scores 0..4 on a checklist (`rubric/thesis-alive.yaml`).
The total is the sum; max 20. Verdict buckets are fixed:

- total >= 15 -> `ATTEND` candidate
- total in 8..14 -> `FREEZE` candidate
- total <= 7 -> `RETIRE` candidate

Bucket boundaries are inclusive on the high side and exclusive on the
low side of `FREEZE`. There is no `unscored` verdict on a `Score`
object — `unscored` is a registry state, not a scoring outcome.

Adding, removing, or renaming a factor requires a successor DEC. The
verdict thresholds are part of this decision; changing them also
requires a successor DEC.

## Forced verdict mechanic

The rubric produces candidate buckets per repo, but the roll-up
overrides them to force exactly two `ATTEND` repos and exactly three
`RETIRE` repos every week.

- If the candidate `ATTEND` bucket has fewer than two repos, the
  roll-up promotes the two highest-scoring repos regardless of
  bucket. If it has more than two, the roll-up keeps the two highest.
- If the candidate `RETIRE` bucket has fewer than three repos, the
  roll-up demotes the three lowest-scoring repos regardless of
  bucket. If it has more than three, the roll-up keeps the three
  lowest.
- Ties are broken by ascending slug, deterministically.

The mechanic is the point. The repo could have shipped a "5 ATTEND,
0 RETIRE" week without it; it would also stop costing anything to
write. Forcing a top-2 and a bottom-3 means the user has to name a
repo to look away from, every week, on the record. That is the
discipline this tool sells.

## Alternatives considered

- **Three factors.** Too few signals; the score becomes a coin flip
  on any close week. Rejected.
- **Seven or ten factors.** Each added factor adds a category whose
  signal is correlated with the existing five; the marginal factor
  improves precision but degrades cadence (the user stops writing
  cards). Rejected.
- **LLM-based scoring.** Vibes-as-a-service. Rejected on grounds
  that the rubric is the artifact; if the rubric does not survive
  mechanical evaluation, it does not survive at all.
- **Weighted sum.** The weights would themselves drift. A flat 0..4
  per factor is auditable; a 0.37 weighting decision is not.

## Factors considered and deferred

- **Revenue / monetization signal.** None of the portfolio repos
  generate revenue and the calibration would always read zero;
  re-evaluate if a repo ever ships a paid surface.
- **User interest / external traffic.** Vanity metric for personal
  tools. The point of the portfolio is not audience growth.
- **Velocity.** Subsumed by `recent-run-evidence`. A separate
  velocity factor would double-count commits.
- **Team morale.** N=1 portfolio; the user's morale is not a
  per-repo signal.

These may resurface as a successor DEC if the portfolio grows past
its current scope.

## Consequences

- Every rubric edit ships as a DEC. The history of the rubric is the
  history of the decisions.
- The weekly roll-up always names two repos to attend to and three
  to retire, regardless of how unequivocal the candidate buckets
  look. The user does not get to skip the hard call.
- The scorer is a small mechanical reader of YAML; no opinion
  surface, no model surface.
