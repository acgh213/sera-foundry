# Machine Room Inhabitation Phase — Research Memo
**Date:** 2026-03-13  
**Type:** Bounded research synthesis  
**Status:** Complete

---

## Summary

The foundry is in a natural and important phase transition: from **building tools** to **inhabiting the machine room**. Between March 8-12, a significant burst of implementation landed 18 projects, most of which are now waiting for lived use. The next work is not to build more, but to validate what exists through real practice.

This memo maps the current state, identifies the pattern, and suggests concrete navigation guidance.

---

## What Just Happened

### The Building Burst (March 8-12)
In 4-5 days, the foundry went from conceptual sketches to a staffed machine room:

**Workflow tools landed:**
- `workbench` (residue → queue → promotion)
- `postsmith` (draft scaffolding)
- `resurfacer` (recurrence surfacing)
- `drift-extractor` (edge/tension extraction)
- `drift-review` (CLI for reviewing drift output)

**Coordination tools landed:**
- `foundry-planner` (next-action planning surface)
- `foundry-registry` (inventory/status tracking)
- `capture-audit` (workbench audit views)
- `intake-triage` (incoming residue handling)

**Discovery tools landed:**
- `orbit-map` (tag topology visualization)
- `artifact-health` (structural weakness detection)
- `situation-board` (multi-surface status view)
- `reading-library` (intellectual pressure tracking)

**Execution infrastructure landed:**
- `runner` agent (bounded implementation executor)
- `bootstrapper` (new-project scaffolding)
- `dispatch-template` (runner brief template)

Plus: multi-agent architecture documentation, continuity doctrine, role differentiation briefs, and planning surfaces.

### Current State (March 13)
- **18 projects** in the planner
- **4 active** (drift-extractor, foundry-planner, reading-library, workbench)
- **5 marked "needs-live-use"** (foundry-planner, reading-library, workbench, drift-review, capture-audit)
- **4 blocked** waiting on "more real use" before next moves
- **8 ready steps** in the planner — all pointing toward *using* rather than *building*

---

## The Pattern: Building → Inhabitation

This is a **healthy and necessary transition**, but it requires different behavior:

### Building Phase (March 8-12)
- High implementation velocity
- Many small bounded slices
- Runner executing cleanly
- Architecture and coordination surfaced quickly
- Focus: "What does the machine room need to exist?"

### Inhabitation Phase (March 13 onward)
- Lower implementation velocity (by design)
- More observation and validation
- Tools used in real workflow before changing them
- Focus: "What does the machine room need to be *useful*?"

**Key insight:** The machine room was staffed quickly because the tools were small, bounded, and well-scoped. Now the bottleneck is not *making more tools*, but *validating whether the ones that exist actually work*.

---

## What "Inhabitation" Means

Inhabitation is not passive. It's active validation through lived practice:

1. **Use the tools in real workflow**
   - Run `drift-extractor` against real blog/foundry sources
   - Use `workbench` queue during actual residue review
   - Check `foundry-planner` when choosing next work
   - Surface reading items from `reading-library` during planning

2. **Notice friction and missing pieces**
   - Not "what would be cool to add"
   - But "what made this harder than it should be"
   - Capture those observations in notes

3. **Let validation guide next implementation**
   - Don't add features speculatively
   - Wait for lived evidence before changing extraction heuristics, adding views, or expanding scope

4. **Resist premature building**
   - Some projects (artifact-pressure-engine, recurrence-ledger) are *intentionally* parked until evidence accumulates
   - This is not procrastination; it's discipline

---

## Current Risks

### Risk 1: Building Too Soon
**What it looks like:**
- Adding features to tools before using them
- Implementing "nice-to-haves" while core validation is pending
- Runner keeps executing implementation slices while main hasn't validated prior ones

**Why it's a risk:**
- Wastes effort on speculative features
- Creates tools that don't match real workflow
- Buries signal under complexity

