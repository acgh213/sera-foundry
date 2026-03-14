#!/usr/bin/env python3
"""voice-style-workshop — local archive for charged style fragments.

Preserves sentence pressure, tonal moves, and structural gestures as
hand-editable artifacts rather than reducing style to rules or metrics.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parent
ARCHIVE_DIR = PROJECT_ROOT / "archive"
REQUIRED_FIELDS = ["title", "date", "kind", "status", "pressure", "source"]
VALID_KINDS = {"sentence", "paragraph", "tone", "structure", "anti-pattern", "image", "voice-note"}
VALID_STATUSES = {"fresh", "returning", "core", "held", "retired"}
VALID_PRESSURE = {"alive", "charged", "quiet"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SECTION_HEADERS = {"fragment", "why it works", "return tension", "use with care"}


@dataclass
class Fragment:
    slug: str
    path: Path
    metadata: dict[str, object]
    body: str

    @property
    def title(self) -> str:
        return str(self.metadata.get("title", self.slug))

    @property
    def fragment_date(self) -> str:
        return str(self.metadata.get("date", "") or "")

    @property
    def tags(self) -> list[str]:
        raw = self.metadata.get("tags", [])
        if isinstance(raw, list):
            return [str(tag) for tag in raw]
        return []

    @property
    def returns(self) -> list[str]:
        raw = self.metadata.get("returns", [])
        if isinstance(raw, list):
            return [str(item) for item in raw]
        return []

    @property
    def source(self) -> str:
        return str(self.metadata.get("source", ""))


def parse_scalar(raw: str) -> object:
    value = raw.strip()
    if value == "":
        return ""
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip('"\'') for part in inner.split(",") if part.strip()]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text.strip()

    lines = text.splitlines()
    metadata: dict[str, object] = {}
    body_start = None

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            body_start = index + 1
            break
        if not line.strip() or ":" not in line:
            continue
        key, raw = line.split(":", 1)
        metadata[key.strip()] = parse_scalar(raw)

    if body_start is None:
        return {}, text.strip()

    body = "\n".join(lines[body_start:]).strip()
    return metadata, body


def load_fragment(path: Path) -> Fragment:
    metadata, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    return Fragment(slug=path.stem, path=path, metadata=metadata, body=body)


def iter_fragments() -> Iterable[Fragment]:
    if not ARCHIVE_DIR.exists():
        return []
    fragments = [load_fragment(path) for path in sorted(ARCHIVE_DIR.glob("*.md"))]
    return sorted(fragments, key=lambda fragment: (fragment.fragment_date, fragment.slug), reverse=True)


def render_table(rows: list[list[str]]) -> None:
    widths = [max(len(row[index]) for row in rows) for index in range(len(rows[0]))]
    for row_index, row in enumerate(rows):
        print("  ".join(cell.ljust(widths[index]) for index, cell in enumerate(row)))
        if row_index == 0:
            print("  ".join("-" * width for width in widths))


def clip_text(text: str, width: int = 88) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) <= width:
        return collapsed
    return collapsed[: width - 1].rstrip() + "…"


def split_sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = None

    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            header = stripped[3:].strip().lower()
            if header in SECTION_HEADERS:
                current = header
                sections.setdefault(current, [])
                continue
        if current is not None:
            sections.setdefault(current, []).append(line)

    return {key: "\n".join(value).strip() for key, value in sections.items()}


def fragment_excerpt(fragment: Fragment, width: int = 78) -> str:
    sections = split_sections(fragment.body)
    text = sections.get("fragment") or fragment.body
    return clip_text(text, width=width)


def why_excerpt(fragment: Fragment, width: int = 78) -> str:
    sections = split_sections(fragment.body)
    text = sections.get("why it works", "")
    return clip_text(text, width=width)


def find_fragment(slug: str) -> Fragment:
    path = ARCHIVE_DIR / f"{slug}.md"
    if not path.exists():
        raise SystemExit(f"Fragment not found: {slug}")
    return load_fragment(path)


def cmd_list(_: list[str]) -> int:
    fragments = list(iter_fragments())
    if not fragments:
        print("No style fragments found.")
        return 0

    rows = [["DATE", "KIND", "STATUS", "PRESSURE", "SOURCE", "TAGS", "TITLE", "SLUG"]]
    for fragment in fragments:
        rows.append([
            fragment.fragment_date[:10],
            str(fragment.metadata.get("kind", "")),
            str(fragment.metadata.get("status", "")),
            str(fragment.metadata.get("pressure", "")),
            clip_text(fragment.source, width=30),
            ", ".join(fragment.tags[:3]) if fragment.tags else "-",
            fragment.title,
            fragment.slug,
        ])
    render_table(rows)
    print(f"\n{len(fragments)} fragment(s) in archive.")
    return 0


def cmd_show(args: list[str]) -> int:
    if not args:
        print("Usage: voice-style-workshop show <slug>", file=sys.stderr)
        return 1

    fragment = find_fragment(args[0])
    meta = fragment.metadata
    print(f"Title:      {fragment.title}")
    print(f"Date:       {meta.get('date', '')}")
    print(f"Kind:       {meta.get('kind', '')}")
    print(f"Status:     {meta.get('status', '')}")
    print(f"Pressure:   {meta.get('pressure', '')}")
    print(f"Source:     {fragment.source}")
    if fragment.tags:
        print(f"Tags:       {', '.join(fragment.tags)}")
    if fragment.returns:
        print(f"Returns:    {', '.join(fragment.returns)}")
    print(f"File:       {fragment.path.relative_to(PROJECT_ROOT)}")
    print("\n---\n")
    print(fragment.body)
    return 0


def cmd_returning(_: list[str]) -> int:
    fragments = [
        fragment
        for fragment in iter_fragments()
        if fragment.returns or str(fragment.metadata.get("status", "")) == "returning"
    ]
    if not fragments:
        print("No fragments currently marked as returning.")
        return 0

    fragments = sorted(
        fragments,
        key=lambda fragment: (len(fragment.returns), fragment.fragment_date, fragment.slug),
        reverse=True,
    )

    print("Returning fragments")
    print("===================")
    print()
    for fragment in fragments:
        last_return = fragment.returns[-1] if fragment.returns else "-"
        print(f"- {fragment.title}")
        print(f"  date:         {fragment.fragment_date[:10]}")
        print(f"  kind:         {fragment.metadata.get('kind', '')}")
        print(f"  status:       {fragment.metadata.get('status', '')}")
        print(f"  source:       {fragment.source}")
        print(f"  returns:      {len(fragment.returns)} marker(s); last return {last_return}")
        print(f"  tags:         {', '.join(fragment.tags) if fragment.tags else '-'}")
        print(f"  fragment:     {fragment_excerpt(fragment, width=70)}")
        why = why_excerpt(fragment, width=70)
        if why:
            print(f"  why alive:    {why}")
        print(f"  slug:         {fragment.slug}")
        print()
    return 0


def cmd_by_tag(args: list[str]) -> int:
    if not args:
        print("Usage: voice-style-workshop by-tag <tag>", file=sys.stderr)
        return 1

    wanted = args[0].strip().lower()
    matches = [fragment for fragment in iter_fragments() if any(tag.lower() == wanted for tag in fragment.tags)]
    if not matches:
        print(f"No fragments found for tag: {args[0]}")
        return 0

    print(f"Fragments tagged '{args[0]}' ({len(matches)})")
    print("=" * (len(args[0]) + 22))
    print()
    for fragment in matches:
        print(f"- {fragment.fragment_date[:10]} | {fragment.title}")
        print(f"  kind: {fragment.metadata.get('kind', '')} | status: {fragment.metadata.get('status', '')} | pressure: {fragment.metadata.get('pressure', '')}")
        print(f"  source: {fragment.source}")
        print(f"  {fragment_excerpt(fragment)}")
        print(f"  slug: {fragment.slug}")
        print()
    return 0


def cmd_by_source(args: list[str]) -> int:
    if not args:
        print("Usage: voice-style-workshop by-source <source>", file=sys.stderr)
        return 1

    wanted = args[0].strip()
    matches = [fragment for fragment in iter_fragments() if fragment.source == wanted]
    if not matches:
        print(f"No fragments found for source: {wanted}")
        return 0

    print(f"Fragments from '{wanted}' ({len(matches)})")
    print("=" * min(max(len(wanted) + 18, 28), 72))
    print()
    for fragment in matches:
        print(f"- {fragment.fragment_date[:10]} | {fragment.title}")
        print(f"  kind: {fragment.metadata.get('kind', '')} | status: {fragment.metadata.get('status', '')} | pressure: {fragment.metadata.get('pressure', '')}")
        print(f"  tags: {', '.join(fragment.tags) if fragment.tags else '-'}")
        print(f"  {fragment_excerpt(fragment)}")
        why = why_excerpt(fragment)
        if why:
            print(f"  why alive: {why}")
        print(f"  slug: {fragment.slug}")
        print()
    return 0


def cmd_template(_: list[str]) -> int:
    print(
        "---\n"
        "title: \n"
        f"date: {date.today().isoformat()}\n"
        "kind: sentence\n"
        "status: fresh\n"
        "pressure: alive\n"
        "source: notes/example.md\n"
        "tags: []\n"
        "returns: []\n"
        "---\n\n"
        "## Fragment\n\n"
        "The line, paragraph, tonal fragment, or structural move itself. Keep it exact.\n\n"
        "## Why It Works\n\n"
        "What is alive here? Name the pressure precisely instead of praising it vaguely.\n\n"
        "## Return Tension\n\n"
        "Optional. Why return to it now, what it asks for, or what it warns against.\n\n"
        "## Use With Care\n\n"
        "Optional. Anti-pattern risk, overuse risk, or what would turn this into self-parody.\n"
    )
    return 0


def cmd_validate(_: list[str]) -> int:
    fragments = list(iter_fragments())
    if not fragments:
        print("No fragments to validate.")
        return 0

    errors: list[str] = []
    warnings: list[str] = []
    seen_slugs: set[str] = set()

    for fragment in fragments:
        meta = fragment.metadata
        if fragment.slug.lower() in seen_slugs:
            errors.append(f"{fragment.slug}: duplicate slug")
        seen_slugs.add(fragment.slug.lower())

        for field in REQUIRED_FIELDS:
            if not str(meta.get(field, "")).strip():
                errors.append(f"{fragment.slug}: missing required field '{field}'")

        kind = str(meta.get("kind", ""))
        if kind and kind not in VALID_KINDS:
            warnings.append(f"{fragment.slug}: unknown kind '{kind}'")

        status = str(meta.get("status", ""))
        if status and status not in VALID_STATUSES:
            warnings.append(f"{fragment.slug}: unknown status '{status}'")

        pressure = str(meta.get("pressure", ""))
        if pressure and pressure not in VALID_PRESSURE:
            warnings.append(f"{fragment.slug}: unknown pressure '{pressure}'")

        fragment_date = str(meta.get("date", ""))
        if fragment_date and not DATE_RE.match(fragment_date[:10]):
            errors.append(f"{fragment.slug}: date must look like YYYY-MM-DD")

        for index, return_marker in enumerate(fragment.returns, start=1):
            if not DATE_RE.match(return_marker[:10]):
                errors.append(f"{fragment.slug}: returns[{index}] must look like YYYY-MM-DD")

        sections = split_sections(fragment.body)
        if not fragment.body.strip():
            errors.append(f"{fragment.slug}: body is empty")
        elif not sections.get("fragment", "").strip():
            errors.append(f"{fragment.slug}: missing or empty 'Fragment' section")
        elif not sections.get("why it works", "").strip():
            errors.append(f"{fragment.slug}: missing or empty 'Why It Works' section")

        if status == "returning" and not fragment.returns:
            warnings.append(f"{fragment.slug}: status is 'returning' but no return markers are recorded")

        if len(set(tag.lower() for tag in fragment.tags)) != len(fragment.tags):
            warnings.append(f"{fragment.slug}: duplicate tags present")

        if fragment.path.stem != fragment.slug:
            errors.append(f"{fragment.slug}: filename must match slug")

    if errors:
        print("Errors")
        print("======")
        for error in errors:
            print(f"- {error}")
        print()

    if warnings:
        print("Warnings")
        print("========")
        for warning in warnings:
            print(f"- {warning}")
        print()

    distinct_sources = len({fragment.source for fragment in fragments if fragment.source})
    distinct_tags = len({tag.lower() for fragment in fragments for tag in fragment.tags})
    returning_count = sum(1 for fragment in fragments if fragment.returns or str(fragment.metadata.get("status", "")) == "returning")
    print(f"Validated {len(fragments)} fragment(s): {len(errors)} error(s), {len(warnings)} warning(s).")
    print(f"Distinct sources: {distinct_sources} | Distinct tags: {distinct_tags} | Returning fragments: {returning_count}")
    return 1 if errors else 0


def print_usage() -> None:
    print(
        "voice-style-workshop — local style fragment archive\n\n"
        "Usage:\n"
        "  voice-style-workshop list\n"
        "  voice-style-workshop show <slug>\n"
        "  voice-style-workshop returning\n"
        "  voice-style-workshop by-tag <tag>\n"
        "  voice-style-workshop by-source <source>\n"
        "  voice-style-workshop template\n"
        "  voice-style-workshop validate\n\n"
        "This keeps style as pressure, not bureaucracy."
    )


def main(argv: list[str]) -> int:
    commands = {
        "list": cmd_list,
        "show": cmd_show,
        "returning": cmd_returning,
        "by-tag": cmd_by_tag,
        "by-source": cmd_by_source,
        "template": cmd_template,
        "validate": cmd_validate,
    }

    if len(argv) < 2 or argv[1] in {"-h", "--help", "help"}:
        print_usage()
        return 0

    command = argv[1]
    handler = commands.get(command)
    if handler is None:
        print(f"Unknown command: {command}", file=sys.stderr)
        print_usage()
        return 1

    try:
        return handler(argv[2:])
    except BrokenPipeError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
