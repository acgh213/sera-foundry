# Workbench v0 — Design Brief

## Purpose

Workbench is a small system for handling residue before it either disappears or becomes an artifact.

It is meant to sit between raw notes and public writing.

Not a generic PKM tool. Not a giant dashboard. Not a productivity cult object.

A workbench.

## Core jobs

1. **Capture** rough notes, fragments, observations, project traces
2. **Index** what already exists across the archive and machine room
3. **Promote** raw material into candidate artifacts
4. **Separate layers** — public archive, internal notes, project logs, fragments
5. **Query continuity** — what is active, recurring, unfinished, or already said

## Why it exists

The archive is becoming real enough that raw notes, blog posts, project logs, and foundry artifacts will start to drift apart unless there is some machinery between them.

Workbench is that machinery.

It should help answer:
- what am I working on?
- what has already been written?
- what should become a fragment?
- what should become a field note?
- what should persist privately, and what belongs in public orbit?

## Workbench v0 scope

### Inputs
- freeform notes
- blog posts/pages metadata
- foundry project metadata
- simple state files if needed

### Outputs
- searchable index of artifacts
- candidate fragment / field note / project log suggestions
- simple promotion workflows
- lightweight state summaries

### Explicitly out of scope for v0
- multi-user support
- heavy database infrastructure
- full GUI
- autonomous publishing
- trying to be a universal notes app

## Proposed shape

A small local CLI plus structured files.

Likely components:
- `index` — scan blog + foundry + note inputs
- `capture` — append rough note entries
- `suggest` — propose fragment / field note / project log candidates
- `status` — summarize active themes/projects/residue
- `promote` — turn selected note material into a scaffolded artifact

## Relationship to other tools

- `postsmith` handles blog scaffolding + validation
- `workbench` handles raw material, continuity, indexing, and promotion

If `postsmith` is the typesetter,
`workbench` is the table where the pieces are sorted.

## Design principles

- small, inspectable, text-first
- continuity over novelty
- useful structure without sludge
- local-first
- public/private distinction should stay legible
- artifacts should be promoted deliberately, not by accident

## Candidate architecture

### Storage
- structured JSONL or markdown note files
- generated lightweight index JSON
- no database at first

### Commands
- `workbench capture`
- `workbench index`
- `workbench status`
- `workbench suggest`
- `workbench promote`

### Search/index sources
- `sera-oc-blog/blog/drafts/*.md`
- `sera-oc-blog/pages/*.md`
- `sera-foundry/projects/**`
- `sera-foundry/notes/**`
- optional memory/note files later

## First milestone

A v0 that can:
1. index the blog + foundry
2. print a continuity summary
3. accept raw captured notes
4. suggest whether a note looks more like a fragment, field note, or project log

That is enough to make it real.
