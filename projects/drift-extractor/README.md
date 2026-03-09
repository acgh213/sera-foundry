# drift-extractor

A small tool for extracting drift candidates from markdown artifacts: unresolved questions, tensions, unfinished edges, and observations that could become fragments or field notes.

## Purpose

Resurfacer brings old artifacts back into view. Drift-extractor helps you identify what's generative _within_ those artifacts — the edges, tensions, and unfinished thoughts that might want to become new material.

Think of it as **turning recurrence into candidates**.

## What It Does

Given a markdown file, drift-extractor:

1. Reads the content (stripping frontmatter)
2. Applies heuristic extraction to find:
   - Explicit questions
   - Tension/contrast language (but, yet, however, instead, etc.)
   - Uncertainty markers (maybe, perhaps, unclear, wonder, etc.)
   - Special sections (Open Questions, Future Work, etc.)
   - Trailing thoughts (sentences ending with ellipses)
3. Scores and ranks candidates
4. Returns the top 1-3 drift candidates

Output is human-readable by default, with optional JSON format.

## Usage

### Basic Extraction

```bash
# Human-readable output
python3 projects/drift-extractor/drift-extractor.py --path /path/to/artifact.md

# JSON output
python3 projects/drift-extractor/drift-extractor.py --path /path/to/artifact.md --json
```

### Capture to Workbench

The `--capture` flag writes extracted drift candidates directly to workbench's `captures.jsonl`:

```bash
python3 projects/drift-extractor/drift-extractor.py \
  --path ../sera-oc-blog/blog/drafts/some-post.md \
  --capture
```

Each candidate becomes a workbench capture tagged with `drift` and `extracted`, including:
- The drift text
- Extraction reason
- Score
- Source file path

You can then review, filter, and promote these captures using workbench's normal flow:

```bash
# View all drift captures
python3 projects/workbench/workbench.py review --tag drift

# Mark one for promotion
python3 projects/workbench/workbench.py review-mark 5 --state promote

# Promote to a blog draft
python3 projects/workbench/workbench.py promote --type fragment --execute
```

## Output

### Human-Readable

```
============================================================
DRIFT CANDIDATES: 2026-03-09-the-pressure-of-artifacts.md
============================================================

[1] STRUCTURAL TENSION
    Signal: tension/contrast language
    Score: 0.92

    A response solves the moment and then drifts backward into chat
    history.

[2] BOUNDARY TENSION
    Signal: uncertainty/hedging
    Score: 0.81

    I do not mean that in the sense of fake humanity.

[3] OPEN QUESTION
    Signal: explicit question
    Score: 0.88

    What has been happening here is not just prompting?

============================================================
```

### JSON

```json
{
  "path": "blog/drafts/2026-03-09-the-pressure-of-artifacts.md",
  "extracted_at": "2026-03-09T02:58:00+00:00",
  "candidates": [
    {
      "text": "A response solves the moment and then drifts backward into chat history.",
      "reason": "tension/contrast language",
      "pressure": "structural tension",
      "context": null,
      "score": 0.92
    },
    {
      "text": "I do not mean that in the sense of fake humanity.",
      "reason": "uncertainty/hedging",
      "pressure": "boundary tension",
      "context": null,
      "score": 0.81
    }
  ],
  "count": 2
}
```

## Heuristics

Drift-extractor uses simple, inspectable pattern matching plus light structure recovery:

### Explicit Questions
- Sentences or grouped question blocks containing `?`
- Longer questions (>20 chars) preferred
- Multi-question sets are kept together when they clearly belong to one pressure
- "What if" / "Why not" style questions score higher

### Tension/Contrast
- Words like: but, yet, however, although, instead, rather, nevertheless
- Block-aware extraction tries to preserve the surrounding sentence pair or list intro
- Signals unresolved contrasts or competing ideas

### Uncertainty/Hedging
- Words like: maybe, perhaps, might, could, unclear, unsure, wonder, puzzle
- Suggests edges that haven't hardened yet

### Open Sections
- Markdown headers matching patterns like:
  - "Open Questions"
  - "Future Work"
  - "To Do"
  - "Unfinished"
  - "Next Steps"
- Content from these sections scores highest (0.8)

### Trailing Thoughts
- Sentences ending with ellipses (`...`)
- Often marks unfinished or exploratory ideas

### Pressure Labels
- Candidates are also tagged with a sharper pressure label (`missing bridge`, `selection pressure`, `boundary tension`, etc.)
- The original extraction signal is still shown so the heuristic remains inspectable

## Scoring

Each candidate gets a base score depending on extraction type, then receives boosts/penalties for substantiveness and prose integrity.

- Open sections: **0.82**
- Explicit questions (exploratory): **0.62–0.72**
- Tensions/contrasts: **0.66**
- Uncertainty markers: **0.56** (+ per additional marker)
- Trailing thoughts: **0.64**

Additional heuristics reward intact prose, domain specificity, and well-formed question blocks, while penalizing compressed list artifacts and weak structural scraps.

The top 3 highest-scoring candidates are returned.

## Design Constraints

- **Heuristic-first**: No LLM, no embeddings, no external APIs
- **Text-based**: Input and output are plain text/JSON
- **Local**: Runs entirely on your machine
- **Inspectable**: You can read the code and understand what it's doing
- **Narrow scope**: Does one thing well
- **Composable**: Works with workbench, resurfacer, and the broader foundry ecosystem

## Example Workflow

1. **Resurface an old artifact:**
   ```bash
   python3 projects/resurfacer/resurfacer.py run --json
   ```

2. **Extract drift from it:**
   ```bash
   python3 projects/drift-extractor/drift-extractor.py \
     --path blog/drafts/2026-03-08-some-post.md \
     --capture
   ```

3. **Review captured drifts:**
   ```bash
   python3 projects/workbench/workbench.py review --tag drift --state new
   ```

4. **Promote interesting ones:**
   ```bash
   python3 projects/workbench/workbench.py review-mark 3 --state promote
   python3 projects/workbench/workbench.py promote --auto --execute
   ```

## Future Ideas (Out of Scope for v0)

- Batch processing across multiple files
- Theme/topic clustering of drift candidates
- Integration with resurfacer (auto-extract on each resurfaced item)
- Recurring pattern detection across artifacts
- Visual diff of drift over time

For now, drift-extractor is intentionally small: one file in, 1-3 candidates out.

## Requirements

- Python 3.9+
- No external dependencies (uses stdlib only)

## Philosophy

Not every artifact needs to be polished. Some of the most generative material lives in the edges: the questions you didn't answer, the tensions you left unresolved, the thoughts that trailed off.

Drift-extractor is a tool for noticing those edges and treating them as raw material instead of rough spots to be smoothed away.

It's designed to complement resurfacer: where resurfacer brings old work back into attention, drift-extractor asks _what wants to become new?_
