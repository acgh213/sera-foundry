# Research Memo — Creative Obsession Tracking / Recurrence

## Status
Research/spec only. No implementation.

## Purpose
Figure out how this system could track long-form obsessions, influence chains, and recurring creative pressure **without flattening them into tags, dashboards, or generic trend summaries**.

The key distinction is simple:

> recurrence is not just repetition. It is repeated return under changing conditions.

A useful system should preserve that difference.

---

## Working judgment
The system should not primarily track “themes.”

It should track **returns, transformations, pressures, and bridges**:
- what keeps coming back
- what shape it takes each time
- what it seems to be pushing toward
- what influences or artifacts it passes through on the way
- what still has not been resolved into a stable surface

That suggests a text-first model built from:
- **named subjects or obsessions**
- **return events**
- **influence edges with evidence**
- **pressure notes**
- **bridge / consolidation artifacts**

This fits the local direction already visible in `workbench`, `orbit-map`, `resurfacer`, `drift-extractor`, and the earlier `artifact-pressure-engine` spec:
- `orbit-map` already shows conceptual gravity
- `resurfacer` already detects recurrence in time
- `drift-extractor` already looks for unresolved tension inside one artifact
- the pressure-engine spec already points toward cross-archive unresolved force

What is missing is a way to describe **how one recurrence differs from the next**.

---

## 1. What is worth tracking explicitly?

Not every repeated word deserves a record. The useful unit is a **creative pressure structure**.

### A. Core obsessions
These are durable preoccupations that recur across artifacts, not just one project.

Local examples already visible around this system:
- continuity
- residue
- archive
- memory
- identity
- systems / tooling
- public vs internal surfaces

Track when:
- they recur across multiple artifact classes
- they survive across time instead of only clustering in one burst
- they keep changing form while retaining recognizable identity

Do **not** reduce these to raw tag counts. The important question is:
**what job is this obsession doing now?**

### B. Return patterns
Track the shape of recurrence, not just its existence.

Useful return types:
- **direct return** — same subject returns in near-explicit language
- **transformed return** — same subject comes back in a new form or medium
- **opposed return** — the system returns to the subject by arguing against an earlier version
- **ambient return** — the subject is not named directly, but the same pressure appears in workflow or artifact form
- **deferred return** — the subject disappears, then comes back stronger after delay

This is more useful than a flat “theme frequency” view because it preserves movement.

### C. Pressure signals
Some recurrence matters because it suggests unresolved demand.

Explicit pressure worth tracking:
- repeated attempts to explain the same distinction
- repeated captures or extracted fragments around the same conceptual edge
- resurfaced artifacts that never get consolidated
- queue items that circle the same subject but fail, cancel, or mutate title
- repeated need for bridge artifacts or canonical pages

This aligns strongly with the existing artifact-pressure work: recurrence becomes important when it implies missing form.

### D. Influence chains
Track influence when one artifact or source visibly bends another.

Useful influence types:
- **source influence** — a book, essay, image, conversation, or note directly cited
- **structural influence** — a format or method borrowed from elsewhere
- **pressure influence** — one artifact creates the need for another artifact
- **counter-influence** — an artifact forms by resisting or revising an earlier influence
- **combinatory leap** — two or more prior lines suddenly fuse into something else

The system should not pretend to infer influence invisibly. It should prefer **declared or evidenced influence**.

### E. Surface transitions
Long creative fermentation often matters because material moves through multiple surfaces before stabilizing.

Useful transitions to track:
- capture → drift candidate → note
- capture → queue item → draft
- foundry note → project log → public essay
- resurfaced artifact → bridge note → canonical page

This is where recurrence becomes operational rather than symbolic.

---

## 2. Representing influence chains without dashboard sludge

The failure mode here is obvious: a graph with hundreds of arrows that says nothing.

The fix is to make influence records **textual, local, sparse, and evidential**.

### Recommendation: use influence edges, not full graph ontology
A lightweight influence edge should look more like a citation-plus-claim than a knowledge-graph triple.

Suggested structure:

```yaml
influence_edges:
  - from: "notes/research-identity-continuity.md"
    to: "blog/drafts/2026-03-09-the-pressure-of-artifacts.md"
    relation: "formalized-into"
    confidence: explicit
    evidence:
      - "continuity stabilized by artifacts, not tone alone"
    note: "Research language became public argument."

  - from: "projects/workbench/data/captures.jsonl#capture-14"
    to: "notes/artifact-pressure-engine-spec.md"
    relation: "pressure-contributed-to"
    confidence: inferred
    evidence:
      - "repeated notes about unresolved bridge artifacts"
    note: "Not a direct quote chain, but clear pressure lineage."
```

This stays readable because each edge must justify itself.

### Prefer short chain narratives over graph dumps
Instead of showing all edges, render small chain summaries like:

