# BrainFlow brain — saved states

Two snapshots of the `brainflow` brain (Cognee Cloud), before and after the skill develops.
These are the "initial brain" and "restructured brain" pictures from the 3-min demo (Beat 2).

| | `brain-initial.json` | `brain-restructured.json` |
| --- | --- | --- |
| Active skill | baseline v1 ("be concise, give a direct answer") | maintainer (3 learned policies) |
| Edges | generic / untyped | typed: contradicts · supersedes · owned_by |
| Contradiction register | none | maintained |
| **Open contradictions** | **0** ("looks healthy") | **6** |
| Supersessions flagged | 0 | 2 |
| Metric drift flagged | 0 | 1 |
| Ownership orphans flagged | 0 | 4 |
| Self-assessment | "looks healthy" | "keeps itself honest" |

Same 42 sources, same graph — the difference is the **skill**. The 11 planted misalignments
are latent in the initial brain and surfaced (with provenance + current-vs-superseded) in the
restructured one.

Visual: `../brain-diagnostic.html` (published artifact) animates this transition — the counter
ticks **0 → 6** as the contradiction edges ignite.
