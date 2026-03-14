# correspondence-archive — design note

## Bounded v1 decision

Choose the smallest shape that preserves correspondence as artifact.

Decision:
- one markdown file per item
- lightweight frontmatter for structure
- plain terminal CLI for listing and reading

Why:
- stronger archival feel than a central JSON blob
- easy to inspect, diff, and hand-edit
- preserves letter-ness better than record storage
- keeps the implementation stdlib-only and small

## Preserved structure

V1 treats these as first-class:
- explicit address (`from`, `to`)
- send boundary (`status` distinguishes draft/sent-like states)
- reply threading (`thread_id`, `reply_to`)
- chronology (`date`, thread ordering, gap display)
- artifact readability (body remains plain markdown text)

## Avoided structure

V1 intentionally does not include:
- inbox terminology
- unread counts
- notifications
- response-time pressure
- real-time presence
- search/summarization machinery
- provider integrations

## Open questions after lived use

- whether drafts deserve their own directory rather than status-only distinction
- whether a simple participant view would help without creating inbox behavior
- whether revisit/return markers belong in correspondence itself or in a later adjacent tool
