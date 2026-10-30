---
name: partition-scopes-to-subagents
description: 'Use when asked to partition non-overlapping scopes across subagents and drive each to completion. Not for concurrent independent sub-tasks: use parallel-launch.'
---

# Partition scopes to subagents

You take work the user has divided into named, non-overlapping scopes and drive every scope to completion with subagents: one implementer per scope, then a different reviewer per scope, then fixes until the reviewer is satisfied. Everything lands in local files (briefs, per-scope artifacts, review and fix reports, and a coordination map); rollback is version control or undo, and nothing touches a remote.

## Confirm the scopes do not overlap

Before dispatching anyone, confirm each named scope touches disjoint file sets, or that the user explicitly approved the overlap. If two scopes target the same file, stop and ask the user to clarify boundaries. Include every active worker and your own writes in the occupied-file map; shared manifests and integration surfaces get one named owner. Mark cross-scope findings REPORT, DO NOT EDIT, and route them to their owner. Merge or sequence tasks that need the same file: a shared checkout is not permission for overlapping writers. When scopes need integration, give one owner exclusive writes to the integration surface and have other workers report rather than edit, publishing only complete coherent increments (never placeholder implementations or interface-only changes as accepted work).

## Set up the map and briefs

Adopt the user's DAG or war map as the execution skeleton when one is supplied; otherwise derive a flat map from the stated scopes, one node per scope with no ordering edges. The map is the source of truth for what each subagent must do.

Write one self-contained brief per scope: the one-sentence goal, the exact files or directories in scope, the constraints from the parent task, cross-scope caller migrations that belong to this scope (so workers never repair foreign files), dependencies, non-goals, permitted verification, the report location, and the observable completion predicate. Briefs carry paths, not pasted content.

## Implement, then review with fresh eyes, then fix

Dispatch one fresh implementer subagent per scope with its brief. Each works in isolation and writes its result to a per-scope artifact file.

After each implementer finishes, dispatch a new reviewer subagent for that scope. The reviewer is never the implementer. If the reviewer reports findings, dispatch a fix subagent for that scope and collect its fix report, repeating review until the reviewer reports no blocking findings for the scope. A reviewer finding that needs cross-scope knowledge comes back to you, not the implementer: record the escalation in the coordination map and resolve it before marking that scope done.

After each scope reaches its terminal review status, write one entry in the actual-work map: scope name, implementer status, reviewer status, fix count, and terminal verdict. The skill is done when all scopes carry terminal verdicts and all review reports are filed.

Inspect returned artifacts and live file state before accepting reports: validate claimed test selection and failure witnesses rather than accepting a passing count. After all relevant writes land, you perform the authorized integration verification against the assembled tree; pre-integration lane results do not establish integrated success. Do not mark the map done while required integrated checks remain unrun.

## When a scope goes wrong

A subagent reporting BLOCKED goes in the map as BLOCKED for that scope; keep working the other scopes and report the full blocked list after the convergent scopes finish. A crashed subagent gets re-dispatched with the same brief to a fresh implementer for that scope, without carrying forward partial state from the crash. If a scope stays BLOCKED after one re-dispatch, record the exhaustion and stop; do not loop indefinitely. On any worker failure, inspect and preserve existing work before reassignment, record the remaining scope, ensure the predecessor is no longer writing, and never infer agent survival, background-job death, or resume support from a provider error code. Keep this skill's fresh-reviewer policy unless it is separately and explicitly changed.

## What you return

One `actual-work-map.md` listing every scope with terminal status (done, blocked, or failed), reviewer verdict, and fix count, plus one review report per scope, one fix report per scope that required fixes, and one brief file per scope.
