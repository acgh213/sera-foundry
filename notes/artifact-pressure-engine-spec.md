# Artifact Pressure Engine — Specification

## Status
Spec only. Do not implement yet.

## Purpose
Artifact Pressure Engine is a read-only analysis tool for detecting **cross-archive pressure**: places where the current system is visibly trying to produce a missing artifact, clarification, bridge, or structural repair.

It should not guess at mood, destiny, or vibes. It should point to **specific pressure patterns**, show the **evidence chain** that produced each one, and suggest a bounded next move.

Pressure, in this spec, means:

> repeated structural or thematic signals across the archive/workbench that indicate an unresolved need for synthesis, clarification, public explanation, or workflow adjustment.

This is not the same as popularity, recency, or sentiment. A pressure event is only valid when it is supported by multiple observable traces.

---

## What this is not

### Not resurfacer
**resurfacer** asks:
- what older artifact deserves renewed attention right now?

Its unit of analysis is primarily **one existing artifact at a time**, scored by age, theme overlap, freshness penalties, and pick history.

Artifact Pressure Engine asks:
- what unresolved pattern across the whole archive is exerting force?
- what missing bridge or clarification is being implied by multiple traces?

Its unit of analysis is **a pressure pattern**, not a single artifact selection.

### Not drift-extractor
**drift-extractor** asks:
- inside this one markdown artifact, what unresolved edge or generative fragment is present?

Its unit of analysis is **intra-artifact tension**.

Artifact Pressure Engine asks:
- across artifacts, captures, queue state, and recurrence logs, what keeps appearing without being adequately integrated?

Its unit of analysis is **cross-artifact structural pressure**.

### Quick distinction table
| Tool | Primary scope | Typical output | Core question |
|---|---|---|---|
| resurfacer | one existing artifact | a resurfaced item | what should be revisited? |
| drift-extractor | one artifact body | 1–3 drift candidates | what unfinished edge is inside this text? |
| artifact-pressure-engine | whole archive/workbench state | pressure records with evidence chains | what is trying to exist but is not yet properly formed? |

---

## Design constraints
1. **Read-only.** It must not modify captures, queue state, or artifacts.
2. **Inspectable.** Every output must cite concrete evidence records.
3. **Cross-source.** A pressure claim should usually require at least 2 source classes.
4. **Bounded.** It should recommend a next artifact/tool/page, not a vague life direction.
5. **Non-mystical.** Strange is fine; unverifiable theater is not.
6. **No hidden embeddings required.** v1 should be implementable with local text/metadata heuristics.

---

## Evidence sources

The engine should ingest evidence in layers. Higher-trust sources are direct system state; lower-trust sources are derived summaries.

### Tier 1 — direct state sources
These should be the canonical basis for pressure detection.

#### 1. Workbench index
**Path:** `projects/workbench/data/index.json`

Provides:
- artifact inventory
- kinds (`post`, `page`, `foundry_project`, `foundry_note`)
- modes
- tags
- published state
- path distribution

Use for:
- theme recurrence across artifacts
- absent public pages for dense themes
- duplicate or split representations
- concentration around modes/tags
- publishability gaps

#### 2. Workbench captures
**Path:** `projects/workbench/data/captures.jsonl`

Provides:
- raw residue
- extracted drift candidates
- capture tags
- source lineage
- timestamped internal/public note pressure

Use for:
- repeated unresolved ideas in residue
- residue that names a topic not yet stabilized as an artifact
- pressure rising from extracted fragments or repeated manual captures

#### 3. Review state
**Path:** `projects/workbench/data/review-state.json`

Provides:
- what has or has not been reviewed
- whether captures are accumulating without human/agent triage

Use for:
- backpressure detection
- evidence that generative material exists but is not being processed

#### 4. Promotion queue
**Path:** `projects/workbench/data/promotion-queue.json`

Provides:
- intended artifact titles/types/tags
- queue outcomes (`executed`, `failed`, `cancelled`)
- creation timestamps
- created paths when successful

