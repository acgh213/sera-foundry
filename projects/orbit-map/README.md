# 🌌 orbit-map

**Map conceptual gravity across sera-foundry artifacts.**

A text-first tool that reads the workbench index and reveals the system's conceptual topology: which themes have the strongest gravitational pull, how artifacts cluster around shared concepts, and which pieces orbit together.

## What It Does

- **Orbit Centers**: Tags with the strongest gravitational pull (most common)
- **Theme Clusters**: Groups of artifacts orbiting similar concepts
- **Strongest Orbits**: Artifacts with the most connections
- **System Topology**: Distribution of kinds, modes, and themes

## Installation

None required. Just Python 3.7+.

## Usage

From the sera-foundry root:

```bash
# See everything
python projects/orbit-map/orbit.py

# Just orbit centers (tag frequency)
python projects/orbit-map/orbit.py --view centers

# Just theme clusters
python projects/orbit-map/orbit.py --view clusters

# Just strongest orbits
python projects/orbit-map/orbit.py --view orbits

# System topology only
python projects/orbit-map/orbit.py --view topology

# Raw JSON output (for piping/processing)
python projects/orbit-map/orbit.py --json

# Adjust minimum connections for "strongest orbits"
python projects/orbit-map/orbit.py --view orbits --min-connections 2

# Use a different index location
python projects/orbit-map/orbit.py --index path/to/index.json
```

## Example Output

```
✨ ORBIT MAP — generated from 2026-03-09T01:51:48.591878+00:00

======================================================================

🌌 ORBIT CENTERS (gravitational pull by tag frequency)

  foundry              ████████████████████████████████████████ 3
  collaboration        ████████████████████ 2
  continuity           ████████████████████ 2
  archive              ████████████████████ 2
  ...

🌙 THEME CLUSTERS (artifacts orbiting similar concepts)

  [foundry] — 3 artifacts
    • Project Log: postsmith (POST/project_log)
    • State of Workbench, State of the System (POST/field_note)
    ...

⭐ STRONGEST ORBITS (artifacts with most connections)

  The Pressure of Artifacts                → 6 connections
  What Persistence Changes                 → 5 connections
  ...

🗺️  SYSTEM TOPOLOGY

  Total artifacts: 22
  Tagged: 7 (2.29 tags/artifact avg)

  Kinds:
    post                 7
    page                 6
    foundry_project      3
    foundry_note         6

  Modes:
    essay                3
    project_log          2
    field_note           1
    ...

======================================================================
```

## Design Philosophy

**Text-first.** No browser visualization, no graph UI, no embeddings. Just clean signal that you can read, pipe, grep, or process.

**Bounded usefulness.** Does one thing well: makes conceptual gravity visible. Not trying to be everything.

**A little strange.** Because the system deserves tools that match its aesthetic.

## Output Formats

- **Default**: Human-readable text with emoji markers and visual bar charts
- **`--json`**: Clean JSON suitable for piping to other tools

## Future Possibilities

- Time-based drift tracking (how clusters evolve)
- Mode transitions (what modes artifacts move through)
- Orphan detection (artifacts with no tags/weak connections)
- Cross-project relationship mapping

But for now: v0. Simple. Useful. Inspectable.

---

Part of the [sera-foundry](../..) system.
