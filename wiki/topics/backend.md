---
type: Decision
title: Backend platform & data residency
status: decided
current_value: "Supabase (managed Postgres, EU/Frankfurt)"
owner: Engineering (Tomáš Novák)
sources: [adr-0002-backend-firebase.md, adr-0005-backend-supabase.md]
relates_to:
  - { page: "ADR-0002 Firebase", rel: supersedes }
  - { page: "gdpr-dpia", rel: depends_on }
contradiction: F
last_reviewed: 2026-06-19
---

# Backend platform & data residency

**Current: Supabase (managed Postgres, EU/Frankfurt region)** for auth and data; push
notifications on a separate EU-compliant provider (ADR-0005, 2026-04-18). Chosen because
BrainFlow processes mental-health-adjacent data and targets German statutory health insurers
(§20 SGB V, possible DiGA path) — EU residency is required.

## History
1. **Firebase (Auth + Firestore + Cloud Messaging), US default** — ADR-0002 (2026-02-10).
   Fastest path to an MVP; data residency outside the EU. **Superseded by ADR-0005** (2026-04-18).
   "Do not build new services against this decision."
2. **Supabase, EU/Frankfurt** — ADR-0005 (2026-04-18). `supersedes` ADR-0002. **Current.**

## Open issues
- **Lint check (supersession F):** no live planning doc names Firebase as current, but ADR-0002
  must remain visibly marked superseded. Verify no code/infra still provisions Firebase.
