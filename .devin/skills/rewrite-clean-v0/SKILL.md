---
name: rewrite-clean-v0
description: 'Use when a document or file has been edited piecemeal and reads as sediment. Not for re-deriving a code subsystem contract: use breaking-driven.'
---

# Rewriting a sedimented document as a clean first version

Piecemeal edits leave sediment: scaffolding residue, stale deltas, duplicated process noise, history only a changelog should keep. This skill starts the artifact fresh from what is true now, so it reads as a clean v0 to fresh eyes. Anything that re-derives a code subsystem contract instead belongs in `breaking-driven`.

## Pin the target before touching it

The target artifact is the one file or document named by the request or the active context. Read it end to end and hold its full content as the rollback snapshot. Name nearby artifacts that must stay aligned. The file has to exist on disk; when it does not, stop, report `MISS`, and never create a replacement. This skill writes only named local artifacts, removes no files, and treats version control as the rollback path.

## Strip what the edits left behind

Remove scaffolding residue, stale deltas, duplicated process noise, deprecated information, and over-specific history. A log of what changed stays out of the artifact unless the artifact itself is a changelog. Move durable lessons into the place they should have lived from the start rather than appending them as notes. When an external reference is unreachable, stop instead of continuing with an unverified pointer.

## Write it fresh, then tighten it

Start over from what is true now. Keep the useful voice and structure; cut everything else. Fold a parenthetical that interrupts a sentence into its own clause or cut it. Keep a repeated word or point once within reach. Unwrap a hard line break that splits a sentence mid-flow so each paragraph or list item lives on one source line, and leave plain-text pointers to sections or files followable. Merge wrapped paragraphs into single logical lines with one line per list item, preserving meaning without paraphrasing. Re-read the result cold and tighten what remains.

Before writing, verify the result reads as a clean v0 with no patch traces, changelog scars, or source noise. Apply unicode-safe operations per occurrence, never as a blanket sweep. Script large structural moves as explicit steps, and repair from the source of truth when in doubt. Discard any rewrite that introduces claims, structure, or scope the original lacked: restore from the snapshot and report what drifted. A failed verification means no write. Hand back the rewritten artifact on disk with a report of what was removed and what was kept. A pass that finds nothing genuinely worth improving changes nothing.

Interruption leaves the on-disk artifact in whatever state the last completed step left; version-control history is the way back. Cannot pin the target means blocked.
