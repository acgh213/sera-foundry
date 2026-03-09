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

# Artifact kinds to consider (exclude certain types)
ARTIFACT_KINDS = {"post", "page", "foundry_project", "foundry_note"}
EXCLUDE_KINDS = set()  # empty for now; could exclude likes if needed


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


def get_artifact_date(artifact: dict) -> datetime | None:
    """Extract date from artifact, trying filename first."""
    path = artifact.get("path", "")
    
    # Try filename
    date = extract_date_from_filename(path)
    if date:
        return date
    
    # Could add more extraction logic here if needed
    return None


def calculate_days_since(date: datetime | None) -> int:
    """Calculate days since the date (or return a large number if no date)."""
    if not date:
        return 999999  # Very old, so it gets high age score
    
    # Make sure we have a timezone-aware datetime
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)
    
    now = datetime.now(timezone.utc)
    delta = now - date
    return max(1, delta.days)  # At least 1 day old


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


def score_artifact(artifact: dict, state: dict, now: datetime) -> ArtifactScore | None:
    """Score a single artifact based on age, themes, and history."""
    
    # Skip excluded kinds
    if artifact.get("kind") in EXCLUDE_KINDS:
        return None
    
    # Skip if not in our considered kinds
    if artifact.get("kind") not in ARTIFACT_KINDS:
        return None
    
    path = artifact.get("path", "")
    artifact_date = get_artifact_date(artifact)
    age_days = calculate_days_since(artifact_date)
    
    # Base score: prefer older artifacts (log scale to avoid too-old being overwhelming)
    age_score = min(age_days / 10.0, 50)  # Cap at 50 points
    
    # Theme score: bonus for matching current themes
    theme_matches = extract_themes_from_artifact(artifact)
    theme_score = len(theme_matches) * 3
    
    # Recency penalty: if it's very recent (< 3 days), penalize
    if age_days < 3:
        age_score *= 0.5
    
    # History penalty: if we've picked it recently, penalize heavily
    recent_picks = state.get("picks", [])
    penalty = 0
    for pick in recent_picks[-5:]:  # Look at last 5 picks
        if pick.get("path") == path:
            days_since_pick = (now - datetime.fromisoformat(pick.get("picked_at", "2000-01-01"))).days
            if days_since_pick < 14:  # Within 2 weeks
                penalty = 100
                break
            elif days_since_pick < 30:
                penalty = 50
                break
    
    final_score = age_score + theme_score - penalty
    
    reasons = []
    if age_days >= 7:
        reasons.append(f"older artifact ({age_days} days)")
    if theme_matches:
        reasons.append(f"matches themes: {', '.join(theme_matches)}")
    if penalty == 0 and recent_picks:
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
        scored = score_artifact(artifact, state, now)
        if scored and scored.score > 0:
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
    rp.set_defaults(func=run)
    
    return p


def main():
    """Entry point."""
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
