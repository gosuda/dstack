---
name: git-cleanup
description: 'Use when the user explicitly invokes branch or worktree cleanup for a repo with accumulated local branches. Don''t use for remote branch deletion or force-push operations.'
disable-model-invocation: true
---

# Clear out dead local branches and worktrees

This skill inventories every local branch and worktree, sorts them by merge evidence, and deletes only what the human confirms command by command. All writes stay local: confirmed branch and clean-worktree deletions only. Rollback is `git reflog` and remote refs. Remote state is never mutated, and force-push operations are out of scope.

The run is complete when every branch is categorized or surfaced as unanalyzed, every recommended deletion carries its evidence, each exact quoted command has final confirmation, and each command is reported as deleted or failed.

## Enumerate everything before judging anything

Run `git branch -vv` and `git worktree list` to list every local branch and worktree. Record the current branch, the default upstream branch, and every branch the repository own configuration marks protected. Those stay excluded from deletion from the start.

For each branch, determine merge status against its upstream and against the current branch: run `git branch --merged` and `git branch --no-merged`, then `git log <branch> --not <upstream> --oneline` to surface unmerged commits. Categorize each branch as `merged`, `unmerged-with-evidence`, or `unanalyzed` when the upstream is missing or the comparison is ambiguous.

For each worktree, run `git -C <path> status --porcelain` and classify it `clean` or `dirty`. Dirty worktrees are refused for deletion.

Attach the evidence to every recommended deletion: the merge commit SHA, the empty `git log` output proving no unique commits, or the worktree clean status. Branches categorized `unanalyzed` get surfaced with their reason and are never recommended.

## Confirm each command exactly, then run what was confirmed

Present the full categorized list first. For each recommended deletion show the exact quoted command the user must confirm (for example `git branch -d <name>` or `git worktree remove <path>`). Nothing executes at this stage.

Wait for explicit human confirmation of each exact quoted command. Confirmation is never batched, abbreviated, or inferred. Then execute only the confirmed commands, one at a time in the confirmed order. After each command record success (`deleted`) or failure with the exact git error message.

## Refusals and recovery

- Dirty worktree: refuse deletion, report the uncommitted changes, and stop. The user commits, stashes, or discards before retrying.
- Protected branch (the current branch, the default upstream, or any branch the repository marks protected): refuse deletion, name the branch, and stop.
- Unanalyzed branch: surface it with its reason (missing upstream, ambiguous merge comparison) and never delete it. Deletion waits on the user resolving the ambiguity and re-invoking.
- Missing confirmation: stop before execution. Partial results are the categorized analysis only. No branch or worktree is removed without per-command confirmation.
- Command failure: record the exact git error, leave all other confirmed commands pending, and report the failure. Retries are never automatic and scope never widens.
- Accidental deletion recovers through `git reflog` and `git branch <name> <sha>` for branches, or re-adding a worktree with `git worktree add`. State that recovery path when reporting any deletion.

## What you hand back

A categorized report of every local branch (`merged`, `unmerged-with-evidence`, `unanalyzed`, or `protected`) and every worktree (`clean`, `dirty`, or `protected`), each recommended deletion with its evidence and exact quoted command, the set of confirmed commands, and a per-command result of `deleted` or `failed` with the git error message. Branches or worktrees never confirmed stay listed as not deleted.
