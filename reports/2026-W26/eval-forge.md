---
repo_slug: eval-forge
iso_week: 2026-W26
total: 8
verdict: FREEZE
---

# eval-forge — 2026-W26

**Thesis.** Retrieval and agent quality regressions should block the PR that caused them, not surface a week later on a dashboard nobody reopens. Five typed checks with one threshold each, one exit code.

**Score.** 8 / 20 -> `FREEZE`

## Factor sub-scores

| Factor | Score |
|---|---|
| model-release-impact | 0 |
| oss-competition | 0 |
| paper-drift | 0 |
| recent-run-evidence | 4 |
| decision-freshness | 4 |

## Evidence trail

### model-release-impact
- No verified offline source for model releases in W26.

### oss-competition
- No verified offline source for OSS competitor movement in W26.

### paper-drift
- No verified offline source for papers in W26.

### recent-run-evidence
- git log: 5 commits in w/c 2026-06-22, including eval-forge v0.1 and CI work.

### decision-freshness
- decisions/: DEC-EF-002-vendor-harness-checks.md dated 2026-06-22.
