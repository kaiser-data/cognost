---
type: ReviewQueue
title: Contradictions & Review Queue
status: open
owner: Product (Lena Hoffmann) — triage; resolution per area owner
last_reviewed: 2026-06-19
---

# Contradictions & Review Queue

The heartbeat of the wiki. Every cross-document disagreement, supersession-still-referenced, or
unresolved decision lives here with provenance. Per `CLAUDE.md` §3, nothing here is silently
resolved — each entry names both sides, states what is current, and waits for a human decision
where authority is unclear.

Status legend: `open` (needs a human) · `current-known` (truth is established; stale refs remain) · `resolved`.

| # | Topic | Type | Current truth | Conflicting sources still live | Status |
| --- | --- | --- | --- | --- | --- |
| A | AI Daily Pick in MVP | Contradiction | **Out of MVP scope** per PRD; PM pulled it in over a recorded Eng scope objection — **unresolved** | PRD §MoSCoW (Won't have) vs Roadmap Q2, Decision Log 2026-05-06, Design Screen 2 | open |
| B | Paywall timing | Supersession | **Day 7** (reverted 2026-04-09) | Roadmap (Day 3) and Design Screen 5 (Day 3) still cite the superseded value | current-known |
| C | B2B HR reporting | Contradiction | **Anonymised, aggregated only** (PRD wins; GDPR risk) | Sales commitment (per-employee, by name) + Design Screen 6 implement it | open |
| D | "40% retention" meaning | Metric drift | **Undefined** — same number, two windows | PRD = 30-day ≥40%; OKR = 7-day ≥40%; GTM = bare "40% retention" | open |
| E | Launch platform / order | Contradiction | **Simultaneous iOS+Android** per ADR-0001 (persona is Android) | Roadmap (iOS-first), GTM (App Store/iOS), Design (iPhone-only shell) contradict it | open |
| F | Backend | Supersession | **Supabase, EU/Frankfurt** (ADR-0005, GDPR/DiGA) | ADR-0002 (Firebase, US) superseded but should be checked for stray references | current-known |
| G | B2C / B2B price | Contradiction | **No source of truth** — pricing has no owner | PRD/OKR imply €4.99/mo; GTM = €3.99/mo; Sales B2B = €22/user/yr (below €25.99 >100-seat tier) | open |
| H | Exercise length | Contradiction | **Undefined across teams** | PRD = 2–5 min; Content spec = 3–10 min; GTM = 5 min; Design self-contradicts (tiles "2–5 min" vs timer 08:00) | open |
| I | Ownership gaps | Orphan | **No owner** for Pricing, AI Daily Pick build, Health/DiGA; GDPR DPIA open | RACI matrix (unassigned rows) + Decision Log 2026-05-19 | open |
| J | Brain Score missing from design | Gap | Decision to add a numeric **Brain Score** (Research Finding 2) **not implemented** | Design Screen 4 shows level + badges, no numeric score | open |
| K | Category label drift | Contradiction | Same category, two names | Design dashboard tile = "Emotional IQ"; Design radar axis = "Emotional Intelligence" | open |

---

## A — Is AI Daily Pick in the MVP?
- **PRD §MoSCoW (2026-01-22):** "Won't have (this MVP): … AI-powered Daily Picks … explicitly out of scope."
- **Decision Log 2026-05-06:** PM decided to include AI Daily Pick in the MVP citing Research Finding 1 (choice overload). **Engineering (Tomáš Novák) recorded a scope-risk objection.**
- **Roadmap Q2 (2026-03-30):** lists "AI Daily Pick: ship … as part of the MVP launch."
- **Design Screen 2 (2026-05-10):** a prominent AI Daily Pick card `violates` the PRD scope.
- **Current:** Conflicting. The PRD still says out-of-scope; a later PM decision pulled it in against an Eng objection and no build owner exists (see I). **Needs a scope decision recorded by the PRD owner.**

## B — Premium-upgrade (paywall) timing
- **PRD §Monetisation (2026-01-22):** Day 7. → **Decision Log 2026-02-14:** moved to Day 3 (Marketing). → **Decision Log 2026-04-09:** reverted to Day 7 (Product), explicitly superseding the Feb decision.
- **Current = Day 7.** The Day-3 value is **superseded** but still printed on the **Roadmap Q2** and the **Design upgrade screen (Screen 5)**. Stale references should be corrected, not re-debated.

## C — What the HR dashboard shows employers
- **PRD §B2B (2026-01-22):** anonymised, aggregated usage only; no individual employee data, by design.
- **Sales commitment (2026-05-12, signed):** per-employee dashboard, by name, with streaks and category breakdowns — to "follow up with low-engagement staff."
- **Design Screen 6:** implements the by-name employee table, matching Sales, contradicting the PRD.
- **Current = PRD (anonymised only).** Sales over-promised in a signed order form → **GDPR / contractual risk. Needs legal + PM resolution.**

## D — Retention target definition
- **PRD §Success (2026-01-22):** 30-day retention ≥ 40%. **OKR (2026-03-05):** 7-day retention ≥ 40% (north-star). **GTM (2026-04-25):** bare "40% retention."
- **Current = undefined.** Same headline number, two different windows; external decks cite it with no window at all. **Needs one agreed definition.**

## E — Which platform do we launch first?
- **ADR-0001 (2026-02-03, accepted):** React Native, **simultaneous iOS + Android**; explicitly rejects single-platform-first; primary persona (Jonas Weber) is on **Android**.
- **Roadmap Q2:** "iOS-first beta … Android ~4 weeks later." **GTM:** Apple App Store featured placement for an iOS beta. **Design:** every frame is an iPhone shell, no Android frame.
- **Current = ADR-0001 (simultaneous).** Roadmap, GTM, and Design all contradict the standing ADR and the primary persona. **Needs alignment to the ADR or a new ADR.**

## F — Backend
- **ADR-0002 (2026-02-10):** Firebase (US default). Status: **superseded by ADR-0005** on 2026-04-18.
- **ADR-0005 (2026-04-18, accepted):** Supabase, EU/Frankfurt, for GDPR / health-data residency / DiGA.
- **Current = Supabase (EU).** Firebase is superseded; "do not build new services against this decision." No live doc still names Firebase as current — confirm in code/infra during lint.

## G — Pricing
- **PRD / OKR:** imply standard B2C **€4.99/mo** (€4.99 referenced as the standard plan against the €3.99 promo). **GTM:** €3.99/mo intro + €49.99/yr. **Sales:** **€22/user/yr** B2B for Müller GmbH (120 seats) — below a >100-seat €25.99 reference tier.
- **Current = no source of truth.** Pricing is **unowned** (RACI). **Needs a pricing owner before any number is authoritative.**

## H — Exercise length
- **PRD §Scope:** 2–5 min. **Content spec (2026-03-18):** 3–10 min. **GTM:** "5 minutes." **Design:** dashboard tiles say "2–5 min" but the Exercise screen timer starts at **08:00** (8 min) — a contradiction *within* the design.
- **Current = undefined across teams.** **Needs one agreed range.**

## I — Ownership gaps (orphans)
- **RACI (2026-05-15):** **Pricing** (Responsible + Accountable unassigned), **AI Daily Pick** (no build owner), **Health insurance / DiGA** (no owner).
- **Decision Log 2026-05-19:** GDPR DPIA for health data — no owner, unresolved.
- **Current = open.** These are accountability gaps, not disagreements; lint must keep surfacing them until owners are named.

## J — Brain Score not in design
- **Research Finding 2 → decision** to add a numeric **Brain Score**. **Design Screen 4** shows "Brain Athlete — Level 4," badges, and a radar chart, but **no numeric score**.
- **Current = agreed-but-unimplemented.** Design owes the score. **Needs a design update or a decision to drop it.**

## K — Category label drift
- **Design Screen 2 tile:** "Emotional IQ." **Design Screen 4 radar axis:** "Emotional Intelligence." (PRD and Content spec both use "Emotional IQ.")
- **Current = same category, two labels.** Trivial to fix; pick one label (PRD uses "Emotional IQ").
