---
repo_slug: binding-constraint
iso_week: 2026-W25
total: 11
verdict: FREEZE
forced_verdict: ATTEND
---

# binding-constraint — 2026-W25

**Thesis.** Most weekly planning waste is downstream of one un-named
binding constraint. Naming the constraint each week is cheaper than
fixing the wrong thing for a quarter.

**Score.** 11 / 20 -> `FREEZE` (rollup overrides to `ATTEND` per DEC-PTP-001)

## Factor sub-scores

| Factor | Score |
|---|---|
| model-release-impact | 2 |
| oss-competition | 1 |
| paper-drift | 2 |
| recent-run-evidence | 3 |
| decision-freshness | 3 |

## Evidence trail

### model-release-impact

- Adjacent model release in 2026-W22 raised long-context retrieval quality; the constraint-naming flow is read-heavy and the bet still holds.

### oss-competition

- Two adjacent planning tools released minor versions; neither overlaps the binding-constraint mechanic.

### paper-drift

- Recent paper on weekly-cadence planning systems engaged the topic at one remove; method neither confirmed nor refuted.

### recent-run-evidence

- Two non-trivial briefs landed in the past 30 days.
- One diagnostic run completed in 2026-W24.

### decision-freshness

- DEC-BC-007 landed 2026-W23 (~14 days old); rubric scores this as "recent thinking update".
