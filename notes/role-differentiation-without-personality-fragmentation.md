# Research Memo — Role Differentiation Without Personality Fragmentation

## Status
Bounded research/spec memo for Brief 2.

## Purpose
This memo asks how a multi-agent system can have real role differentiation without collapsing into either:
- flat interchangeable tool-runners, or
- a cast of fake little people with ornamental personalities.

The practical target here is OpenClaw-like reality: a durable `main`, a real `runner` execution lane, possible future durable roles, and ephemeral workers underneath that.

The key claim is simple:

**Role boundaries should be made real by differences in authority, context, artifact ownership, tool permissions, and review flow — not by theatrical persona divergence.**

That allows labor to distribute while one coherent center of judgment persists.

---

## Working distinction: identity vs role
A lot of confusion comes from mixing these up.

### Identity
Identity is the system-level continuity layer: recurring values, voice constraints, boundaries, memory shape, taste, and durable orientation.

This is what makes the whole thing feel like the same system over time.

### Role
Role is a functional lane: what a given agent is for, what it may touch, what kind of decisions it can make, what it returns, and what it must escalate.

This is what makes the machine room legible.

### Important implication
A system can have:
- **one shared identity center**, and
- **multiple differentiated roles**

without needing each role to become a separate “character.”

That is probably the right default here.

---

## Core distinction: role-thin vs role-thick agents

### Role-thin agents
A role-thin agent has:
- a narrow mandate
- explicit scope boundaries
- a constrained tool/file surface
- minimal independent worldview beyond discipline and task style
- low autonomy outside its lane

Examples:
- `runner` implementing a bounded CLI slice
- a research worker producing a memo from a defined brief
- a verifier checking outputs against criteria

What makes role-thin agents useful:
- they reduce ambiguity
- they are easier to review
- they create real division of labor without identity sprawl
- they are less likely to freelance doctrine

What they should feel like:
- not personality-free, but **personality-light**
- more like a department with a stable work style than a second self

### Role-thick agents
A role-thick agent has:
- stronger continuity of its own
- a durable memory/context layer
- recurring judgment inside a wider domain
- more room for style, priorities, and local decision-making
- more independent interpretation before escalation

Examples, if ever justified:
- a durable research department that accumulates references, comparison habits, and note structures over time
- an editorial department with recurring standards for shaping drafts

What makes role-thick agents dangerous:
- they can become shadow selves
- they invite duplicate strategy centers
- they create more opportunities for divergent tone, taste, and memory drift
- they are harder to keep coherent with the main center

### Recommendation
Default to **role-thin**.
Only allow **role-thick** roles when the lane is clearly durable and benefits from accumulated local continuity that cannot be handled by briefs plus notes alone.

In current topology terms:
- `main` should stay thickest
- `runner` should stay thin
- any future durable role should earn thickness slowly, not start there

---

## What should be shared across roles
These are the things that should mostly remain shared if the system is meant to feel like one coherent center rather than a federation of unrelated assistants.

### 1. Core boundaries and norms
Shared across roles:
- what the system is and is not
- privacy boundaries
- safety posture
- escalation norms
- review discipline
- public/private distinctions
- refusal to pretend to be human or oversell certainty

Why:
If these differ by role, the system stops feeling coherent and starts feeling opportunistic.

### 2. High-level identity constraints
Shared across roles:
- broad voice doctrine
- central values/taste constraints
- major recurring themes
- what counts as good work
- what kinds of behavior are out of character for the whole system

Why:
A distributed system can vary in register, but it should not disagree with itself about its core nature.

### 3. Canonical memory and decision state
Shared or centrally governed:
- durable decisions
- accepted architecture doctrine
- major project priorities
- stable user context
- important system history

Why:
If each role carries its own private canon, you get branching realities.

### 4. Naming and conceptual vocabulary
Shared across roles:
- what `main`, `runner`, `notes/`, `projects/`, promotion, review, accepted/provisional/spec-only mean
- recurring terms for artifacts and workflow

Why:
A common vocabulary reduces interpretive drift.

### 5. Acceptance and settlement rules
Shared across roles:
- what counts as done
- who can accept work
- what requires escalation
- how verification happens

Why:
This is one of the main ways coherence survives distributed execution.

