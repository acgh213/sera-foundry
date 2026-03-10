# Weak Residue Handling Policy

## Status
Working draft v1.

## Purpose
Define how weak residue should be treated in the system without defaulting to deletion, over-cleanup, or false neatness.

This policy follows the first explicit review of weak captures in `notes/weak-residue-review.md`.

---

## Core principle
Weak residue is still residue.
It may retain provenance value, historical value, or evidence of how a tool/system used to behave even when it no longer carries strong active pressure.

The goal is not to erase it.
The goal is to keep it from dominating default views when stronger material now exists.

---

## Current categories

### 1. Meaningful extracted pressure
Short or partial material that still carries real conceptual pressure and should remain visible in ordinary review contexts.

Examples:
- capture #4
- capture #6

### 2. Weak but meaningful planning residue
Short rough notes or seeds that still preserve an early real design pressure.
They are weak as standalone artifacts, but not empty.

Examples:
- capture #1
- capture #2

### 3. Weak low-value residue
Material whose present value is mostly provenance/history rather than live interpretive force.

Examples:
- capture #3
- capture #5

---

## Policy rules

### Rule 1 — Do not delete weak residue by default
Weak residue should remain available for provenance and historical inspection unless there is a later explicit deletion/trashing decision.

### Rule 2 — Default views should not treat all residue equally
Tools and summaries should be allowed to deprioritize **weak low-value residue** in default views.

### Rule 3 — Meaningful extracted pressure should stay visible
Material that still carries real conceptual pressure should not be hidden merely because it is short or extracted.

### Rule 4 — Weak but meaningful planning residue should remain accessible
These captures should usually remain visible in broader review/history contexts, but they do not need to dominate compact default views.

### Rule 5 — Provenance should survive even when pressure fades
If a weak item documents an earlier heuristic/tool weakness or a real early design seed, that historical role still matters.

---

## Default-view recommendation

### In compact/default views
Prefer this order of surfacing:
1. meaningful extracted pressure
2. stronger planning residue
3. weak but meaningful planning residue
4. weak low-value residue only when there is room or when explicitly requested

### In expanded/history views
Show everything, including weak low-value residue.

### Rule
Default views should optimize for current usefulness.
History views should optimize for continuity and provenance.

---

## Marker / state recommendation
At this stage, do **not** add a heavy new state system just for weak residue.

Preferred approach for now:
- lightweight classification in audit/review surfaces
- no deletion
- no complex lifecycle machinery

Possible future step if pressure grows:
- add a simple weak-residue marker or classification field for review tools only

But do not build that yet unless repeated use proves it necessary.

---

## Practical current recommendation
For the current system:
- keep all reviewed captures
- treat #3 and #5 as weak low-value residue
- treat #1 and #2 as weak but meaningful planning residue
- treat #4 and #6 as meaningful extracted pressure
- allow future tools (digest/audit/review helpers) to surface weak low-value residue less aggressively by default

---

## What this means for future work
The next bounded implementation opportunity, if needed, would be something like:
- a small review/audit refinement that classifies or deprioritizes weak low-value residue in default outputs

This should remain a small surface-level improvement, not a new management system.

---

## Anti-goals
Do not:
- delete weak residue just to make the archive look cleaner
- treat all short captures as noise
- create a complicated residue bureaucracy
- hide historical evidence of earlier heuristic weakness
- confuse default surfacing priority with ontological importance

---

## Summary
Weak residue should:
- remain inspectable
- remain historically available
- stop dominating default views when stronger material exists

This is a retrieval and presentation policy, not a purity policy.
