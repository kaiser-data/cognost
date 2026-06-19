"""Shared config and helpers for the BrainFlow Company Brain.

Two-tier memory (per the hackathon brief):
  - Session memory  : ephemeral per-run Q&A events + feedback  -> brain/session/*.jsonl
  - Permanent graph : the durable Cognee graph + the wiki/ pages it is built from

Self-improvement = distilling scored session feedback into the permanent graph via
cognee.improve(), plus explicitly applying a proposed rewrite of the maintainer skill.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent          # .../Cognost
BRAIN = ROOT / "brain"
RAW_DIR = ROOT / "raw"
WIKI_DIR = ROOT / "wiki"
SKILLS_DIR = BRAIN / "skills"
SESSION_DIR = BRAIN / "session"
PROPOSALS_DIR = BRAIN / "proposals"
EVIDENCE_DIR = BRAIN / "evidence"

for d in (SESSION_DIR, PROPOSALS_DIR, EVIDENCE_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Load the project .env (LLM_PROVIDER=ollama, the cognee-distilled model, etc.)
load_dotenv(ROOT / ".env")

DATASET = "brainflow"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_skill(name: str = "wiki-maintainer") -> str:
    """Load a maintainer skill (a Markdown file that defines agent behavior)."""
    p = SKILLS_DIR / f"{name}.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def session_append(session_id: str, event: dict) -> None:
    """Write one event to the ephemeral session-memory log."""
    event = {"ts": now(), **event}
    with (SESSION_DIR / f"{session_id}.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def extract_answer(recall_result) -> tuple[str, str | None]:
    """Pull (answer_text, qa_id) out of a cognee.recall() response list."""
    if isinstance(recall_result, str):
        return recall_result, None
    text_parts, qa_id = [], None
    for entry in recall_result or []:
        ans = getattr(entry, "answer", None) or getattr(entry, "text", None)
        if ans:
            text_parts.append(ans if isinstance(ans, str) else str(ans))
        qa_id = qa_id or getattr(entry, "qa_id", None) or getattr(entry, "entry_id", None)
    return ("\n".join(text_parts).strip() or str(recall_result)), qa_id


# --- Scoring rubric -----------------------------------------------------------
# A good stakeholder-wiki answer (CLAUDE.md §3, §7-Query) must:
#   1. cite at least one source document,
#   2. surface the disagreement when the topic is contested (name both sides),
#   3. state which value is current vs. superseded where relevant.
# Deterministic so the demo's before/after is reproducible with a small local model.

_SOURCE_RE = re.compile(r"\b[\w-]+\.md\b|\bADR-\d+\b|PRD\b|Decision Log\b|Roadmap\b|OKR\b", re.I)


def score_answer(answer: str, expect_terms: list[str], expect_conflict: bool) -> dict:
    a = (answer or "").lower()
    cited = bool(_SOURCE_RE.search(answer or ""))
    hit_terms = [t for t in expect_terms if t.lower() in a]
    # The conflict is "surfaced" if the answer either names it explicitly OR reports both of the
    # opposing values (expect_terms for a contested topic ARE the values that disagree).
    surfaced_conflict = (
        any(w in a for w in ("contradic", "conflict", "disagree", "supersede", "stale",
                             "both", "however", "whereas", "but ", "vs"))
        or len(hit_terms) >= 2
    )
    states_currency = any(w in a for w in ("current", "superseded", "now", "reverted"))

    score = 0
    score += 3 if cited else 0
    score += 3 if (len(hit_terms) >= max(2, len(expect_terms) - 1)) else (1 if hit_terms else 0)
    if expect_conflict:
        score += 3 if surfaced_conflict else 0
        score += 1 if states_currency else 0
    else:
        score += 4 if hit_terms else 0
    score = min(score, 10)

    notes = []
    notes.append("cited a source" if cited else "NO source citation")
    notes.append(f"matched {len(hit_terms)}/{len(expect_terms)} key facts")
    if expect_conflict:
        notes.append("surfaced the disagreement" if surfaced_conflict else "MISSED the disagreement")
        notes.append("stated current-vs-superseded" if states_currency else "did not state currency")
    return {"score": score, "cited": cited, "surfaced_conflict": surfaced_conflict,
            "states_currency": states_currency, "hit_terms": hit_terms, "notes": "; ".join(notes)}
