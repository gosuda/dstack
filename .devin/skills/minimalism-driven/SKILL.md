---
name: minimalism-driven
description: 'Use when writing or restructuring code, before adding a helper, wrapper, config key, or dependency, or when the user asks for minimal or DRY code. Not for performance tuning: use optimize.'
---

# Minimalism driven

Build the smallest code that fully satisfies the ask. Nothing more. Every helper, wrapper, config key, branch, or dependency must earn its place with a concrete reason, and broken structure gets replaced in clean form rather than patched around.

## When this applies

Reach for this when you are writing or restructuring code, when you are considering adding a helper, wrapper, config key, or dependency, or when the request asks for minimal code, DRY code, or no gold-plating. Performance tuning is out of scope here. Use optimize for that.

## What you may touch

Make reversible local edits inside the requested scope only, with no remote mutation. Rollback is version control or undo. Get human approval before removing a live or consumer-facing surface, discarding stored data or history, or taking any irreversible, remote, or paid action.

Your change replaces broken structure with its clean re-derived form: absorb special cases, delete the obsolete mechanism, and migrate every in-scope dependent in the same change. Adjacent improvements stay out of the change set. Mention one separately only when it materially affects the requested work.

You are done when every addition has a concrete reason, intent and failure behavior are obvious from the code itself, broken structure is replaced rather than worked around, every in-scope dependent resolves to the replacement, and the resulting scope matches the ask exactly.

## What you need before starting

The requested behavior and the local code surface to change, plus any explicit constraints or acceptance criteria that exist. Nearby implementations and call sites are the required evidence for reuse decisions. No input is truly optional if its absence would force you to guess at behavior. In that case stop instead of inventing it.

## Working through it

1. Bound the requested behavior, the affected files, and the acceptance criteria before editing. The bound is set when all three are stated and nothing required remains unknown.
2. Look through the affected code and its relevant call sites for an existing implementation or convention that already satisfies the ask, and reuse it before creating a second form. Record the reuse-or-create decision and the candidates you considered.
3. Try deletion first, then clean replacement of the broken structure. Add new code only when neither can produce the required behavior. When the structure in scope is broken, replace it by default (absorb special cases into the replacement, delete the obsolete mechanism, migrate every in-scope consumer in the same change), and patch around it only when replacement would exceed the disclosed scope or need withheld approval. Leave a structure that meets its contract alone.
4. Before keeping any helper, wrapper, config key, dependency, branch, or other new surface, state its concrete necessity in one sentence. Drop anything whose removal would leave the requested outcome unchanged.
5. Keep each retained addition sufficient, not merely short: use clear names, handle the required error paths, and encode or state assumptions anywhere the code would otherwise permit a silent gap. Intent stays in the code itself, not in explanatory comments.
6. Verify with the narrowest available check that actually exercises the changed behavior (compilation alone proves nothing about behavior), then inspect the final change set. It holds up when the check passes, every addition still has its concrete necessity, intent and failure behavior remain obvious, and nothing lies outside the ask.

## Stop and report instead of pushing through

- Required behavior or acceptance criteria unknowable from the request and local evidence: make no speculative edit. Return `blocked: missing contract` with the exact missing fact.
- Neither deletion, reuse, nor modification can satisfy the ask without breaking required behavior: keep the smallest necessary addition and name the constraint that forces it. Where that constraint cannot be established, return `blocked: necessity unproven`.
- The changed behavior fails its check: restore the touched files to their pre-edit contents, or leave the failing edits clearly identified as a partial result. Return `non-converged: verification failed` with the failed check and what you observed.
- Completion would need unrelated files, remote mutation, credentials, publishing, deployment, or an unauthorized dependency: do that work under no circumstances. Return `blocked: scope expansion required` with the exact boundary.
- Approval withheld, or the work runs past the disclosed scope: make no further change and return `blocked` naming the gated surface or the additional path. Never cut on silence and never widen scope implicitly.

Never claim the work is done while a required check fails or evidence is missing.

## What to hand back

The completed local code change plus a concise report: the behavior implemented, the files changed, the necessity behind each new surface, the verification you ran and what it showed, and any adjacent work left blocked. On failure, give the exact blocked or non-converged classification above and leave the tree preserved or restored as specified.
