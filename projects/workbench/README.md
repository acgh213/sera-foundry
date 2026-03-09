# workbench

A small continuity tool for turning residue into artifacts.

Workbench is meant to sit between rough notes and public outputs. It helps collect notes, index the existing archive/machine room, and suggest what kinds of artifacts might emerge from raw material.

## v0 goals

- capture rough notes
- review captured notes before promotion
- index the blog + foundry
- summarize continuity state
- suggest whether a note looks like a fragment, field note, or project log
- query what already exists in the archive
- promote residue into a real scaffolded draft via `postsmith`

## Commands

```bash
python3 projects/workbench/workbench.py capture --text "Need to write about archive structure" --layer internal
python3 projects/workbench/workbench.py review
python3 projects/workbench/workbench.py review --layer internal --tag flow
python3 projects/workbench/workbench.py review --text continuity --recent 10 --with-suggest
python3 projects/workbench/workbench.py review-show 2 --with-suggest
python3 projects/workbench/workbench.py index --blog-repo ../sera-oc-blog --foundry-repo .
python3 projects/workbench/workbench.py status --blog-repo ../sera-oc-blog --foundry-repo .
python3 projects/workbench/workbench.py suggest --text "Built a validator for blog frontmatter and integrated it into the workflow"
python3 projects/workbench/workbench.py query --text postsmith
python3 projects/workbench/workbench.py promote --text "Built a small CLI for scaffolding blog drafts." --title "Project Log: postsmith" --auto
```

## Review flow

Captured notes live in `projects/workbench/data/captures.jsonl`.

Use `review` to inspect them in a compact terminal format with stable line-based IDs.

- `--layer internal|draft|public` filters by continuity layer
- `--tag TAG` filters by exact tag match
- `--text QUERY` does a simple case-insensitive substring match against note text and tags
- `--recent N` keeps the latest `N` matching notes before display
- `--limit N` caps displayed results (default: `20`)
- `--with-suggest` adds the current Workbench suggestion beside each result

Use `review-show ID` when you want the full text and metadata for one captured note.

## Layers

Captured notes can currently be marked as:

- `internal`
- `draft`
- `public`

This is the first step toward keeping rough residue, public-facing material, and in-between states legible.

## Suggestion output

`suggest` now returns:

- a primary suggested type
- a secondary candidate
- rough confidence
- score breakdown
- brief reasons for the classification

The goal is not perfect intelligence. The goal is legible, useful sorting.

The heuristic is intentionally simple, but it now weighs brevity against implementation language and active-work observation instead of assuming every short note is a fragment.

## Promotion

`promote` builds a `postsmith scaffold-post` handoff.

- by default it is **dry-run only** and prints the exact command it would run
- with `--execute`, it actually creates the draft in the blog repo
- use `--type` for explicit mode selection or `--auto` to use Workbench's suggestion result

## Design constraints

- text-first
- local-first
- inspectable
- small scope
- public/private boundaries remain visible
