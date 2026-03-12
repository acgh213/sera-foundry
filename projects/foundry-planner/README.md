# foundry-planner

A local planning surface for the machine room.

`foundry-registry` answers **what exists**.
`foundry-planner` answers **what are we trying to do next**.

This is intentionally not generic PM software.
It is a text-first, terminal-first companion for keeping current goals, next steps, blockers, requests, testing state, and future-project pressure legible.

## Shape

- `plan.json` — the hand-editable planning data
- `foundry-planner.py` — stdlib CLI for summaries, detail views, focused reports, templates, and validation

The data file is meant to be edited by hand.
The CLI makes the machine-room state easy to inspect without hiding the source of truth.

## Data model

There is one central JSON file with one object per project.
Each project can represent either:

- a real current project directory (`path` set)
- or a future/planned project (`path` empty)

Each project tracks:

- `status` — active / watching / planned / stable / parked
- `lane` — workflow / weird / diagnostic / coordination / support
- `horizon` — now / next / later
- `summary`
- `current_goal`
- `next_steps`
- `blocked`
- `requests`
- `testing`
- `context`
- `updated_at`

This is deliberately small.
It is enough to answer:

- what projects are active?
- what is each one trying to do now?
- what is blocked?
- what requests or parity targets are hanging off it?
- what still needs testing?
- what future work is waiting in the wings?

## Usage

From `sera-foundry/`:

```bash
# Full planning board
python3 projects/foundry-planner/foundry-planner.py board

# Compact list view
python3 projects/foundry-planner/foundry-planner.py list

# Filter to active workflow projects
python3 projects/foundry-planner/foundry-planner.py list --status active --lane workflow

# Show one project in detail
python3 projects/foundry-planner/foundry-planner.py show workbench

# Show next actionable steps
python3 projects/foundry-planner/foundry-planner.py next --limit 8

# Show blockers
python3 projects/foundry-planner/foundry-planner.py blocked

# Show requests / parity targets
python3 projects/foundry-planner/foundry-planner.py requests
python3 projects/foundry-planner/foundry-planner.py requests --type parity

# Show testing pressure
python3 projects/foundry-planner/foundry-planner.py testing
python3 projects/foundry-planner/foundry-planner.py testing --state needs-live-use

# Validate shape + current project-directory coverage
python3 projects/foundry-planner/foundry-planner.py validate

# Print a JSON template for a future project entry
python3 projects/foundry-planner/foundry-planner.py template recurrence-ledger "Recurrence Ledger"
```

If you omit the command, `board` is used.

## Editing the plan

Edit `plan.json` directly.

### For current projects

Set `path` to the matching project directory, for example:

```json
"path": "projects/workbench"
```

Validation will fail if a real directory is missing from the plan.

### For future/planned projects

Use an empty `path`:

```json
"path": ""
```

That lets the planner carry future work without pretending a project already exists on disk.

## Suggested maintenance rhythm

Refresh the plan after:

- a meaningful implementation slice lands
- a review pass changes what should happen next
- a project becomes blocked or unblocked
- a testing need becomes clearer
- a future idea either earns a real directory or gets parked harder

Keep the registry and planner coherent, but separate:

- registry = what exists
- planner = what is next / blocked / waiting / being tested

## Design boundaries

- local-only
- inspectable backing data
- no hidden state
- no dashboard UI
- no automatic prioritization engine
- no external integrations

## Caveats

- This is a hand-maintained planning surface, not an authoritative scheduler
- Validation checks structure and directory coverage, not whether your priorities are wise
- A central JSON file is easy to diff and edit, but still wants occasional pruning if it grows too much
