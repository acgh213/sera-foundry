# Research Brief — Lived-Use Bottleneck in the Foundry (2026-03-20)

## Why this thread
A single thread appears repeatedly across planning notes, project goals, and blockers:

> Most active projects are no longer blocked by missing code; they are blocked by missing **lived-use evidence**.

This makes it the best current internal thread to deepen, because it directly affects sequencing across Workbench, drift surfaces, and newer archive tools.

## Evidence snapshot
From `projects/foundry-planner/plan.json` and adjacent notes:

- Workbench, reading-library, correspondence-archive, field-notes, voice-style-workshop, drift-extractor, drift-review, and capture-audit all explicitly call for real use before adding features.
- `drift-extractor` and `drift-review` are both waiting on review passes, not conceptual design.
- `next-attention-plan.md` and the integration notes already warn against speculative expansion.

Pattern: the machine room has enough architecture and enough tools; the weak point is now **decision quality under real usage**.

## Diagnosis
The current risk is not under-building. It is **parallel uncertainty**:

- too many active surfaces each waiting for “use it and see”
- no single recurring protocol that turns usage into comparable evidence
- easy drift back into design memos instead of operational decisions

If this continues, projects stay in an “active but unproven” state and the center of gravity blurs.

## Bounded recommendation
Introduce one small cross-project proving loop instead of adding new features:

## "Two-Project Proof Cycle" (1 week pilot)

At any moment, only two projects are in explicit proving mode:

1. **Center project**: one workflow-core surface (default: Workbench)
2. **Edge project**: one weird or archive surface (default: drift-review or reading-library)

Everything else remains watch/maintenance unless a breakage appears.

### Required output per proof pass (short, inspectable)
For each proving session, write a 6-line log entry (in a single note file):

1. task attempted
2. command(s) used
3. friction observed
4. what worked
5. decision: keep / adjust / defer
6. concrete next action (if any)

This creates comparable evidence without introducing dashboards.

### Graduation gate for a feature request
A queued feature only advances when both are true:

- the same friction appears in **2+ independent proving logs**
- the fix can be stated as one bounded slice

This preserves the current doctrine: operationalize before expanding.

## Suggested immediate pairing
For the next cycle:

- **Center:** Workbench (residue → review → promotion path)
- **Edge:** drift-review (strong vs weak extracted pressure in practice)

Reason: this pair sits directly on the continuity substrate and resolves the most central uncertainty cluster first.

## What to postpone (explicitly)
For this week, defer:

- by-theme/by-project expansion in reading-library
- second-slice enrichments for field-notes/correspondence/workshop
- any pressure-engine implementation work

These are good ideas, but they are downstream of proving discipline.

## Bottom line
The highest-value move is not another tool slice. It is a tiny recurring evidence protocol that makes “needs lived use” actionable and comparable. Once that exists, sequencing decisions become clearer and faster.