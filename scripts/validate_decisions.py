"""Validate DEC records for the spec 0002 decision ledger.

Checks per R-PTP-013 / R-PTP-014:
- Every DEC file carries required YAML front matter.
- DEC filenames and front-matter ids use the same DEC-PTP-NNN prefix.
- Decision status is either `accepted` or `superseded`.

Exits 0 on success, 1 on any failure.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DECISIONS_DIR = REPO_ROOT / "decisions"
REQUIRED_KEYS = ("id", "title", "date", "status", "supersedes")
VALID_STATUSES = {"accepted", "superseded"}


def _front_matter(text: str) -> tuple[dict[str, Any] | None, str | None]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None, "missing YAML front matter"

    for idx, line in enumerate(lines[1:], start=1):
        if line == "---":
            raw = "\n".join(lines[1:idx])
            data = yaml.safe_load(raw)
            if not isinstance(data, dict):
                return None, "YAML front matter must be a mapping"
            return data, None

    return None, "unterminated YAML front matter"


def check_file(path: Path) -> str | None:
    name_parts = path.name.split("-", maxsplit=3)
    if (
        len(name_parts) != 4
        or name_parts[0] != "DEC"
        or name_parts[1] != "PTP"
        or not name_parts[2].isdigit()
        or len(name_parts[2]) != 3
        or not name_parts[3].endswith(".md")
        or name_parts[3] == ".md"
    ):
        return "filename must match DEC-PTP-NNN-<slug>.md"

    expected_id = "-".join(name_parts[:3])
    text = path.read_text(encoding="utf-8")
    data, error = _front_matter(text)
    if error is not None:
        return error
    assert data is not None

    for key in REQUIRED_KEYS:
        if key not in data:
            return f"missing front-matter key {key!r}"

    if data["id"] != expected_id:
        return f"front-matter id {data['id']!r} does not match {expected_id!r}"

    if data["status"] not in VALID_STATUSES:
        return "status must be accepted or superseded"

    return None


def main() -> int:
    paths = sorted(DECISIONS_DIR.glob("DEC-PTP-*.md")) if DECISIONS_DIR.exists() else []

    for path in paths:
        error = check_file(path)
        if error is not None:
            rel_path = path.relative_to(REPO_ROOT)
            print(f"validate_decisions: {rel_path}: {error}", file=sys.stderr)
            return 1

    print(f"validate_decisions: {len(paths)} decisions ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
