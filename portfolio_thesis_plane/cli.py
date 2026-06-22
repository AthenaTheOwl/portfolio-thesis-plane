"""Command-line entry for portfolio-thesis-plane.

Subcommands:
- `validate`: run the canonical no-arg sanity check over the committed
  registry, rubric, and schemas. Read-only; exits 0 on success.
- `score`: print one repo's `Score` dict for an ISO week as JSON.
- `generate`: render cards + rollup for an ISO week into `reports/<week>/`.
- `list-repos`: print the registry slugs.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Sequence

from . import ledger, loader
from .report import render_card, render_rollup
from .score import FACTOR_NAMES, build_rollup, score_repo

SCRIPTS_DIR = loader.REPO_ROOT / "scripts"


def _load_script_main(script_name: str):
    """Load a `scripts/<name>.py` module and return its `main` callable.

    The `scripts/` directory is not an importable package, so load each
    validator by path. Keeps the canonical checks in one place rather
    than duplicating their logic here.
    """
    path = SCRIPTS_DIR / f"{script_name}.py"
    spec = importlib.util.spec_from_file_location(f"_ptp_{script_name}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.main


def _cmd_validate(_: argparse.Namespace) -> int:
    """Run the canonical no-arg sanity check over committed artifacts.

    Validates the schemas, the repo registry, and the rubric — the three
    typed inputs the rest of the tool reads. Read-only; writes nothing.
    Exits 0 only if every check passes.
    """
    checks = ("validate_schemas", "validate_registry", "validate_rubric")
    rc = 0
    for name in checks:
        try:
            check_main = _load_script_main(name)
        except Exception as exc:  # pragma: no cover - import guard
            print(f"validate: could not load {name}: {exc}", file=sys.stderr)
            rc = 1
            continue
        result = check_main()
        if result != 0:
            rc = 1
    if rc == 0:
        print("validate: registry, rubric, and schemas ok")
    return rc


def _cmd_list_repos(_: argparse.Namespace) -> int:
    for entry in loader.load_registry():
        print(entry["slug"])
    return 0


def _extract_scores_and_evidence(
    repo_signals: dict | None,
) -> tuple[dict[str, int], dict[str, list[str]]]:
    if not isinstance(repo_signals, dict):
        return {name: 0 for name in FACTOR_NAMES}, {name: [] for name in FACTOR_NAMES}
    raw_scores = repo_signals.get("scores") or {}
    raw_evidence = repo_signals.get("evidence") or {}
    scores = {name: int(raw_scores.get(name, 0)) for name in FACTOR_NAMES}
    evidence = {name: list(raw_evidence.get(name, [])) for name in FACTOR_NAMES}
    return scores, evidence


def _cmd_score(args: argparse.Namespace) -> int:
    registry = loader.load_registry()
    slugs = {entry["slug"] for entry in registry}
    if args.repo not in slugs:
        print(f"score: unknown repo {args.repo!r}", file=sys.stderr)
        return 1

    signals = loader.load_signals(args.week)
    sub_scores, _ = _extract_scores_and_evidence(signals.get(args.repo))
    result = score_repo(args.repo, args.week, sub_scores)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def _cmd_generate(args: argparse.Namespace) -> int:
    registry = loader.load_registry()
    signals = loader.load_signals(args.week)

    out_dir = Path(args.out) if args.out else loader.REPO_ROOT / "reports" / args.week
    out_dir.mkdir(parents=True, exist_ok=True)

    repo_totals: list[tuple[str, int]] = []
    scores: list[dict] = []
    for entry in registry:
        slug = entry["slug"]
        sub_scores, evidence = _extract_scores_and_evidence(signals.get(slug))
        result = score_repo(slug, args.week, sub_scores)
        card_md = render_card(result, evidence, entry["thesis_statement"])
        (out_dir / f"{slug}.md").write_text(card_md, encoding="utf-8")
        repo_totals.append((slug, result["total"]))
        scores.append(result)

    rollup = build_rollup(args.week, repo_totals)
    rollup_md = render_rollup(rollup, registry)
    (out_dir / "_rollup.md").write_text(rollup_md, encoding="utf-8")

    final_by_slug: dict[str, str] = {}
    for bucket, verdict in (("attend", "ATTEND"), ("freeze", "FREEZE"), ("retire", "RETIRE")):
        for item in rollup[bucket]:
            final_by_slug[item["repo_slug"]] = verdict
    rows = [ledger.build_row(s, final_by_slug[s["repo_slug"]]) for s in scores]
    ledger_file = ledger.append_run(args.week, rows)

    print(
        f"generate: wrote {len(registry)} cards + rollup to {out_dir}; "
        f"appended {len(rows)} rows to {ledger_file}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="portfolio-thesis-plane",
        description="Weekly thesis-alive scorer for the AthenaTheOwl portfolio.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_validate = sub.add_parser(
        "validate",
        help="Validate the committed registry, rubric, and schemas (no args).",
    )
    p_validate.set_defaults(func=_cmd_validate)

    p_list = sub.add_parser("list-repos", help="Print registry slugs.")
    p_list.set_defaults(func=_cmd_list_repos)

    p_score = sub.add_parser("score", help="Print one repo's score as JSON.")
    p_score.add_argument("--repo", required=True)
    p_score.add_argument("--week", required=True, help="ISO week (e.g. 2026-W25)")
    p_score.set_defaults(func=_cmd_score)

    p_gen = sub.add_parser("generate", help="Render cards + rollup for one week.")
    p_gen.add_argument("--week", required=True, help="ISO week (e.g. 2026-W25)")
    p_gen.add_argument("--out", default=None, help="Output directory (default: reports/<week>)")
    p_gen.set_defaults(func=_cmd_generate)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
