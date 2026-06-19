"""Step 2b — SELF-IMPROVE (distill session feedback into the permanent brain).

The loop the hackathon judges (session memory -> permanent graph distillation):

  1. read scored Q&A feedback from session memory (written by query.py)
  2. distill it into the permanent graph         -> cognee.improve(session_ids=[...])
  3. synthesize a PROPOSED maintainer-skill rewrite from the observed failures, sourcing each
     new rule from the CLAUDE.md schema           -> brain/proposals/  (NOT applied)
  4. apply the proposal explicitly on request     -> brain/skills/wiki-maintainer.md

    python brain/selfimprove.py --from-tag before        # distill + write a proposal
    python brain/selfimprove.py --apply <proposal-file>  # explicitly adopt a proposal
"""
from __future__ import annotations

import argparse
import asyncio
import json
import shutil

import cognee

from common import DATASET, PROPOSALS_DIR, SESSION_DIR, SKILLS_DIR, now

# Governing policies, lifted verbatim-in-spirit from CLAUDE.md §3/§7/§9. Each is keyed by the
# rubric dimension whose failure should teach it. This is what "learning from feedback" means
# here: the brain adopts the operating rule that would have fixed its low-scoring answers.
POLICY_LIBRARY = {
    "cite": ("## Provenance is mandatory (CLAUDE.md §3.1)\n"
             "Every claim cites its source document and date, e.g. `(PRD §Scope, 2026-01-22)`.\n"
             "A claim with no traceable source is not stated."),
    "conflict": ("## Preserve contradictions; never silently resolve them (CLAUDE.md §3.2)\n"
                 "When sources disagree, present BOTH with provenance and name the conflict.\n"
                 "Do not pick a winner by guessing — the disagreement is the information the\n"
                 "stakeholder needs."),
    "currency": ("## Always state current vs. superseded (CLAUDE.md §3.6)\n"
                 "Say which value is current, what it superseded, and the date. Never present a\n"
                 "superseded fact as live."),
}
ROLE = ("# Skill: BrainFlow stakeholder-alignment wiki maintainer\n\n"
        "You maintain a wiki whose job is not to store documents but to surface where the\n"
        "documents disagree, track which decisions are current, and flag what has no owner.\n"
        "A correct answer tells a stakeholder what is true *now*, what it superseded, and where\n"
        "sources still conflict. Answer plainly; the authority comes from being traceable and\n"
        "honest about disagreement (CLAUDE.md §9).\n")


def _load_session(tag: str) -> list[dict]:
    p = SESSION_DIR / f"q-{tag}.jsonl"
    if not p.exists():
        raise SystemExit(f"no session memory at {p} — run query.py --tag {tag} first")
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def _diagnose(events: list[dict]) -> dict:
    qa = [e for e in events if e.get("kind") == "qa"]
    fail = {
        "cite": sum(1 for e in qa if not e.get("cited")),
        "conflict": sum(1 for e in qa if e.get("expect_conflict", True) and not e.get("surfaced_conflict")),
        "currency": sum(1 for e in qa if not e.get("states_currency")),
    }
    avg = round(sum(e["score"] for e in qa) / max(len(qa), 1), 2)
    return {"n": len(qa), "avg": avg, "fail": fail}


def propose(tag: str) -> dict:
    events = _load_session(tag)
    diag = _diagnose(events)
    # Adopt a policy whenever that failure showed up at all.
    chosen = [k for k in ("cite", "conflict", "currency") if diag["fail"][k] > 0]
    skill_text = ROLE + "\n" + "\n\n".join(POLICY_LIBRARY[k] for k in chosen) + "\n"
    fname = f"wiki-maintainer.{now().replace(':', '').replace('-', '')}.md"
    (PROPOSALS_DIR / fname).write_text(skill_text, encoding="utf-8")

    rationale = {
        "from_session": f"q-{tag}", "diagnosis": diag,
        "policies_added": chosen,
        "reason": {k: f"{diag['fail'][k]} answer(s) failed the '{k}' rubric dimension" for k in chosen},
        "proposal_file": f"brain/proposals/{fname}", "applied": False,
    }
    (PROPOSALS_DIR / (fname + ".rationale.json")).write_text(json.dumps(rationale, indent=2))
    print(f"· diagnosed run q-{tag}: avg {diag['avg']}/10, failures {diag['fail']}")
    print(f"· PROPOSAL written (not applied): brain/proposals/{fname}")
    print(f"  adopts policies: {', '.join(chosen) or '(none — already healthy)'}")
    print(f"  to apply: python brain/selfimprove.py --apply {fname}")
    return rationale


async def distill(tag: str) -> None:
    """Distill the scored session into the permanent graph (the self-improvement step)."""
    session_id = f"q-{tag}"
    print(f"· distilling session '{session_id}' into the permanent graph via cognee.improve() …")
    try:
        await cognee.improve(dataset=DATASET, session_ids=[session_id])
        print("  ✓ permanent graph updated from session feedback")
    except Exception as e:
        print(f"  (improve skipped: {e})")


def apply(proposal_file: str) -> None:
    src = PROPOSALS_DIR / proposal_file
    if not src.exists():
        raise SystemExit(f"no such proposal: {src}")
    active = SKILLS_DIR / "wiki-maintainer.md"
    archive = SKILLS_DIR / "archive" / f"wiki-maintainer.replaced-{now().replace(':', '')}.md"
    archive.parent.mkdir(exist_ok=True)
    shutil.copy(active, archive)
    shutil.copy(src, active)
    rationale = src.with_suffix(src.suffix + ".rationale.json")
    if rationale.exists():
        r = json.loads(rationale.read_text()); r["applied"] = True
        rationale.write_text(json.dumps(r, indent=2))
    print(f"✓ applied {proposal_file} -> brain/skills/wiki-maintainer.md")
    print(f"  previous skill archived at {archive.relative_to(SKILLS_DIR.parent.parent)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-tag", default="before", help="session tag to learn from")
    ap.add_argument("--apply", metavar="PROPOSAL", help="explicitly adopt a proposal file")
    ap.add_argument("--no-distill", action="store_true", help="skip cognee.improve() distillation")
    args = ap.parse_args()
    if args.apply:
        apply(args.apply)
    else:
        if not args.no_distill:
            asyncio.run(distill(args.from_tag))
        propose(args.from_tag)
