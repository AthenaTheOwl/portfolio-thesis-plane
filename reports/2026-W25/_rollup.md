---
iso_week: 2026-W25
attend:
  - { repo_slug: binding-constraint, total_score: 11 }
  - { repo_slug: portfolio-thesis-plane, total_score: 10 }
retire:
  - { repo_slug: portfolio-repo-20, total_score: 0 }
  - { repo_slug: portfolio-repo-19, total_score: 0 }
  - { repo_slug: portfolio-repo-18, total_score: 0 }
freeze:
  - { repo_slug: athena-site, total_score: 2 }
  - { repo_slug: portfolio-repo-04, total_score: 0 }
  - { repo_slug: portfolio-repo-05, total_score: 0 }
  - { repo_slug: portfolio-repo-06, total_score: 0 }
  - { repo_slug: portfolio-repo-07, total_score: 0 }
  - { repo_slug: portfolio-repo-08, total_score: 0 }
  - { repo_slug: portfolio-repo-09, total_score: 0 }
  - { repo_slug: portfolio-repo-10, total_score: 0 }
  - { repo_slug: portfolio-repo-11, total_score: 0 }
  - { repo_slug: portfolio-repo-12, total_score: 0 }
  - { repo_slug: portfolio-repo-13, total_score: 0 }
  - { repo_slug: portfolio-repo-14, total_score: 0 }
  - { repo_slug: portfolio-repo-15, total_score: 0 }
  - { repo_slug: portfolio-repo-16, total_score: 0 }
  - { repo_slug: portfolio-repo-17, total_score: 0 }
---

# Portfolio roll-up — 2026-W25

This is the calibration week. The rubric runs against hand-curated
signals; the forced top-2 ATTEND and bottom-3 RETIRE per DEC-PTP-001
are applied to the candidate buckets.

## ATTEND

The two highest-scoring repos this week. Promotion is forced even
though both fall inside the `FREEZE` candidate band, because the
mechanic requires exactly two ATTENDs every week.

| Slug | Name | Score | Notes |
|---|---|---|---|
| `binding-constraint` | Binding Constraint | 11 | Active development; recent DEC; one supporting paper |
| `portfolio-thesis-plane` | Portfolio Thesis Plane | 10 | Born this week — scaffold and DEC-PTP-001 both land in 2026-W25 |

## RETIRE

The three lowest-scoring repos this week. All three placeholder rows
that have not yet been bound to real portfolio repos. Tie at 0/20
broken by slug DESC (alphabetically later loses).

| Slug | Name | Score | Notes |
|---|---|---|---|
| `portfolio-repo-20` | Placeholder Repo 20 | 0 | Tie-break loser; alphabetically last placeholder slug |
| `portfolio-repo-19` | Placeholder Repo 19 | 0 | Tie-break loser |
| `portfolio-repo-18` | Placeholder Repo 18 | 0 | Tie-break loser |

## FREEZE

Everyone else.

| Slug | Name | Score |
|---|---|---|
| `athena-site` | Athena Site | 2 |
| `portfolio-repo-04` | Placeholder Repo 04 | 0 |
| `portfolio-repo-05` | Placeholder Repo 05 | 0 |
| `portfolio-repo-06` | Placeholder Repo 06 | 0 |
| `portfolio-repo-07` | Placeholder Repo 07 | 0 |
| `portfolio-repo-08` | Placeholder Repo 08 | 0 |
| `portfolio-repo-09` | Placeholder Repo 09 | 0 |
| `portfolio-repo-10` | Placeholder Repo 10 | 0 |
| `portfolio-repo-11` | Placeholder Repo 11 | 0 |
| `portfolio-repo-12` | Placeholder Repo 12 | 0 |
| `portfolio-repo-13` | Placeholder Repo 13 | 0 |
| `portfolio-repo-14` | Placeholder Repo 14 | 0 |
| `portfolio-repo-15` | Placeholder Repo 15 | 0 |
| `portfolio-repo-16` | Placeholder Repo 16 | 0 |
| `portfolio-repo-17` | Placeholder Repo 17 | 0 |

## Calibration notes

- The candidate `ATTEND` bucket was empty this week (no repo scored
  >= 15). The forced top-2 mechanic still names two attention picks.
  This is the point of the mechanic — without it the user would
  spend zero attention on the portfolio this week, which is exactly
  the failure mode the rubric exists to prevent.
- Seventeen placeholder rows dominate the bottom of the distribution.
  As the canonical AthenaTheOwl repo list is confirmed, real entries
  replace the placeholders and the bottom-3 RETIRE bucket starts
  picking real targets.
- This is the anchor data point against which spec 0002 (signal
  ingest and weekly cadence) will calibrate.
