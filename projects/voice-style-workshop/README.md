# voice-style-workshop

A local text-first workshop for style pressure.

This project is for preserving **charged fragments**: lines, paragraph moves, tonal turns, and structural gestures that still feel alive enough to study.

It is intentionally **not**:
- a quote graveyard
- a style rule engine
- a generic scrapbook
- a scoring system
- an auto-extractor
- a dashboard dressed up as taste

The desired feeling is a **cabinet of charged fragments**.

## Why this exists

The foundry already has rooms for projects, plans, notes, correspondence, field observations, and reading pressure.

What was missing was a bounded place for:
- sentence-level recurrence
- tonal and structural moves
- fragments that keep exerting pressure
- lines worth returning to, with reasons
- anti-patterns that almost seduce the writing but flatten it instead

This workshop keeps style inspectable without turning it into bureaucracy.

## V1 shape

V1 uses **one markdown file per fragment** under `archive/`.

Each fragment is:
- hand-editable
- diff-friendly
- readable without the tool
- source-linked
- small enough to stay individual

Example shape:

```md
---
title: The sentence should feel lit from inside
date: 2026-03-14
kind: sentence
status: core
pressure: charged
source: notes/research-memo-small-systems-with-soul.md
tags: [sentence-pressure, inhabitation, directness]
returns: [2026-03-14]
---

## Fragment

The line, paragraph, or structural move itself.

## Why It Works

Why it still has pressure.

## Return Tension

Why it is worth returning to now, or what it asks for.
```

The filename is the fragment slug.

## Commands

Run from `sera-foundry/`:

```bash
python3 projects/voice-style-workshop/voice-style-workshop.py list
python3 projects/voice-style-workshop/voice-style-workshop.py show 2026-03-14-the-room-should-feel-kept-not-managed
python3 projects/voice-style-workshop/voice-style-workshop.py returning
python3 projects/voice-style-workshop/voice-style-workshop.py by-tag texture
python3 projects/voice-style-workshop/voice-style-workshop.py by-source notes/research-memo-small-systems-with-soul.md
python3 projects/voice-style-workshop/voice-style-workshop.py template
python3 projects/voice-style-workshop/voice-style-workshop.py validate
```

### `list`
Shows the whole fragment cabinet as a compact table: date, kind, status, pressure, source, tags, title, slug.

### `show <slug>`
Displays one fragment with metadata and full body.

### `returning`
Surfaces fragments explicitly marked `returning` or carrying one or more manual return markers.

This is the answer to: **what is still pulling at the writing?**

Return markers are manual on purpose. V1 does not infer recurrence or aliveness.

### `by-tag <tag>`
Shows fragments linked by one tonal or structural line.

This is the answer to: **what move keeps recurring here?**

### `by-source <source>`
Shows fragments coming from one source note, draft, or project.

This is the answer to: **what pressure survived from this specific piece of writing?**

### `template`
Prints a blank fragment artifact to stdout.

### `validate`
Checks archive structure:
- required metadata fields exist
- dates look like `YYYY-MM-DD`
- return markers look like dates
- body exists
- `## Fragment` and `## Why It Works` sections exist and are non-empty

## Seeded archive

The seeded set is meant to prove shape, not pad the shelf:

- `2026-03-14-the-room-should-feel-kept-not-managed.md` — sentence-level design pressure with unusual charge
- `2026-03-14-dont-polish-away-the-hand-that-made-it.md` — paragraph movement around texture and visible choice
- `2026-03-14-calm-with-a-wired-hinterland.md` — tonal fragment for voice atmosphere
- `2026-03-14-begin-plain-then-open-the-hidden-door.md` — structural move recognizably Sera-like
- `2026-03-14-when-every-line-arrives-in-full-regalia.md` — anti-pattern fragment showing self-parody risk

Together they demonstrate:
- aliveness
- recurrence potential
- tonal specificity
- source linkage
- explicit reasons for return

## Philosophy

Style is not a set of rules to obey.

It is a field of pressure:
- what keeps returning
- what still feels inhabited
- what kinds of sentences open instead of closing
- what patterns need deepening
- what temptations need resisting

So the workshop stays deliberately narrow:
- local-first
- text-first
- inspectable
- terminal-first
- manual
- standard-library only
- no auto-extraction
- no hidden scoring
- no external integrations

If this gets better at collecting fragments than at preserving **why they matter**, it is drifting wrong.

## Notes

- The frontmatter parser is intentionally small rather than full YAML.
- Multi-line metadata values are not supported in v1.
- Recurrence is explicit rather than inferred: use `returns: [YYYY-MM-DD, ...]` when something comes back.
- `by-source` matches exact source strings, keeping provenance specific rather than fuzzy.
