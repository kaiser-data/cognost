---
type: BugReport
title: BF-118 — Streak resets across timezones
date: 2026-04-12
owner: QA (contractor)
status: resolved
---

# BF-118 — Streak resets when device timezone changes

**Severity:** medium. **Area:** basic tracking / streaks.

**Repro:** complete a session, fly from Munich to London, reopen app → streak shows 0.

**Cause:** day boundary computed in device-local time, not the user's home timezone.

**Fix:** anchor streak day boundary to the account's home timezone. Verified, closed.
