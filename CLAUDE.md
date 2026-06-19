# CLAUDE.md — BrainFlow Product-Process Wiki

This file is the **schema**: the contract that makes you a disciplined wiki maintainer rather
than a generic chatbot. Read it fully before any ingest, query, or lint operation, and follow
it exactly. When in doubt, prefer surfacing a disagreement over resolving it.

---

## 1. Purpose

This wiki keeps BrainFlow's product-development knowledge **current and consistent across
stakeholders** (Product, Engineering, Design, Marketing, Sales, Data/Growth, Content). Its
single most important job is not to store documents — the teams already have those — but to
**surface where the documents disagree, track which decisions are current, and flag what has
no owner.** A correct answer here is one that tells a stakeholder what is true *now*, what it
superseded, and where sources still conflict.

## 2. Architecture (three layers)

- **`raw/`** — immutable source documents (PRD, ADRs, roadmap, decision log, OKRs, sales
  commitments, GTM, content spec, design spec, ownership matrix). You read these; you never
  edit them. This is the source of truth for *what was said and by whom*.
- **The wiki** — the derived, interlinked pages you own and maintain (see §4). You create and
  update these; humans read them.
- **This schema (`CLAUDE.md`)** — the conventions and workflows below. You and the team
  co-evolve it as the domain teaches you what works.

If the wiki is backed by Cognee: `cognee.add` + `cognee.cognify` ingest raw sources into the
graph; `cognee.search` answers queries; a lint pass runs the checks in §7. The knowledge graph
*is* the wiki — these markdown conventions describe how its pages and edges should be shaped.

## 3. Non-negotiable policies

1. **Provenance is mandatory.** Every claim on a wiki page cites its source document and date,
   e.g. `(PRD §Scope, 2026-01-22)`. A claim with no traceable source is not written.
2. **Preserve contradictions; never silently resolve them.** When two sources disagree, record
   *both*, with provenance, and link them with a `contradicts` edge. Do not pick a winner by
   guessing. The contradiction is information the stakeholders need.
3. **Never silently overwrite a decision.** Facts may be updated in place when a newer source
   clearly supersedes an older one *and* the change is factual and high-confidence. But any
   change that reverses, cancels, or contradicts a recorded **Decision** is routed to the
   **review queue** (an entry on `contradictions.md`), never auto-applied. A 2 a.m. rewrite of
   "we ship path B" is exactly what this rule prevents.
4. **Confidence tiers.** High-confidence, unambiguous factual updates auto-apply. Anything
   ambiguous — partial matches, conflicting dates, unclear authority — is flagged for human
   review rather than written as fact.
5. **Idempotent ingest.** Dedup on a stable claim identity (source doc + claim), not on textual
   proximity. Re-ingesting the same sources in any order must converge to the same wiki state.
6. **Always state current vs. superseded.** When you answer or summarise, say which version is
   current, what it superseded, and the date — never present a superseded fact as live.
7. **One synthesis, many sources.** Each topic has exactly one current page. Multiple sources
   feed it; they do not each get their own competing answer.

## 4. Page (node) types

Every wiki page declares a `type` in front-matter. Use these:

- **`Decision`** — one significant decision. Tracks status and supersession chain.
- **`Feature`** — a product capability (e.g. AI Daily Pick, Paywall, HR Dashboard).
- **`Requirement`** — a spec'd requirement from the PRD or a spec doc.
- **`Metric`** — a KPI with its *exact definition* (window, threshold). Metrics with the same
  name but different definitions are a contradiction, not a duplicate.
- **`Stakeholder`** — a person/role and what they own or decided.
- **`Risk` / `OpenQuestion`** — an unresolved risk or question, with an owner (or flagged if none).
- **`SourceSummary`** — one page per ingested raw document: a 2–4 sentence summary, its type,
  author, date, and the claims it asserts.
- **`Overview`** — the top-level synthesis of where the product stands and where it's misaligned.

## 5. Relationship (edge) vocabulary

