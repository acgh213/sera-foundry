# drift-extractor Refinement Summary
**Date:** 2026-03-09  
**Commit:** 9ded2ed

## What Changed

### Core Improvements

1. **Context-aware extraction**
   - Added `extract_sentence_with_context()` that pulls in surrounding sentences for legibility
   - Paragraph-aware: tries to stay within natural paragraph boundaries to avoid mixing unrelated sections
   - Dynamic context window: uses less context for already-substantial sentences

2. **Markdown cleaning**
   - Added `clean_text()` that strips:
     - Headers (# ## ###)
     - List markers (- * + 1.)
     - Bold/italic markers (** * __ _)
     - Code backticks (`)
   - Normalizes whitespace to prevent run-on text

3. **Low-value fragment filtering**
   - Added `is_low_value_fragment()` that removes:
     - Too short (< 40 chars) or too long (> 350 chars)
     - Generic phrases ("I think", "Maybe", etc. standing alone)
     - Mostly markdown syntax
     - Structural list content (high ratio of short words)

4. **Substantiveness scoring**
   - Added `calculate_substantiveness_score()` that boosts:
     - Proper nouns (capitalized mid-sentence words)
     - Numbers and specific data
     - Domain terms (8+ char words)
     - Question words in actual questions
   - Penalizes filler words (very, really, actually, etc.)

5. **Better deduplication**
   - Improved `score_and_rank()` with:
     - Substring detection (one candidate inside another)
     - Fuzzy overlap matching (>75% word overlap)
     - Sequential comparison to catch near-duplicates

6. **Output formatting**
   - Improved `format_human_output()` with:
     - Word-wrapped text (76 chars per line)
     - No confusing truncation artifacts
     - Cleaner visual presentation

### Before vs After

**Before:**
- Candidates often included markdown headers: `#### Strong idea from the reading Gwern's...`
- List items mixed with text: `what am I working on? - what has already been written? - what should...`
- Short, context-free fragments: `Tone matters, but tone alone is cheap`
- Duplicates with slight variations

**After:**
- Clean text with no markdown artifacts
- Legible snippets with enough context to understand
- 1-3 focused candidates per file
- Substantive, meaningful edges

## Test Results

### notes/research-2026-03-09-morning.md
Extracted 3 strong candidates:
1. Question about pressure detection across archives (score: 1.30)
2. Tension about what gives continuity weight (score: 1.15)
3. Contrast between voice, artifacts, and workflow (score: 1.15)

### notes/workbench-brief.md
Extracted 2 focused questions:
1. Core workbench questions about current work (score: 0.95)
2. Layer separation questions (score: 0.95)

### notes/research-identity-continuity.md
Extracted 3 substantive candidates:
1. Identity from recurrence vs performance (score: 1.05)
2. Design direction for the system (score: 0.95)
3. Coherence without fake humanity (score: 0.93)

## Technical Details

**Files changed:** 1 (`projects/drift-extractor/drift-extractor.py`)  
**Lines changed:** +317 -55  
**New functions:** 4 (`clean_text`, `is_low_value_fragment`, `extract_sentence_with_context`, `calculate_substantiveness_score`)  
**Modified functions:** 5 (all extraction functions + `score_and_rank` + `format_human_output`)

## Acceptance Criteria Met

✅ Outputs 1-3 candidates that feel like actual unresolved edges  
✅ Candidate snippets include enough context to be legible  
✅ Obviously weak scraps are filtered out  
✅ Behavior demonstrated on real local artifacts  
✅ Text-first CLI shape preserved  
✅ Did not drift into summary mode  
✅ No heavy machinery added

## Caveats

1. **List artifact remnants**: Some candidates still contain traces of list structure (e.g., "The right direction is likely: local-first text-first...") - this is tolerable and maintains the original phrasing.

2. **Scoring tunability**: The substantiveness scoring uses hardcoded weights that could be tweaked based on real-world usage patterns.

3. **Context window trade-offs**: Current logic uses a 1-sentence window by default, 0 for already-long sentences. This is conservative to avoid bloat but could miss valuable adjacent context in some cases.

4. **Paragraph detection**: Simple double-newline splitting may not catch all logical section boundaries in heavily structured documents.

## Future Improvements (out of scope for this pass)

- Batch processing across multiple files
- Theme/pattern detection across candidates
- Integration with resurfacer for automatic extraction
- Configurable scoring weights via CLI flags
- Learning from promoted vs rejected candidates
