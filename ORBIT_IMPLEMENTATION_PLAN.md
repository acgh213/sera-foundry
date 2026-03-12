# Orbit Map — Implementation Plan for Next 3 Slices

**Generated:** 2026-03-09T02:51 UTC  
**Status:** Planning only — no code implementation  
**Philosophy:** Real state only, terminal-first, inspectable, no fake telemetry

---

## Slice 1: Drift Detector

### Goal
Track how the conceptual topology changes over time by capturing snapshots and computing diffs.

### Why It Matters Now
- The system is actively growing (22 artifacts currently, increasing daily)
- Cassie and Sera are iterating on foundry structure — drift tracking would reveal what's stabilizing vs. what's churning
- Visualization of evolution is inherently interesting and validates the "living archive" concept
- Grounds future work in historical reality rather than speculation

### Exact Scope
**Add to orbit-map:**
- `--snapshot` flag: save current topology to timestamped JSON in `data/snapshots/YYYY-MM-DD-HHmmss.json`
- `--diff <snapshot1> <snapshot2>` command: compare two snapshots and output:
  - New/removed artifacts
  - Tag frequency deltas (which orbit centers strengthened/weakened)
  - Mode/kind distribution changes
  - Cluster membership changes (artifacts that shifted themes)
  
**Output format:**
- Terminal-first diff view (like git diff aesthetic: `+` for additions, `-` for removals, `~` for changes)
- Optional `--json` for machine-readable diff

**Data structure (snapshot):**
```json
{
  "timestamp": "2026-03-09T02:51:00Z",
  "artifact_count": 22,
  "tag_frequencies": { "foundry": 3, "collaboration": 2, ... },
  "kind_distribution": { "post": 7, "page": 6, ... },
  "mode_distribution": { "essay": 3, "project_log": 2, ... },
  "clusters": { "foundry": ["path1", "path2"], ... },
  "artifact_checksums": { "path": "title|tags_hash", ... }
}
```

### Out of Scope
- Automatic snapshot scheduling (cron) — keep it manual for now
- Embedding-based drift (no vectors, pure structural)
- Browser visualization — text diff only
- Predictive "where is this going" analysis

### Commands to Add
```bash
# Save snapshot
python projects/orbit-map/orbit.py --snapshot

# Compare two snapshots
python projects/orbit-map/orbit.py --diff data/snapshots/2026-03-08-120000.json data/snapshots/2026-03-09-025100.json

# Show all available snapshots
python projects/orbit-map/orbit.py --snapshots
```

### How It Stays Grounded in Real State
- Snapshots are read-only captures of actual index.json state at that moment
- Diffs compare only what changed between two real snapshots
- No interpolation, no prediction — just diff arithmetic
- Timestamps anchor everything to real time

### Suggested Model for Delegation
**Haiku** — straightforward data structure work, diffing logic is mechanical

### Likely Risks / Failure Modes
- **Snapshot sprawl:** If run too frequently, could accumulate many snapshots. Mitigation: manual only, user decides retention.
- **Noisy diffs:** Trivial changes (e.g., tag reordering) could trigger false positives. Mitigation: normalize tag lists before hashing.
- **Path changes:** If artifacts move, they'll appear as delete+add. Mitigation: document this as expected behavior (structural change is real).

---

## Slice 2: Artifact Health Report

### Goal
Detect structural weaknesses: orphaned artifacts, over-connected "bridge" artifacts, untagged/undertagged pieces, and stale (never-picked) artifacts.

### Why It Matters Now
- Current index has artifacts with `tags: null` (foundry projects/notes) — are these intentional or gaps?
- Some posts have 0-1 tags; others have 3-4. Is this healthy variation or signal loss?
- Resurfacer picks reveal which artifacts are actually surfacing vs. buried — health report would make this visible
- Grounds decisions about tagging/structure in actual metrics, not vibes

### Exact Scope
**New command:** `orbit.py --health`

**Health checks:**
1. **Orphans**: Artifacts with 0 tags
2. **Weak connections**: Artifacts with only 1 tag (questionable discoverability)
3. **Bridges**: Artifacts with 5+ tags (potential over-indexing)
4. **Stale artifacts**: Artifacts never picked by resurfacer (or not picked in last N days)
5. **Null metadata**: Artifacts with `null` tags/mode/published fields
6. **Kind/mode mismatches**: Artifacts where kind suggests a mode but mode is missing/generic

