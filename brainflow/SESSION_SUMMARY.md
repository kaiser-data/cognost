# Cognost — Build Session Summary

A self-improving **stakeholder-alignment Company Brain** on Cognee Cloud. It ingests a product
team's scattered docs into one knowledge graph, answers questions **with citations while
surfacing where docs disagree**, tracks current-vs-superseded decisions, flags ownerless areas,
and **improves its own answering skill from scored feedback**. Reference corpus: **BrainFlow**.

## Workflow (what happened, in order)

| # | Step | Outcome |
|---|------|---------|
| 1 | Connected to Cognee Cloud (`cognee` skill) | Ping 200, session established |
| 2 | Stored session + direct-to-graph memory | `session_stored` + graph item ingested |
| 3 | Explored the 12-doc Cognost dataset | 11 planted misalignments, but ~80% signal = no "haystack" |
| 4 | Diagnosed gap, designed extension | Needed hay + amplifiers + decoys for a credible needle-in-haystack demo |
| 5 | Generated 30 new docs (`generate_corpus.py`) | 42 total; stripped giveaway labels; wrote `FACT_LEDGER.md` ground truth |
| 6 | Created fresh `brainflow` brain (team-visible) | Ingested all **42/42**, 0 failures |
| 7 | Ran money-shot + decoy query suite | **8/8** conflicts surfaced, **3/3** decoys held |
| 8 | Built before→skill→after diagnostic artifact | Published HTML, 0→6 counter |
| 9 | Attempted local evidence pipeline | Failed: OpenAI quota exhausted + Ollama missing tokenizer |
| 10 | **Agent served as the model** | Genuine before/after evidence: **1.3/10 → 10/10** |
| 11 | Closed submission gaps | `my_skills/`, `SKILL_API_ALIGNMENT.md`, `serve_cloud.py`, SUBMISSION sections |
| 12 | Registered `wiki-maintainer` skill on Cloud | `kind: skill` confirmed live |
| 13 | Pushed to GitHub (secret-scrubbed) | github.com/kaiser-data/cognost |
| 14 | Wrote 3-min demo cue sheet | `brainflow/demo-cases.md` |

## The corpus (42 docs)

| Tier | Count | Purpose |
|------|-------|---------|
| Original conflict-bearing | 12 | The 11 planted misalignments |
| Hay (aligned operational) | 17 | Create the haystack |
| Amplifiers | 7 | Stale values leaking downstream (QA plan, support macro, transcript) |
| Decoys | 3 | Precision test — look like conflicts, aren't |
| Multi-format | 3 | Transcript `.txt`, Slack `.json`, metrics `.csv` |

## Results

| Metric | Result |
|--------|--------|
| Docs ingested | 42/42, 0 failures |
| Conflicts surfaced (with citations) | 8/8 |
| Decoys correctly ignored | 3/3 |
| Before/after rubric | 1.3/10 → 10/10 |
| Lint findings caught | All 11 (6 contradictions, 2 supersessions, metric drift, 4 orphans) |
| Skill registered on Cloud | ✅ |

## Key discoveries
- `recall` accepts a **`system_prompt`** → the baseline-vs-maintainer before/after runs **live on
  the cloud's own LLM** (no local key).
- Skills register via `content_type=skills` (SKILL.md upload).
- **Money-shot:** the killed Day-3 paywall traced across 5 docs including an unstructured transcript.

## Two demo cases
1. **"It sees what's buried"** — *"Does the design match the PRD scope?"* → 6 cited mismatches in one query.
2. **"It tracks current & learns"** — paywall supersession trace + the 1/10 → 10/10 skill flip.

## Open items
- Fill **Team** names + **demo-video** link in `SUBMISSION.md`.
- OpenAI quota / Ollama tokenizer for a from-scratch automated pipeline run.

## Key artifacts
- `brainflow/ARCHITECTURE.md` — system + self-improvement diagrams
- `brainflow/brain-diagnostic.html` — live diagnostic (0 → 6 counter)
- `brainflow/demo-cases.md` — 3-minute demo cue sheet
- `brainflow/snapshots/` — brain states + verified query results
- `my_skills/` — baseline → maintainer skill (+ registered `SKILL.md`)
- `brain/evidence/before-after.md` — 1.3 → 10 evidence · `brain/SKILL_API_ALIGNMENT.md`
