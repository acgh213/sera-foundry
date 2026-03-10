#!/usr/bin/env python3
"""
drift-review

Small terminal review surface for extracted drift captures.

Reads Workbench captures/review state and helps answer:
- what extracted drift captures exist?
- which ones still feel live?
- which ones look like weak extraction residue?
- which source artifacts are producing the strongest pressure?

This is intentionally downstream of drift-extractor.
It does not modify capture state or widen extraction logic.
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

STRONG_PRESSURE = "strong extracted pressure"
POSSIBLE_PRESSURE = "possible extracted pressure"
WEAK_RESIDUE = "weak extraction residue"

CLASS_PRIORITY = {
    STRONG_PRESSURE: 0,
    POSSIBLE_PRESSURE: 1,
    WEAK_RESIDUE: 2,
}

LOW_VALUE_PHRASES = {
    "a fragment kept instead of discarded",
    "fragment kept instead of discarded",
    "kept instead of discarded",
}

PRESSURE_WORDS = {
    "continuity",
    "coherent",
    "pressure",
    "question",
    "questions",
    "return",
    "returns",
    "artifact",
    "artifacts",
    "workflow",
    "memory",
    "identity",
    "boundary",
    "boundaries",
    "design",
    "public",
    "private",
    "archive",
    "recurrence",
    "promotion",
    "residue",
}

HIGH_SIGNAL_PRESSURES = {
    "missing bridge",
    "selection pressure",
    "method pressure",
    "structural tension",
    "boundary tension",
    "design pressure",
    "unfinished thread",
}


@dataclass
class DriftCapture:
    id: int
    timestamp: str
    dt: datetime | None
    review_state: str
    review_updated_at: str | None
    text: str
    source: str
    source_family: str
    source_file: Path | None
    layer: str
    tags: list[str]
    reason: str | None
    pressure: str | None
    score: float | None
    classification: str
    char_count: int
    word_count: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review extracted drift captures in a compact terminal format.")
    parser.add_argument("command", nargs="?", default="list", choices=["list", "show", "sources"], help="View mode")
    parser.add_argument("capture_id", nargs="?", type=int, help="Capture id for show mode")
    parser.add_argument("--captures", type=Path, default=CAPTURE_FILE, help=f"Path to captures jsonl (default: {CAPTURE_FILE})")
    parser.add_argument("--review-state", type=Path, default=REVIEW_STATE_FILE, help=f"Path to review-state json (default: {REVIEW_STATE_FILE})")
    parser.add_argument("--all", action="store_true", help="Include weak extraction residue in default list output")
    parser.add_argument("--weak-only", action="store_true", help="Show only weak extraction residue")
    parser.add_argument("--source", help="Filter by source file path/name substring")
    parser.add_argument("--state", choices=sorted(REVIEW_STATES), help="Filter by review state")
    parser.add_argument("--ungrouped", action="store_true", help="Show a flat list instead of grouping by source artifact")
    parser.add_argument("--limit", type=int, default=12, help="Max captures to show in list output")
    parser.add_argument("--source-limit", type=int, default=8, help="Max sources to show in sources output")
    parser.add_argument("--excerpt-chars", type=int, default=420, help="Max chars for source excerpts in show mode")
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


def looks_like_drift_capture(raw: dict) -> bool:
    tags = set(raw.get("tags") or [])
    source = raw.get("source") or ""
    metadata = raw.get("metadata") or {}
    if "drift" in tags:
        return True
    if source.startswith("drift-extractor:"):
        return True
    return bool(metadata.get("source_file") and metadata.get("reason"))


def normalize_text(text: str) -> str:
    lowered = text.casefold()
    lowered = re.sub(r"[^\w\s]", " ", lowered)
    lowered = re.sub(r"\s+", " ", lowered).strip()
    return lowered


def classify_capture(text: str, pressure: str | None, reason: str | None, score: float | None, word_count: int) -> str:
    lowered = text.casefold().strip()
    tokens = set(re.findall(r"\b\w+\b", lowered))

    if lowered in LOW_VALUE_PHRASES or any(phrase in lowered for phrase in LOW_VALUE_PHRASES):
        return WEAK_RESIDUE

    pressure = (pressure or "").strip().casefold()
    reason = (reason or "").strip().casefold()
    score = float(score or 0.0)

    pressure_hits = len(tokens & PRESSURE_WORDS)
    has_question = "?" in text
    long_enough = word_count >= 12
    medium_enough = word_count >= 8
    high_signal_pressure = pressure in HIGH_SIGNAL_PRESSURES
    strong_reason = reason.startswith('from "') or reason in {"explicit question", "tension/contrast language"}

    if high_signal_pressure and (score >= 0.72 or long_enough or pressure_hits >= 2):
        return STRONG_PRESSURE

    if has_question and (score >= 0.62 or medium_enough):
        return STRONG_PRESSURE

    if score >= 0.78:
        return STRONG_PRESSURE

    if strong_reason and (pressure_hits >= 2 or (medium_enough and score >= 0.58) or lowered.startswith("but ")):
        return STRONG_PRESSURE

    if (score >= 0.64 and medium_enough) or (strong_reason and pressure_hits >= 1) or pressure_hits >= 3:
        return POSSIBLE_PRESSURE

    return WEAK_RESIDUE


def read_drift_captures(path: Path, review_states: dict[int, dict[str, str | None]]) -> list[DriftCapture]:
    if not path.exists():
        raise SystemExit(f"Capture file not found: {path}")

    captures: list[DriftCapture] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            raw = json.loads(line)
            if not looks_like_drift_capture(raw):
                continue

            text = (raw.get("text") or "").strip()
            metadata = raw.get("metadata") or {}
            source = raw.get("source") or "unknown"
            review = review_states.get(line_number, {})
            word_count = len(re.findall(r"\b\w+\b", text))
            score = metadata.get("score")
            try:
                score = float(score) if score is not None else None
            except (TypeError, ValueError):
                score = None

            capture = DriftCapture(
                id=line_number,
                timestamp=raw.get("timestamp") or "",
                dt=parse_datetime(raw.get("timestamp")),
                review_state=(review.get("state") or "new"),
                review_updated_at=review.get("updated_at"),
                text=text,
                source=source,
                source_family=source_family_for(source),
                source_file=Path(metadata["source_file"]) if metadata.get("source_file") else None,
                layer=raw.get("layer") or "internal",
                tags=list(raw.get("tags") or []),
                reason=metadata.get("reason"),
                pressure=metadata.get("pressure"),
                score=score,
                classification=classify_capture(text, metadata.get("pressure"), metadata.get("reason"), score, word_count),
                char_count=len(re.sub(r"\s+", "", text)),
                word_count=word_count,
            )
            captures.append(capture)
    return captures


def preview(text: str, width: int = 92) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= width:
        return compact
    return compact[: width - 1] + "…"


def fmt_dt(dt: datetime | None) -> str:
    if not dt:
        return "unknown"
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def score_label(score: float | None) -> str:
    if score is None:
        return "--"
    return f"{score:.2f}"


def apply_filters(captures: list[DriftCapture], args: argparse.Namespace) -> list[DriftCapture]:
    items = captures
    if args.source:
        needle = args.source.casefold()
        items = [
            capture
            for capture in items
            if needle in capture.source.casefold()
            or (capture.source_file and needle in str(capture.source_file).casefold())
            or needle in capture.text.casefold()
        ]
    if args.state:
        items = [capture for capture in items if capture.review_state == args.state]
    if args.weak_only:
        items = [capture for capture in items if capture.classification == WEAK_RESIDUE]
    elif not args.all:
        items = [capture for capture in items if capture.classification != WEAK_RESIDUE]
    return items


def sort_key(capture: DriftCapture):
    return (
        CLASS_PRIORITY.get(capture.classification, 99),
        capture.review_state != "new",
        -(capture.score or 0.0),
        capture.dt or datetime.min.replace(tzinfo=timezone.utc),
        capture.id,
    )


def summarize_source(captures: Iterable[DriftCapture]) -> tuple[str, Counter, float]:
    captures = list(captures)
    counts = Counter(capture.classification for capture in captures)
    best_score = max((capture.score or 0.0) for capture in captures) if captures else 0.0
    source_file = next((str(c.source_file) for c in captures if c.source_file), captures[0].source if captures else "unknown")
    return source_file, counts, best_score


def render_list(captures: list[DriftCapture], hidden_weak_count: int, args: argparse.Namespace) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = []
    counts = Counter(c.classification for c in captures)

    lines.append("╭─ DRIFT REVIEW")
    lines.append(f"│ Generated: {now}")
    lines.append(f"│ Capture file: {args.captures}")
    lines.append(f"│ Drift captures in view: {len(captures)}")
    if not args.all and not args.weak_only:
        lines.append(f"│ Weak residue hidden by default: {hidden_weak_count}  (use --all or --weak-only)")
    lines.append("│")
    lines.append(
        "│ Classes: "
        f"{counts.get(STRONG_PRESSURE, 0)} strong · "
        f"{counts.get(POSSIBLE_PRESSURE, 0)} possible · "
        f"{counts.get(WEAK_RESIDUE, 0)} weak"
    )
    lines.append("│ Default goal: keep strong extracted pressure visible without erasing provenance.")
    lines.append("")

    if not captures:
        lines.append("╰─ No matching drift captures.")
        return "\n".join(lines)

    if args.ungrouped:
        lines.append("╭─ CAPTURES")
        for capture in sorted(captures, key=sort_key)[: args.limit]:
            lines.append(
                f"│ #{capture.id}  [{capture.review_state}] [{capture.classification}] score={score_label(capture.score)}"
            )
            lines.append(f"│   pressure: {capture.pressure or 'unknown'}")
            lines.append(f"│   source: {capture.source_file or capture.source}")
            lines.append(f"│   {preview(capture.text)}")
        lines.append("╰─")
        return "\n".join(lines)

    grouped: dict[str, list[DriftCapture]] = defaultdict(list)
    for capture in captures:
        key = str(capture.source_file) if capture.source_file else capture.source
        grouped[key].append(capture)

    source_items = sorted(
        grouped.items(),
        key=lambda item: (
            min(CLASS_PRIORITY.get(c.classification, 99) for c in item[1]),
            -max((c.score or 0.0) for c in item[1]),
            item[0],
        ),
    )

    shown = 0
    for source_key, group in source_items:
        if shown >= args.limit:
            break
        _, source_counts, best_score = summarize_source(group)
        lines.append(f"╭─ SOURCE: {Path(source_key).name}")
        lines.append(f"│ Path: {source_key}")
        lines.append(
            "│ Summary: "
            f"{source_counts.get(STRONG_PRESSURE, 0)} strong · "
            f"{source_counts.get(POSSIBLE_PRESSURE, 0)} possible · "
            f"{source_counts.get(WEAK_RESIDUE, 0)} weak · "
            f"best score={best_score:.2f}"
        )
        for capture in sorted(group, key=sort_key):
            lines.append(
                f"│ #{capture.id}  [{capture.review_state}] [{capture.classification}] [{capture.pressure or capture.reason or 'unknown'}] score={score_label(capture.score)}"
            )
            lines.append(f"│   {preview(capture.text)}")
        shown += 1
    lines.append("╰─")
    return "\n".join(lines)


def render_sources(captures: list[DriftCapture], args: argparse.Namespace) -> str:
    grouped: dict[str, list[DriftCapture]] = defaultdict(list)
    for capture in captures:
        key = str(capture.source_file) if capture.source_file else capture.source
        grouped[key].append(capture)

    rows = []
    for source_key, group in grouped.items():
        _, counts, best_score = summarize_source(group)
        rows.append((source_key, len(group), counts, best_score))

    rows.sort(key=lambda row: (-row[1], -row[3], row[0]))

    lines = ["╭─ DRIFT SOURCES", f"│ Sources in view: {len(rows)}", "│"]
    if not rows:
        lines.append("╰─ No matching sources.")
        return "\n".join(lines)

    for source_key, total, counts, best_score in rows[: args.source_limit]:
        lines.append(f"│ {Path(source_key).name}")
        lines.append(f"│   total={total} · strong={counts.get(STRONG_PRESSURE, 0)} · possible={counts.get(POSSIBLE_PRESSURE, 0)} · weak={counts.get(WEAK_RESIDUE, 0)} · best={best_score:.2f}")
        lines.append(f"│   {source_key}")
    lines.append("╰─")
    return "\n".join(lines)


def split_paragraphs(text: str) -> list[str]:
    blocks = re.split(r"\n\s*\n", text)
    return [block.strip() for block in blocks if block.strip()]


def best_source_excerpt(source_text: str, capture_text: str, max_chars: int) -> str:
    if capture_text and capture_text in source_text:
        idx = source_text.index(capture_text)
        start = max(0, idx - max_chars // 3)
        end = min(len(source_text), idx + len(capture_text) + max_chars // 2)
        excerpt = source_text[start:end].strip()
        if start > 0:
            excerpt = "…" + excerpt
        if end < len(source_text):
            excerpt = excerpt + "…"
        return excerpt

    target_tokens = set(normalize_text(capture_text).split())
    best_block = ""
    best_overlap = 0
    for block in split_paragraphs(source_text):
        block_tokens = set(normalize_text(block).split())
        overlap = len(target_tokens & block_tokens)
        if overlap > best_overlap:
            best_overlap = overlap
            best_block = block

    excerpt = best_block or source_text[:max_chars]
    excerpt = re.sub(r"\s+", " ", excerpt).strip()
    if len(excerpt) > max_chars:
        excerpt = excerpt[: max_chars - 1].rstrip() + "…"
    return excerpt


def render_show(captures: list[DriftCapture], capture_id: int | None, excerpt_chars: int) -> str:
    if capture_id is None:
        raise SystemExit("show mode requires a capture id")

    capture = next((item for item in captures if item.id == capture_id), None)
    if not capture:
        raise SystemExit(f"drift capture not found: #{capture_id}")

    lines = ["╭─ DRIFT CAPTURE"]
    lines.append(f"│ id: #{capture.id}")
    lines.append(f"│ captured: {fmt_dt(capture.dt)}")
    lines.append(f"│ review state: {capture.review_state}")
    lines.append(f"│ classification: {capture.classification}")
    lines.append(f"│ pressure: {capture.pressure or 'unknown'}")
    lines.append(f"│ reason: {capture.reason or 'unknown'}")
    lines.append(f"│ score: {score_label(capture.score)}")
    lines.append(f"│ layer: {capture.layer}")
    lines.append(f"│ source: {capture.source}")
    lines.append(f"│ source file: {capture.source_file or 'missing'}")
    lines.append("│")
    lines.append("│ Capture text:")
    for line in capture.text.splitlines() or [capture.text]:
        lines.append(f"│   {line}")

    if capture.source_file and capture.source_file.exists():
        source_text = capture.source_file.read_text(encoding="utf-8")
        excerpt = best_source_excerpt(source_text, capture.text, excerpt_chars)
        lines.append("│")
        lines.append("│ Source excerpt:")
        for line in excerpt.splitlines() or [excerpt]:
            lines.append(f"│   {line}")
    else:
        lines.append("│")
        lines.append("│ Source excerpt: unavailable (source file missing)")

    lines.append("╰─")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    review_states = read_review_states(args.review_state)
    captures = read_drift_captures(args.captures, review_states)

    hidden_weak_count = sum(1 for capture in captures if capture.classification == WEAK_RESIDUE)
    filtered = apply_filters(captures, args)

    if args.command == "show":
        print(render_show(captures, args.capture_id, args.excerpt_chars))
        return

    if args.command == "sources":
        print(render_sources(filtered, args))
        return

    print(render_list(filtered, hidden_weak_count, args))


if __name__ == "__main__":
    main()