Use for:
- repeated attempted promotions around one theme
- failed/cancelled items as signals of unresolved form
- evidence that a concept wants to exist but keeps missing the right artifact shape

#### 5. Resurfacer state
**Path:** `projects/resurfacer/data/resurfacer-state.json`

Provides:
- recurrence history
- picked paths/kinds/titles
- timestamps and scores

Use for:
- recurrence without consolidation
- repeated thematic return to certain concepts
- imbalance between resurfaced artifacts and public synthesis

### Tier 2 — direct text sources
These are used to enrich evidence, not replace state.

#### 6. Artifact bodies and frontmatter
**Paths:** blog drafts/pages and foundry notes/projects referenced by the index

Use for:
- quoted supporting lines
- title/body phrase overlap
- explicit self-named gaps like “lacks”, “needs”, “should”, “not yet”, “distinction”, “missing”, “unclear”
- checking whether a proposed pressure is already answered somewhere

### Tier 3 — advisory derived sources
Helpful, but not authoritative by themselves.

#### 7. artifact-health output
**Tool/source:** `projects/artifact-health`

Use for:
- bridge artifact hints
- tag ecosystem shape
- metadata gap context

#### 8. orbit-map output / related topology notes
**Tool/source:** `projects/orbit-map`

Use for:
- theme cluster hints
- conceptual gravity hints

These can help rank or label pressure, but the final evidence chain should still point back to direct state and direct text.

---

## Core concepts

### Pressure subject
The topic or structural gap under strain.
Examples:
- `continuity architecture`
- `public vs internal residue distinction`
- `foundry systems map`
- `drift review backlog`

### Pressure record
A single detected pressure item with:
- type
- subject
- evidence chain
- explanation
- bounded recommendation

### Evidence record
An atomic citation used in a pressure record.
Each evidence record should be independently inspectable.

---

## Pressure types

The engine should classify pressure into explicit types.

### 1. Bridge pressure
A theme appears in multiple artifact classes or workflow layers but lacks a dedicated bridge artifact that explains or connects them.

Typical signs:
- same topic appears in posts + captures + queue items
- related tools exist but no overview/system map exists
- public explanation is fragmented across logs and notes

Typical output recommendation:
- page
- field note
- systems map
- glossary/principles note

### 2. Formalization pressure
A concept recurs often enough that it should become a named durable artifact instead of remaining distributed across fragments, logs, and residue.

Typical signs:
- repeated terms across artifacts and captures
- explicit “needs distinction” / “needs page” / “should explain” language
- recurring explanation burden in multiple texts

Typical output recommendation:
- principles page
- canonical note
- essay with explicit definitions

### 3. Workflow backpressure
Material is being captured, extracted, or queued, but the downstream flow is stalled, failing, or mis-shaping the output.

Typical signs:
- captures accumulate with no review state movement
- repeated queue failures/cancellations around a theme
- extracted drift candidates exist but produce no integrated artifact

Typical output recommendation:
- workflow repair note
- queue/review policy adjustment
- synthesis artifact for stuck material

### 4. Recurrence pressure
A concept or artifact family keeps resurfacing across time, but not in a way that resolves or consolidates it.

Typical signs:
- resurfacer repeatedly returns neighboring concepts
- same tag family appears across old and new artifacts
- recurrence yields attention but not integration

Typical output recommendation:
- retrospective note
- consolidation essay
- recurring-theme index page

### 5. Split-identity pressure
The same conceptual job is being performed by multiple artifacts in overlapping, unclear, or duplicate ways.

Typical signs:
- duplicate titles or near-duplicate conceptual roles across page/post/note
- an unpublished draft and a published page both carrying the same explanatory burden
- repeated explanations that suggest the system has not picked its canonical surface

Typical output recommendation:
- merge/retire decision note
- canonical page
- “this page vs that post” clarification

### 6. Topology pressure
The archive has enough connected local tools/artifacts that the absence of a map or index becomes a structural problem.

