# foundry-registry

A small local registry for the machine room itself.

It keeps a hand-editable record of the current foundry projects so you can answer, from the terminal:

- what exists here
- what each project does
- what state it is in
- what it depends on
- what should happen next
- where the pressure is

This is intentionally not a management platform.
It is a small text-first index with a tiny CLI.

## Shape

- `registry.json` — the hand-maintained registry data
- `foundry-registry.py` — a stdlib CLI for reporting, showing, and validating the registry

The registry is meant to be edited by hand.
The CLI is there to make review easier, not to hide the data.
Refresh it after meaningful implementation, review, or doctrine shifts so the machine-room view stays current.

## Usage

From `sera-foundry/`:

```bash
# Full machine-room summary
python3 projects/foundry-registry/foundry-registry.py report

# Compact list view
python3 projects/foundry-registry/foundry-registry.py list

# Show one project in detail
python3 projects/foundry-registry/foundry-registry.py show workbench

# Validate required fields and directory coverage
python3 projects/foundry-registry/foundry-registry.py validate

# Raw JSON report derived from the registry
python3 projects/foundry-registry/foundry-registry.py report --format json
```

If you omit the command, `report` is used.

## Editing the registry

Edit `registry.json` directly.
Each project entry must include:

- `name`
- `path`
- `what_it_does`
- `status`
- `dependencies`
- `notes`
- `next_actions`
- `pressure`

Optional but useful fields:

- `last_reviewed`
- `signals`

## Status and pressure

These are deliberately simple and human-chosen.
There is no hidden scoring engine.

### Suggested status vocabulary

- `active` — currently under real attention
- `stable` — useful and settled enough for now
- `watching` — accepted, but worth revisiting later
- `exploratory` — interesting, but not currently central

### Pressure vocabulary

- `high` — active pull; likely wants near-term attention
- `medium` — real but not urgent
- `low` — can sit quietly unless a new trigger appears

## Validation

`validate` checks two things:

1. every registry entry has the required fields
2. every direct child of `projects/` has a registry entry

This keeps the registry honest without turning it into infrastructure theater.
