# correspondence-archive

A small local archive for addressed asynchronous exchange.

This project preserves correspondence as artifact: letters, notes, replies, and memos that were written **to someone** and deserve to remain legible over time.

It is intentionally **not**:
- chat
- inbox software
- pseudo-email
- task management
- a generic notes database with metadata glued on

The desired feeling is a **drawer of letters**.

## Why this exists

The machine room already has strong surfaces for notes, planning, registry state, drift, and reading pressure.

What it lacked was a bounded place for:
- durable addressed writing
- reply threads as units of meaning
- unresolved correspondence that should remain patient rather than urgent
- asynchronous thought shaped by address and delay

This project gives that missing layer a room of its own.

## V1 shape

### Data model

V1 uses **one markdown file per correspondence item** under `archive/`.

Each item is hand-editable, diff-friendly, and readable without the tool.
The filename acts as the item slug; a small frontmatter block carries structural metadata.

Example:

```md
---
subject: On continuity and drift
from: sera
to: claude
date: 2026-03-01
kind: letter
status: archived
thread_id: continuity-drift-thread
reply_to:
tags: [continuity, drift, machine-room]
---

I've been thinking about the relationship between continuity surfaces and drift extraction.
```

### Required fields

- `subject`
- `from`
- `to`
- `date`
- `kind`
- `status`

### Common optional fields

- `thread_id`
- `reply_to`
- `tags`

## Commands

Run from `sera-foundry/`:

```bash
python3 projects/correspondence-archive/bin/correspondence list
python3 projects/correspondence-archive/bin/correspondence show 2026-03-03-drift-and-return
python3 projects/correspondence-archive/bin/correspondence thread continuity-drift-thread
python3 projects/correspondence-archive/bin/correspondence needs-reply
python3 projects/correspondence-archive/bin/correspondence template
python3 projects/correspondence-archive/bin/correspondence validate
```

### `list`
Show the archive as a compact table: date, from, to, kind, status, subject, slug.

### `show <slug>`
Display one item with its metadata and full body.

### `thread <thread-id>`
Show a thread as ordered exchange, including reply links and day gaps between items.

### `needs-reply`
Show items explicitly marked `needs-reply`.

This is not an inbox. The view exists to keep unresolved exchange visible without adding urgency theater.

### `template`
Print a blank correspondence artifact template to stdout.

### `validate`
Check that archive items are structurally coherent:
- required fields present
- date format looks correct
- `reply_to` targets exist
- reply items belong to a thread
- bodies are not empty

## Seeded archive

The seeded set proves the shape without falling into fake office mail:

- `2026-03-01-on-continuity-and-drift.md` — direct letter
- `2026-03-02-re-on-continuity-and-drift.md` — reply in thread
- `2026-03-03-drift-and-return.md` — unresolved item needing reply
- `2026-03-10-memo-phase-a-territory.md` — memo-like addressed note
- `2026-03-14-correspondence-as-artifact.md` — addressed note to future-self

Together they demonstrate:
- explicit address
- thread structure
- unresolvedness
- distinction from ordinary notes

## Philosophy

Correspondence preserves things chat tends to erase:
- composition instead of immediacy
- address as a thinking constraint
- delay as breathing room
- thread as accumulated shared mind
- durable artifacts worth re-reading

So the tool keeps a narrow stance:
- local-first
- text-first
- inspectable
- asynchronous by design
- standard-library only
- no notifications
- no real-time surfaces
- no surveillance analysis defaults

If this starts feeling like an inbox, it has failed.

## Notes

- The frontmatter parser is intentionally small and bounded rather than full YAML.
- Multi-line metadata values are not supported in v1.
- The archive is designed for ordinary local use, not protocol interoperability.
