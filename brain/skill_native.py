"""Reference implementation of the self-improvement loop on Cognee's NATIVE skill API.

This mirrors brain/selfimprove.py but uses the first-class primitives directly:
  - record each scored answer as a SkillRunEntry (graph-backed) via cognee.remember()
  - propose a rewrite from the low-scoring runs via improve_skill(apply=False)
  - adopt it via improve_skill(apply=True, proposal_id=...)

See brain/SKILL_API_ALIGNMENT.md for the 1:1 mapping. Run:

    python brain/skill_native.py --skill wiki-maintainer --record --propose
    python brain/skill_native.py --skill wiki-maintainer --apply <proposal_id>
"""
from __future__ import annotations

import argparse
import asyncio
import time

import cognee
from cognee.memory import SkillRunEntry

from common import DATASET


async def record_run(skill_name: str, task: str, summary: str, score10: int) -> None:
    """Persist one scored skill execution to the graph (success_score normalised to [0,1])."""
    entry = SkillRunEntry(
        selected_skill_id=skill_name,
        task_text=task,
        result_summary=summary,
        success_score=max(0.0, min(1.0, score10 / 10.0)),
        feedback=(score10 / 10.0) * 2 - 1,          # 0..10  ->  -1..1
        started_at_ms=int(time.time() * 1000),
        node_set="skills",
    )
    await cognee.remember(entry=entry, dataset_name=DATASET)
    print(f"· recorded SkillRun for {skill_name!r}: score {score10}/10")


async def propose(skill_name: str) -> None:
    """Draft a SkillImprovementProposal from the recorded low-scoring runs (NOT applied)."""
    proposal = await cognee.remember(
        skill_improvement={
            "skill_name": skill_name,
            "apply": False,
            "score_threshold": 0.5,
            "max_runs": 5,
        },
        dataset_name=DATASET,
    )
    print("· proposal (not applied):", getattr(proposal, "proposal_id", proposal))


async def apply(skill_name: str, proposal_id: str) -> None:
    """Explicitly adopt a proposal — archives the previous procedure."""
    await cognee.remember(
        skill_improvement={"skill_name": skill_name, "apply": True, "proposal_id": proposal_id},
        dataset_name=DATASET,
    )
    print(f"✓ applied proposal {proposal_id} to {skill_name!r}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", default="wiki-maintainer")
    ap.add_argument("--record", action="store_true", help="record a sample low-scoring run")
    ap.add_argument("--propose", action="store_true", help="propose a rewrite from failures")
    ap.add_argument("--apply", metavar="PROPOSAL_ID", help="adopt a proposal explicitly")
    args = ap.parse_args()

    async def main():
        if args.record:
            await record_run(args.skill, "Is the AI Daily Pick in the MVP?",
                             "Answered 'yes' with no citation and no conflict surfaced.", 3)
        if args.propose:
            await propose(args.skill)
        if args.apply:
            await apply(args.skill, args.apply)

    asyncio.run(main())
