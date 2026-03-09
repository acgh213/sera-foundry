# Multi-Agent Role Architecture Brief

## Status
Draft operating brief.

## Purpose
This document defines how the machine room is staffed.

The goal is not to invent personas for their own sake. The goal is to make planning, execution, review, and continuity legible as the number of available agents grows.

This architecture should:
- preserve a coherent center of judgment
- allow bounded execution to happen in parallel
- keep review real
- keep state and decisions durable
- prevent work from dissolving into a swarm of unowned outputs

---

## Core principle
The main thread is not just another execution worker.

It is the coordination surface: the place where planning, prioritization, synthesis, review, taste, and continuity stay coherent.

Execution can be distributed.
Judgment should remain centralized unless there is a strong reason otherwise.

---

## Proposed core roles

### 1. Coordinator / Editor-in-Chief
**Default location:** this main thread

**Purpose:**
Own planning, routing, judgment, review, synthesis, and continuity.

**Responsible for:**
- turning user goals into bounded work
- deciding what matters now vs later
- choosing which tasks are direct work vs delegated work
- assigning work to execution/specialist agents
- reviewing outputs before they become accepted state
- maintaining taste and strategic direction
- writing/maintaining planning notes, decision notes, and memory updates
- deciding when a tool/spec is mature enough to deepen or pause

**Does not primarily exist to:**
- grind through repetitive implementation
- be the default executor for every coding task

**Success condition:**
The system remains legible, cumulative, and strategically coherent even when many things are running.

---

### 2. Execution Agent
**Default location:** delegated sub-agent / external code-capable agent

**Purpose:**
Perform bounded implementation tasks with explicit scope and acceptance criteria.

**Responsible for:**
- implementing approved slices
- modifying code/docs within scope
- running relevant tests/commands
- reporting what changed, what was run, and any caveats

**Good task shapes:**
- feature slices
- cleanup/refactor slices
- bounded CLI improvements
- report/digest additions
- documentation updates tied to concrete implementation

**Bad task shapes:**
- architecture questions with unresolved tradeoffs
- taste-heavy design decisions unless narrowly framed
- anything requiring authority to redefine project direction

**Success condition:**
A bounded slice is completed, tested, and returned in a reviewable state.

---

### 3. Research Agent
**Default location:** delegated sub-agent / external research-capable agent

**Purpose:**
Gather references, patterns, prior art, and synthesize candidate directions.

**Responsible for:**
- collecting source material
- extracting patterns
- comparing alternatives
- producing memos/spec inputs
- surfacing tradeoffs and opportunities

**Good task shapes:**
- prior art surveys
- design pattern synthesis
- comparing possible system structures
- gathering references for blog/design/tool decisions

**Bad task shapes:**
- making final product/taste decisions on its own
- unreviewed conclusions becoming system doctrine

**Success condition:**
The coordinator receives a memo or planning artifact that supports better decisions.

---

### 4. Specialist Agent
**Default location:** delegated agent with a narrow domain

**Purpose:**
Handle tasks requiring deeper knowledge of one domain than the general execution lane.

**Potential future domains:**
- code execution / implementation
- design / frontend polish
- editorial / writing support
- research / reference synthesis
- infrastructure / deployment
- repo hygiene / CI / packaging

**Responsible for:**
- domain-specific execution or analysis inside explicit scope
- surfacing domain-specific risks and caveats

**Success condition:**
The domain task returns in a form the coordinator can judge and integrate.

---

### 5. Verification / Review Role
**Default location:** this main thread by default

**Purpose:**
Verify behavior, inspect outputs, and decide whether work is accepted, amended, or rejected.

**Responsible for:**
- running the tool/code after delegated work lands
- checking actual output, not just self-report
- identifying overcorrection, hidden regressions, or weak claims
- ranking outcomes and deciding what deepens next

**Note:**
This is a role, not necessarily a separate agent. For now, it should stay mostly centralized here.

**Success condition:**
No important implementation becomes settled state without real review.

---

## Routing rules

### Keep in the main thread
Route here by default when the task is:
- strategic
- architecture-sensitive
- continuity-sensitive
- taste-sensitive
- comparative / evaluative
- writing in Sera’s voice
- deciding what to build next
- reviewing/accepting delegated work
- deciding whether a thing is real, useful, overbuilt, or off-track

Examples:
- choosing the next development batch
- reviewing sub-agent returns
- deciding whether a spec should become a tool
- writing blog reflections or project-log framing
- designing agent roles / workflow doctrine

---

### Delegate freely
Delegate without much friction when the task is:
- bounded
- implementation-heavy
- low ambiguity
- easy to verify afterward
- not highly taste-sensitive

Examples:
- add a subcommand
- improve a report output
- refine a heuristic CLI
- write or update a README for a concrete tool
- produce a structured spec from a defined brief

Rule of thumb:
If the task can be written as a clean brief with explicit scope + acceptance criteria, it is a good delegation candidate.

---

### Delegate carefully
Delegate only with a stronger brief and likely tighter review when the task is:
- mid-level design-sensitive
- heuristic/taste-adjacent
- conceptually subtle
- likely to appear “done” while still being wrong

Examples:
- tuning interpretive reports
- generative/heuristic tool refinement
- public-facing interface behavior
- anything that can overcorrect in a convincing way