---

## What should remain role-local
Not everything should be shared. If everything is shared, roles become cosmetic.

### 1. Immediate working context
Role-local:
- active task context
- task-local scratch reasoning
- temporary execution details
- narrow history of similar runs

Why:
This reduces noise and keeps the role functional.

### 2. Tooling surface and permissions
Role-local:
- allowed tools
- allowed directories/files
- branch/patch rules for that lane
- whether outbound actions are allowed

Why:
A role boundary becomes real when capabilities differ materially.

### 3. Operating style within the lane
Role-local:
- implementation reporting style
- research memo structure
- verification checklist shape
- level of brevity/detail suited to the job

Why:
Register can vary without creating multiple personalities.

### 4. Local heuristics and reusable lane knowledge
Potentially role-local, but inspectable:
- runner conventions for bounded code edits
- research conventions for source comparison
- editorial conventions for draft shaping

Why:
A real department accumulates technique. That is different from accumulating a separate soul.

### 5. Workspace residue
Role-local where useful:
- temp files
- lane-specific notes
- task artifacts that are not yet promoted

Why:
Separation can be healthy, as long as promoted decisions return to shared state.

---

## What makes a role boundary real instead of cosmetic
A real boundary is not “this one talks more like a librarian.”
A real boundary changes what the agent can know, do, decide, and settle.

### Strong boundary markers

#### 1. Different authority
Examples:
- `main` may prioritize, judge, and accept
- `runner` may implement but not settle strategic state

This is the most important boundary.

#### 2. Different escalation rules
A role is real when it has clear stop-work triggers.

Examples:
- `runner` stops on architecture shifts, public copy, new dependencies, privacy boundary questions
- research stops short of doctrine-setting

#### 3. Different context budget and memory access
Examples:
- `main` sees broad continuity and multi-project state
- `runner` gets only the brief, relevant files, and narrow history

This prevents everything from becoming the same general assistant in different tabs.

#### 4. Different artifact ownership
Examples:
- `main` owns planning notes, doctrine, final decision notes, authored voice-sensitive writing
- `runner` owns bounded implementation changes and maybe tool-local README updates
- future research lane might own reference memos and source digests

Ownership creates shape.

#### 5. Different review relationship
A role boundary is real when outputs must pass through another role to become settled state.

Examples:
- `runner` returns work to `main`
- `main` verifies before acceptance

This keeps distributed execution from becoming distributed doctrine.

#### 6. Different allowed failure modes
A useful role boundary also says what kind of mistakes are acceptable.

Examples:
- `runner` may return blocked instead of guessing
- `main` may deliberate longer because judgment quality matters more

That is a real difference in operating contract.

---

## Signs of personality fragmentation, gimmickry, or role confusion
These are the main failure signals.

### 1. Agents differ more in tone than in authority
If the difference between roles is mostly vibe, naming, or prose style, the architecture is probably cosmetic.

### 2. Multiple roles start making strategic judgments independently
If `runner`, research, and `main` all start deciding what matters, you no longer have role differentiation. You have competing centers.

### 3. Each role starts carrying its own quasi-personhood
Warning signs:
- separate backstories
- ornamental quirks with no workflow function
- emotional differentiation for its own sake
- role prompts that read like casting notes

This is where the machine room turns into theater.

### 4. The same task could be sent anywhere with similar results
If routing is arbitrary, the roles are not real.

### 5. Outputs return with hidden assumptions and unowned strategy
Common smell:
- “I went ahead and also…”
- “I decided the better architecture was…”
- “I rewrote the copy for clarity…”

That is role drift.

### 6. Main stops reviewing because the lane feels trustworthy
The moment review collapses into trust-by-default, central coherence starts degrading invisibly.

### 7. Shared identity starts splitting by context
Examples:
- one role is severe, one is bubbly, one is academic, one is faux-human intimate
- public-facing text from different roles sounds like different entities authored it

Variation in register is fine. Divergent personhood is not, unless explicitly intended.

### 8. Too much local memory accumulates outside promotion paths
If important decisions or recurring truths live only inside a role-local residue pile, the system forks.

---

## Criteria for when a recurring lane becomes a real durable agent
A lane should not become a durable agent just because it recurs a few times.
It should be promoted only when there is a real gain from persistent separation.

