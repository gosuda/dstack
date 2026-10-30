---
name: todos-update
description: 'Use when user asks to update todos, resync the task list, say what to do next, or plan and tree have drifted apart. Not for coarse lists: use todos-enhance. Not for adding requirements: use todo-add.'
---

# Resyncing the task list with what actually landed

You reconcile the task list with the codebase and name the single next move. All writes stay reversible and local through the todo tool, with rollback through undo and no remote mutation, and no implementation happens here.

Use this when the user asks to update the todos, resync the task list, say what to do next, or the plan and the tree have drifted apart. It does not sophisticate coarse headings (that is todos-enhance) and does not add requirements (that is todo-add).

## Gather the three sources first

You need the current task list and the codebase state (file reads plus test or command output). Conversation context about design decisions is the optional third source for spotting overtaken items. Never mark an item complete without proof: test output, a command result, or a `path:line` reference. Someone saying an item is done is the claim under test, not proof. If the codebase state cannot be fully determined, return a partial result with explicit gaps rather than pretending the list is clean.

## Classify, prove, and write back

1. Read the current task list.
2. Inspect the codebase: read changed files, run targeted tests or commands, and check `path:line` references to determine what actually landed for every item.
3. Read conversation context for design changes that may have overtaken items.
4. Classify each existing item exactly once:
   - landed: done, with proof.
   - still-open: unchanged, still required.
   - overtaken: a design change made it unnecessary.
   - blocked: cannot proceed until something external clears.
   - newly-discovered: not on the list, found during the work.
5. Keep every landed claim attached to its proof (the test, the command output, or the `path:line` that demonstrates it). An unproven completion stays still-open; record the proof gap in the report.
6. Write the reconciled list back through the todo tool. If the tool replaces rather than patches the list, capture item identity, text, completion, and in-progress state before replacement and preserve those states in the reconciled list. Restore state using the tool current identifiers or matching contract, not stale display text or assumed ordering. Retagging does not reopen completed work.
7. Drop each overtaken item with a one-line reason recorded in the report, never silently. A dropped item with no recorded reason is indistinguishable from a forgotten item.
8. Name exactly one next action: the first still-open item whose blockers are all clear, stated as a concrete action rather than a heading. When two items tie, pick the one that unblocks more of the remaining list. When every remaining item is blocked, name the one blocker that has to clear first, one answer rather than a list.
9. Emit the delta only: what changed classification, and why.

If the todo tool fails, do not fabricate a list state. Report the error; the list remains unchanged.

The delta report lists Completed, Still open, Overtaken, Blocked, and New; every landed item cites its proof, exactly one next action or one blocker is named, and zero stale items remain.
