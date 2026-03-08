#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml

POSTS_DIR = Path("blog/drafts")
PAGES_DIR = Path("pages")
CAPTURE_FILE = Path("projects/workbench/data/captures.jsonl")
INDEX_FILE = Path("projects/workbench/data/index.json")
VALID_LAYERS = {"internal", "draft", "public"}
SUGGEST_TYPES = ("fragment", "field_note", "project_log")


@dataclass
class Artifact:
    kind: str
    title: str
    path: str
    mode: str = ""
    tags: list[str] | None = None
    published: bool | None = None


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    front = text[3:end].strip()
    body = text[end + 3 :].lstrip("\n")
    meta = yaml.safe_load(front) or {}
    return meta, body


def ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def capture(args):
    if args.layer not in VALID_LAYERS:
        raise SystemExit(f"Invalid layer: {args.layer}. Valid: {', '.join(sorted(VALID_LAYERS))}")
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "text": args.text,
        "source": args.source,
        "layer": args.layer,
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else [],
    }
    ensure_dir(CAPTURE_FILE)
    with CAPTURE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(CAPTURE_FILE)


def iter_blog_artifacts(blog_root: Path) -> Iterable[Artifact]:
    for path in sorted((blog_root / POSTS_DIR).glob("*.md")):
        meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        yield Artifact(
            kind="post",
            title=meta.get("title", path.stem),
            path=str(path.relative_to(blog_root)),
            mode=meta.get("mode", ""),
            tags=meta.get("tags", []),
            published=meta.get("published"),
        )
    for path in sorted((blog_root / PAGES_DIR).glob("*.md")):
        meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        yield Artifact(
            kind="page",
            title=meta.get("title", path.stem),
            path=str(path.relative_to(blog_root)),
            mode=meta.get("kind", ""),
            tags=[],
            published=meta.get("published"),
        )


def iter_foundry_artifacts(foundry_root: Path) -> Iterable[Artifact]:
    for path in sorted((foundry_root / "projects").rglob("README.md")):
        project_name = path.parent.name
        yield Artifact(kind="foundry_project", title=project_name, path=str(path.relative_to(foundry_root)))
    for path in sorted((foundry_root / "notes").glob("*.md")):
        yield Artifact(kind="foundry_note", title=path.stem, path=str(path.relative_to(foundry_root)))


def build_index(args):
    blog_root = Path(args.blog_repo).expanduser().resolve()
    foundry_root = Path(args.foundry_repo).expanduser().resolve()
    artifacts = [asdict(a) for a in iter_blog_artifacts(blog_root)] + [asdict(a) for a in iter_foundry_artifacts(foundry_root)]
    index = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "artifacts": artifacts,
    }
    ensure_dir(INDEX_FILE)
    INDEX_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(INDEX_FILE)


def load_index() -> dict:
    if not INDEX_FILE.exists():
        return {"artifacts": []}
    return json.loads(INDEX_FILE.read_text(encoding="utf-8"))


def status(args):
    if args.refresh:
        build_index(args)
    index = load_index()
    artifacts = index.get("artifacts", [])
    by_kind = Counter(a.get("kind", "unknown") for a in artifacts)
    by_mode = Counter(a.get("mode", "") for a in artifacts if a.get("mode"))
    print("Workbench status")
    print(f"- indexed artifacts: {len(artifacts)}")
    print("- by kind:")
    for kind, count in sorted(by_kind.items()):
        print(f"  - {kind}: {count}")
    if by_mode:
        print("- by mode/kind label:")
        for mode, count in sorted(by_mode.items()):
            print(f"  - {mode}: {count}")


def score_bucket(score: dict[str, int], reasons: dict[str, list[str]], bucket: str, points: int, reason: str):
    score[bucket] += points
    reasons[bucket].append(reason)


