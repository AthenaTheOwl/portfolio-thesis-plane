"""Error-path tests for the CLI verbs.

A nonexistent week or a malformed signals file should print an
actionable message to stderr and exit non-zero, not dump a traceback.
"""

from __future__ import annotations

from portfolio_thesis_plane import cli, loader


def test_score_unknown_week_exits_nonzero(capsys) -> None:
    rc = cli.main(["score", "--repo", "binding-constraint", "--week", "1999-W01"])
    assert rc == 1
    err = capsys.readouterr().err
    assert err.startswith("score:")
    assert "1999-W01" in err


def test_generate_unknown_week_exits_nonzero(tmp_path, capsys) -> None:
    rc = cli.main(
        ["generate", "--week", "1999-W01", "--out", str(tmp_path / "out")]
    )
    assert rc == 1
    err = capsys.readouterr().err
    assert err.startswith("generate:")
    assert "1999-W01" in err


def test_show_malformed_signals_exits_nonzero(tmp_path, monkeypatch, capsys) -> None:
    # a signals file that parses to a scalar (not a mapping) trips the
    # loader's ValueError; show should catch it, not raise.
    signals_dir = tmp_path / "signals"
    signals_dir.mkdir()
    (signals_dir / "2026-W25.yaml").write_text("just a string\n", encoding="utf-8")
    monkeypatch.setattr(loader, "SIGNALS_DIR", signals_dir)

    rc = cli.main(["show", "--week", "2026-W25"])
    assert rc == 1
    assert capsys.readouterr().err.startswith("show:")


def test_show_broken_yaml_exits_nonzero(tmp_path, monkeypatch, capsys) -> None:
    # broken YAML syntax raises yaml.YAMLError from the loader; show
    # should catch it rather than surface a traceback.
    signals_dir = tmp_path / "signals"
    signals_dir.mkdir()
    (signals_dir / "2026-W25.yaml").write_text("key: [unterminated\n", encoding="utf-8")
    monkeypatch.setattr(loader, "SIGNALS_DIR", signals_dir)

    rc = cli.main(["show", "--week", "2026-W25"])
    assert rc == 1
    assert capsys.readouterr().err.startswith("show:")
