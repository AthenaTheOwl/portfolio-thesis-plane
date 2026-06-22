"""Make the `portfolio_thesis_plane` package importable for pytest.

When the test runner is `python -m uv run pytest` the package is
already on sys.path because `[tool.uv] package = true` triggers an
editable install. This conftest is the belt-and-braces fallback for a
plain `python -m pytest` invocation from the repo root: it puts the
repo root on sys.path so `import portfolio_thesis_plane` resolves.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