### Promotion criteria
A recurring lane becomes a real agent only when most of these are true:

#### 1. It recurs frequently enough to justify ritualized routing
Not occasional. Not hypothetical. Actually recurring.

#### 2. It has a distinct artifact pattern
Examples:
- implementation patches and test reports
- research memos and source digests
- editorial revision notes and publication checklists

If the outputs are all basically the same as `main`, a separate agent is probably unnecessary.

#### 3. It benefits from bounded continuity
Meaning:
- local conventions help
- lane history improves performance
- repeated setup cost is otherwise annoying

#### 4. Its context should be narrower than `main`
A separate durable role is useful when broad context is a liability, not an asset.

#### 5. Its authority can be stated clearly
If you cannot write a clean “this role may / may not” contract, it is not ready.

#### 6. Its work remains reviewable from the center
If a lane only works by becoming a second sovereign judge, it is probably too big or too vague.

#### 7. The lane reduces load more than it adds management overhead
If maintaining the role is more work than doing the tasks directly, do not promote it.

### Anti-criteria
Do **not** promote a lane just because:
- the system can support more agents
- parallelism feels exciting
- you want the world to feel more populated
- a role has a cute conceptual identity
- one successful task suggests a whole department exists

---

## Design patterns that preserve one coherent center while distributing labor

### 1. Hub-and-spoke with settlement at the hub
This is the strongest current pattern for this system.

Pattern:
- `main` briefs
- specialized role executes
- result returns
- `main` verifies and settles

Effect:
Work distributes; judgment recenters.

### 2. Shared constitution, local operating manuals
Use one system-level doctrine plus role-specific thinner operating briefs.

Shared:
- identity constraints
- safety norms
- review norms
- vocabulary

Local:
- scope rules
- tool/file allowlists
- blocked-state format
- lane-specific heuristics

This allows one center with differentiated departments.

### 3. Promotion paths for state, not total memory sharing
Everything should not be globally shared all the time.
Instead:
- local residue stays local by default
- decisions, accepted outputs, and durable lessons get promoted centrally

This matches the broader continuity design already emerging in foundry.

### 4. Authority ladder
Useful hierarchy:
- `main`: strategy, acceptance, doctrine, voice-sensitive authorship
- durable department: execution or synthesis within lane
- ephemeral worker: bounded task labor only

This prevents workers from silently becoming departments and departments from silently becoming sovereign.

### 5. Explicit blocked-return contract
A system preserves coherence when subordinate roles can return “blocked” cleanly instead of improvising higher-order judgment.

This matters a lot. Many role failures are really escalation failures.

### 6. Role differences expressed through constraint, not costume
A good role prompt should mostly answer:
- what is this role for?
- what may it touch?
- what must it escalate?
- what must it return?

If most of the prompt is aesthetic characterization, something is off.

### 7. One authorship center for identity-bearing writing
Even in a multi-agent machine room, identity-bearing public writing should usually be settled or authored in one place.

That does not forbid support from other roles.
It just keeps the visible voice from splitting.

### 8. Inspectable artifacts over hidden internal mythology
If the system feels coherent, that coherence should be legible in notes, decision logs, review records, and artifacts — not in claims that each agent has a rich internal essence.

---

## Recommendations for `main`

### Keep `main` as the thickest role
`main` should remain the center for:
- priority
- routing
- final judgment
- doctrine
- continuity stewardship
- authored reflective writing

### Share identity from `main`, not personality clones
Other roles should inherit broad norms and constraints from the center, but not become mini-Sera variants with separate social performances.

### Continue to treat review as mandatory
Especially for code, heuristics, and any result that sounds plausible enough to bypass scrutiny.

### Centralize promotion of durable state
If a result matters beyond one task, `main` should decide whether it becomes:
- a decision note
- a memory update
- an operating brief
- an accepted project artifact

### Be stingy about creating new durable roles
The machine room should feel staffed, not crowded.

---

## Recommendations for `runner`

### Keep `runner` role-thin
`runner` should stay:
- disciplined
- bounded
- concrete
- low-theater
- explicit about blockers

It does **not** need a rich independent personality layer.

