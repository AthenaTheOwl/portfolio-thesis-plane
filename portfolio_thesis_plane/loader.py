"""Filesystem loaders for the registry, rubric, and signals.

Pure I/O. No scoring or rendering decisions live here.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "registry" / "repos.yaml"
RUBRIC_PATH = REPO_ROOT / "rubric" / "thesis-alive.yaml"
SIGNALS_DIR = REPO_ROOT / "signals"


def load_registry(path: Path | None = None) -> list[dict[str, Any]]:
    path = path or REGISTRY_PATH
    with path.open("r", encoding="utf-8") as fh:
        entries = yaml.safe_load(fh)
    if not isinstance(entries, list):
        raise ValueError(f"{path}: expected a YAML list")
    return entries


def load_rubric(path: Path | None = None) -> dict[str, Any]:
    path = path or RUBRIC_PATH
    with path.open("r", encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    if not isinstance(doc, dict) or "factors" not in doc:
        raise ValueError(f"{path}: expected a mapping with `factors`")
    return doc


def latest_week(signals_dir: Path | None = None) -> str:
    """Return the most recent ISO week with a committed signals file.

    The signals directory holds one `<iso-week>.yaml` per scored week.
    ISO-week strings (e.g. `2026-W25`) sort lexicographically in
    chronological order, so the max filename stem is the latest week.
    """
    signals_dir = signals_dir or SIGNALS_DIR
    weeks = sorted(p.stem for p in signals_dir.glob("*.yaml"))
    if not weeks:
        raise FileNotFoundError(f"no committed signals files under {signals_dir}")
    return weeks[-1]


def load_signals(iso_week: str, signals_dir: Path | None = None) -> dict[str, Any]:
    """Load all signal YAMLs for one ISO week.

    Returns `{repo_slug: {factor_name: int}}` — the per-factor sub-scores
    hand-curated for that week. Repos absent from the signals file get
    a default of 0 for every factor (a fully-zero card is a RETIRE
    candidate, which is the right default for a dormant repo).
    """
    signals_dir = signals_dir or SIGNALS_DIR
    week_path = signals_dir / f"{iso_week}.yaml"
    if not week_path.is_file():
        raise FileNotFoundError(
            f"no hand-curated signals for {iso_week} at {week_path}"
        )
    with week_path.open("r", encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    if not isinstance(doc, dict):
        raise ValueError(f"{week_path}: expected a mapping")
    return doc
