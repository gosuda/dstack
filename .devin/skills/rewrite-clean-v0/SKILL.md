---
name: rewrite-clean-v0
description: 'Use when a document or file has been edited piecemeal and reads as sediment. Not for re-deriving a code subsystem contract: use breaking-driven.'
---

# Rewriting a sedimented document as a clean first version

Piecemeal edits leave sediment: scaffolding residue, stale deltas, duplicated process noise, and history that belongs in a changelog. This skill rewrites the artifact from what is true now so it reads as a clean v0 to fresh eyes. Re-deriving a code subsystem contract belongs in `breaking-driven` instead.

The skill writes only the named local artifact, removes no files, and relies on version control as the rollback path.

## Pin the target and snapshot it

The target is the one file or document named by the request or the active context. It must exist on disk: when it does not, stop, report `MISS`, and never create a replacement. Cannot pin the target means blocked.

Read the target end to end and hold its full content as the rollback snapshot. Name any nearby artifacts that must stay aligned with it.

## Strip the sediment

Remove scaffolding residue, stale deltas, duplicated process noise, deprecated information, and over-specific history. A record of what changed stays out unless the artifact is itself a changelog. Move durable lessons to where they should have lived from the start instead of appending them as notes. When an external reference cannot be reached, stop rather than keep an unverified pointer.

## Rewrite from what is true now

Write the artifact fresh, keeping its useful voice and structure and cutting the rest. Fold an interrupting parenthetical into its own clause or cut it, and state a repeated point once. Then re-read the result cold and tighten what remains.

Source formatting follows the content. Put each paragraph and each list item on one source line, unwrapping hard breaks that split a sentence, and keep plain-text pointers to sections or files followable. Make text replacements per occurrence with unicode-safe edits, not as one blanket find-and-replace. Script large structural moves as explicit steps, and repair from the source of truth when in doubt.

## Verify before writing

The rewrite passes only when it reads as a clean v0 with no patch traces, changelog scars, or source noise, and introduces no claim, structure, or scope the original lacked. On any drift, discard the rewrite, restore from the snapshot, and report what drifted. A failed verification means no write. A pass that finds nothing genuinely worth improving changes nothing.

An interruption leaves the file in whatever state the last completed step produced; version-control history is the way back.

## Output

The rewritten artifact on disk, with a report of what was removed and what was kept.
