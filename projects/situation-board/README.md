# situation-board v1

A bounded local tool that reads manual note files and generates a compact markdown board.

## Intent

This tool helps you maintain situational awareness by consolidating manually-declared items from three note files into a single readable board. It is:

- **Local-only**: No network, no external services
- **Text-first**: Plain markdown in, plain markdown out
- **Inspectable**: All inputs and outputs are human-readable files
- **Modest**: Does not infer, surveil, or decide for you

## What it is NOT

- Not a dashboard UI
- Not a notification system
- Not a passive ingestion pipeline
- Not a broad inference engine
- Questions are not automatically projects

## Input format

The tool reads three manual note files from `notes/situation/`:

1. **inbox.md** — Current attention items
2. **follow-ups.md** — Items for follow-up
3. **hold.md** — Items on hold or not-now

Each file should contain simple markdown bullet lists. Non-empty bullet items become entries on the board.

### Optional lightweight conventions

- Prefix items with `!` for emphasis (e.g., `- ! Critical bug fix`)
- Add `due: YYYY-MM-DD` for date markers (e.g., `- Review PR due: 2026-03-15`)

The tool is forgiving and does not require these markers.

## Output format

The tool generates `notes/situation-board.md` with these sections:

- **Current attention** (from inbox.md)
- **Follow-up** (from follow-ups.md)
- **Hold / Not now** (from hold.md)

The board includes a header note: "This board reflects declared inputs only."

## Usage

Run the tool directly; bundled default inputs are resolved relative to the script location, so it works even if your current directory is somewhere else:

```bash
python situation-board.py
```

### Optional flags

- `--inbox PATH` — Path to inbox file (default: `notes/situation/inbox.md`)
- `--follow-ups PATH` — Path to follow-ups file (default: `notes/situation/follow-ups.md`)
- `--hold PATH` — Path to hold file (default: `notes/situation/hold.md`)
- `--output PATH` — Path to output board (default: `notes/situation-board.md`)

### Example with custom paths

```bash
python situation-board.py --inbox my-inbox.md --output my-board.md
```

## Design boundaries

- **Manual input only**: You control what goes in
- **Stable structure**: Same inputs produce the same sections and item ordering; only the generated timestamp changes
- **No classification**: The tool respects your declared categorization
- **Current-legibility over cleverness**: Simple, readable code
- **Standard library only**: No external dependencies

## Sample workflow

1. Edit `notes/situation/inbox.md` to add current attention items
2. Edit `notes/situation/follow-ups.md` for follow-up items
3. Edit `notes/situation/hold.md` for items on hold
4. Run `python situation-board.py`
5. View the generated `notes/situation-board.md`

## Files

- `README.md` — This file
- `situation-board.py` — The tool script
- `notes/situation/inbox.md` — Current attention input
- `notes/situation/follow-ups.md` — Follow-up input
- `notes/situation/hold.md` — Hold input
- `notes/situation-board.md` — Generated board (output)

## Caveats

- The tool does not validate date formats or markers
- Empty sections are shown with "(none)" on the board
- The tool overwrites the output file on each run
- Missing input files are treated as empty sections
