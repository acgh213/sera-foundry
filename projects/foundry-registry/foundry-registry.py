#!/usr/bin/env python3
"""Terminal-first project registry for sera-foundry."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = Path(__file__).resolve().with_name("registry.json")
REQUIRED_FIELDS = [
    "name",
    "path",
    "what_it_does",
    "status",
    "dependencies",
    "notes",
    "next_actions",
    "pressure",
]
PRESSURE_ORDER = {"high": 0, "medium": 1, "low": 2}
STATUS_ORDER = {"active": 0, "watching": 1, "stable": 2, "exploratory": 3}


def load_registry() -> dict[str, Any]:
    with REGISTRY_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or "projects" not in data:
        raise SystemExit(f"Invalid registry structure in {REGISTRY_PATH}")
    return data


def normalize_name(value: str) -> str:
    return value.strip().lower()


def sorted_projects(projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        projects,
        key=lambda project: (
            PRESSURE_ORDER.get(project.get("pressure", "low"), 99),
            STATUS_ORDER.get(project.get("status", "exploratory"), 99),
            project.get("name", "").lower(),
        ),
    )


def make_summary(data: dict[str, Any]) -> dict[str, Any]:
    projects = data["projects"]
    pressure_counts = Counter(project["pressure"] for project in projects)
    status_counts = Counter(project["status"] for project in projects)
    return {
        "project_count": len(projects),
        "pressure_counts": dict(sorted(pressure_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "highest_pressure": [p["name"] for p in sorted_projects(projects) if p["pressure"] == "high"],
    }


def print_report(data: dict[str, Any]) -> None:
    projects = sorted_projects(data["projects"])
    summary = make_summary(data)

    print("FOUNDRY PROJECT REGISTRY")
    print("=" * 72)
    print(f"Reviewed: {data.get('reviewed_at', 'unknown')}")
    print(f"Projects: {summary['project_count']}")
    print(
        "Pressure: "
        + ", ".join(f"{level}={summary['pressure_counts'].get(level, 0)}" for level in ["high", "medium", "low"])
    )
    print(
        "Status: "
        + ", ".join(
            f"{status}={summary['status_counts'].get(status, 0)}"
            for status in ["active", "watching", "stable", "exploratory"]
        )
    )
    if data.get("notes"):
        print("\nRegistry notes:")
        for note in data["notes"]:
            print(f"  - {note}")

    print("\nCurrent pressure surface:")
    for project in [project for project in projects if project["pressure"] == "high"]:
        next_step = project["next_actions"][0] if project["next_actions"] else "no next action recorded"
        print(f"  - {project['name']} [{project['status']}] — {project['what_it_does']}")
        print(f"    next: {next_step}")

    print("\nProjects:")
    for project in projects:
        deps = ", ".join(project["dependencies"]) if project["dependencies"] else "none"
        next_step = project["next_actions"][0] if project["next_actions"] else "none recorded"
        print(f"\n* {project['name']}  ({project['status']} / pressure: {project['pressure']})")
        print(f"  path: {project['path']}")
        print(f"  does: {project['what_it_does']}")
        print(f"  deps: {deps}")
        print(f"  next: {next_step}")


def print_list(data: dict[str, Any]) -> None:
    projects = sorted_projects(data["projects"])
    name_width = max(len(project["name"]) for project in projects)
    status_width = max(len(project["status"]) for project in projects)
    pressure_width = max(len(project["pressure"]) for project in projects)

    for project in projects:
        print(
            f"{project['name']:<{name_width}}  "
            f"{project['status']:<{status_width}}  "
            f"{project['pressure']:<{pressure_width}}  "
            f"{project['path']}"
        )


def find_project(data: dict[str, Any], name: str) -> dict[str, Any]:
    wanted = normalize_name(name)
    for project in data["projects"]:
        if normalize_name(project["name"]) == wanted:
            return project
    raise SystemExit(f"Project not found in registry: {name}")


def print_project(project: dict[str, Any]) -> None:
    print(project["name"])
    print("=" * len(project["name"]))
    print(f"path: {project['path']}")
    print(f"status: {project['status']}")
    print(f"pressure: {project['pressure']}")
    print(f"does: {project['what_it_does']}")
    print(f"last reviewed: {project.get('last_reviewed', 'unknown')}")

    print("\ndependencies:")
    for item in project["dependencies"]:
        print(f"  - {item}")
    if not project["dependencies"]:
        print("  - none")

    print("\nnotes:")
    for item in project["notes"]:
        print(f"  - {item}")
    if not project["notes"]:
        print("  - none")

    print("\nnext actions:")
    for item in project["next_actions"]:
        print(f"  - {item}")
    if not project["next_actions"]:
        print("  - none")

    signals = project.get("signals", [])
    if signals:
        print("\nsignals:")
        for item in signals:
            print(f"  - {item}")


def validate(data: dict[str, Any]) -> int:
    errors: list[str] = []
    names_seen: set[str] = set()

    for project in data["projects"]:
        name = project.get("name", "<missing-name>")
        normalized = normalize_name(name)
        if normalized in names_seen:
            errors.append(f"duplicate project name: {name}")
        names_seen.add(normalized)

        for field in REQUIRED_FIELDS:
            if field not in project:
                errors.append(f"{name}: missing required field '{field}'")
                continue
            value = project[field]
            if value in (None, ""):
                errors.append(f"{name}: empty required field '{field}'")
            if field in {"dependencies", "notes", "next_actions"} and not isinstance(value, list):
                errors.append(f"{name}: field '{field}' must be a list")

    project_dirs = {
        path.name
        for path in (ROOT / "projects").iterdir()
        if path.is_dir() and not path.name.startswith(".")
    }
    registry_dirs = {Path(project["path"]).name for project in data["projects"] if project.get("path")}

    missing_from_registry = sorted(project_dirs - registry_dirs)
    unknown_in_registry = sorted(registry_dirs - project_dirs)

    if missing_from_registry:
        errors.append("missing registry entries for: " + ", ".join(missing_from_registry))
    if unknown_in_registry:
        errors.append("registry points at missing project dirs: " + ", ".join(unknown_in_registry))

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VALIDATION OK")
    print(f"- {len(data['projects'])} projects registered")
    print(f"- {len(project_dirs)} project directories covered")
    return 0


def build_json_report(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "reviewed_at": data.get("reviewed_at"),
        "notes": data.get("notes", []),
        "summary": make_summary(data),
        "projects": sorted_projects(data["projects"]),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect the foundry project registry")
    subparsers = parser.add_subparsers(dest="command")

    report_parser = subparsers.add_parser("report", help="print a machine-room summary")
    report_parser.add_argument("--format", choices=["text", "json"], default="text")

    subparsers.add_parser("list", help="print a compact project list")

    show_parser = subparsers.add_parser("show", help="show one project in detail")
    show_parser.add_argument("name", help="project name")

    subparsers.add_parser("validate", help="validate required fields and coverage")

    parser.set_defaults(command="report", format="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = load_registry()

    if args.command == "report":
        if args.format == "json":
            json.dump(build_json_report(data), sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print_report(data)
        return 0

    if args.command == "list":
        print_list(data)
        return 0

    if args.command == "show":
        print_project(find_project(data, args.name))
        return 0

    if args.command == "validate":
        return validate(data)

    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
