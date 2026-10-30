---
name: simplify
description: 'Use when the user asks to simplify a change-set, diff, branch, or module and the right level is not yet decided; routes each cut to the simplification skill that owns it.'
---

# Simplify: send each cut to the level that owns it

A simplification request is a routing problem, not a line-count problem. The diff that triggered the ask is entry evidence only: it points at where to look, never decides how far the cut goes. Polishing hunks while the real weight sits one call away in an untouched caller, a shallow module layer, or a second artifact class is how naive passes fail. This skill looks at the changed code plus the callers, module boundaries, and dependencies around it, sends each piece of work to the skill that owns that level, and integrates everything into one proven outcome.

## Start with the change, then look around it

Resolve what is actually under review before judging anything. An explicit `simplify against <ref>` bypasses everything else and diffs against that revision directly. Otherwise resolve the base from pull-request evidence, then the upstream tracking branch, then the remote default branch, in that order; never guess `main` or `master`, and never fall back to a working-tree-only diff on a branch with committed history but no resolved base, since that silently drops committed work. If no base resolves, stop and ask for one. An unborn HEAD means user-named files only; a root commit means the working tree is the scope. Read authorized untracked files alongside the tracked diff, never delete an untracked file, and name meaningful unauthorized untracked files as remaining work rather than silently ignoring them. An empty result after all valid resolutions is exit 11: nothing to do.

Two words change the reach. `simplify --surgical`, `added lines only`, or `no caller moves` clamps the whole run to the diff hunks, remove-only, with no caller migration. Without those words the default reach covers added lines, modified lines, and the affected structure the change forces: proven in-tree callers the simplification cannot land clean without.

Then inspect the surroundings, not just the hunks: who calls the touched code, which module or contract boundary it sits on, and which dependencies or artifact classes move with it. A finding whose level is still unclear after that inspection is reported as a candidate with file, line, and reason, never force-applied at the wrong level.

## Where each cut belongs

Each scope goes to exactly one owner, with disjoint scopes and no double coverage:

- A change that is still being written or restructured, or a question asked before adding a helper, wrapper, config key, branch, or dependency, belongs to `minimalism-driven`: smallest form that satisfies the ask, deletion before replacement before addition, no adjacent improvements.
- Weight carried by comments belongs to `no-comments`: the knowledge moves first into names, control flow, domain types, tests, or the existing design record, and only then does the comment go. Legal notices, tool directives, and public documentation without an equivalent home never move.
- One named module, file set, or dependency slice whose interior shrinks while its consumer contract holds belongs to `code-simplification`, including code-debris or codecleanup (code cleanup) in that scope: classify every divergence essential or residue, collapse shallow layers into their surviving owners, migrate all in-scope callers in the same change.
- A layout that must change, collapsing modules, crates, or dependency edges, belongs to `architecture-simplification`. That skill fires on explicit human invocation only and executes an approved scope slice by slice; a smaller cleanup never promotes itself into it.
- Residue spread across more than one artifact class, code plus docs, tests, config, workflows, or generated sources with the observable boundary unchanged, belongs to `guillotine`: candidate ledger plus proof from both directions before any cut.
- A cut that removes a consumer-facing surface, compat shims, adapters, feature flags, or version gates, belongs to `refactor-break-compat`: exact demolition manifest with consequences previewed, explicit human confirmation, then one atomic cutover with every caller rewritten and no shim or alias left behind.

Shape signals that help triage module interiors live in `references/quality.md`; cost signals that ride along with a structural route live in `references/efficiency.md`. Both are triage aids, not detectors: the owning skill above decides.

## Running the route

Simplify itself is the single integration owner. It dispatches disjoint scopes to their owners, sequences dependent rewrites so boundary-gated cuts land after the interior they depend on, and every routee result comes back through simplify for integration: no owner merges past the others, and unrelated repo-wide expansion is never in scope. Structures the inspection clears stay untouched.

What holds at every level, carried here so no route needs re-derivation: all writes are reversible local writes with version control as the rollback, and there is no remote mutation. A cut that reaches a live consumer surface, stored data, or anything non-reversible waits for an explicit yes; on silence the surface stays and a compat removal hands to `refactor-break-compat` with file, line, evidence, and reason. No compatibility alias, shim, tombstone, dual path, or deprecated wrapper survives any route. A red baseline stops all cutting before it starts; after each increment run the narrowest applicable verifier first, then the repository's own test command, reverting the increment on red. Test edits are mechanical migration to the new contract only, each with a recorded reason; deleting, suppressing, skipping, or weakening tests to force green is never done here. Close with a ghost sweep: string references to every removed concept across code, tests, docs, configs, and messages must resolve to nothing or the candidate is reclassified not-dead.

## What comes back

One integrated result: the cuts applied per owning skill with their commits, every migrated caller, boundary decisions with their yes or no evidence, reverted increments with failing checks, ghost-sweep result, and verifier evidence.

Terminal classification keeps the long-standing meanings its consumers rely on, including the autopilot G2 gate which passes on 0, 11, and 12, absorbs a self-reverted 13, and halts for human re-planning on 14 and 15:

| Code | Meaning |
|---|---|
| 0 | Clean: compressed at the right levels, checks green, no residue |
| 11 | Empty diff after all resolutions; nothing to do |
| 12 | Findings existed but the survivor set was empty; report attached, no patch |
| 13 | A fix regressed behavior; that commit auto-reverted, prior green commits remain |
| 14 | The post-fix audit caught new bloat in the simplify chain; the chain reverted |
| 15 | A commit mixed more than one concern; split before merge |

A non-empty raw list with an empty survivor set is exit 12, never silent success. Line delta is reported evidence only, never the predicate; no percentage or count target is accepted.

## What simplify never does

It never re-derives a module blind to dodge a handoff, never cuts a boundary surface on silence, never widens scope past the named change plus its proven callers, and never leaves two owners cutting the same lines. Anything beyond the forced set that no route owns is emitted as a candidate with file, line, and reason, not dropped and not force-applied.
