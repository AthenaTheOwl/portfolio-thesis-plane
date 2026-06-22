"""Markdown report rendering — canonical module name.

`report` is the primary public name for the card and rollup renderer.
The implementation lives in `renderer` (kept for back-compat with the
v0.1 test suite); this module re-exports the public surface.
"""

from __future__ import annotations

from .renderer import render_card, render_rollup

__all__ = ["render_card", "render_rollup"]
