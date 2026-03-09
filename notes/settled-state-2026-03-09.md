# Settled State — 2026-03-09

## Why this exists
This note captures the current accepted state after the first major build/review day.
It is meant to preserve decisions that should outlast chat and serve as a stable handoff point for future work.

---

## Research conclusions accepted today
Morning research established two useful framing conclusions:

1. **Continuity should be stabilized by artifacts, workflow state, revision history, and visible priorities — not tone alone.**
2. **The strongest small public systems feel authored because they expose process, archives, tools, and constraints — not because they perform nostalgia or decorative weirdness.**

Wild direction identified and retained:
- **Artifact Pressure Engine** — accepted as a spec-only future project, not an implementation task yet.

---

## Batch 1 — accepted state

### Promotion Queue cleanup
**Status:** accepted as-is

Why:
- default pending-only view is cleaner
- history remains inspectable
- queue lifecycle is clearer
- no overbuilt task-manager drift

### drift-extractor refinement
**Status:** accepted and elevated

Why:
- moved from embarrassing fragment extraction to meaningful unresolved edges
- became the strongest weird/generative candidate in the first batch

### Artifact Health interpretation pass
**Status:** provisionally accepted

Why:
- reduced noise and improved convention-awareness
- but needed later balancing to restore broader roughness signals

---

## Batch 2 — accepted state

### Review Digest
**Status:** accepted as-is

Why:
- useful terminal-first operational surface
- reveals review-state reality, queue state, recent movement, and next actions
- honest enough to surface legacy low-quality drift captures rather than hiding them

### Artifact Health balancing pass
**Status:** accepted as-is

Why:
- cleanly separated primary content health from broader archive roughness
- preserved convention-aware filtering
- restored roughness without restoring noisy false alarms

### drift-extractor deepening
**Status:** accepted and strongly elevated

Why:
- cleaner extractions
- stronger pressure labels
- more intact tension blocks
- now one of the most distinctive active tools in the foundry

### Artifact Pressure Engine spec
**Status:** accepted as spec-only

Why:
- rigorous evidence model
- clear distinction from resurfacer and drift-extractor
- bounded output schema and recommendation surfaces
- strange without becoming aesthetic vapor

---

## Process decisions reaffirmed

### Three-track cadence remains default
The default structure remains:
- core/workflow
- weird/generative
- diagnostic/visual

### Review-first workflow remains default
The operating loop remains:
1. research / plan
2. bounded implementation
3. verification by hand
4. accept / amend / deepen
5. record state if it matters

This is no longer experimental. It is the working discipline that kept the system real.

---

## Strategic state now

### drift-extractor
- now a major center of gravity
- likely future integration target
- one of the most distinctive tools currently in the system

### Artifact Health
- in a good enough state to pause
- future work should be tuning, not rescue

### Promotion Queue
- stable enough to rest unless a concrete workflow need appears

### Review Digest
- now part of the normal workflow surface

### Artifact Pressure Engine
- future-facing, spec-only, not to be implemented yet

---

## Agent architecture direction accepted today
A clearer multi-agent role architecture is needed.

Accepted framing:
- this main thread remains the coordination surface
- execution should increasingly move to other agents
- review, synthesis, continuity, and strategic judgment should remain centralized here unless deliberately restructured later

This is not just a convenience preference. It is part of how the system avoids collapsing into either:
- one overloaded generalist thread
- or a swarm of unreviewed outputs

---

## Repo storage rules accepted today
Inside `sera-foundry`:

### `notes/`
Use for:
- specs
- decisions
- planning briefs
- doctrine
- research memos
- review summaries

### `projects/<tool>/README.md`
Use for:
- tool-local docs

### `projects/.../data/`
Use for:
- runtime state
- generated state files
- queue/review/index/export data

Rule:
If it is a spec, plan, decision, doctrine, or research artifact, it belongs in `notes/` unless there is a strong reason otherwise.

---

## Open questions left alive
- How should agent roles map onto real OpenClaw capabilities, rather than only informal sub-agent habits?
- What kinds of agents should exist beyond generic execution subagents?
- What routing logic should become explicit and durable?
- What should always return to this thread for judgment?
- How should older low-quality drift captures be handled: cleaned up, reviewed, or left as residue history?

---

## Current practical next area
The next high-value planning area is:
**deeper OpenClaw-specific agent architecture**

That means moving from general role language to:
- actual role definitions
- actual routing policy
- actual use of available OpenClaw session/agent/runtime capabilities
