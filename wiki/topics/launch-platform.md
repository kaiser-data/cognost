---
type: Decision
title: Launch platform & order
status: decided
current_value: "Simultaneous iOS + Android (React Native)"
owner: Engineering (Tomáš Novák)
sources: [adr-0001-frontend-stack.md, roadmap-2026.md, gtm-onepager.md, design-spec.md]
relates_to:
  - { page: "roadmap-2026", rel: contradicts }
  - { page: "gtm-onepager", rel: contradicts }
contradiction: E
last_reviewed: 2026-06-19
---

# Launch platform & order

**Current: build in React Native and launch iOS and Android simultaneously on day one**
(ADR-0001, 2026-02-03). The ADR explicitly **rejects** a single-platform-first launch because it
would exclude a large share of target users — and the primary persona, **Jonas Weber, is on
Android** (PRD §Target user).

## History
1. **Simultaneous iOS + Android, React Native** — ADR-0001 (2026-02-03, accepted). Standing decision.

## Open issues (contradiction E — live, unresolved)
- **Roadmap Q2 (2026-03-30):** "iOS-first beta … Android ~4 weeks later."
- **GTM (2026-04-25):** featured placement on the Apple App Store for the iOS beta.
- **Design (2026-05-10):** every frame is an iPhone shell with iOS chrome; no Android frame exists.
- Three downstream docs contradict the standing ADR **and** the Android-first persona. Either
  realign them to ADR-0001 or record a new ADR that supersedes it — do not let the drift stand.
