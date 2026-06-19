# Skill-improvement API alignment

How Cognost's self-improvement loop maps onto Cognee 1.2's **native** skill API
(`SkillRunEntry`, `improve_skill`, `cognee.improve`). Runnable reference: `brain/skill_native.py`.

## The native primitives (verified against the installed `cognee==1.2.0.dev1`)

| Primitive | Where | What it does |
| --- | --- | --- |
| `Skill` (name, procedure) | `cognee.modules.engine.models` | the maintainer skill as a graph node |
| `SkillRunEntry` | `cognee.memory` | one scored execution record; `success_score ∈ [0,1]`, `feedback ∈ [-1,1]` |
| `cognee.remember(entry=SkillRunEntry(...))` | `api/v1/remember` | persists a run to the **graph** (node_set `skills`) |
| `improve_skill(name, dataset, apply, score_threshold, max_runs)` | `modules/memify/skill_improvement` | reads low-scoring runs → drafts a `SkillImprovementProposal` (`apply=False`); adopts it (`apply=True`) |
| `cognee.remember(skill_improvement={...})` | `api/v1/remember` | the public entry point that drives `improve_skill_from_config` |
| `cognee.improve(dataset, session_ids=[...])` | `api/v1/improve` | distils a scored **session** into the permanent graph |

## 1:1 mapping to Cognost's loop

| Cognost (`brain/`) | Native Cognee API | Note |
| --- | --- | --- |
| `score_answer()` → 0–10 | `SkillRunEntry.success_score` (÷10 → 0–1) | same rubric: cited? · surfaced conflict? · current-vs-superseded? |
| `session/*.jsonl` event | `SkillRunEntry` via `remember()` | session-cache → **graph-backed** run record |
| `selfimprove.propose()` | `improve_skill(..., apply=False)` → `SkillImprovementProposal` | proposal-first; **never auto-applied** |
| `selfimprove.apply()` | `improve_skill(..., apply=True, proposal_id=…)` | adopts proposal, archives the old procedure |
| `distill()` → `cognee.improve(session_ids=…)` | `cognee.improve(...)` | unchanged — complementary session→graph distillation |

**Result:** Cognost's hand-rolled loop and Cognee's native skill API are the *same loop*. The
custom `POLICY_LIBRARY` makes the proposal deterministic for a small local model (reproducible
demo); `improve_skill` does the LLM-drafted equivalent. Both are proposal-first and honour
`CLAUDE.md §3` (never silently resolve, explicit apply).
