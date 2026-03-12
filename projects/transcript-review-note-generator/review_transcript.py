#!/usr/bin/env python3
"""Transcript Review Note Generator v1.

Local, inspectable heuristic tool that turns one transcript text file into one
markdown review note. It does not auto-promote anything; it surfaces candidate
items with evidence pointers and visible uncertainty.
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
from dataclasses import dataclass
from typing import Iterable

SECTIONS = [
    ("decisions", "Decisions"),
    ("open_threads", "Open Threads"),
    ("project_ideas", "Candidate Project Ideas"),
    ("memory_promotions", "Candidate Memory Promotions"),
    ("artifact_candidates", "Candidate Authored Artifacts"),
    ("residue", "Residue"),
]

LAYER_LABELS = {
    "daily_note": "Layer 2 — daily note / session residue",
    "project_note": "Layer 3 — project note / line-of-work memory",
    "long_term_memory": "Layer 4 — long-term continuity memory",
    "authored_artifact": "Layer 5 — authored artifact",
    "leave_unpromoted": "Leave unpromoted / residue",
}


@dataclass
class Line:
    number: int
    text: str


@dataclass
class Item:
    section: str
    statement: str
    line_start: int
    line_end: int
    evidence: str
    destination: str | None
    confidence: str
    score: int
    reason: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a transcript review note from a text transcript.")
    parser.add_argument("transcript", help="Path to a UTF-8 plain text transcript")
    parser.add_argument("-o", "--output", help="Output markdown file path")
    parser.add_argument(
        "--max-items-per-section",
        type=int,
        default=8,
        help="Maximum items to emit per section (default: 8)",
    )
    return parser.parse_args()


def load_lines(path: pathlib.Path) -> list[Line]:
    raw = path.read_text(encoding="utf-8")
    return [Line(i + 1, line.rstrip()) for i, line in enumerate(raw.splitlines())]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def speakerless_text(text: str) -> str:
    return re.sub(r"^[A-Za-z0-9_. -]{1,24}:\s*", "", text).strip()


def evidence_for(lines: list[Line], index: int, window: int = 0) -> tuple[int, int, str]:
    start = max(0, index - window)
    end = min(len(lines) - 1, index + window)
    snippet = " ".join(speakerless_text(lines[i].text) for i in range(start, end + 1) if lines[i].text.strip())
    snippet = normalize(snippet)
    if len(snippet) > 220:
        snippet = snippet[:217] + "..."
    return lines[start].number, lines[end].number, snippet


def confidence_from_score(score: int) -> str:
    if score >= 5:
        return "high"
    if score >= 3:
        return "medium"
    return "low"


class Heuristics:
    DECISION = [
        (re.compile(r"\b(decide|decided|decision|settled|default|constraint|must|won't|will not|do not|keep|remain|ship)\b", re.I), 3),
        (re.compile(r"\b(we should|let's|we'll|we are going to|we're going to|i'll|i will)\b", re.I), 2),
        (re.compile(r"\b(no ui|local-only|text-first|terminal-first|standard library)\b", re.I), 2),
    ]
    OPEN_THREAD = [
        (re.compile(r"\?"), 2),
        (re.compile(r"\b(open question|open thread|unresolved|unclear|not sure|maybe later|follow up|need to|still need|should we|could we|whether)\b", re.I), 3),
        (re.compile(r"\b(maybe|perhaps|might)\b", re.I), 1),
    ]
    PROJECT_IDEA = [
        (re.compile(r"\b(project|tool|script|generator|workflow|bridge|prototype|cli|utility)\b", re.I), 2),
        (re.compile(r"\b(build|make|create|spin up|try|ship)\b", re.I), 1),
        (re.compile(r"\bidea\b", re.I), 2),
    ]
    MEMORY = [
        (re.compile(r"\b(always|never|prefer|prefers|call me|timezone|works at|engaged|trans woman|identity|anti-goal|collaboration norm)\b", re.I), 3),
        (re.compile(r"\b(don't become|do not become|weirdness should stay|review-first|inspectable|hidden automation)\b", re.I), 2),
        (re.compile(r"\b(recurring|stable|durable|long-term)\b", re.I), 2),
    ]
    ARTIFACT = [
        (re.compile(r"\b(essay|spec|README|readme|note|blog|post|doctrine|write this down|artifact|draft)\b", re.I), 3),
        (re.compile(r"\b(should become text|worth writing|deserves a note|turn into a note)\b", re.I), 3),
    ]
    RESIDUE = [
        (re.compile(r"\b(lol|haha|thanks|cool|nice|okay|ok|yep|sure|sounds good)\b", re.I), 2),
        (re.compile(r"\b(brb|later|morning|afternoon|tonight|tomorrow)\b", re.I), 1),
    ]


def score_patterns(text: str, patterns: Iterable[tuple[re.Pattern[str], int]]) -> int:
    score = 0
    for pattern, weight in patterns:
        if pattern.search(text):
            score += weight
    return score


def make_statement(text: str) -> str:
    text = speakerless_text(text)
    text = normalize(text)
    if not text:
        return "(empty)"
    if len(text) <= 110:
        return text
    cut = text[:107].rsplit(" ", 1)[0]
    return cut + "..."


def has_token(text: str, token: str) -> bool:
    return re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", text) is not None


def destination_for(section: str, text: str) -> str | None:
    lower = text.lower()
    if section == "decisions":
        if any(has_token(lower, word) for word in ["local-only", "text-first", "terminal-first", "project", "tool", "script", "cli"]):
            return "project_note"
        if any(has_token(lower, word) for word in ["always", "never", "identity", "cassie", "sera"]):
            return "long_term_memory"
        return "daily_note"
    if section == "open_threads":
        if any(has_token(lower, word) for word in ["project", "tool", "build", "script", "cli"]):
            return "project_note"
        return "daily_note"
    if section == "project_ideas":
        return "project_note"
    if section == "memory_promotions":
        if any(has_token(lower, word) for word in ["essay", "spec", "doctrine", "blog"]):
            return "authored_artifact"
        if any(has_token(lower, word) for word in ["identity", "cassie", "sera", "always", "never", "prefer", "prefers", "anti-goal"]):
            return "long_term_memory"
        return "project_note"
    if section == "artifact_candidates":
        return "authored_artifact"
    if section == "residue":
        return "leave_unpromoted"
    return None


def residue_reason(text: str) -> str:
    lower = text.lower()
    if len(lower) < 28:
        return "Short conversational residue with low durable pressure."
    if any(token in lower for token in ["thanks", "cool", "nice", "lol", "haha"]):
        return "Social acknowledgement or lightweight chatter; useful in the moment, not a promotion candidate."
    if any(token in lower for token in ["tomorrow", "tonight", "morning", "later"]):
        return "Timing/logistics residue; likely daily-only at most."
    return "No strong decision, open-thread, memory, project, or artifact signal detected."


def collect_items(lines: list[Line]) -> list[Item]:
    items: list[Item] = []
    for idx, line in enumerate(lines):
        text = line.text.strip()
        if not text:
            continue
        bare = speakerless_text(text)
        if not bare:
            continue
        lowered = bare.lower()

        decision_score = score_patterns(bare, Heuristics.DECISION)
        open_score = score_patterns(bare, Heuristics.OPEN_THREAD)
        project_score = score_patterns(bare, Heuristics.PROJECT_IDEA)
        memory_score = score_patterns(bare, Heuristics.MEMORY)
        artifact_score = score_patterns(bare, Heuristics.ARTIFACT)
        residue_score = score_patterns(bare, Heuristics.RESIDUE)

        if "?" in bare and decision_score > 0:
            decision_score -= 1
        if any(token in lowered for token in ["maybe", "not sure", "perhaps", "might"]) and decision_score > 0:
            decision_score -= 1
        if any(token in lowered for token in ["decide", "default", "constraint", "must", "do not", "won't"]) and open_score > 0:
            open_score -= 1

        section_scores = {
            "decisions": decision_score,
            "open_threads": open_score,
            "project_ideas": project_score,
            "memory_promotions": memory_score,
            "artifact_candidates": artifact_score,
        }
        for section, score in section_scores.items():
            if score >= 3:
                start, end, evidence = evidence_for(lines, idx, window=0)
                items.append(
                    Item(
                        section=section,
                        statement=make_statement(bare),
                        line_start=start,
                        line_end=end,
                        evidence=evidence,
                        destination=destination_for(section, bare),
                        confidence=confidence_from_score(score),
                        score=score,
                    )
                )

        if all(score < 3 for score in section_scores.values()):
            residue_total = residue_score + (1 if len(bare) < 40 else 0)
            if residue_total >= 1:
                start, end, evidence = evidence_for(lines, idx, window=0)
                items.append(
                    Item(
                        section="residue",
                        statement=make_statement(bare),
                        line_start=start,
                        line_end=end,
                        evidence=evidence,
                        destination="leave_unpromoted",
                        confidence="low",
                        score=residue_total,
                        reason=residue_reason(bare),
                    )
                )
    return dedupe_items(items)


def dedupe_items(items: list[Item]) -> list[Item]:
    best: dict[tuple[str, int, str], Item] = {}
    for item in items:
        key = (item.section, item.line_start, item.statement)
        current = best.get(key)
        if current is None or item.score > current.score:
            best[key] = item
    return list(best.values())


def render_section(items: list[Item], title: str) -> str:
    lines: list[str] = [f"## {title}", ""]
    if not items:
        lines.extend(["_No strong candidates detected._", ""])
        return "\n".join(lines)

    for item in items:
        pointer = f"L{item.line_start}" if item.line_start == item.line_end else f"L{item.line_start}-L{item.line_end}"
        lines.append(f"- **{item.statement}**")
        lines.append(f"  - evidence: `{pointer}` — \"{item.evidence}\"")
        if item.destination:
            lines.append(f"  - suggested destination: {LAYER_LABELS[item.destination]}")
        lines.append(f"  - confidence/strength: {item.confidence}")
        if item.reason:
            lines.append(f"  - note: {item.reason}")
        lines.append("")
    return "\n".join(lines)


def render_note(transcript_path: pathlib.Path, items: list[Item]) -> str:
    grouped: dict[str, list[Item]] = {key: [] for key, _ in SECTIONS}
    for item in sorted(items, key=lambda item: (-item.score, item.line_start, item.statement)):
        grouped[item.section].append(item)

    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    out: list[str] = [
        "# Transcript Review Note",
        "",
        f"- source: `{transcript_path}`",
        f"- generated_at: `{now}`",
        "- mode: local heuristic review; advisory only",
        "- note: this output proposes candidates and residue for human review. It does not auto-promote anything.",
        "",
    ]
    for key, title in SECTIONS:
        out.append(render_section(grouped[key], title))
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    transcript_path = pathlib.Path(args.transcript).expanduser().resolve()
    if not transcript_path.exists():
        raise SystemExit(f"Transcript not found: {transcript_path}")

    output_path = pathlib.Path(args.output).expanduser().resolve() if args.output else transcript_path.with_suffix(".review.md")
    lines = load_lines(transcript_path)
    items = collect_items(lines)

    capped: list[Item] = []
    counts = {key: 0 for key, _ in SECTIONS}
    for item in sorted(items, key=lambda item: (-item.score, item.line_start, item.statement)):
        if counts[item.section] >= args.max_items_per_section:
            continue
        capped.append(item)
        counts[item.section] += 1

    note = render_note(transcript_path, capped)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(note, encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
