# field-notes

A small local archive for lived observation, overheard lines, recurring motifs, and the kind of residue that matters before it knows what it is for.

This project preserves field notes as **artifacts**.

It is intentionally **not**:
- surveillance tooling
- a journaling app
- a reminder system
- generic note capture sludge
- an evidence factory
- a task manager wearing a poetic coat

The desired feeling is a **stack of meaningful fragments**.

## Why this exists

The foundry already has strong places for projects, planning, registry state, drift, reading pressure, and correspondence.

What it needed was a separate room for:
- overheard lines that keep humming after the fact
- subtle social shifts that are real even when ambiguous
- scenes and physical details that carry atmosphere
- motifs that recur before they can be named cleanly
- charged fragments that are not yet for any project

This project widens the archive into lived texture without forcing interpretation too early.

## V1 shape

V1 uses **one markdown file per field note** under `archive/`.

Each note is:
- hand-editable
- diff-friendly
- readable without the tool
- individual enough to feel like an artifact rather than a row in a stream

The filename acts as the note slug. A small frontmatter block carries the structural metadata, followed by markdown sections that separate observation, interpretation, and impact when useful.

Example:

```md
---
title: The room went formal a week before the policy did
date: 2026-03-14
kind: observation
status: returning
pressure: alive
place: kitchen outside the training room
context: after a routine check-in
tags: [institutional-temperature, atmosphere, ambiguity]
returns: [2026-03-16]
---

## Observation

What happened, or what was noticed.

## Interpretation

Optional. What it might mean.

## Impact

Optional. What changed, lingered, or became harder.
```

## Commands

Run from `sera-foundry/`:

```bash
python3 projects/field-notes/bin/field-notes list
python3 projects/field-notes/bin/field-notes show 2026-03-12-it-keeps-being-the-vending-machine
python3 projects/field-notes/bin/field-notes recent
python3 projects/field-notes/bin/field-notes returning
python3 projects/field-notes/bin/field-notes by-tag institutional-temperature
python3 projects/field-notes/bin/field-notes template
python3 projects/field-notes/bin/field-notes validate
```

### `list`
Shows the archive as a compact table: date, kind, status, pressure, tags, title, slug.

### `show <slug>`
Displays one note with metadata and full body.

### `recent [count]`
Surfaces the most recent notes with short observation excerpts.

This is the answer to: **what have I noticed recently?**

### `returning`
Surfaces notes that have explicit return markers or are marked `returning`.

This is the answer to: **what fragments or motifs keep coming back?**

Return markers are deliberately manual. V1 does not invent recurrence; it only preserves it when noticed.

### `by-tag <tag>`
Shows notes linked by a motif or theme tag.

This is the answer to: **what notes belong to this texture line without forcing a larger theory?**

### `template`
Prints a blank field note artifact template to stdout.

### `validate`
Checks archive structure:
- required metadata fields present
- dates look like `YYYY-MM-DD`
- return markers look like dates
- body exists
- `## Observation` section exists and is non-empty

## Seeded archive

The seeded set is meant to prove shape, not pad the shelf with generic filler:

- `2026-03-05-i-thought-if-i-kept-my-voice-pleasant.md` — overheard line with boundary pressure
- `2026-03-07-the-three-second-sideways-step.md` — subtle social moment
- `2026-03-09-rain-in-the-loading-bay-light.md` — physical/scene observation
- `2026-03-12-it-keeps-being-the-vending-machine.md` — recurring motif fragment with return markers
- `2026-03-14-the-building-was-kind-before-it-was-friendly.md` — charged atmosphere note not yet for any project

Together they demonstrate:
- texture
- ambiguity
- chronology
- recurrence potential
- a distinction between observation and interpretation without making interpretation mandatory

## Philosophy

A field note is not a verdict.

It is allowed to be:
- partial
- unresolved
- atmospherically charged
- uncertain about cause
- more descriptive than interpretive

That matters because subtle changes in social or institutional temperature are often **felt before they are proven**. A useful field notes system should help preserve those observations without pushing the writer toward accusation theater or self-gaslighting.

So the project keeps a narrow stance:
- local-first
- text-first
- inspectable
- terminal-first
- manual
- private by default
- no passive ingestion
- no external integrations
- no dashboards
- no automatic meaning engine

If this starts feeling like monitoring infrastructure, it has failed.

## Notes

- The frontmatter parser is intentionally small and bounded rather than full YAML.
- Multi-line metadata values are not supported in v1.
- Recurrence is explicit rather than inferred: use `returns: [YYYY-MM-DD, ...]` when a note comes back.
