# Cognost — a self-improving stakeholder-alignment Company Brain

> Cognee Cloud Hackathon · 2026-06-19

Most "chat with your docs" tools paper over disagreement — they pick one source and sound
confident. **Cognost does the opposite.** It ingests a product team's scattered documents, answers
questions **with citations while surfacing where the docs disagree**, tracks which decisions are
current vs. superseded, flags what has no owner, and **improves its own answering behaviour from
feedback**.

Built on [Cognee](https://github.com/topoteretes/cognee) `1.2.0.dev1`. Runs on OpenAI by default
(local Ollama path included), Cognee-Cloud-ready.

## The three operations

```bash
python brain/ingest.py --reset      # 1 INGEST  → permanent knowledge graph
python brain/query.py  --tag run    # 2 QUERY   → cited, conflict-aware answers
python brain/selfimprove.py --from-tag run   #   + SELF-IMPROVE (distil feedback → graph)
python brain/lint.py                # 3 LINT    → contradictions / supersessions / orphans
```

One-shot end-to-end demo: **`bash brain/run_demo.sh`**.

## Architecture — two-tier memory

| Tier | What lives here | Where |
| --- | --- | --- |
| **Session memory** (ephemeral) | raw Q&A events, scores, feedback per run | `brain/session/*.jsonl` + Cognee session |
| **Permanent graph** (durable) | entities, typed relationships, summaries, the synthesised wiki | Cognee graph + [`wiki/`](wiki/) |

**Self-improvement = distilling scored session feedback into the permanent graph**
(`cognee.improve`) plus an explicit, reviewable rewrite of the maintainer *skill* — the brain
learns its own operating rules from its mistakes, sourcing them from the [`CLAUDE.md`](CLAUDE.md)
schema. See [`SUBMISSION.md`](SUBMISSION.md) for the full loop and before/after evidence.

## What's in here

| Path | What |
| --- | --- |
| [`brain/`](brain/) | the runnable Cognee pipeline (ingest / query / self-improve / lint) — see [`brain/README.md`](brain/README.md) |
| [`wiki/`](wiki/) | the human-readable wiki: overview, contradiction register, topic & source pages |
| [`raw/`](raw/) | the BrainFlow source documents (12 docs, 11 planted misalignments) |
| [`CLAUDE.md`](CLAUDE.md) | the maintainer contract (provenance, never silently resolve a contradiction, current-vs-superseded) |
| [`SUBMISSION.md`](SUBMISSION.md) | hackathon write-up |
| [`DATASET.md`](DATASET.md) | notes on the synthetic dataset and its planted issues |

## The dataset

[BrainFlow](DATASET.md) is a mental-fitness app for stressed professionals (DACH market). Its 12
docs (PRD, ADRs, roadmap, decision log, OKRs, sales commitments, GTM, specs, RACI) contain **11
deliberately planted contradictions and supersessions** — e.g. the PRD marks "AI Daily Pick" as
*Won't have* while the roadmap, a PM decision, and the design all ship it. Cognost's job is to
catch exactly these.

## Quickstart

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.template .env        # add your OpenAI key
bash brain/run_demo.sh
```

## Cognee Cloud (bonus)

Add `COGNEE_CLOUD_URL` / `COGNEE_CLOUD_API_KEY` to `.env`, then:

```bash
python brain/ingest.py --reset --push   # builds locally and pushes the dataset to your Cloud instance
```
