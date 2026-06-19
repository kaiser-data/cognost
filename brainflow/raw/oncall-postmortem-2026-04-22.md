---
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
