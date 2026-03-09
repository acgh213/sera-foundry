#!/usr/bin/env python3
"""
Artifact Health Report

A diagnostic CLI that analyzes the structural health of the artifact ecosystem
in the Sera Foundry. Reports on untagged artifacts, weak connections, bridges,
stale entries, and metadata gaps.

Text-first output with optional JSON reporting.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


INDEX_FILE = Path("projects/workbench/data/index.json")


@dataclass
class HealthMetrics:
    """Summary of artifact ecosystem health."""
    total_artifacts: int
    untagged: int
    weakly_connected: int
    bridge_artifacts: int
    stale_entries: int
    null_metadata_count: int


def load_index() -> dict:
    """Load the workbench index."""
    if not INDEX_FILE.exists():
        raise SystemExit(f"Index not found at {INDEX_FILE}")
    return json.loads(INDEX_FILE.read_text(encoding="utf-8"))


def classify_artifact(artifact: dict) -> str:
    """Classify artifact by kind, with special handling for null/missing values."""
    kind = artifact.get("kind", "unknown")
    if kind in ["foundry_project", "foundry_note"]:
        return f"{kind} (no tags)"
    return kind


def analyze_untagged(artifacts: list[dict]) -> tuple[list[dict], int]:
    """Find artifacts with no tags or empty tag lists."""
    untagged = []
    count = 0
    for artifact in artifacts:
        tags = artifact.get("tags")
        # null, None, [], or missing = untagged
        if not tags:
            untagged.append(artifact)
            count += 1
    return untagged, count


def analyze_tag_distribution(artifacts: list[dict]) -> dict[str, int]:
    """Get frequency of tags across all artifacts."""
    tag_freq = Counter()
    for artifact in artifacts:
        tags = artifact.get("tags") or []
        if isinstance(tags, list):
            tag_freq.update(tags)
    return dict(tag_freq)


def analyze_weak_connections(artifacts: list[dict], threshold: int = 1) -> list[dict]:
    """Find artifacts with very few tags (indicating weak connection to ecosystem)."""
    weak = []
    for artifact in artifacts:
        tags = artifact.get("tags") or []
        if isinstance(tags, list) and len(tags) <= threshold:
            weak.append(artifact)
    return weak


def analyze_bridge_artifacts(artifacts: list[dict], tag_freq: dict[str, int], threshold_pct: float = 70.0) -> list[dict]:
    """
    Find 'bridge' artifacts that:
    - Have multiple tags
    - Connect disparate parts of the archive via shared tagging
    
    A bridge artifact is one whose tags are individually common (top tier),
    connecting otherwise isolated groups.
    """
    if not tag_freq:
        return []
    
    # Top threshold% of tags by frequency
    sorted_tags = sorted(tag_freq.items(), key=lambda x: x[1], reverse=True)
    total_unique_tags = len(sorted_tags)
    top_count = max(1, int(total_unique_tags * threshold_pct / 100))
    top_tags = set(tag for tag, _ in sorted_tags[:top_count])
    
    bridges = []
    for artifact in artifacts:
        tags = artifact.get("tags") or []
        if isinstance(tags, list):
            # Must have 2+ tags, all from top tier
            if len(tags) >= 2 and all(t in top_tags for t in tags):
                bridges.append(artifact)
    
    return bridges


def analyze_metadata_gaps(artifacts: list[dict]) -> list[dict]:
    """Find artifacts with missing or null critical metadata."""
    gaps = []
    for artifact in artifacts:
        issues = []
        
        # Check for null/missing fields
        if not artifact.get("title"):
            issues.append("missing title")
        if not artifact.get("path"):
            issues.append("missing path")
        if artifact.get("kind") is None:
            issues.append("null kind")
        if artifact.get("tags") is None:
            issues.append("null tags")
        
        # Special checks for foundry items (expect no mode/published)
        kind = artifact.get("kind", "")
        if kind not in ["foundry_project", "foundry_note"]:
            if not artifact.get("mode"):
                issues.append("missing mode")
        
        if issues:
            gaps.append({
                "artifact": artifact,
                "issues": issues
            })
    
    return gaps


def infer_staleness(artifacts: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Infer staleness from available signals:
    - foundry_note / foundry_project with no published field (passive)
    - posts marked published=False (explicit draft/dormant)
    
    Returns (stale_candidates, unpublished_drafts)
    """
    stale_candidates = []
    unpublished_drafts = []
    
    for artifact in artifacts:
        kind = artifact.get("kind", "")
        published = artifact.get("published")
        
        # Foundry items are structural, not "stale"
        if kind in ["foundry_project", "foundry_note"]:
            continue
        
        # Explicit draft status
        if published is False:
            unpublished_drafts.append(artifact)
        
        # Posts with null published status might be stale
        if kind == "post" and published is None:
            stale_candidates.append(artifact)
    
    return stale_candidates, unpublished_drafts


