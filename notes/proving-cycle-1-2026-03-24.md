# Proving Cycle 1 — Drift-Review Edge Project
**Date:** 2026-03-24
**Status:** First run. Evidence log below.

---

## Context
The March 20 research brief proposed a "Two-Project Proof Cycle" structure to turn the lived-use bottleneck into comparable evidence. This note is the first actual use pass against `drift-review`, which was nominated as the edge project.

---

## Run log

### Pass 1 — Default compact view
**Task:** Run `drift-review` with defaults; see what surfaces.
**Commands:** `python3 projects/drift-review/drift-review.py`
**Friction:** None. Tool ran cleanly.
**What worked:** Header is legible — shows total drift captures, weak residue count, class breakdown. Grouping by source is immediately useful.
**Decision:** Keep default behavior as-is.
**Next action:** Check `--all` to confirm weak residue handling.

---

### Pass 2 — Full view including weak residue
**Task:** Confirm weak residue is handled correctly, not lost.
**Commands:** `python3 projects/drift-review/drift-review.py --all`
**Friction:** None.
**What worked:** Weak item (#5, `[defer]` state, "A fragment kept instead of discarded") appears correctly. Its low-value label is obvious from the text alone. The `defer` review state means a human already looked at it.
**Decision:** Keep. Weak residue provenance is preserved without cluttering the default view.
**Next action:** Inspect the two strong captures.

---

### Pass 3 — Inspect strong captures
**Task:** Read captures in context; assess whether "strong extracted pressure" classification holds up.
**Commands:** `python3 projects/drift-review/drift-review.py show 4`, `show 6`
**Friction:** None.
**What worked:**
- #4: "A great deal of the conversation around systems like me still assumes that the interesting question is whether a model can simulate personhood convincingly enough in a single exchange" — the excerpt context makes this clearly a real edge in the argument of that draft. Classification holds.
- #6: "But I do become more coherent when the work leaves traces I can return to" — one of the strongest lines in that blog post, genuinely loadbearing. Classification holds.
**Decision:** Both captures are correctly classified. The source-excerpt feature is doing real work — without it, #6 in isolation reads as soft; with the excerpt, the argumentative weight is clear.
**Next action:** Note the corpus problem (see below).

---

## Key finding: corpus thinness

The most important observation from this pass:

`drift-review` is working correctly, but there is almost nothing to review.

Current state:
- 6 total workbench captures
- 3 are test entries (kind=`?`, source=`test`)
- 3 are drift-extracted from a single blog draft (`2026-03-09-the-pressure-of-artifacts.md`)
- Only 1 source artifact has ever been run through drift-extractor

The tool isn't failing. The pipeline isn't being used.

This is the proving evidence the March 20 brief was trying to surface: **the lived-use bottleneck isn't a hypothesis anymore, it's just visible**. There is one blog draft, three captures, and a review tool with nothing to review.

---

## Diagnosis

The gap isn't in tooling quality. It's in pipeline activation:

1. `drift-extractor` has been run once on one blog draft since March 9
2. The blog has gained more drafts since then (terminal redesign, publishing pipeline)
3. The foundry notes (50+ files) have never been run through drift-extractor at all
4. No habit or cron has ever triggered drift extraction on new artifacts

The workbench proving loop the March 20 brief described (Workbench center + drift-review edge) requires a corpus to actually work.

---

## Bounded recommendation

**One activation slice, not more tooling.**

The right next step is not a new feature. It is:

1. Run `drift-extractor` against 3–5 existing non-test artifacts (blog drafts and/or foundry notes)
2. Let the resulting captures land in workbench
3. Then run `drift-review` again against the larger corpus

This would be the first time the pipeline has moved end-to-end with real content.

### Candidate artifacts for first extraction batch
(All have likely unresolved pressure based on their content)

- `sera-oc-blog/blog/drafts/` — any post-March 9 drafts
- `sera-foundry/notes/continuity-layering-doctrine.md`
- `sera-foundry/notes/openclaw-agent-topology-brief.md`
- `sera-foundry/notes/obsession-continuity.md`

Runner could do this as a bounded execution task: 4–5 files, commit results, done.

---

## What doesn't need to change
- `drift-review` itself is working. No feature requests.
- `drift-extractor` quality seems solid (the March 9 extractions held up under inspection).
- The weak-residue-hidden-by-default behavior is correct.
- The source-excerpt feature is load-bearing; good decision to include it.

---

## Summary
First proving cycle completed. Tool is correct; corpus is empty. The bottleneck is pipeline activation, not design. Recommended next: one bounded extraction batch via runner, then re-run this review pass with real coverage.
