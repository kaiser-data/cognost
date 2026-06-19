# my_skills/ — the agent skills the brain runs and improves

This folder holds the **maintainer skills** that govern how Cognost answers. Each `.md` file is
a skill: its filename is the skill name, its body is the skill *procedure* (loaded as the
`system_prompt` for `cognee.recall`). These map directly onto Cognee's `Skill` graph nodes
(`name` + `procedure`), discovered by `find_skill_by_name(...)`.

| File | Role |
| --- | --- |
| `wiki-maintainer.baseline.md` | **Before** — naive v1: "be concise, give a direct answer". No provenance, no conflict-surfacing. |
| `wiki-maintainer.md` | **After** — the learned skill: provenance mandatory, preserve contradictions, current-vs-superseded. |

## How the skill improves itself (native Cognee API)

The self-improvement loop is Cognee's native skill API — see `../brain/SKILL_API_ALIGNMENT.md`
and the runnable `../brain/skill_native.py`:

1. **Run** — `recall(query, GRAPH_COMPLETION)` with the skill as `system_prompt`.
2. **Record** — each scored answer becomes a `SkillRunEntry` (`success_score ∈ [0,1]`) via
   `cognee.remember(entry=SkillRunEntry(...))` — graph-backed, not just session cache.
3. **Propose** — `improve_skill(skill_name, dataset, apply=False)` reads the low-scoring runs
   and drafts a `SkillImprovementProposal` (status `proposed`, never auto-applied).
4. **Apply** — `improve_skill(skill_name, dataset, apply=True, proposal_id=…)` adopts it; the
   previous procedure is archived.

The brain **learns its own operating rules from its own low-scoring answers**, sourcing each new
rule from the `CLAUDE.md` contract — `baseline → maintainer` is the captured before/after.
