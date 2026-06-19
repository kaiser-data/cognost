# Cognost — the BrainFlow Company Brain

A self-improving **stakeholder-alignment wiki** built on Cognee. It ingests a product team's
scattered docs, answers questions **with citations while surfacing where the docs disagree**,
learns from feedback on its own answers, and lints the knowledge base for contradictions,
superseded-but-still-referenced decisions, and ownership gaps.

The maintainer contract is `../CLAUDE.md`. The human-readable wiki is `../wiki/`. This folder is
the runnable Cognee pipeline.

## Setup
```bash
cd ..                       # Cognost/ project root
uv venv && source .venv/bin/activate
uv pip install "cognee==1.2.0.dev1" transformers
# .env is already configured for local Ollama (cognee-distilled model + nomic-embed-text)
ollama serve &              # if not already running
```

## The three operations
```bash
# 1 — INGEST: build the permanent graph from raw/ (+ wiki/ synthesis without --raw-only)
python brain/ingest.py --reset --raw-only

# 2 — QUERY + SELF-IMPROVE
python brain/query.py --skill archive/wiki-maintainer.v1-baseline --tag before   # naive baseline
python brain/selfimprove.py --from-tag before        # distill feedback -> graph; propose a skill rewrite
python brain/selfimprove.py --apply <proposal.md>    # adopt the proposal explicitly
python brain/query.py --tag after                    # re-run with the improved skill
python brain/evidence.py                             # before/after score table

# 3 — LINT
python brain/lint.py            # writes evidence/lint-report.md; exit code = open findings
python brain/lint.py --ask      # also route the lint prompt through the graph
```

Or run the whole thing: `bash brain/run_demo.sh`.

## Cognee Cloud (bonus)
```bash
export COGNEE_CLOUD_URL=...   COGNEE_CLOUD_API_KEY=...
python brain/ingest.py --reset --raw-only --push     # push the dataset to your Cloud instance
```

## Layout
| Path | What |
| --- | --- |
| `ingest.py` | Step 1 — add + cognify (+ memify/push) |
| `query.py` · `queries.py` | Step 2a — run demo queries, score, capture feedback |
| `selfimprove.py` | Step 2b — distill session→graph (`cognee.improve`), propose/apply skill rewrites |
| `lint.py` | Step 3 — contradiction / supersession / orphan report |
| `evidence.py` | before/after score comparison |
| `common.py` | config, two-tier memory helpers, scoring rubric |
| `skills/` | maintainer skills (the agent's behavior contract); `archive/` keeps the baseline |
| `session/` | ephemeral session memory (per-run Q&A + feedback, JSONL) |
| `proposals/` | self-improvement proposals (written, not applied, until adopted) |
| `evidence/` | run scores, before/after, lint report, ingest log |
