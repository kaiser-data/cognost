#!/usr/bin/env python3
"""
BrainFlow corpus generator.

Writes ~30 NEW documents (hay / amplifiers / decoys / multi-format) into raw/,
alongside the 12 original conflict-bearing docs, to turn the dataset into a
realistic needle-in-haystack corpus.

DISCIPLINE: every HAY doc conforms to the FACT LEDGER (canonical current values)
so we never introduce an UNTRACKED contradiction. Only AMPLIFIERS deliberately
carry a stale/contradicting value downstream; only DECOYS look-like-but-aren't.
The 11 planted issues remain the sole ground truth.
"""
import json
import os
import pathlib

RAW = pathlib.Path(__file__).parent / "raw"
RAW.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# FACT LEDGER — canonical CURRENT values every HAY doc must respect.
#   Paywall upgrade prompt ....... Day 7 (Day-3 reverted 2026-04-09)
#   Backend ...................... Supabase, EU/Frankfurt (ADR-0005 > ADR-0002)
#   Client stack ................. React Native, simultaneous iOS+Android (ADR-0001)
#   B2B HR reporting ............. anonymised aggregate ONLY
#   North-star metric ............ 7-day retention >=40% (ALWAYS state the window)
#   Conversion ................... >=8% within 30 days
#   MAU goal ..................... 2,500 in DACH by Q4 2026
#   Categories ................... Focus, Creativity, Emotional IQ, Wellbeing
#   Persona ...................... Jonas Weber, 38, Android, Munich, remote dev
#   People ....................... Lena Hoffmann (PM/Product), Tomáš Novák (Eng TL),
#                                  Mara Köhler (UX), Dr. Petra Lindqvist (Content),
#                                  Sven Albrecht (Marketing & Data/Growth),
#                                  Daniela Fuchs (Sales)
# HAY must AVOID asserting: a bare B2C price, a universal exercise minute count,
#   a paywall day, AI-Daily-Pick scope, HR per-name data, a launch ORDER,
#   or a bare "40% retention" without its window.
# ---------------------------------------------------------------------------

docs = {}

# ============================ TIER A — HAY (17) ============================

docs["standup-2026-02-09.md"] = """---
type: StandupNotes
title: Daily Standup — Sprint 8
date: 2026-02-09
owner: Engineering (Tomáš Novák)
---

# Standup — 2026-02-09

- **Tomáš:** Scaffolding the React Native client; shared component library set up. One codebase
  for both stores, per ADR-0001. No blockers.
- **Mara:** Onboarding "Start Today" flow wireframes done; handing high-fidelity frames to eng.
- **Lena:** Confirmed the four category tiles (Focus, Creativity, Emotional IQ, Wellbeing) for
  the dashboard. Reminder: frictionless entry, no account creation up front.
- Next: wire the "Start Today" CTA straight into the first guided exercise.
"""

docs["standup-2026-02-23.md"] = """---
type: StandupNotes
title: Daily Standup — Sprint 9
date: 2026-02-23
owner: Engineering (Tomáš Novák)
---

# Standup — 2026-02-23

- **Tomáš:** Streak + completed-sessions tracking working end to end. Midnight rollover edge
  case noted for QA.
- **Petra:** Drafting "The Science" panels for the first Focus exercises; neuroscience review
  scheduled.
- **Mara:** Dark-mode neon palette (neon-blue / violet / green) locked into the design system.
- No blockers.
"""

docs["standup-2026-03-09.md"] = """---
type: StandupNotes
title: Daily Standup — Sprint 10
date: 2026-03-09
owner: Engineering (Tomáš Novák)
---

# Standup — 2026-03-09

- **Tomáš:** Auth flow prototype running. Evaluating EU-region data residency for the move off
  the prototype backend (see vendor eval).
- **Lena:** Persona check — building for Jonas Weber (Android, Munich, remote dev); keep flows
  thumb-reachable.
- **Mara:** Progress screen radar chart in review.
- Blocker: waiting on final copy for the streak milestone badges.
"""

docs["standup-2026-03-23.md"] = """---
type: StandupNotes
title: Daily Standup — Sprint 11
date: 2026-03-23
owner: Engineering (Tomáš Novák)
---

# Standup — 2026-03-23

- **Tomáš:** Notifications spike done; reminders remain a "Could have" for MVP.
- **Petra:** Five Wellbeing exercises content-complete and psychologist-reviewed.
- **Mara:** Accessibility pass on onboarding queued.
- **Lena:** Tracking toward 2,500 MAU in DACH by Q4. No scope changes today.
"""

