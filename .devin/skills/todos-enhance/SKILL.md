---
name: todos-enhance
description: 'Use when tasks are too vague, read as headings, or the user asks to sophisticate the todos. Not for stale reconciliation: use todos-update. Not for adding requirements: use todo-add.'
---

# Turning a vague list into executable work

You rewrite a coarse task list in your reply so every item names one behavior, sits where its dependencies are met, and carries a checkable finish line. Nothing leaves this session as a file, version control, or remote change.

Use this when the user says to sophisticate the todos, says the tasks are too vague, or the list reads as headings rather than executable work. It does not reconcile a drifted list against the tree (that is todos-update) and does not add requirements (that is todo-add). The full current task list must be present in context; without it, stop and say a task list is required.

## Diagnose every item once

Classify each item into exactly one bucket:

- atomic: one behavior, executable as written.
- compound: hides two or more separable pieces of work.
- vague: names an area, not a change.
- unordered: correct, but placed where its dependencies are unmet.
- unverifiable: executable, but nobody can tell when it is done.

## Split, order, then pin the finish line

1. Split every compound item into atomic tasks. A task is atomic when it names one behavior and can be executed without a further design decision. Length is not the test: a one-line task that still forces a choice between two approaches is compound. Stop when no task hides more than one decision.
2. Draw the dependency edges. B depends on A only when B cannot function without the output of A, not merely because A feels earlier. Mark genuinely independent tasks as parallel. Introduce a phase only where a real barrier exists, never to make the list look organized.
3. Give every task one observable acceptance test: a command, an output, or a state someone can check. Stop when zero items remain vague or unverifiable and every task carries exactly one criterion.

## Know when to stop instead of claiming success

If the list is empty, the finish condition holds vacuously; report that. If any task remains unclassified, unverifiable, or compound after one pass, do not claim success. Report the remaining items by class. On any failure, discard the rewritten list and present the diagnostic; the original list is unchanged.

The output is a rewritten task list where every item is atomic, ordered by real dependency, and annotated with one observable acceptance criterion each, or a terminal report listing the remaining unclassified or unverifiable items when the finish condition cannot be reached.
