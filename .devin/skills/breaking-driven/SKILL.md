---
name: breaking-driven
description: 'Use when bloated code needs clean re-derivation, or the user says "this module is bloated" or "break it and rebuild". Not for untracked data or changes without VCS rollback.'
---

# Breaking-driven development

Some modules are past patching: layers of accretion, duplicated branches, indirection that no longer serves any caller. This skill rebuilds such a module from its consumer contract instead of refactoring its structure, so the accretion cannot reproduce itself under fresh names. It runs on one target at a time, deletes everything the contract does not require, and commits each target atomically with its essential behaviors tested.

It works only where version control can undo it: every mutation touches VCS-tracked targets, the exact set is shown before anything is deleted, and nothing is pushed anywhere. There is no remote mutation in this skill.

## Name the target

A named path goes straight to work. A blank invocation or explicit repo-wide wording is the only license to survey: rank candidates by bloat signal, size, duplication, indirection depth, and branch density, then work the list in order, one target committed before the next begins. Anything identifiable scopes to itself. Escalating a named grievance into a whole-tree campaign is this skill's worst failure, and trigger phrasing alone never distinguishes a single target from a sweep.

## Separate interior from boundary

Inventory the target's consumers and mark each surface as one of:

*   Interior: every caller is in-tree, nothing persisted or shipped.
*   Boundary: public API, wire or on-disk format, config running in someone else's deployment, plugin point, anything a version was promised against.

Interior is a conclusion, not a default: every consumer channel static analysis cannot resolve (reflection, string dispatch, generated code, external integrations, operator runbooks) carries boundary class until evidence or an explicit yes moves it. An empty grep over dynamic dispatch is not evidence; unresolved means boundary. Nothing below proceeds on an unclassified surface.

## Write the contract, then look away

State what the target owes its callers, sourced from call-site usage, existing tests, and the public signature (never from the target's own internals), and build the replacement from that statement alone. Reaching into the old structure for the contract is how the accretion reproduces itself; state the contract, then look away.
## Walk every old behavior

Go through the old implementation function by function, branch by branch within a single function, and for each behavior name where it lives in the replacement or classify it. Read for behavior rather than structure: branches, guards, early returns, side effects, ordering guarantees, error and failure semantics, state transitions. This audit is the only backstop in the method (nothing executable proves the replacement equivalent), so a behavior never read is a feature deleted by accident, and the walk is exhaustive, not impressionistic. Classify each behavior with a one-line reason as one of:

*   Essential: fold it into the replacement.
*   Residue: cut it.

Performance characteristics are out of scope; benchmark separately when the target is hot. Nothing is cut or kept without its classification.

## Ask before touching the boundary

Present every boundary surface and get an explicit answer before touching it. Interior surfaces need no ask; demolish them. Each boundary surface carries a recorded answer:

*   Yes: cut it.
*   No: keep it permanently. It is contract, not residue.

Cut none on silence or after a no. This is the one place the skill stops, and stopping is the design, not hedging.

## Demolish, test, commit

Delete the old implementation and every surface reachable only from it. Do not write an adapter from the new shape back to the old: that resurrects the demolished structure under a new name. Run the repo's existing test suite, and cover every behavior classified essential that had no test. Commit this target atomically before starting the next. A search for every symbol classified residue must return nothing (no unused imports, deps, types, or files survive), while surfaces kept essential or refused at the boundary gate keep their identifiers: they are the contract, not leftovers. Half-demolished is the forbidden state: finish a target or revert it via version control to the last green commit, never ship the middle.

## When it goes wrong

- Residue remains (exit 1): symbols, imports, config keys, or doc references classified residue still resolve. Delete them; do not ship until the search is empty.
- Verifier red (exit 2): the repo's own tests or build fail against the replacement. Fix the replacement or revert the target; never ship red.
- Campaign stalled mid-target (exit 3): a target is half old, half new. Finish it or revert it to the last green commit; never ship the middle.
- Divergence unclassified (exit 4): old behavior neither folded in as essential nor cut as residue. Complete the walk before proceeding.
- Boundary cut without an answer (exit 5): a published surface was destroyed on silence or after a no. Restore it from version control and settle the question.
- Scope exceeded (exit 6): a repo-wide sweep ran off a named target. Revert the untargeted work.
- A half-demolished target is never left in the tree. Revert to the last green commit rather than widen scope or invent evidence, and never swallow a verifier failure or pretend the work is done when it is not.

## What you hand back

Each target produces a clean demolition: consumer contract restated, replacement derived from it, every old behavior classified essential or residue, residue deleted, essential behaviors tested, target committed atomically with the verifier green. A repo-wide campaign produces one such commit per target in ranked order.
