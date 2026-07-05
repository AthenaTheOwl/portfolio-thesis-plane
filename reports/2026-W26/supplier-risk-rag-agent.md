---
repo_slug: supplier-risk-rag-agent
iso_week: 2026-W26
total: 6
verdict: RETIRE
---

# supplier-risk-rag-agent — 2026-W26

**Thesis.** A RAG agent over supplier-risk filings is only worth trusting if every answer points at a verbatim retrieved span; citation faithfulness checked after generation, not asserted, is what makes the refusal behavior credible.

**Score.** 6 / 20 -> `RETIRE`

## Factor sub-scores

| Factor | Score |
|---|---|
| model-release-impact | 0 |
| oss-competition | 0 |
| paper-drift | 0 |
| recent-run-evidence | 3 |
| decision-freshness | 3 |

## Evidence trail

### model-release-impact
- No verified offline source for model releases in W26.

### oss-competition
- No verified offline source for OSS competitor movement in W26.

### paper-drift
- No verified offline source for papers in W26.

### recent-run-evidence
- git log: 6 commits in w/c 2026-06-22, including app entrypoint and CI work.

### decision-freshness
- decisions/: latest W26-or-earlier DEC is DEC-EVL-008-eval-replay-command.md dated 2026-05-28.