def format_artifact_line(artifact: dict, indent: str = "  ") -> str:
    """Format an artifact as a readable line."""
    title = artifact.get("title", "?")
    kind = artifact.get("kind", "unknown")
    tags = artifact.get("tags") or []
    
    tag_str = ", ".join(tags) if tags else "-"
    path = artifact.get("path", "")
    
    return f"{indent}• {title} [{kind}]\n{indent}  tags: {tag_str}\n{indent}  path: {path}"


def report_text(artifacts: list[dict]) -> str:
    """Generate human-readable text report."""
    lines = []
    
    # Basic counts
    lines.append("╭─ ARTIFACT HEALTH REPORT")
    lines.append(f"│ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"│ Total artifacts indexed: {len(artifacts)}")
    lines.append("")
    
    # Analyze all dimensions
    untagged, untagged_count = analyze_untagged(artifacts)
    tag_freq = analyze_tag_distribution(artifacts)
    weak = analyze_weak_connections(artifacts, threshold=1)
    bridges = analyze_bridge_artifacts(artifacts, tag_freq)
    gaps = analyze_metadata_gaps(artifacts)
    stale_cand, unpublished = infer_staleness(artifacts)
    
    # Untagged section
    lines.append("╭─ UNTAGGED ARTIFACTS")
    lines.append(f"│ Count: {untagged_count}")
    if untagged_count > 0:
        lines.append("│")
        for artifact in untagged[:10]:  # Show first 10
            formatted = format_artifact_line(artifact, "│ ")
            lines.append(formatted)
        if untagged_count > 10:
            lines.append(f"│ ... and {untagged_count - 10} more")
    else:
        lines.append("│ ✓ All artifacts are tagged")
    lines.append("")
    
    # Weakly connected
    lines.append("╭─ WEAKLY CONNECTED ARTIFACTS")
    lines.append(f"│ Count: {len(weak)} (1 or fewer tags)")
    if len(weak) > 0:
        lines.append("│")
        for artifact in weak[:10]:
            formatted = format_artifact_line(artifact, "│ ")
            lines.append(formatted)
        if len(weak) > 10:
            lines.append(f"│ ... and {len(weak) - 10} more")
    else:
        lines.append("│ ✓ Good connectivity across ecosystem")
    lines.append("")
    
    # Bridge artifacts
    lines.append("╭─ BRIDGE ARTIFACTS")
    lines.append(f"│ Count: {len(bridges)} (multiple tags, high-frequency)")
    if len(bridges) > 0:
        lines.append("│")
        for artifact in bridges[:5]:
            formatted = format_artifact_line(artifact, "│ ")
            lines.append(formatted)
        if len(bridges) > 5:
            lines.append(f"│ ... and {len(bridges) - 5} more")
    else:
        lines.append("│ (None detected in this archive)")
    lines.append("")
    
    # Metadata gaps
    lines.append("╭─ METADATA GAPS")
    lines.append(f"│ Count: {len(gaps)} artifact(s) with missing/null fields")
    if len(gaps) > 0:
        lines.append("│")
        for item in gaps[:10]:
            artifact = item["artifact"]
            issues = item["issues"]
            title = artifact.get("title", "?")
            issue_str = ", ".join(issues)
            lines.append(f"│ • {title}")
            lines.append(f"│   issues: {issue_str}")
        if len(gaps) > 10:
            lines.append(f"│ ... and {len(gaps) - 10} more")
    else:
        lines.append("│ ✓ All artifacts have complete core metadata")
    lines.append("")
    
    # Staleness signals
    lines.append("╭─ STALENESS SIGNALS")
    lines.append(f"│ Unpublished drafts: {len(unpublished)}")
    lines.append(f"│ Stale candidates (null published): {len(stale_cand)}")
    if unpublished:
        lines.append("│")
        lines.append("│ Unpublished drafts:")
        for artifact in unpublished[:5]:
            title = artifact.get("title", "?")
            lines.append(f"│ • {title}")
        if len(unpublished) > 5:
            lines.append(f"│ ... and {len(unpublished) - 5} more")
    lines.append("")
    
    # Tag ecosystem summary
    lines.append("╭─ TAG ECOSYSTEM")
    lines.append(f"│ Unique tags: {len(tag_freq)}")
    lines.append(f"│ Average tags per artifact: {sum(len(a.get('tags') or []) for a in artifacts) / len(artifacts):.1f}")
    if tag_freq:
        top_tags = sorted(tag_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        lines.append("│")
        lines.append("│ Top tags by frequency:")
        for tag, count in top_tags:
            lines.append(f"│ • {tag}: {count}")
    lines.append("")
    
    # Overall health
    lines.append("╭─ OVERALL HEALTH")
    health_issues = []
    if untagged_count > 0:
        health_issues.append(f"{untagged_count} untagged")
    if len(weak) > len(artifacts) * 0.2:
        health_issues.append("many weakly-connected")
    if len(gaps) > 0:
        health_issues.append("metadata gaps")
    
    if not health_issues:
        lines.append("│ ✓ HEALTHY - No major structural issues detected")
    else:
        lines.append(f"│ ⚠ AREAS TO ADDRESS: {', '.join(health_issues)}")
    
    lines.append("╰─")
    
    return "\n".join(lines)


def report_json(artifacts: list[dict]) -> str:
    """Generate JSON report."""
    untagged, untagged_count = analyze_untagged(artifacts)
    tag_freq = analyze_tag_distribution(artifacts)
    weak = analyze_weak_connections(artifacts, threshold=1)
    bridges = analyze_bridge_artifacts(artifacts, tag_freq)
    gaps = analyze_metadata_gaps(artifacts)
    stale_cand, unpublished = infer_staleness(artifacts)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_artifacts": len(artifacts),
        "untagged": {
            "count": untagged_count,
            "examples": untagged[:5]
        },
        "weakly_connected": {
            "count": len(weak),
            "threshold": "1 or fewer tags",
            "examples": weak[:5]
        },
        "bridge_artifacts": {
            "count": len(bridges),
            "examples": bridges[:3]
        },
        "metadata_gaps": {
            "count": len(gaps),
            "issues": [{"artifact": item["artifact"], "issues": item["issues"]} for item in gaps[:5]]
        },
        "staleness": {
            "unpublished_drafts": len(unpublished),
            "stale_candidates": len(stale_cand),
            "examples": unpublished[:3]
        },
        "tag_ecosystem": {
            "unique_tags": len(tag_freq),
            "avg_tags_per_artifact": sum(len(a.get("tags") or []) for a in artifacts) / len(artifacts) if artifacts else 0,
            "top_tags": dict(sorted(tag_freq.items(), key=lambda x: x[1], reverse=True)[:15])
        }
    }
    
    return json.dumps(report, indent=2)


def status(args):
    """Show workbench status with artifact health context."""
    index = load_index()
    artifacts = index.get("artifacts", [])
    
    if args.format == "json":
        print(report_json(artifacts))
    else:
        print(report_text(artifacts))


def build_parser():
    """Build argument parser."""
    parser = argparse.ArgumentParser(
        description="Artifact Health Report: analyze structural integrity of the archive."
    )
    
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    
    return parser


def main():
    """Entry point."""
    parser = build_parser()
    args = parser.parse_args()
    status(args)


if __name__ == "__main__":
    main()
