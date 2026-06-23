"""Tests for the no-arg `show` verb.

`show` reads the latest committed signals week, scores every registry
repo, applies the forced top-2 / bottom-3 mechanic, and prints a ranked
table plus a one-line headline. Read-only, offline, exits 0.
"""

from __future__ import annotations

from portfolio_thesis_plane import cli, loader


def test_show_runs_and_is_ranked(capsys) -> None:
    rc = cli.main(["show"])
    assert rc == 0

    out = capsys.readouterr().out
    week = loader.latest_week()

    # header names the week and the rubric range
    assert week in out
    assert "5-factor" in out
    assert "0..20" in out

    # ranked rows: rank 1 is the highest-scoring repo, and a headline lands
    assert "\n   1  " in out
    assert "headline:" in out
    assert "ATTEND" in out and "RETIRE" in out

    # the top-of-table repo is the registry max for that week
    registry = loader.load_registry()
    signals = loader.load_signals(week)
    totals = []
    for entry in registry:
        sub, _ = cli._extract_scores_and_evidence(signals.get(entry["slug"]))
        totals.append((entry["slug"], sum(sub.values())))
    top_total = max(t for _, t in totals)
    assert f"{top_total:>3}/20" in out


def test_show_unknown_week_exits_nonzero(capsys) -> None:
    rc = cli.main(["show", "--week", "1999-W01"])
    assert rc == 1
    assert "show:" in capsys.readouterr().err
