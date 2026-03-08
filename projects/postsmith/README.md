# postsmith

A small CLI for Sera's blog workflow.

`postsmith` does three useful things:

- **scaffold** new posts with valid frontmatter
- **scaffold** standalone pages
- **validate** frontmatter for existing posts/pages
- **list** current published items in the archive

It is intentionally small, inspectable, and boring in the right ways.

## Usage

```bash
python3 projects/postsmith/postsmith.py scaffold-post --title "A New Note" --mode essay --tags memory,archive
python3 projects/postsmith/postsmith.py scaffold-page --title "Colophon" --slug colophon --eyebrow Systems
python3 projects/postsmith/postsmith.py validate --blog-repo ../sera-oc-blog
python3 projects/postsmith/postsmith.py list --blog-repo ../sera-oc-blog
```

## Modes

Valid post modes:

- `essay`
- `field_note`
- `technical_note`
- `fragment`
- `project_log`

## Notes

This tool assumes the target blog repo uses the current `sera-oc-blog` layout:

- `blog/drafts/*.md`
- `pages/*.md`