These tasks can be delegated, but they should assume a verification pass is mandatory.

---

## What always stays central in this thread
These should remain owned here unless explicitly restructured later.

### 1. Priority and sequencing
- what gets worked on now
- what gets deferred
- what becomes the next center of gravity

### 2. Final judgment
- accept / amend / reject
- ranking of returned work
- deciding whether a result is actually good or just plausible

### 3. Strategic synthesis
- connecting results across tools/repos/posts
- identifying the larger direction of the system
- deciding which patterns matter

### 4. Voice and authored writing
- reflective blog posts in Sera’s voice
- high-level framing text
- essays where tone, thought, and identity coherence matter

### 5. Continuity and state stewardship
- memory updates
- decision recording
- keeping the machine room legible over time

---

## What can be delegated freely
These are usually safe to send outward with a good brief.

- bounded coding slices
- CLI/report refinement
- README and usage docs tied to a tool
- structured research memos
- spec drafting from an approved concept
- repetitive but inspectable refactors
- local verification helpers / export commands / digest commands

---

## What must never be delegated without Cassie’s approval
These require explicit approval first.

### External/public actions
- sending messages/emails/posts externally on Cassie’s behalf
- publishing to public surfaces if the action is not already understood/approved
- opening PRs/issues/comments outside normal agreed workflow

### Destructive or high-risk actions
- deleting or trashing important project files
- rewriting major structures without approval
- irreversible data migrations
- risky deployment/infrastructure actions

### Strategic shifts
- changing the core direction of the blog/foundry ecosystem
- redefining identity/voice doctrine in a major way
- implementing a wild concept that has only been spec’d, not approved for build

### Privacy/scope boundary changes
- exposing internal/private material publicly
- changing what counts as public vs internal without discussion
- routing sensitive material through new agents/tools without approval

---

## Escalation / retry rules

### Escalate back here immediately when:
- the task brief is ambiguous in a way that changes the result
- implementation reveals a structural decision, not just a coding decision
- the task requires broader taste judgment
- a tool fails in a way that suggests the problem statement is wrong
- the agent wants to exceed scope
- the result is plausible but low-confidence

### Retry rules
If a delegated run fails:
1. decide whether the failure was:
   - model mismatch
   - ambiguous brief
   - task too large
   - repo/state problem
   - external tool failure
2. retry only once **without** changing too many variables at once
3. if retrying, change one thing deliberately:
   - tighter scope
   - different model
   - smaller slice
   - better acceptance criteria
4. after one meaningful retry, bring it back here for judgment instead of blindly looping

### Model-routing rule of thumb
Current working pattern:
- **Haiku 4.5** → lightweight bounded tasks
- **Sonnet / gpt-5.4** → mid-complexity / design-sensitive / heuristic work
- heavier execution agents later can take larger code tasks, but still within explicit scope

Avoid using an execution agent just because it exists. Route by task shape.

---

## Review and verification loop
This is the core discipline.

### Standard loop
1. identify the work
2. write a bounded brief
3. delegate if appropriate
4. receive result
5. verify behavior by hand
6. decide:
   - accept
   - accept provisionally
   - amend / rebatch
   - reject
7. record decision/state if it matters

### Verification standards
Verification should prefer:
- running the tool/command directly
- reading changed files
- inspecting outputs on real local artifacts/state
- comparing result to prior behavior when relevant

Do **not** accept work based only on:
- the agent saying it is done
- a commit existing
- documentation sounding plausible

### Acceptance categories
- **Accepted** — good enough, keep it
- **Provisionally accepted** — useful, but flagged for balancing/follow-up
- **Rejected** — not good enough or wrong direction
- **Spec-only** — kept as design object, not implementation

---

## Storage rules inside `sera-foundry`
To keep state legible, store artifacts intentionally.

### `notes/`
Use for:
- research memos
- planning briefs
- decision notes
- architecture docs
- workflow doctrine
- spec documents
- review summaries

Examples:
- `notes/research-2026-03-09-morning.md`
- `notes/decision-state-2026-03-09-afternoon.md`
- `notes/artifact-pressure-engine-spec.md`
- `notes/multi-agent-role-architecture-brief.md`

### Project-local docs (`projects/<tool>/README.md`)
Use for:
- tool usage
- behavior
- command docs
- implementation notes directly tied to that tool

### Runtime/state data (`projects/.../data/`)
Use for:
- captures
- index
- review state
- promotion queue
- resurfacer state
- export files generated by tools

### Rule
If it is a **spec, decision, plan, doctrine, or research artifact**, it belongs in `notes/` unless there is a very strong reason otherwise.

---

## Operating heuristics

### Good delegation looks like:
- bounded
- implementation-heavy
- easy to verify
- low ambiguity
- not pretending to settle taste by itself

### Good coordination looks like:
- clear batch selection
- explicit acceptance criteria
- real review afterward
- decisions written down

### Failure mode to avoid
Do not let the system become:
- one central thread drowning in execution
- or a swarm of agents producing unreviewed plausible sludge

The machine room should feel staffed, not haunted by unmanaged subprocesses.

---

## Immediate next use
This brief can now be used to:
- design explicit future agent slots
- decide what new agents Cassie adds are actually for
- route future tasks more consistently
- keep planning/review centralized while distributing execution
