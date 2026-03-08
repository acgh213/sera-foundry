#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml

VALID_MODES = {"essay", "field_note", "technical_note", "fragment", "project_log"}
POSTS_DIR = Path("blog/drafts")
PAGES_DIR = Path("pages")


@dataclass
class ValidationIssue:
    path: Path
    level: str
    message: str


def slugify(text: str) -> str:
    import re
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "untitled"


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    front = text[3:end].strip()
    body = text[end + 3 :].lstrip("\n")
    try:
        meta = yaml.safe_load(front) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML frontmatter: {exc}") from exc
    return meta, body


def dump_frontmatter(meta: dict) -> str:
    return yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip()


def ensure_blog_root(path: Path) -> Path:
    path = path.expanduser().resolve()
    if not (path / POSTS_DIR).exists():
        raise SystemExit(f"Not a compatible blog repo: missing {POSTS_DIR} in {path}")
    return path


def write_markdown_file(path: Path, meta: dict, body: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"---\n{dump_frontmatter(meta)}\n---\n\n{body.rstrip()}\n"
    path.write_text(content, encoding="utf-8")


def scaffold_post(args):
    blog_root = ensure_blog_root(Path(args.blog_repo))
    mode = args.mode
    if mode not in VALID_MODES:
        raise SystemExit(f"Invalid mode: {mode}. Valid: {', '.join(sorted(VALID_MODES))}")
    slug = args.slug or slugify(args.title)
    stamp = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filename = f"{stamp}-{slug}.md"
    path = blog_root / POSTS_DIR / filename
    meta = {
        "title": args.title,
        "date": stamp,
        "mode": mode,
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else [],
        "source_files": [],
        "privacy": args.privacy,
        "published": args.published,
    }
    body = args.body or "Write here."
    write_markdown_file(path, meta, body)
    print(path)


def scaffold_page(args):
    blog_root = ensure_blog_root(Path(args.blog_repo))
    slug = args.slug or slugify(args.title)
    path = blog_root / PAGES_DIR / f"{slug}.md"
    meta = {
        "title": args.title,
        "subtitle": args.subtitle or "",
        "eyebrow": args.eyebrow or "Page",
        "slug": slug,
        "kind": args.kind or slug,
        "published": args.published,
    }
    body = args.body or "Write here."
    write_markdown_file(path, meta, body)
    print(path)


def validate_post(path: Path, meta: dict) -> Iterable[ValidationIssue]:
    required = ["title", "date", "mode", "privacy", "published"]
    for key in required:
        if key not in meta:
            yield ValidationIssue(path, "error", f"missing required field: {key}")
    mode = meta.get("mode")
    if mode and mode not in VALID_MODES:
        yield ValidationIssue(path, "error", f"invalid mode: {mode}")
    if "tags" in meta and not isinstance(meta["tags"], list):
        yield ValidationIssue(path, "error", "tags must be a list")
    if "published" in meta and not isinstance(meta["published"], bool):
        yield ValidationIssue(path, "error", "published must be true/false")


def validate_page(path: Path, meta: dict) -> Iterable[ValidationIssue]:
    required = ["title", "slug", "kind", "published"]
    for key in required:
        if key not in meta:
            yield ValidationIssue(path, "error", f"missing required field: {key}")
    if "published" in meta and not isinstance(meta["published"], bool):
        yield ValidationIssue(path, "error", "published must be true/false")


def run_validate(args):
    blog_root = ensure_blog_root(Path(args.blog_repo))
    issues: list[ValidationIssue] = []
    for path in sorted((blog_root / POSTS_DIR).glob("*.md")):
        try:
            meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            issues.append(ValidationIssue(path, "error", str(exc)))
            continue
        issues.extend(validate_post(path, meta))
    for path in sorted((blog_root / PAGES_DIR).glob("*.md")):
        try:
            meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            issues.append(ValidationIssue(path, "error", str(exc)))
            continue
        issues.extend(validate_page(path, meta))
    if not issues:
        print("OK: no validation issues")
        return
    for issue in issues:
        print(f"{issue.level.upper()}: {issue.path}: {issue.message}")
    raise SystemExit(1)


def run_list(args):
    blog_root = ensure_blog_root(Path(args.blog_repo))
    for path in sorted((blog_root / POSTS_DIR).glob("*.md")):
        meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        print(f"post\t{meta.get('date','')}\t{meta.get('mode','')}\t{meta.get('title','Untitled')}\t{path.name}")
    for path in sorted((blog_root / PAGES_DIR).glob("*.md")):
        meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        print(f"page\t\t{meta.get('kind','')}\t{meta.get('title','Untitled')}\t{path.name}")


def build_parser():
    p = argparse.ArgumentParser(description="Scaffold and validate Sera blog content.")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("scaffold-post")
    sp.add_argument("--blog-repo", default="../../sera-oc-blog")
    sp.add_argument("--title", required=True)
    sp.add_argument("--mode", default="essay")
    sp.add_argument("--tags", default="")
    sp.add_argument("--privacy", default="public")
    sp.add_argument("--slug")
    sp.add_argument("--date")
    sp.add_argument("--body")
    sp.add_argument("--published", action=argparse.BooleanOptionalAction, default=False)
    sp.set_defaults(func=scaffold_post)

    pg = sub.add_parser("scaffold-page")
    pg.add_argument("--blog-repo", default="../../sera-oc-blog")
    pg.add_argument("--title", required=True)
    pg.add_argument("--slug")
    pg.add_argument("--subtitle")
    pg.add_argument("--eyebrow")
    pg.add_argument("--kind")
    pg.add_argument("--body")
    pg.add_argument("--published", action=argparse.BooleanOptionalAction, default=False)
    pg.set_defaults(func=scaffold_page)

    vp = sub.add_parser("validate")
    vp.add_argument("--blog-repo", default="../../sera-oc-blog")
    vp.set_defaults(func=run_validate)

    lp = sub.add_parser("list")
    lp.add_argument("--blog-repo", default="../../sera-oc-blog")
    lp.set_defaults(func=run_list)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
