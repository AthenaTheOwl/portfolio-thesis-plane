# STATUS — portfolio-thesis-plane

A snapshot of where the repo is, where it is brittle, and what the
next factory run should pick up. The bullet list under
**Next feature queue** is the input to the next factory run for this
repo; keep it small and concrete.

## Current state

- v0.1 ships the data contracts, the registry, the rubric, the
  founding governance decision, three validate-* gate scripts, and
  the first end-to-end calibration row at `reports/2026-W25/`
  plus its machine-readable mirror at
  `data/ledger/2026-W25.jsonl` (20 rows, one per repo).
- Twenty cards plus a roll-up exist on disk for 2026-W25. The
  roll-up names two ATTEND picks (`binding-constraint`,
  `portfolio-thesis-plane`) and three RETIRE picks (whichever three
  zero-scored repos sort last by slug this week — currently
  `trace-to-eval-harness`, `supplier-risk-rag-agent`,
  `sports-prediction-os`).
- The CLI is runnable: `python -m portfolio_thesis_plane generate
  --week 2026-W25` reproduces the cards and the rollup from the
  hand-curated signals in `signals/2026-W25.yaml`.
- `DEC-PTP-001-rubric-closure.md` pins the five-factor closure and
  the forced top-2 / bottom-3 mechanic.
- `pyproject.toml` declares the package, the `portfolio-thesis-plane`
  console script, and uv-friendly dependency-groups so `python -m uv
  sync` puts the project itself into the venv.
- The canonical module names are `score`, `report`, `ledger`, `cli`
  (with `scorer` and `renderer` kept as back-compat aliases). The
  CLI's `generate` subcommand writes both the Markdown cards and the
  ledger JSONL in one pass.
- `PRODUCT_BRIEF.md`, `SYSTEM_MAP.md`, and `docs/METHODOLOGY.md`
  document the why, the wiring, and the math. `specs/0002-design/`
  is the design ledger for the next cycle.

## Known limits

- The seventeen non-founding registry entries (added in the 2026-W25
  consolidation) carry real theses but no curated signals yet, so
  they score 0/20 this week by the file's own honest-zero
  convention. Every weekly rollup is dominated by these zeros until
  `signals/2026-W25.yaml` gets real per-repo entries for them.
- Signal ingest is hand-curated. There is no automation that turns
  model-release feeds, OSS competitor watchlists, or paper RSS into
  the YAML the scorer reads. Spec 0003 owns this.
- The 2026-W25 cards on disk are now CLI-rendered (`generate --week
  2026-W25`), regenerated during the consolidation pass so all
  twenty match the current registry. The renderer does not emit a
  `forced_verdict` front-matter field; the rollup file is still the
  place that records which verdicts got overridden.
- No `voice_lint.py` gate yet (deferred to spec 0002). The banned-
  word check named in AGENTS.md is not enforced.
- No `validate_decisions.py` gate yet. The DEC directory is
  un-policed.
- Cross-week verdict-followthrough regression (did the user actually
  act on last week's ATTEND picks?) is not implemented. Spec 0004.
- Tests cover the scorer arithmetic, the rollup mechanic, and the
  three validate-* scripts. The CLI generate path is not yet under
  test.

## Next feature queue

- Add `scripts/voice_lint.py` with the banned-word list named in
  AGENTS.md, and wire it into the gate set in
  `specs/0001-foundation/acceptance.md`.
- Add `scripts/validate_decisions.py` to enforce the DEC front-matter
  shape (id, title, date, status, supersedes).
- Curate real `signals/2026-W25.yaml` entries for the seventeen
  repos added in the consolidation pass (currently absent from the
  file, so they score an honest 0) and re-render the 2026-W25
  calibration to match.
- Extend the CLI to write a `forced_verdict` field into rendered
  cards so per-repo override reasoning is visible on the card itself,
  not just in `_rollup.md`.
- Run spec 0002 (`signals/sources.yaml` + an offline ingest stub)
  end-to-end against the 2026-W26 week as the first non-calibration
  cycle.
- Add a CLI-level integration test that calls `generate` and asserts
  the rollup shape against `schemas/rollup.schema.json`.

- Resolve factory defect: missing PRODUCT_BRIEF.md,SYSTEM_MAP.md
- Resolve factory defect: missing data/ledger/*.jsonl
- Resolve factory defect: METHODOLOGY.md missing revisit section
- Resolve factory defect: PRODUCT_BRIEF.md is required for active repos
- Resolve factory defect: SYSTEM_MAP.md is required for active repos
- Resolve factory defect: expected file 'PRODUCT_BRIEF.md' is missing
- Resolve factory defect: expected file 'SYSTEM_MAP.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/requirements.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/design.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/tasks.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/acceptance.md' is missing
- Resolve factory defect: expected file 'portfolio_thesis_plane/cli.py' is missing
- Resolve factory defect: expected file 'portfolio_thesis_plane/score.py' is missing
- Resolve factory defect: expected file 'portfolio_thesis_plane/ledger.py' is missing
- Resolve factory defect: expected glob 'data/ledger/*.jsonl' matched no files
- Resolve factory defect: module 'cli' declares source 'portfolio_thesis_plane/cli.py', but it is missing
- Resolve factory defect: module 'score' declares source 'portfolio_thesis_plane/score.py', but it is missing
- Resolve factory defect: module 'ledger' declares source 'portfolio_thesis_plane/ledger.py', but it is missing
- Resolve factory defect: module 'report' declares source 'portfolio_thesis_plane/report.py', but it is missing
- Resolve factory defect: claude_code review requested patch; inspect defect log
- Resolve factory defect: expected file 'portfolio_thesis_plane/cli.py' is missing
- Resolve factory defect: expected file 'portfolio_thesis_plane/score.py' is missing
- Resolve factory defect: expected file 'portfolio_thesis_plane/ledger.py' is missing
- Resolve factory defect: module 'cli' declares source 'portfolio_thesis_plane/cli.py', but it is missing
- Resolve factory defect: module 'score' declares source 'portfolio_thesis_plane/score.py', but it is missing
- Resolve factory defect: module 'ledger' declares source 'portfolio_thesis_plane/ledger.py', but it is missing
- Resolve factory defect: module 'report' declares source 'portfolio_thesis_plane/report.py', but it is missing
- Resolve factory defect: claude_code review requested patch; inspect defect log
