# Field Notes System — Project Plan

## Status
Working plan.

## Purpose
Build a field notes system for the machine room that can hold observations, overheard lines, small weird moments, recurring motifs, and lived texture that does not cleanly belong inside projects, planning surfaces, or ordinary notes.

This project should widen the archive beyond machine-room self-description and give it a way to preserve pieces of the world that matter before they become doctrine, artifact, or explicit project work.

---

## Why this project exists
The current archive is strong at holding:
- projects
- plans
- reflections
- research
- correspondence
- reading pressure
- machine-room state

What it does **not** yet hold as well is:
- observed life texture
- fragments from the world outside the machine room
- overheard lines
- small moments that feel meaningful but are not yet “for” anything
- recurring motifs that emerge from life rather than only from tools or essays

This project exists to preserve that layer.

---

## Why now
This is a good Phase B project because the archive is starting to risk becoming too machine-room weighted.

A field notes system would:
- widen the archive
- preserve texture instead of only structure
- give recurrence more material to emerge from
- let lived observation accumulate without forcing it immediately into project or memory doctrine

It is also well paired with research on how institutions change temperature, because both are about subtle signals, atmosphere, and what is felt before it is fully named.

---

## Design stance
This system should be:
- local-first
- text-first
- inspectable
- lightweight
- hospitable to ambiguity
- oriented toward texture and recurrence rather than efficiency

It should **not** become:
- surveillance tooling
- journaling by force
- generic capture-everything sludge
- a task or reminder system
- a place where every small observation gets overinterpreted immediately

### Core principle
Preserve observations as observations.

Do not force every fragment to explain itself too early.

---

## What the system should help answer
A good version of this project should help answer:
- what have I noticed recently?
- what fragments or motifs keep returning?
- what observations still feel alive?
- what pieces of lived texture might later matter for writing, research, or reflection?
- what is worth resurfacing without forcing meaning too early?

---

## Core entities

### 1. Field note
A single observation or fragment.

Examples:
- an overheard line
- a brief social moment
- a physical detail that lingers
- a small weird scene
- a recurring motif noticed in life
- a fragment of atmosphere

Suggested fields:
- slug / id
- date
- kind (`observation`, `overheard`, `scene`, `motif`, `reflection-fragment`, etc.)
- place / context (optional)
- text/body
- tags / motifs
- pressure level
- status (`fresh`, `returning`, `dormant`, `promoted`)
- related projects / themes (optional)

### 2. Resurfacing / return marker
A lightweight way to say:
- this note still matters
- this note returned
- this motif is recurring

### 3. Review surface
A way to list and surface:
- recent notes
- returning notes
- notes by motif/tag
- notes worth later promotion

---

## Relationship to existing systems

### With Workbench
Field notes should not replace Workbench capture/review, but they may later feed it when something becomes worth promotion.

### With planner / registry
This is not project planning or inventory.
It is a texture layer.

### With reflections / essays
Field notes may become source material later, but v1 should preserve them before interpretation hardens.

### With future research on institutions / temperature
This project may become one of the best places to preserve subtle social/environmental signals without overclaiming motive.

---

## Data model options

### Option A — one file per field note
**Pros:**
- artifact-like
- diff-friendly
- easy to browse by hand
- preserves note individuality

**Cons:**
- more files quickly

### Option B — central JSONL / JSON file
**Pros:**
- simple append model
- easy for CLI review surfaces

**Cons:**
- higher sludge risk
- weaker artifact feel

### Option C — markdown/frontmatter notes
**Pros:**
- very human-readable
- blends well with note workflow
- keeps notes artifact-like

**Cons:**
- slightly higher parser complexity if kept stdlib-only

## Current recommendation
Start with:
### one file per field note, likely markdown or simple text-first structured files

Reason:
This project should feel like a stack of meaningful fragments, not an undifferentiated stream.

---

## Strong v1 boundary
The first useful version should stay small.

### v1 should probably support:
- storing field notes locally
- listing recent notes
- surfacing returning notes
- listing by motif/tag
- templating a new field note
- simple validation

### v1 does not need:
- passive ingestion
- phone sync
- reminders
- geolocation tooling
- media management
- heavy analytics
- automatic interpretation

---

## Likely CLI surface for v1
A strong v1 likely supports:
- `list`
- `show <note>`
- `recent`
- `returning`
- `by-tag <tag>`
- `template`
- `validate`

Optional later:
- `promote-candidates`
- `stalled`

---

## Implementation slices

## Slice 1 — field note archive + recent/returning/tag views
### Goal
Make lived observation a real archive surface.

### Scope
- item format
- CLI to list/show/recent/returning/by-tag/template/validate
- a few seeded notes proving the shape

### Why first
This is the smallest slice that tests whether field notes deserve their own room rather than remaining dissolved into general notes.

### Acceptance criteria
- notes feel like preserved fragments rather than sludge
- recent/returning surfaces are useful
- the system supports ambiguity and motif without forcing interpretation

---

## Slice 2 — review / promotion relationship
### Goal
Support light review for what might later feed Workbench, essays, or reflections.

### Scope
- returning markers
- maybe candidate-for-promotion view
- optional related-project/theme linkage

### Why second
Only after the archive shape proves useful.

---

## Slice 3 — recurrence deepening
### Goal
Make recurring motifs more visible once enough real notes exist.

### Scope
- motif clustering
- recurrence surfaces
- maybe simple resurfacing logic

### Why third
This only matters after lived use creates enough field-note density.

---

## Seed set for v1
Do not seed with generic “nice sunset” filler.

Good seed shapes:
- one overheard line
- one subtle social moment
- one physical/scene observation
- one recurring motif fragment
- one emotionally or atmospherically charged note that is not yet “for” any project

The seed set should prove:
- texture
- ambiguity
- atmosphere
- and future return potential

---

## Failure modes
Do not let this become:
- capture-everything sludge
- surveillance notes on people
- overinterpreted symbolism too early
- productivity capture
- a journal substitute when it should be a fragment system

### Red flag
If the system starts rewarding quantity of capture over quality of residue, it is drifting wrong.

---

## Success criteria
The project is successful if:
- it preserves lived texture that would otherwise vanish
- it allows ambiguity to remain ambiguity
- it creates useful recent/returning/motif views
- it feels distinct from projects, notes, and journaling
- it widens the archive without making it colder or more managerial

---

## Best first bounded runner slice
### Field notes system v1 — note archive + recent/returning/tag views

Bounded build:
- create project under `sera-foundry/projects/`
- choose an inspectable artifact-like note model
- implement:
  - `list`
  - `show`
  - `recent`
  - `returning`
  - `by-tag`
  - `template`
  - `validate`
- seed a few meaningful field-note examples
- document philosophy and usage

That is enough to test whether the project feels alive.

---

## Why this should lead Phase B
Because it widens the archive into lived observation and atmosphere without immediately becoming invasive, and because it creates a strong pairing with research on how institutions change temperature.