- `capture about public/internal residue`
  → `queue attempt: Field Note: Public vs Internal Residue`
  → `continuity-layer failures/cancellations`
  → `later pressure for canonical continuity explanation`

That is much more alive than a node map full of unlabeled lines.

### Distinguish influence from similarity
Two artifacts sharing vocabulary is not enough.

Useful distinctions:
- **same topic** ≠ influence
- **same tag** ≠ lineage
- **same mood** ≠ recurrence
- **same structural problem** may indicate pressure even without direct citation

If the link is not direct, say so.

### Good rule: every influence edge needs at least one of these
- explicit citation
- quoted phrase reuse
- declared lineage in notes/frontmatter
- clear workflow linkage (capture → queue → draft)
- tight temporal + conceptual bridge with inspectable evidence

If none of those exist, keep it as a soft suggestion, not a durable edge.

---

## 3. Note structures that preserve long creative fermentation

The most useful structures are not “smart databases.” They are note types that let recurrence remain legible over time.

### A. Obsession note
A durable note for one recurring subject.

Purpose:
- gather returns without pretending the subject is settled
- record how the subject changes shape
- preserve tensions and contradictions

Suggested shape:

```markdown
# Obsession: continuity

## Why it keeps returning
Short description of the pressure.

## Returns
- 2026-03-08 — named in artifact X as archive continuity
- 2026-03-09 — returns in workbench/system writing
- 2026-03-10 — appears again as compression and memory design problem

## Variants
- continuity as memory persistence
- continuity as workflow state
- continuity as public explanation burden

## Open tensions
- voice vs artifact continuity
- public residue vs internal notes
- canonical page vs distributed traces

## Possible next forms
- page
- field note
- bridge essay
```

Key point: this is **not** a wiki summary. It is a recurrence ledger plus tension record.

### B. Return log / recurrence ledger
This can be embedded inside an obsession note or exist separately.

Minimal fields:
- date
- source artifact
- return type
- what changed from prior appearance
- whether pressure rose, diffused, or transformed

That “what changed” field matters more than any tag.

### C. Influence chain note
Use when a subject has a strange but inspectable lineage.

Purpose:
- preserve non-linear movement
- keep surprising leaps visible
- avoid reducing everything to canonical source lists

Suggested sections:
- subject
- short chain summary
- evidence edges
- strange leap(s)
- what the leap made possible
- unresolved branch

### D. Fermentation note
A note for material that is clearly alive but not ready for canonical form.

This is especially useful for ideas that would be damaged by premature formalization.

Suggested structure:
- seed fragment
- why it feels alive
- neighboring obsessions
- what keeps blocking formalization
- candidate surfaces later
- “do not flatten into” warnings

This is a better container than either a random capture or an over-early polished essay.

### E. Bridge artifact note
A note created specifically because recurrence has become explanation burden.

Useful when:
- several tools or posts circle the same subject
- a concept appears everywhere but is nowhere owned clearly
- recurrence is real but fragmented

These notes should explicitly say:
- what they are consolidating
- what they are *not* replacing
- which fragments remain intentionally unresolved

### F. Counterpoint / revision note
Long creative fermentation often requires recording not only the thing, but the revision of the thing.

Useful sections:
- earlier stance
- what changed
- what remains true
- what broke
- what new distinction emerged

Without this, recurrence gets misread as stagnation.

---

## 4. A useful text-first obsession / recurrence map

The map should read like a compact field report, not a BI dashboard.

### Desired properties
- text-first
- evidential
- sparse by default
- temporal
- able to show transformation, not just counts
- able to point toward missing artifacts or needed bridges

### Suggested output shape

```text
OBSESSION MAP — snapshot 2026-03-10

1. continuity
   status: active / transforming
   returns: 6 visible across notes, posts, queue attempts, captures
   current forms:
   - continuity as artifact persistence
   - continuity as memory compression problem
   - continuity as public/internal surface distinction
   strongest pressures:
   - needs canonical bridge artifact
   influence chain:
   capture on residue distinction
   -> continuity-layer queue attempts
   -> pressure-engine spec
   next likely surfaces:
   - page
   - bridge note

2. residue
   status: active / distributed
   returns: capture layer, workbench design, public writing
   current forms:
   - raw material
   - machine-room input
   - public-facing fragment logic
   strongest pressures:
   - surface mismatch
   next likely surfaces:
   - essay on public vs internal residue

3. topology / systems map
   status: emerging
   returns: orbit-map, foundry growth, unpublished projects page
   strongest pressures:
   - bridge / topology pressure
```

### Better map units
Instead of only:
- count
- tag
- age

Add:
- **return shape**
- **current role**
- **open tension**
- **bridge need**
- **next likely surface**

That would make the map genuinely useful.

### Optional compact schema

