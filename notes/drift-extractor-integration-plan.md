# Drift-Extractor Integration Plan

## Status
Working plan.

## Purpose
Define how `drift-extractor` should connect to the rest of the system now that:
- the tool itself has become strong enough to matter
- recurrence structures are starting to exist
- the machine room has a clearer continuity substrate

The goal is not to expand `drift-extractor` randomly.
The goal is to connect it in ways that preserve its strength: surfacing unresolved pressure from existing artifacts.

---

## Current judgment
`drift-extractor` is now one of the strongest distinctive tools in the foundry.

What it already does well:
- finds unresolved pressure inside artifacts
- returns candidate tensions rather than generic summaries
- preserves some context and pressure labels
- acts as one of the first real recurrence → new material tools

What it does **not** yet do:
- connect cleanly to recurrence structures
- distinguish between extraction value and later review value
- feed a structured recurrence layer
- help separate meaningful extracted pressure from weak low-value residue at the workflow level

---

## Integration principle
`drift-extractor` should not become a universal analysis engine.
It should stay narrow.

Its job is:
- detect unresolved pressure inside an artifact
- produce candidate returns/tensions
- hand them into better downstream structures

That means integration should happen **after extraction**, not by making extraction itself enormous.

---

## Best current integration targets

### 1. Recurrence structures
This is now the strongest target.

Why:
- the new recurrence note gives drift outputs somewhere more meaningful to go
- extracted tension can become a return event or pressure input rather than just a loose capture

Possible relationship:
- drift extraction produces candidate pressure
- recurrence note/log decides whether the candidate represents a meaningful return

### 2. Workbench review flow
Why:
- drift outputs currently become captures, but they are not yet clearly distinguished in downstream review
- review should be able to tell the difference between strong extracted pressure and weak extraction residue

Possible relationship:
- review helpers or summaries could surface extracted pressure differently from ordinary captures

### 3. Digest surfaces
Why:
- the digest is now part of normal workflow
- it may eventually need to reflect recurrence/drift pressure without becoming cluttered

Possible relationship:
- not full integration yet, but a future compact section for live drift pressure or reviewed extracted items

---

## Recommended integration order

### Step 1 — conceptual alignment
Treat `drift-extractor` outputs as candidates for recurrence structures, not just generic captures.

This is mostly a framing shift, but it matters.

### Step 2 — review-layer distinction
Add a small workflow distinction between:
- meaningful extracted pressure
- weak low-value extraction residue

This may happen through existing audit/review surfaces rather than through `drift-extractor` itself.

### Step 3 — one bounded integration slice
Only after the above should a concrete integration slice be implemented.

---

## Best first bounded slice
### Candidate: drift review helper
A small helper surface that:
- lists extracted drift captures
- shows pressure labels/context
- helps distinguish strong extracted pressure from weak residue
- optionally groups by source artifact

Why this first:
- bounded
- directly useful
- supports recurrence thinking without forcing a whole new system
- keeps `drift-extractor` itself narrow

---

## Alternative bounded slice
### Candidate: recurrence-ready drift export
A small output mode or helper that emits drift results in a shape more useful for obsession notes / return logs.

Why maybe later instead of first:
- slightly more abstract
- easier to get wrong without seeing the recurrence structures used a bit first

---

## What not to do yet
Do not:
- make `drift-extractor` a global meaning engine
- force all extracted drift into a recurrence ontology
- add heavy state or dashboard surfaces
- try to solve review, recurrence, and extraction quality all at once
- build pressure-engine implementation on top of unresolved drift integration assumptions

---

## Immediate recommendation
The next live path should be:
1. keep using the new recurrence structures note
2. let the continuity obsession note exist as the first real recurrence experiment
3. then dispatch one bounded **drift review helper** or equivalent review-surface slice

That preserves the order:
- recurrence framing first
- drift integration second

Which is the correct sequence.
