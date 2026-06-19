# Lint — live run on Cognee Cloud (brainflow brain)

Ran the canonical lint prompt (CLAUDE.md §7) against the live 42-doc `brainflow` brain via
`recall` with the maintainer skill as `system_prompt`. Cloud server-side LLM (no local key).
Date: 2026-06-19. Reports only; decisions never auto-resolved.

## Coverage vs. the 11 planted ground-truth issues

| Issue | This single lint pass |
| --- | --- |
| A — AI Daily Pick scope | ✅ contradiction + supersession |
| B — Paywall timing | ✅ contradiction + supersession (Day 7 current) |
| F — Backend | ✅ contradiction (Supabase EU current) |
| H — Exercise length | ✅ contradiction (undefined) |
| I — Ownership orphans | ✅ all 4 (Pricing, AI Daily Pick, HR, DiGA) |
| Open questions | ✅ GDPR DPIA + pricing owner |
| Supersessions (B, paywall) | ✅ stale refs named (Roadmap, Design, QA) |
| C — HR per-employee vs anonymised | ⚠️ flagged ownerless, not as the privacy contradiction |
| D / E / G / J / K | ❌ not surfaced in this single pass |

A single lint `recall` catches ~7/11 plus orphans, open questions and supersessions — the
structural backbone. The subtler five (retention window D, platform E, price spread G, Brain
Score J, category drift K) need targeted checks — verified separately at 8/8 in
`brainflow/snapshots/query-results.json`. The exhaustive structured pass is
`brain/evidence/lint-report.md` (all 11).

## Verbatim output

- **Contradiction #1 – Premium-upgrade (paywall) timing** — Decision Log 2026-04-09 reverts to
  **Day 7** (current, supersedes Feb-14); Roadmap and Design Spec v2.1 still cite Day 3; PRD says
  Day 7. Current = Day 7.
- **Superseded but still cited (paywall)** — Roadmap + Design Spec v2.1 still present Day 3 as active.
- **Contradiction #2 – AI Daily Pick scope** — PRD "Won't have" vs Roadmap (ship in MVP) +
  Decision Log 2026-05-06 (PM includes it, Eng objection recorded). Documents disagree.
- **Contradiction #3 – Exercise duration** — PRD 2–5 min vs Content Spec 3–10 min. Undefined.
- **Contradiction #4 – Backend / residency** — Release Notes v0.9: **Supabase (EU/Frankfurt)**
  current; prototype backend historic.
- **Ownerless (RACI 2026-05-15)** — AI Daily Pick (no Responsible), **Pricing** (no R/A),
  B2B HR dashboard (no Responsible), Health/DiGA (no R/A).
- **Open questions** — health-data DPIA (no owner); who owns the GDPR DPIA; who owns pricing
  source of truth across PRD/OKR/GTM/Sales.

_All findings reported without adjudication — documented contradictions, superseded references,
ownerless features and open questions, with the current version indicated where a clear decision exists._
