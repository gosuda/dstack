---
name: todo-add
description: 'Use when a message contains `TODO ADD: <requirement>`. Not for deepening coarse lists: use todos-enhance. Not for resyncing lists: use todos-update. Not for retitling/reordering/completing todos.'
---

# Adding one requirement in two places

You take a single `TODO ADD:` line and record it twice, once as a native todo and once in its durable requirement source, so both stay in agreement. Writes stay reversible and local, limited to one durable source and one native todo, with rollback through version control or undo and no remote mutation.

This runs only when a message contains `TODO ADD: <requirement>`. It does not deepen coarse lists, resync drifted lists, retitle, reorder, or complete work. Those belong to todos-enhance or todos-update.

## Pick the one durable source

Use the current durable plan or specification when one clearly owns the work. If none exists, create or update `.outline/requirements/todo-add.md`. Never scatter the requirement across multiple documents. The durable source and the native todo must contain the same requirement in the same turn.

## Add the requirement without losing it

Follow this order, because the recovery rule depends on it.

1. Parse the text after the first `TODO ADD:` as one requirement. Reject an empty requirement.
2. Compare it semantically with the current durable source and the native todo list.
3. If it is already present in both, return `Duplicate: no change` and stop.
4. If it conflicts with an existing requirement, write nothing. Ask one question that presents the two incompatible forms and wait.
5. Assign the todo phase by the work's owning module or domain, not by wording or chronology.
6. Append the native todo first, with a backlink or stable reference to the requirement source.
7. Update the durable requirement source with the same normalized requirement and the native todo identifier.
8. Verify both sides resolve to the same text and ownership.

Refusals that hold for the whole flow: no empty requirement, no durable-source write when native todo creation failed, no silent removal of a retained todo on partial failure, and no write while a conflict is unresolved.

## Handle the one partial failure honestly

If native todo creation fails, do not touch the durable source. If the durable-source write fails after native todo creation, retain the native todo, mark it `requirement-source-write-failed`, and warn with the exact failed path and the recovery action. Do not claim success. Never silently remove the retained todo.

Return `Added`, `Duplicate`, `Conflict`, or `Partial failure`, plus the requirement-source path and native todo identifier when they exist.
