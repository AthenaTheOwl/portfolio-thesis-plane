from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_voice_lint():
    spec = importlib.util.spec_from_file_location(
        "voice_lint", REPO_ROOT / "scripts" / "voice_lint.py"
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_clean_file_passes(tmp_path: Path) -> None:
    voice_lint = _load_voice_lint()
    path = tmp_path / "clean.md"
    path.write_text("A plain weekly note with measured evidence.\n", encoding="utf-8")

    assert voice_lint.scan_file(path) == []


def test_banned_word_caught(tmp_path: Path) -> None:
    voice_lint = _load_voice_lint()
    path = tmp_path / "bad.md"
    path.write_text("This would be a revolutionary shift.\n", encoding="utf-8")

    assert voice_lint.scan_file(path)
