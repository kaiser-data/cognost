---
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
