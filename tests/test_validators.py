"""Smoke tests for the validate_* scripts. Each is run as a subprocess
so the test verifies the on-disk artifacts the gate would actually check.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"


def _run(name: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def test_validate_schemas_passes() -> None:
    result = _run("validate_schemas.py")
    assert result.returncode == 0, result.stderr


def test_validate_registry_passes() -> None:
    result = _run("validate_registry.py")
    assert result.returncode == 0, result.stderr


def test_validate_rubric_passes() -> None:
    result = _run("validate_rubric.py")
    assert result.returncode == 0, result.stderr
