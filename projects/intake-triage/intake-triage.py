#!/usr/bin/env python3
"""
intake-triage: Read manual intake items and emit structured triage review surface.
"""

import json
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


DISPOSITIONS = [
    "respond-soon",
    "actionable",
    "note-candidate",
    "project-candidate",
    "ambient",
    "ignore",
    "unclear"
]


def parse_intake_file(file_path: str) -> List[Dict]:
    """Parse JSONL intake file and return list of items."""
    items = []
    path = Path(file_path)

    if not path.exists():
        print(f"Error: Input file not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            try:
                item = json.loads(line)
                if 'text' not in item:
                    print(f"Warning: Line {line_num} missing 'text' field, skipping", file=sys.stderr)
                    continue
                items.append(item)
            except json.JSONDecodeError as e:
                print(f"Warning: Line {line_num} invalid JSON, skipping: {e}", file=sys.stderr)
                continue

    return items


def extract_urgency_signals(text: str) -> List[str]:
    """Extract urgency-related cues from text."""
    signals = []
    text_lower = text.lower()

    urgency_patterns = [
        (r'\basap\b', 'asap'),
        (r'\burgent\b', 'urgent'),
        (r'\bimmediately\b', 'immediately'),
        (r'\btoday\b', 'today'),
        (r'\bdeadline\b', 'deadline'),
        (r'\boverdue\b', 'overdue'),
        (r'\bcritical\b', 'critical'),
        (r'\bemergency\b', 'emergency'),
    ]

    for pattern, label in urgency_patterns:
        if re.search(pattern, text_lower):
            signals.append(label)

    return signals


def extract_question_signals(text: str) -> bool:
    """Check if text contains question markers."""
    if '?' in text:
        return True

    question_starters = [
        r'\bhow\s',
        r'\bwhat\s',
        r'\bwhen\s',
        r'\bwhere\s',
        r'\bwhy\s',
        r'\bwho\s',
        r'\bcan\s+you\b',
        r'\bcould\s+you\b',
        r'\bwould\s+you\b',
        r'\bshould\s+we\b',
    ]

    text_lower = text.lower()
    for pattern in question_starters:
        if re.search(pattern, text_lower):
            return True

    return False


def extract_observation_signals(text: str) -> bool:
    """Check if text looks like an observation or insight."""
    observation_patterns = [
        r'\bnoticed\b',
        r'\bobserved\b',
        r'\bpattern in\b',
        r'\binteresting pattern\b',
        r'\bseems like\b',
        r'\bappears\b',
        r'\btrend\b',
        r'\binsight\b',
    ]

    text_lower = text.lower()
    for pattern in observation_patterns:
        if re.search(pattern, text_lower):
            return True

    return False


def extract_project_signals(text: str) -> bool:
    """Check if text suggests a larger project or initiative."""
    project_patterns = [
        r'\bproject\b',
        r'\binitiative\b',
        r'\bproposal\b',
        r'\bwe should build\b',
        r'\bwe could create\b',
        r'\bnew feature\b',
        r'\bsystem for\b',
        r'\bframework\b',
        r'\barchitecture\b',
    ]

    text_lower = text.lower()
    for pattern in project_patterns:
        if re.search(pattern, text_lower):
            return True

    return False


def extract_ambient_signals(text: str) -> bool:
    """Check if text is ambient context or FYI."""
    ambient_patterns = [
        r'\bfyi\b',
        r'\bfor your information\b',
        r'\bheads up\b',
        r'\bjust so you know\b',
        r'\bbackground:\b',
        r'\bcontext:\b',
    ]

    text_lower = text.lower()
    for pattern in ambient_patterns:
        if re.search(pattern, text_lower):
            return True

    return False


def extract_ignore_signals(text: str) -> bool:
    """Check if text should likely be ignored."""
    ignore_patterns = [
        r'\bunsubscribe\b',
        r'\bspam\b',
        r'\btest\s+message\b',
        r'\bnever mind\b',
        r'\bignore\b',
        r'\bdisregard\b',
    ]

    text_lower = text.lower()
    for pattern in ignore_patterns:
        if re.search(pattern, text_lower):
            return True

    # Very short items with no clear signal
    if len(text.strip()) < 10:
        return True

    return False


def triage_item(item: Dict) -> Dict:
    """
    Apply heuristics to determine disposition, urgency, confidence, and rationale.

    Returns a dict with:
    - disposition: one of DISPOSITIONS
    - urgency: high/medium/low/none
    - confidence: high/medium/low
    - rationale: str
    - hooks: list of extracted cues (optional)
    """
    text = item.get('text', '')
    source = item.get('source', '')

    hooks = []
    urgency_signals = extract_urgency_signals(text)
    is_question = extract_question_signals(text)
    is_observation = extract_observation_signals(text)
    is_project = extract_project_signals(text)
    is_ambient = extract_ambient_signals(text)
    is_ignore = extract_ignore_signals(text)

    if urgency_signals:
        hooks.extend(urgency_signals)

    # Apply disposition logic
    disposition = "unclear"
    urgency = "none"
    confidence = "medium"
    rationale = ""

    # Check ignore first
    if is_ignore:
        disposition = "ignore"
        urgency = "none"
        confidence = "medium"
        rationale = "Appears to be spam, test, or not relevant"

    # Check ambient
    elif is_ambient:
        disposition = "ambient"
        urgency = "none"
        confidence = "high"
        rationale = "Background context or FYI, no action required"

    # Check note candidate for observations (before questions, since observations can contain question-like phrasing)
    elif is_observation:
        disposition = "note-candidate"
        urgency = "low"
        confidence = "high"
        rationale = "Observational insight worth capturing"

    # Check respond-soon (urgency signals first)
    elif urgency_signals:
        disposition = "respond-soon"
        urgency = "high"
        confidence = "high"
        if is_question:
            rationale = "Direct question with urgency indicators"
        else:
            rationale = "Contains urgency indicators requiring timely response"

    # Check respond-soon (questions without urgency)
    elif is_question:
        disposition = "respond-soon"
        urgency = "medium"
        confidence = "high"
        rationale = "Direct question requiring response"

    # Check actionable (request patterns without urgency)
    elif any(word in text.lower() for word in ['please', 'need to', 'should', 'must', 'required']):
        disposition = "actionable"
        urgency = "low"
        confidence = "medium"
        rationale = "Contains action language or request"

    # Check project candidate
    elif is_project:
        disposition = "project-candidate"
        urgency = "low"
        confidence = "medium"
        rationale = "Suggests larger project or initiative"

    # Check for vague or unclear items
    elif len(text.strip()) < 20:
        disposition = "unclear"
        urgency = "none"
        confidence = "low"
        rationale = "Too short or vague to determine disposition"

    # Default to note-candidate for longer descriptive text
    elif len(text.split()) > 10:
        disposition = "note-candidate"
        urgency = "low"
        confidence = "low"
        rationale = "Descriptive text without clear action or urgency"

    # Truly unclear
    else:
        disposition = "unclear"
        urgency = "none"
        confidence = "low"
        rationale = "Cannot determine clear disposition from available information"

    result = {
        'disposition': disposition,
        'urgency': urgency,
        'confidence': confidence,
        'rationale': rationale,
    }

    if hooks:
        result['hooks'] = hooks

    return result


def generate_markdown_output(triaged_items: List[Dict], output_path: Path) -> None:
    """Generate human-readable markdown triage surface."""
    lines = []

    # Header
    lines.append("# Intake Triage Review")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Total items: {len(triaged_items)}")
    lines.append("")

    # Summary by disposition
    disposition_counts = {}
    for item in triaged_items:
        disp = item['triage']['disposition']
        disposition_counts[disp] = disposition_counts.get(disp, 0) + 1

    lines.append("## Summary")
    lines.append("")
    for disp in DISPOSITIONS:
        count = disposition_counts.get(disp, 0)
        lines.append(f"- **{disp}**: {count}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group items by disposition
    grouped = {}
    for item in triaged_items:
        disp = item['triage']['disposition']
        if disp not in grouped:
            grouped[disp] = []
        grouped[disp].append(item)

    # Output each disposition group
    for disp in DISPOSITIONS:
        if disp not in grouped:
            continue

        items = grouped[disp]
        lines.append(f"## {disp}")
        lines.append("")

        for idx, item in enumerate(items, 1):
            lines.append(f"### Item {idx}")
            lines.append(f"**Text:** {item['text']}")

            if 'source' in item:
                lines.append(f"**Source:** {item['source']}")

            if 'timestamp' in item:
                lines.append(f"**Timestamp:** {item['timestamp']}")

            triage = item['triage']
            lines.append(f"**Urgency:** {triage['urgency']}")
            lines.append(f"**Confidence:** {triage['confidence']}")
            lines.append(f"**Rationale:** {triage['rationale']}")

            if 'hooks' in triage:
                lines.append(f"**Hooks:** {', '.join(triage['hooks'])}")

            if 'context' in item:
                lines.append(f"**Context:** {item['context']}")

            lines.append("")

        lines.append("---")
        lines.append("")

    # Write to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Markdown review surface written to: {output_path}")


def generate_json_output(triaged_items: List[Dict], output_path: Path) -> None:
    """Generate machine-readable JSON companion file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_data = {
        'generated': datetime.now().isoformat(),
        'total_items': len(triaged_items),
        'items': triaged_items
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"JSON output written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Intake triage tool: read intake items and emit structured triage surface'
    )
    parser.add_argument('input', help='Input JSONL file with intake items')
    parser.add_argument('--output', default='triage/', help='Output directory (default: triage/)')
    parser.add_argument('--json', action='store_true', help='Also emit JSON companion file')

    args = parser.parse_args()

    # Parse input
    items = parse_intake_file(args.input)

    if not items:
        print("No valid items found in input file", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(items)} items from {args.input}")

    # Triage each item
    triaged_items = []
    for item in items:
        triage_result = triage_item(item)
        triaged_item = {**item, 'triage': triage_result}
        triaged_items.append(triaged_item)

    # Generate outputs
    output_dir = Path(args.output)
    md_path = output_dir / 'current.md'
    generate_markdown_output(triaged_items, md_path)

    if args.json:
        json_path = output_dir / 'current.json'
        generate_json_output(triaged_items, json_path)

    print("\nTriage complete.")


if __name__ == '__main__':
    main()