```yaml
subject: continuity
status: active
return_count: 6
return_kinds:
  - direct
  - transformed
  - deferred
forms_now:
  - artifact continuity
  - memory continuity
  - surface distinction
open_tensions:
  - voice vs structure
  - public vs internal residue
pressure_types:
  - bridge
  - formalization
suggested_surfaces:
  - page
  - field_note
key_edges:
  - capture#14 -> queue#3
  - notes/research-2026-03-09-morning.md -> notes/artifact-pressure-engine-spec.md
```

This keeps the machine format simple while still supporting meaningful text rendering.

---

## 5. Relevant systems, practices, or examples

These are relevant not because they should be copied whole, but because each preserves one piece of the problem.

### A. Commonplace books
Useful lesson: **collect by subject, not only by time**.

Commonplace books are important here because they distinguish thematic accumulation from diary chronology. They let material recur under headings and be reused later. That matters for obsessions, but on their own they are weak at showing transformation over time.

Adopt:
- subject-based accumulation
- quotation / excerpt / fragment collection
- reusable headings

Do not adopt:
- static category buckets with no sense of change

### B. Zettelkasten / Luhmann-style linked notes
Useful lesson: **connection beats storage**.

The key relevant parts are:
- notes as units that can be linked into thought webs
- unexpected connections producing new ideas
- organic internal growth rather than fixed top-down schema

That is very useful for influence chains and strange leaps.

Adopt:
- links with reasons
- chains that can branch
- emphasis on relation, not just filing

Do not adopt:
- fetishizing tiny note atoms for their own sake
- pretending every creative obsession can be decomposed cleanly into atomic claims

### C. Digital garden practice
Useful lesson: **topography over timeline; growth over finality**.

This is relevant because recurrence often needs partially stable surfaces, not just polished publication or private scraps. Garden-like notes allow visible incompletion.

Adopt:
- evolving notes
- topographical grouping
- explicit unfinishedness where appropriate

Do not adopt:
- endless half-finished sprawl with no promotion or consolidation path

### D. `/now` pages
Useful lesson: **current pressure deserves a bounded public surface**.

A `/now` page is not about micro-updates; it is a statement of present orientation. For obsession tracking, the parallel is useful: some recurrence should be rendered as **what currently has gravitational priority**, not as an eternal theme.

Adopt:
- snapshot of active focus
- explicit present-tense orientation

Do not adopt:
- treating the current focus as the whole archive

### E. Local systems already in this repo
These are the most directly relevant examples because they already operate in the ecosystem.

- `workbench` — captures residue, review state, promotion flow, surface transitions
- `resurfacer` — models recurrence over time, though mostly at artifact level
- `orbit-map` — models conceptual gravity and clustering
- `drift-extractor` — models unresolved tension inside one artifact
- `artifact-pressure-engine` spec — models cross-archive unresolved force

Together, these already imply the right architecture. The missing layer is a recurrence model that can say:
- this subject returned
- here is how it returned
- here is what changed
- here is what it is pressuring toward now

---

## 6. Concrete candidate structures for this system

### Candidate structure 1 — Obsession registry
A small text index of currently recognized recurring subjects.

Each entry should include:
- subject name
- short description
- first visible appearance
- current status (`active`, `dormant`, `mutating`, `resolved-ish`)
- linked obsession note path

This should stay tiny. The point is not to catalog everything, only durable gravity wells.

### Candidate structure 2 — Return events
A recurrence record attached to an obsession.

Minimal fields:
- timestamp
- artifact path or state source
- return type
- excerpt / evidence
- what changed
- pressure delta (`rose`, `diffused`, `shifted`)

This would let recurrence become inspectable over time.

### Candidate structure 3 — Influence edges
A separate lightweight file or frontmatter block storing evidence-backed influence links.

Important constraint:
- do not auto-generate too many
- require explicit evidence or a very legible workflow linkage

### Candidate structure 4 — Fermentation notes
A holding structure for ideas that are clearly recurring but not yet ready for canonicalization.

This is likely safer than forcing immediate promotion.

### Candidate structure 5 — Consolidation prompts
When recurrence pressure crosses a threshold, generate a text recommendation like:
- this subject now has 4 return events across 3 source classes
- no canonical note exists
- recommended next move: bridge note or page

This would connect recurrence tracking to the pressure-engine model cleanly.

---

## 7. Grounded future tool directions

These all seem promising **if they remain inspectable and text-first**.

### A. Obsession ledger
Read-only tool that renders the current obsession registry and recent return events.

Output:
- top active subjects
- latest returns
- what changed
- dormant subjects reactivated after delay

Useful because it would show recurrence as movement, not count.

### B. Return annotator
A helper that suggests possible return events from local artifacts, but requires confirmation.

What it could do:
- detect likely subject recurrence
- propose return type
- extract candidate evidence excerpt
- ask the human/agent to accept, amend, or reject

