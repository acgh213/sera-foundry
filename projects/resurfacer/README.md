# resurfacer

A small CLI for surfacing older artifacts from the archive and foundry.

Resurfacer looks across blog posts, pages, and foundry projects, preferring materials that are aging and not recently revisited. It uses simple heuristics to avoid random picks and instead favors artifacts that align with current ecosystem themes.

## Purpose

Over time, a blog and foundry accumulate layers of material. Some of it gets attention; much of it recedes into the background. Resurfacer brings overlooked pieces back into view on a regular basis — not through SEO magic or algorithmic ranking, but through intentional, inspectable scoring.

Think of it as a form of **active curation through temporal depth**.

## How It Works

### Scoring

Each artifact gets a score based on:

1. **Age** (primary): Older artifacts score higher via score banding:
   - 7-30 days: 10-20 points
   - 31-90 days: 20-35 points
   - 91+ days: 35-50 points (capped)
   - Artifacts younger than 7 days are excluded entirely
2. **Themes** (secondary): Artifacts matching current ecosystem themes get bonus points. Current themes include: `continuity`, `residue`, `artifacts`, `workbench`, `postsmith`, `projects`, `drift`, `memory`, `archive`, `persistence`, `foundry`.
3. **Active cluster avoidance**: Themes associated with current active work (`workbench`, `postsmith`, `foundry`, `projects`) receive reduced weight to avoid over-resurfacing from the immediate work context.
4. **Diversity**: Artifact kinds (post, page, foundry_project, foundry_note) that have been picked multiple times recently receive penalties to encourage variety across categories.
5. **History**: Resurfacer keeps a small state file (`data/resurfacer-state.json`) tracking the last 10 picks, ensuring the same artifact doesn't get surfaced repeatedly within 2 months.

### Selection

On each `run`, Resurfacer:

1. Loads the workbench-generated index (`projects/workbench/data/index.json`)
2. Scores all eligible artifacts
3. Picks the highest-scoring candidate
4. Outputs its metadata and reasoning
5. Appends the pick to the state file (unless `--dry-run`)

### Data

- **Input**: Workbench index (automatically generated via `workbench.py index`)
- **State**: Tiny JSON file at `projects/resurfacer/data/resurfacer-state.json` (one object per pick)

## Usage

### Basic

```bash
# Surface one artifact, print human-readable output
python3 projects/resurfacer/resurfacer.py run

# Same, but output as JSON
python3 projects/resurfacer/resurfacer.py run --json

# Dry run: show what would be picked without updating state
python3 projects/resurfacer/resurfacer.py run --dry-run
```

### With Custom Paths

```bash
# Specify blog and foundry repos explicitly
python3 projects/resurfacer/resurfacer.py run \
  --blog-repo /path/to/sera-oc-blog \
  --foundry-repo /path/to/sera-foundry
```

### With Filters

```bash
# Only surface blog posts
python3 projects/resurfacer/resurfacer.py run --kind post

# Only surface artifacts matching a specific theme
python3 projects/resurfacer/resurfacer.py run --theme memory

# Combine filters
python3 projects/resurfacer/resurfacer.py run --kind page --theme drift
```

## Output

### Human-Readable

```
============================================================
RESURFACED: What Persistence Changes
============================================================
Kind:    post
Mode:    essay
Path:    blog/drafts/2026-03-08-what-persistence-changes.md
Age:     1 days

Why this was chosen:
  • matches themes: continuity, memory, persistence
  • not picked recently

Why now: relates to continuity and memory infrastructure; 
archive piece from 1 days ago
Score:   3.5
============================================================
```

### JSON

```json
{
  "title": "What Persistence Changes",
  "kind": "post",
  "path": "blog/drafts/2026-03-08-what-persistence-changes.md",
  "mode": "essay",
  "age_days": 1,
  "theme_matches": ["continuity", "memory", "persistence"],
  "reasons": [
    "matches themes: continuity, memory, persistence",
    "not picked recently"
  ],
  "why_now": "relates to continuity and memory infrastructure; archive piece from 1 days ago",
  "score": 3.5
}
```

## State File

The state file tracks recent picks to prevent repetition:

```json
{
  "picks": [
    {
      "path": "blog/drafts/2026-03-08-what-persistence-changes.md",
      "title": "What Persistence Changes",
      "picked_at": "2026-03-09T01:45:00+00:00",
      "score": 3.5
    }
  ],
  "generated_at": "2026-03-09T01:45:00+00:00"
}
```

## Setup

Resurfacer requires:

- The workbench index to exist (`projects/workbench/data/index.json`)
- Python 3.9+
- PyYAML (same as workbench)

If the index doesn't exist yet:

```bash
python3 projects/workbench/workbench.py index --blog-repo ../sera-oc-blog --foundry-repo .
```

## Design Notes

- **Text-first**: All output is inspectable, human-readable JSON or plain text.
- **Local-first**: No external APIs, embeddings, or ranking services.
- **Simple**: Heuristics are intentionally transparent and easy to adjust.
- **Stateful**: The pick history is durable and visible.
- **No UI, no cron**: This is a CLI you call when you want. Scheduling is left to the user (e.g., cron, systemd timer, or manual invocation).

## Themes

Current themes capture the ecosystem's preoccupations:

- **continuity**: sessions, memory, persistence, state
- **residue**: fragments, signals, raw notes, leftovers
- **artifacts**: concrete outputs, tools, projects
- **workbench**: the workbench tool itself and its ecosystem
- **postsmith**: blogging scaffolding
- **projects**: foundry projects in general
- **drift**: the drift page and concept
- **memory**: memory systems, persistence
- **archive**: archive structure, indexing
- **persistence**: persistence infrastructure
- **foundry**: foundry projects and concepts

Edit the `CURRENT_THEMES` set in `resurfacer.py` to adjust what you want to surface.

## Future Ideas

- Threshold-based picking (e.g., only pick if score > X)
- Multiple picks per run (e.g., `--count 5`)
- Theme-specific resurfacing
- Integration with blog generation (surface → blog post → promotion)
- Time-decay curves (e.g., prefer quadratic decay instead of linear)

For v0, these are all deferred. The focus is on a small, working, inspectable tool.
