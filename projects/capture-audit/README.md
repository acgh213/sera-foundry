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
- heuristic residue classes
- oldest unreviewed captures
- suspiciously short captures
- exact normalized duplicate groups
- a compact default-surfacing section

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

### Residue classes

The tool applies a lightweight presentation-only classification that is **not** stored back into Workbench state.

Current output distinguishes:

- `meaningful extracted pressure`
- `weak but meaningful planning residue`
- `weak low-value residue`
- `other residue`

Current heuristics are intentionally coarse:

- extracted captures with enough length or visible pressure/tension language stay in `meaningful extracted pressure`
- short extracted fragments fall into `weak low-value residue`
- manual notes with obvious planning/design language fall into `weak but meaningful planning residue`
- very short or especially generic fragments fall into `weak low-value residue`

This is meant to improve default surfacing, not to introduce a new review-state system.

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
