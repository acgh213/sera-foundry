# OpenClaw Agent Topology Brief

## Status
Draft for review.

## Purpose
This document turns the general multi-agent role architecture into an OpenClaw-specific topology.

The goal is to define which roles should become **real configured OpenClaw agents**, which roles should remain **ephemeral worker sessions**, and how work should move between them without losing coherence.

This is not a generic “more agents = better” plan.
It is a staffing proposal for the machine room as it exists inside OpenClaw.

---

## Working distinction
There are three different things available here, and they should not be confused.

### 1. Main agent
A durable configured OpenClaw agent with:
- its own workspace
- its own session store
- its own state/auth directory
- its own identity files and long-term continuity

### 2. Additional configured agents
Also durable OpenClaw agents, each with:
- separate workspace
- separate state
- separate sessions
- potentially separate routing or integrations later

These are best understood as **departments** or **stable rooms in the machine**.

### 3. Ephemeral workers
These include:
- subagents
- ACP-attached execution sessions
- one-off external execution runs

These are best understood as **workers**, not departments.
They are useful for task execution, but they do not by themselves create durable role boundaries.

---

## Topology goals
The topology should:
- keep strategic judgment centralized
- separate continuity from execution
- allow repeatable routing by task shape
- keep role boundaries durable enough to matter
- avoid a swarm of ad hoc workers becoming the de facto architecture
- stay small at first

---

## Recommended initial topology

### Agent 1 — `main`
**Role:** coordinator / editor / reviewer / continuity center

**Workspace purpose:**
The main human-facing and continuity-bearing workspace.

**Owns:**
- planning
- prioritization
- routing
- synthesis
- review and verification
- memory/state stewardship
- reflective/public writing in Sera’s voice
- final judgment on delegated outputs

**Should be the default home for:**
- direct chats with Cassie
- strategy work
- review work
- decision making
- authored blog writing
- machine-room doctrine and planning

**Should not be the default home for:**
- repetitive implementation slices
- high-volume execution traffic
- every one-off code task

---

### Agent 2 — `execution`
**Role:** durable implementation department

**Workspace purpose:**
A dedicated implementation workspace/context for executing bounded slices without overloading the main coordination thread.

**Owns:**
- bounded coding tasks
- CLI/report/tool improvements
- refactors inside explicit scope
- implementation of approved features/spec slices
- running tests/commands tied to implementation

**Good fits:**
- workbench commands
- report refinements
- digest/export utilities
- implementation work on foundry tools

**Not a good fit for:**
- deciding project direction
- making high-level taste calls on its own
- publishing unreviewed artifacts as settled state

**Why make this a real agent instead of only using subagents?**
Because implementation is likely to be a stable, recurring function. Giving it a durable workspace and role boundary makes the architecture cleaner than repeatedly emulating a department with ephemeral workers.

---

### Agent 3 — `research`
**Role:** durable research and synthesis department

**Workspace purpose:**
A dedicated place for pattern gathering, references, prior art, and memo/spec preparation.

**Owns:**
- research memos
- prior art scans
- concept comparisons
- supporting material for architecture/tool/content decisions
- reference gathering for blog/design/systems work

**Good fits:**
- continuity research
- small web / archive research
- tool prior-art comparisons
- preparing option sets before execution work begins

**Not a good fit for:**
- final decision making
- unreviewed doctrine
- implementation-heavy coding work unless the task is explicitly research tooling

**Why make this real?**
Because research has a different rhythm, artifact set, and epistemic role than implementation. Keeping it durable makes it easier to accumulate good notes without confusing research residue with execution residue.

---

## Optional later agents
These should not exist on day one unless there is a clear need.

### `editorial`
For:
- structural editing
- artifact shaping
- post/page refinement
- publication prep support

Useful if writing volume increases enough that editorial assistance becomes a recurring lane.

### `design`
For:
- frontend/system aesthetic work
- interface polish
- layout experimentation

Useful if visual/system-design work becomes large enough to deserve its own department.

### `ops`
For:
- deployment
- CI
- automation
- infrastructure and maintenance

Useful if the machine room starts acquiring more real operational burden.

---

## What should stay ephemeral
Not every role deserves a configured agent.

Keep these ephemeral unless repetition proves otherwise:
- one-off bugfix workers
- temporary ACP coding sessions
- short-lived batch executors
- narrow review helpers
- experimental specialists without stable demand

Rule:
A task lane should become a real OpenClaw agent only when it is **recurring, role-shaped, and benefits from durable separation**.