**Output format:**
```
🩺 ARTIFACT HEALTH REPORT — generated 2026-03-09T02:51

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  ORPHANS (0 tags)
  • pages/about.md (page/about)
  • pages/colophon.md (page/colophon)
  [5 total orphans — 22.7% of corpus]

⚡ WEAK CONNECTIONS (1 tag)
  • blog/drafts/2026-03-08-first-residue.md (fragment)
  [1 total weak — 4.5% of corpus]

🌉 BRIDGES (5+ tags)
  • blog/drafts/2026-03-09-the-pressure-of-artifacts.md (4 tags — close but not bridge)
  [0 true bridges]

💀 STALE (never picked by resurfacer)
  • pages/projects.md (unpublished — expected)
  • blog/drafts/2026-03-09-project-log-workbench-promotion-bridge.md (unpublished — expected)
  [2 stale, both unpublished]

🔍 NULL METADATA
  • 9 artifacts with null tags (all foundry_project/foundry_note kinds)
  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SUMMARY
  Total artifacts: 22
  Healthy (2+ tags, picked recently): 5
  Needs attention: 17
  
Suggested actions:
  - Tag foundry projects/notes or mark as infrastructure
  - Consider tagging pages (or accept them as tag-free navigation)
  - Review stale unpublished drafts for promotion/archival
```

**Machine-readable version:** `--health --json`

### Out of Scope
- Auto-fixing (no automatic tag addition)
- Recommendations for *which* tags to add (human decision)
- Integration with workbench review flow (separate concern)
- Historical health tracking (that's drift detector's job)

### Commands to Add
```bash
# Full health report
python projects/orbit-map/orbit.py --health

# Health with custom thresholds
python projects/orbit-map/orbit.py --health --min-tags 2 --stale-days 7

# JSON output
python projects/orbit-map/orbit.py --health --json
```

### How It Stays Grounded in Real State
- Reads only index.json and resurfacer-state.json (both real, existing files)
- Orphan/bridge detection is pure tag counting — no interpretation
- Stale detection uses actual pick timestamps from resurfacer
- Null metadata is exact match on JSON field values
- No synthetic "health scores" — just counts and thresholds

### Suggested Model for Delegation
**Haiku** — straightforward counting, filtering, threshold logic

### Likely Risks / Failure Modes
- **False positives:** Pages might intentionally have no tags (navigation structure, not content). Mitigation: make thresholds configurable, document expected orphans.
- **Stale definition drift:** "Never picked" vs "not picked in 30 days" are different. Mitigation: make stale-days configurable.
- **Noise from infrastructure artifacts:** Foundry notes/projects might not need tags. Mitigation: allow filtering by kind.

---

## Slice 3: Resurfacer History Visualization

### Goal
Make resurfacer pick patterns visible: what gets picked repeatedly, what gets picked once and buried, score decay over time, and pick clustering around specific artifacts.

### Why It Matters Now
- Resurfacer is running and accumulating pick history (13 picks currently)
- Pick scores reveal what the system finds "interesting" — visualizing this validates or challenges assumptions
- Pattern detection (e.g., postsmith picked 2x, workbench picked 2x — is this healthy rotation or fixation?)
- Informs resurfacer tuning (score decay rates, cooldown periods)
- Grounds future "surfaces" work in what actually gets resurfaced

### Exact Scope
**New command:** `orbit.py --resurface-history`

**Visualizations:**
1. **Pick timeline**: Chronological list of picks with scores
2. **Artifact pick frequency**: Which artifacts get picked most/least
3. **Score distribution**: Histogram of pick scores (are they clustering? spreading?)
4. **Recency analysis**: Time since last pick per artifact
5. **Pick clusters**: Detect runs of similar picks (e.g., 3 workbench picks in a row)

