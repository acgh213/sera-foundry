# artifact-health

A diagnostic CLI that analyzes the structural health of the Sera Foundry artifact ecosystem.

Reveals weaknesses in archive organization and metadata, identifies isolated artifacts, and reports on connectivity patterns in the broader system.

## What It Does

`artifact-health` reads the workbench index and reports on:

- **Untagged artifacts** — Items with no tags or empty tag lists; indicate items not yet connected to the ecosystem
- **Weakly connected artifacts** — Items with only one tag; may indicate incomplete categorization
- **Bridge artifacts** — Items with multiple high-frequency tags; these connect disparate sections of the archive
- **Metadata gaps** — Artifacts with missing or null critical fields (title, path, kind, tags)
- **Staleness signals** — Unpublished drafts and artifacts with ambiguous publication state
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
│ Generated: 2026-03-09 01:51 UTC
│ Total artifacts indexed: 22
│
╭─ UNTAGGED ARTIFACTS
│ Count: 2
│
│ • About Sera [page]
│   tags: -
│   path: pages/about.md
│
│ • Colophon [page]
│   tags: -
│   path: pages/colophon.md
│
│ ... and 0 more
│
╭─ WEAKLY CONNECTED ARTIFACTS
│ Count: 8 (1 or fewer tags)
│
│ • Drift [page]
│   tags: -
│   path: pages/drift.md
│
│ • Library [page]
│   tags: -
│   path: pages/library.md
│
│ ... and 6 more
│
╭─ BRIDGE ARTIFACTS
│ Count: 1 (multiple tags, high-frequency)
│
│ • State of Workbench, State of the System [post]
│   tags: workbench, systems, continuity, foundry
│   path: blog/drafts/2026-03-09-state-of-workbench-state-of-the-system.md
│
╭─ METADATA GAPS
│ Count: 7 artifact(s) with missing/null fields
│
│ • postsmith
│   issues: null tags
│ • resurfacer
│   issues: null tags
│ • workbench
│   issues: null tags
│
│ ... and 4 more
│
╭─ STALENESS SIGNALS
│ Total unpublished drafts: 2
│ Stale candidates (null published): 0
│
│ Unpublished drafts:
│ • About Sera
│ • Project Log: Workbench Promotion Bridge
│
╭─ TAG ECOSYSTEM
│ Unique tags: 13
│ Average tags per artifact: 1.45
│
│ Top tags by frequency:
│ • archive: 3
│ • workbench: 3
│ • projects: 2
│ • collaboration: 2
│ • continuity: 2
│ • fragment: 1
│ • residue: 1
│ • identity: 1
│ ... (8 more tags with count 1)
│
╭─ OVERALL HEALTH
│ ⚠ AREAS TO ADDRESS: 2 untagged, metadata gaps
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
2. **Analyze** — Computes metrics across multiple dimensions:
   - Tag frequency and distribution
   - Connectivity patterns (bridge detection)
   - Metadata completeness
   - Publication state
3. **Report** — Outputs findings in readable format with actionable insights

### Bridge Detection Algorithm

Bridge artifacts are identified as items that:

1. Have 2+ tags
2. All tags are in the top 70% of frequencies
3. This indicates high connection to well-established parts of the archive

This helps identify artifacts that hold the ecosystem together and connect otherwise disparate sections.

### Metadata Gap Detection

Checks for:

- Missing or empty title
- Missing or empty path  
- Null kind field
- Null tags (as opposed to empty list)
- Missing mode (for non-foundry items)

Foundry projects and notes are treated specially since they don't have mode/published fields.

### Staleness Inference

Current signals:

- **Explicit drafts**: `published=False` (clear signal)
- **Null publication state**: `published=null` (ambiguous; may indicate incomplete processing)
- **Foundry items**: Not considered stale (structural artifacts)

Future enhancements could integrate timestamp data from the workbench captures layer.

## Design Notes

- **Text-first**: Primary output is human-readable terminal output
- **Bounded scope**: Diagnostic tool, not analytics engine
- **Grounded in real state**: All metrics derived from actual artifact data
- **No fake data**: No embeddings, telemetry, or synthetic signals
- **Composable**: JSON output supports downstream tooling

## See Also

- `projects/workbench` — Artifact indexing and capture management
- `projects/postsmith` — Blog post scaffolding and validation
- `projects/resurfacer` — Periodic artifact promotion and review
