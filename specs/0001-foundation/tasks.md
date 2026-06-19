# Tasks — 0001 Foundation

Checkbox tasks ordered for the first two to three PRs after the
scaffold.

## PR 1 — Registry, rubric, schemas

- [ ] Write `schemas/repo-entry.schema.json` per R-PTP-002
- [ ] Write `schemas/score.schema.json`
- [ ] Write `schemas/card.schema.json` and
      `schemas/rollup.schema.json`
- [ ] Write `registry/repos.yaml` listing all ~20 portfolio repos
      with thesis statements
- [ ] Write `rubric/thesis-alive.yaml` declaring the five factors
      and the 0..4 rules per factor
- [ ] Add `decisions/DEC-PTP-001-rubric-closure.md`
- [ ] Add `scripts/validate_schemas.py` skeleton
- [ ] Add `scripts/validate_registry.py` skeleton
- [ ] Add `scripts/validate_rubric.py` skeleton

## PR 2 — Hand-computed calibration week

- [ ] Hand-curate `signals/model-releases.yaml`,
      `signals/oss-competitors.yaml`, `signals/papers.yaml` for
      ISO week 2026-W25
- [ ] Hand-compute per-repo scores under
      `reports/2026-W25/<slug>.md`
- [ ] Hand-compute the roll-up at `reports/2026-W25/_rollup.md`
- [ ] Add `scripts/voice_lint.py` skeleton

## PR 3 — Scorer and renderer skeletons

- [ ] Implement `src/portfolio_thesis_plane/scorer.py` reading
      the rubric and the signals and producing a `Score` per repo
- [ ] Implement `src/portfolio_thesis_plane/renderer.py` rendering
      cards and the roll-up
- [ ] Wire CLI entry: `python -m portfolio_thesis_plane generate
      --week 2026-W26`
- [ ] Add `scripts/validate_decisions.py` skeleton
- [ ] Document the forced-verdict mechanic in DEC-PTP-002
- [ ] Update README install + run section once the CLI runs end-
      to-end