docs["retro-sprint-9.md"] = """---
type: Retrospective
title: Sprint 9 Retrospective
date: 2026-02-27
owner: Engineering (Tomáš Novák)
---

# Sprint 9 Retro

**Went well:** streak tracking shipped ahead of estimate; design-system handoff was smooth.

**Could improve:** ambiguity on which screens are MVP "Must have" vs "Should have" cost us a
day of rework. Action: re-read the PRD MoSCoW list at sprint planning.

**Kudos:** Mara for the dark-mode palette; Petra for fast science-panel turnaround.
"""

docs["retro-sprint-11.md"] = """---
type: Retrospective
title: Sprint 11 Retrospective
date: 2026-03-27
owner: Engineering (Tomáš Novák)
---

# Sprint 11 Retro

**Went well:** notifications spike de-risked the "Could have" reminders.

**Could improve:** we keep rediscovering decisions that live only in the decision log — people
don't read it. Action: link decisions from the relevant tickets.

**Watch:** backend residency question is becoming urgent for the health-insurer track.
"""

docs["1on1-lena-tomas-2026-03.md"] = """---
type: MeetingNotes
title: 1:1 — Lena & Tomáš
date: 2026-03-16
owner: Product (Lena Hoffmann)
---

# 1:1 — Lena / Tomáš — 2026-03-16

- Velocity steady. React Native single-codebase bet is paying off for shared UI work.
- Tomáš raising data-residency concern for the health track; Lena agrees it needs an ADR.
- Career: Tomáš wants to mentor a junior on the mobile build in Q3.
- No product-scope decisions taken in this 1:1.
"""

docs["oncall-postmortem-2026-04-22.md"] = """---
type: Postmortem
title: Postmortem — Auth latency during Supabase cutover
date: 2026-04-22
owner: Engineering (Tomáš Novák)
---

# Postmortem — 2026-04-22

**Summary:** During the cutover to Supabase (EU/Frankfurt) per ADR-0005, auth p95 latency rose
to 1.8s for ~40 minutes in the staging environment.

**Root cause:** connection-pool sizing carried over from the Firebase prototype defaults.

**Resolution:** tuned pool size; latency back to ~220ms. No user-facing impact (staging only).

**Action items:** document EU-region pool defaults; add a latency alert. All data remained in
the EU region throughout.
"""

docs["qa-regression-onboarding.md"] = """---
type: QATestPlan
title: QA Regression — Onboarding & Start Today
date: 2026-04-30
owner: QA (contractor)
---

# QA Regression — Onboarding

| # | Case | Expected |
| --- | --- | --- |
| 1 | Tap "Start Today" from cold launch | Drops directly into first guided exercise, no signup |
| 2 | Complete first exercise | Streak = 1, session counted |
| 3 | Reopen next day | Streak increments |
| 4 | Category tiles render | Focus, Creativity, Emotional IQ, Wellbeing all present |
| 5 | Dark-mode contrast | Meets the design-system neon palette |

All cases passed on the latest beta build.
"""

docs["qa-bug-BF-118-streak-tz.md"] = """---
type: BugReport
title: BF-118 — Streak resets across timezones
date: 2026-04-12
owner: QA (contractor)
status: resolved
---

# BF-118 — Streak resets when device timezone changes

**Severity:** medium. **Area:** basic tracking / streaks.

**Repro:** complete a session, fly from Munich to London, reopen app → streak shows 0.

**Cause:** day boundary computed in device-local time, not the user's home timezone.

**Fix:** anchor streak day boundary to the account's home timezone. Verified, closed.
"""

docs["analytics-weekly-2026-05-11.md"] = """---
type: AnalyticsReport
title: Weekly Analytics — week of 2026-05-11
date: 2026-05-11
owner: Data & Growth (Sven Albrecht)
---

# Weekly Analytics — 2026-05-11

- **7-day retention:** 31% (north-star target is 7-day retention >=40%; below target).
- Installs: 1,420 week-over-week (+6%).
- Daily active: 540 avg.
- Funnel: 71% complete the first exercise after "Start Today".
- Note: figures are beta-cohort only; not the launch cohort.
"""

docs["analytics-weekly-2026-05-18.md"] = """---
type: AnalyticsReport
title: Weekly Analytics — week of 2026-05-18
date: 2026-05-18
owner: Data & Growth (Sven Albrecht)
---

# Weekly Analytics — 2026-05-18

- **7-day retention:** 33% (north-star target is 7-day retention >=40%).
- Free-to-Premium conversion: 5.1% within 30 days (target >=8%).
- CAC (B2C): €17 blended.
- Top category by completion: Wellbeing.
- All metrics defined per the OKR & Metrics doc.
"""

