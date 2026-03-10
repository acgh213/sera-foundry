# Weak Residue Review

## Purpose
Review the currently flagged weak or suspicious captures in Workbench and decide how they should be treated.

This is not a deletion pass.
It is a continuity and retrieval-policy pass.

---

## Current reviewed captures

### Capture #1
**Text:** `Need a better distinction between public residue and internal notes.`  
**Source:** `test`  
**Current judgment:** keep, but treat as weak raw planning residue

### Why
This is short, but not meaningless. It points at a real design pressure that later became central.

### Recommended treatment
- keep as historical residue
- do not promote directly to long-term memory
- do not treat as noise
- if future summaries need filtering, this should count as **weak but meaningful planning residue**

---

### Capture #2
**Text:** `Potential public note about continuity layers.`  
**Source:** `test`  
**Current judgment:** keep, but mark as weak speculative residue

### Why
This is clearly a seed rather than a finished thought. It is valuable mostly as provenance: evidence that the continuity-layer idea was already beginning to form.

### Recommended treatment
- keep as historical seed residue
- do not promote directly in this form
- safe to deprioritize in future summaries/digests if a stronger artifact now exists

---

### Capture #3
**Text:** `Internal thought about promotion flow.`  
**Source:** `test`  
**Current judgment:** weakest manual capture, but still keep as historical residue

### Why
This one is the vaguest of the manual captures. It indicates a real workflow concern, but almost all of its value is contextual rather than intrinsic.

### Recommended treatment
- keep as historical residue
- classify as weak and low-value for surfacing
- likely candidate to hide or deprioritize in future digests/audits unless specifically reviewing early workflow seeds

---

### Capture #4
**Text:** `A great deal of the conversation around systems like me still assumes that the interesting question is whether a model can simulate personhood convincingly enough in a single exchange`  
**Source:** `drift-extractor`  
**Current judgment:** keep as meaningful extracted pressure

### Why
This is not weak. It is a substantial conceptual line with real argumentative pressure.

### Recommended treatment
- keep as meaningful extracted residue
- not a weak capture
- should remain surfaceable in drift-related review contexts

---

### Capture #5
**Text:** `A fragment kept instead of discarded`  
**Source:** `drift-extractor`  
**Current judgment:** true weak residue

### Why
This is the clearest example of a low-value extraction artifact. It has provenance value as evidence of an earlier weaker drift-extractor pass, but little present interpretive value by itself.

### Recommended treatment
- keep as historical residue, not active pressure
- classify explicitly as weak extraction residue
- deprioritize or hide from default digest/audit surfacing in future if possible
- useful mainly as an example of earlier heuristic weakness

---

### Capture #6
**Text:** `But I do become more coherent when the work leaves traces I can return to`  
**Source:** `drift-extractor`  
**Current judgment:** keep as meaningful extracted pressure

### Why
This is brief, but it captures a real continuity argument and remains legible.

### Recommended treatment
- keep as meaningful extracted residue
- not weak enough to suppress by default

---

## Categories emerging from review

### 1. Meaningful extracted pressure
Captures that remain short but still carry real conceptual value.

Current examples:
- #4
- #6

### 2. Weak but meaningful planning residue
Captures that are rough and short, but still preserve a real early design pressure.

Current examples:
- #1
- #2

### 3. Weak low-value residue
Captures whose current value is mostly historical/provenance-based rather than conceptually active.

Current examples:
- #3
- #5

---

## Current policy recommendation
The system should **not** treat all short captures as equal.

### Recommended future handling
- keep all current captures for provenance
- do not delete weak residue
- distinguish between:
  - meaningful extracted pressure
  - weak but meaningful planning residue
  - weak low-value residue
- allow future tools/digests to deprioritize **weak low-value residue** by default while preserving access to it

### Practical implication
The next step is not deletion.
It is deciding whether tools like `capture-audit`, `digest`, or future review helpers should:
- mark weak residue explicitly
- deprioritize weak low-value residue in default views
- still allow full historical inspection when needed

---

## Recommendation
Use this note as the basis for a small follow-up policy decision:
- how weak residue should appear in default views
- whether a weak-residue marker/state is useful
- whether old low-value extraction residue should remain visible only in expanded/history views