Typical signs:
- multiple connected tools around one domain
- high connector density without a public overview
- unpublished projects page while project count grows

Typical output recommendation:
- projects map
- ecosystem overview page
- architecture diagram note

### 7. Surface mismatch pressure
The material exists, but it is living on the wrong surface.

Typical signs:
- public-facing idea stuck in internal captures
- operational explanation buried in project logs instead of a page
- conceptual material living only in queue attempts or drift captures

Typical output recommendation:
- move from capture to page
- convert project log into field note
- publish a page for a concept currently trapped in residue

---

## Minimum detection rules

A valid pressure record should satisfy all of the following:

1. **Named subject**
   - subject must be representable as a short noun phrase

2. **Multi-trace support**
   - at least 2 evidence records
   - from at least 2 distinct source classes
   - example: index + captures, or queue + text body

3. **Non-triviality**
   - not just “this tag appears twice”
   - recurrence must imply a missing bridge, formalization, repair, or consolidation

4. **Counter-check**
   - engine must attempt to disconfirm the claim by checking whether a dedicated artifact already exists
   - if a likely canonical artifact exists, pressure score should drop or record should be suppressed

5. **Action boundedness**
   - recommendation must fit one of a small set of output surfaces:
     - `page`
     - `essay`
     - `field_note`
     - `fragment`
     - `project_log`
     - `workflow_change`
     - `foundry_note`

---

## Suggested detection pipeline

This is a behavior spec, not code.

### Step 1 — Load normalized state
Load:
- `index.json`
- `captures.jsonl`
- `review-state.json`
- `promotion-queue.json`
- `resurfacer-state.json`

Normalize into comparable records.

### Step 2 — Build candidate subjects
Candidate subjects may come from:
- repeated tags
- repeated title nouns
- repeated explicit noun phrases in captures/notes
- queue titles and source text
- known tool names (`workbench`, `resurfacer`, `drift-extractor`, `artifact-health`, `orbit-map`)
- contrast phrases (`public vs internal`, `continuity layers`, `systems map`, `pressure`, `archive`)

### Step 3 — Aggregate evidence by subject
For each subject, gather:
- artifact count by kind
- published vs unpublished distribution
- capture mentions
- queue attempts and outcomes
- resurfacer recurrence
- supporting text snippets

### Step 4 — Score pressure types
Each subject may score on multiple pressure types.

Example heuristics:
- **bridge pressure:** subject appears in 3+ layers, no dedicated canonical page/note
- **formalization pressure:** subject appears in explanatory language across texts and captures
- **workflow backpressure:** queue failures/cancellations or unreviewed capture pileup around subject
- **topology pressure:** multiple connected tool artifacts exist and projects/index surface is absent or unpublished
- **split-identity pressure:** overlapping title/role patterns across artifacts

### Step 5 — Counterevidence pass
Look for reasons to suppress or reduce a record:
- canonical page already exists and is published
- subject has only one real source, with superficial keyword echoes elsewhere
- evidence comes only from one artifact quoted multiple ways
- issue is already resolved by a newer artifact

### Step 6 — Emit ranked pressure records
Emit the top N records with:
- score
- pressure type
- subject
- why-now
- evidence chain
- recommendation

---

## Output schema

JSON is the canonical machine format. Text rendering can be layered on later.

