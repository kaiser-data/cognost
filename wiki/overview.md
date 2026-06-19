---
type: Overview
title: BrainFlow — Where We Stand
status: current
owner: Product (Lena Hoffmann)
last_reviewed: 2026-06-19
---

# BrainFlow — Where We Stand

BrainFlow is a mental-fitness micro-exercise app for stressed professionals in the DACH market.
This page is the top-level synthesis of **what is true now and where stakeholders disagree.** It is
derived from the 12 source documents in `raw/`; every claim is traceable. When sources conflict,
the conflict is named, not hidden (`CLAUDE.md` §3).

## Settled (current truth)
- **Backend:** Supabase, EU/Frankfurt — for GDPR / health-data residency (ADR-0005, supersedes ADR-0002 Firebase). *(F)*
- **Paywall timing:** Day 7 after first use — reverted from a brief Day-3 experiment (Decision Log 2026-04-09 supersedes 2026-02-14). *(B)*
- **Client:** React Native, **simultaneous iOS + Android** at launch (ADR-0001) — though downstream docs have drifted (see below). *(E)*
- **Categories:** Focus, Creativity, Emotional IQ, Wellbeing (PRD, Content spec).
- **Goal:** 2,500 MAU in DACH by Q4 2026 (PRD).

## Misaligned (needs a human decision)
| # | Topic | The disagreement | Page |
| --- | --- | --- | --- |
| A | AI Daily Pick scope | PRD "Won't have" vs PM decision + Roadmap + Design shipping it | [ai-daily-pick](topics/ai-daily-pick.md) |
| C | HR dashboard | PRD anonymised-only vs signed Sales promise (by-name) + Design | [hr-dashboard](topics/hr-dashboard.md) |
| D | Retention target | 30-day vs 7-day, both "40%" | [retention-target](topics/retention-target.md) |
| E | Launch platform | ADR simultaneous vs Roadmap/GTM/Design iOS-first | [launch-platform](topics/launch-platform.md) |
| G | Pricing | €4.99 vs €3.99 vs €22/yr — and no owner | [pricing](topics/pricing.md) |
| H | Exercise length | 2–5 vs 3–10 vs 5 min (design self-contradicts) | [exercise-length](topics/exercise-length.md) |
| K | Category label | "Emotional IQ" vs "Emotional Intelligence" in design | [category-naming](topics/category-naming.md) |

## Stale references to fix (truth is known)
- **B:** Roadmap Q2 and Design Screen 5 still say paywall "Day 3" — current is Day 7.
- **F:** Confirm no code/infra still provisions Firebase.

## Gaps (no owner / unimplemented)
- **I:** Pricing, AI Daily Pick build, Health/DiGA track — no owner; GDPR DPIA unresolved → [gdpr-dpia](topics/gdpr-dpia.md).
- **J:** Agreed numeric Brain Score not implemented in the design → [brain-score](topics/brain-score.md).

→ Full register with provenance: **[contradictions.md](contradictions.md)**.
