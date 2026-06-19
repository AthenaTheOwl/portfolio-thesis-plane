# AGENTS.md — portfolio-thesis-plane

Operating contract for AI agents working in this repo. Conventions
match the AthenaTheOwl portfolio.

## What this repo is

A weekly cadence tool that emits one typed card per repo plus a roll-
up. The card carries a thesis-alive score and a forced ATTEND /
FREEZE / RETIRE verdict. The roll-up forces a top-two attention pick
and a bottom-three retire list.

This is a personal planning tool. The user is the audience. Discipline
matters more than scale.

## Roles you may see in tasks

| Role | What they do |
|---|---|
| `signal-ingester` | Pulls typed signals (model releases, OSS drops, papers) |
| `rubric-scorer` | Applies the five-factor rubric to one repo for one week |
| `card-renderer` | Composes the per-repo card from the score and signals |
| `rollup-writer` | Picks top-2 ATTEND and bottom-3 RETIRE from the cards |
| `cadence-runner` | Weekly cron orchestrator |

These roles exist in the spec ledger; not all are implemented in v0.

## Voice constraints

- No marketing words. The banned set will live in
  `scripts/voice_lint.py::BANNED_FAIL` once the gate lands.
- No antithetical reversals as a structural device.
- The rubric scores use numbers, not adjectives.
- The verdict is a single word: `ATTEND`, `FREEZE`, or `RETIRE`. No
  modifiers, no hedges.

## Gates (will land in spec 0002)

Planned local gates before pushing:

- `pytest`
- `voice_lint.py` on `reports/*.md`
- `spec_check.py` against `specs/`
- `validate_registry.py` — every repo in `registry/repos.yaml` has a
  thesis statement and a current verdict
- `validate_rubric.py` — every rubric factor has a scoring rule

## Out of scope

- Auto-execution of verdicts. ATTEND does not start a build; it
  flags one. The user does the work.
- A web dashboard. Markdown cards under `reports/` are the artifact.
- Tracking repos outside the AthenaTheOwl portfolio. v0 is scoped to
  the ~20 listed in the registry.
- LLM-based scoring. Rubric is mechanical; signal ingest may use LLM
  classification but the score arithmetic is fixed.
