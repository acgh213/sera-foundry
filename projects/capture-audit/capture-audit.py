#!/usr/bin/env python3
"""
Capture Audit

Read-only terminal audit for Workbench captures.

Reports on:
- overall capture shape
- review-state coverage
- suspiciously short captures
- exact normalized duplicate groups
- a compact residue-class surfacing section

The heuristics are intentionally small and inspectable.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

CAPTURE_FILE = Path("projects/workbench/data/captures.jsonl")
REVIEW_STATE_FILE = Path("projects/workbench/data/review-state.json")
REVIEW_STATES = {"new", "reviewed", "promote", "defer", "dormant"}

MEANINGFUL_EXTRACTED_PRESSURE = "meaningful extracted pressure"
WEAK_MEANINGFUL_PLANNING = "weak but meaningful planning residue"
WEAK_LOW_VALUE = "weak low-value residue"
OTHER_RESIDUE = "other residue"

PRESSURE_MARKERS = {
    "but",
    "still",
    "because",
    "whether",
    "when",
    "instead",
    "yet",
    "however",
    "coherent",
    "question",
}
PLANNING_MARKERS = {
    "need",
    "better",
    "potential",
    "public",
    "internal",
    "note",
    "notes",
    "continuity",
    "layers",
    "layer",
    "promotion",
    "flow",
    "distinction",
    "design",
    "workflow",
    "plan",
    "planning",
}
LOW_VALUE_PHRASES = {
    "thought about",
    "fragment kept",
    "kept instead of discarded",
}
RESIDUE_PRIORITY = {
    MEANINGFUL_EXTRACTED_PRESSURE: 0,
    WEAK_MEANINGFUL_PLANNING: 1,
    WEAK_LOW_VALUE: 2,
    OTHER_RESIDUE: 3,
}


@dataclass
class Capture:
    id: int
    timestamp: str
    dt: datetime | None
    layer: str
    source: str
    source_family: str
    text: str
    tags: list[str]
    metadata: dict
    review_state: str
    review_updated_at: str | None
    length_chars: int
    word_count: int
    extraction_mode: str
    residue_class: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Workbench captures without modifying state.")
    parser.add_argument("--captures", type=Path, default=CAPTURE_FILE, help=f"Path to captures jsonl (default: {CAPTURE_FILE})")
    parser.add_argument("--review-state", type=Path, default=REVIEW_STATE_FILE, help=f"Path to review-state json (default: {REVIEW_STATE_FILE})")
    parser.add_argument("--oldest-limit", type=int, default=5, help="How many oldest unreviewed captures to show")
    parser.add_argument("--short-limit", type=int, default=5, help="How many short captures to show")
    parser.add_argument("--duplicate-limit", type=int, default=5, help="How many duplicate groups to show")
    parser.add_argument("--inspect-limit", type=int, default=8, help="How many default-surfaced items to show")
    parser.add_argument("--short-chars", type=int, default=45, help="Suspicious-short threshold by non-space character count")
    parser.add_argument("--short-words", type=int, default=7, help="Suspicious-short threshold by word count")
    return parser.parse_args()


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def read_review_states(path: Path) -> dict[int, dict[str, str | None]]:
    if not path.exists():
        return {}

    raw = json.loads(path.read_text(encoding="utf-8"))
    states: dict[int, dict[str, str | None]] = {}
    for key, value in raw.items():
        try:
            capture_id = int(key)
        except (TypeError, ValueError):
            continue

        state = None
        updated_at = None
        if isinstance(value, str):
            state = value
        elif isinstance(value, dict):
            state = value.get("state")
            updated_at = value.get("updated_at")

        if state in REVIEW_STATES:
            states[capture_id] = {"state": state, "updated_at": updated_at}
    return states


def source_family_for(source: str) -> str:
    if not source:
        return "unknown"
    if ":" in source:
        return source.split(":", 1)[0]
    return source


def extraction_mode_for(raw: dict, source_family: str) -> str:
    tags = set(raw.get("tags") or [])
    metadata = raw.get("metadata") or {}
    if "extracted" in tags:
        return "extracted"
    if source_family.endswith("extractor"):
        return "extracted"
    if metadata.get("reason") or metadata.get("source_file"):
        return "extracted"
    if raw.get("source"):
        return "manual"
    return "unknown"


def classify_residue(text: str, extraction_mode: str, word_count: int) -> str:
    lowered = text.casefold()
    tokens = set(re.findall(r"\b\w+\b", lowered))
    has_pressure_marker = bool(tokens & PRESSURE_MARKERS)
    has_planning_marker = bool(tokens & PLANNING_MARKERS)
    has_low_value_phrase = any(phrase in lowered for phrase in LOW_VALUE_PHRASES)

    if extraction_mode == "extracted":
        if has_low_value_phrase:
            return WEAK_LOW_VALUE
        if word_count >= 10 or has_pressure_marker:
            return MEANINGFUL_EXTRACTED_PRESSURE
        return WEAK_LOW_VALUE

    if has_low_value_phrase or word_count <= 5:
        return WEAK_LOW_VALUE
    if has_planning_marker:
        return WEAK_MEANINGFUL_PLANNING
    return OTHER_RESIDUE


def read_captures(path: Path, review_states: dict[int, dict[str, str | None]]) -> list[Capture]:
    if not path.exists():
        raise SystemExit(f"Capture file not found: {path}")

    captures: list[Capture] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            raw = json.loads(line)
            text = (raw.get("text") or "").strip()
            timestamp = raw.get("timestamp") or ""
            dt = parse_datetime(timestamp)
            source = raw.get("source") or "unknown"
            source_family = source_family_for(source)
            review = review_states.get(line_number, {})
            word_count = len(re.findall(r"\b\w+\b", text))
            extraction_mode = extraction_mode_for(raw, source_family)
            captures.append(
                Capture(
                    id=line_number,
                    timestamp=timestamp,
                    dt=dt,
                    layer=raw.get("layer") or "internal",
                    source=source,
                    source_family=source_family,
                    text=text,
                    tags=list(raw.get("tags") or []),
                    metadata=dict(raw.get("metadata") or {}),
                    review_state=(review.get("state") or "new"),
                    review_updated_at=review.get("updated_at"),
                    length_chars=len(re.sub(r"\s+", "", text)),
                    word_count=word_count,
                    extraction_mode=extraction_mode,
                    residue_class=classify_residue(text, extraction_mode, word_count),
                )
            )
    return captures


def normalize_text(text: str) -> str:
    lowered = text.casefold()
    lowered = re.sub(r"[^\w\s]", " ", lowered)
    lowered = re.sub(r"\s+", " ", lowered).strip()
    return lowered


def format_counter(counter: Counter) -> list[str]:
    if not counter:
        return ["  - none"]
    width = max(len(str(value)) for value in counter.values())
    return [f"  {value:>{width}}  {key}" for key, value in counter.most_common()]


def fmt_dt(dt: datetime | None) -> str:
    if not dt:
        return "unknown"
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def preview(text: str, width: int = 88) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= width:
        return compact
    return compact[: width - 1] + "…"


def find_unreviewed(captures: Iterable[Capture]) -> list[Capture]:
    items = [capture for capture in captures if capture.review_state == "new"]
    return sorted(items, key=lambda item: (item.dt or datetime.max.replace(tzinfo=timezone.utc), item.id))


def find_short(captures: Iterable[Capture], short_chars: int, short_words: int) -> list[Capture]:
    suspects = []
    for capture in captures:
        if capture.length_chars <= short_chars or capture.word_count <= short_words:
            suspects.append(capture)
    return sorted(suspects, key=lambda item: (item.length_chars, item.word_count, item.id))


def find_duplicate_groups(captures: Iterable[Capture]) -> list[list[Capture]]:
    buckets: dict[str, list[Capture]] = defaultdict(list)
    for capture in captures:
        norm = normalize_text(capture.text)
        if not norm:
            continue
        buckets[norm].append(capture)

    groups = [group for group in buckets.values() if len(group) > 1]
    groups.sort(key=lambda group: (-len(group), min(item.id for item in group)))
    return groups


def build_default_surfacing(captures: list[Capture]) -> list[Capture]:
    return sorted(
        captures,
        key=lambda item: (
            RESIDUE_PRIORITY.get(item.residue_class, 99),
            item.review_state != "new",
            item.dt or datetime.max.replace(tzinfo=timezone.utc),
            item.id,
        ),
    )


def report(captures: list[Capture], args: argparse.Namespace) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = []
    lines.append("╭─ CAPTURE AUDIT")
    lines.append(f"│ Generated: {now}")
    lines.append(f"│ Capture file: {args.captures}")
    lines.append(f"│ Review state: {args.review_state} {'(missing → all treated as new)' if not args.review_state.exists() else ''}")
    lines.append(f"│ Total captures: {len(captures)}")
    lines.append("")

    layer_counts = Counter(c.layer for c in captures)
    source_family_counts = Counter(c.source_family for c in captures)
    source_counts = Counter(c.source for c in captures)
    extraction_counts = Counter(c.extraction_mode for c in captures)
    review_counts = Counter(c.review_state for c in captures)
    residue_counts = Counter(c.residue_class for c in captures)

    lines.append("╭─ SHAPE")
    lines.append("│ By layer:")
    lines.extend(format_counter(layer_counts))
    lines.append("│")
    lines.append("│ By source family:")
    lines.extend(format_counter(source_family_counts))
    lines.append("│")
    lines.append("│ By extraction mode:")
    lines.extend(format_counter(extraction_counts))
    lines.append("│")
    lines.append("│ Review states:")
    lines.extend(format_counter(review_counts))
    lines.append("│")
    lines.append("│ Residue classes (heuristic):")
    lines.extend(format_counter(residue_counts))
    if source_counts:
        lines.append("│")
        lines.append("│ Top exact sources:")
        lines.extend(format_counter(source_counts))
    lines.append("")

    unreviewed = find_unreviewed(captures)
    lines.append("╭─ OLDEST UNREVIEWED")
    lines.append(f"│ Count: {len(unreviewed)}")
    if not unreviewed:
        lines.append("│ ✓ No unreviewed captures")
    else:
        for capture in unreviewed[: args.oldest_limit]:
            lines.append(
                f"│ #{capture.id}  {fmt_dt(capture.dt)}  [{capture.layer}] [{capture.source_family}] [{capture.residue_class}]"
            )
            lines.append(f"│   {preview(capture.text)}")
    lines.append("")

    short_items = find_short(captures, args.short_chars, args.short_words)
    lines.append("╭─ SUSPICIOUSLY SHORT")
    lines.append(f"│ Threshold: <= {args.short_chars} chars (no spaces) OR <= {args.short_words} words")
    lines.append(f"│ Count: {len(short_items)}")
    if not short_items:
        lines.append("│ ✓ No suspiciously short captures")
    else:
        for capture in short_items[: args.short_limit]:
            lines.append(
                f"│ #{capture.id}  {capture.word_count}w/{capture.length_chars}c  [{capture.review_state}] [{capture.source_family}] [{capture.residue_class}]"
            )
            lines.append(f"│   {preview(capture.text)}")
    lines.append("")

    duplicate_groups = find_duplicate_groups(captures)
    lines.append("╭─ DUPLICATE-ISH (EXACT NORMALIZED TEXT)")
    lines.append("│ Heuristic: lowercase + punctuation-stripped + whitespace-collapsed exact match")
    lines.append(f"│ Groups: {len(duplicate_groups)}")
    if not duplicate_groups:
        lines.append("│ ✓ No exact normalized duplicate groups found")
    else:
        for group in duplicate_groups[: args.duplicate_limit]:
            ids = ", ".join(f"#{item.id}" for item in group)
            lines.append(f"│ {ids}  ({len(group)} captures)")
            lines.append(f"│   {preview(group[0].text)}")
    lines.append("")

    surfaced = build_default_surfacing(captures)
    lines.append("╭─ DEFAULT SURFACING")
    lines.append("│ Order: meaningful extracted pressure → weak planning residue → weak low-value residue")
    if not surfaced:
        lines.append("│ ✓ Nothing clearly surfaced by current heuristics")
    else:
        for capture in surfaced[: args.inspect_limit]:
            deprioritized = " (deprioritized)" if capture.residue_class == WEAK_LOW_VALUE else ""
            lines.append(
                f"│ #{capture.id}  [{capture.review_state}] [{capture.layer}] [{capture.source_family}] [{capture.residue_class}]{deprioritized}"
            )
            lines.append(f"│   {preview(capture.text)}")
    lines.append("")

    weak_low_value = [capture for capture in surfaced if capture.residue_class == WEAK_LOW_VALUE]
    lines.append("╭─ DEPRIORITIZED WEAK LOW-VALUE")
    lines.append(f"│ Count: {len(weak_low_value)}")
    if not weak_low_value:
        lines.append("│ ✓ No weak low-value residue surfaced by current heuristics")
    else:
        for capture in weak_low_value[: args.short_limit]:
            lines.append(f"│ #{capture.id}  [{capture.review_state}] [{capture.source_family}]")
            lines.append(f"│   {preview(capture.text)}")
    lines.append("")

    lines.append("╭─ NOTES")
    lines.append("│ This tool is read-only.")
    lines.append("│ Residue classification is heuristic and intentionally lightweight; it is not stored as state.")
    lines.append("│ Meaningful extracted pressure stays near the top of default surfacing.")
    lines.append("│ Weak low-value residue remains visible, but is called out as deprioritized by default.")
    lines.append("│ Duplicate detection only catches exact normalized matches, not semantic overlap.")
    lines.append("╰─")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    review_states = read_review_states(args.review_state)
    captures = read_captures(args.captures, review_states)
    print(report(captures, args))


if __name__ == "__main__":
    main()
