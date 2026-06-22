# Tasks — 0002 Design

## PR 1 — Voice gate

- [ ] Add `scripts/voice_lint.py` with `BANNED_FAIL` constant
- [ ] Walk `reports/`, `decisions/`, `docs/` and exit non-zero on
      any hit
- [ ] Add a test that exercises one banned-word hit and one clean
      file
- [ ] Wire `voice_lint.py` into `specs/0001-foundation/acceptance.md`
      gate list (already named there; remove the "deferred" caveat)

## PR 2 — Decision gate

- [ ] Add `scripts/validate_decisions.py`
- [ ] Validate front-matter shape on every `DEC-PTP-*.md`
- [ ] Validate filename pattern against `id`
- [ ] Add a test that exercises one malformed DEC and one clean DEC

## PR 3 — Ledger integration

- [ ] Extend `portfolio_thesis_plane.ledger.append_run()` to
      record both `candidate_verdict` and `final_verdict`
- [ ] Wire `ledger.append_run()` into the CLI `generate` path so
      every run writes `data/ledger/<week>.jsonl`
- [ ] Add a test that asserts the JSONL row shape matches the
      ledger contract in `design.md`

## PR 4 — 2026-W26 cadence row

- [ ] Curate `signals/2026-W26.yaml` against fresh signals
- [ ] Run `python -m portfolio_thesis_plane generate --week 2026-W26`
- [ ] Commit `reports/2026-W26/` (cards + rollup)
- [ ] Commit `data/ledger/2026-W26.jsonl`
- [ ] Hand-write `reports/2026-W26/_followthrough.md` against the
      2026-W25 ATTEND picks
- [ ] Update `STATUS.md` "Current state" to note 2026-W26 shipped
      and to clear the matching item from "Next feature queue"
