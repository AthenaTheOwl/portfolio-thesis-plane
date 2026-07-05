"""Lint prose artifacts for the spec 0002 voice constraints.

Checks per R-PTP-011 / R-PTP-012:
- Markdown reports, decisions, and docs avoid banned marketing terms.
- Markdown reports, decisions, and docs avoid antithetical reversals.

Exits 0 on success, 1 on any failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ("reports", "decisions", "docs")

BANNED_FAIL: set[str] = {
    "cutting-edge",
    "delight",
    "game-changing",
    "industry-leading",
    "next-gen",
    "revolutionary",
    "seamless",
    "world-class",
}

ANTITHETICAL_REVERSAL = re.compile(r"\bnot\b.{1,60}\bbut\b", re.IGNORECASE)
_BANNED_PATTERNS = {
    term: re.compile(rf"(?<![\w-]){re.escape(term)}(?![\w-])", re.IGNORECASE)
    for term in BANNED_FAIL
}


def iter_markdown_files() -> list[Path]:
    paths: list[Path] = []
    for dir_name in SCAN_DIRS:
        scan_dir = REPO_ROOT / dir_name
        if scan_dir.exists():
            paths.extend(sorted(scan_dir.rglob("*.md")))
    return sorted(paths)


def scan_file(path: Path) -> list[tuple[int, str]]:
    violations: list[tuple[int, str]] = []
    text = path.read_text(encoding="utf-8")

    for line_no, line in enumerate(text.splitlines(), start=1):
        lowered = line.lower()
        for term, pattern in _BANNED_PATTERNS.items():
            if pattern.search(lowered):
                violations.append((line_no, f"banned term {term!r}"))
        if ANTITHETICAL_REVERSAL.search(line):
            violations.append((line_no, "antithetical reversal"))

    return violations


def main() -> int:
    paths = iter_markdown_files()
    failed = False

    for path in paths:
        for line_no, message in scan_file(path):
            rel_path = path.relative_to(REPO_ROOT)
            print(f"voice_lint: {rel_path}:{line_no}: {message}", file=sys.stderr)
            failed = True

    if failed:
        return 1

    print(f"voice_lint: {len(paths)} files ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
