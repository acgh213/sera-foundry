# capture-audit

A small read-only terminal audit for Workbench captures.

It reads:

- `projects/workbench/data/captures.jsonl`
- optionally `projects/workbench/data/review-state.json`

And surfaces:

- total captures
- counts by layer
- counts by source family and exact source
- extracted vs manual capture split (heuristic)
- oldest unreviewed captures
- suspiciously short captures
- exact normalized duplicate groups
- a compact `worth inspecting` section

## Usage

From `sera-foundry/`:

```bash
python3 projects/capture-audit/capture-audit.py
```

Optional tuning:

```bash
python3 projects/capture-audit/capture-audit.py \
  --oldest-limit 8 \
  --short-limit 8 \
  --short-chars 45 \
  --short-words 7
```

## Heuristics

The tool is intentionally small and inspectable.

### Extracted vs manual

A capture is treated as `extracted` if any of these are true:

- tag includes `extracted`
- source family ends with `extractor`
- metadata includes extraction-style fields like `reason` or `source_file`

Otherwise, if it has a source, it is treated as `manual`.

### Suspiciously short

Flagged when either threshold matches:

- non-space character count is at or below `--short-chars`
- word count is at or below `--short-words`

This is a review hint, not a deletion suggestion.

### Duplicate-ish

Currently this only catches **exact normalized duplicates**:

- lowercase
- punctuation stripped
- whitespace collapsed

That keeps the result legible and avoids fuzzy scoring theater.

## Constraints

- read-only
- local-only
- standard library only
- terminal-first
