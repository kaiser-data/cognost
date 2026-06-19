---
type: Decision
title: Premium upgrade prompt timing
status: decided
current_value: "Day 7 after first use"
owner: Product (Lena Hoffmann)
sources: [prd-brainflow-mvp.md, decision-log.md, roadmap-2026.md, design-spec.md]
relates_to:
  - { page: "Paywall Day-3 (Feb 2026)", rel: supersedes }
  - { page: "free-to-premium-conversion", rel: depends_on }
contradiction: B
last_reviewed: 2026-06-19
---

# Premium upgrade prompt timing

**Current: the premium upgrade prompt appears on Day 7 after first use** (PRD §Monetisation,
2026-01-22; reaffirmed Decision Log 2026-04-09). Rationale: users convert only after experiencing
a streak (User Research Finding 3); establish trust before asking for payment.

## History
1. **Day 7** — PRD §Monetisation (2026-01-22). Original spec.
2. **Day 3** — Decision Log 2026-02-14 (Marketing, Sven Albrecht). Moved earlier to lift
   free-to-premium conversion toward the 8% target. `superseded_by` the 2026-04-09 decision.
3. **Day 7 (revert)** — Decision Log 2026-04-09 (Product). Research evidence outweighed the
   short-term revenue argument. `supersedes` the Day-3 decision. **This is current.**

## Open issues
- **Stale references (contradiction B):** Roadmap Q2 (2026-03-30) still says "Day 3," and the
  Design upgrade screen (Screen 5, 2026-05-10) is annotated "Trigger: Day 3 after first use."
  Both predate or ignore the revert and should be corrected — not re-litigated.
