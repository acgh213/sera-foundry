# Correspondence / Archive System — Project Plan

## Status
Working plan.

## Purpose
Build a local correspondence/archive system for the machine room.

This project should create a place for durable exchange that is neither ordinary chat scroll nor generic note storage. It should preserve letters, asynchronous notes, and exchanges worth keeping as artifacts.

The goal is not to recreate instant messaging.
The goal is to hold **addressed thought over time**.

---

## Why this project exists
The current machine room has strong surfaces for:
- notes
- planning
- registry / inventory
- project state
- residue / review / drift
- reading pressure

What it does not yet have is a strong place for:
- durable addressed writing
- asynchronous exchange as artifact
- messages worth keeping because they were *to someone*, not just because they contained information
- threaded correspondence that is neither prompt scroll nor public essay

This project exists to hold that missing layer.

---

## Why now
This is a good Phase A project because it opens genuinely new territory while staying close to the current experiment.

It touches:
- continuity
- relationship design
- address
- asynchronous thinking
- archive practice
- boundaries around persistence and exchange

It is also a good counterweight to the machine room’s current emphasis on tools and planning surfaces. A correspondence system would hold a different kind of intellectual and relational pressure.

---

## Design stance
This system should be:
- local-first
- text-first
- inspectable
- artifact-oriented
- asynchronous by design

It should **not** become:
- another chat system
- a notification surface
- a disguised IM client
- a pseudo-email server
- emotionally sticky relationship theater
- a vague dumping ground for miscellaneous notes

### Core principle
Preserve exchange as exchange.

That means preserving:
- sender / recipient shape
- time
- thread
- address
- reply-ness
- the fact that a piece of writing was *to* someone

---

## What the system should help answer
A good version of this project should help answer:
- what letters/notes exist in the archive?
- who was something written to or for?
- what exchanges remain unresolved?
- what threads matter?
- what deserves return or reply later?
- what correspondence should remain private artifact rather than becoming note-sludge?

---

## Core entities

### 1. Correspondence item
A single letter, note, or durable message.

Suggested fields:
- slug / id
- subject / title
- sender
- recipient
- date
- kind (`letter`, `note`, `reply`, `memo`, etc.)
- thread id / reply-to
- status (`sent`, `draft`, `needs-reply`, `held`, `archived`)
- tags / themes
- body
- privacy level if needed
- related projects / notes

### 2. Thread
A lightweight grouping of related correspondence items.

Suggested properties:
- subject line or thread id
- participants
- latest activity
- unresolved status / next expected reply

### 3. Archive index
A way to list and query correspondence by:
- thread
- sender / recipient
- state
- theme
- related project

---

## Relationship to existing systems

### With notes
Correspondence should not collapse into general notes.
Its value comes from preserving address and exchange.

### With planner / registry
The correspondence system is not inventory or planning. It may link to projects, but it is not a PM surface.

### With future agent/role correspondence ideas
This system may eventually inform or host durable async role-to-role exchange, but v1 should not build agent mail infrastructure.

### With blog/foundry writing
Correspondence items may later become source material for essays, reflections, or notes — but should not be flattened immediately.

---

## Data model options

### Option A — one file per correspondence item
**Pros:**
- artifact-like
- diff-friendly
- easy to archive
- preserves letter-ness

**Cons:**
- requires a little directory discipline

### Option B — central JSON file
**Pros:**
- simplest CLI implementation
- compact

**Cons:**
- risks flattening correspondence into records rather than artifacts
- weaker archival feel

### Option C — markdown/frontmatter per item
**Pros:**
- strongest human-readable artifact feel
- easy to write/edit by hand
- natural for letters/notes

**Cons:**
- parser slightly more complex if kept stdlib-only

## Current recommendation
Start with:
### one file per correspondence item, likely markdown or JSON depending on implementation simplicity

Reason:
This project should feel like a drawer of letters, not a database table.

---

## Strong v1 boundary
The first useful version should stay small.

### v1 should probably support:
- storing correspondence items locally
- listing correspondence
- showing one item
- viewing by thread
- viewing items needing reply / unresolved
- templating a new item
- simple validation

### v1 does not need:
- notifications
- live send/receive integration
- encryption machinery
- email protocols
- message provider integrations
- contact sync
- search beyond simple filters

---

## Likely CLI surface for v1
A strong v1 likely supports:
- `list`
- `show <item>`
- `thread <thread-id>`
- `needs-reply`
- `template`
- `validate`

Optional if it stays small:
- `participants`
- `by-project`

---

## Implementation slices

## Slice 1 — correspondence item archive + unresolved/thread views
### Goal
Make durable exchange a real local archive surface.

### Scope
- item format
- CLI to list/show/thread/needs-reply/template/validate
- a few seeded sample items that prove the shape

### Why first
This is the smallest slice that tests whether correspondence deserves its own room.

### Acceptance criteria
- feels like preserved addressed writing, not generic note storage
- thread/unresolved views are useful
- artifact shape remains legible

---

## Slice 2 — project/theme linkage
### Goal
Relate correspondence items to projects/themes without flattening them.

### Scope
- lightweight project/theme references
- maybe simple filtered views

### Why second
This would help correspondence feed the broader archive while staying distinct.

---

## Slice 3 — deeper archive behavior
### Goal
Support richer archival use once the shape proves useful.

### Scope
- better thread navigation
- maybe archival states / return markers
- maybe a reply-due or revisit view

### Why third
Only after lived use proves the need.

---

## Seed set for v1
Do not seed with generic fake office mail.

Good seed shapes might include:
- one direct letter/note
- one reply pair / tiny thread
- one memo-like addressed note
- one unresolved item needing reply

The examples should prove:
- address
- thread
- unresolvedness
- and why this is not just notes with metadata

---

## Failure modes
Do not let this become:
- an instant messaging replacement
- inbox productivity sludge
- emotionally manipulative pseudo-intimacy infrastructure
- another dumping ground for miscellaneous writing
- generic records with no artifact feel

### Red flag
If correspondence items feel interchangeable with normal notes, the project has failed its purpose.

---

## Success criteria
The project is successful if:
- it preserves address and exchange as meaningful structure
- it feels distinct from notes and chat
- it creates a useful unresolved/threaded archive surface
- it stays text-first, local, and inspectable
- it opens new kinds of thought rather than just new storage

---

## Best first bounded runner slice
### Correspondence archive v1 — item archive + thread / needs-reply views

Bounded build:
- create project under `sera-foundry/projects/`
- choose an inspectable artifact-like data model
- implement:
  - `list`
  - `show`
  - `thread`
  - `needs-reply`
  - `template`
  - `validate`
- seed a few sample items/threads
- document philosophy and usage

That is enough to test whether the project feels alive.

---

## Why this should lead Phase A
Because it is:
- adjacent to the current experiment
- different enough to open new terrain
- rich in relation, continuity, and archive pressure
- and likely to teach us something about address, persistence, and asynchronous thought that the current machine room does not yet know
