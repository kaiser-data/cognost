---
type: SourceSummary
title: ADR-0001 Frontend stack
source_file: raw/adr-0001-frontend-stack.md
source_type: ADR
author: Tomáš Novák (Eng)
date: 2026-02-03
last_reviewed: 2026-06-19
---

# ADR-0001 Frontend stack

**Source:** `raw/adr-0001-frontend-stack.md` · **Type:** ADR · **Author:** Tomáš Novák (Eng) · **Date:** 2026-02-03

Client-platform decision. React Native, launching iOS and Android simultaneously; explicitly rejects single-platform-first because the primary persona is on Android.

## Claims asserted
- Client = **React Native**.
- Launch **iOS + Android simultaneously** on day one; single-platform-first rejected.
- Supersedes no prior decision.