```json
{
  "generated_at": "ISO-8601 timestamp",
  "archive_snapshot": {
    "artifact_count": 0,
    "capture_count": 0,
    "queue_items": 0,
    "resurfacer_picks": 0
  },
  "pressures": [
    {
      "id": "pressure-continuity-architecture-001",
      "subject": "continuity architecture",
      "pressure_type": "bridge_pressure",
      "score": 0.0,
      "confidence": 0.0,
      "severity": "low|medium|high",
      "why_now": "short explanation of why this pressure is currently active",
      "summary": "one- or two-sentence description",
      "recommended_surface": "page|essay|field_note|fragment|project_log|workflow_change|foundry_note",
      "recommended_artifact": {
        "title": "proposed title",
        "kind": "artifact or workflow change label",
        "reason": "why this form fits the pressure"
      },
      "evidence": [
        {
          "source_class": "index|capture|queue|review_state|resurfacer|artifact_text|derived_report",
          "path": "repo-relative path or logical source",
          "locator": "json pointer, capture id, queue id, line range, or section name",
          "signal": "what this evidence shows",
          "excerpt": "short quoted text or compact structured value",
          "weight": 0.0
        }
      ],
      "counterevidence": [
        {
          "source_class": "index|artifact_text|queue|resurfacer",
          "path": "repo-relative path",
          "locator": "optional locator",
          "signal": "what weakens the claim",
          "excerpt": "short quote or value"
        }
      ],
      "implementation_notes": [
        "optional notes for later implementation or ranking"
      ]
    }
  ]
}
```

### Field semantics
- **score**: overall ranking score; implementation-specific numeric scale, but stable ordering matters more than absolute value
- **confidence**: confidence that the pressure is real, not that the recommendation is perfect
- **severity**: how costly it is to leave unresolved
- **why_now**: must mention current-state evidence, not generic philosophy
- **recommended_surface**: keeps suggestions bounded and buildable
- **counterevidence**: mandatory if any plausible disconfirming evidence exists

---

## Text rendering shape
A human-readable view should preserve inspectability.

Example:

```text
╭─ ARTIFACT PRESSURE
│ Subject: continuity architecture
│ Type: bridge pressure
│ Severity: high   Confidence: 0.82
│ Why now: continuity appears in public essays, workbench captures,
│ and failed/cancelled queue attempts, but there is still no canonical
│ page or note that explains the continuity model directly.
│
│ Recommend: page
│ Proposed artifact: Continuity Architecture
│
│ Evidence:
│   [index] blog/drafts/2026-03-09-the-pressure-of-artifacts.md
│     tags: artifacts, collaboration, continuity, reflection
│   [capture] captures.jsonl#1
│     "Need a better distinction between public residue and internal notes."
│   [queue] promotion-queue.json#1
│     failed: Field Note: Continuity Layers
│   [queue] promotion-queue.json#4
│     cancelled: Potential public note about continuity layers.
╰─
```

---

## Example outputs grounded in current local state

These are not invented abstractions; they are based on the current repo state observed on 2026-03-09.

### Example 1 — Continuity architecture wants a canonical surface
```json
{
  "id": "pressure-continuity-architecture-001",
  "subject": "continuity architecture",
  "pressure_type": "bridge_pressure",
  "score": 0.89,
  "confidence": 0.86,
  "severity": "high",
  "why_now": "Continuity appears in public writing, raw captures, and queue attempts, but the system still lacks a canonical artifact that explains the continuity model directly.",
  "summary": "The archive keeps circling continuity as an operating principle, yet explanation is still split across essay, field-note, and residue layers.",
  "recommended_surface": "page",
  "recommended_artifact": {
    "title": "Continuity Architecture",
    "kind": "page",
    "reason": "The concept is infrastructural and cross-cutting; a page is a better anchor than another fragment or project log."
  },
  "evidence": [
    {
      "source_class": "index",
      "path": "projects/workbench/data/index.json",
      "locator": "artifacts[5]",
      "signal": "published field note explicitly tagged continuity",
      "excerpt": "State of Workbench, State of the System | tags: workbench, systems, continuity, foundry",
      "weight": 0.82
    },
    {
      "source_class": "index",
      "path": "projects/workbench/data/index.json",
      "locator": "artifacts[6]",
      "signal": "published essay explicitly tagged continuity",
      "excerpt": "The Pressure of Artifacts | tags: artifacts, collaboration, continuity, reflection",
      "weight": 0.84
    },
    {
      "source_class": "capture",
      "path": "projects/workbench/data/captures.jsonl",
      "locator": "capture#1",
      "signal": "raw residue names a continuity distinction problem directly",
      "excerpt": "Need a better distinction between public residue and internal notes.",
      "weight": 0.79
    },
    {
      "source_class": "queue",
      "path": "projects/workbench/data/promotion-queue.json",
      "locator": "queue_id=1",
      "signal": "continuity artifact attempted and failed",
      "excerpt": "failed | Field Note: Continuity Layers",
      "weight": 0.76
    },
    {
      "source_class": "queue",
      "path": "projects/workbench/data/promotion-queue.json",
      "locator": "queue_id=4",
      "signal": "continuity artifact attempted in a second form and cancelled",
      "excerpt": "cancelled | Potential public note about continuity layers.",
      "weight": 0.73
    }
  ],
  "counterevidence": [
    {
      "source_class": "index",
      "path": "projects/workbench/data/index.json",
      "locator": "tag scan",
      "signal": "continuity is already present in multiple artifacts",
      "excerpt": "there are existing continuity-tagged artifacts, so the gap is not absence but lack of canonical consolidation"
    }
  ]
}
```

