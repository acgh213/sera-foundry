#!/usr/bin/env python3
"""
bootstrapper — scaffold new foundry projects with minimal, sensible structure.

This tool creates a new project directory under projects/ with:
- README.md (with name, description, usage stubs)
- notes/DESIGN.md (for planning, decisions, context)
- A starter script or stub if applicable

Keep projects small and inspectable. If a project grows into something
substantial, reusable, or independently interesting, graduate it into
its own repository.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path


def slugify(text: str) -> str:
    """Convert text to a valid project name."""
    import re
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9-]+", "-", text)
    return text.strip("-") or "untitled"


def create_project(args):
    """Create a new project directory with minimal scaffolding."""
    name = args.name.strip()
    description = args.description.strip()
    project_type = (args.type or "generic").strip().lower()
    
    if not name:
        raise SystemExit("Project name is required.")
    
    slug = slugify(name)
    base_path = Path(__file__).parent.parent
    project_path = base_path / slug
    
    if project_path.exists():
        raise SystemExit(f"Project directory already exists: {project_path}")
    
    # Create project structure
    project_path.mkdir(parents=True, exist_ok=True)
    notes_path = project_path / "notes"
    notes_path.mkdir(parents=True, exist_ok=True)
    
    # Generate README.md
    readme_content = f"""# {name}

{description}

## Overview

A small, focused tool or experiment living in the foundry.

## Usage

```bash
# TODO: Add usage examples once the project takes shape
```

## Structure

- `notes/DESIGN.md` — planning, decisions, and context
- Project files here (scripts, code, data, etc.)

## Status

Early stage. This project is experimental and may change significantly.

## Next Steps

- Define the core behavior
- Add basic tests if applicable
- Document assumptions and limitations
"""
    
    readme_path = project_path / "README.md"
    readme_path.write_text(readme_content, encoding="utf-8")
    
    # Generate notes/DESIGN.md
    now = datetime.now(timezone.utc).isoformat()
    design_content = f"""# {name} — Design Notes

**Created:** {now}
**Type:** {project_type}

## Purpose

{description}

## Goals

- [ ] Define core behavior
- [ ] Establish minimal scope
- [ ] Keep it inspectable

## Architecture

(Describe the shape of this project. What does it do? How does it do it?)

## Assumptions

(What assumptions are we making? What constraints do we have?)

## Open Questions

(What do we still need to figure out?)

## Decisions

(Record key decisions and why we made them.)

## References

(Links to related projects, inspiration, or dependencies.)
"""
    
    design_path = notes_path / "DESIGN.md"
    design_path.write_text(design_content, encoding="utf-8")
    
    # Create a starter script stub if this looks like a Python project
    if project_type in ("python", "cli", "tool", "generic"):
        stub_name = slug.replace("-", "_")
        stub_path = project_path / f"{stub_name}.py"
        if not stub_path.exists():
            stub_content = f'''#!/usr/bin/env python3
"""
{name} — {description}
"""

from __future__ import annotations

import argparse
import sys


def build_parser():
    """Build argument parser."""
    p = argparse.ArgumentParser(
        description="{description}"
    )
    sub = p.add_subparsers(dest="command")
    
    # TODO: Add subcommands here
    
    return p


def main():
    """Entry point."""
    parser = build_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # TODO: Implement commands


if __name__ == "__main__":
    main()
'''
            stub_path.write_text(stub_content, encoding="utf-8")
            stub_path.chmod(0o755)
    
    print(f"✓ Created project: {project_path}")
    print(f"  - README.md")
    print(f"  - notes/DESIGN.md")
    if project_type in ("python", "cli", "tool", "generic"):
        print(f"  - {stub_name}.py")
    print(f"\nNext: cd {project_path} and start hacking")


def build_parser():
    """Build main argument parser."""
    p = argparse.ArgumentParser(
        description="Scaffold a new foundry project with minimal structure.",
        epilog="Keep projects small, focused, and inspectable."
    )
    sub = p.add_subparsers(dest="command", required=True)
    
    cp = sub.add_parser(
        "create",
        help="Create a new project"
    )
    cp.add_argument(
        "--name",
        required=True,
        help="Project name (will be slugified)"
    )
    cp.add_argument(
        "--description",
        required=True,
        help="Short description of the project"
    )
    cp.add_argument(
        "--type",
        default="generic",
        help="Project type: python, cli, tool, generic (default: generic)"
    )
    cp.set_defaults(func=create_project)
    
    return p


def main():
    """Entry point."""
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
