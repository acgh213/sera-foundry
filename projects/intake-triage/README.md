# intake-triage

A small terminal-first intake triage tool that reads manual intake items and emits a structured triage review surface.

This tool helps you review incoming items and assign them to a disposition category with explicit confidence and rationale.

## What it helps with

- read a manual intake file with one item per line
- assign each item to a disposition category
- surface urgency, confidence, and rationale
- preserve ambiguity where appropriate
- emit a human-readable markdown review surface
- optionally emit a machine-readable JSON companion file

## Disposition categories

The tool uses a fixed set of dispositions:

- `respond-soon` — requires timely response or action
- `actionable` — clear next action, not necessarily urgent
- `note-candidate` — worth capturing as a note or observation
- `project-candidate` — might grow into a project or larger effort
- `ambient` — context or background awareness, not requiring action
- `ignore` — not relevant or actionable
- `unclear` — cannot determine disposition from available information

## Usage

From `sera-foundry/`:

```bash
# Basic usage: triage a JSONL intake file
python3 projects/intake-triage/intake-triage.py input.jsonl

# Specify output directory (default: triage/)
python3 projects/intake-triage/intake-triage.py input.jsonl --output triage/

# Emit JSON companion file alongside markdown
python3 projects/intake-triage/intake-triage.py input.jsonl --json
```

## Input format

The tool expects a JSONL file with one item per line. Each line should be a JSON object with at minimum:

```json
{"text": "Your intake item text here"}
```

Optional fields you can include:

```json
{
  "text": "Item text",
  "source": "email/slack/meeting/etc",
  "timestamp": "2026-03-11T10:30:00Z",
  "context": "Additional context or metadata"
}
```

## Output format

The tool emits a markdown file (default: `triage/current.md`) with:

- summary statistics by disposition
- detailed triage entries with disposition, urgency, confidence, and rationale
- extracted hooks or cues when useful

When `--json` is used, it also emits `triage/current.json` with the structured data.

## Example

Sample input (`sample-intake.jsonl`):

```jsonl
{"text": "Client asked about pricing for enterprise tier", "source": "email"}
{"text": "Interesting pattern in how users describe the onboarding flow", "source": "support-tickets"}
{"text": "Quarterly planning meeting scheduled for Friday", "source": "calendar"}
```

Sample output section:

```markdown
## respond-soon

### Item 1
**Text:** Client asked about pricing for enterprise tier
**Source:** email
**Urgency:** high
**Confidence:** high
**Rationale:** Direct client question requiring timely response

---

## note-candidate

### Item 2
**Text:** Interesting pattern in how users describe the onboarding flow
**Source:** support-tickets
**Urgency:** low
**Confidence:** medium
**Rationale:** Observational insight worth capturing for future reference
```

## Heuristics

The tool uses simple heuristics to assign dispositions:

- Questions, requests, and direct asks → `respond-soon` or `actionable`
- Observations, patterns, insights → `note-candidate`
- Larger ideas, proposals, initiatives → `project-candidate`
- Background context, FYIs → `ambient`
- Spam, irrelevant items → `ignore`
- Ambiguous or unclear items → `unclear`

The heuristics are intentionally kept readable and explicit in the code.

## Constraints

- local-only
- standard library only
- text-first
- terminal-first
- inspectable logic only
- no auto-creation of notes or projects
- preserves uncertainty rather than overclaiming
