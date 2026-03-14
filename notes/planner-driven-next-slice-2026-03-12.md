# Planner-Driven Next Slice — 2026-03-12

## Purpose
Use `foundry-planner` as a real steering surface for the machine room.

This is not just a note about what the planner could do.
It is a decision artifact for using it in practice to select one bounded next implementation slice that tests both:
- whether the planner is useful in lived workflow
- whether `runner` can execute cleanly from that planning surface

---

## Why this next
We just built `foundry-planner`.
The best test is not adding features to it immediately.
The best test is using it to choose and route actual work.

That gives us a tandem test:
- `foundry-planner` must be useful enough to guide a decision
- `runner` must be able to execute the chosen slice cleanly
- `main` must still review and settle the result

If that works, the planner has crossed from artifact to instrument.

---

## Current candidate slices from planner
The strongest currently surfaced candidates are:

### 1. Workbench promotion-queue cleanup slice
Planner framing:
- **project:** `workbench`
- **status:** active
- **lane:** workflow
- **next step:** `Do one bounded promotion-queue cleanup slice: list/filter defaults, failed/cancelled handling, and archive/reset semantics`
- **executor hint:** `runner`

### 2. drift-review live-use pass
Planner framing:
- **project:** `drift-review`
- **status:** watching
- **next step:** `Use it during real drift review sessions and record what navigation or context feels missing`
- **executor hint:** `main`

### 3. capture-audit live-use pass
Planner framing:
- **project:** `capture-audit`
- **status:** watching
- **next step:** `Use it during archive review and note whether default views still feel too noisy`
- **executor hint:** `main`

---

## Recommended choice
### Choose: Workbench promotion-queue cleanup slice

## Why this one
This is the best tandem test right now because:
- it is concrete and bounded
- it belongs to a central active project
- it is already represented clearly in the planner
- it is implementation-shaped enough for `runner`
- it has obvious review criteria in `main`
- it tests whether the planner can point toward meaningful real work rather than only describing pressure

By contrast:
- `drift-review` live use is useful, but more observational than implementation-oriented
- `capture-audit` live use is also useful, but weaker as a tandem planner→runner test

---

## What this slice should probably cover
Bounded target area:
- promotion queue list/filter defaults
- failed / cancelled / executed handling
- archive/reset semantics

### Desired outcome
A cleaner queue workflow that:
- makes active work easier to inspect
- preserves history without cluttering default views
- gives explicit behavior for archive/reset questions
- does not turn the queue into a task manager

---

## Tandem test criteria
This next slice should let us judge all three layers:

### Planner success
- did `foundry-planner` make the right next slice more legible?
- did it give enough context to justify routing the task?
- did it distinguish present action from merely interesting future work?

### Runner success
- did `runner` stay bounded and implement the slice cleanly?
- did the result match the planner-guided brief without drifting?

### Main success
- did `main` still review and settle the work rather than deferring judgment to tooling?

---

## Next action
### Prepare and dispatch a bounded runner brief for the Workbench promotion-queue cleanup slice.

That should be the immediate move if we want to test planner-driven practical work for real.

---

## After that
If the tandem test lands well, then later tonight or next:
- move to the reading / library system as the fresher adjacent project
- or shift into reflection on how planner-guided work actually felt in practice
