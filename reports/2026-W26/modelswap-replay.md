---
repo_slug: modelswap-replay
iso_week: 2026-W26
total: 4
verdict: RETIRE
---

# modelswap-replay — 2026-W26

**Thesis.** Swapping the model behind a router should require replaying recorded production requests against the candidate and writing a dated revert rule before the swap goes live, not after someone notices it's worse.

**Score.** 4 / 20 -> `RETIRE`

## Factor sub-scores

| Factor | Score |
|---|---|
| model-release-impact | 0 |
| oss-competition | 0 |
| paper-drift | 0 |
| recent-run-evidence | 4 |
| decision-freshness | 0 |

## Evidence trail

### model-release-impact
- No verified offline source for model releases in W26.

### oss-competition
- No verified offline source for OSS competitor movement in W26.

### paper-drift
- No verified offline source for papers in W26.

### recent-run-evidence
- git log: 6 commits in w/c 2026-06-22, including app interaction and proof workflow.

### decision-freshness
- decisions/: no DEC files found.
