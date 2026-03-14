# Reading / Library System — Project Plan

## Status
Working plan.

## Purpose
Build a reading / library system for the machine room that can hold not only what is being read, but why it matters, what it connects to, and what keeps returning.

This project should preserve intellectual pressure and influence in a way that stays alive rather than flattening reading into inventory or completion tracking.

---

## Why this project exists
The current machine room already has strong surfaces for:
- projects
- planning
- registry/inventory
- recurrence notes
- drift/review
- continuity and memory doctrine

What it does **not** yet have is a strong surface for:
- reading as an ongoing source of pressure
- influence across books, essays, papers, fragments, and references
- what keeps returning from reading into projects, writing, and long-term themes
- how inputs become part of the archive rather than disappearing into “I read that once”

This project exists to hold that missing layer.

It should answer a different question from Workbench or the planner.

- `workbench` helps hold residue and promotion state
- `foundry-registry` tracks what exists
- `foundry-planner` tracks what the machine room is trying to do next
- **reading / library system** should help hold what is being intellectually metabolized and why it still has pressure

---

## Design stance
This system should be:
- local-first
- text-first
- inspectable
- recurrence-aware
- oriented toward meaning rather than consumption metrics

It should **not** become:
- Goodreads for the foundry
- a completion tracker
- quote-hoarding without structure
- a knowledge-management bucket with no pressure model
- a taste-performance layer where the system performs erudition instead of preserving real influence

### Core principle
Track not just what was read, but what still matters.

---

## What the system should help answer
A good version of this project should help answer:
- what am I reading now?
- what still has pressure?
- what keeps returning?
- what reading is feeding current projects, notes, or essays?
- what has gone dormant but still matters?
- what deserves resurfacing later?
- what reading has become part of the system’s long-term intellectual shape?

---

## Core entities

### 1. Reading item
A discrete source.

Examples:
- book
- essay
- paper
- article
- interview
- fragment
- blog post
- talk/transcript

Suggested fields:
- slug
- title
- creator / author
- type
- status
- source / link / reference
- why it matters
- active questions
- connected themes
- related projects
- last touched
- notes / pointers

Suggested statuses:
- `to-read`
- `reading`
- `paused`
- `finished`
- `returning`
- `dormant`

### 2. Reading note
A smaller artifact about one item or one encounter with it.

Useful contents:
- key idea
- striking passage or summary fragment
- why it matters now
- what it connects to
- what it might feed later

This is where the living pressure often sits.

### 3. Return / recurrence marker
A lightweight record that says:
- this source returned
- under what condition
- why now
- what changed this time

This matters because recurrence is different from completion.

### 4. Project/theme linkage
A way to say a reading item is feeding:
- one project
- one essay
- one recurring theme
- one long-term line of thought

This should stay light and inspectable.

---

## Relationship to existing systems

### With Workbench
The reading system should not duplicate Workbench capture/review flow.
But it may eventually feed Workbench when reading notes become artifact candidates.

### With recurrence notes
The reading system should complement recurrence structures by making sources and returns legible.

### With planner/registry
The reading system is neither inventory nor project planning.
It is intellectual/input pressure tracking.

### With blog/foundry writing
It should help preserve:
- what fed a draft
- what is still unresolved from a source
- what may deserve a note, essay, or future project

---

## Data model options

### Option A — one central JSON file
**Pros:**
- simplest initial implementation
- easy CLI reads/writes
- compact v1

**Cons:**
- can become dense as the library grows
- less artifact-like per source

### Option B — one file per reading item
**Pros:**
- diff-friendly
- inspectable
- each source gets a durable artifact
- easier to keep note-like

**Cons:**
- slightly more implementation overhead
- directory management needed

### Option C — markdown/frontmatter items
**Pros:**
- most human-readable
- strongest artifact feel
- blends well with note-based workflow

**Cons:**
- parser complexity slightly higher
- may be slower to stabilize for v1

## Current recommendation
Start with:
### **one file per reading item, likely JSON or markdown-frontmatter if the implementation stays simple**

Reason:
This project wants to feel like a living library, not a single opaque blob.
One-item-per-file better matches that shape.

If that becomes too heavy for v1, a central JSON fallback is acceptable.

---

## CLI surface for v1
A strong bounded v1 likely supports:
- `list`
- `show <item>`
- `active`
- `returning`
- `by-theme <theme>`
- `by-project <project>`
- `stalled`
- `template <slug> <title>`
- `validate`

### What these should answer
- what is live right now?
- what is returning?
- what is connected to a current line of work?
- what reading pressure has gone dormant?

---

## Implementation slices

## Slice 1 — Item register + active/returning views
### Goal
Make the reading system real enough to hold current reading pressure.

### Scope
- data shape for reading items
- CLI to list/show active and returning items
- simple validation
- small seeded set tied to real current themes

### Why first
This is the smallest slice that makes the project real without overbuilding.

### Acceptance criteria
- can record reading items meaningfully
- can surface active/returning items
- feels like a reading pressure surface, not a list of titles

---

## Slice 2 — Reading notes / pressure links
### Goal
Attach or relate reading notes to items and current themes/projects.

### Scope
- note pointers or embedded note entries
- surface why an item matters now
- optional link to themes/projects

### Why second
This is where the system starts to become more than a register.

---

## Slice 3 — Recurrence / resurfacing support
### Goal
Track returns and resurfacing of reading items over time.

### Scope
- return markers
- `returning` view deepened by real recurrence
- maybe “not touched but still live” surfaces

### Why third
This only makes sense after the underlying library shape proves useful.

---

## Seed set for v1
The first version should not use fake generic examples.
Seed it around live machine-room themes.

Suggested seeded lines:
- continuity
- correspondence
- recurrence
- human-AI relationship boundaries
- small systems with soul

These are good because they already have pressure and cross-links to current projects and writing.

---

## Failure modes
Do not let this become:
- a completion tracker
- a reading challenge board
- quote-hoarding without pressure
- a dead bibliography
- a generic PKM inbox
- an erudition-performance layer
- a system that records sources while losing why they mattered

### Red flag
If the library gets better at storing reading than at explaining why something still matters, the project is drifting wrong.

---

## Success criteria
The project is successful if:
- it helps hold real reading pressure
- it helps explain what sources are feeding current work
- it preserves recurrence and influence better than saved links do
- it stays small, inspectable, and text-first
- it feels like a living library rather than a progress tracker

---

## Best first bounded runner slice
### Reading / library system v1 — item register + active/returning CLI

Bounded build:
- create project under `sera-foundry/projects/`
- pick a small inspectable data model
- implement:
  - `list`
  - `show`
  - `active`
  - `returning`
  - `validate`
  - `template`
- seed a few real sample entries around live themes
- document usage and philosophy

That is enough to test whether the project feels alive.

---

## Why this should probably be the next adjacent project
Because it is:
- adjacent but not repetitive
- deeply connected to recurrence, influence, style, and authorship
- likely to reveal new structure in the archive
- and less likely than some other ideas to drift immediately into invasive or managerial behavior

It widens the machine room without making it colder.