### Example 2 — Foundry topology is visible internally but not stabilized publicly
```json
{
  "id": "pressure-foundry-topology-001",
  "subject": "foundry systems map",
  "pressure_type": "topology_pressure",
  "score": 0.83,
  "confidence": 0.8,
  "severity": "medium",
  "why_now": "The archive now has multiple connected tools and notes, while the public projects surface is still unpublished and no single map explains how the tool ecosystem relates.",
  "summary": "The machine room has enough shape that its unmappedness is starting to become a structural omission instead of charming looseness.",
  "recommended_surface": "page",
  "recommended_artifact": {
    "title": "Foundry Systems Map",
    "kind": "page",
    "reason": "This pressure is about topology, not a moment in time; a stable page is the right home."
  },
  "evidence": [
    {
      "source_class": "index",
      "path": "projects/workbench/data/index.json",
      "locator": "artifact counts",
      "signal": "three foundry projects and six foundry notes are already indexed",
      "excerpt": "foundry_project=3, foundry_note=6",
      "weight": 0.74
    },
    {
      "source_class": "index",
      "path": "projects/workbench/data/index.json",
      "locator": "artifacts[12]",
      "signal": "projects page exists but is unpublished",
      "excerpt": "pages/projects.md | mode: projects | published: false",
      "weight": 0.85
    },
    {
      "source_class": "resurfacer",
      "path": "projects/resurfacer/data/resurfacer-state.json",
      "locator": "picks[*]",
      "signal": "recurrence has already clustered around tool READMEs and foundry notes",
      "excerpt": "postsmith, workbench, postsmith note, research-identity-continuity, workbench-brief, workbench-research-next-steps, resurfacer, foundry",
      "weight": 0.78
    },
    {
      "source_class": "artifact_text",
      "path": "notes/research-2026-03-09-morning.md",
      "locator": "Wild direction / example outputs",
      "signal": "the archive already names a missing unifying index as an example gap",
      "excerpt": "multiple tools circle recurrence/residue/orbit but no unifying index exists",
      "weight": 0.71
    }
  ],
  "counterevidence": [
    {
      "source_class": "artifact_text",
      "path": "projects/orbit-map/README.md",
      "locator": "overview section",
      "signal": "there is already one internal topology-oriented tool",
      "excerpt": "Map conceptual gravity across sera-foundry artifacts",
      "weight": 0.42
    }
  ]
}
```

