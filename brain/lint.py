"""Step 3 — LINT (deduplicate, resolve conflicts, prune stale; CLAUDE.md §7-Lint).

Computes the alignment checks from the wiki and writes brain/evidence/lint-report.md:
  - Contradictions          (incompatible live claims across sources)
  - Superseded-but-referenced (a superseded decision still cited as current somewhere)
  - Orphans / no owner       (Features/Pricing/tracks with no owner)
  - Open questions / risks
  - Metric drift             (same metric name, different definitions)
  - Spec-vs-design gaps

Reports; does not auto-fix decisions (§7). Exit code is the number of OPEN findings, so this
doubles as a CI gate. Use --ask to also route the lint prompt through the brain.

    python brain/lint.py
    python brain/lint.py --ask     # additionally ask the Cognee graph to lint itself
"""
from __future__ import annotations

import argparse
import asyncio
import re
from pathlib import Path

from common import WIKI_DIR

FM = re.compile(r"^---\n(.*?)\n---", re.S)


def _front_matter(text: str) -> dict:
    m = FM.match(text)
    fm: dict[str, str] = {}
    if not m:
        return fm
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "-", "#")):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"')
    return fm


def _topics() -> list[dict]:
    out = []
    for p in sorted((WIKI_DIR / "topics").glob("*.md")):
        fm = _front_matter(p.read_text(encoding="utf-8"))
        fm["_file"] = f"wiki/topics/{p.name}"
        out.append(fm)
    return out


def _register_rows() -> list[dict]:
    """Parse the summary table in contradictions.md (| # | Topic | Type | Current | ... |)."""
    text = (WIKI_DIR / "contradictions.md").read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 6 and re.fullmatch(r"[A-K]", cells[0]):
            rows.append({"id": cells[0], "topic": cells[1], "type": cells[2],
                         "current": cells[3], "conflicting": cells[4], "status": cells[5]})
    return rows


def build_report() -> tuple[str, int]:
    rows = _register_rows()
    topics = _topics()

    def by_type(*types):
        return [r for r in rows if any(t.lower() in r["type"].lower() for t in types)]

    contradictions = by_type("contradiction")
    supersessions = by_type("supersession")
    metric_drift = by_type("metric")
    gaps = by_type("gap")

    orphans = [t for t in topics
               if any(x in (t.get("owner", "") + t.get("current_value", "")).lower()
                      for x in ("(none)", "unassigned", "no source of truth", "no owner", "tbd"))]
    open_q = [t for t in topics if t.get("type") == "OpenQuestion" or t.get("status") == "open"]

    open_count = sum(1 for r in rows if r["status"] in ("open",))

    L = ["# BrainFlow Wiki — Lint Report", "",
         f"Generated from `wiki/` · {len(rows)} registered findings · **{open_count} open** (need a human).",
         "", "_Reports only; decisions are never auto-resolved (CLAUDE.md §7)._", ""]

    def section(title, items, render):
        L.append(f"## {title} ({len(items)})")
        if not items:
            L.append("- none")
        for it in items:
            L.append(render(it))
        L.append("")

    section("Contradictions — incompatible live claims", contradictions,
            lambda r: f"- **[{r['id']}] {r['topic']}** — current: {r['current']}. Conflicts: {r['conflicting']}. _({r['status']})_")
    section("Superseded but still referenced", supersessions,
            lambda r: f"- **[{r['id']}] {r['topic']}** — current: {r['current']}. Stale refs: {r['conflicting']}.")
    section("Metric drift — same name, different definition", metric_drift,
            lambda r: f"- **[{r['id']}] {r['topic']}** — {r['conflicting']}.")
    section("Orphans / no owner", orphans,
            lambda t: f"- **{t.get('title','?')}** ({t.get('type','?')}) — owner: {t.get('owner','?')}  ·  {t['_file']}")
    section("Open questions / risks", open_q,
            lambda t: f"- **{t.get('title','?')}** — {t.get('current_value','?')}  ·  {t['_file']}")
    section("Spec-vs-design gaps", gaps,
            lambda r: f"- **[{r['id']}] {r['topic']}** — {r['current']}.")

    return "\n".join(L), open_count


async def ask_brain() -> None:
    import cognee
    from cognee.modules.search.types import SearchType
    from common import DATASET
    prompt = ("Review the BrainFlow wiki. List (1) contradictions between documents, "
              "(2) decisions superseded but still referenced, (3) features/areas with no owner, "
              "(4) unresolved open questions. Cite the source documents and state which version is current.")
    print("· asking the brain to lint itself …")
    try:
        res = await cognee.recall(query_text=prompt, query_type=SearchType.GRAPH_COMPLETION,
                                  datasets=[DATASET])
        from common import extract_answer
        ans, _ = extract_answer(res)
        print("\n--- brain lint (LLM) ---\n" + ans + "\n")
    except Exception as e:
        print(f"  (brain lint skipped: {e})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ask", action="store_true", help="also route the lint prompt through Cognee")
    args = ap.parse_args()
    report, open_count = build_report()
    out = Path(__file__).resolve().parent / "evidence" / "lint-report.md"
    out.write_text(report, encoding="utf-8")
    print(report)
    print(f"\n✓ wrote {out.relative_to(out.parents[2])} — {open_count} open findings")
    if args.ask:
        asyncio.run(ask_brain())
    raise SystemExit(0 if open_count == 0 else 1)