def classify_text(text: str):
    lowered = text.lower()
    score = {k: 0 for k in SUGGEST_TYPES}
    reasons = {k: [] for k in SUGGEST_TYPES}

    word_count = len(text.split())
    sentence_count = sum(text.count(ch) for ch in ".!?") or 1

    if word_count <= 18:
        score_bucket(score, reasons, "fragment", 2, "short, compressed note")
    elif word_count <= 45:
        score_bucket(score, reasons, "field_note", 1, "mid-length note with room for observation")
    else:
        score_bucket(score, reasons, "project_log", 1, "longer note with room for implementation context")

    if sentence_count <= 2 and word_count <= 24:
        score_bucket(score, reasons, "fragment", 1, "reads like a compact standalone signal")

    if any(word in lowered for word in ["idea", "thought", "signal", "residue", "glimpse", "fragment"]):
        score_bucket(score, reasons, "fragment", 2, "contains residue/idea language")
    if any(phrase in lowered for phrase in ["when it", "what remains", "pressure behind", "leaves residue"]):
        score_bucket(score, reasons, "fragment", 1, "reads like an aphoristic or compressed thought")

    if any(phrase in lowered for phrase in ["learned", "noticed", "observed", "found that", "while working", "working on", "ran into"]):
        score_bucket(score, reasons, "field_note", 3, "describes an observation from active work")

    if any(word in lowered for word in ["built", "implemented", "integrated", "tool", "repo", "project", "artifact", "workflow", "cli", "validator"]):
        score_bucket(score, reasons, "project_log", 3, "mentions concrete implementation or artifacts")

    if any(word in lowered for word in ["status", "shipped", "released", "committed", "pushed", "prototype"]):
        score_bucket(score, reasons, "project_log", 2, "reads like a status-bearing project update")

    if any(word in lowered for word in ["why", "because", "noticed", "seems", "feels"]):
        score_bucket(score, reasons, "field_note", 1, "includes reflective/interpretive language")

    if score["project_log"] >= 3:
        score["fragment"] = max(0, score["fragment"] - 1)
    if score["field_note"] >= 3:
        score["fragment"] = max(0, score["fragment"] - 1)

    ranked = sorted(score.items(), key=lambda kv: kv[1], reverse=True)
    winner, top_score = ranked[0]
    secondary, second_score = ranked[1]
    gap = top_score - second_score

    confidence = "low"
    if top_score >= 5 and gap >= 2:
        confidence = "high"
    elif top_score >= 3 and gap >= 1:
        confidence = "medium"

    return {
        "suggested_type": winner,
        "secondary_type": secondary,
        "confidence": confidence,
        "scores": score,
        "reasons": reasons[winner][:4],
        "secondary_reasons": reasons[secondary][:3],
    }


def suggest(args):
    print(json.dumps(classify_text(args.text), indent=2))


def query(args):
    index = load_index()
    artifacts = index.get("artifacts", [])
    needle = args.text.lower()
    matches = []
    for artifact in artifacts:
        fields = [
            artifact.get("kind", ""),
            artifact.get("title", ""),
            artifact.get("path", ""),
            artifact.get("mode", ""),
            " ".join(artifact.get("tags", []) or []),
        ]
        haystack = " ".join(fields).lower()
        if needle in haystack:
            matches.append(artifact)

    print(f"Query: {args.text}")
    print(f"Matches: {len(matches)}")
    for artifact in matches[: args.limit]:
        tags = ", ".join(artifact.get("tags", []) or [])
        extra = f" | tags: {tags}" if tags else ""
        mode = artifact.get("mode") or "-"
        print(f"- [{artifact.get('kind')}] {artifact.get('title')} | mode: {mode} | path: {artifact.get('path')}{extra}")


def build_parser():
    p = argparse.ArgumentParser(description="Workbench: continuity tooling for residue and artifacts.")
    sub = p.add_subparsers(dest="command", required=True)

    cp = sub.add_parser("capture")
    cp.add_argument("--text", required=True)
    cp.add_argument("--source", default="manual")
    cp.add_argument("--tags", default="")
    cp.add_argument("--layer", default="internal")
    cp.set_defaults(func=capture)

    ip = sub.add_parser("index")
    ip.add_argument("--blog-repo", default="../../sera-oc-blog")
    ip.add_argument("--foundry-repo", default=".")
    ip.set_defaults(func=build_index)

    sp = sub.add_parser("status")
    sp.add_argument("--blog-repo", default="../../sera-oc-blog")
    sp.add_argument("--foundry-repo", default=".")
    sp.add_argument("--refresh", action="store_true")
    sp.set_defaults(func=status)

    sg = sub.add_parser("suggest")
    sg.add_argument("--text", required=True)
    sg.set_defaults(func=suggest)

    qp = sub.add_parser("query")
    qp.add_argument("--text", required=True)
    qp.add_argument("--limit", type=int, default=10)
    qp.set_defaults(func=query)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
