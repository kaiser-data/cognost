# Cognost — Architecture

**A self-improving, stakeholder-alignment Company Brain on Cognee Cloud.**

Cognost ingests a product team's scattered documents into one knowledge graph, then answers
questions **with citations while surfacing where the documents disagree** — tracking which
decisions are current vs. superseded, flagging what has no owner, and **improving its own
answering behaviour from scored feedback**.

The reference corpus is **BrainFlow**: 42 documents (12 conflict-bearing + 30 realistic
operational docs) with 11 planted misalignments hiding in the noise — a needle-in-a-haystack test.

---

## System architecture

```mermaid
flowchart TB
  subgraph SRC["① Sources — 42 documents, multi-format"]
    direction LR
    S1["Product &amp; Eng<br/>PRD · ADRs · Roadmap · Decision Log"]
    S2["GTM &amp; Ops<br/>OKRs · Sales · GTM · Content · Design · RACI"]
    S3["Hay (operational)<br/>Standups · Retros · QA · Support · Investor"]
    S4["Multi-format<br/>Transcript .txt · Slack .json · Metrics .csv"]
  end

  subgraph ING["② Ingestion — Cognee Cloud"]
    I1["POST /api/v1/remember<br/>file upload"]
    I2["cognify pipeline<br/>chunk → extract entities &amp; typed relations"]
    I1 --> I2
  end

  subgraph BRAIN["③ The Brain — Cognee Cloud · dataset: brainflow"]
    direction LR
    G1["Knowledge graph<br/>typed edges:<br/>contradicts · supersedes · owned_by · cites"]
    G2["Vector store<br/>semantic chunks"]
    M1["Session memory<br/>(ephemeral) scored Q&amp;A"]
    M2["Permanent graph<br/>(durable) register + summaries"]
  end

  subgraph GOV["④ Governance — the maintainer contract"]
    C1["CLAUDE.md schema<br/>§3 provenance · preserve-conflict · current-vs-superseded"]
    C2["wiki-maintainer skill<br/>loaded as recall system prompt"]
    C1 --> C2
  end

  subgraph OPS["⑤ Operations"]
    O1["Query / Recall<br/>GRAPH_COMPLETION<br/>cited, conflict-aware answers"]
    O2["Lint<br/>contradictions · supersessions<br/>orphans · metric drift"]
    O3["Self-improve<br/>score → diagnose → propose → apply"]
  end

  subgraph OUT["⑥ Outputs"]
    P1["Cited answers"]
    P2["Contradiction register"]
    P3["Diagnostic artifact (HTML) · 0 → 6"]
    P4["State snapshots (JSON)"]
  end

  SRC --> ING --> BRAIN
  C2 --> O1
  BRAIN --> O1
  BRAIN --> O2
  BRAIN --> O3
  O1 --> P1
  O2 --> P2
  O2 --> P3
  O2 --> P4
  O1 -. "scored feedback" .-> M1
  M1 --> O3
  O3 -. "cognee.improve(session_ids)" .-> M2
  O3 -. "learned policies" .-> C2

  classDef brain fill:#0C1719,stroke:#4FD0C5,stroke-width:2px,color:#DCE7E4;
  classDef gov fill:#16100a,stroke:#E8B23A,color:#E8E0D0;
  classDef ops fill:#1a0f0d,stroke:#FF5C49,color:#F0DAD6;
  class G1,G2,M1,M2 brain;
  class C1,C2 gov;
  class O1,O2,O3 ops;
```

---

## Components

| # | Component | Responsibility | Implementation |
|---|---|---|---|
| ① | **Sources** | The raw, immutable team knowledge — never edited | 42 docs in `raw/` (md/txt/json/csv) |
| ② | **Ingestion** | Turn documents into graph + vectors | `/api/v1/remember` → Cognee `cognify` |
| ③ | **The Brain** | Persist entities + typed relationships and embeddings; two-tier memory | Cognee Cloud dataset `brainflow` |
| ④ | **Governance** | The contract that makes the brain a disciplined maintainer, not a chatbot | `CLAUDE.md` schema → `wiki-maintainer` skill |
| ⑤ | **Operations** | Query, lint, and self-improve | `/api/v1/recall`, lint pass, self-improve loop |
| ⑥ | **Outputs** | What stakeholders consume | Answers, register, the diagnostic artifact, JSON snapshots |

### Two-tier memory (③)

| Tier | Holds | Lifetime |
|---|---|---|
| **Session memory** | raw scored Q&A events, feedback per run | ephemeral (per `session_id`) |
| **Permanent graph** | entities, typed edges, summaries, contradiction register | durable |

**Self-improvement = distilling scored session feedback into the permanent graph.**

---

## The self-improvement loop (⑤·O3)

```mermaid
flowchart LR
  A["Remember skill<br/>baseline v1"] --> B["Run<br/>recall(GRAPH_COMPLETION)"]
  B --> C["Score<br/>cited? · surfaced conflict? · current-vs-superseded?"]
  C --> D{"rubric<br/>failures?"}
  D -- "yes" --> E["Propose skill rewrite<br/>adopt CLAUDE.md policy<br/>(not applied)"]
  E --> F["Apply explicitly<br/>--apply"]
  F --> A
  C -. "distill" .-> G["cognee.improve(session_ids)"]
  G --> H["Permanent graph enriched"]

  classDef hot fill:#1a0f0d,stroke:#FF5C49,color:#F0DAD6;
  class D hot;
```

The brain literally **learns its own operating rules from its mistakes**, sourcing each new rule
from the `CLAUDE.md` schema rather than inventing it. Proposals are written but **never applied
silently** — adoption is an explicit step.

---

## Data flow — a single query

1. `recall(query, GRAPH_COMPLETION, session_id)` runs against the `brainflow` graph, with the
   `wiki-maintainer` skill as the system prompt.
2. The graph traverses **typed edges** (`contradicts`, `supersedes`, `owned_by`) — not just
   nearest-neighbour chunks — so it can present *both* sides of a disagreement.
3. The answer cites every claim, names the current value, and what it superseded.
4. The interaction is written to **session memory**; a useful synthesis can be filed back into
   the **permanent graph** so explorations compound.

---

## Verification (live, 2026-06-19)

Run against the live `brainflow` brain on Cognee Cloud:

- **8/8** stakeholder questions surfaced their conflict with citations + current-vs-superseded.
- **3/3** decoys correctly *not* flagged (competitor price, superseded ADR, unapproved draft) — no false positives.
- The reverted **Day-3 paywall** was traced across 5 documents (roadmap, design, QA plan, decision log, meeting transcript).

See `snapshots/query-results.json` and `brain-diagnostic.html` for the evidence.

---

## Tech stack

- **Cognee Cloud** — managed knowledge-graph + vector memory (`remember` / `recall` / `improve`).
- **Graph operations** — `GRAPH_COMPLETION` recall over typed relationships.
- **Governance** — `CLAUDE.md` maintainer schema; versioned `wiki-maintainer` skill.
- **Presentation** — self-contained HTML diagnostic (Canvas graph viz, no external deps).
