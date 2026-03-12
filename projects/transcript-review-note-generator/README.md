# Transcript Review Note Generator

A small local CLI that turns one plain-text transcript into one markdown review note.

This is a bounded v1 for the conversation-to-artifact bridge: it does **routing-style review**, not generic summarization and not automatic memory writing.

## What it does

Given one transcript file, it emits a markdown note with explicit sections for:

- decisions
- open threads
- candidate project ideas
- candidate memory promotions
- candidate authored artifacts
- residue

Each emitted item includes:

- a short statement
- evidence snippet and line pointer
- suggested destination layer where relevant
- confidence/strength marker

Residue is treated as first-class output instead of being silently discarded.

## Why this shape

This tool stays deliberately small and inspectable:

- local-only
- text-first
- terminal-first
- standard library only
- heuristic and auditable rather than hidden/overclaimed

It is meant to help a human review what might deserve promotion, follow-up, or preservation.
It does **not** claim that every candidate should be promoted.

## Usage

```bash
python3 projects/transcript-review-note-generator/review_transcript.py \
  projects/transcript-review-note-generator/samples/sample-transcript.txt
```

By default it writes next to the transcript with a `.review.md` suffix.

Custom output path:

```bash
python3 projects/transcript-review-note-generator/review_transcript.py \
  projects/transcript-review-note-generator/samples/sample-transcript.txt \
  --output projects/transcript-review-note-generator/samples/sample-output.md
```

Optional cap per section:

```bash
python3 projects/transcript-review-note-generator/review_transcript.py transcript.txt --max-items-per-section 5
```

## Input assumptions

V1 assumes:

- one transcript at a time
- UTF-8 plain text
- a line-oriented conversation or session log
- moderate transcript size

It works best when the transcript has visible turns or statements, but it does not require a strict format.

## Heuristic behavior

The classifier is intentionally simple:

- decisions are inferred from commitment/constraint/default language
- open threads from unresolved or question-shaped language
- project ideas from build/tool/workflow language
- memory promotions from durable preference/identity/collaboration language
- artifact candidates from note/spec/blog/doctrine/writing cues
- residue from lightweight chatter, logistics, or low-pressure lines

This means:

- it will miss some subtle cases
- it may sometimes over-surface ambiguous lines
- evidence is always shown so a human can disagree quickly

## Suggested destination layers

The tool uses the continuity layering model as labels only:

- Layer 2 — daily note / session residue
- Layer 3 — project note / line-of-work memory
- Layer 4 — long-term continuity memory
- Layer 5 — authored artifact
- Leave unpromoted / residue

These are recommendations, not actions.

## Sample files

- `samples/sample-transcript.txt` — tiny local example transcript
- `samples/sample-output.md` — generated output from the sample transcript

## Non-goals

This tool does **not**:

- auto-edit `MEMORY.md`
- write into project memory stores
- ingest live chat providers
- run a server or UI
- preserve everything
- replace authored notes
- produce a single flattened session summary as its main output

## Possible next refinements

If v1 proves useful, likely next steps would be:

- chunking nearby lines into better multi-line evidence spans
- slightly richer residue typing
- optional machine-readable sidecar output
- transcript-format adapters for specific local log shapes

Still local, still inspectable.
