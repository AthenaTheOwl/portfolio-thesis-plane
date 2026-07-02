"""Tests for the append-only ledger row builder and writer.

`build_row` carries both the candidate verdict (from the score's own
arithmetic) and the final verdict (from the forced rollup). These are
distinct fields for a reason: pinning a case where they differ catches a
swap of the two.
"""

from __future__ import annotations

import json

from portfolio_thesis_plane import ledger


def _score() -> dict:
    return {
        "repo_slug": "binding-constraint",
        "iso_week": "2026-W25",
        "factor_scores": {
            "model-release-impact": 1,
            "oss-competition": 1,
            "paper-drift": 1,
            "recent-run-evidence": 2,
            "decision-freshness": 1,
        },
        "total": 6,
        "verdict": "FREEZE",
    }


def test_build_row_keeps_candidate_and_final_verdicts_distinct() -> None:
    # candidate verdict (FREEZE, from the score) differs from the final
    # verdict (ATTEND, forced by the rollup) so a swap of the two fails.
    row = ledger.build_row(_score(), "ATTEND", recorded_at="2026-06-25T12:00:00Z")

    assert row["candidate_verdict"] == "FREEZE"
    assert row["final_verdict"] == "ATTEND"
    assert row["repo_slug"] == "binding-constraint"
    assert row["iso_week"] == "2026-W25"
    assert row["total"] == 6
    assert row["factor_scores"] == _score()["factor_scores"]
    assert row["recorded_at"] == "2026-06-25T12:00:00Z"


def test_append_run_round_trips(tmp_path) -> None:
    row = ledger.build_row(_score(), "ATTEND", recorded_at="2026-06-25T12:00:00Z")
    path = ledger.append_run("2026-W25", [row], base_dir=tmp_path)

    assert path == tmp_path / "2026-W25.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0]) == row
