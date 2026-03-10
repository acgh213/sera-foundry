# dispatch-template

A tiny terminal-first helper that prints a reusable execution-brief scaffold for bounded implementation tasks.

It is intentionally small:

- prints to stdout
- local-only
- standard library only
- no state or tracking system
- no routing or orchestration logic

## Usage

From `sera-foundry/`:

```bash
python3 projects/dispatch-template/dispatch-template.py
```

With a title:

```bash
python3 projects/dispatch-template/dispatch-template.py "cleanup promotion queue"
```

With objective and target hints:

```bash
python3 projects/dispatch-template/dispatch-template.py \
  "dispatch-template CLI" \
  --objective "Build a tiny helper that prints a bounded execution-brief scaffold to stdout." \
  --target "projects/dispatch-template/"
```

If you want a cleaner pasted artifact without a generated timestamp:

```bash
python3 projects/dispatch-template/dispatch-template.py \
  "capture-audit follow-up" \
  --target "projects/capture-audit/" \
  --no-timestamp
```

## What it emits

The scaffold includes sections for:

- objective
- scope
- non-goals
- acceptance criteria
- constraints
- allowed files / directories
- disallowed / protected paths
- allowed tools
- escalation triggers
- verification expectations
- commit / workflow expectation
- output contract
- blocked-state contract

## Intended use

Use it when you want to hand a bounded implementation slice to an execution agent or future-you without rewriting the doctrine from scratch each time.

Typical flow:

1. generate the scaffold
2. paste it into a dispatch or note
3. lightly edit the placeholders and allowlists
4. run the implementation slice
5. verify and review

The tool does **not** track dispatches, make routing decisions, or write to other files by default.

## Sample output

```text
# Dispatch: dispatch-template CLI

Target: `projects/dispatch-template/`

## Objective
Build a tiny helper that prints a bounded execution-brief scaffold to stdout.

## Scope
- Build or change only what is necessary for this slice.
- Keep the implementation narrow, inspectable, and easy to verify.
- Prefer direct edits and obvious behavior over architecture expansion.

## Non-goals
- Do not broaden this into a platform, framework, or orchestration system.
- Do not add speculative features that are not required for the objective.
- Do not rewrite unrelated code or documentation.
```

## Constraints

- terminal-first
- local-only
- standard library only
- narrow scope
- clarity over cleverness
