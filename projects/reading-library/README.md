# reading-library

A small local library for machine-room reading pressure.

This project is not a completion tracker.
It does not care how many pages were consumed.
It does not try to become Goodreads for the foundry.

Its job is narrower and stranger:

- hold real reading items in a hand-editable form
- preserve why they matter now
- show what is active
- show what is returning
- keep links to themes and projects visible

The point is not to store titles.
The point is to keep intellectual pressure legible.

## Shape

- `data/items/*.json` — one inspectable JSON file per reading item
- `reading-library.py` — stdlib CLI for listing, showing, validating, and templating items

One-file-per-item was chosen because it keeps the library artifact-like and diff-friendly without adding parser complexity.
Markdown/frontmatter would have had a nice feel, but JSON keeps v1 tighter while staying hand-editable.

## Data model

Each item is a JSON object with fields such as:

- `slug`
- `title`
- `creator`
- `type`
- `status`
- `pressure`
- `last_touched`
- `source`
- `why_it_matters`
- `why_now`
- `themes`
- `related_projects`
- `active_questions`
- `signals`
- `return_markers`
- `notes`

The model is intentionally small.
There are no page counts, finish percentages, streaks, scores, or recommendation features.

## Commands

From `sera-foundry/`:

```bash
# Compact list of all reading items
python3 projects/reading-library/reading-library.py list

# Show one item in detail
python3 projects/reading-library/reading-library.py show the-human-use-of-human-beings

# Surface current reading pressure
python3 projects/reading-library/reading-library.py active

# Surface returning sources and why they came back
python3 projects/reading-library/reading-library.py returning

# Validate item files and schema shape
python3 projects/reading-library/reading-library.py validate

# Print a starter JSON template to stdout
python3 projects/reading-library/reading-library.py template

# Print a template with a few fields prefilled
python3 projects/reading-library/reading-library.py template --slug new-item --title "A New Item"
```

If you omit the command, `active` is used.

## How `active` works

`active` is deliberately not the same as `status=reading`.

An item appears on the active surface if either:

- its status is `reading` or `returning`
- or its declared `pressure` is `high`

That keeps the surface oriented toward what still pulls at current work, not only what is literally open on the desk.

## How `returning` works

An item appears on the returning surface if either:

- its status is `returning`
- or it has one or more `return_markers`

A return marker records:

- `date`
- `trigger`
- `why_now`

That is enough for v1 to preserve recurrence without inventing a larger state system.

## Seed set

The seeded items are tied to live machine-room themes rather than toy examples:

- continuity
- correspondence
- recurrence
- human-AI relationship boundaries
- small systems with soul

They are there to prove the pressure surface on real lines of thought.

## Design limits

This project intentionally does **not** do any of the following in v1:

- quote extraction
- EPUB/PDF ingestion
- annotation sync
- completion tracking
- graph UI or dashboard
- recommendation engine

If the tool ever gets better at storing reading than at showing why something still matters, it is drifting in the wrong direction.
