---
type: ADR
id: ADR-0001
title: Use React Native for a simultaneous cross-platform launch
status: accepted
date: 2026-02-03
owner: Engineering (Tomáš Novák, Tech Lead)
decided_by: [Tomáš Novák, Lena Hoffmann]
---

# ADR-0001: Use React Native for a simultaneous cross-platform launch

## Context
Our primary persona (Jonas Weber) is on **Android**, but the addressable DACH market and the
later B2B buyers skew toward mixed device fleets. We need to decide the client platform and
launch order.

## Decision
Build the client in **React Native** and launch **iOS and Android simultaneously** on day one.
We explicitly reject a single-platform-first launch: shipping Android-only or iOS-only would
exclude a large share of the target users and the primary persona is on Android.

## Consequences
- One codebase, two stores at launch.
- Slightly slower initial velocity than a single native app, accepted for reach.

## Status notes
Accepted. Supersedes no prior decision.
