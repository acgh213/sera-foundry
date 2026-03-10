# Creative Recurrence Structures

## Status
Working draft v1.

## Purpose
This note picks the first small recurrence structures worth actually trying.

It does **not** attempt to define a full recurrence system.
The goal is to keep the creative-recurrence thread alive in a usable, text-first form without hardening it too early into a taxonomy, dashboard, or graph fetish.

---

## Why this note exists
The recurrence memo established an important distinction:

> recurrence is not just repetition. It is repeated return under changing conditions.

That means the system does not primarily need better tags.
It needs a small set of structures that can preserve:
- what keeps coming back
- how it returns
- what changed
- what it seems to be pushing toward now

The first iteration should be modest.
If it works, it can deepen later.

---

## Chosen first structures

### 1. Obsession note
### 2. Return log / recurrence ledger

These are the first two structures worth trying.

### Why these two
Together they give:
- one durable subject surface
- one temporal record of how the subject keeps returning

That is enough to test recurrence as a real design problem without overbuilding.

---

## Structure 1 — Obsession note

### Purpose
A durable note for one recurring subject, pressure field, or long-running fascination.

The goal is **not** to summarize the subject completely.
The goal is to preserve:
- why it keeps returning
- what forms it keeps taking
- what tensions remain live
- what it seems to be pushing toward

### When to make one
Create an obsession note when most of the following are true:
- the subject has returned across multiple artifacts, notes, or conversations
- it survives across time, not just one burst of intensity
- it keeps changing form while retaining recognizable identity
- it has enough pressure that losing track of it would distort future work or interpretation

### Suggested sections
```markdown
# Obsession: <name>

## Why it keeps returning
Short description of the pressure.

## Current role
What job the obsession seems to be doing now.

## Returns
- date / artifact / short note on how it returned
- date / artifact / short note on how it returned

## Variants
Different forms or surfaces it has taken.

## Open tensions
What remains unresolved.

## Likely next forms
Where it seems to be pushing next.
```

### Important rule
This note should remain alive and partial.
It is a pressure ledger, not a wiki page.

### Failure mode
If it becomes a polished encyclopedia entry, it has probably gone dead.

---

## Structure 2 — Return log / recurrence ledger

### Purpose
A compact record of meaningful recurrence events.

This is the structure that tracks:
- **this returned**
- **how it returned**
- **what changed**
- **whether pressure intensified, transformed, or diffused**

### Why it matters
Without a return log, recurrence collapses into:
- vague memory
- tag frequency
- or retrospective storytelling

The return log keeps recurrence inspectable.

### When to log a return
Log a return when:
- a recurring subject clearly reappears in a new artifact, note, or workflow event
- the return is meaningful, not just lexical coincidence
- something about the return changed form, pressure, or direction

### Suggested fields
```markdown
- date:
- subject:
- source artifact / note / event:
- return type:
- what changed:
- current pressure:
- likely next surface:
```

### Recommended return types
Use a small vocabulary at first:
- **direct return** — same subject returns explicitly
- **transformed return** — same subject returns in a new form or medium
- **opposed return** — the subject returns as revision/resistance to an earlier form
- **ambient return** — the pressure returns without the same explicit language
- **deferred return** — it disappeared for a while, then came back stronger

### Important rule
The “what changed” field matters more than any tag.

That is what preserves recurrence as movement rather than repetition.

---

## Why not start with influence chains
Influence chains are interesting, but they are more fragile.

They require:
- stronger evidence
- more careful distinctions between similarity and lineage
- more restraint to avoid false narrative certainty

So for now:
- keep influence as a warm secondary idea
- do not make it a first structure

If obsession notes and return logs prove useful, influence edges can come later.

---

## Where these structures should live
For now, these should remain **notes-first structures**.

Likely home:
- `notes/`
- possibly a subfolder later if the number grows enough to need structure

Do **not** start by making them a database or dashboard.

Text-first use is the right first test.

---

## Suggested naming pattern
### Obsession notes
- `notes/obsession-<slug>.md`

### Return logs
Either:
- embedded inside the obsession note
or
- `notes/recurrence-log-<slug>.md`

### Current recommendation
Start with the return log embedded inside the obsession note.
That keeps the first experiment compact.

---

## First live test recommendation
Do not start with a trivial subject.
Start with something that already has visible recurrence and real pressure.

Good candidates might include:
- continuity
- public vs internal residue
- memory / archive / return
- execution vs coordination

### Current recommendation
The strongest first test is probably:
## **continuity**

Why:
- it recurs across notes, essays, tools, and architecture
- it links the practical and the personal
- it has already changed form multiple times
- it remains central without being exhausted

---

## Relationship to existing tools
These structures should complement the current foundry tools rather than replace them.

### Current tool relationships
- `workbench` captures residue
- `resurfacer` catches temporal return
- `drift-extractor` catches intra-artifact unresolved pressure
- `orbit-map` catches conceptual gravity
- `artifact-pressure-engine` spec imagines cross-archive force

### What recurrence structures add
They preserve:
- how the return changed
- what role the subject is currently playing
- what it seems to be pushing toward

That is the missing middle layer.

---

## Anti-goals
Do not:
- turn recurrence into tag math
- build a dashboard
- invent a rigid ontology too early
- flatten living pressure into a neat theme list
- imply lineage/influence where evidence is weak
- make the structure so formal that it stops feeling alive

---

## Current recommendation
The next actual experiment should be:
1. create one obsession note
2. embed a small return log inside it
3. use a subject with real existing recurrence
4. review whether the structure stays alive or immediately turns dead

### Best current candidate
- `continuity`

If that works, then later follow-ups could include:
- a second obsession note on a more creative/media-linked subject
- a separate influence-edge experiment
- drift-extractor integration designed around recurrence rather than generic extraction
