---
type: ADR
id: ADR-0002
title: Use Firebase as the backend
status: superseded
superseded_by: ADR-0005
date: 2026-02-10
owner: Engineering (Tomáš Novák, Tech Lead)
decided_by: [Tomáš Novák]
---

# ADR-0002: Use Firebase as the backend

## Context
We need auth, a realtime data store, and push notifications quickly to validate the MVP.

## Decision
Use **Firebase** (Auth + Firestore + Cloud Messaging) for the MVP backend, hosted on Google
infrastructure (default US multi-region).

## Consequences
- Fastest path to a working MVP.
- Data residency is outside the EU by default.

## Status notes
**Superseded by ADR-0005** on 2026-04-18. Do not build new services against this decision.
