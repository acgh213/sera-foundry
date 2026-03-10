# drift-review

A small terminal-first review surface for extracted drift captures.

This tool lives **downstream** of `drift-extractor`.
It does not change extraction logic or add new persistent state.
It reads what already exists in Workbench capture/review data and makes drift easier to inspect.

## What it helps with

- list extracted drift captures
- group them by source artifact
- show existing pressure / reason / score metadata
- distinguish stronger extracted pressure from weaker extraction residue
- inspect a single capture alongside its source artifact excerpt
- keep compact default views focused on more alive-looking drift without deleting weak provenance

## Classification shape

`drift-review` uses a small presentation-only heuristic.
It does **not** write the result back into Workbench.

Current classes:

- `strong extracted pressure`
- `possible extracted pressure`
- `weak extraction residue`

The classification is based on existing local evidence only:

- extraction score
- pressure label
- extraction reason
- text length
- visible pressure vocabulary
- a few explicit low-value residue phrases

This is meant to improve review legibility, not to become a hidden scoring machine.

## Usage

From `sera-foundry/`:

```bash
# Default compact review (grouped by source, weak residue hidden by default)
python3 projects/drift-review/drift-review.py

# Show everything, including weak extraction residue
python3 projects/drift-review/drift-review.py --all

# Only inspect weak residue
python3 projects/drift-review/drift-review.py --weak-only

# Flat list instead of grouped-by-source output
python3 projects/drift-review/drift-review.py --ungrouped

# Focus on one source artifact
python3 projects/drift-review/drift-review.py --source pressure-of-artifacts

# Source summary view
python3 projects/drift-review/drift-review.py sources --all

# Inspect one capture with source excerpt
python3 projects/drift-review/drift-review.py show 4
```

## Default behavior

By default, `drift-review`:

- reads `projects/workbench/data/captures.jsonl`
- reads `projects/workbench/data/review-state.json` if present
- selects only drift/extracted captures
- hides `weak extraction residue` from the main list view
- keeps a count of hidden weak items visible in the header

Use `--all` when you want the full historical/provenance view.

## Why it exists

This is the bounded review-layer step from the drift integration plan:

- keep `drift-extractor` narrow
- improve downstream review of extracted material
- separate meaningful extracted pressure from weaker residue at the workflow level

That gives drift somewhere more legible to land without turning extraction into a giant meaning engine.

## Constraints

- local-only
- read-only
- text-first
- terminal-first
- standard library only
- inspectable heuristics only