**Output format:**
```
🔄 RESURFACER HISTORY — 13 picks from 2026-03-09T01:28 to 01:52

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 PICK TIMELINE (most recent first)

  2026-03-09 01:52:08  foundry (note)                        score: 10.0
  2026-03-09 01:52:08  resurfacer (project)                  score: 10.0
  2026-03-09 01:52:08  Drift (page)                          score: 13.0
  2026-03-09 01:52:08  What Persistence Changes (post)       score: 13.0
  2026-03-09 01:52:08  First Residue (post)                  score: 16.0
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔁 PICK FREQUENCY

  postsmith (project)                     ████████ 3 picks
  workbench (project)                     ████████ 2 picks
  research-identity-continuity (note)     ████ 1 pick
  First Residue (post)                    ████ 1 pick
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SCORE DISTRIBUTION

  [56.0]  ████████████████████████████████ 7 picks (53.8%)
  [16.0]  ████ 1 pick (7.7%)
  [13.0]  ████████ 3 picks (23.1%)
  [10.0]  ████ 2 picks (15.4%)

  Score clustering detected: 7/13 picks at identical score (56.0)
  → Suggests homogeneous artifact set or flat scoring

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️  RECENCY ANALYSIS

  Picked within last hour:     5 artifacts
  Picked within last 24h:       13 artifacts
  Never picked:                 9 artifacts
  
  Longest dry spell:            foundry (note) — 10 minutes since last pick
  Most recently picked:         foundry (note) — just now

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Machine-readable:** `--resurface-history --json`

### Out of Scope
- Modifying resurfacer behavior based on history (pure read-only analysis)
- Embedding-based "why was this picked" explanations (scoring logic is in resurfacer)
- Browser-based timeline visualization (text-first)
- Predictive "what will be picked next" (no ML here)

### Commands to Add
```bash
# Full history analysis
python projects/orbit-map/orbit.py --resurface-history

# Filter to specific time window
python projects/orbit-map/orbit.py --resurface-history --since 2026-03-08

# Show only top N most-picked artifacts
python projects/orbit-map/orbit.py --resurface-history --top 5

# JSON output
python projects/orbit-map/orbit.py --resurface-history --json
```

### How It Stays Grounded in Real State
- Reads only resurfacer-state.json (real pick log with timestamps and scores)
- Pick frequency is exact counting from history
- Score distribution is histogram of actual scores (no bucketing unless explicit)
- Recency is timestamp math (current_time - last_pick_time)
- No synthetic "interestingness" metric — just what actually got picked

### Suggested Model for Delegation
**Haiku** — timestamp parsing, counting, histogram generation — all mechanical

### Likely Risks / Failure Modes
- **Short history bias:** With only 13 picks, patterns might be noise. Mitigation: document "N < 50 picks, patterns not statistically meaningful" in output.
- **Score clustering confusion:** If all scores are identical, frequency analysis becomes less meaningful. Mitigation: detect and warn about homogeneous scores.
- **Timestamp interpretation:** Picks in quick succession (batch run) vs. organic picks over days look different. Mitigation: show both pick count and time span.

---

## Implementation Order Recommendation

1. **Slice 2 (Health Report)** — Immediate value, reveals current state weaknesses, informs tagging/structure decisions
2. **Slice 3 (Resurfacer History)** — Validates resurfacer behavior, informs scoring tuning
3. **Slice 1 (Drift Detector)** — Long-term value, requires snapshots to accumulate before diffs are meaningful

## Cross-Slice Synergies

- Health report reveals orphans → drift detector shows if orphan count is increasing/decreasing over time
- Resurfacer history shows pick bias → health report shows if un-picked artifacts are also unhealthy (correlation analysis)
- Drift detector shows tag frequency changes → health report shows current tag health → together they reveal "is tagging improving?"

## Non-Slice Opportunities (Deferred)

These candidates didn't make the cut but are worth noting for future slices:

- **Static HTML report generator:** Export orbit map + health + history as a single-page HTML artifact (small-web aesthetic)
- **Cross-project relationship mapping:** For multi-project foundries, show which projects share conceptual gravity
- **Mode transition tracker:** Detect when artifacts move from draft → essay → field_note (lifecycle analysis)
- **Tag suggestion tool:** Based on cluster membership, suggest tags for orphans (but risky — prefer human tagging)

---

## Philosophy Alignment Check

✅ **Real state only:** All three slices read existing JSON files, no synthetic data  
✅ **Terminal-first:** Text output with optional JSON, no browser UIs required  
✅ **Inspectable:** Output shows data sources, thresholds, and counts explicitly  
✅ **No fake telemetry:** Metrics are counts/timestamps/diffs of actual artifacts, not proxies  
✅ **Bounded usefulness:** Each slice does one thing well, composes with others  
✅ **Severe/small-web aesthetic:** Clean text, emoji markers, diff-like output  

---

**End of plan. Ready for review and delegation.**
