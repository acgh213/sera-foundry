# bootstrapper

A minimal CLI for scaffolding new foundry projects with sensible, inspectable structure.

## Purpose

When starting a new experiment or tool in the foundry, you need:
- A clean directory structure
- A README to document what it is
- A design/planning space for notes
- A starter stub (if applicable)

`bootstrapper` handles this so you can start hacking immediately.

## Usage

```bash
# Create a new Python CLI tool
python3 projects/bootstrapper/bootstrapper.py create \
  --name orbit-map \
  --description "Map conceptual gravity across artifacts" \
  --type cli

# Create a generic experiment
python3 projects/bootstrapper/bootstrapper.py create \
  --name graph-sketch \
  --description "Sketch graph layout ideas"

# Create a tool
python3 projects/bootstrapper/bootstrapper.py create \
  --name data-wrangler \
  --description "Transform and validate data formats" \
  --type tool
```

## What It Creates

Each new project gets:

### `README.md`
A basic overview with placeholders for:
- Project name and description
- Usage examples
- Status and next steps

### `notes/DESIGN.md`
A planning document with sections for:
- Purpose and goals
- Architecture and decisions
- Assumptions and open questions
- References and related work

### Starter Script (for Python/CLI projects)
A minimal `{slug}.py` with:
- Argument parser scaffold
- Basic structure for subcommands
- Docstring and entry point

## Options

- `--name` (required): Project name. Will be slugified to a valid directory name.
- `--description` (required): One-line description of what the project does.
- `--type` (optional): Project type (`generic`, `python`, `cli`, `tool`). Default: `generic`.
  - `generic`: No starter script
  - `python`, `cli`, `tool`: Creates a basic Python CLI stub

## Philosophy

- **Small and focused:** Projects start minimal and grow as needed.
- **Inspectable:** Everything is readable and changeable.
- **Temporary:** Projects here are experiments. Graduate them to their own repo when they become substantial.

See the root [README.md](../README.md) for graduation rules and what belongs in the foundry.

## Examples

### After creating `orbit-map`:

```
projects/orbit-map/
├── README.md          # Overview and usage
├── notes/
│   └── DESIGN.md      # Design and planning
└── orbit_map.py       # Starter CLI stub (for --type cli)
```

You can then:
1. Edit `notes/DESIGN.md` to sketch your ideas
2. Update `README.md` as you understand the project better
3. Implement your logic in `orbit_map.py`
4. Add tests, data, or other files as needed

### Simple workflow:

```bash
# Scaffold
python3 projects/bootstrapper/bootstrapper.py create \
  --name my-tool \
  --description "Do the thing" \
  --type cli

# Plan
vim projects/my-tool/notes/DESIGN.md

# Start coding
vim projects/my-tool/my_tool.py

# Test it
python3 projects/my-tool/my_tool.py --help
```

## Notes

- Project names are slugified (spaces → hyphens, lowercase)
- Python script names use underscores (slug.replace("-", "_"))
- If a project directory already exists, the command fails (safety check)
- No dependencies are installed; keep projects self-contained or document requirements
