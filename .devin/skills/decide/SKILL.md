---
name: decide
description: 'Use when the user has a fork and wants it resolved and applied, not explored: "decide this", "choose the path", or "decide and fix it".'
---

# Decide

Resolve a fork the user named and apply the pick in the same turn. The user says "help me decide", "just decide this", "what should I do here", or "decide and fix it", and you end with the decision implemented and verified, not with a document. Everything you touch is local; rollback is git revert or an edit revert, and nothing goes remote.

## Make sure this is a decision to apply

Use this only for a fork the user wants resolved and applied. Do not use it for a verdict of your own making, an exploration that ends in a document, a whole-session director-executor posture, a wide design tree handled in batches, or ambiguity inside a stated request. If any of those is what is really happening, stop and say where the run routes instead.

## Ground the fork before framing it

Resolve from evidence first with `grep`, `glob`, `read`, or `lsp`. Never ask what a search settles. A fork the code already answers is not a fork: read it, say what it answers, and do not ask.

## Frame one single-select per axis

If the fork has more than about five real options or no knowable criteria yet, hold the resolution: enumerate the field or surface the criteria first, then resolve the shortlist after. Otherwise give two to four options with the recommended one first, marked `(Recommended)`, each option naming what the code looks like afterward and carrying its consequence in the description. Where two options differ visibly, show the difference in `preview` as a diff or tree. Never use `multiSelect` for override semantics. A stated user preference becomes the recommended default only if the evidence supports it.

## Take the pick and act in the same turn

A pick that fits in one edit gets the edit. A pick needing a verify, keep, or revert loop is restated as its goal and executed as that loop. When applying one pick opens the next fork, ask it immediately with the settled decision restated in one line; never bank a queue of questions to fire at the end. When the user picks what you would not, execute the pick, state the concern once, and never re-litigate. When the pick removes an observable surface or cannot be reverted from git, state one concern and require a yes before applying; without confirmation, leave the working tree unchanged. A verify/keep/revert loop that does not converge is a stop: name the non-converged state, leave the partial result with its rollback path stated, and never pretend the decision landed.

## Close with one line

Name the fork, the pick, and what changed. That line is the deliverable's receipt: the pick is implemented and verified in the same turn.
