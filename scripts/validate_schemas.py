"""Validate that every schema in `schemas/` is a syntactically valid
JSON Schema (Draft 2020-12).

Exits 0 on success, 1 on any failure. Prints the offending path and a
short reason on failure.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = REPO_ROOT / "schemas"


def main() -> int:
    if not SCHEMAS_DIR.is_dir():
        print(f"validate_schemas: missing directory {SCHEMAS_DIR}", file=sys.stderr)
        return 1

    schema_paths = sorted(SCHEMAS_DIR.glob("*.schema.json"))
    if not schema_paths:
        print(f"validate_schemas: no schemas found under {SCHEMAS_DIR}", file=sys.stderr)
        return 1

    for path in schema_paths:
        try:
            with path.open("r", encoding="utf-8") as fh:
                schema = json.load(fh)
        except json.JSONDecodeError as exc:
            print(f"validate_schemas: {path}: invalid JSON ({exc})", file=sys.stderr)
            return 1

        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            print(f"validate_schemas: {path}: invalid schema ({exc.message})", file=sys.stderr)
            return 1

    print(f"validate_schemas: {len(schema_paths)} schema(s) ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
