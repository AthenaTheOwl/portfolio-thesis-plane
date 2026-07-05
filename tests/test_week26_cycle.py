"""Regression tests for the committed 2026-W26 cadence artifacts."""

from __future__ import annotations

import json
from pathlib import Path

from portfolio_thesis_plane import loader
from portfolio_thesis_plane.report import render_card
from portfolio_thesis_plane.scorer import FACTOR_NAMES, score_repo

WEEK = "2026-W26"


def _scores_and_evidence(repo_signals: dict | None) -> tuple[dict[str, int], dict[str, list[str]]]:
    if not isinstance(repo_signals, dict):
        return {name: 0 for name in FACTOR_NAMES}, {name: [] for name in FACTOR_NAMES}
    raw_scores = repo_signals.get("scores") or {}
    raw_evidence = repo_signals.get("evidence") or {}
    return (
        {name: int(raw_scores.get(name, 0)) for name in FACTOR_NAMES},
        {name: list(raw_evidence.get(name, [])) for name in FACTOR_NAMES},
    )


def test_week26_signals_parse_with_bounded_integer_scores() -> None:
    registry_slugs = {entry["slug"] for entry in loader.load_registry()}
    signals = loader.load_signals(WEEK)

    assert set(signals) <= registry_slugs
    assert signals
    for slug, repo_signals in signals.items():
        assert set(repo_signals["scores"]) == set(FACTOR_NAMES), slug
        for value in repo_signals["scores"].values():
            assert isinstance(value, int)
            assert 0 <= value <= 4


def test_week26_ledger_has_one_row_per_registry_slug() -> None:
    registry_slugs = [entry["slug"] for entry in loader.load_registry()]
    path = loader.REPO_ROOT / "data" / "ledger" / f"{WEEK}.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    slugs = [row["repo_slug"] for row in rows]

    assert len(slugs) == len(registry_slugs)
    assert sorted(slugs) == sorted(registry_slugs)
    assert len(slugs) == len(set(slugs))


def test_week26_cards_are_deterministic_from_committed_signals() -> None:
    registry = loader.load_registry()
    signals = loader.load_signals(WEEK)

    for entry in registry:
        slug = entry["slug"]
        factor_scores, evidence = _scores_and_evidence(signals.get(slug))
        score = score_repo(slug, WEEK, factor_scores)
        expected = render_card(score, evidence, entry["thesis_statement"])
        card_path = loader.REPO_ROOT / "reports" / WEEK / f"{slug}.md"

        assert card_path.read_text(encoding="utf-8") == expected


def _count_rows_in_section(markdown: str, section: str) -> int:
    lines = markdown.splitlines()
    start = lines.index(f"## {section}")
    count = 0
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        if line.startswith("| `"):
            count += 1
    return count


def test_week26_rollup_forces_two_attend_and_three_retire() -> None:
    rollup_path = loader.REPO_ROOT / "reports" / WEEK / "_rollup.md"
    markdown = rollup_path.read_text(encoding="utf-8")

    assert _count_rows_in_section(markdown, "ATTEND") == 2
    assert _count_rows_in_section(markdown, "RETIRE") == 3
