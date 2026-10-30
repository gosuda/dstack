---
name: git-branchless
description: 'Use when asked for multi-commit stack edits, rebases, fixups, or stacked-PR publishing with branchless git idioms. Not for plain-git workflows in repos without branchless.'
disable-model-invocation: true
---

# Edit stacks without branches

Branchless git treats the commit stack as the unit of work. Commits move, fixups absorb, and restacks propagate, all without juggling branch names. Plain-git commands stay fine wherever they fall outside the classes below.

This skill goes silently inert in repositories where branchless is absent, yielding to plain git. Interactive rebase, hard resets, and force flags are never used here.

## Confirm branchless is active or stand down

Resolve the git common directory so linked worktrees are handled, then run:

```
test -d "$(git rev-parse --git-common-dir)/branchless" && git config --get branchless.core.mainBranch
```

Both checks passing means the skill is active. Acknowledge with one line: `git-branchless active: main=<value>`. Either check failing means the skill is silently inert. Emit one line: `git-branchless not initialized; skill inactive`. Make no mutation and yield to plain git. Never suggest `git branchless init` unless the user explicitly asks how to enable.

## Sort the work into its operation class

| Class | Always | Never |
|---|---|---|
| Stack edits (reorder, fixup, squash, split) | `git move`, `git move -F`, `git reword`, `git split`. | `git rebase -i` to drive stack edits. |
| Base updates (rebase a stack onto fresh main) | `git sync --pull` (or `git move -b 'stack()' -d origin/main`). Read the skip summary. | `git pull --rebase` against a stack. |
| Undoing committed history | `git undo -i`. | `git reset --hard <SHA>` against any commit already made. |
| Discarding local work in progress | `git hide -r <tip>` (recoverable). | `git branch -D` or `git reset --hard` purely to wipe. |
| Branch creation for ephemeral work | Detached HEAD until publish; commit immediately, branch later. | `git checkout -b feature/X` before the first commit exists. |
| Publishing (feature stacks) | Name the tip, then `git submit -c @` (first publish) or `git submit @` (update). Stock `git push -u origin <feature>` only if submit is denied. | `git submit` targeting `main`, `master`, or `release/*`. Writing `--force` or `--force-with-lease` in recipes. |
| Publishing (gated main) | Only when the user requested main or HEAD is already on local `main` or `master`: `git sync --pull`, prove `@` descends from `origin/main`, then stock `git push -u origin main`. Detached: fast-forward-only attach to local main first. | `git submit` for main. Blind `git switch -C main` or `git branch -f main`. Any force flag. |

Three plain-git edge cases stay legitimate and unblocked: `git reset --soft HEAD~` against staging when nothing is committed yet; `git rebase --onto` for a one-off non-interactive upstream sync in a repo where branchless is not initialized (the skill is inert there anyway); `git checkout -b` when the work is genuinely about to be pushed.

## Pick the command sequence for the goal

| Goal | Command sequence |
|---|---|
| Insert a fixup mid-stack | `git commit --fixup <target>` then `git move -s HEAD -d <target> --fixup` |
| Reorder commits | `git move -s <src> -d <dest>` |
| Squash two commits | `git move -s <child> -d <parent> --fixup` |
| Split a commit | `git split <commit>` |
| Rebase stack onto main | `git sync --pull` |
| Find first failing commit | `git test run --search binary --exec '<cmd>' 'stack()'` |
| Recover lost work | `git undo -i` |
| Discard a local experiment | `git hide -r <tip>` |
| Publish feature stack | `git branch <name> @` then `git submit -c @` (update: `git submit @`) |
| Land on main (gated) | `git sync --pull` plus ancestor of `origin/main` plus stock `git push -u origin main` |
| Post-merge hygiene | `git sync --pull` then `git hide -r <merged-tips>`; optional `git gc` |

## Pass the publish gate before anything leaves the machine

Main path: only when the user requested main or HEAD is already on local `main` or `master`. Run `git sync --pull`, prove `@` descends from `origin/main`, then stock `git push -u origin main`. `git submit` never targets main. Force flags never appear. Detached heads attach to local main fast-forward-only first.

Feature path: `git branch <name> @` then `git submit -c @` (first publish) or `git submit @` (update). Stock `git push -u origin <feature>` only when submit is denied. Never target `main`, `master`, or `release/*`. Never write `--force` or `--force-with-lease`.

GitLab feature path (provider constraint): `git submit` has no verified submit-to-MR path on GitLab, so publish the stack as one MR per branch. Local restack mechanics are unchanged. For each stack branch from bottom to top: push the branch with stock `git push -u origin <branch>`, then after the exact-write preview is approved create its MR with `glab mr create --source-branch <branch> --target-branch <parent-or-main> --title <title> --description-file <file> -y` (forks add `-H <head-repo> -R <target-repo>`; each stacked MR targets its parent branch). Select the provider from the verified remote, never by guessing the host. `glab mr create` has no `--dry-run`, so the previewed command, title, description, and branch pair stand as the preview. Never target `main`, `master`, or `release/*` as a source, and never write `--force` or `--force-with-lease`.

## Restack, clean up, and read the skip line

After `git amend`, `git reword`, `git move`, or `git split`, descendants restack automatically in memory. Run `git restack` manually only when the smartlog warns about abandoned subtrees (`✕` ancestors). After a land or merge, run `git sync --pull` then `git hide -r <merged-tips>`; `git gc` stays optional. Read the skip summary line after every `git sync` and `git move`. Speculative-merge skips stay silent unless that line is read.

## When branchless says no

- Not initialized: emit the inert line, make no mutation, yield to plain git. Suggest `git branchless init` only when asked.
- Version-gated flag rejected: fall back to the closest documented alternative and tell the user which feature was unavailable. Unverified flags are never invented.
- `git submit --forge github` is unsuitable for general use (upstream arxanas/git-branchless#1184): stack reordering can lose PR ancestry. Prefer the default forge `branch` with `git submit -c @` or `git submit @` for feature stacks; never submit main. Stock `git push -u` is the gated-main path and the submit-denied fallback.
- The event log is per-repository and per-clone: `git undo` cannot reach state from a different clone or machine. Say so when cross-clone recovery is requested.
- Speculative-merge skips during `git sync` and `git move` stay silent unless the summary line is read. A missed skip means re-run and read the summary before assuming success.
- Errors are never swallowed and done predicates are never pretended. A failed command gets its exact failure reported, then the skill stops rather than widening scope.

## What you hand back

The applied branchless command sequence and resulting smartlog state; or a publish result (feature stack submitted, or main pushed after the ancestry check); or the explicit inert line `git-branchless not initialized; skill inactive`.
