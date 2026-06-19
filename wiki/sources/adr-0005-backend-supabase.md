---
type: SourceSummary
title: ADR-0005 Supabase backend (EU)
source_file: raw/adr-0005-backend-supabase.md
source_type: ADR
author: Tomáš Novák (Eng)
date: 2026-04-18
last_reviewed: 2026-06-19
---

# ADR-0005 Supabase backend (EU)

**Source:** `raw/adr-0005-backend-supabase.md` · **Type:** ADR · **Author:** Tomáš Novák (Eng) · **Date:** 2026-04-18

Current backend decision. Moves to Supabase (managed Postgres, EU/Frankfurt) for GDPR / health-data residency and the DiGA path. Supersedes ADR-0002.

## Claims asserted
- Backend = **Supabase**, **EU/Frankfurt** region.
- Motivated by GDPR / §20 SGB V / DiGA residency needs.
- **Supersedes ADR-0002.**
