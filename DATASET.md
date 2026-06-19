# BrainFlow Process Wiki — Synthetic Dataset

A small, realistic set of product-development-process documents for **BrainFlow** (a mental-fitness
micro-exercise app for stressed professionals, DACH market). It's designed to feed an LLM wiki
(e.g. Cognee) so the wiki can **align stakeholders by surfacing where the documents disagree**.

The docs contain **deliberately planted contradictions and supersessions** so your ingest →
query → lint demo has guaranteed "money-shot" moments. This file is your cheat sheet — keep it
*out* of what you show the judges.

## Files (`raw/`)
| File | Stakeholder voice |
| --- | --- |
| `prd-brainflow-mvp.md` | Product — canonical MVP spec |
| `adr-0001-frontend-stack.md` | Engineering — client/platform decision |
| `adr-0002-backend-firebase.md` | Engineering — backend (superseded) |
| `adr-0005-backend-supabase.md` | Engineering — backend (supersedes 0002) |
| `roadmap-2026.md` | Product — quarterly plan (has drifted) |
| `decision-log.md` | Cross-team — append-only decisions/meetings |
| `okr-metrics.md` | Data & Growth — metric definitions |
| `sales-commitments.md` | Sales — signed B2B pilot promises |
| `gtm-onepager.md` | Marketing — in-market messaging |
| `content-spec.md` | Content — exercise format |
| `design-spec.md` | Design/UX — screen inventory (transcribed mockups) |
| `ownership-raci.md` | Product — who owns what |

## Planted issues (the demo cheat sheet)
| # | Type | What | Where | "Correct" answer |
| --- | --- | --- | --- | --- |
| A | Contradiction | AI Daily Pick in MVP? | PRD says **Won't have**; Roadmap (Q2) and Decision Log 2026-05-06 say **ship in MVP**; Research motivated it | Out of scope per PRD; pulled in by PM over an Eng scope objection — unresolved |
| B | Supersession | Paywall timing | PRD = **Day 7**; Decision Log 2026-02-14 = **Day 3**; Decision Log 2026-04-09 = **revert to Day 7**; Roadmap still says **Day 3** | Current = **Day 7**; Roadmap is stale |
| C | Contradiction | B2B HR reporting | PRD = **anonymised only**; Sales commitment = **per-employee, by name** | PRD wins; Sales over-promised (GDPR risk) |
| D | Contradiction | "40% retention" meaning | PRD = **30-day** ≥40%; OKR = **7-day** ≥40%; GTM = bare "40% retention" | Same number, different windows — undefined |
| E | Contradiction | Launch order / platform | ADR-0001 = **simultaneous iOS+Android**, persona is **Android**; Roadmap & GTM = **iOS-first** | ADR-0001 wins; Roadmap/GTM contradict it and the primary persona |
| F | Supersession | Backend | ADR-0002 = **Firebase (US)**, status superseded; ADR-0005 = **Supabase (EU)** | Current = **Supabase**, for GDPR/DiGA |
| G | Contradiction | B2C price | PRD/OKR imply **€4.99/mo**; GTM = **€3.99/mo**; Sales B2B = **€22/user/yr** (below the €25.99 >100 tier) | Pricing has no owner → no source of truth |
| H | Contradiction | Exercise length | PRD = **2–5 min**; Content spec = **3–10 min**; GTM = **5 min** | Undefined across teams |
| I | Orphan / gap | No owner | RACI: **Pricing**, **AI Daily Pick**, **Health/DiGA** unassigned; **GDPR DPIA** open question | Lint should flag these |
| J | Gap | Agreed feature missing from design | Research Finding 2 → decision to add a **Brain Score**; Design Progress screen shows level + badges but **no numeric score** | Design hasn't implemented an agreed decision |
| K | Contradiction | Category label drift | Design dashboard tile = **"Emotional IQ"**; Design radar axis = **"Emotional Intelligence"** | Same category, two names |

### How the design spec reinforces existing issues
- **A (Daily Pick):** Dashboard mockup shows a prominent **AI Daily Pick card** — i.e. the design *ships* a feature the PRD marks "Won't have." The clearest visual money-shot.
- **B (paywall):** Upgrade screen is annotated **"Day 3,"** matching the stale roadmap and contradicting the reverted Day-7 decision.
- **C (HR privacy):** B2B HR Dashboard lists employees **by name** with per-person engagement — matches the Sales promise, contradicts the PRD's anonymised-only rule.
- **E (platform):** All frames are in an **iPhone shell with iOS chrome**; no Android frame — contradicts ADR-0001 (simultaneous) and the Android persona.
- **G (price):** Upgrade screen shows **€3.99/mo**, matching GTM, contradicting the PRD's €4.99.
- **H (duration):** Dashboard tiles say **"2–5 min"** but the Exercise screen timer starts at **08:00** — a contradiction *within the design itself*, and it sides with the content spec's 3–10 min over the PRD.

## Ingest (Cognee)
```python
import cognee, asyncio, glob

async def main():
    for path in glob.glob("raw/*.md"):
        await cognee.add(open(path).read(), dataset_name="brainflow")
    await cognee.cognify(["brainflow"])
    # optional: build memory algorithms / self-improvement layer
    # await cognee.memify()

asyncio.run(main())
```
Put each source *type* in its own dataset if you prefer (`dataset_name="prds"`, `"adrs"`, …)
so you can re-ingest one type without disturbing the rest.

## Demo queries that hit the planted issues
- "What's the current premium-upgrade timing, and was it ever changed?" → exposes B (supersession).
- "Is the AI Daily Pick part of the MVP?" → exposes A (PRD vs roadmap vs decision).
- "What does the HR dashboard show employers?" → exposes C (anonymised vs per-employee).
- "What's our retention target?" → exposes D (30-day vs 7-day, same 40%).
- "Which platform do we launch on first?" → exposes E (ADR vs roadmap vs persona).
- "What backend are we using?" → exposes F (Firebase superseded by Supabase).
- "What does BrainFlow Premium cost?" → exposes G (€4.99 vs €3.99 vs B2B rate).
- "Does the current design match the PRD scope?" → exposes A, B, C, H, J at once via the design spec.

## Suggested lint prompt
> Review the BrainFlow wiki. List (1) contradictions between documents, (2) decisions that have
> been superseded but are still referenced elsewhere, (3) features or areas with no owner, and
> (4) unresolved open questions. For each, cite the source documents and state which version is
> current.

A good lint pass should surface B and F as supersessions (with the stale references), A/C/D/E/G/H
as live contradictions, and I as ownership gaps — exactly the misalignments a stakeholder wiki exists to catch.