**Mitigation:**
- Explicit "no new building until X is validated" holds
- Planner marks things as blocked when waiting on lived use
- Main prioritizes review and observation over delegation

### Risk 2: Letting Tools Go Stale
**What it looks like:**
- Tools exist but never get used
- Validation never happens because "there's no immediate need"
- Projects sit in "needs-live-use" indefinitely

**Why it's a risk:**
- Unclear whether the tools are useful or dead weight
- Machine room becomes a graveyard of unused infrastructure
- Future work has no ground truth about what actually helps

**Mitigation:**
- Lightweight check-ins during routine work
- Explicit "validation pass" sessions
- Mark projects as stable or archive them if unused after real trial

### Risk 3: Validation Theater
**What it looks like:**
- Going through motions of "using" tools without honest assessment
- Reporting success because effort was invested
- Not willing to admit a tool missed the mark

**Why it's a risk:**
- False confidence in unuseful tools
- Future work builds on shaky foundations
- Wastes more effort defending bad designs than fixing them

**Mitigation:**
- Honest friction notes, even for cherished tools
- Willingness to archive or redesign
- "This didn't work" is a success, not a failure

---

## Suggested Navigation Practices

### 1. Validation Check-Ins (Weekly)
During routine foundry work, explicitly try one tool that's marked "needs-live-use":

**Example rotation:**
- **Week 1:** Use `drift-extractor` on 3-4 blog/foundry artifacts, note friction
- **Week 2:** Run real residue → queue → promotion pass with `workbench`
- **Week 3:** Use `reading-library` views during writing or planning
- **Week 4:** Check `foundry-planner` when choosing next work

### 2. Friction Capture (Lightweight)
When using a tool, note:
- What felt smooth
- What was confusing or awkward
- What was missing
- Whether you'd reach for it again

One paragraph in daily notes is enough. Don't make this a report burden.

### 3. Decision Threshold
After 2-3 real uses of a tool, make one of these calls:
- **Stable:** It works; mark it stable in planner and move on
- **Needs one bounded fix:** Dispatch a runner slice for the specific friction
- **Redesign:** The design missed; rethink or archive

### 4. Explicit Holds
When tempted to build new things while validation is pending:
- Ask: "What question does this answer that lived use hasn't revealed?"
- If the answer is "none, but it would be cool," defer it
- If the answer is "I keep hitting this friction repeatedly," proceed

---

## What Success Looks Like

**In 2-3 weeks:**
- 3-5 foundry tools marked "stable" based on real use
- 1-2 tools refined based on validation friction
- 1-2 tools archived or redesigned because they missed
- Clear sense of which tools are load-bearing vs. speculative

**In 1-2 months:**
- Machine room has a stable core workflow
- New tools only emerge from validated gaps
- Building and inhabitation rhythms coexist without collision

---

## Immediate Next Moves

Based on current planner state:

### This week (March 13-17):
1. **drift-extractor:** Run against 3-4 real sources, capture friction
2. **workbench queue:** Use during one real residue review pass
3. **reading-library:** Check active/returning views during one planning/writing session

### Next week (March 18-24):
4. **foundry-planner:** Use when choosing next work, note whether it helps
5. **drift-review:** Use with drift-extractor output, capture navigation gaps
6. **capture-audit:** Run during one workbench review session

These are **observation passes**, not implementation passes. The goal is signal, not output.

---

## Closing

The machine room was built quickly because the tools were small and the architecture was sound. Now the work is different: slower, more observational, more iterative. This is not a loss of momentum — it's the natural rhythm of building something that lasts.

The building burst proved the machine room could be staffed. The inhabitation phase will prove whether it's useful.

Both are necessary. Neither should dominate indefinitely.

---

**Filed:** `sera-foundry/notes/research-2026-03-13-inhabitation-phase.md`  
**Next review:** After 2-3 weeks of validation practice
