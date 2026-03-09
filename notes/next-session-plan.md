# Next Session Plan

## Where we stopped

A large amount of real infrastructure landed:

- `postsmith`
- `workbench`
- `resurfacer`
- `bootstrapper`
- `orbit-map`
- `artifact-health`
- `drift-extractor`
- Workbench review flow + review states
- Workbench promotion queue

The system now has enough moving parts that the next priority is not invention for its own sake, but selective tightening.

## Priority order for next time

### 1. Promotion Queue cleanup slice
This is the most central workflow tool and the one closest to becoming genuinely solid.

Focus:
- queue hygiene
- better defaults for list/filter views
- clear handling for failed/cancelled/executed items
- possibly archive/reset semantics that do not create clutter
- better title defaults if needed

Goal:
Make the residue → queue → artifact path feel clean instead of slightly messy.

### 2. drift-extractor refinement slice
The concept is strong, but the current extraction quality is too shallow.

Focus:
- avoid chopped sentence fragments
- extract fuller unresolved edges with better context
- improve ranking so the top 1–3 candidates feel meaningfully generative
- preserve narrow scope; do not turn it into summarization sludge

Goal:
Make recurrence actually produce useful new material.

### 3. Artifact Health interpretation pass
The tool is already useful, but its diagnostics are blunt.

Focus:
- distinguish true structural issues from current conventions
- reduce overlap between “untagged” and “weakly connected” reporting
- tune what counts as a real problem

Goal:
Keep the report diagnostic rather than noisy.

## Broader operating cadence

Continue using the three-track model:
- workflow
- weird/generative
- diagnostic/visual

Continue using the proven loop:
1. bounded plan
2. implementation (delegate if appropriate)
3. review by hand
4. decide what deepens next

## Delegation guidance

Current sub-agent model policy that actually works:
- Haiku 4.5 → small edits / bounded utility work
- Sonnet → mid-complexity reasoning + implementation
- gpt-5.4 → heavier coding / workflow-sensitive tasks

## Main lesson from this session

Small slices win.
Review matters.
Tools become real when they are forced through actual use, not just designed in the abstract.
