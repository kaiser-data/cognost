---
type: OpenQuestion
title: GDPR Data Protection Impact Assessment (health data)
status: open
current_value: "Unresolved — no owner"
owner: (none) — flagged
sources: [decision-log.md, ownership-raci.md, adr-0005-backend-supabase.md, sales-commitments.md]
relates_to:
  - { page: "backend", rel: depends_on }
  - { page: "hr-dashboard", rel: depends_on }
contradiction: I
last_reviewed: 2026-06-19
---

# GDPR Data Protection Impact Assessment (health data)

**Current: open, no owner.** Do we need a formal GDPR DPIA before the health-insurer pilots?
Raised in the Decision Log 2026-05-19; no owner assigned; unresolved.

## Why it matters
- BrainFlow processes mental-health-adjacent data and targets German statutory health insurers
  (§20 SGB V / DiGA) — the reason the backend moved to EU Supabase (ADR-0005).
- The Q4 health-insurer / DiGA pilots plausibly **depend on** a completed DPIA.
- The unresolved HR-dashboard contradiction (C) — individual-level data in a signed contract —
  raises the stakes further.

## Open issues
- **No owner** (RACI: Health insurance / DiGA track unassigned; "who owns the GDPR DPIA?" listed as
  an open question). Lint must keep surfacing this until an owner is named.
