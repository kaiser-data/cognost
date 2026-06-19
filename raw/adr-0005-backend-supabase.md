---
type: ADR
id: ADR-0005
title: Move the backend to Supabase (EU region) for GDPR / health-data residency
status: accepted
supersedes: ADR-0002
date: 2026-04-18
owner: Engineering (Tomáš Novák, Tech Lead)
decided_by: [Tomáš Novák, Lena Hoffmann]
---

# ADR-0005: Move the backend to Supabase (EU region)

## Context
BrainFlow processes mental-health-adjacent usage data and aims to partner with German
statutory health insurers (§20 SGB V, possible DiGA path). Storing user data in the US
(ADR-0002) creates GDPR and health-data-residency problems and complicates any DiGA route.

## Decision
Replace Firebase with **Supabase (managed Postgres, EU/Frankfurt region)** for auth and data.
Push notifications move to a separate EU-compliant provider.

## Consequences
- All user data stays in the EU.
- Migration cost from the Firebase prototype, accepted.

## Status notes
Accepted. **Supersedes ADR-0002.**
