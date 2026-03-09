# artifact-health

A diagnostic CLI that analyzes the structural health of the Sera Foundry artifact ecosystem.

Reveals weaknesses in archive organization and metadata, identifies isolated artifacts, and reports on connectivity patterns in the broader system. Distinguishes between structural conventions and real issues to provide clear, actionable diagnostics.

## What It Does

`artifact-health` reads the workbench index and reports on:

- **Untagged content** — Posts/essays without tags; indicates disconnection from ecosystem. Pages and foundry items excluded (conventionally untagged)
- **Weakly connected content** — Posts/essays with only one tag; may indicate incomplete categorization. Pages and foundry items excluded
- **Bridge artifacts** — Content with 3+ high-frequency tags; these connect disparate sections of the archive and indicate core ecosystem connectors
- **Metadata gaps** — Artifacts with missing or null critical fields. Foundry items excluded (null tags by design)
- **Content state** — Publication status of posts and pages; unpublished drafts tracked separately
- **Tag ecosystem** — Frequency distribution of tags and average connectivity

## Usage

Basic report (text-first, terminal-readable):

```bash
python3 projects/artifact-health/artifact-health.py
```

JSON output for parsing:

```bash
python3 projects/artifact-health/artifact-health.py --format json
```

## Output

### Text Report

A human-readable diagnostic with box-drawing characters and structured sections:

```
╭─ ARTIFACT HEALTH REPORT
│ Generated: 2026-03-09 12:32 UTC
│ Total artifacts indexed: 22

╭─ UNTAGGED CONTENT (posts, etc.)
│ Count: 0
│ ✓ All content artifacts are tagged

╭─ WEAKLY CONNECTED CONTENT (single tag)
│ Count: 0
│ ✓ All content artifacts have multi-tag connection

╭─ BRIDGE ARTIFACTS (ecosystem connectors)
│ Count: 3 (3+ tags, high-frequency)
│ Insight: These artifacts connect disparate sections of the archive
│
│ • About Sera [post]
│   tags: about, identity, archive
│   path: blog/drafts/2026-03-08-about-sera.md
│ • First Residue [post]
│   tags: fragment, residue, archive
│   path: blog/drafts/2026-03-08-first-residue.md
│ • Project Log: postsmith [post]
│   tags: projects, foundry, tooling
│   path: blog/drafts/2026-03-08-postsmith-project-log.md

╭─ METADATA GAPS
│ Count: 0 artifact(s) with missing/null fields
│ ✓ All artifacts have complete core metadata

╭─ CONTENT STATE
│ Published content: 10/13
│ Unpublished drafts: 3
│ Stale candidates (null state): 0
│
│ Unpublished drafts:
│ • About Sera [post]
│ • Project Log: Workbench Promotion Bridge [post]
│ • Projects [page]

╭─ TAG ECOSYSTEM
│ Unique tags: 18
│ Average tags per artifact: 1.05
│
│ Top tags by frequency:
│ • archive: 2
│ • foundry: 2
│ • collaboration: 2
│ • workbench: 2
│ • continuity: 2
│ ... (13 more tags with count 1)

╭─ OVERALL ASSESSMENT
│ ✓ HEALTHY
│ • All content is tagged and connected
│ • No critical metadata gaps
│ • Archive ecosystem is well-formed
│ • 10/13 content published
│
│ Note: foundry_project and foundry_note (structural artifacts)
│       are excluded from tagging and publication assessments.
╰─
```

### JSON Report

Structured data for downstream processing:

```json
{
  "timestamp": "2026-03-09T01:51:48.591878+00:00",
  "total_artifacts": 22,
  "untagged": {
    "count": 2,
    "examples": [ ... ]
  },
  "weakly_connected": {
    "count": 8,
    "threshold": "1 or fewer tags",
    "examples": [ ... ]
  },
  "bridge_artifacts": {
    "count": 1,
    "examples": [ ... ]
  },
  "metadata_gaps": {
    "count": 7,
    "issues": [ ... ]
  },
  "staleness": {
    "unpublished_drafts": 2,
    "stale_candidates": 0,
    "examples": [ ... ]
  },
  "tag_ecosystem": {
    "unique_tags": 13,
    "avg_tags_per_artifact": 1.45,
    "top_tags": { ... }
  }
}
```

## Dependencies

- Python 3.8+
- Standard library only (pathlib, json, collections, datetime)

## How It Works

1. **Load Index** — Reads `projects/workbench/data/index.json` (built by workbench CLI)
2. **Classify Artifacts** — Distinguishes artifact types:
   - **Structural**: foundry_project, foundry_note (not subject to content tagging rules)
   - **Conventional**: pages (conventionally untagged by design)
   - **Content**: posts, essays, notes (should be tagged and connected)
3. **Analyze** — Computes metrics across multiple dimensions:
   - Tag frequency and distribution (for content artifacts only)
   - Connectivity patterns (bridge detection for content)
   - Metadata completeness
   - Publication state
4. **Report** — Outputs findings in readable format with actionable insights

### Untagged/Weakly Connected Detection

Focuses exclusively on **content artifacts** (posts, essays, etc.):

- **Untagged**: Content with 0 tags → disconnected from ecosystem
- **Weakly connected**: Content with exactly 1 tag → incomplete categorization

Excludes:
- Foundry items (have null tags by convention)
- Pages (have empty tags by convention)

This prevents false positives and noise from structural artifacts.

### Bridge Detection Algorithm

Bridge artifacts are identified as content items that:

1. Have 3+ tags (meaningful multi-dimensional connection)
2. All tags are in the top 70% of frequencies
3. This indicates high connection to established ecosystem sections

These artifacts are valuable connectors and indicate strong ecosystem integration.

### Metadata Gap Detection

Checks for:

- Missing or empty title
- Missing or empty path  
- Null kind field
- Null tags (for non-foundry items; foundry items excluded)
- Missing mode (for content items; structural items excluded)

Foundry items are exempt from tag and mode checks (by design).

### Content State Assessment

Tracks publication status of content (posts and pages):

- Published vs. unpublished counts
- Identifies unpublished drafts
- Flags high unpublished ratios (>33%) in overall health

## Design Notes

- **Text-first**: Primary output is human-readable terminal output with clear section labels
- **Bounded scope**: Diagnostic tool, not analytics engine
- **Convention-aware**: Distinguishes intentional patterns (foundry items, pages) from real issues
- **Low noise**: Reduces false positives by excluding structural/conventional artifacts from tagging assessments
- **Actionable signals**: Improvements focus on content connectivity, not on items that are untagged by design
- **Grounded in real state**: All metrics derived from actual artifact data
- **No fake data**: No embeddings, telemetry, or synthetic signals
- **Composable**: JSON output supports downstream tooling
- **Inspectable**: Simple heuristics (tag counts, publication state) remain visible and understandable

## See Also

- `projects/workbench` — Artifact indexing and capture management
- `projects/postsmith` — Blog post scaffolding and validation
- `projects/resurfacer` — Periodic artifact promotion and review