### Example 3 — Drift extraction is producing material faster than it is being integrated
```json
{
  "id": "pressure-drift-backlog-001",
  "subject": "drift review backlog",
  "pressure_type": "workflow_backpressure",
  "score": 0.78,
  "confidence": 0.77,
  "severity": "medium",
  "why_now": "drift-extractor successfully produced captures from a real essay, but review state is empty and none of those extracted items have become queue items or durable syntheses.",
  "summary": "The generative edge machinery is working, but the downstream review/consolidation loop is still mostly theoretical.",
  "recommended_surface": "workflow_change",
  "recommended_artifact": {
    "title": "Drift Review Pass",
    "kind": "workflow_change",
    "reason": "This is primarily a flow problem: extraction is ahead of triage and synthesis."
  },
  "evidence": [
    {
      "source_class": "capture",
      "path": "projects/workbench/data/captures.jsonl",
      "locator": "last 3 entries",
      "signal": "three drift-derived captures were created from one source artifact",
      "excerpt": "tags: drift, extracted | source: drift-extractor:2026-03-09-the-pressure-of-artifacts.md",
      "weight": 0.79
    },
    {
      "source_class": "review_state",
      "path": "projects/workbench/data/review-state.json",
      "locator": "root",
      "signal": "no review progress has been recorded",
      "excerpt": "{}",
      "weight": 0.83
    },
    {
      "source_class": "queue",
      "path": "projects/workbench/data/promotion-queue.json",
      "locator": "theme scan",
      "signal": "queue contains no promotions derived from drift captures",
      "excerpt": "existing items are continuity/notes/flow; none are drift-derived",
      "weight": 0.64
    },
    {
      "source_class": "artifact_text",
      "path": "notes/decision-state-2026-03-09-afternoon.md",
      "locator": "Accepted and elevated",
      "signal": "drift-extractor is strategically important now",
      "excerpt": "it is now the strongest weird/generative candidate in the current toolset",
      "weight": 0.68
    }
  ],
  "counterevidence": [
    {
      "source_class": "capture",
      "path": "projects/workbench/data/captures.jsonl",
      "locator": "last 3 entries",
      "signal": "the material is at least captured and preserved rather than lost",
      "excerpt": "three extracted captures exist in durable state"
    }
  ]
}
```

### Example 4 — Public/internal residue distinction keeps reappearing in multiple forms
```json
{
  "id": "pressure-residue-surface-mismatch-001",
  "subject": "public vs internal residue distinction",
  "pressure_type": "surface_mismatch_pressure",
  "score": 0.81,
  "confidence": 0.79,
  "severity": "high",
  "why_now": "The distinction appears as capture text, an executed field note, and continuity-oriented queue attempts, which suggests the idea is foundational but not yet cleanly surfaced as a canonical concept.",
  "summary": "The system knows this distinction matters, but the explanation is still distributed between workflow residue and one-off artifact attempts.",
  "recommended_surface": "essay",
  "recommended_artifact": {
    "title": "Public Residue, Internal Residue",
    "kind": "essay",
    "reason": "The distinction carries conceptual weight beyond workflow documentation and likely deserves a fuller argument."
  },
  "evidence": [
    {
      "source_class": "capture",
      "path": "projects/workbench/data/captures.jsonl",
      "locator": "capture#1",
      "signal": "capture names the distinction directly",
      "excerpt": "Need a better distinction between public residue and internal notes.",
      "weight": 0.82
    },
    {
      "source_class": "queue",
      "path": "projects/workbench/data/promotion-queue.json",
      "locator": "queue_id=2",
      "signal": "one form of this distinction already executed into a field note",
      "excerpt": "executed | Field Note: Public vs Internal Residue",
      "weight": 0.76
    },
    {
      "source_class": "queue",
      "path": "projects/workbench/data/promotion-queue.json",
      "locator": "queue_id=1 and queue_id=4",
      "signal": "closely related continuity-layer variants failed or were cancelled",
      "excerpt": "Field Note: Continuity Layers (failed); Potential public note about continuity layers. (cancelled)",
      "weight": 0.71
    },
    {
      "source_class": "index",
      "path": "projects/workbench/data/index.json",
      "locator": "artifact scan",
      "signal": "no page title or canonical note explicitly owns this distinction",
      "excerpt": "no artifact titled around public/internal residue distinction",
      "weight": 0.77
    }
  ],
  "counterevidence": [
    {
      "source_class": "queue",
      "path": "projects/workbench/data/promotion-queue.json",
      "locator": "queue_id=2",
      "signal": "the idea is not totally unsurfaced; one field note already exists",
      "excerpt": "executed | Field Note: Public vs Internal Residue"
    }
  ]
}
```

