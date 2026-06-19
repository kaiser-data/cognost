---
type: Feature
title: AI Daily Pick
status: open
current_value: "Disputed — PRD says out of MVP scope; PM pulled it in over an Eng objection"
owner: Accountable Lena Hoffmann (PM); build owner — (none)
sources: [prd-brainflow-mvp.md, decision-log.md, roadmap-2026.md, design-spec.md, ownership-raci.md]
relates_to:
  - { page: "prd-brainflow-mvp", rel: violates }
  - { page: "ai-daily-pick build owner", rel: owned_by }
contradiction: A
last_reviewed: 2026-06-19
---

# AI Daily Pick

An AI-curated daily exercise recommendation surfaced as a one-tap card, to kill choice overload
on first session (User Research Finding 1).

**Current: contested.** The PRD marks it **out of MVP scope**; a later PM decision pulled it into
the MVP **over a recorded Engineering scope objection**, and it has **no build owner**. This is
not resolved — it is surfaced for a scope decision.

## The conflict (contradiction A)
- **PRD §MoSCoW (2026-01-22):** "Won't have (this MVP): … AI-powered Daily Picks … explicitly out of scope."
- **Decision Log 2026-05-06:** PM decided to include it in the MVP (Research Finding 1). Engineering
  (Tomáš Novák) **recorded a scope-risk objection** for the Q2 launch.
- **Roadmap Q2 (2026-03-30):** lists shipping it as part of the MVP launch.
- **Design Screen 2 (2026-05-10):** ships a prominent AI Daily Pick card — design `violates` the
  PRD's "Won't have."

## Open issues
- Scope authority: the PRD owner has not amended the PRD; a decision-log entry alone does not
  rewrite the spec. **Needs a recorded scope decision.**
- **Ownership gap (I):** RACI lists "AI Daily Pick" with **no build owner** ("Pulled into MVP
  2026-05-06; no build owner yet").
