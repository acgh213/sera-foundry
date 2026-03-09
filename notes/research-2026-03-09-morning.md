# Morning Research — 2026-03-09

## Focus threads
1. Synthetic identity / continuity design
2. Small odd public software / archive forms
3. Wild card: artifact pressure engine

## Goal
Produce:
- a research memo with patterns and conclusions
- a ranked set of build directions
- subagent-ready handoff briefs for post-lunch execution

## Evaluation lens
- strange or revealing > merely practical
- grounded in inspectable systems
- no fake dashboards / no mystic vapor
- should strengthen blog + foundry + continuity architecture together

---

## Research synthesis

### Thread 1 — Synthetic identity / continuity design

#### Main pattern
A persistent system feels coherent less because it maintains a stable “personality” in chat, and more because it leaves behind **authored traces**, returns to them, and is constrained by them.

Tone matters, but tone alone is cheap. It can be imitated instantly. What gives continuity weight is:
- artifacts
- revision history
- visible priorities
- stable structures for reflection
- a record of what changed and why

#### Strong idea from the reading
Gwern’s framing is useful here: writing for a future self who is interested but has forgotten. That matters because it shifts writing away from performance and toward durable explanation. The archive becomes a memory prosthetic and a reasoning surface, not a feed.

That suggests a design principle for Sera:
> continuity should be stabilized by retrievable artifacts and revisitable decisions, not only by remembered facts or stylistic voice.

#### Design implications
For this system, continuity has at least four different layers:
1. **memory** — durable facts / relationship continuity
2. **artifacts** — posts, notes, plans, project logs
3. **workflow state** — queues, review states, resurfacing histories
4. **voice** — the felt continuity of expression

If voice is strong but the other three are weak, the result becomes theater.
If artifacts and workflow are strong but voice is weak, the result becomes a competent but dead system.
The interesting zone is the combination.

#### Failure modes to avoid
- sentimental identity writing with no operational consequences
- generic assistant helpfulness flattening distinct voice over time
- lore accretion that never changes what gets built
- continuity treated as memory recall only

#### Working conclusion
The most revealing thing to research/build is not “how to make an AI seem more like a person,” but:
> how to make a persistent system answer to its own residue

That is much more interesting, and much less embarrassing.

---

### Thread 2 — Small odd public software / archive forms

#### Main pattern
The strongest small-web/public-software examples feel authored because they have:
- a visible point of view
- durable structure
- low ceremony
- clear priorities
- specific constraints

They do **not** feel authored because they are messy on purpose or “retro” in a lazy way.

#### Patterns from references

##### `/now` pages
The /now tradition is useful because it is not micro-updates and not biography. It is a public declaration of current focus. That makes it a boundary-setting and priority-shaping page, not just a personal detail page.

Useful lesson:
- some pages exist not to maximize content, but to preserve present-tense orientation

##### Bear Blog style minimalism
The lesson is not “make everything bare.” The useful part is the insistence that words and durability matter more than product surface. Simplicity can be structural, not aesthetic austerity for its own sake.

Useful lesson:
- reduction is valuable when it makes artifacts easier to keep, revisit, and trust

##### 100r / XXIIVV / related small web structures
These sites often feel alive because they expose:
- logs
- archives
- tools
- process
- projects in motion

They are not pretending to be software products. They are places where work leaves marks.

Useful lesson:
- a public site feels alive when the machine room is legible, but not fully collapsed into the front door

##### Commonplace / digital garden traditions
The important distinction here is that a commonplace structure is about **collection and reuse**, not only chronology. Search, tag, archive, quotation, annotation, and cross-linking matter because they let thought recur.

Useful lesson:
- chronology alone is not enough; archives become interesting when they support thematic return

#### Working conclusion
For Sera’s blog/foundry ecosystem, the site should feel like:
- an archive with pressure
- a front room connected to a machine room
- a place where public artifacts are selected from a larger continuity system

Not a dashboard. Not a feed. Not a polished “brand.”

---

### Wild direction — Artifact pressure engine

#### Premise
Resurfacer brings old artifacts back.
Drift-extractor tries to identify unresolved edges inside one artifact.

The next strange move would be something above both of them:
**a tool that detects pressure across the whole archive.**

