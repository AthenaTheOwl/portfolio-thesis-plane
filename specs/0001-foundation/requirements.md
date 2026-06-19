# Requirements — 0001 Foundation

Numbered requirements for the v0 scaffold of portfolio-thesis-plane.
The R-PTP-* prefix is the brand tag and appears in every downstream
spec, decision, and gate.

## Registry

- **R-PTP-001** The repo ships a registry under
  `registry/repos.yaml` listing the ~20 portfolio repos. Each entry
  has `slug`, `name`, `thesis_statement`, `created_at`,
  `current_verdict`.
- **R-PTP-002** The registry schema is under
  `schemas/repo-entry.schema.json` and is enforced by
  `scripts/validate_registry.py`.

## Rubric

- **R-PTP-003** The thesis-alive rubric lives in
  `rubric/thesis-alive.yaml`. It declares exactly five factors:
  `model-release-impact`, `oss-competition`, `paper-drift`,
  `recent-run-evidence`, `decision-freshness`.
- **R-PTP-004** Each factor scores 0 to 4. The thesis-alive score
  is the sum; max 20.
- **R-PTP-005** The verdict mapping is fixed: score >= 15 -> ATTEND
  candidate, 8..14 -> FREEZE candidate, <= 7 -> RETIRE candidate.
  The roll-up applies the forced top-2 ATTEND and bottom-3 RETIRE
  on top of the candidate sets.

## Cards

- **R-PTP-006** A weekly card is rendered per repo at
  `reports/<iso-week>/<repo-slug>.md`. Fields: thesis-alive score,
  per-factor sub-scores, evidence trail, verdict.
- **R-PTP-007** The weekly roll-up is rendered at
  `reports/<iso-week>/_rollup.md` and names the forced top-2 ATTEND
  and bottom-3 RETIRE.

## Signals

- **R-PTP-008** Signals live under `signals/` in typed YAML files
  by source: `model-releases.yaml`, `oss-competitors.yaml`,
  `papers.yaml`. The rubric reads from these files; live signal
  ingest is deferred to spec 0003.

## Cadence

- **R-PTP-009** v0 ships one fully-computed calibration week
  (`reports/2026-W25/`). The week is computed by hand to anchor
  the rubric before automation.

## Governance

- **R-PTP-010** Architectural choices are recorded in
  `decisions/DEC-PTP-NNN-<slug>.md`. The first decision (DEC-PTP-001)
  justifies the five-factor rubric closure and the forced verdict
  mechanic.
