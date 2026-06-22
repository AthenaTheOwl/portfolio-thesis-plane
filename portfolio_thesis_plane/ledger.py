"""Append-only ledger writer.

Every weekly run appends one row per repo to
`data/ledger/<iso-week>.jsonl`. The row shape is fixed by the
spec 0002 design ledger and includes both `candidate_verdict` (what
the arithmetic alone says) and `final_verdict` (what the forced
top-2 / bottom-3 mechanic decided). The ledger is the cross-week
audit trail; the renderer can be rewritten without losing history.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping

from .loader import REPO_ROOT

LEDGER_DIR = REPO_ROOT / "data" / "ledger"


def ledger_path(iso_week: str, base_dir: Path | None = None) -> Path:
    base = base_dir or LEDGER_DIR
    return base / f"{iso_week}.jsonl"


def build_row(
    score: Mapping,
    final_verdict: str,
    recorded_at: str | None = None,
) -> dict:
    """Compose one ledger row from a `Score` dict + the final verdict.

    The score dict's `verdict` field is the candidate verdict (what the
    arithmetic alone says). The final verdict is the rollup's decision.
    """
    return {
        "repo_slug": score["repo_slug"],
        "iso_week": score["iso_week"],
        "factor_scores": dict(score["factor_scores"]),
        "total": score["total"],
        "candidate_verdict": score["verdict"],
        "final_verdict": final_verdict,
        "recorded_at": recorded_at or datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
    }


def append_run(
    iso_week: str,
    rows: Iterable[Mapping],
    base_dir: Path | None = None,
) -> Path:
    """Append `rows` to `data/ledger/<iso-week>.jsonl`. Returns the path."""
    path = ledger_path(iso_week, base_dir=base_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
    return path


__all__ = ["LEDGER_DIR", "ledger_path", "build_row", "append_run"]
