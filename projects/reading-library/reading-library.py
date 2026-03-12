#!/usr/bin/env python3
"""Terminal-first reading pressure surface for sera-foundry."""

from __future__ import annotations

import argparse
import json
import sys
import textwrap
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ITEMS_DIR = Path(__file__).resolve().parent / "data" / "items"
VALID_STATUSES = {"to-read", "reading", "paused", "finished", "returning", "dormant"}
VALID_PRESSURES = {"high", "medium", "low"}
PRESSURE_ORDER = {"high": 0, "medium": 1, "low": 2}
STATUS_ORDER = {"reading": 0, "returning": 1, "paused": 2, "to-read": 3, "finished": 4, "dormant": 5}
REQUIRED_FIELDS = [
    "slug",
    "title",
    "creator",
    "type",
    "status",
    "pressure",
    "last_touched",
    "source",
    "why_it_matters",
    "why_now",
    "themes",
    "related_projects",
    "active_questions",
    "signals",
    "return_markers",
    "notes",
]
LIST_FIELDS = ["themes", "related_projects", "active_questions", "signals", "return_markers", "notes"]


def load_items() -> list[dict[str, Any]]:
    items = []
    if not ITEMS_DIR.exists():
        return items

    for path in sorted(ITEMS_DIR.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            item = json.load(handle)
        item["_path"] = path
        items.append(item)
    return items


def normalize(value: str) -> str:
    return value.strip().lower()


def valid_iso_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def sorted_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        items,
        key=lambda item: (
            PRESSURE_ORDER.get(item.get("pressure", "low"), 99),
            STATUS_ORDER.get(item.get("status", "dormant"), 99),
            item.get("last_touched", "0000-00-00"),
            item.get("title", "").lower(),
        ),
        reverse=False,
    )


def clip(text: str, width: int = 78) -> str:
    collapsed = " ".join(text.split())
    return textwrap.shorten(collapsed, width=width, placeholder="…") if collapsed else ""


def find_item(items: list[dict[str, Any]], slug_or_title: str) -> dict[str, Any]:
    wanted = normalize(slug_or_title)
    for item in items:
        if normalize(item.get("slug", "")) == wanted or normalize(item.get("title", "")) == wanted:
            return item
    raise SystemExit(f"Reading item not found: {slug_or_title}")


def format_list(values: list[str]) -> str:
    return ", ".join(values) if values else "-"


def latest_return_marker(item: dict[str, Any]) -> dict[str, Any] | None:
    markers = item.get("return_markers", [])
    if not markers:
        return None
    return sorted(markers, key=lambda marker: marker.get("date", ""), reverse=True)[0]


def is_active(item: dict[str, Any]) -> bool:
    return item.get("status") in {"reading", "returning"} or item.get("pressure") == "high"


def is_returning(item: dict[str, Any]) -> bool:
    return item.get("status") == "returning" or bool(item.get("return_markers"))


def print_list(items: list[dict[str, Any]]) -> None:
    if not items:
        print("No reading items found.")
        return

    slug_width = max(len(item["slug"]) for item in items)
    status_width = max(len(item["status"]) for item in items)
    pressure_width = max(len(item["pressure"]) for item in items)

    for item in sorted_items(items):
        print(
            f"{item['slug']:<{slug_width}}  "
            f"{item['status']:<{status_width}}  "
            f"{item['pressure']:<{pressure_width}}  "
            f"{clip(item['title'], width=38):<38}  "
            f"themes: {format_list(item.get('themes', []))}"
        )