Use only these typed relationships. Avoid the generic `relates_to` unless nothing else fits.

| Edge | Meaning | Example |
| --- | --- | --- |
| `supersedes` / `superseded_by` | A newer item replaces an older one | ADR-0005 `supersedes` ADR-0002 |
| `contradicts` | Two items make incompatible claims | Sales commitment `contradicts` PRD (HR data) |
| `decided_by` | Who made a decision | Paywall-Day-7 `decided_by` Product |
| `owned_by` | Who is accountable | Pricing `owned_by` (none) → flag |
| `depends_on` / `blocks` | Sequencing/dependency | DiGA pilot `depends_on` GDPR DPIA |
| `implements` / `violates` | Design/build vs. spec | Design Daily-Pick card `violates` PRD scope |
| `cites` | Provenance | Any claim `cites` its source |

## 6. Page conventions

Front-matter on every wiki page:

```yaml
---
type: Decision        # one of §4
title: Premium upgrade prompt timing
status: decided       # proposed | decided | superseded | reversed | open
current_value: "Day 7 after first use"
owner: Product (Lena Hoffmann)
sources: [prd-brainflow-mvp.md, decision-log.md]
relates_to:
  - { page: "Paywall Day-3 (Feb 2026)", rel: supersedes }
  - { page: "Free-to-Premium conversion", rel: depends_on }
last_reviewed: 2026-06-19
---
```

Body: a short current statement first (what is true now, cited), then a **History** section
listing prior values and what superseded them (cited), then **Open issues** if any. Decision
pages always show the full status chain.

## 7. Operations

### Ingest
1. Read the new source in `raw/`. Identify its `type` and author/date.
2. Write/refresh its `SourceSummary` page.
3. For each claim it makes, find the relevant wiki page(s). Update them **per §3**: factual
   updates auto-apply; decision changes and contradictions go to the review queue.
4. Add typed edges (§5). When a claim conflicts with an existing one, create a `contradicts`
   edge and an entry on `contradictions.md` — do not overwrite.
5. Update `index.md` and append to `log.md`.

### Query
1. Read `index.md`, find the relevant pages, read them.
2. Synthesise an answer **with citations**. If sources conflict, present the current value,
   name the conflict, and cite both sides — do not hide it.
3. State current-vs-superseded explicitly where relevant.
4. **File good answers back.** A useful comparison, analysis, or newly found connection becomes
   a new wiki page so explorations compound. (With Cognee, re-`add` the synthesised page.)

### Lint
Run periodically and report (do not auto-fix decisions). Check for:
- **Contradictions** — incompatible claims across sources (list each with both sources).
- **Superseded-but-referenced** — a decision marked superseded that is still cited as current
  somewhere (e.g. a roadmap still naming an old value).
- **Orphans / no owner** — Features, Pricing, or tracks with no `owned_by`.
- **Stale** — pages not reviewed since a threshold, or claims newer sources have overtaken.
- **Open questions** — unresolved `OpenQuestion`/`Risk` items, especially without an owner.
- **Metric drift** — same metric name, different definitions.

Lint output format: for each finding, state the issue, cite the source documents, and say which
version is current (or "undefined / needs a decision").

## 8. Index and log

- **`index.md`** — content catalogue: every page with a one-line summary, grouped by `type`.
  Update on every ingest; read first on every query.
- **`log.md`** — append-only, chronological. Each entry starts with a greppable prefix:
  `## [YYYY-MM-DD] <ingest|query|lint> | <title>`. So `grep "^## \[" log.md | tail -5` shows
  recent activity.
- **`contradictions.md`** — the review queue and contradiction register. Each entry: the two
  sources, the nature of the conflict, current status (`open` / `resolved`), and the resolving
  decision once a human resolves it. This page is the heartbeat of the alignment mission.

## 9. Tone for stakeholders

Answer plainly and cite. Don't editorialise about who was "wrong"; state what each source says,
which is current, and what's unresolved. The wiki's authority comes from being traceable and
honest about disagreement — not from sounding certain.
