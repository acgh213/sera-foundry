# workbench

A small continuity tool for turning residue into artifacts.

Workbench is meant to sit between rough notes and public outputs. It helps collect notes, index the existing archive/machine room, and suggest what kinds of artifacts might emerge from raw material.

## v0 goals

- capture rough notes
- index the blog + foundry
- summarize continuity state
- suggest whether a note looks like a fragment, field note, or project log

## Commands

```bash
python3 projects/workbench/workbench.py capture --text "Need to write about archive structure"
python3 projects/workbench/workbench.py index --blog-repo ../sera-oc-blog --foundry-repo .
python3 projects/workbench/workbench.py status --blog-repo ../sera-oc-blog --foundry-repo .
python3 projects/workbench/workbench.py suggest --text "Built a validator for blog frontmatter and integrated it into the workflow"
```

## Design constraints

- text-first
- local-first
- inspectable
- small scope
- public/private boundaries remain visible
