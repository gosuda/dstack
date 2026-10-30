---
name: subagent-driven
description: 'Use when a user says execute with subagents or hands over an ordered multi-task plan. Not for credential, paid, or deployment work, or any mutation outside the skill''s designated workspace.'
---

# Subagent-driven development

An ordered multi-task plan becomes a chain of fresh subagents, each implementing one task, each gated by its own reviewer, with the whole branch reviewed once more before an atomic ship. You orchestrate. Workers implement and review in isolation. The ledger at `.outline/sdd/progress.md` tracks completion, and `git log` rebuilds it when sessions compact.

Saying "execute with subagents" or handing over an ordered multi-task plan invokes this skill. Credential, paid, and deployment work stay out, as does any mutation outside the designated workspace. Publishing the branch via git-branchless `submit` needs explicit human invocation. All other writes (commits, briefs, reports, diff packages, the ledger) stay local, with version control as the rollback.

## What the plan must give you

The plan file defines task boundaries, file scopes, and done criteria. Model selection for each dispatch is required. An omitted model silently inherits the session most expensive model and defeats cost control, so always set one explicitly. Fresh subagents see only what gets put in front of them: the task brief path, relevant context from earlier tasks, and every decision or interface the implementer must respect.

Before execution, scan the plan for self-conflicts (tasks contradicting each other, Global Constraints, or plan-mandated defects). Batch every finding into one user question. A clean scan proceeds silently.

Check the recovery ledger before starting: `cat "$(git rev-parse --show-toplevel)/.outline/sdd/progress.md"`. Tasks marked complete there are done. Resume at the first incomplete task. When the ledger is missing, reconstruct it from `git log` using the plan task order and the timestamps of commits matching each task concern.

## Run each task through implement, review, and gate

Work tasks in order, one at a time:

1. Split the task into one-concern work with explicit file boundaries. Two tasks editing the same file are not independent. Sequence or merge them.
2. Run `scripts/task-brief PLAN_FILE N`. It extracts the full task text to a uniquely named file and prints the path. That brief is the single source of requirements.
3. Record the BASE commit (current HEAD) before dispatching.
4. Dispatch one fresh implementer with `references/implementer-prompt.md` filled in. Fresh means no carried context and no resumed worker. Always name the model.
5. The implementer works, verifies, commits one concern, self-reviews, writes a full report to the report file, and returns a short status: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, or BLOCKED.
6. Resolve the status before moving on. Missing context gets supplied and the task re-dispatches. Reasoning problems re-dispatch on a more capable model. Oversized tasks split first. Plan errors escalate to the user. A worker saying it is stuck always triggers a change of some kind before retry. Never retry unchanged.
7. Run `scripts/review-package BASE HEAD`. It writes one file (commit list, stat summary, full diff with context) and prints the path. Use the recorded BASE, never HEAD~1.
8. Dispatch a fresh reviewer with `references/task-reviewer-prompt.md` filled in, handing it the brief path, report path, diff-package path, and the verbatim Global Constraints.
9. Gate on audit clean and verifier green, then mark the task complete. Critical or Important findings dispatch one fix worker with the complete findings list, followed by re-review. An audit that cannot clear aborts the chain rather than building on it. Never squash or force through.

Requirements living in unchanged code or spanning tasks come back from reviewers as Cannot Verify from Diff items. Those never block: resolve each centrally before marking the task complete. A confirmed gap is a failed spec review. Return to the implementer, then re-review.

## Close the branch and ship it whole

After every task lands, run `scripts/review-package MERGE_BASE HEAD` with MERGE_BASE from `git merge-base main HEAD`. Dispatch the final reviewer on the most capable model, pointed at the Minor findings the ledger accumulated. Its findings dispatch one fix worker with the complete list, then re-review.

Ship through the atomic path: sort work into atomic commits in detached HEAD, then publish with git-branchless `submit`.

Then run the closing chain in this order. Complete the implementation path first. Run this skill own review and fix gate to green (audit clean and verifier green per task, then the whole-branch review), bounded at 3 fix cycles per unit. Past that bound, stop as blocked or non-converged instead of widening scope to unrelated code. Finish with an offensive simplify pass: re-derive the general case from contracts, delete old structure with no shims, aliases, or flags, collapse special cases, migrate every caller in the same change, keep one concern per atomic commit. Ask first before removing any live consumer surface, and stay inside this skill authority throughout. Run the verifier after each increment and revert the increment on red. End with a simplify compression pass over dead branches, duplicated logic, and one-use wrappers, with behavior preserved and checks green.

## Recover dead workers without destroying the tree

A worker dying mid-task leaves a dirty tree. Inspect first (`git status`, `git diff`) and revert only that worker changes: discard its edits, remove the stray files it created, leave pre-existing uncommitted work untouched. Never blanket-reset or `git clean` the whole tree. A dead worker never resumes onto a dirty tree, and the next task never builds on uncommitted partial work.

Before retrying, inspect the designated workspace, actual commit objects, dirty and untracked state, report, and ledger. Verify which outcomes exist and which remain incomplete. Continue only the remaining work in that preserved workspace, with a brief naming completed work that must not repeat. Provider or quota failures with no productive execution are resource blockers, never evidence that a full redispatch will help. Partial work and ownership carry over, and recovery grants no new push, merge, or publication authority.
