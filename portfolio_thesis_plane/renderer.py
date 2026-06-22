"""Markdown card and rollup renderer.

The renderer is deliberately small: it formats a per-repo score plus
its evidence trail into one Markdown card, and a list of scores into
one rollup. No I/O — callers pass dicts in, get strings out.
"""

from __future__ import annotations

from typing import Sequence

from .scorer import FACTOR_NAMES


def render_card(score: dict, evidence: dict[str, list[str]], thesis_statement: str) -> str:
    repo_slug = score["repo_slug"]
    iso_week = score["iso_week"]
    factor_scores = score["factor_scores"]
    total = score["total"]
    verdict = score["verdict"]

    lines: list[str] = []
    lines.append("---")
    lines.append(f"repo_slug: {repo_slug}")
    lines.append(f"iso_week: {iso_week}")
    lines.append(f"total: {total}")
    lines.append(f"verdict: {verdict}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {repo_slug} — {iso_week}")
    lines.append("")
    lines.append(f"**Thesis.** {thesis_statement.strip()}")
    lines.append("")
    lines.append(f"**Score.** {total} / 20 -> `{verdict}`")
    lines.append("")
    lines.append("## Factor sub-scores")
    lines.append("")
    lines.append("| Factor | Score |")
    lines.append("|---|---|")
    for name in FACTOR_NAMES:
        lines.append(f"| {name} | {factor_scores[name]} |")
    lines.append("")
    lines.append("## Evidence trail")
    lines.append("")
    for name in FACTOR_NAMES:
        lines.append(f"### {name}")
        items = evidence.get(name, [])
        if not items:
            lines.append("- (no evidence on file this week)")
        else:
            for item in items:
                lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_rollup(rollup: dict, registry: Sequence[dict]) -> str:
    by_slug = {entry["slug"]: entry for entry in registry}
    iso_week = rollup["iso_week"]

    def _row(bucket_entry: dict) -> str:
        slug = bucket_entry["repo_slug"]
        score = bucket_entry["total_score"]
        name = by_slug.get(slug, {}).get("name", slug)
        return f"| `{slug}` | {name} | {score} |"

    lines: list[str] = []
    lines.append("---")
    lines.append(f"iso_week: {iso_week}")
    lines.append("---")
    lines.append("")
    lines.append(f"# Portfolio roll-up — {iso_week}")
    lines.append("")
    lines.append(
        "Forced top-2 ATTEND and bottom-3 RETIRE per DEC-PTP-001."
    )
    lines.append("")
    lines.append("## ATTEND")
    lines.append("")
    lines.append("| Slug | Name | Score |")
    lines.append("|---|---|---|")
    for entry in rollup["attend"]:
        lines.append(_row(entry))
    lines.append("")
    lines.append("## RETIRE")
    lines.append("")
    lines.append("| Slug | Name | Score |")
    lines.append("|---|---|---|")
    for entry in rollup["retire"]:
        lines.append(_row(entry))
    lines.append("")
    lines.append("## FREEZE")
    lines.append("")
    if rollup["freeze"]:
        lines.append("| Slug | Name | Score |")
        lines.append("|---|---|---|")
        for entry in rollup["freeze"]:
            lines.append(_row(entry))
    else:
        lines.append("(none)")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"