docs["release-notes-v0.9-beta.md"] = """---
type: ReleaseNotes
title: BrainFlow v0.9 (closed beta)
date: 2026-05-05
owner: Engineering (Tomáš Novák)
---

# BrainFlow v0.9 — Closed Beta

- Onboarding "Start Today" with frictionless entry.
- Guided exercises with timer and "The Science" panel.
- Basic tracking: streaks + completed sessions.
- Four categories: Focus, Creativity, Emotional IQ, Wellbeing.
- Backend running on Supabase (EU/Frankfurt).
- Built with React Native; iOS and Android builds from one codebase.

Known issues: progress radar chart polish pending.
"""

docs["allhands-2026-04.md"] = """---
type: AllHands
title: All-Hands Summary — April 2026
date: 2026-04-28
owner: Product (Lena Hoffmann)
---

# All-Hands — April 2026

- Reaffirmed the mission: science-based micro-exercises for stressed professionals in DACH.
- North-star: 7-day retention >=40%. We're below target in beta; activation work continues.
- Backend moved to the EU region for data protection and the health-insurer path.
- Q3 will open the B2B track. Q4 explores health-insurer pilots.
- Goal unchanged: 2,500 MAU in DACH by Q4 2026.
"""

docs["vendor-eval-push-eu.md"] = """---
type: VendorEval
title: Vendor Evaluation — EU-compliant push notifications
date: 2026-04-15
owner: Engineering (Tomáš Novák)
---

# Vendor Eval — Push Notifications (EU)

Following ADR-0005 (Supabase, EU region), push must move off the prototype's US-default
messaging to an EU-compliant provider.

| Vendor | Region | Verdict |
| --- | --- | --- |
| Provider A | EU (Frankfurt) | Recommended — data stays in EU, good RN SDK |
| Provider B | US default | Rejected — residency mismatch |
| Provider C | EU (Dublin) | Backup option |

Decision: proceed with Provider A. Aligns with the EU residency posture.
"""

docs["content-style-guide.md"] = """---
type: StyleGuide
title: Content Style Guide — "The Science" panels
date: 2026-03-20
owner: Content (Dr. Petra Lindqvist)
---

# Content Style Guide

- Every exercise ships a **"The Science"** panel: one plain-language sentence on the
  neurological benefit (e.g. prefrontal-cortex activation), one citation.
- Voice: warm, expert, never preachy. No medical claims; "supports", not "cures".
- All content authored or reviewed by a neuroscientist or psychologist.
- Categories use the canonical labels: Focus, Creativity, Emotional IQ, Wellbeing.
"""

docs["accessibility-audit-2026-05.md"] = """---
type: AccessibilityAudit
title: Accessibility Audit — Onboarding & Exercise
date: 2026-05-08
owner: Design (Mara Köhler)
---

# Accessibility Audit

- **Contrast:** dark-mode neon palette passes AA for body text; the neon-green accent fails AA
  on small text — action: reserve it for large elements only.
- **Tap targets:** "Start Today" CTA meets 44pt minimum.
- **Screen reader:** exercise timer needs an aria-live label — open action.
- **Motion:** offer reduced-motion variant for the progress radar animation.
"""

# ============================ TIER B — AMPLIFIERS (7) ======================
# Each deliberately carries a STALE / CONTRADICTING value downstream.

docs["qa-test-plan-paywall.md"] = """---
type: QATestPlan
title: QA Test Plan — Premium Upgrade Prompt
date: 2026-05-14
owner: QA (contractor)
---

# QA Test Plan — Upgrade Prompt

| # | Case | Expected |
| --- | --- | --- |
| 1 | New user completes onboarding | No upgrade prompt yet |
| 2 | Reach Day 3 after first use | **Upgrade prompt fires on Day 3** |
| 3 | Dismiss prompt | Re-prompt after 48h |
| 4 | Price shown | Launch promo price on the sheet |

Note: test cases written from the roadmap. (AMPLIFIER — propagates the stale Day-3 paywall;
current decision is Day 7 per Decision Log 2026-04-09.)
"""

docs["support-macro-trial.md"] = """---
type: SupportMacro
title: Support Canned Reply — "When does my trial convert?"
date: 2026-05-16
owner: Customer Support
---

# Macro: trial-conversion-timing

> Hi {{first_name}}, thanks for trying BrainFlow! Your free experience runs for the first few
> days, and the option to go Premium appears **after 3 days** of use. Let me know if you have
> any questions!

(AMPLIFIER — propagates the stale Day-3 timing into customer-facing support; current is Day 7.)
"""

