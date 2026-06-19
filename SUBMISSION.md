# Cognost — a self-improving stakeholder-alignment Company Brain

**Cognee Cloud Hackathon · 2026-06-19**

## One-liner
A Company Brain for a product team that doesn't just *store* docs — it **surfaces where the docs
disagree**, tracks which decisions are current, flags what has no owner, and **improves its own
answering behavior from feedback**.

## The idea
Every product org has the same failure mode: the PRD says one thing, the roadmap drifted, Sales
signed a contradicting promise, and the design shipped a feature marked "Won't have." The truth
is *knowable* but scattered across a dozen documents written by seven stakeholders. A normal RAG
bot papers over this — it picks one source and sounds confident. **Cognost is built to do the
opposite: preserve the contradiction, cite both sides, and say which version is current.**

We use the synthetic **BrainFlow** dataset (12 product docs with 11 planted misalignments) as the
team knowledge. The brain's operating contract is `CLAUDE.md` (provenance mandatory, never
silently resolve a contradiction, always state current-vs-superseded).

## Architecture — two-tier memory
| Tier | What lives here | In this project |
| --- | --- | --- |
| **Session memory** (ephemeral) | raw Q&A events, scores, feedback per run | `brain/session/*.jsonl` + Cognee session (`session_id`) |
| **Permanent graph** (durable) | entities, typed relationships, summaries, the synthesized wiki | Cognee graph (`cognee.cognify`) + `wiki/` pages |

**Self-improvement = distillation from session → permanent**, via `cognee.improve(session_ids=…)`
plus an explicit rewrite of the maintainer *skill* learned from scored feedback.

## The three operations
```bash
python brain/ingest.py --reset --raw-only          # 1 INGEST  → permanent graph
python brain/query.py  --tag run                    # 2 QUERY   → cited, conflict-aware answers
python brain/selfimprove.py --from-tag run          #   IMPROVE → distill + propose skill rewrite
python brain/lint.py                                # 3 LINT    → contradictions / orphans report
```
One-shot: `bash brain/run_demo.sh`.

## The self-improvement loop (what the judges asked for)
The hackathon's skill cycle — *remember skill → run → score → record feedback (propose, don't
apply) → apply explicitly* — maps 1:1 onto the native Cognee 1.2 API:

1. **Remember skill** — the maintainer skill (`brain/skills/wiki-maintainer.md`) is loaded as the
   `system_prompt` for `cognee.recall`.
2. **Run** — `recall(query, GRAPH_COMPLETION, session_id=…)` answers from the permanent graph and
   writes the interaction to **session memory**.
3. **Score** — a deterministic rubric (cited a source? surfaced the disagreement? stated
   current-vs-superseded?) scores each answer 0–10.
4. **Record feedback (propose, don't apply)** — failures are written to session memory and chained
   to Cognee via `FeedbackEntry(qa_id, score, text)`. `selfimprove.py` then **diagnoses which
   rubric dimensions failed** and writes a **proposed** new skill — adopting the exact `CLAUDE.md`
   policy that would have fixed each failure — to `brain/proposals/` **without applying it**.
5. **Apply explicitly** — `selfimprove.py --apply <proposal>` swaps it into the active skill
   (archiving the previous one). `cognee.improve(session_ids=…)` distills the scored session into
   the permanent graph.

The brain literally **learns its own operating rules from its mistakes**, sourcing them from the
schema rather than inventing them.

## Before / after evidence
See `brain/evidence/before-after.md` (generated). Same questions, no question text changed:

<!-- EVIDENCE -->
_(populated by `python brain/evidence.py` after a run)_

The "after" answers gain source citations, surface the planted contradictions, and state which
value is current — exactly the behaviors the baseline skill omitted.

## Lint (the alignment money-shot)
`brain/evidence/lint-report.md` catches all 11 planted issues: 6 live contradictions, 2
superseded-but-still-referenced decisions, metric drift, 4 ownership orphans, and a
spec-vs-design gap — each with provenance and the current value. Decisions are **reported, never
auto-resolved** (`CLAUDE.md` §7).

## Cognee Cloud
`python brain/ingest.py --push` pushes the dataset to a Cloud instance
(`COGNEE_CLOUD_URL` / `COGNEE_CLOUD_API_KEY`) without restructuring the code — qualifies for the
Cloud bonus.

## Stack
Cognee `1.2.0.dev1`, local Ollama (cognee-distilled extraction model + `nomic-embed-text`), no
cloud key required to run. Python 3.12.

## Run it
```bash
cd Cognost && uv venv && source .venv/bin/activate
uv pip install "cognee==1.2.0.dev1" transformers
bash brain/run_demo.sh
```
