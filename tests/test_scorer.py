"""Unit tests for the scorer arithmetic and verdict mapping."""

from __future__ import annotations

from portfolio_thesis_plane.scorer import (
    FACTOR_NAMES,
    score_repo,
    verdict_for_total,
)


def test_factor_closure_is_five() -> None:
    assert len(FACTOR_NAMES) == 5
    assert set(FACTOR_NAMES) == {
        "model-release-impact",
        "oss-competition",
        "paper-drift",
        "recent-run-evidence",
        "decision-freshness",
    }


def test_verdict_thresholds() -> None:
    assert verdict_for_total(20) == "ATTEND"
    assert verdict_for_total(15) == "ATTEND"
    assert verdict_for_total(14) == "FREEZE"
    assert verdict_for_total(8) == "FREEZE"
    assert verdict_for_total(7) == "RETIRE"
    assert verdict_for_total(0) == "RETIRE"


def test_score_repo_sums_factors_and_buckets() -> None:
    factor_scores = {name: 3 for name in FACTOR_NAMES}
    result = score_repo("binding-constraint", "2026-W25", factor_scores)
    assert result["total"] == 15
    assert result["verdict"] == "ATTEND"
    assert result["repo_slug"] == "binding-constraint"
    assert result["iso_week"] == "2026-W25"
