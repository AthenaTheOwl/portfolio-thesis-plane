"""Validate `registry/repos.yaml` against `schemas/repo-entry.schema.json`.

Checks per R-PTP-001 / R-PTP-002:
- Every entry validates against the repo-entry schema.
- Every entry carries a non-empty `thesis_statement`.
- Slugs are unique across the registry.

Exits 0 on success, 1 on any failure.
"""

from __future__ import annotations

import datetime as _dt
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "registry" / "repos.yaml"
SCHEMA_PATH = REPO_ROOT / "schemas" / "repo-entry.schema.json"


def _normalize_dates(value):
    """Coerce YAML-parsed date/datetime values to ISO-8601 strings.

    PyYAML's safe_load turns an unquoted `2026-06-22` into a
    `datetime.date`, but the schema declares `created_at` as a string
    with `format: date`. Normalize so the canonical committed registry
    validates without forcing every date to be quoted in the YAML.
    """
    if isinstance(value, _dt.datetime):
        return value.date().isoformat()
    if isinstance(value, _dt.date):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _normalize_dates(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize_dates(v) for v in value]
    return value


def main() -> int:
    if not SCHEMA_PATH.is_file():
        print(f"validate_registry: missing schema {SCHEMA_PATH}", file=sys.stderr)
        return 1
    if not REGISTRY_PATH.is_file():
        print(f"validate_registry: missing registry {REGISTRY_PATH}", file=sys.stderr)
        return 1

    with SCHEMA_PATH.open("r", encoding="utf-8") as fh:
        schema = json.load(fh)
    with REGISTRY_PATH.open("r", encoding="utf-8") as fh:
        entries = _normalize_dates(yaml.safe_load(fh))

    if not isinstance(entries, list) or not entries:
        print(
            f"validate_registry: {REGISTRY_PATH} must be a non-empty YAML list",
            file=sys.stderr,
        )
        return 1

    validator = Draft202012Validator(schema)
    seen_slugs: set[str] = set()

    for idx, entry in enumerate(entries):
        if not isinstance(entry, dict):
            print(
                f"validate_registry: entry {idx} is not a mapping",
                file=sys.stderr,
            )
            return 1

        try:
            validator.validate(entry)
        except ValidationError as exc:
            slug = entry.get("slug", f"<entry {idx}>")
            print(
                f"validate_registry: {slug}: schema violation: {exc.message}",
                file=sys.stderr,
            )
            return 1

        slug = entry["slug"]
        if slug in seen_slugs:
            print(f"validate_registry: duplicate slug {slug!r}", file=sys.stderr)
            return 1
        seen_slugs.add(slug)

        thesis = entry["thesis_statement"].strip()
        if not thesis:
            print(
                f"validate_registry: {slug}: empty thesis_statement",
                file=sys.stderr,
            )
            return 1

    print(f"validate_registry: {len(entries)} entries ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
