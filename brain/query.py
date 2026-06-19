"""Step 2a — QUERY (and capture feedback into session memory).

Runs the canonical demo queries through the currently-active maintainer skill, scores each
answer against the rubric (cite a source / surface the disagreement / state current-vs-superseded),
and records a FeedbackEntry chained to each answer's qa_id. Nothing is distilled yet — that is
brain/selfimprove.py (Step 2b).

    python brain/query.py                                   # use the active skill
    python brain/query.py --skill archive/wiki-maintainer.v1-baseline   # use a specific skill
    python brain/query.py --tag before                      # label the run (for evidence)
"""
from __future__ import annotations

import argparse
import asyncio
import json

import cognee
from cognee.modules.search.types import SearchType

from common import (DATASET, EVIDENCE_DIR, extract_answer, load_skill,
                    score_answer, session_append)
from queries import QUERIES


MODES = {"graph": SearchType.GRAPH_COMPLETION, "rag": SearchType.RAG_COMPLETION}


async def run(skill_name: str, tag: str, mode: str = "graph") -> dict:
    skill = load_skill(skill_name) or "Answer the question."
    session_id = f"q-{tag}"
    query_type = MODES.get(mode, SearchType.GRAPH_COMPLETION)
    print(f"\n=== QUERY run [{tag}] · skill='{skill_name}' · mode={mode} ===")
    results, total = [], 0
    for item in QUERIES:
        q = item["q"]
        try:
            res = await cognee.recall(
                query_text=q,
                query_type=query_type,
                datasets=[DATASET],
                system_prompt=skill,
                session_id=session_id,
            )
            answer, qa_id = extract_answer(res)
        except Exception as e:                       # keep the demo resilient
            answer, qa_id = f"[recall error: {e}]", None

        sc = score_answer(answer, item["expect_terms"], item["expect_conflict"])
        total += sc["score"]
        print(f"\n[{item['issue']}] {q}\n  → {answer[:280].replace(chr(10), ' ')}")
        print(f"  score {sc['score']}/10 — {sc['notes']}")

        # session memory: the raw Q&A event + the score
        session_append(session_id, {"kind": "qa", "issue": item["issue"], "q": q,
                                    "answer": answer, "qa_id": qa_id, **sc})

        # record feedback to Cognee, chained to this answer (does NOT modify the graph yet)
        if qa_id:
            try:
                await cognee.remember(
                    cognee.FeedbackEntry(qa_id=qa_id, feedback_text=sc["notes"],
                                         feedback_score=sc["score"]),
                    dataset_name=DATASET, session_id=session_id,
                )
            except Exception as e:
                print(f"    (feedback not recorded: {e})")
        results.append({"issue": item["issue"], "q": q, "answer": answer, **sc})

    avg = round(total / len(QUERIES), 2)
    print(f"\n=== run [{tag}] average score: {avg}/10 ===")
    summary = {"tag": tag, "skill": skill_name, "mode": mode, "session_id": session_id,
               "avg_score": avg, "results": results}
    (EVIDENCE_DIR / f"run-{tag}.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", default="wiki-maintainer", help="skill name under brain/skills/")
    ap.add_argument("--tag", default="run", help="label for this run (e.g. before/after)")
    ap.add_argument("--mode", default="graph", choices=["graph", "rag"],
                    help="graph=GRAPH_COMPLETION (graph memory), rag=RAG_COMPLETION (naive chunks)")
    args = ap.parse_args()
    asyncio.run(run(args.skill, args.tag, args.mode))