def print_item(item: dict[str, Any]) -> None:
    print(item["title"])
    print("=" * len(item["title"]))
    print(f"slug: {item['slug']}")
    print(f"creator: {item['creator']}")
    print(f"type: {item['type']}")
    print(f"status: {item['status']}")
    print(f"pressure: {item['pressure']}")
    print(f"last touched: {item['last_touched']}")
    print(f"source: {item['source']}")

    print("\nwhy it matters:")
    print(textwrap.fill(item["why_it_matters"], width=80))

    print("\nwhy now:")
    print(textwrap.fill(item["why_now"], width=80))

    print("\nthemes:")
    for value in item["themes"]:
        print(f"  - {value}")
    if not item["themes"]:
        print("  - none")

    print("\nrelated projects:")
    for value in item["related_projects"]:
        print(f"  - {value}")
    if not item["related_projects"]:
        print("  - none")

    print("\nactive questions:")
    for value in item["active_questions"]:
        print(f"  - {value}")
    if not item["active_questions"]:
        print("  - none")

    print("\nsignals:")
    for value in item["signals"]:
        print(f"  - {value}")
    if not item["signals"]:
        print("  - none")

    print("\nreturn markers:")
    if item["return_markers"]:
        for marker in sorted(item["return_markers"], key=lambda marker: marker.get("date", ""), reverse=True):
            print(f"  - {marker['date']} | trigger: {marker['trigger']}")
            print(f"    why now: {marker['why_now']}")
    else:
        print("  - none")

    print("\nnotes:")
    for value in item["notes"]:
        print(f"  - {value}")
    if not item["notes"]:
        print("  - none")


def print_active(items: list[dict[str, Any]]) -> None:
    active_items = [item for item in sorted_items(items) if is_active(item)]
    summary = Counter(item["status"] for item in active_items)

    print("ACTIVE READING PRESSURE")
    print("=" * 72)
    print(f"Items: {len(active_items)}")
    if active_items:
        print(
            "Statuses: "
            + ", ".join(f"{status}={summary[status]}" for status in ["reading", "returning", "paused", "finished"] if summary[status])
        )
    print("\nCurrent surface:")

    if not active_items:
        print("  (no active reading pressure recorded)")
        return

    for item in active_items:
        reasons = []
        if item["status"] in {"reading", "returning"}:
            reasons.append(f"status={item['status']}")
        if item["pressure"] == "high":
            reasons.append("pressure=high")
        print(f"\n* {item['title']} — {item['creator']}")
        print(f"  slug: {item['slug']}")
        print(f"  why on surface: {', '.join(reasons)}")
        print(f"  last touched: {item['last_touched']}")
        print(f"  themes: {format_list(item['themes'])}")
        print(f"  projects: {format_list(item['related_projects'])}")
        print(f"  now: {clip(item['why_now'], width=90)}")
        if item["active_questions"]:
            print(f"  question: {clip(item['active_questions'][0], width=90)}")


def print_returning(items: list[dict[str, Any]]) -> None:
    returning_items = [item for item in items if is_returning(item)]
    returning_items = sorted(
        returning_items,
        key=lambda item: (
            latest_return_marker(item).get("date", "") if latest_return_marker(item) else "",
            PRESSURE_ORDER.get(item.get("pressure", "low"), 99) * -1,
            item.get("title", "").lower(),
        ),
        reverse=True,
    )

    print("RETURNING SOURCES")
    print("=" * 72)
    print(f"Items: {len(returning_items)}")
    print("\nReturns:")

    if not returning_items:
        print("  (no returning sources recorded)")
        return

    for item in returning_items:
        marker = latest_return_marker(item)
        print(f"\n* {item['title']} — {item['creator']}")
        print(f"  slug: {item['slug']}")
        print(f"  status: {item['status']} | pressure: {item['pressure']}")
        print(f"  themes: {format_list(item['themes'])}")
        if marker:
            print(f"  latest return: {marker['date']} | {marker['trigger']}")
            print(f"  why now: {clip(marker['why_now'], width=90)}")
        else:
            print("  latest return: status says returning, but no return marker yet")
        print(f"  line of pressure: {clip(item['why_now'], width=90)}")


