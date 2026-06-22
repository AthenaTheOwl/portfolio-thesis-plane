"""Unit tests for the forced top-2 / bottom-3 rollup mechanic."""

from __future__ import annotations

from portfolio_thesis_plane.scorer import build_rollup


def _score(slug: str, total: int) -> dict:
    return {"repo_slug": slug, "total_score": total}


def test_rollup_picks_top_two_and_bottom_three() -> None:
    scores = [
        ("alpha", 18),
        ("bravo", 16),
        ("charlie", 12),
        ("delta", 11),
        ("echo", 9),
        ("foxtrot", 4),
        ("golf", 3),
        ("hotel", 2),
    ]
    rollup = build_rollup("2026-W25", scores)

    assert rollup["iso_week"] == "2026-W25"
    assert rollup["attend"] == [_score("alpha", 18), _score("bravo", 16)]
    assert rollup["retire"] == [
        _score("hotel", 2),
        _score("golf", 3),
        _score("foxtrot", 4),
    ]
    freeze_slugs = [item["repo_slug"] for item in rollup["freeze"]]
    assert freeze_slugs == ["charlie", "delta", "echo"]


def test_rollup_breaks_ties_by_slug() -> None:
    scores = [
        ("zulu", 10),
        ("alpha", 10),
        ("mike", 10),
        ("november", 10),
        ("oscar", 10),
    ]
    rollup = build_rollup("2026-W25", scores)

    assert [s["repo_slug"] for s in rollup["attend"]] == ["alpha", "mike"]
    assert [s["repo_slug"] for s in rollup["retire"]] == [
        "zulu",
        "oscar",
        "november",
    ]
