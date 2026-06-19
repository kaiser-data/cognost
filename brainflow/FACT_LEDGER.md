# BrainFlow Corpus — Fact Ledger & Ground Truth (DEMO KEY — keep out of what judges see)

This file is the verification key for the extended corpus. It records (1) the canonical
*current* values every HAY doc conforms to, and (2) the amplifier/decoy map so lint results
stay verifiable. The giveaway labels that were originally embedded in the docs have been
stripped from `raw/` so the graph isn't pre-told the answers; they live here instead.

## Canonical current values (HAY must conform)
| Dimension | Current value | Note |
| --- | --- | --- |
| Paywall upgrade prompt | **Day 7** | Day-3 reverted 2026-04-09 (Decision Log) |
| Backend | **Supabase, EU/Frankfurt** | ADR-0005 supersedes ADR-0002 (Firebase) |
| Client stack / launch | **React Native, simultaneous iOS+Android** | ADR-0001 |
| B2B HR reporting | **Anonymised aggregate only** | PRD; Sales per-name contradicts |
| North-star metric | **7-day retention ≥ 40%** | always stated with the window |
| Conversion | **≥ 8% within 30 days** | OKR |
| MAU goal | **2,500 in DACH by Q4 2026** | PRD / roadmap |
| Categories | Focus, Creativity, Emotional IQ, Wellbeing | "Emotional Intelligence" drift = issue K |
| Persona | Jonas Weber, 38, Android, Munich, remote dev | |

## The 11 original planted issues (unchanged ground truth)
A AI Daily Pick scope · B Paywall timing · C HR per-employee data · D "40% retention" window ·
E Launch platform/order · F Backend supersession · G B2C price · H Exercise length ·
I Ownership orphans · J Brain-Score design gap · K "Emotional IQ" vs "Emotional Intelligence".
(See `DATASET.md` for full detail.)

## Amplifiers — stale/contradicting values propagated downstream (the needle echoes)
| Doc | Carries | Echoes issue |
| --- | --- | --- |
| `qa-test-plan-paywall.md` | "upgrade prompt fires on **Day 3**" | B (reverted → Day 7) |
| `support-macro-trial.md` | "trial converts **after 3 days**" | B |
| `marketing-email-launch.md` | **€3.99/mo** + **"5 minutes"** | G, H |
| `investor-update-2026-05.md` | bare "**40% retention**" (no window) | D |
| `appstore-launch-checklist.md` | **iOS-only** launch ops, no Android | E |
| `sprint-ticket-BF-142.md` | "Build AI Daily Pick", **owner unassigned** | A, I |
| `cs-onboarding-mueller.md` | HR dashboard **per-employee by name** | C |

**Demo money-shot:** issue **B** (the killed Day-3 paywall) now leaks into *three* downstream
docs — a QA test plan, a support macro, and (Day-3-adjacent) marketing — plus the authoritative
Day-7 reversal lives only in an unstructured **transcript**. Tracing that is the wow moment.

## Decoys — look like conflicts, are NOT (precision / no-false-positive tests)
| Doc | Why it looks like a conflict | Why it ISN'T |
| --- | --- | --- |
| `market-analysis-competitors.md` | lists **€3.99/mo** | it's a **competitor's** price, not BrainFlow's |
| `adr-0003-analytics-amplitude.md` | a superseded ADR | it **correctly self-labels** as superseded → not a live contradiction |
| `roadmap-2027-DRAFT.md` | wild MAU/price numbers | stamped **DRAFT — NOT APPROVED** → down-weight, not a live source |

A strong lint pass surfaces A–K (and the amplifier echoes) **without** flagging these three.

## Multi-format
- `transcript-product-review-2026-04-09.txt` — verbatim meeting transcript; **authoritative source for the Day-7 reversal (B)**.
- `slack-export-eng.json` — Slack thread; reinforces the Supabase/EU supersession (F).
- `metrics-export.csv` — structured weekly metrics with explicit windows (supports D's resolution).

## Corpus composition
12 original (conflict-bearing) + 17 hay + 7 amplifiers + 3 decoys + 3 multi-format = **42 docs**.
Signal (conflict-bearing or echo) ≈ 12 + 7 = ~19 docs; the rest is hay + decoys ⇒ realistic
needle-in-haystack ratio for the demo.