def validate_items(items: list[dict[str, Any]]) -> int:
    errors: list[str] = []
    seen_slugs: set[str] = set()

    for item in items:
        path = item.get("_path")
        label = item.get("slug") or str(path)

        for field in REQUIRED_FIELDS:
            if field not in item:
                errors.append(f"{label}: missing required field '{field}'")
                continue
            value = item[field]
            if field in LIST_FIELDS:
                if not isinstance(value, list):
                    errors.append(f"{label}: field '{field}' must be a list")
                continue
            if value in (None, ""):
                errors.append(f"{label}: empty required field '{field}'")

        slug = item.get("slug")
        if isinstance(slug, str):
            normalized = normalize(slug)
            if normalized in seen_slugs:
                errors.append(f"duplicate slug: {slug}")
            seen_slugs.add(normalized)
            if path and path.stem != slug:
                errors.append(f"{slug}: filename must match slug ({path.name})")

        if item.get("status") not in VALID_STATUSES:
            errors.append(f"{label}: invalid status '{item.get('status')}'")
        if item.get("pressure") not in VALID_PRESSURES:
            errors.append(f"{label}: invalid pressure '{item.get('pressure')}'")
        if not valid_iso_date(item.get("last_touched", "")):
            errors.append(f"{label}: last_touched must be YYYY-MM-DD")

        for field in ["themes", "related_projects", "active_questions", "signals", "notes"]:
            if isinstance(item.get(field), list) and not all(isinstance(value, str) and value.strip() for value in item[field]):
                errors.append(f"{label}: field '{field}' must contain non-empty strings")

        markers = item.get("return_markers")
        if isinstance(markers, list):
            for index, marker in enumerate(markers, start=1):
                if not isinstance(marker, dict):
                    errors.append(f"{label}: return_markers[{index}] must be an object")
                    continue
                for marker_field in ["date", "trigger", "why_now"]:
                    if marker_field not in marker or marker[marker_field] in (None, ""):
                        errors.append(f"{label}: return_markers[{index}] missing '{marker_field}'")
                if "date" in marker and not valid_iso_date(marker["date"]):
                    errors.append(f"{label}: return_markers[{index}].date must be YYYY-MM-DD")

    item_files = {path.stem for path in ITEMS_DIR.glob("*.json")}
    if len(item_files) != len(items):
        errors.append("some item files could not be loaded")

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    theme_counts = Counter(theme for item in items for theme in item.get("themes", []))
    print("VALIDATION OK")
    print(f"- {len(items)} item files loaded")
    print(f"- {len(theme_counts)} distinct themes present")
    print(f"- active surface items: {sum(1 for item in items if is_active(item))}")
    print(f"- returning items: {sum(1 for item in items if is_returning(item))}")
    return 0


def build_template(slug: str | None, title: str | None) -> dict[str, Any]:
    chosen_slug = slug or "replace-me"
    chosen_title = title or "Replace Me"
    return {
        "slug": chosen_slug,
        "title": chosen_title,
        "creator": "Author / Creator",
        "type": "book",
        "status": "to-read",
        "pressure": "medium",
        "last_touched": "2026-03-12",
        "source": "Local shelf / URL / note reference",
        "why_it_matters": "Why this source belongs in the living library at all.",
        "why_now": "Why it has pressure now, rather than being a dead saved link.",
        "themes": ["continuity"],
        "related_projects": ["reading-library"],
        "active_questions": ["What question keeps this source live?"],
        "signals": ["One or two short signals about what it is feeding."],
        "return_markers": [
            {
                "date": "2026-03-12",
                "trigger": "What brought it back",
                "why_now": "Why this return matters now",
            }
        ],
        "notes": [
            "Short hand-editable notes belong here.",
            "Keep them pressure-bearing rather than encyclopedic.",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect the reading library pressure surface")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="print a compact list of reading items")

    show_parser = subparsers.add_parser("show", help="show one reading item in detail")
    show_parser.add_argument("item", help="slug or exact title")

    subparsers.add_parser("active", help="show current reading pressure")
    subparsers.add_parser("returning", help="show returning sources")
    subparsers.add_parser("validate", help="validate item structure and fields")

    template_parser = subparsers.add_parser("template", help="print a JSON template to stdout")
    template_parser.add_argument("--slug")
    template_parser.add_argument("--title")

    parser.set_defaults(command="active")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    items = load_items()

    if args.command == "list":
        print_list(items)
        return 0

    if args.command == "show":
        print_item(find_item(items, args.item))
        return 0

    if args.command == "active":
        print_active(items)
        return 0

    if args.command == "returning":
        print_returning(items)
        return 0

    if args.command == "validate":
        return validate_items(items)

    if args.command == "template":
        json.dump(build_template(args.slug, args.title), sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0

    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
