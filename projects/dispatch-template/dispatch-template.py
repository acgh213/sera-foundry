#!/usr/bin/env python3
"""
Dispatch Template

Print a bounded-task execution brief scaffold to stdout.

This is intentionally small and inspectable:
- terminal-first
- local-only
- standard library only
- no file writes by default
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

DEFAULT_ALLOWED_TOOLS = [
    "read",
    "write",
    "edit",
    "exec/process for local commands/tests",
]

DEFAULT_ESCALATION_TRIGGERS = [
    "needs new dependencies",
    "needs files outside the allowlist",
    "starts turning into a broader platform/system instead of the requested slice",
    "requires unclear strategic judgment rather than bounded implementation",
    "needs external/network actions not explicitly allowed",
]

DEFAULT_VERIFICATION = [
    "run the tool or code locally",
    "include sample invocation(s)",
    "include sample output or observed behavior",
    "include syntax/runtime validation notes",
]

DEFAULT_OUTPUT_CONTRACT = [
    "what changed",
    "files changed",
    "commands/tests run",
    "sample output or result summary",
    "caveats",
    "commit id if committed",
]

DEFAULT_BLOCKED_CONTRACT = [
    "blocked reason",
    "what you tried",
    "what decision is needed",
    "2–3 concrete next options",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a reusable execution-brief scaffold for bounded implementation tasks."
    )
    parser.add_argument(
        "title",
        nargs="*",
        help="Dispatch title/name. If omitted, a placeholder title is used.",
    )
    parser.add_argument(
        "-o",
        "--objective",
        help="Optional objective sentence or paragraph to prefill.",
    )
    parser.add_argument(
        "-t",
        "--target",
        help="Optional target path, tool name, or component hint.",
    )
    parser.add_argument(
        "--no-timestamp",
        action="store_true",
        help="Omit the generated-at timestamp line.",
    )
    return parser.parse_args()


def bullet_list(items: list[str], empty_placeholder: str = "- _fill in_") -> str:
    if not items:
        return empty_placeholder
    return "\n".join(f"- {item}" for item in items)


def numbered_list(items: list[str]) -> str:
    if not items:
        return "1. _fill in_"
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def placeholder_or_text(text: str | None, placeholder: str) -> str:
    return text.strip() if text and text.strip() else placeholder


def render(args: argparse.Namespace) -> str:
    title = " ".join(args.title).strip() or "<task title>"
    objective = placeholder_or_text(
        args.objective,
        "State the concrete outcome this dispatch should produce.",
    )
    target = args.target.strip() if args.target and args.target.strip() else None

    lines: list[str] = []
    lines.append(f"# Dispatch: {title}")
    lines.append("")

    if not args.no_timestamp:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        lines.append(f"Generated: {now}")
        lines.append("")

    if target:
        lines.append(f"Target: `{target}`")
        lines.append("")

    lines.append("## Objective")
    lines.append(objective)
    lines.append("")

    lines.append("## Scope")
    lines.append("- Build or change only what is necessary for this slice.")
    lines.append("- Keep the implementation narrow, inspectable, and easy to verify.")
    lines.append("- Prefer direct edits and obvious behavior over architecture expansion.")
    lines.append("")

    lines.append("## Non-goals")
    lines.append("- Do not broaden this into a platform, framework, or orchestration system.")
    lines.append("- Do not add speculative features that are not required for the objective.")
    lines.append("- Do not rewrite unrelated code or documentation.")
    lines.append("")

    lines.append("## Acceptance criteria")
    lines.append(numbered_list([
        "The requested slice runs locally from the repo.",
        "The result is readable, useful, and bounded to the stated objective.",
        "The implementation stays small and inspectable.",
        "Verification is included in the return summary.",
    ]))
    lines.append("")

    lines.append("## Constraints")
    lines.append(bullet_list([
        "terminal-first unless explicitly told otherwise",
        "local-only unless external actions are explicitly allowed",
        "standard library only if possible",
        "clarity over cleverness",
        "prefer narrow scope over premature extensibility",
    ]))
    lines.append("")

    lines.append("## Allowed files / directories")
    if target:
        lines.append(f"- `{target}`")
    else:
        lines.append("- _fill in exact file(s) or directory allowlist_")
    lines.append("- _add any other explicitly allowed path if needed_")
    lines.append("")

    lines.append("## Disallowed / protected paths")
    lines.append(bullet_list([
        "unrelated repos, deployment, auth, or runtime state files",
        "identity/persona files unless explicitly in scope",
        "memory files unless explicitly in scope",
        "any path outside the allowlist",
    ]))
    lines.append("")

    lines.append("## Allowed tools")
    lines.append(bullet_list(DEFAULT_ALLOWED_TOOLS))
    lines.append("- _add or remove tool permissions for this dispatch if needed_")
    lines.append("")

    lines.append("## Escalation triggers")
    lines.append("Stop and return to main if the task:")
    lines.append(bullet_list(DEFAULT_ESCALATION_TRIGGERS))
    lines.append("")

    lines.append("## Verification expectations")
    lines.append(bullet_list(DEFAULT_VERIFICATION))
    lines.append("")

    lines.append("## Commit / workflow expectation")
    lines.append(bullet_list([
        "patch-oriented is fine if the slice stays small and self-contained",
        "keep commits narrow and specific",
        "do not create extra workflow machinery unless explicitly requested",
    ]))
    lines.append("")

    lines.append("## Output contract")
    lines.append("Return with:")
    lines.append(bullet_list(DEFAULT_OUTPUT_CONTRACT))
    lines.append("")

    lines.append("## Blocked-state contract")
    lines.append("If blocked, return:")
    lines.append(bullet_list(DEFAULT_BLOCKED_CONTRACT))
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    print(render(args), end="")


if __name__ == "__main__":
    main()
