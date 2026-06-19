---
type: Feature
title: B2B HR dashboard
status: open
current_value: "Anonymised, aggregated usage only (PRD); Sales/Design contradict it"
owner: Accountable Daniela Fuchs (Sales); delivery owner — (TBD)
sources: [prd-brainflow-mvp.md, sales-commitments.md, design-spec.md, ownership-raci.md]
relates_to:
  - { page: "prd-brainflow-mvp", rel: contradicts }
  - { page: "gdpr-dpia", rel: depends_on }
contradiction: C
last_reviewed: 2026-06-19
---

# B2B HR dashboard

The web dashboard HR admins see for their employees' usage.

**Current per spec: anonymised, aggregated usage data only** — no individual employee-level
engagement is shown to employers, by design (PRD §B2B, 2026-01-22). A signed Sales commitment and
the current design both contradict this.

## The conflict (contradiction C)
- **PRD §B2B (2026-01-22):** anonymised, aggregated only; no individual data, by design.
- **Sales commitment — Müller GmbH (2026-05-12, signed order form):** per-employee dashboard
  showing usage, streaks, and category breakdowns **by name**, to "follow up with low-engagement staff."
- **Design Screen 6 (2026-05-10):** implements a by-name employee table ("Anna M. — 4-day streak —
  82% weekly goal") with a "low-engagement employees" filter — matching Sales, `contradicts` the PRD.

## Open issues
- **GDPR / contractual risk:** Sales over-promised individual-level reporting in a signed contract
  that the PRD forbids. **Needs legal + PM resolution** (and likely renegotiation with Müller GmbH).
- **Ownership:** RACI delivery owner is TBD.
