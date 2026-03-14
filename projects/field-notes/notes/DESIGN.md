# field-notes v1 design

## Chosen shape

V1 uses **one markdown file per field note**.

Why:
- preserves note individuality
- keeps the archive hand-editable and diff-friendly
- fits the project's artifact-oriented stance
- resists the feeling of a capture stream or hidden database

## Structural choices

### Frontmatter
Small frontmatter carries just enough metadata for views:
- `title`
- `date`
- `kind`
- `status`
- `pressure`
- `place` (optional)
- `context` (optional)
- `tags` (optional list)
- `returns` (optional list of dates)

### Body sections
The body uses markdown sections:
- `## Observation`
- `## Interpretation`
- `## Impact`

Only `Observation` is required by validation.

This keeps the distinction between description, interpretation, and felt consequence available without forcing every note to perform all three.

## Returning logic

Returning is explicit in v1.

A note appears in `returning` when either:
- `status: returning`, or
- `returns:` contains one or more dates

This was chosen on purpose. Inference would push the system toward hidden scoring, pseudo-analytics, or mood-reading. Manual return markers keep the archive honest.

## By-tag logic

`by-tag` is exact-match on tags.

This is deliberately simple. It gives motif-linked views without requiring a taxonomy engine or soft-semantic search layer.

## Anti-drift constraints

V1 refuses several tempting directions:
- no passive ingestion
- no reminders
- no notifications
- no confidence scoring
- no accusation workflow
- no trend charts
- no task/project coupling by default

The system should help preserve subtle texture, not become a machine for over-reading it.