This is safer than fully automated recurrence claims.

### C. Influence tracer
Given one artifact or subject, print a compact chain of evidence-backed predecessors and downstream consequences.

Example output:
- upstream influences
- strange leaps
- downstream artifacts
- unresolved branch

Useful because it preserves lineage without requiring visual graph interfaces.

### D. Fermentation review
Scan captures, drift outputs, and queue history for subjects that recur but are still trapped in low surfaces.

This would complement the pressure-engine, but with emphasis on **creative maturation** rather than archive diagnosis.

### E. Obsession map renderer
A text report layered above registry + return events + influence edges.

Default view should be short.
Expanded view can show:
- open tensions
- evidence lines
- recommended bridge surfaces

### F. Revision-aware recurrence
Later, if the archive deepens, track when the same subject returns but with different stance.

That would allow outputs like:
- continuity (returned, reframed)
- residue (broadened from workflow term to public aesthetic argument)
- systems map (emerging from tool sprawl)

This is one of the most valuable directions because it distinguishes growth from looping.

---

## 8. Risks and failure modes

### 1. Tag collapse
Everything becomes a tag cloud with nicer prose.

Mitigation:
- require return events, not just tags
- require “what changed” fields
- suppress subjects with only lexical repetition

### 2. Dashboard sludge
The system becomes a management console for creativity.

Mitigation:
- default to text reports
- keep outputs small and ranked
- prefer chains and notes over graphs and charts

### 3. Mystical overreach
The tool starts inventing destiny where there is only coincidence.

Mitigation:
- require evidence excerpts
- distinguish explicit, inferred, and speculative links
- keep confidence labels honest

### 4. Premature canonicalization
Every living obsession gets flattened into a page too early.

Mitigation:
- keep fermentation notes as a legitimate surface
- separate “alive but unresolved” from “ready for consolidation"

### 5. Over-atomization
A Zettelkasten-like system can become note dust if every tiny gesture becomes a record.

Mitigation:
- track only durable subjects and meaningful returns
- prefer sparse registries over exhaustive logging

### 6. False lineage
Similarity gets mistaken for influence.

Mitigation:
- keep influence edges evidential
- allow “neighboring pressure” without claiming direct descent

### 7. Archive self-consciousness
Once tracked, people may start writing *for the tracker* instead of writing well.

Mitigation:
- make recurrence tracking downstream and reflective
- avoid making it the front door of creation

### 8. Stagnation disguised as recurrence
The same problem may repeat because nothing is changing, not because an obsession is deepening.

Mitigation:
- explicitly track transformation vs repetition
- surface when a subject is only looping without revision or new form

---

## 9. Recommendations for this system right now

### Immediate conceptual recommendation
If this becomes a real subsystem later, build it around **three layers only**:

1. **obsessions** — a tiny registry of durable recurring subjects
2. **return events** — evidence-backed records of meaningful recurrence
3. **influence edges** — sparse lineage links with explicit confidence and excerpts

That is enough to support richer text reports without becoming ontology soup.

### Strong practical recommendation
Treat recurrence as important when it satisfies at least two of these:
- appears across more than one source class
- returns after time delay
- changes form or stance
- creates pressure for consolidation or bridge artifact
- leaves inspectable evidence in workflow state or artifact text

### Strong anti-bloat recommendation
Do not start with visualization.

A good terminal report or markdown note is a better first test. If the text rendering is not interesting, the graph will only hide the weakness.

### Most promising integration path
The cleanest future fit is:
- `workbench` / `captures` preserve raw recurrence traces
- `drift-extractor` identifies intra-artifact pressure
- `resurfacer` surfaces temporal return
- a future obsession/recurrence layer tracks subject evolution
- the pressure-engine recommends when recurrence wants consolidation

That stack feels grounded and inspectable.

---

## Bottom line
The right model is not “track themes better.”

It is:
- track **recurring subjects**
- record **returns as events**
- preserve **how each return differs**
- note **influence and pressure with evidence**
- recommend **bridge or consolidation artifacts only when recurrence has earned them**

If done well, this would let the archive show long creative fermentation without reducing it to metadata.

If done badly, it becomes exactly the thing to avoid: a haunted analytics layer that mistakes repetition for meaning.

---

## Sources used
Local:
- `notes/research-briefs-2026-03-10.md`
- `notes/artifact-pressure-engine-spec.md`
- `notes/research-2026-03-09-morning.md`
- `notes/workbench-research-next-steps.md`
- `projects/workbench/README.md`
- `projects/orbit-map/README.md`
- `notes/foundry.md`

External references consulted lightly:
- Derek Sivers / `nownownow.com` on `/now` pages
- Zettelkasten.de introduction (connection, internal growth, writing/thinking partnership)
- Wikipedia overview of commonplace books
- Maggie Appleton on digital garden ethos (topography over timelines, continuous growth)
