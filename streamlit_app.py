"""portfolio-thesis-plane — live demo (Streamlit Community Cloud).

Reads the committed registry (registry/repos.yaml) and the latest committed
signals week (signals/*.yaml), scores every repo against the 5-factor
thesis-alive rubric, applies the forced top-2 ATTEND / bottom-3 RETIRE
mechanic, and renders a ranked scorecard. No network, no secrets — runs
entirely off committed files via the local package.

Deploy: Streamlit Community Cloud -> New app -> repo
AthenaTheOwl/portfolio-thesis-plane, branch main, main file streamlit_app.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

REPO = Path(__file__).resolve().parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from portfolio_thesis_plane import loader  # noqa: E402
from portfolio_thesis_plane.score import (  # noqa: E402
    FACTOR_NAMES,
    build_rollup,
    score_repo,
)


def _sub_scores(repo_signals: dict | None) -> dict[str, int]:
    raw = (repo_signals or {}).get("scores") or {}
    return {name: int(raw.get(name, 0)) for name in FACTOR_NAMES}


st.set_page_config(page_title="portfolio-thesis-plane", layout="wide")
st.title("portfolio-thesis-plane")
st.caption(
    "weekly thesis-alive scorecard across the AthenaTheOwl portfolio. each repo "
    "scores 0..20 on five typed factors; a forced top-2 ATTEND / bottom-3 RETIRE "
    "mechanic decides where attention goes."
)

try:
    week = loader.latest_week()
    registry = loader.load_registry()
    signals = loader.load_signals(week)
except FileNotFoundError as exc:
    st.warning(f"no committed signals found: {exc}")
    st.stop()

name_by_slug = {e["slug"]: e.get("name", e["slug"]) for e in registry}
thesis_by_slug = {e["slug"]: (e.get("thesis_statement") or "").strip() for e in registry}

scored: list[dict] = []
totals: list[tuple[str, int]] = []
for entry in registry:
    slug = entry["slug"]
    result = score_repo(slug, week, _sub_scores(signals.get(slug)))
    scored.append(result)
    totals.append((slug, result["total"]))

rollup = build_rollup(week, totals)
verdict_by_slug: dict[str, str] = {}
for bucket, verdict in (("attend", "ATTEND"), ("freeze", "FREEZE"), ("retire", "RETIRE")):
    for item in rollup[bucket]:
        verdict_by_slug[item["repo_slug"]] = verdict

ranked = sorted(scored, key=lambda s: (-s["total"], s["repo_slug"]))
n_repos = len(scored)
n_dormant = sum(1 for s in scored if s["total"] == 0)
top = ranked[0]

st.subheader(f"week {week}")

c1, c2, c3 = st.columns(3)
c1.metric("repos scored", n_repos)
c2.metric("top score", f"{top['total']}/20", help=name_by_slug[top["repo_slug"]])
c3.metric("dormant (score 0)", n_dormant, help="zero run-evidence and zero on every factor")

verdict_filter = st.multiselect(
    "show verdicts",
    options=["ATTEND", "FREEZE", "RETIRE"],
    default=["ATTEND", "FREEZE", "RETIRE"],
)

shown = [s for s in ranked if verdict_by_slug[s["repo_slug"]] in verdict_filter]

rows = []
for rank, s in enumerate(ranked, start=1):
    slug = s["repo_slug"]
    if verdict_by_slug[slug] not in verdict_filter:
        continue
    fs = s["factor_scores"]
    rows.append(
        {
            "#": rank,
            "repo": name_by_slug[slug],
            "score /20": s["total"],
            "verdict": verdict_by_slug[slug],
            "release": fs["model-release-impact"],
            "oss": fs["oss-competition"],
            "paper": fs["paper-drift"],
            "run-evidence": fs["recent-run-evidence"],
            "decision": fs["decision-freshness"],
        }
    )

st.dataframe(rows, use_container_width=True, hide_index=True)

attend_names = [name_by_slug[i["repo_slug"]] for i in rollup["attend"]]
retire_names = [name_by_slug[i["repo_slug"]] for i in rollup["retire"]]
st.info(
    f"**headline:** {name_by_slug[top['repo_slug']]} leads at {top['total']}/20. "
    f"ATTEND is forced onto {', '.join(attend_names)}; {n_dormant} of {n_repos} repos "
    f"score 0, so the bottom-3 RETIRE bucket is {', '.join(retire_names)}. "
    f"the mechanic spends attention every week even when no repo clears the ATTEND band."
)

with st.expander("thesis statements for the ATTEND repos"):
    for item in rollup["attend"]:
        slug = item["repo_slug"]
        st.markdown(f"**{name_by_slug[slug]}** — {thesis_by_slug.get(slug) or '(no thesis on file)'}")

# ---------------------------------------------------------------------------
# Run the real scoring engine live. This is not a viewer — the sliders below
# call portfolio_thesis_plane.score.score_repo (the same function that scored
# the committed week) and then re-run build_rollup with your repo injected, so
# you can watch the forced top-2 ATTEND / bottom-3 RETIRE mechanic re-decide.
# ---------------------------------------------------------------------------
st.divider()
st.subheader("score a repo yourself")
st.caption(
    "drive the actual rubric engine — `portfolio_thesis_plane.score.score_repo` "
    "+ `build_rollup` — with your own per-factor signals. set the five factors, "
    "watch the total, verdict, and the forced ATTEND/RETIRE rollup recompute live."
)

FACTOR_HELP = {
    "model-release-impact": "recent foundation-model releases that strengthen or invalidate the bet",
    "oss-competition": "open-source competitors crossing a visibility or capability threshold",
    "paper-drift": "recent papers that confirm or undercut the approach",
    "recent-run-evidence": "real work (runs, briefs, artifacts) that landed in the repo in 30 days",
    "decision-freshness": "how recently an architectural decision (DEC) was revised",
}

your_name = st.text_input("your repo name", value="my-new-bet")

cols = st.columns(len(FACTOR_NAMES))
your_factors: dict[str, int] = {}
for col, factor in zip(cols, FACTOR_NAMES):
    with col:
        your_factors[factor] = st.slider(
            factor, 0, 4, 2, help=FACTOR_HELP.get(factor)
        )

try:
    from portfolio_thesis_plane.score import verdict_for_total

    your_result = score_repo("__yours__", week, your_factors)
    your_total = your_result["total"]
    your_verdict_candidate = verdict_for_total(your_total)

    m1, m2, m3 = st.columns(3)
    m1.metric("your total", f"{your_total}/20")
    m2.metric("candidate band", your_verdict_candidate, help="before the forced rollup")
    m3.metric("vs. top repo", f"{your_total - top['total']:+d}", help=f"top is {name_by_slug[top['repo_slug']]} at {top['total']}/20")

    # Re-run the real rollup with the user's repo injected into the portfolio.
    injected_totals = [(slug, t) for slug, t in totals] + [("__yours__", your_total)]
    new_rollup = build_rollup(week, injected_totals)
    new_verdict_by_slug: dict[str, str] = {}
    for bucket, verdict in (("attend", "ATTEND"), ("freeze", "FREEZE"), ("retire", "RETIRE")):
        for item in new_rollup[bucket]:
            new_verdict_by_slug[item["repo_slug"]] = verdict
    your_forced_verdict = new_verdict_by_slug["__yours__"]

    if your_forced_verdict == "ATTEND":
        st.success(
            f"with these signals your repo lands **ATTEND** ({your_total}/20) — it forces "
            f"its way into the top-2 attention band this week."
        )
    elif your_forced_verdict == "RETIRE":
        st.error(
            f"with these signals your repo lands **RETIRE** ({your_total}/20) — it falls into "
            f"the forced bottom-3. raise run-evidence or decision-freshness to climb out."
        )
    else:
        st.warning(
            f"with these signals your repo lands **FREEZE** ({your_total}/20) — alive but not "
            f"forced into the attention band. push two factors up to contend for ATTEND."
        )

    # Show whom the user displaced from ATTEND, if anyone.
    old_attend = {i["repo_slug"] for i in rollup["attend"]}
    new_attend = {i["repo_slug"] for i in new_rollup["attend"] if i["repo_slug"] != "__yours__"}
    displaced = old_attend - new_attend
    if your_forced_verdict == "ATTEND" and displaced:
        st.caption(
            "injecting your repo pushed "
            + ", ".join(name_by_slug.get(s, s) for s in sorted(displaced))
            + " out of the ATTEND band."
        )

    st.caption(
        "the score, the verdict, and the rollup above are all computed by the real "
        "`score_repo` / `build_rollup` functions — not a lookup. move a slider and the "
        "forced top-2 / bottom-3 mechanic re-decides."
    )
except Exception as exc:  # pragma: no cover - defensive for cloud import differences
    st.info(f"interactive scoring needs the package importable ({exc}). the scorecard above still renders.")

st.caption(
    "scoring lives in `portfolio_thesis_plane/`; this page reads the committed "
    "`registry/repos.yaml` + latest `signals/*.yaml`, and the section above drives "
    "the real scorer. repo: github.com/AthenaTheOwl/portfolio-thesis-plane"
)
