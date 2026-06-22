"""Validate `rubric/thesis-alive.yaml` against the five-factor closure
of DEC-PTP-001.

Checks per R-PTP-003 / R-PTP-004:
- The rubric declares exactly the five named factors (no more, no
  less): `model-release-impact`, `oss-competition`, `paper-drift`,
  `recent-run-evidence`, `decision-freshness`.
- Each factor's `rules` array covers scores {0,1,2,3,4} exactly once.
- Every rule has a non-empty `condition`.

Exits 0 on success, 1 on any failure.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
RUBRIC_PATH = REPO_ROOT / "rubric" / "thesis-alive.yaml"

REQUIRED_FACTORS = {
    "model-release-impact",
    "oss-competition",
    "paper-drift",
    "recent-run-evidence",
    "decision-freshness",
}
REQUIRED_SCORES = {0, 1, 2, 3, 4}


def main() -> int:
    if not RUBRIC_PATH.is_file():
        print(f"validate_rubric: missing rubric {RUBRIC_PATH}", file=sys.stderr)
        return 1

    with RUBRIC_PATH.open("r", encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)

    if not isinstance(doc, dict) or "factors" not in doc:
        print(
            f"validate_rubric: {RUBRIC_PATH}: top-level must be a mapping with `factors`",
            file=sys.stderr,
        )
        return 1

    factors = doc["factors"]
    if not isinstance(factors, dict):
        print("validate_rubric: `factors` must be a mapping", file=sys.stderr)
        return 1

    declared = set(factors.keys())
    if declared != REQUIRED_FACTORS:
        missing = REQUIRED_FACTORS - declared
        extra = declared - REQUIRED_FACTORS
        msg_parts = []
        if missing:
            msg_parts.append(f"missing: {sorted(missing)}")
        if extra:
            msg_parts.append(f"unexpected: {sorted(extra)}")
        print(
            "validate_rubric: factor closure violated ("
            + "; ".join(msg_parts)
            + ")",
            file=sys.stderr,
        )
        return 1

    for factor_name, factor in factors.items():
        if not isinstance(factor, dict):
            print(
                f"validate_rubric: factor {factor_name!r} must be a mapping",
                file=sys.stderr,
            )
            return 1

        rules = factor.get("rules")
        if not isinstance(rules, list):
            print(
                f"validate_rubric: factor {factor_name!r} missing `rules` list",
                file=sys.stderr,
            )
            return 1

        scores_seen: list[int] = []
        for rule in rules:
            if not isinstance(rule, dict):
                print(
                    f"validate_rubric: {factor_name}: rule must be a mapping",
                    file=sys.stderr,
                )
                return 1
            score = rule.get("score")
            condition = rule.get("condition")
            if not isinstance(score, int) or score not in REQUIRED_SCORES:
                print(
                    f"validate_rubric: {factor_name}: rule has invalid score {score!r}",
                    file=sys.stderr,
                )
                return 1
            if not isinstance(condition, str) or not condition.strip():
                print(
                    f"validate_rubric: {factor_name}: score {score} has empty condition",
                    file=sys.stderr,
                )
                return 1
            scores_seen.append(score)

        if set(scores_seen) != REQUIRED_SCORES or len(scores_seen) != 5:
            print(
                f"validate_rubric: {factor_name}: rules must cover {{0,1,2,3,4}} exactly once "
                f"(saw {scores_seen})",
                file=sys.stderr,
            )
            return 1

    print(f"validate_rubric: {len(factors)} factor(s) ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
