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
# Capture
python3 projects/workbench/workbench.py capture --text "Need to write about archive structure" --layer internal

# Review
python3 projects/workbench/workbench.py review
python3 projects/workbench/workbench.py review --layer internal --tag flow
python3 projects/workbench/workbench.py review --state new --recent 10 --with-suggest
python3 projects/workbench/workbench.py review --text continuity --state promote
python3 projects/workbench/workbench.py review-show 2 --with-suggest
python3 projects/workbench/workbench.py review-mark 2 --state reviewed
python3 projects/workbench/workbench.py review-mark 7 --state promote
python3 projects/workbench/workbench.py digest
python3 projects/workbench/workbench.py digest --limit 5 --recent 8

# Index & status
python3 projects/workbench/workbench.py index --blog-repo ../sera-oc-blog --foundry-repo .
python3 projects/workbench/workbench.py status --blog-repo ../sera-oc-blog --foundry-repo .

# Suggest & query
python3 projects/workbench/workbench.py suggest --text "Built a validator for blog frontmatter and integrated it into the workflow"
python3 projects/workbench/workbench.py query --text postsmith

# Promotion (legacy direct mode)
python3 projects/workbench/workbench.py promote --text "Built a small CLI for scaffolding blog drafts." --title "Project Log: postsmith" --auto

# Promotion queue (recommended)
python3 projects/workbench/workbench.py promote-add 2 --auto
python3 projects/workbench/workbench.py promote-list              # pending items only
python3 projects/workbench/workbench.py promote-list --all        # all statuses
python3 projects/workbench/workbench.py promote-show 1
python3 projects/workbench/workbench.py promote-run 1 --execute --blog-repo ../sera-oc-blog
python3 projects/workbench/workbench.py promote-update 1 --title "New Title"
python3 projects/workbench/workbench.py promote-cancel 1
```

## Review flow

Captured notes live in `projects/workbench/data/captures.jsonl`.

Review state lives separately in `projects/workbench/data/review-state.json`, keyed by capture id. Missing state is treated as `new`, so Workbench can stay stateful without rewriting capture history.

Use `review` to inspect notes in a compact terminal format with stable line-based IDs and lightweight triage state.

- `--layer internal|draft|public` filters by continuity layer
- `--tag TAG` filters by exact tag match
- `--text QUERY` does a simple case-insensitive substring match against note text and tags
- `--state new|reviewed|promote|defer|dormant` filters by review state
- `--recent N` keeps the latest `N` matching notes before display
- `--limit N` caps displayed results (default: `20`)
- `--with-suggest` adds the current Workbench suggestion beside each result

`review` now shows each capture's current state and prints a small count summary for the displayed result set.

Use `review-show ID` when you want the full text and metadata for one captured note.

Use `review-mark ID --state ...` to triage a note without editing the note itself.

Use `digest` when you want the smallest operational summary of review reality: what is still new, what has been marked for promotion, what is deferred or dormant, and what recently moved in review/promotion state. The digest is terminal-first and only reflects local capture, review, and promotion queue files.

Available review states:

- `new`
- `reviewed`
- `promote`
- `defer`
- `dormant`

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

## Promotion queue

The promotion queue provides a first-class pipeline for managing captures that are ready to become artifacts.

Queue items are stored in `projects/workbench/data/promotion-queue.json` and retain linkage to their original captures while tracking promotion state through to execution.

### Queue commands

```bash
# Add a capture to the promotion queue (with auto-suggest)
python3 projects/workbench/workbench.py promote-add 2 --auto

# Add with explicit type and title
python3 projects/workbench/workbench.py promote-add 5 --type field_note --title "Field Note: Archive Structure"

# List queue items (shows pending by default)
python3 projects/workbench/workbench.py promote-list

# List all items regardless of status
python3 projects/workbench/workbench.py promote-list --all

# Filter by specific status
python3 projects/workbench/workbench.py promote-list --status executed
python3 projects/workbench/workbench.py promote-list --status failed

# Show details for a queue item
python3 projects/workbench/workbench.py promote-show 1

# Execute a queue item (dry-run by default)
python3 projects/workbench/workbench.py promote-run 1

# Execute for real
python3 projects/workbench/workbench.py promote-run 1 --execute --blog-repo ../sera-oc-blog

# Update a pending queue item
python3 projects/workbench/workbench.py promote-update 1 --title "New Title" --type project_log

# Cancel a pending queue item
python3 projects/workbench/workbench.py promote-cancel 1
```

### Queue item lifecycle

Items move through these states:

1. **pending** - newly added, ready to be executed
2. **executed** - successfully created a draft in the blog repo
3. **failed** - execution failed (check error in queue state file)
4. **cancelled** - manually cancelled via `promote-cancel`

**Rules:**
- Only `pending` items can be updated or cancelled
- Once executed, failed, or cancelled, items become immutable records
- `promote-list` shows only `pending` items by default (use `--all` to see everything)
- Failed and cancelled items remain visible in the queue for debugging and history
- To hide completed/failed items from the default view, they must stay in non-pending status

**Queue hygiene:**
- Use `promote-list` (default) to see active work
- Use `promote-list --all` to review history and diagnose failures
- Use `promote-list --status failed` to focus on errors
- Use `promote-cancel` to mark items you no longer want to execute
- The queue retains history by design - completed items don't clutter the default view

### Design notes

- Original captures remain immutable
- Queue items include snapshot of capture text, tags, and metadata at promotion time
- Each queue item tracks its `created_path` when successfully executed
- Dry-run mode shows the exact `postsmith` command before execution
- Failed executions preserve error messages in the queue state

## Design constraints

- text-first
- local-first
- inspectable
- small scope
- public/private boundaries remain visible
