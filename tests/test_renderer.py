"""Golden-master tests for the Markdown card and rollup renderer.

These pin the renderer's current output to exact literals. The card
golden locks the score line ("<total> / 20 -> <verdict>"), the
YAML front-matter, and the factor sub-score table; the rollup golden
locks the ATTEND / RETIRE / FREEZE sections including the `(none)`
empty-freeze branch. Any change to the emitted Markdown will fail here.
"""

from __future__ import annotations

from portfolio_thesis_plane.report import render_card, render_rollup
from portfolio_thesis_plane.scorer import FACTOR_NAMES


def test_render_card_matches_golden() -> None:
    score = {
        "repo_slug": "binding-constraint",
        "iso_week": "2026-W25",
        "factor_scores": {name: i for i, name in enumerate(FACTOR_NAMES)},
        "total": 10,
        "verdict": "FREEZE",
    }
    evidence = {
        "model-release-impact": ["GPT-x shipped", "new SOTA"],
        "oss-competition": [],
        "paper-drift": ["arxiv 1234"],
        "recent-run-evidence": [],
        "decision-freshness": [],
    }

    expected = (
        "---\n"
        "repo_slug: binding-constraint\n"
        "iso_week: 2026-W25\n"
        "total: 10\n"
        "verdict: FREEZE\n"
        "---\n"
        "\n"
        "# binding-constraint — 2026-W25\n"
        "\n"
        "**Thesis.** A tidy thesis.\n"
        "\n"
        "**Score.** 10 / 20 -> `FREEZE`\n"
        "\n"
        "## Factor sub-scores\n"
        "\n"
        "| Factor | Score |\n"
        "|---|---|\n"
        "| model-release-impact | 0 |\n"
        "| oss-competition | 1 |\n"
        "| paper-drift | 2 |\n"
        "| recent-run-evidence | 3 |\n"
        "| decision-freshness | 4 |\n"
        "\n"
        "## Evidence trail\n"
        "\n"
        "### model-release-impact\n"
        "- GPT-x shipped\n"
        "- new SOTA\n"
        "\n"
        "### oss-competition\n"
        "- (no evidence on file this week)\n"
        "\n"
        "### paper-drift\n"
        "- arxiv 1234\n"
        "\n"
        "### recent-run-evidence\n"
        "- (no evidence on file this week)\n"
        "\n"
        "### decision-freshness\n"
        "- (no evidence on file this week)\n"
    )

    # leading/trailing whitespace on the thesis is stripped by the renderer
    assert render_card(score, evidence, "  A tidy thesis.  ") == expected


def _rollup(freeze: list[dict]) -> dict:
    return {
        "iso_week": "2026-W25",
        "attend": [
            {"repo_slug": "alpha", "total_score": 18},
            {"repo_slug": "bravo", "total_score": 16},
        ],
        "freeze": freeze,
        "retire": [{"repo_slug": "zulu", "total_score": 2}],
    }


_REGISTRY = [
    {"slug": "alpha", "name": "Alpha Repo"},
    {"slug": "bravo", "name": "Bravo Repo"},
]


def test_render_rollup_empty_freeze_matches_golden() -> None:
    expected = (
        "---\n"
        "iso_week: 2026-W25\n"
        "---\n"
        "\n"
        "# Portfolio roll-up — 2026-W25\n"
        "\n"
        "Forced top-2 ATTEND and bottom-3 RETIRE per DEC-PTP-001.\n"
        "\n"
        "## ATTEND\n"
        "\n"
        "| Slug | Name | Score |\n"
        "|---|---|---|\n"
        "| `alpha` | Alpha Repo | 18 |\n"
        "| `bravo` | Bravo Repo | 16 |\n"
        "\n"
        "## RETIRE\n"
        "\n"
        "| Slug | Name | Score |\n"
        "|---|---|---|\n"
        "| `zulu` | zulu | 2 |\n"
        "\n"
        "## FREEZE\n"
        "\n"
        "(none)\n"
    )
    assert render_rollup(_rollup([]), _REGISTRY) == expected


def test_render_rollup_nonempty_freeze_matches_golden() -> None:
    freeze = [{"repo_slug": "charlie", "total_score": 10}]
    expected = (
        "---\n"
        "iso_week: 2026-W25\n"
        "---\n"
        "\n"
        "# Portfolio roll-up — 2026-W25\n"
        "\n"
        "Forced top-2 ATTEND and bottom-3 RETIRE per DEC-PTP-001.\n"
        "\n"
        "## ATTEND\n"
        "\n"
        "| Slug | Name | Score |\n"
        "|---|---|---|\n"
        "| `alpha` | Alpha Repo | 18 |\n"
        "| `bravo` | Bravo Repo | 16 |\n"
        "\n"
        "## RETIRE\n"
        "\n"
        "| Slug | Name | Score |\n"
        "|---|---|---|\n"
        "| `zulu` | zulu | 2 |\n"
        "\n"
        "## FREEZE\n"
        "\n"
        "| Slug | Name | Score |\n"
        "|---|---|---|\n"
        "| `charlie` | charlie | 10 |\n"
    )
    assert render_rollup(_rollup(freeze), _REGISTRY) == expected
