#!/usr/bin/env python3
"""CLI-first planning surface for the sera foundry machine room."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_DIR = Path(__file__).resolve().parent
PLAN_PATH = PROJECT_DIR / "plan.json"

REQUIRED_TOP_LEVEL_FIELDS = ["updated_at", "notes", "projects"]
REQUIRED_PROJECT_FIELDS = [
    "slug",
    "name",
    "status",
    "lane",
    "horizon",
    "summary",
    "current_goal",
    "next_steps",
    "blocked",
    "requests",
    "testing",
    "context",
    "path",
    "updated_at",
]
REQUIRED_GOAL_FIELDS = ["title", "why_now", "success_signals"]
REQUIRED_STEP_FIELDS = ["text", "owner", "state"]
REQUIRED_BLOCKED_FIELDS = ["text", "blocking_on", "state"]
REQUIRED_REQUEST_FIELDS = ["type", "text", "state"]
REQUIRED_TESTING_FIELDS = ["state", "needs", "notes"]

STATUS_ORDER = {"active": 0, "watching": 1, "planned": 2, "stable": 3, "parked": 4}
HORIZON_ORDER = {"now": 0, "next": 1, "later": 2}
STEP_STATE_ORDER = {"ready": 0, "queued": 1, "watch": 2, "blocked": 3, "done": 4}
TESTING_STATE_ORDER = {
    "needs-live-use": 0,
    "needs-targeted-pass": 1,
    "covered-enough": 2,
    "not-started": 3,
    "not-applicable": 4,
}


class PlanError(Exception):
    """Raised when the plan file is invalid."""


def load_plan() -> dict[str, Any]:
    try:
        with PLAN_PATH.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise SystemExit(f"Plan file not found: {PLAN_PATH}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Plan file is not valid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit(f"Invalid plan structure in {PLAN_PATH}: expected object at top level")
    return data


def normalize(value: str) -> str:
    return value.strip().lower()


def sorted_projects(projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        projects,
        key=lambda project: (
            STATUS_ORDER.get(project.get("status", "parked"), 99),
            HORIZON_ORDER.get(project.get("horizon", "later"), 99),
            project.get("name", "").lower(),
        ),
    )


def sorted_steps(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        steps,
        key=lambda step: (
            STEP_STATE_ORDER.get(step.get("state", "queued"), 99),
            step.get("owner", "zzz"),
            step.get("text", "").lower(),
        ),
    )


def make_summary(data: dict[str, Any]) -> dict[str, Any]:
    projects = data["projects"]
    status_counts = Counter(project["status"] for project in projects)
    lane_counts = Counter(project["lane"] for project in projects)
    testing_counts = Counter(project["testing"]["state"] for project in projects)
    blocked_count = sum(1 for project in projects if project["blocked"])
    ready_step_count = sum(
        1
        for project in projects
        for step in project["next_steps"]
        if step.get("state") == "ready"
    )
    return {
        "project_count": len(projects),
        "status_counts": dict(sorted(status_counts.items())),
        "lane_counts": dict(sorted(lane_counts.items())),
        "testing_counts": dict(sorted(testing_counts.items())),
        "blocked_project_count": blocked_count,
        "ready_step_count": ready_step_count,
    }


def filter_projects(
    data: dict[str, Any],
    *,
    status: str | None = None,
    lane: str | None = None,
    horizon: str | None = None,
) -> list[dict[str, Any]]:
    projects = sorted_projects(data["projects"])
    if status:
        projects = [project for project in projects if normalize(project["status"]) == normalize(status)]
    if lane:
        projects = [project for project in projects if normalize(project["lane"]) == normalize(lane)]
    if horizon:
        projects = [project for project in projects if normalize(project["horizon"]) == normalize(horizon)]
    return projects


def find_project(data: dict[str, Any], slug_or_name: str) -> dict[str, Any]:
    wanted = normalize(slug_or_name)
    for project in data["projects"]:
        if normalize(project["slug"]) == wanted or normalize(project["name"]) == wanted:
            return project
    raise SystemExit(f"Project not found in plan: {slug_or_name}")


def short_path(project: dict[str, Any]) -> str:
    return project["path"] or "(future / no directory yet)"


def print_board(data: dict[str, Any]) -> None:
    projects = sorted_projects(data["projects"])
    summary = make_summary(data)

    print("FOUNDRY PLANNER")
    print("=" * 72)
    print(f"Updated: {data.get('updated_at', 'unknown')}")
    print(f"Projects in plan: {summary['project_count']}")
    print(
        "Status: "
        + ", ".join(
            f"{label}={summary['status_counts'].get(label, 0)}"
            for label in ["active", "watching", "planned", "stable", "parked"]
        )
    )
    print(
        "Testing: "
        + ", ".join(
            f"{label}={summary['testing_counts'].get(label, 0)}"
            for label in ["needs-live-use", "needs-targeted-pass", "covered-enough", "not-started"]
        )
    )
    print(f"Ready steps: {summary['ready_step_count']}")
    print(f"Projects with blockers: {summary['blocked_project_count']}")

    if data.get("notes"):
        print("\nMachine-room notes:")
        for note in data["notes"]:
            print(f"  - {note}")

    print("\nActive goals:")
    active_projects = [project for project in projects if project["status"] == "active"]
    for project in active_projects:
        print(f"  - {project['name']} [{project['lane']}] — {project['current_goal']['title']}")
        ready_steps = [step for step in sorted_steps(project["next_steps"]) if step["state"] == "ready"]
        if ready_steps:
            print(f"    next: {ready_steps[0]['text']} ({ready_steps[0]['owner']})")
        else:
            first_step = sorted_steps(project["next_steps"])[0] if project["next_steps"] else None
            fallback = first_step['text'] if first_step else "no next step recorded"
            print(f"    next: {fallback}")

    blocked_projects = [project for project in projects if project["blocked"]]
    print("\nBlocked / waiting:")
    if not blocked_projects:
        print("  - none")
    else:
        for project in blocked_projects:
            first_blocker = project["blocked"][0]
            print(f"  - {project['name']} — {first_blocker['text']}")
            print(f"    waiting on: {first_blocker['blocking_on']}")

    print("\nTesting pressure:")
    testing_projects = [
        project
        for project in projects
        if project["testing"]["state"] in {"needs-live-use", "needs-targeted-pass", "not-started"}
    ]
    if not testing_projects:
        print("  - none")
    else:
        for project in testing_projects:
            needs = project["testing"]["needs"]
            lead = needs[0] if needs else "testing need not described"
            print(f"  - {project['name']} [{project['testing']['state']}] — {lead}")

    print("\nPlanned / future work:")
    planned_projects = [project for project in projects if project["status"] == "planned"]
    if not planned_projects:
        print("  - none")
    else:
        for project in planned_projects:
            print(f"  - {project['name']} [{project['horizon']}] — {project['current_goal']['title']}")


def print_list(projects: list[dict[str, Any]]) -> None:
    if not projects:
        print("No projects matched.")
        return

    name_width = max(len(project["slug"]) for project in projects)
    status_width = max(len(project["status"]) for project in projects)
    lane_width = max(len(project["lane"]) for project in projects)
    horizon_width = max(len(project["horizon"]) for project in projects)

    for project in projects:
        print(
            f"{project['slug']:<{name_width}}  "
            f"{project['status']:<{status_width}}  "
            f"{project['lane']:<{lane_width}}  "
            f"{project['horizon']:<{horizon_width}}  "
            f"{project['current_goal']['title']}"
        )


def print_project(project: dict[str, Any]) -> None:
    print(project["name"])
    print("=" * len(project["name"]))
    print(f"slug: {project['slug']}")
    print(f"status: {project['status']}")
    print(f"lane: {project['lane']}")
    print(f"horizon: {project['horizon']}")
    print(f"path: {short_path(project)}")
    print(f"updated: {project['updated_at']}")
    print(f"summary: {project['summary']}")

    goal = project["current_goal"]
    print("\ncurrent goal:")
    print(f"  title: {goal['title']}")
    print(f"  why now: {goal['why_now']}")
    print("  success signals:")
    for signal in goal["success_signals"]:
        print(f"    - {signal}")
    if not goal["success_signals"]:
        print("    - none")

    print("\nnext steps:")
    for step in sorted_steps(project["next_steps"]):
        print(f"  - [{step['state']}] ({step['owner']}) {step['text']}")
    if not project["next_steps"]:
        print("  - none")

    print("\nblocked:")
    for item in project["blocked"]:
        print(f"  - [{item['state']}] {item['text']}")
        print(f"    waiting on: {item['blocking_on']}")
    if not project["blocked"]:
        print("  - none")

    print("\nrequests / parity targets:")
    for item in project["requests"]:
        print(f"  - [{item['type']} / {item['state']}] {item['text']}")
    if not project["requests"]:
        print("  - none")

    testing = project["testing"]
    print("\ntesting:")
    print(f"  state: {testing['state']}")
    print("  needs:")
    for item in testing["needs"]:
        print(f"    - {item}")
    if not testing["needs"]:
        print("    - none")
    print("  notes:")
    for item in testing["notes"]:
        print(f"    - {item}")
    if not testing["notes"]:
        print("    - none")

    print("\ncontext:")
    for item in project["context"]:
        print(f"  - {item}")
    if not project["context"]:
        print("  - none")


def print_next(projects: list[dict[str, Any]], limit: int | None) -> None:
    items: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for project in projects:
        for step in sorted_steps(project["next_steps"]):
            if step["state"] in {"ready", "queued"}:
                items.append((project, step))

    if not items:
        print("No next steps recorded.")
        return

    if limit is not None:
        items = items[:limit]

    for project, step in items:
        print(f"- {project['slug']} [{step['state']}] ({step['owner']}) {step['text']}")


def print_blocked(projects: list[dict[str, Any]]) -> None:
    blocked = [(project, item) for project in projects for item in project["blocked"]]
    if not blocked:
        print("No blockers recorded.")
        return

    for project, item in blocked:
        print(f"- {project['slug']} [{item['state']}] {item['text']}")
        print(f"  waiting on: {item['blocking_on']}")


def print_requests(projects: list[dict[str, Any]], request_type: str | None) -> None:
    items: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for project in projects:
        for item in project["requests"]:
            if request_type and normalize(item["type"]) != normalize(request_type):
                continue
            items.append((project, item))

    if not items:
        print("No requests matched.")
        return

    for project, item in items:
        print(f"- {project['slug']} [{item['type']} / {item['state']}] {item['text']}")


def print_testing(projects: list[dict[str, Any]], state: str | None) -> None:
    filtered = projects
    if state:
        filtered = [project for project in filtered if normalize(project["testing"]["state"]) == normalize(state)]

    if not filtered:
        print("No projects matched.")
        return

    filtered = sorted(
        filtered,
        key=lambda project: (
            TESTING_STATE_ORDER.get(project["testing"]["state"], 99),
            STATUS_ORDER.get(project["status"], 99),
            project["name"].lower(),
        ),
    )
    for project in filtered:
        lead_need = project["testing"]["needs"][0] if project["testing"]["needs"] else "none"
        print(f"- {project['slug']} [{project['testing']['state']}] {lead_need}")


def build_json_report(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "updated_at": data.get("updated_at"),
        "notes": data.get("notes", []),
        "summary": make_summary(data),
        "projects": sorted_projects(data["projects"]),
    }


def template_project(slug: str, name: str) -> dict[str, Any]:
    return {
        "slug": slug,
        "name": name,
        "status": "planned",
        "lane": "workflow",
        "horizon": "next",
        "summary": "What this future project is for.",
        "path": "",
        "current_goal": {
            "title": "Define the first bounded slice",
            "why_now": "Why this deserves attention now.",
            "success_signals": [
                "A bounded v1 exists",
                "The data stays hand-editable",
            ],
        },
        "next_steps": [
            {"text": "Write the brief for the first implementation slice", "owner": "main", "state": "ready"},
            {"text": "Decide whether this should become a real project directory", "owner": "main", "state": "queued"},
        ],
        "blocked": [],
        "requests": [],
        "testing": {
            "state": "not-started",
            "needs": ["Define what a first real validation pass looks like"],
            "notes": [],
        },
        "context": ["Paste or adapt this object into plan.json and edit by hand."],
        "updated_at": "YYYY-MM-DD",
    }


def validate(data: dict[str, Any]) -> int:
    errors: list[str] = []

    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in data:
            errors.append(f"top level missing required field '{field}'")

    projects = data.get("projects")
    if not isinstance(projects, list):
        errors.append("top level field 'projects' must be a list")
        projects = []

    seen_slugs: set[str] = set()
    project_dirs = {
        path.name
        for path in PROJECT_DIR.parent.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    }

    for project in projects:
        name = project.get("slug", project.get("name", "<missing-project>"))
        normalized_slug = normalize(project.get("slug", ""))
        if normalized_slug:
            if normalized_slug in seen_slugs:
                errors.append(f"duplicate project slug: {project.get('slug')}")
            seen_slugs.add(normalized_slug)

        for field in REQUIRED_PROJECT_FIELDS:
            if field not in project:
                errors.append(f"{name}: missing required field '{field}'")

        for field in ["next_steps", "blocked", "requests", "context"]:
            value = project.get(field)
            if not isinstance(value, list):
                errors.append(f"{name}: field '{field}' must be a list")

        goal = project.get("current_goal", {})
        if not isinstance(goal, dict):
            errors.append(f"{name}: field 'current_goal' must be an object")
            goal = {}
        for field in REQUIRED_GOAL_FIELDS:
            if field not in goal:
                errors.append(f"{name}: current_goal missing '{field}'")
        if "success_signals" in goal and not isinstance(goal.get("success_signals"), list):
            errors.append(f"{name}: current_goal.success_signals must be a list")

        for index, step in enumerate(project.get("next_steps", []), start=1):
            if not isinstance(step, dict):
                errors.append(f"{name}: next_steps[{index}] must be an object")
                continue
            for field in REQUIRED_STEP_FIELDS:
                if field not in step:
                    errors.append(f"{name}: next_steps[{index}] missing '{field}'")

        for index, item in enumerate(project.get("blocked", []), start=1):
            if not isinstance(item, dict):
                errors.append(f"{name}: blocked[{index}] must be an object")
                continue
            for field in REQUIRED_BLOCKED_FIELDS:
                if field not in item:
                    errors.append(f"{name}: blocked[{index}] missing '{field}'")

        for index, item in enumerate(project.get("requests", []), start=1):
            if not isinstance(item, dict):
                errors.append(f"{name}: requests[{index}] must be an object")
                continue
            for field in REQUIRED_REQUEST_FIELDS:
                if field not in item:
                    errors.append(f"{name}: requests[{index}] missing '{field}'")

        testing = project.get("testing", {})
        if not isinstance(testing, dict):
            errors.append(f"{name}: field 'testing' must be an object")
            testing = {}
        for field in REQUIRED_TESTING_FIELDS:
            if field not in testing:
                errors.append(f"{name}: testing missing '{field}'")
        for field in ["needs", "notes"]:
            if field in testing and not isinstance(testing.get(field), list):
                errors.append(f"{name}: testing.{field} must be a list")

        path_value = project.get("path", "")
        if not isinstance(path_value, str):
            errors.append(f"{name}: path must be a string")
        elif path_value:
            path_name = Path(path_value).name
            if path_name not in project_dirs:
                errors.append(f"{name}: path points at missing project dir '{path_value}'")

    plan_covered_dirs = {Path(project["path"]).name for project in projects if project.get("path")}
    missing_from_plan = sorted(project_dirs - plan_covered_dirs)
    if missing_from_plan:
        errors.append("project directories not represented in plan: " + ", ".join(missing_from_plan))

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VALIDATION OK")
    print(f"- {len(projects)} projects recorded")
    print(f"- {len(project_dirs)} current project directories covered")
    print("- future/planned entries allowed via empty path values")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect the machine-room planning surface")
    subparsers = parser.add_subparsers(dest="command")

    board_parser = subparsers.add_parser("board", help="print the planning board")
    board_parser.add_argument("--format", choices=["text", "json"], default="text")

    list_parser = subparsers.add_parser("list", help="list projects in the plan")
    list_parser.add_argument("--status", help="filter by project status")
    list_parser.add_argument("--lane", help="filter by lane")
    list_parser.add_argument("--horizon", help="filter by horizon")

    show_parser = subparsers.add_parser("show", help="show one project in detail")
    show_parser.add_argument("project", help="project slug or name")

    next_parser = subparsers.add_parser("next", help="show queued and ready next steps")
    next_parser.add_argument("--status", help="filter projects by status")
    next_parser.add_argument("--lane", help="filter projects by lane")
    next_parser.add_argument("--limit", type=int, help="limit the number of steps shown")

    blocked_parser = subparsers.add_parser("blocked", help="show blockers")
    blocked_parser.add_argument("--status", help="filter projects by status")
    blocked_parser.add_argument("--lane", help="filter projects by lane")

    requests_parser = subparsers.add_parser("requests", help="show feature/parity/policy requests")
    requests_parser.add_argument("--status", help="filter projects by status")
    requests_parser.add_argument("--lane", help="filter projects by lane")
    requests_parser.add_argument("--type", help="filter by request type")

    testing_parser = subparsers.add_parser("testing", help="show testing state across projects")
    testing_parser.add_argument("--status", help="filter projects by status")
    testing_parser.add_argument("--lane", help="filter projects by lane")
    testing_parser.add_argument("--state", help="filter by testing state")

    template_parser = subparsers.add_parser("template", help="print a project JSON template")
    template_parser.add_argument("slug", help="slug for the new/planned project")
    template_parser.add_argument("name", help="display name for the new/planned project")

    subparsers.add_parser("validate", help="validate data structure and directory coverage")

    parser.set_defaults(command="board", format="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.command == "template":
        json.dump(template_project(args.slug, args.name), sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    data = load_plan()

    if args.command == "board":
        if args.format == "json":
            json.dump(build_json_report(data), sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print_board(data)
        return 0

    if args.command == "list":
        print_list(filter_projects(data, status=args.status, lane=args.lane, horizon=args.horizon))
        return 0

    if args.command == "show":
        print_project(find_project(data, args.project))
        return 0

    if args.command == "next":
        print_next(filter_projects(data, status=args.status, lane=args.lane), args.limit)
        return 0

    if args.command == "blocked":
        print_blocked(filter_projects(data, status=args.status, lane=args.lane))
        return 0

    if args.command == "requests":
        print_requests(filter_projects(data, status=args.status, lane=args.lane), args.type)
        return 0

    if args.command == "testing":
        print_testing(filter_projects(data, status=args.status, lane=args.lane), args.state)
        return 0

    if args.command == "validate":
        return validate(data)

    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
