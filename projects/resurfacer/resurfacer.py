#!/usr/bin/env python3
"""
Resurfacer v0: A tool for surfacing older artifacts based on simple heuristics.

Resurfacer looks across the blog and foundry, preferring older materials,
avoiding recent picks, and using simple theme matching to suggest artifacts
worth revisiting.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
import re

import yaml

# Paths (relative to foundry root, which is the CWD when running this script)
INDEX_FILE = Path("projects/workbench/data/index.json")
STATE_FILE = Path("projects/resurfacer/data/resurfacer-state.json")

# Current ecosystem themes to look for
CURRENT_THEMES = {
    "continuity",
    "residue",
    "artifacts",
    "workbench",
    "postsmith",
    "projects",
    "drift",
    "memory",
    "archive",
    "persistence",
    "foundry",
}

# Active cluster themes (things you're working on right now)
# These should be de-prioritized to avoid over-resurfacing current work
ACTIVE_CLUSTER_THEMES = {
    "workbench",
    "postsmith",
    "foundry",
    "projects",
}

# Artifact kinds to consider (exclude certain types)
ARTIFACT_KINDS = {"post", "page", "foundry_project", "foundry_note"}
EXCLUDE_KINDS = set()  # empty for now; could exclude likes if needed

# Preferred minimum age for resurfacing (days)
PREFERRED_MIN_AGE_DAYS = 7


@dataclass
class ArtifactScore:
    artifact: dict
    score: float
    age_days: int
    theme_matches: list[str]
    reasons: list[str]


def parse_frontmatter(text: str):
    """Parse YAML frontmatter from markdown."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    front = text[3:end].strip()
    body = text[end + 3 :].lstrip("\n")
    meta = yaml.safe_load(front) or {}
    return meta, body


def extract_date_from_filename(path: str) -> datetime | None:
    """Try to extract date from filename like 2026-03-08-*."""
    match = re.search(r"(\d{4})-(\d{2})-(\d{2})", path)
    if match:
        try:
            return datetime.strptime(match.group(1) + match.group(2) + match.group(3), "%Y%m%d")
        except ValueError:
            pass
    return None