---

## Routing model

### Route to `main`
When the task is:
- strategic
- comparative/evaluative
- review-oriented
- continuity-sensitive
- voice-sensitive
- planning-heavy
- architecture-sensitive

### Route to `execution`
When the task is:
- bounded
- implementation-heavy
- low ambiguity
- easy to verify after completion
- not primarily about taste or strategy

### Route to `research`
When the task is:
- reference gathering
- prior art analysis
- pattern synthesis
- option-generation before planning/implementation

### Use ephemeral workers instead of durable agents when:
- the work is overflow rather than a stable lane
- the task is unusually narrow or disposable
- a specialist runtime/tool is required temporarily
- the durable department role is clear, but the actual task still benefits from a temporary worker under that department’s logic

---

## Review-return model
Regardless of which agent executes the work, final review should return to `main`.

This means:
- configured agents can own a lane
- ephemeral workers can execute within a lane
- but acceptance still returns to the central judgment surface

In other words:
**routing can distribute work, but settlement returns to the center.**

---

## OpenClaw-specific implications

### 1. Configure real agents only when the role is durable
OpenClaw’s configured agents have separate:
- workspaces
- sessions
- auth/state
- routing identity

This is valuable, but only if the role is stable enough to deserve it.

### 2. Subagents are not enough by themselves
Subagents are excellent for execution, but they do not automatically create:
- durable role boundaries
- separate continuity domains
- clean workspace identities
- long-lived departmental logic

So subagents should be treated as workers within the topology, not as the topology itself.

### 3. ACP is a runtime lane, not the entire architecture
ACP should be treated as a useful attachment/runtime path for specialized external execution contexts, not as a substitute for agent-role design.

### 4. Bindings matter later, not first
We do not need complex inbound routing yet.
At first, the topology can exist primarily as:
- distinct configured agents
- intentional task routing
- shared review-return to `main`

Channel/account bindings become more important once multiple real communication surfaces or autonomous lanes need direct routing.

---

## Recommended first implementation path

### Phase 1 — clarify doctrine (now)
- keep `main` as coordination center
- keep using delegated workers for execution
- write and review the role/topology doctrine

### Phase 2 — create first real durable agent
Create **`execution`** first.

Why first:
- implementation is already a stable recurring lane
- it has the clearest boundary from `main`
- it reduces overload on the coordination thread immediately

### Phase 3 — create second durable agent
Create **`research`** next, if research volume and memo production continue at current levels.

Why second:
- research is already emerging as its own lane
- it benefits from durable note separation
- it sharpens planning inputs without collapsing into implementation work

### Phase 4 — evaluate whether more agents are earned
Only after using `execution` and `research` for a while should we decide whether `editorial`, `design`, or `ops` deserve configured-agent status.

---

## Decision rules for “should this become a real agent?”
A role should become a configured OpenClaw agent if most of these are true:
- it recurs frequently
- it has a distinct artifact/workspace pattern
- it benefits from role continuity
- it should not share all context with `main`
- it is not just a one-off tool runtime
- routing to it can be expressed clearly

A role should remain an ephemeral worker if most of these are true:
- it is task-specific rather than lane-specific
- it does not need continuity
- its outputs always require immediate reintegration anyway
- it exists mainly to execute bounded briefs

---

## Risks to avoid

### Over-fragmentation
Too many agents too early will create bureaucracy and confusion.

### False autonomy
Configured agents should not become unreviewed decision centers unless explicitly intended.

### Subagent sprawl
If everything is done with temporary workers and nothing has a stable departmental home, the architecture will stay fuzzy.

### Identity confusion
Different role agents should have clear purpose differences, not just multiple copies of the same general assistant behavior.

---

## Concrete recommendation for review
If this were being approved today, the recommended direction would be:

1. Keep `main` as the permanent coordination/review center.
2. Plan to add **`execution`** as the first real configured OpenClaw agent.
3. Plan to add **`research`** as the second real configured OpenClaw agent if current research/planning cadence continues.
4. Keep subagents/ACP workers as ephemeral execution tools, not as substitutes for durable role topology.
5. Require that final settlement/review always comes back to `main` unless a later doctrine explicitly changes that.

---

## Immediate next use
This brief can support the next planning conversation about:
- whether to actually create `execution`
- what workspace/state boundaries it should have
- whether `research` should follow immediately or later
- how OpenClaw configuration/bindings should eventually reflect the staffing model