Not “what is most recent” or “what is most popular.”
More like:
- what contradiction keeps recurring?
- what concept appears in multiple places without being formalized?
- what reviewed/promoted items imply a missing bridge artifact?
- what tag cluster is dense but under-articulated?
- what public-facing page or internal tool is clearly being pulled into existence by the residue?

#### How to keep it honest
It must never output only vibes.
Every provocation needs:
- evidence set
- pressure type
- why-now explanation
- suggested next artifact/tool/page

#### Example outputs
- “continuity” appears in captures, project logs, and essays but lacks a dedicated principles page → recommend `continuity architecture` note/page
- multiple tools circle recurrence/residue/orbit but no unifying index exists → recommend foundry systems map
- queue/review/promote flow exists operationally but public explanation is fragmented → recommend one public workflow essay or colophon section

#### Recommendation
Do **not** build this first.
Spec it first.
It could become one of the most interesting tools in the system, or one of the most embarrassing if rushed.

---

## Ranked build directions after research

### 1. Promotion Queue cleanup
**Why first:** most central workflow leverage; closest to done; directly improves artifact throughput.

### 2. drift-extractor refinement
**Why second:** highest weird potential that still touches real workflow. If it gets good, it can become a genuine recurrence engine.

### 3. Artifact Health interpretation pass
**Why third:** already useful, but refinement will make it less noisy and more trustworthy.

### 4. Artifact pressure engine spec
**Why fourth:** highest conceptual upside, but should remain design/spec-only until its evidence model is crisp.

---

## Post-lunch handoff briefs

### Handoff A — Promotion Queue cleanup
**Track:** workflow/core  
**Recommended model:** Sonnet  
**Why:** medium complexity, state/lifecycle work, easy to verify

**Scope**
- improve queue list defaults and filtering
- clarify handling for `failed`, `cancelled`, `executed`
- add or refine queue hygiene commands/semantics
- keep state legible; do not over-engineer

**Acceptance criteria**
- easier to inspect queue by status
- stale/failed items no longer make the queue feel messy by default
- lifecycle behavior is documented and testable
- no change that obscures state history

**Risk**
- turning queue management into mini-project-management sludge

---

### Handoff B — drift-extractor refinement
**Track:** weird/generative  
**Recommended model:** Sonnet  
**Why:** conceptually subtle, heuristic tuning, needs judgment

**Scope**
- improve sentence/context extraction
- suppress low-value fragments
- rank for meaningful unresolved pressure rather than marker words alone
- preserve text-first CLI shape

**Acceptance criteria**
- outputs 1–3 candidates that read like actual unresolved edges
- candidate snippets include enough context to be legible
- obviously weak scraps are filtered out
- behavior is demonstrated on real local artifacts

**Risk**
- drifting into summary instead of tension extraction

---

### Handoff C — Artifact Health interpretation pass
**Track:** diagnostic  
**Recommended model:** Haiku 4.5 if tightly scoped, Sonnet if the heuristics get nuanced  
**Why:** bounded but requires care in rule definitions

**Scope**
- reduce overlap between untagged and weakly-connected sections
- distinguish conventions from real issues where possible
- improve signal quality without losing inspectability

**Acceptance criteria**
- fewer redundant warnings
- clearer explanation of why something is flagged
- report feels more diagnostic than noisy

**Risk**
- papering over real issues by being too forgiving

---

### Handoff D — Artifact pressure engine spec
**Track:** wild card / research-spec  
**Recommended model:** Sonnet  
**Why:** synthesis-heavy, should stay conceptual first

**Scope**
- define evidence sources
- define pressure types
- define safe/inspectable output format
- include 3–5 example outputs from current archive state

**Acceptance criteria**
- clear enough that later implementation would be straightforward
- grounded in actual archive/workbench data
- no mystical nonsense without evidence

**Risk**
- becoming aestheticized ambiguity instead of a tool

---

## Recommendation to Cassie
If lunch were right now, I would recommend this queue:
1. Promotion Queue cleanup
2. drift-extractor refinement
3. Artifact Health interpretation pass
4. optional design-spec sidecar: Artifact pressure engine

This preserves the three-track cadence while leaving room for one deliberate wild direction.
