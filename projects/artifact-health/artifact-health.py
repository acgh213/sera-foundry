#!/usr/bin/env python3
"""
Artifact Health Report

A diagnostic CLI that analyzes the structural health of the artifact ecosystem
in the Sera Foundry. Reports on content-health signals first, then a secondary
layer of broader archive roughness and conventions worth watching.

Text-first output with optional JSON reporting.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


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


def is_structural_artifact(artifact: dict) -> bool:
    """Check if artifact is structural (foundry items) and not subject to tagging."""
    kind = artifact.get("kind", "")
    return kind in ["foundry_project", "foundry_note"]


def is_conventional_untagged(artifact: dict) -> bool:
    """Check if artifact type conventionally has no tags (e.g., pages)."""
    kind = artifact.get("kind", "")
    return kind == "page"


def is_content_artifact(artifact: dict) -> bool:
    """Artifacts that should participate in content-health tagging checks."""
    return not is_structural_artifact(artifact) and not is_conventional_untagged(artifact)


def analyze_untagged(artifacts: list[dict]) -> tuple[list[dict], int]:
    """Find content artifacts (posts, etc.) with no tags."""
    untagged = []
    count = 0
    for artifact in artifacts:
        if not is_content_artifact(artifact):
            continue

        tags = artifact.get("tags")
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
    """Find content artifacts with very few tags (weak ecosystem connection)."""
    weak = []
    for artifact in artifacts:
        if not is_content_artifact(artifact):
            continue

        tags = artifact.get("tags") or []
        if isinstance(tags, list) and len(tags) <= threshold:
            weak.append(artifact)
    return weak


def analyze_bridge_artifacts(artifacts: list[dict], tag_freq: dict[str, int], threshold_pct: float = 70.0) -> list[dict]:
    """
    Find 'bridge' artifacts that:
    - Have 3+ tags (real multi-dimensional connection)
    - Connect disparate parts of the archive via shared tagging

    Excludes foundry items and pages (structural, not ecosystem bridges).
    """
    if not tag_freq:
        return []

    sorted_tags = sorted(tag_freq.items(), key=lambda x: x[1], reverse=True)
    total_unique_tags = len(sorted_tags)
    top_count = max(1, int(total_unique_tags * threshold_pct / 100))
    top_tags = set(tag for tag, _ in sorted_tags[:top_count])

    bridges = []
    for artifact in artifacts:
        if not is_content_artifact(artifact):
            continue

        tags = artifact.get("tags") or []
        if isinstance(tags, list) and len(tags) >= 3 and all(t in top_tags for t in tags):
            bridges.append(artifact)

    return bridges


def analyze_metadata_gaps(artifacts: list[dict]) -> list[dict]:
    """Find artifacts with missing or null critical metadata."""
    gaps = []
    for artifact in artifacts:
        kind = artifact.get("kind", "")
        issues = []

        if not artifact.get("title"):
            issues.append("missing title")
        if not artifact.get("path"):
            issues.append("missing path")
        if artifact.get("kind") is None:
            issues.append("null kind")

        if not is_structural_artifact(artifact) and artifact.get("tags") is None:
            issues.append("null tags (should be list or empty)")

        if kind not in ["foundry_project", "foundry_note", "page"] and not artifact.get("mode"):
            issues.append("missing mode")

        if issues:
            gaps.append({
                "artifact": artifact,
                "issues": issues,
            })

    return gaps


def infer_staleness(artifacts: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """
    Infer staleness from available signals:
    - posts marked published=False (explicit draft/dormant)
    - pages marked published=False (worth watching, but not a content-health failure)
    - posts with null published status (stale candidates)

    Returns (stale_candidates, unpublished_posts, unpublished_pages)
    """
    stale_candidates = []
    unpublished_posts = []
    unpublished_pages = []

    for artifact in artifacts:
        kind = artifact.get("kind", "")
        published = artifact.get("published")

        if kind in ["foundry_project", "foundry_note"]:
            continue

        if kind == "post" and published is False:
            unpublished_posts.append(artifact)
        elif kind == "page" and published is False:
            unpublished_pages.append(artifact)

        if kind == "post" and published is None:
            stale_candidates.append(artifact)

    return stale_candidates, unpublished_posts, unpublished_pages


def analyze_archive_roughness(artifacts: list[dict], tag_freq: dict[str, int]) -> dict:
    """
    Capture broader archive roughness without treating it as primary content failure.

    These signals are intentionally simple and inspectable. They describe early-stage
    sparsity, structural exclusions, and conventions that still shape how the archive feels.
    """
    pages = [a for a in artifacts if a.get("kind") == "page"]
    structural = [a for a in artifacts if is_structural_artifact(a)]
    singleton_tags = sorted((tag, count) for tag, count in tag_freq.items() if count == 1)

    content_artifacts = [a for a in artifacts if is_content_artifact(a)]
    content_with_singleton_tags = []
    for artifact in content_artifacts:
        tags = artifact.get("tags") or []
        if any(tag_freq.get(tag, 0) == 1 for tag in tags):
            content_with_singleton_tags.append(artifact)

    unpublished_pages = [a for a in pages if a.get("published") is False]

    return {
        "conventionally_untagged_pages": pages,
        "structural_artifacts": structural,
        "singleton_tags": singleton_tags,
        "content_with_singleton_tags": content_with_singleton_tags,
        "unpublished_pages": unpublished_pages,
    }


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

    lines.append("╭─ ARTIFACT HEALTH REPORT")
    lines.append(f"│ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"│ Total artifacts indexed: {len(artifacts)}")
    lines.append("")

    untagged, untagged_count = analyze_untagged(artifacts)
    tag_freq = analyze_tag_distribution(artifacts)
    weak = analyze_weak_connections(artifacts, threshold=1)
    bridges = analyze_bridge_artifacts(artifacts, tag_freq)
    gaps = analyze_metadata_gaps(artifacts)
    stale_cand, unpublished_posts, unpublished_pages = infer_staleness(artifacts)
    roughness = analyze_archive_roughness(artifacts, tag_freq)

    content_artifacts = [a for a in artifacts if is_content_artifact(a)]
    publishable = [a for a in artifacts if a.get("kind") in ["post", "page"]]
    published_count = sum(1 for a in publishable if a.get("published") is True)
    avg_content_tags = (
        sum(len(a.get("tags") or []) for a in content_artifacts) / len(content_artifacts)
        if content_artifacts else 0
    )

    lines.append("╭─ UNTAGGED CONTENT (posts, etc.)")
    lines.append(f"│ Count: {untagged_count}")
    if untagged_count > 0:
        lines.append("│ Issue: Content without tags is disconnected from the ecosystem")
        lines.append("│")
        for artifact in untagged[:10]:
            lines.append(format_artifact_line(artifact, "│ "))
        if untagged_count > 10:
            lines.append(f"│ ... and {untagged_count - 10} more")
    else:
        lines.append("│ ✓ All content artifacts are tagged")
    lines.append("")

    lines.append("╭─ WEAKLY CONNECTED CONTENT (single tag)")
    lines.append(f"│ Count: {len(weak)}")
    if weak:
        lines.append("│ Issue: Content with only 1 tag has limited ecosystem connection")
        lines.append("│")
        for artifact in weak[:10]:
            lines.append(format_artifact_line(artifact, "│ "))
        if len(weak) > 10:
            lines.append(f"│ ... and {len(weak) - 10} more")
    else:
        lines.append("│ ✓ All content artifacts have multi-tag connection")
    lines.append("")

    lines.append("╭─ BRIDGE ARTIFACTS (ecosystem connectors)")
    lines.append(f"│ Count: {len(bridges)} (3+ tags, high-frequency)")
    if bridges:
        lines.append("│ Insight: These artifacts connect disparate sections of the archive")
        lines.append("│")
        for artifact in bridges[:5]:
            lines.append(format_artifact_line(artifact, "│ "))
        if len(bridges) > 5:
            lines.append(f"│ ... and {len(bridges) - 5} more")
    else:
        lines.append("│ (None detected—ecosystem may be compartmentalized)")
    lines.append("")

    lines.append("╭─ METADATA GAPS")
    lines.append(f"│ Count: {len(gaps)} artifact(s) with missing/null fields")
    if gaps:
        lines.append("│")
        for item in gaps[:10]:
            artifact = item["artifact"]
            issue_str = ", ".join(item["issues"])
            lines.append(f"│ • {artifact.get('title', '?')} [{artifact.get('kind', '?')}]")
            lines.append(f"│   issues: {issue_str}")
        if len(gaps) > 10:
            lines.append(f"│ ... and {len(gaps) - 10} more")
    else:
        lines.append("│ ✓ All artifacts have complete core metadata")
    lines.append("")

    lines.append("╭─ CONTENT STATE")
    lines.append(f"│ Published artifacts: {published_count}/{len(publishable)}")
    lines.append(f"│ Unpublished posts/drafts: {len(unpublished_posts)}")
    lines.append(f"│ Stale post candidates (null state): {len(stale_cand)}")
    if unpublished_posts:
        lines.append("│")
        lines.append("│ Unpublished posts/drafts:")
        for artifact in unpublished_posts[:5]:
            lines.append(f"│ • {artifact.get('title', '?')} [{artifact.get('kind', '?')}]")
        if len(unpublished_posts) > 5:
            lines.append(f"│ ... and {len(unpublished_posts) - 5} more")
    lines.append("")

    lines.append("╭─ TAG ECOSYSTEM (content view)")
    lines.append(f"│ Unique tags: {len(tag_freq)}")
    lines.append(f"│ Average tags per content artifact: {avg_content_tags:.1f}")
    if tag_freq:
        top_tags = sorted(tag_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        lines.append("│")
        lines.append("│ Top tags by frequency:")
        for tag, count in top_tags:
            lines.append(f"│ • {tag}: {count}")
    lines.append("")

    lines.append("╭─ BROADER ARCHIVE ROUGHNESS (context, not failure)")
    lines.append("│ These do not count as primary content-health failures.")
    lines.append("│ They are the rough edges and conventions still shaping the archive.")
    lines.append("│")
    lines.append(
        f"│ • {len(roughness['conventionally_untagged_pages'])} page(s) sit outside the tag ecosystem by convention"
    )
    lines.append(
        f"│ • {len(roughness['structural_artifacts'])} foundry artifact(s) are structural and excluded from publication/tagging checks"
    )
    singleton_count = len(roughness["singleton_tags"])
    if tag_freq:
        lines.append(
            f"│ • {singleton_count}/{len(tag_freq)} tags appear only once; the archive vocabulary is still sparse"
        )
    singleton_content = roughness["content_with_singleton_tags"]
    if content_artifacts:
        lines.append(
            f"│ • {len(singleton_content)}/{len(content_artifacts)} content artifact(s) still rely on at least one one-off tag"
        )
    if unpublished_pages:
        lines.append("│ • Unpublished pages worth watching:")
        for artifact in unpublished_pages[:5]:
            lines.append(f"│   - {artifact.get('title', '?')} [{artifact.get('kind', '?')}]")
    if roughness["singleton_tags"]:
        preview = ", ".join(tag for tag, _ in roughness["singleton_tags"][:8])
        lines.append(f"│ • One-off tags (sample): {preview}")
    lines.append("")

    lines.append("╭─ OVERALL ASSESSMENT")
    content_issues = []
    context_notes = []

    if untagged_count > 0 and content_artifacts:
        pct = (untagged_count / len(content_artifacts)) * 100
        content_issues.append(f"{untagged_count} untagged content items ({pct:.0f}%)")
    if weak and content_artifacts:
        pct = (len(weak) / len(content_artifacts)) * 100
        content_issues.append(f"{len(weak)} single-tag items ({pct:.0f}%)")
    if gaps:
        content_issues.append(f"metadata gaps in {len(gaps)} artifact(s)")

    if roughness["singleton_tags"] and tag_freq:
        context_notes.append(
            f"tag reuse is still thin ({len(roughness['singleton_tags'])}/{len(tag_freq)} tags are one-offs)"
        )
    if unpublished_pages:
        page_word = "page remains" if len(unpublished_pages) == 1 else "pages remain"
        context_notes.append(f"{len(unpublished_pages)} unpublished {page_word} outside the main content lane")
    if not bridges:
        context_notes.append("no bridge artifacts detected yet")

    if unpublished_posts and content_artifacts:
        pct = (len(unpublished_posts) / len(content_artifacts)) * 100
        if pct > 33:
            content_issues.append(f"high unpublished post ratio: {len(unpublished_posts)}/{len(content_artifacts)} ({pct:.0f}%)")

    if not content_issues:
        lines.append("│ ✓ CONTENT HEALTHY")
        lines.append("│ • Primary content checks are clean: tags, connectivity, and metadata look solid")
        if publishable:
            lines.append(f"│ • {published_count}/{len(publishable)} publishable artifacts are live")
    else:
        lines.append("│ ⚠ CONTENT ATTENTION NEEDED")
        for issue in content_issues:
            lines.append(f"│ • {issue}")

    if context_notes:
        lines.append("│")
        lines.append("│ Roughness worth keeping in view:")
        for note in context_notes:
            lines.append(f"│ • {note}")

    lines.append("│")
    lines.append("│ Note: pages and foundry artifacts are handled as conventions/context,")
    lines.append("│       not as automatic content-health failures.")
    lines.append("╰─")

    return "\n".join(lines)


def report_json(artifacts: list[dict]) -> str:
    """Generate JSON report."""
    untagged, untagged_count = analyze_untagged(artifacts)
    tag_freq = analyze_tag_distribution(artifacts)
    weak = analyze_weak_connections(artifacts, threshold=1)
    bridges = analyze_bridge_artifacts(artifacts, tag_freq)
    gaps = analyze_metadata_gaps(artifacts)
    stale_cand, unpublished_posts, unpublished_pages = infer_staleness(artifacts)
    roughness = analyze_archive_roughness(artifacts, tag_freq)

    content_artifacts = [a for a in artifacts if is_content_artifact(a)]

    report = {
        "timestamp": datetime.now().isoformat(),
        "total_artifacts": len(artifacts),
        "untagged": {
            "count": untagged_count,
            "examples": untagged[:5],
        },
        "weakly_connected": {
            "count": len(weak),
            "threshold": "1 or fewer tags",
            "examples": weak[:5],
        },
        "bridge_artifacts": {
            "count": len(bridges),
            "examples": bridges[:3],
        },
        "metadata_gaps": {
            "count": len(gaps),
            "issues": [{"artifact": item["artifact"], "issues": item["issues"]} for item in gaps[:5]],
        },
        "staleness": {
            "unpublished_posts": len(unpublished_posts),
            "unpublished_pages": len(unpublished_pages),
            "stale_post_candidates": len(stale_cand),
            "post_examples": unpublished_posts[:3],
            "page_examples": unpublished_pages[:3],
        },
        "tag_ecosystem": {
            "unique_tags": len(tag_freq),
            "avg_tags_per_content_artifact": (
                sum(len(a.get("tags") or []) for a in content_artifacts) / len(content_artifacts)
                if content_artifacts else 0
            ),
            "top_tags": dict(sorted(tag_freq.items(), key=lambda x: x[1], reverse=True)[:15]),
        },
        "archive_roughness": {
            "conventionally_untagged_pages": len(roughness["conventionally_untagged_pages"]),
            "structural_artifacts": len(roughness["structural_artifacts"]),
            "singleton_tags": {
                "count": len(roughness["singleton_tags"]),
                "sample": [tag for tag, _ in roughness["singleton_tags"][:10]],
            },
            "content_with_singleton_tags": {
                "count": len(roughness["content_with_singleton_tags"]),
                "examples": roughness["content_with_singleton_tags"][:5],
            },
            "unpublished_pages": roughness["unpublished_pages"][:5],
        },
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
        help="Output format (default: text)",
    )

    return parser


def main():
    """Entry point."""
    parser = build_parser()
    args = parser.parse_args()
    status(args)


if __name__ == "__main__":
    main()
