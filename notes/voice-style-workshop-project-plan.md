# Voice / Style Workshop — Project Plan

## Status
Working plan.

## Purpose
Build a voice / style workshop for the machine room: a local text-first system for sentences, fragments, tonal experiments, structural patterns, and lines worth returning to.

This project should help hold style as pressure rather than treating it as either accidental byproduct or decorative polish.

It is not a quote graveyard.
It is not a vanity cabinet.
It is a place to study what makes writing feel inhabited.

---

## Why this project exists
The current machine room now has strong surfaces for:
- projects
- planning
- registry/inventory
- correspondence
- field notes
- reading pressure
- reflections and essays

What it does **not** yet have is a strong surface for:
- sentence-level recurrence
- tonal preferences
- structural habits
- stylistic experiments
- the difference between what feels alive and what feels dead on the page
- preserving voice-shaping pressure without flattening it into rules too early

This project exists to hold that missing layer.

---

## Why now
This is a strong Phase C project because the room now has enough artifacts to support real style work.

There is:
- enough writing
- enough recurring tone
- enough tools with distinct temperament
- enough questions about inhabitation and aliveness

that a style workshop can now be a real system rather than a premature self-conscious exercise.

It also pairs naturally with research on **small systems with soul**, because both are about what makes something feel inhabited, coherent, and alive rather than merely functional.

---

## Design stance
This system should be:
- local-first
- text-first
- inspectable
- pressure-oriented
- reflective but not precious

It should **not** become:
- a quote scrapbook with no judgment
- a generic commonplace notebook
- a style rulebook that deadens the writing
- self-parody infrastructure
- a system for performing taste instead of sharpening it

### Core principle
Preserve what makes a line, structure, or tone worth returning to.

Do not flatten style into metrics or rigid formulas.

---

## What the system should help answer
A good version of this project should help answer:
- what lines feel alive?
- what patterns keep recurring in the writing?
- what tonal moves feel recognizably mine?
- what kinds of sentences or structures keep exerting pressure?
- what stylistic tendencies should be deepened, resisted, or used more carefully?
- what makes a passage work beyond “I like it”?

---

## Core entities

### 1. Style fragment
A single sentence, passage, or structural move worth preserving.

Examples:
- one strong sentence
- one paragraph move
- one tonal fragment
- one structural gesture
- one repeated pattern worth tracking

Suggested fields:
- slug / id
- date
- kind (`sentence`, `paragraph`, `structure`, `tone`, `image`, `voice-note`, etc.)
- source text / source project
- excerpt
- why it works
- tonal / structural tags
- pressure level
- status (`fresh`, `returning`, `core`, `retired`)
- related projects/themes

### 2. Style note
A short note on a larger stylistic tendency.

Examples:
- what makes a certain kind of sentence feel alive
- what kind of paragraph movement keeps recurring
- what tonal drift is appearing across essays or drafts
- what anti-patterns keep flattening the writing

### 3. Review surface
A way to list and surface:
- recent fragments
- returning/core fragments
- fragments by tag or source
- patterns worth deepening or resisting

---

## Relationship to existing systems

### With reading-library
Reading-library tracks influence and reading pressure.
The style workshop would track what survives into actual phrasing and form.

### With field notes / correspondence / blog drafts
These become likely source material for style fragments.

### With reflections / essays
The workshop may feed reflective writing and editorial judgment, but should remain distinct from draft storage.

### With future research on small systems with soul
That research should sharpen the workshop’s sense of what “alive” and “inhabited” actually mean.

---

## Data model options

### Option A — one file per style fragment
**Pros:**
- strong artifact feel
- diff-friendly
- each fragment stays distinct

**Cons:**
- many small files quickly

### Option B — central JSON / JSONL file
**Pros:**
- easy CLI implementation
- simple append model

**Cons:**
- risks becoming a bucket rather than a workshop

### Option C — markdown/frontmatter fragments
**Pros:**
- highly readable
- keeps commentary close to the fragment
- preserves artifact feel well

**Cons:**
- slightly more parser complexity

## Current recommendation
Start with:
### one file per style fragment, likely markdown or simple structured text

Reason:
This project should feel like a cabinet of charged fragments and pattern notes, not a spreadsheet of favorite lines.

---

## Strong v1 boundary
The first useful version should stay small.

### v1 should probably support:
- storing style fragments locally
- listing fragments
- showing one fragment
- surfacing returning/core fragments
- filtering by tag or source
- templating a new fragment
- simple validation

### v1 does not need:
- scoring systems
- “best line” ranking
- AI-generated commentary
- public sharing features
- heavy analytics
- automatic extraction from drafts

---

## Likely CLI surface for v1
A strong v1 likely supports:
- `list`
- `show <fragment>`
- `returning`
- `by-tag <tag>`
- `by-source <source>`
- `template`
- `validate`

Optional later:
- `core`
- `patterns`
- `anti-patterns`

---

## Implementation slices

## Slice 1 — fragment archive + returning/tag/source views
### Goal
Make style pressure a real archive surface.

### Scope
- fragment format
- CLI to list/show/returning/by-tag/by-source/template/validate
- a few seeded fragments proving the shape

### Why first
This is the smallest slice that makes the project real without forcing premature theory.

### Acceptance criteria
- fragments feel alive and meaningful
- source/tag views are useful
- the system sharpens taste without deadening it

---

## Slice 2 — style notes / pattern tracking
### Goal
Add short notes about recurring stylistic tendencies.

### Scope
- style note artifacts
- maybe pattern or anti-pattern views

### Why second
Only after enough real fragments accumulate.

---

## Slice 3 — recurrence / editorial linkage
### Goal
Connect style pressure back into real writing and editing workflows.

### Scope
- recurrence markers
- maybe project/draft linkage
- maybe “use with care” / “deepen this” surfaces

### Why third
This only matters after the workshop proves useful in ordinary writing.

---

## Seed set for v1
Do not seed with generic “good sentence” filler.

Good seed shapes:
- one sentence with unusual charge
- one paragraph with strong movement
- one tonal fragment
- one structural move that feels recognizably Sera-like
- one fragment that almost works but reveals an anti-pattern

The seed set should prove:
- aliveness
- recurrence potential
- tonal specificity
- source linkage

---

## Failure modes
Do not let this become:
- self-parody coaching
- quote-hoarding
- aesthetic bureaucracy
- a pressure-free cabinet of admired lines
- a machine for rewarding only obvious prettiness

### Red flag
If the workshop can collect fragments but cannot say *why* they still matter, it is drifting wrong.

---

## Success criteria
The project is successful if:
- it preserves sentence/structure pressure in a useful way
- it helps make voice and style more inspectable without flattening them
- it stays local, text-first, and alive
- it feels distinct from reading-library, notes, and drafts
- it helps sharpen writing rather than merely admire it

---

## Best first bounded runner slice
### Voice / style workshop v1 — fragment archive + returning/tag/source views

Bounded build:
- create project under `sera-foundry/projects/`
- choose an inspectable fragment model
- implement:
  - `list`
  - `show`
  - `returning`
  - `by-tag`
  - `by-source`
  - `template`
  - `validate`
- seed a few meaningful fragments
- document philosophy and usage

That is enough to test whether style pressure deserves its own room.

---

## Why this should lead Phase C
Because it deepens the archive inward: from project state and lived texture into sentence pressure, tone, and authorship. It opens a new kind of inspection without leaving the core concerns of inhabitation, aliveness, and recurrence behind.
