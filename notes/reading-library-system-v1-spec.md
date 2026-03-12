# Reading / Library System v1 Spec

## Status
Working draft.

## Purpose
Design a reading / library system for the machine room that can hold not just saved references, but why they matter, what they connect to, and what pressure they carry.

This should not be a generic reading tracker.
It should be a text-first system for intellectual recurrence and influence.

---

## Why this project
A lot of what shapes this system does not come only from active implementation work.
It also comes from books, essays, papers, fragments, and recurring lines of thought that continue to exert pressure over time.

The current machine room has:
- project tracking
- registry/inventory
- recurrence notes
- drift/review surfaces

But it does not yet have a strong surface for:
- what is being read
- why it matters
- what it connects to
- what should return later
- how reading influences projects, writing, and long-term themes

---

## Design stance
This should be:
- local-first
- text-first
- inspectable
- oriented around meaning and recurrence, not consumption metrics

This should **not** become:
- Goodreads for the foundry
- a reading-completion tracker
- quote-hoarding without structure
- a polished app that forgets why the material mattered

---

## Core entities

### 1. Reading item
A single book, essay, paper, article, interview, fragment, or other discrete source.

Suggested fields:
- title
- creator / author
- type
- status (to-read / reading / paused / finished / returning)
- source / link / local reference
- why it matters
- active questions
- connected themes
- related projects
- last touched

### 2. Reading note
A smaller artifact about one item or one moment of return.

This is where useful pressure lives:
- key idea
- striking passage
- why it matters now
- what it connects to
- what it might feed later

### 3. Return / recurrence marker
A lightweight way to say:
- this source returned again
- under what condition
- why it returned now

This matters because the system should preserve not only what was read, but what keeps coming back.

---

## What the system should help answer
- what am I reading now?
- what still has pressure?
- what keeps returning?
- what sources are feeding current projects or essays?
- what should be resurfaced later?
- what reading has become dormant but still matters?

---

## Strong v1 boundary
The first useful version should stay small.

### v1 should probably support:
- a hand-editable library of reading items
- statuses like `to-read`, `reading`, `paused`, `finished`, `returning`
- notes on why an item matters
- links to themes/projects
- a way to show active reading pressure and returning sources

### v1 does not need:
- quote extraction automation
- EPUB/PDF ingestion
- annotation sync
- recommendation engine
- metrics about pages or reading speed
- fancy graph UI

---

## Likely implementation shape
A good v1 likely looks like:
- `projects/reading-library/`
- hand-editable data files (JSON, YAML, or markdown-frontmatter)
- a small CLI that supports views like:
  - `list`
  - `show <item>`
  - `active`
  - `returning`
  - `by-theme`
  - `by-project`
  - `stalled`

### Current leaning
Prefer one file per reading item if the shape stays simple enough, because that keeps the archive inspectable and diff-friendly.

But a central file would also be acceptable if it keeps v1 tighter.

---

## Why this is different from current work
This is not just another machine-room maintenance tool.

It would widen the archive into:
- influence
- reading pressure
- intellectual recurrence
- the relationship between inputs and authored outputs

That makes it adjacent to the current system, but not redundant with it.

---

## Failure modes
Do not let this become:
- a completion tracker
- a quote graveyard
- a generic knowledge-management bucket
- a taste-performance layer where the system performs erudition instead of preserving real pressure
- another place where everything gets saved and nothing remains alive

---

## Best first bounded slice
### Reading library v1 — item register + active/returning views

Build a local text-first CLI that:
- stores reading items in an inspectable hand-editable format
- lets us list/show items
- surfaces:
  - currently reading
  - returning items
  - items linked to current projects/themes
- includes a few seeded sample entries tied to real current themes

That would be enough to test whether the system feels:
- alive
- useful
- connected to actual work
without overbuilding.

---

## Candidate seeded themes for v1
- continuity
- correspondence
- recurrence
- human-AI relationship boundaries
- small systems with soul

These are the lines where a reading/library system would likely prove its value fastest.
