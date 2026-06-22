"""Rubric scorer and forced-verdict rollup mechanic.

The scorer is a small mechanical reader. It takes a dict of
per-factor sub-scores (0..4 each) and returns a `Score`-shaped dict.
The rollup takes a list of `(repo_slug, total)` tuples and applies the
DEC-PTP-001 forced top-2 / bottom-3 mechanic.

Per DEC-PTP-001:
- total >= 15: ATTEND candidate
- total in 8..14: FREEZE candidate
- total <= 7: RETIRE candidate

The rollup overrides candidate buckets to force exactly two ATTEND
and exactly three RETIRE per ISO week.
"""

from __future__ import annotations

from typing import Iterable, Sequence

FACTOR_NAMES: tuple[str, ...] = (
    "model-release-impact",
    "oss-competition",
    "paper-drift",
    "recent-run-evidence",
    "decision-freshness",
)


def verdict_for_total(total: int) -> str:
    if total >= 15:
        return "ATTEND"
    if total >= 8:
        return "FREEZE"
    return "RETIRE"


def score_repo(
    repo_slug: str, iso_week: str, factor_scores: dict[str, int]
) -> dict:
    missing = set(FACTOR_NAMES) - set(factor_scores)
    if missing:
        raise ValueError(f"missing factor scores for {repo_slug}: {sorted(missing)}")
    extra = set(factor_scores) - set(FACTOR_NAMES)
    if extra:
        raise ValueError(f"unexpected factor scores for {repo_slug}: {sorted(extra)}")

    for name, value in factor_scores.items():
        if not isinstance(value, int) or value < 0 or value > 4:
            raise ValueError(
                f"{repo_slug}/{name}: factor score must be int 0..4, got {value!r}"
            )

    total = sum(factor_scores[name] for name in FACTOR_NAMES)
    return {
        "repo_slug": repo_slug,
        "iso_week": iso_week,
        "factor_scores": {name: factor_scores[name] for name in FACTOR_NAMES},
        "total": total,
        "verdict": verdict_for_total(total),
    }


def build_rollup(
    iso_week: str, repo_totals: Iterable[tuple[str, int]]
) -> dict:
    """Force the top-2 ATTEND and bottom-3 RETIRE; everything else FREEZE.

    Tie rule: among repos tied on total, the alphabetically earlier slug
    gets the better outcome. For ATTEND (good outcome) that means earlier
    slug wins the spot; for RETIRE (bad outcome) the earlier slug escapes
    and the alphabetically later slugs fall into RETIRE.
    """
    pairs = list(repo_totals)
    if len(pairs) < 5:
        raise ValueError(
            f"need at least 5 repo totals to force top-2 / bottom-3, got {len(pairs)}"
        )

    attend_sorted = sorted(pairs, key=lambda item: (-item[1], item[0]))
    attend_picks = attend_sorted[:2]
    attend_slugs = {slug for slug, _ in attend_picks}

    remaining = [p for p in pairs if p[0] not in attend_slugs]
    by_slug_desc = sorted(remaining, key=lambda item: item[0], reverse=True)
    retire_sorted = sorted(by_slug_desc, key=lambda item: item[1])
    retire_picks = retire_sorted[:3]
    retire_slugs = {slug for slug, _ in retire_picks}

    freeze_picks = sorted(
        (p for p in remaining if p[0] not in retire_slugs),
        key=lambda item: (-item[1], item[0]),
    )

    def _entries(rows: Sequence[tuple[str, int]]) -> list[dict]:
        return [{"repo_slug": slug, "total_score": total} for slug, total in rows]

    return {
        "iso_week": iso_week,
        "attend": _entries(attend_picks),
        "freeze": _entries(freeze_picks),
        "retire": _entries(retire_picks),
    }
