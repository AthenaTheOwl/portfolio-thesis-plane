"""Score arithmetic — canonical module name.

`score` is the primary public name for the rubric arithmetic and the
forced top-2 / bottom-3 rollup mechanic. The implementation lives in
`scorer` (kept for back-compat with the v0.1 test suite); this module
re-exports the public surface.
"""

from __future__ import annotations

from .scorer import (
    FACTOR_NAMES,
    build_rollup,
    score_repo,
    verdict_for_total,
)

__all__ = [
    "FACTOR_NAMES",
    "build_rollup",
    "score_repo",
    "verdict_for_total",
]