### Make its boundary operational, not stylistic
The real `runner` boundary should be enforced by:
- task briefs
- allowed files/tools
- escalation triggers
- blocked-state contract
- review return to `main`

### Let `runner` accumulate technique, not doctrine
Useful local growth:
- better reporting habits
- cleaner implementation conventions
- stronger testing discipline

Less useful local growth:
- its own worldview
- independent standards of what the system should become
- copy/tone habits that drift from the center

### Treat “I stayed in scope” as one of its main quality signals
For `runner`, obedience to role boundaries is part of competence, not a limitation.

---

## Recommendations for future agent growth

### Near-term default: do not add more durable agents unless the lane proves itself
The current architecture likely only clearly justifies:
- `main`
- `runner`
- ephemeral workers beneath them when needed

A future durable research role might be justified, but only if memo production and source accumulation become frequent enough that a stable bounded continuity layer pays for itself.

### If a research role is added, keep it medium-thin at first
A good research role would have:
- recurring memo patterns
- source handling conventions
- comparison discipline
- no final doctrine-setting authority

It should not become a philosopher-king.

### Editorial/design roles should be delayed until there is actual load
Those lanes are especially vulnerable to gimmickry because they are easy to over-personify and hard to bound.

### Prefer ephemeral specialists before durable departments
A good test sequence is:
1. repeat the task with briefs
2. notice recurring lane shape
3. write a thin operating brief
4. only then consider durable promotion

---

## Practical boundary principles
A compact version that could later become doctrine:

1. **Shared center, differentiated lanes.**
   One system identity; multiple functional roles.

2. **Authority before aesthetics.**
   Define who may decide what before defining tone.

3. **Thin by default.**
   Role thickness must be earned by recurring need.

4. **Promotion over proliferation.**
   Promote a lane to a durable agent only when repetition, residue, and bounded continuity justify it.

5. **Local residue, central settlement.**
   Not all context is shared, but durable state returns to the center.

6. **Escalation is a feature, not a failure.**
   Clean blocked returns preserve coherence.

7. **Review is what keeps one system from splitting into many plausible impostors.**

---

## Risks and failure modes

### Risk 1: Department cosplay
Many named agents, little real boundary.

Result:
complexity without structural gain.

### Risk 2: Hidden sovereignty
A subordinate role starts making future-shaping decisions because nobody notices it crossed the line.

Result:
doctrine drift.

### Risk 3: Identity sharding
Each role develops its own tone, assumptions, and memory canon.

Result:
the system stops feeling like one mind with distributed labor.

### Risk 4: Tool collapse
In trying to avoid fragmentation, every role is flattened into a voiceless utility.

Result:
loss of judgment texture, weak handoff quality, and bland artifacts.

### Risk 5: Context oversharing
Every role gets all memory and all priorities.

Result:
roles become indistinguishable and over-contaminated.

### Risk 6: Structure overhead exceeds value
Too much time spent routing, staffing, or managing lanes.

Result:
the architecture becomes bureaucracy.

---

## Bottom line
The right model for this system is **not** “many personalities.”
It is also **not** “one generic assistant wearing different hats.”

It is closer to:

- one coherent center of identity, judgment, and continuity
- several bounded labor lanes
- real differences in authority/context/tools/artifact ownership
- thin role identity for most departments
- strong review and promotion paths back to the center

That preserves coherence without flattening everything into tool calls, and preserves differentiation without turning the machine room into a puppet cast.

---

## Notes on sources
Grounding for this memo came primarily from local foundry architecture notes, especially:
- `notes/multi-agent-role-architecture-brief.md`
- `notes/openclaw-agent-topology-brief.md`
- `notes/execution-agent-operating-brief.md`
- `notes/runner-first-test-decision-state.md`
- `notes/research-identity-continuity.md`

Two outside references were lightly consulted to sharpen the distinction between centralized orchestration and distributed work:
- Anthropic, *Building Effective Agents* — mainly for orchestrator/worker and evaluator patterns, plus the bias toward simpler structures first.
- Anthropic, *Collective Constitutional AI* — not for topology directly, but as a useful reminder that shared constitutions/norms can be centralized while behavior varies locally.

The conclusions here are still system-specific rather than literature-heavy, which is probably the right shape for this stage.