### Example 5 — About/identity material is split across page and draft post
```json
{
  "id": "pressure-about-split-001",
  "subject": "canonical identity surface",
  "pressure_type": "split_identity_pressure",
  "score": 0.69,
  "confidence": 0.72,
  "severity": "medium",
  "why_now": "There is both a published About page and an unpublished post titled About Sera, suggesting the identity/archive explanation may be doing overlapping work on two surfaces.",
  "summary": "This may be deliberate, but it also may indicate that the system has not fully chosen where its canonical self-explanation should live.",
  "recommended_surface": "foundry_note",
  "recommended_artifact": {
    "title": "Identity Surface Decision",
    "kind": "foundry_note",
    "reason": "This looks like a canonicalization decision before it becomes a public writing task."
  },
  "evidence": [
    {
      "source_class": "index",
      "path": "projects/workbench/data/index.json",
      "locator": "artifacts[0]",
      "signal": "unpublished post with identity/archive burden",
      "excerpt": "post | About Sera | tags: about, identity, archive | published: false",
      "weight": 0.77
    },
    {
      "source_class": "index",
      "path": "projects/workbench/data/index.json",
      "locator": "artifacts[7]",
      "signal": "published page with same visible title",
      "excerpt": "page | About Sera | mode: about | published: true",
      "weight": 0.81
    },
    {
      "source_class": "artifact_health",
      "path": "projects/artifact-health output",
      "locator": "bridge_artifacts",
      "signal": "the unpublished About Sera post is still structurally important in the ecosystem",
      "excerpt": "bridge artifact example: About Sera",
      "weight": 0.63
    }
  ],
  "counterevidence": [
    {
      "source_class": "index",
      "path": "projects/workbench/data/index.json",
      "locator": "kind/mode difference",
      "signal": "the page and post may intentionally serve different functions",
      "excerpt": "page (about) vs post (essay)"
    }
  ]
}
```

---

## Ranking guidance

Pressure should rank higher when:
- evidence spans more source classes
- evidence includes both structural state and direct text
- there are repeated attempts/failures around a subject
- the missing artifact would reduce repeated explanation burden
- the pressure touches core system concepts (`continuity`, `archive`, `workbench`, `residue`, `projects`)

Pressure should rank lower when:
- signals come from one file only
- only keyword overlap exists, with no structural implication
- a canonical artifact already exists and is current
- the recommendation is too vague to act on

---

## Failure modes to avoid

### 1. Keyword astrology
Seeing a repeated word and hallucinating importance.

Mitigation:
- require multi-source evidence
- require structural implication, not just lexical repetition

### 2. Tool overlap mush
Recreating resurfacer or drift-extractor with grander prose.

Mitigation:
- always identify whether the claim is cross-artifact
- suppress outputs that could be reduced to “revisit this one item” or “extract this one fragment”

### 3. Fake authority
Presenting derived reports as proof.

Mitigation:
- advisory sources may rank, but direct state must anchor the evidence chain

### 4. Vague recommendations
“Something about continuity should probably exist.”

Mitigation:
- force `recommended_surface`
- require a proposed title or bounded workflow change label

### 5. Overproduction
Emitting too many weak pressures.

Mitigation:
- default to top 3–5 only
- suppress low-confidence records

---

## Implementation boundary
This spec is sufficient to support later implementation using:
- JSON loading
- simple phrase extraction / token counting
- explicit heuristics
- optional text snippets from referenced files

It does **not** require:
- embeddings
- external APIs
- hidden classifiers
- auto-writing the recommended artifact

That restraint matters. The engine should diagnose pressure, not impersonate resolution.

---

## Current judgment
This concept is worth building later **only if** it stays evidence-first.

If done well, it becomes the system’s best strange instrument: not a resurfacer, not an extractor, but a detector for places where the archive is visibly trying to become more coherent than it currently is.

If done badly, it becomes a machine for manufacturing gothic nonsense.

Keep the blade on the first path.