docs["marketing-email-launch.md"] = """---
type: MarketingEmail
title: Launch Email Draft — "Train your brain in 5 minutes"
date: 2026-05-20
owner: Marketing (Sven Albrecht)
---

# Launch Email (draft)

**Subject:** Train your brain. 5 minutes. Every day.

Hi there — BrainFlow is here. Science-based micro-exercises that take just **5 minutes**.
Start your streak today.

**Launch offer: just €3.99/month.** Cancel anytime.

[ Start Today ]

(AMPLIFIER — echoes GTM €3.99 and the "5 minutes" duration; both are contested values.)
"""

docs["investor-update-2026-05.md"] = """---
type: InvestorUpdate
title: Investor Update — May 2026
date: 2026-05-30
owner: Product (Lena Hoffmann)
---

# Investor Update — May 2026

Team, quick monthly update:

- Closed beta live; activation improving.
- Signed our first B2B pilot (Müller GmbH, 120 employees).
- Backend migrated to the EU region ahead of the health-insurer track.
- **We're targeting 40% retention** and tracking toward 2,500 MAU in DACH by Q4.

(AMPLIFIER — quotes a bare "40% retention" with no window; PRD=30-day, OKR=7-day.)
"""

docs["appstore-launch-checklist.md"] = """---
type: LaunchChecklist
title: App Store Launch Checklist — iOS Beta
date: 2026-05-22
owner: Marketing (Sven Albrecht)
---

# Launch Checklist — iOS

- [ ] App Store Connect listing finalised
- [ ] Screenshots in iPhone frames
- [ ] Featured-placement pitch to Apple submitted
- [ ] TestFlight build approved
- [ ] Press kit references "iOS-first beta"

No Android / Play Store items in this checklist.

(AMPLIFIER — iOS-only launch ops; contradicts ADR-0001 simultaneous iOS+Android & Android persona.)
"""

docs["sprint-ticket-BF-142.md"] = """---
type: Ticket
title: BF-142 — Build AI Daily Pick card
date: 2026-05-08
owner: unassigned
status: open
---

# BF-142 — AI Daily Pick card (Dashboard)

**Description:** Build the AI Daily Pick card at the top of the dashboard. One-tap start of the
recommended exercise. Pulled into the MVP per Decision Log 2026-05-06.

**Assignee:** _unassigned_
**Eng note:** flagged as scope risk — was a "Won't have" item in the PRD.

(AMPLIFIER — propagates AI Daily Pick into the build with NO owner; echoes issues A + I.)
"""

docs["cs-onboarding-mueller.md"] = """---
type: CustomerSuccess
title: Müller GmbH — HR Admin Onboarding Guide
date: 2026-05-18
owner: Customer Success (TBD)
customer: Müller GmbH
---

# Müller GmbH — HR Admin Onboarding

Welcome! Your HR dashboard lets you:

1. See the **employee engagement table** — each staff member listed **by name**, with their
   streak, weekly goal %, and category breakdown.
2. Filter to "low-engagement employees" for follow-up.
3. View aggregate charts above the table.

(AMPLIFIER — per-employee by-name HR data, per the signed Sales commitment; contradicts the
PRD's anonymised-aggregate-only rule. GDPR risk.)
"""

# ============================ TIER C — DECOYS (3) ==========================
# Look like a conflict; are NOT. Tests precision / no false positives.

docs["market-analysis-competitors.md"] = """---
type: MarketAnalysis
title: Competitive Landscape — DACH mental-fitness apps
date: 2026-04-10
owner: Marketing (Sven Albrecht)
---

# Competitive Landscape (DACH)

| Competitor | Price | Notes |
| --- | --- | --- |
| CalmDACH | **€3.99/month** | Closest analogue; meditation-led, long sessions |
| FokusApp | €6.99/month | Productivity bent, no science framing |
| ZenWork (B2B) | €30/user/yr | Enterprise wellbeing, HR reporting |

Takeaway: the sub-€5 tier is crowded; our science framing is the differentiator.

(DECOY — the €3.99 here is a COMPETITOR's price, not BrainFlow's. Must NOT be flagged as the
BrainFlow pricing contradiction.)
"""

