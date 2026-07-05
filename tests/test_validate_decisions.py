from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_validate_decisions():
    spec = importlib.util.spec_from_file_location(
        "validate_decisions", REPO_ROOT / "scripts" / "validate_decisions.py"
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_clean_decision_passes(tmp_path: Path) -> None:
    validate_decisions = _load_validate_decisions()
    path = tmp_path / "DEC-PTP-002-followthrough.md"
    path.write_text(
        "---\n"
        "id: DEC-PTP-002\n"
        "title: Followthrough cadence\n"
        "date: 2026-06-29\n"
        "status: accepted\n"
        "supersedes: null\n"
        "---\n"
        "\n"
        "# DEC-PTP-002\n",
        encoding="utf-8",
    )

    assert validate_decisions.check_file(path) is None


def test_missing_front_matter_fails(tmp_path: Path) -> None:
    validate_decisions = _load_validate_decisions()
    path = tmp_path / "DEC-PTP-002-followthrough.md"
    path.write_text("# DEC-PTP-002\n", encoding="utf-8")

    assert validate_decisions.check_file(path) is not None


def test_bad_id_fails(tmp_path: Path) -> None:
    validate_decisions = _load_validate_decisions()
    path = tmp_path / "DEC-PTP-002-followthrough.md"
    path.write_text(
        "---\n"
        "id: DEC-PTP-999\n"
        "title: Followthrough cadence\n"
        "date: 2026-06-29\n"
        "status: accepted\n"
        "supersedes: null\n"
        "---\n",
        encoding="utf-8",
    )

    assert validate_decisions.check_file(path) is not None


def test_bad_status_fails(tmp_path: Path) -> None:
    validate_decisions = _load_validate_decisions()
    path = tmp_path / "DEC-PTP-002-followthrough.md"
    path.write_text(
        "---\n"
        "id: DEC-PTP-002\n"
        "title: Followthrough cadence\n"
        "date: 2026-06-29\n"
        "status: proposed\n"
        "supersedes: null\n"
        "---\n",
        encoding="utf-8",
    )

    assert validate_decisions.check_file(path) is not None
