"""Build brain/evidence/before-after.md from the before/after query runs.

Shows the measurable improvement the brain gained by distilling its own scored feedback into a
better maintainer skill (the self-improvement the hackathon judges).
"""
from __future__ import annotations

import json

from common import EVIDENCE_DIR


def load(tag: str) -> dict | None:
    p = EVIDENCE_DIR / f"run-{tag}.json"
    return json.loads(p.read_text()) if p.exists() else None


def main() -> None:
    before, after = load("before"), load("after")
    if not (before and after):
        raise SystemExit("need run-before.json and run-after.json (run query.py --tag before/after)")

    b = {r["issue"]: r for r in before["results"]}
    a = {r["issue"]: r for r in after["results"]}

    L = ["# Self-Improvement Evidence — Before vs After", "",
         f"- **Before** · skill `{before['skill']}` → avg **{before['avg_score']}/10**",
         f"- **After**  · skill `{after['skill']}` → avg **{after['avg_score']}/10**",
         f"- **Δ avg score: {round(after['avg_score'] - before['avg_score'], 2):+}**", "",
         "The brain scored its own answers, recorded the failures as session feedback, distilled "
         "them into the permanent graph (`cognee.improve`), and adopted the operating rules that "
         "would have fixed them (skill rewrite, applied explicitly). No question text changed.", "",
         "| Issue | Before | After | Δ | What improved |",
         "| --- | --- | --- | --- | --- |"]
    for issue in sorted(b):
        bs, as_ = b[issue]["score"], a.get(issue, {}).get("score", 0)
        gained = []
        if not b[issue]["cited"] and a.get(issue, {}).get("cited"):
            gained.append("now cites a source")
        if not b[issue]["surfaced_conflict"] and a.get(issue, {}).get("surfaced_conflict"):
            gained.append("now surfaces the disagreement")
        if not b[issue]["states_currency"] and a.get(issue, {}).get("states_currency"):
            gained.append("now states current-vs-superseded")
        L.append(f"| {issue} | {bs}/10 | {as_}/10 | {as_-bs:+} | {', '.join(gained) or '—'} |")

    L += ["", "## Sample answers", ""]
    for issue in sorted(b):
        L += [f"### [{issue}] {b[issue]['q']}",
              f"**Before ({b[issue]['score']}/10):** {b[issue]['answer'][:400]}", "",
              f"**After ({a.get(issue,{}).get('score','?')}/10):** {a.get(issue,{}).get('answer','')[:400]}", ""]

    out = EVIDENCE_DIR / "before-after.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L[:9]))
    print(f"\n✓ wrote {out}")


if __name__ == "__main__":
    main()