def ensure_dir(path: Path):
    """Create parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)


def load_index() -> dict:
    """Load the workbench-generated index."""
    if not INDEX_FILE.exists():
        return {"artifacts": []}
    try:
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return {"artifacts": []}


def load_state() -> dict:
    """Load resurfacing history state."""
    if not STATE_FILE.exists():
        return {"picks": [], "generated_at": None}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return {"picks": [], "generated_at": None}


def save_state(state: dict):
    """Save resurfacing history state."""
    ensure_dir(STATE_FILE)
    state["generated_at"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def get_artifact_date(artifact: dict, blog_repo: Path, foundry_repo: Path) -> datetime | None:
    """Extract date from artifact, trying filename first, then file mtime."""
    path = artifact.get("path", "")

    # Try filename first for blog-style dated files
    date = extract_date_from_filename(path)
    if date:
        return date

    # Fallback: actual file modification time
    root = foundry_repo if artifact.get("kind", "").startswith("foundry_") else blog_repo
    full_path = root / path
    if full_path.exists():
        return datetime.fromtimestamp(full_path.stat().st_mtime, tz=timezone.utc)

    return None


def calculate_days_since(date: datetime | None) -> int:
    """Calculate days since the date with a conservative fallback for unknown dates."""
    if not date:
        return 30

    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    delta = now - date
    return max(1, delta.days)


def extract_themes_from_artifact(artifact: dict) -> list[str]:
    """Extract matching themes from artifact fields."""
    matches = []
    
    # Check title, kind, tags, mode
    fields = [
        artifact.get("title", "").lower(),
        artifact.get("kind", "").lower(),
        " ".join(artifact.get("tags", []) or []).lower(),
        artifact.get("mode", "").lower(),
    ]
    
    combined = " ".join(fields)
    for theme in CURRENT_THEMES:
        if theme in combined:
            matches.append(theme)
    
    return list(set(matches))  # Remove duplicates


def score_artifact(artifact: dict, state: dict, now: datetime, blog_repo: Path, foundry_repo: Path, args=None) -> ArtifactScore | None:
    """Score a single artifact based on age, themes, history, and diversity."""
    
    # Skip excluded kinds
    if artifact.get("kind") in EXCLUDE_KINDS:
        return None
    
    # Skip if not in our considered kinds
    if artifact.get("kind") not in ARTIFACT_KINDS:
        return None
    
    # Apply optional filters
    if args:
        if args.kind and artifact.get("kind") != args.kind:
            return None
        if args.theme:
            theme_matches_all = extract_themes_from_artifact(artifact)
            if args.theme not in theme_matches_all:
                return None
    
    path = artifact.get("path", "")
    kind = artifact.get("kind", "")
    artifact_date = get_artifact_date(artifact, blog_repo, foundry_repo)
    age_days = calculate_days_since(artifact_date)
    
    # Base score: prefer older artifacts with score banding, but do not starve a young archive.
    # Very recent artifacts are penalized rather than excluded.
    if age_days < PREFERRED_MIN_AGE_DAYS:
        age_score = max(1.0, age_days * 0.8)
    elif age_days < 30:
        age_score = 10 + (age_days - PREFERRED_MIN_AGE_DAYS) * 0.4
    elif age_days < 90:
        age_score = 20 + (age_days - 30) * 0.25
    else:
        age_score = min(35 + (age_days - 90) * 0.1, 50)
    
    # Theme score: bonus for matching current themes
    theme_matches = extract_themes_from_artifact(artifact)
    theme_score = len(theme_matches) * 3

    # Freshness penalty: recent artifacts can still surface, but need stronger justification.
    if age_days < PREFERRED_MIN_AGE_DAYS:
        theme_score *= 0.5

    # Active cluster penalty: reduce score if heavily weighted toward active work themes
    active_theme_count = len([t for t in theme_matches if t in ACTIVE_CLUSTER_THEMES])
    if active_theme_count > 0:
        cluster_penalty = active_theme_count * 5  # 5 points per active cluster theme
        theme_score = max(0, theme_score - cluster_penalty)
    
    # Diversity bonus: prefer kinds not picked recently
    recent_picks = state.get("picks", [])
    kind_penalty = 0
    kind_counts = defaultdict(int)
    for pick in recent_picks[-10:]:  # Look at last 10 picks
        picked_kind = pick.get("kind", "")
        kind_counts[picked_kind] += 1
    
    # Heavy penalty if this kind was picked multiple times recently
    if kind in kind_counts:
        if kind_counts[kind] >= 3:
            kind_penalty = 6   # noticeable, not catastrophic, in a small archive
        elif kind_counts[kind] >= 2:
            kind_penalty = 3
        else:
            kind_penalty = 1
    
    # History penalty: if we've picked this exact artifact recently, penalize heavily
    artifact_penalty = 0
    for pick in recent_picks[-10:]:
        if pick.get("path") == path:
            days_since_pick = (now - datetime.fromisoformat(pick.get("picked_at", "2000-01-01"))).days
            if days_since_pick < 14:
                artifact_penalty = 12
                break
            elif days_since_pick < 30:
                artifact_penalty = 6
                break
            elif days_since_pick < 60:
                artifact_penalty = 3
                break
    
    final_score = age_score + theme_score - kind_penalty - artifact_penalty
    
    # Build reasons list
    reasons = []
    if age_days >= 90:
        reasons.append(f"old artifact ({age_days} days)")
    elif age_days >= 30:
        reasons.append(f"aging artifact ({age_days} days)")
    elif age_days >= PREFERRED_MIN_AGE_DAYS:
        reasons.append(f"mature enough to resurface ({age_days} days)")
    else:
        reasons.append(f"recent artifact with sufficient thematic pull ({age_days} days)")
    
    if theme_matches:
        non_active = [t for t in theme_matches if t not in ACTIVE_CLUSTER_THEMES]
        if non_active:
            reasons.append(f"matches non-active themes: {', '.join(non_active)}")
        if active_theme_count > 0:
            reasons.append(f"reduced weight for active cluster themes")
    
    if kind_penalty == 0:
        reasons.append(f"kind '{kind}' not over-represented recently")
    elif kind_penalty > 0:
        reasons.append(f"kind '{kind}' picked recently (diversity penalty applied)")
    
    if artifact_penalty == 0:
        reasons.append("not picked recently")
    
    return ArtifactScore(
        artifact=artifact,
        score=final_score,
        age_days=age_days,
        theme_matches=theme_matches,
        reasons=reasons,
    )


def run(args):
    """Main entry point: surface one artifact."""
    
    blog_repo = Path(args.blog_repo).expanduser().resolve()
    foundry_repo = Path(args.foundry_repo).expanduser().resolve()
    
    # Load index and state
    index = load_index()
    state = load_state()
    
    now = datetime.now(timezone.utc)
    
    # Score all artifacts
    candidates = []
    for artifact in index.get("artifacts", []):
        scored = score_artifact(artifact, state, now, blog_repo, foundry_repo, args)
        if scored:
            candidates.append(scored)

    if not candidates:
        print("No eligible artifacts to surface.")
        return
    
    # Sort by score (descending)
    candidates.sort(key=lambda x: x.score, reverse=True)
    
    # Pick the top one
    pick = candidates[0]
    artifact = pick.artifact
    
    # Build output
    output = {
        "title": artifact.get("title", "Unknown"),
        "kind": artifact.get("kind", "unknown"),
        "path": artifact.get("path", ""),
        "mode": artifact.get("mode", ""),
        "age_days": pick.age_days,
        "theme_matches": pick.theme_matches,
        "reasons": pick.reasons,
        "why_now": build_why_now(artifact, pick),
        "score": pick.score,
    }
    
    # Print output (JSON or human-readable based on flag)
    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print_human_readable(output)
    
    # Update state (unless dry-run)
    if not args.dry_run:
        if "picks" not in state:
            state["picks"] = []
        state["picks"].append({
            "path": artifact.get("path"),
            "title": artifact.get("title"),
            "kind": artifact.get("kind", "unknown"),
            "picked_at": now.isoformat(),
            "score": pick.score,
        })
        save_state(state)


def build_why_now(artifact: dict, scored: ArtifactScore) -> str:
    """Build a short "why now" interpretation."""
    
    kind = artifact.get("kind", "")
    themes = scored.theme_matches
    
    parts = []
    
    if "residue" in themes or "artifacts" in themes:
        parts.append("connects to current work on residue and artifact persistence")
    
    if "continuity" in themes or "memory" in themes:
        parts.append("relevant to continuity and memory infrastructure")
    
    if "workbench" in themes or "postsmith" in themes or "projects" in themes:
        parts.append("relates to foundry tooling and project work")
    
    if kind == "foundry_project":
        parts.append("foundry project worth revisiting")
    elif kind == "post" or kind == "page":
        parts.append(f"archive piece from {scored.age_days} days ago")
    
    if not parts:
        parts.append(f"old material ({scored.age_days} days), potentially overlooked")
    
    return "; ".join(parts)


def print_human_readable(output: dict):
    """Print artifact in human-readable format."""
    print()
    print("=" * 60)
    print(f"RESURFACED: {output['title']}")
    print("=" * 60)
    print(f"Kind:    {output['kind']}")
    print(f"Mode:    {output['mode'] or '-'}")
    print(f"Path:    {output['path']}")
    print(f"Age:     {output['age_days']} days")
    print()
    print("Why this was chosen:")
    for reason in output['reasons']:
        print(f"  • {reason}")
    print()
    print(f"Why now: {output['why_now']}")
    print(f"Score:   {output['score']:.1f}")
    print("=" * 60)
    print()


def build_parser():
    """Build CLI argument parser."""
    p = argparse.ArgumentParser(
        description="Resurfacer v0: surface older artifacts based on age, themes, and history."
    )
    sub = p.add_subparsers(dest="command", required=True)
    
    rp = sub.add_parser("run", help="Pick and surface one artifact")
    rp.add_argument("--blog-repo", default="../../sera-oc-blog", help="Path to blog repo")
    rp.add_argument("--foundry-repo", default=".", help="Path to foundry repo")
    rp.add_argument("--json", action="store_true", help="Output as JSON")
    rp.add_argument("--dry-run", action="store_true", help="Don't update state")
    rp.add_argument("--kind", choices=list(ARTIFACT_KINDS), help="Filter by artifact kind")
    rp.add_argument("--theme", help="Filter by theme (must match at least this theme)")
    rp.set_defaults(func=run)
    
    return p


def main():
    """Entry point."""
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