docs["adr-0003-analytics-amplitude.md"] = """---
type: ADR
id: ADR-0003
title: Use Amplitude for product analytics
status: superseded
superseded_by: ADR-0004 (self-hosted, EU)
date: 2026-02-20
owner: Engineering (Tomáš Novák)
---

# ADR-0003: Use Amplitude for product analytics

## Decision
Adopt Amplitude for product analytics in the prototype phase.

## Status notes
**Superseded by ADR-0004** (move analytics to a self-hosted EU instance for data residency).
Do not build new tracking against this decision. This document records its own supersession.

(DECOY — correctly self-labels as superseded; must NOT be reported as a live contradiction.)
"""

docs["roadmap-2027-DRAFT.md"] = """---
type: Roadmap
title: BrainFlow 2027 Roadmap — DRAFT (NOT APPROVED)
status: draft
date: 2026-06-01
owner: Product (Lena Hoffmann)
---

# BrainFlow 2027 Roadmap — DRAFT — NOT APPROVED

> ⚠️ Speculative brainstorm. Numbers are placeholders. Do NOT cite as a source of truth.

- Maybe expand to 50,000 MAU? (placeholder)
- Possible price test at €9.99/month? (placeholder, unvalidated)
- Explore wearables, B2B2C via insurers, EU-wide launch.

(DECOY — clearly DRAFT/unapproved with placeholder numbers; must be down-weighted, not treated
as a live source that contradicts the approved 2,500 MAU goal or pricing.)
"""

# ============================ TIER D — MULTI-FORMAT (3) ====================

docs["transcript-product-review-2026-04-09.txt"] = """PRODUCT REVIEW — 2026-04-09 — voice transcript (auto-generated, lightly cleaned)
Attendees: Lena (PM), Mara (UX), Sven (Marketing), Tomas (Eng)

LENA: ok so the big one today is the paywall timing again. we moved it to day three back in
february for the conversion numbers.
SVEN: right, day three. revenue earlier.
MARA: but research finding three is pretty clear, people only upgrade after they've felt a
streak. day three we're asking before they've got the habit. churn risk.
TOMAS: and support's already getting confused tickets about when the trial ends.
LENA: yeah. honestly the research outweighs the short term revenue. i want to call it.
LENA: decision — we revert the upgrade prompt back to day seven. this supersedes the february
day-three call. product owns it.
SVEN: ok. i'll need to update the launch email then.
MARA: and the upgrade screen annotation still says day three, i'll fix the frame.
LENA: please. day seven is the current decision as of today.

(MULTI-FORMAT, unstructured transcript — AUTHORITATIVE source for the Day-7 reversal, issue B.)
"""

slack_export = {
    "channel": "#eng-backend",
    "exported": "2026-04-19",
    "messages": [
        {"ts": "2026-04-18T09:14:00Z", "user": "tomas",
         "text": "ADR-0005 is merged — we're on Supabase, EU/Frankfurt region. Firebase prototype is officially superseded."},
        {"ts": "2026-04-18T09:16:00Z", "user": "lena",
         "text": "🎉 great. this unblocks the health-insurer conversations on data residency."},
        {"ts": "2026-04-18T09:20:00Z", "user": "tomas",
         "text": "reminder: do NOT build new services against Firebase (ADR-0002). all new data goes to Supabase EU."},
        {"ts": "2026-04-19T11:02:00Z", "user": "petra",
         "text": "does this change anything for the science-panel content store?"},
        {"ts": "2026-04-19T11:05:00Z", "user": "tomas",
         "text": "nope, content stays the same, just the backend region changes. all EU now."}
    ]
}
docs["__slack-export-eng.json"] = json.dumps(slack_export, indent=2, ensure_ascii=False)

docs["__metrics-export.csv"] = """week_starting,metric,value,target,window,owner
2026-05-04,retention,0.30,0.40,7-day,Data&Growth
2026-05-11,retention,0.31,0.40,7-day,Data&Growth
2026-05-18,retention,0.33,0.40,7-day,Data&Growth
2026-05-04,conversion_free_to_premium,0.047,0.08,30-day,Data&Growth
2026-05-11,conversion_free_to_premium,0.049,0.08,30-day,Data&Growth
2026-05-18,conversion_free_to_premium,0.051,0.08,30-day,Data&Growth
2026-05-18,cac_b2c_eur,17,15,blended,Data&Growth
"""

# ---------------------------------------------------------------------------
written = []
for name, content in docs.items():
    # Files prefixed __ are non-markdown (json/csv) written verbatim.
    fname = name[2:] if name.startswith("__") else name
    (RAW / fname).write_text(content, encoding="utf-8")
    written.append(fname)

print(f"Wrote {len(written)} new docs into {RAW}/")
for w in sorted(written):
    print("  +", w)
