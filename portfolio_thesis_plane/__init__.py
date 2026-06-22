"""Portfolio Thesis Plane — weekly thesis-alive scorer for the
AthenaTheOwl portfolio.

Public surface for v0.1:
- `score`: rubric arithmetic and rollup mechanic (alias of `scorer`)
- `report`: Markdown card and rollup composition (alias of `renderer`)
- `ledger`: append-only JSONL audit trail at `data/ledger/<week>.jsonl`
- `cli`: `python -m portfolio_thesis_plane ...` entry

`scorer` and `renderer` remain importable for back-compat with the v0.1
test suite; `score` and `report` are the canonical names going forward.
"""

__version__ = "0.1.0"
