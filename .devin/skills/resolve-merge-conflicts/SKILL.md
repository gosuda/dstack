---
name: resolve-merge-conflicts
description: 'Use when a merge, rebase, cherry-pick, or stash pop stops on conflicts. Not for people-mediation conflicts.'
---

# Finish a stopped merge, rebase, cherry-pick, or stash pop

A stopped integration is git waiting on you: a merge, rebase, cherry-pick, or stash pop halted with unmerged paths, and nothing moves until every hunk is resolved deliberately. Your job is to understand why each side changed what it did, keep both intents alive where they fit together, choose honestly where they genuinely conflict, and leave the tree with no markers, green scoped checks, and the integration fully completed.

This is text-conflict work in tracked files only. It has nothing to do with disagreements between people; the shared word "conflict" is the only overlap, and team or interpersonal disputes are out of scope.

Everything here is reversible and local: editing conflicted files, staging resolutions, regenerating lockfiles with the project's own package manager, running scoped checks, and completing the in-progress operation (committing a merge, `git rebase --continue`, `git cherry-pick --continue`, `git stash drop` only after the resolution is committed). There is no push, no tag, no force-push, no remote mutation of any kind. If the human asks to roll back before anything is committed, that means `git merge --abort`, `git rebase --abort`, `git cherry-pick --abort`, or `git checkout -- <file>` for a single file. A hard `git reset --hard` is never offered as a recovery path; it stays the user's own action if they choose it.

## Start from the conflict stop, not from a guess

Run `git status` first. Name which integration is actually in progress and list every unmerged path; `git status` together with `git diff --name-only --diff-filter=U` is authoritative for that list. If there are zero unmerged paths, the reason you were called does not hold, so stop.

When asked to find conflict stops across worktrees, enumerate the registered worktrees from structured porcelain records, resolve each exact gitdir relative to its own workspace, and record the operation markers, unmerged entries, and read errors per workspace. Never parse a commit OID as a path. A complete scan with zero stops ends the run with trigger-not-met plus the enumerated coverage; an unreadable workspace is unknown, never clear. Report a live worker's integration without taking it over, and treat newly created workspaces as invalidating the earlier coverage set.

## Learn both sides before touching a hunk

For each conflicted file, read all three versions: the common ancestor (`git show :1:<file>`), the current side (`git show :2:<file>`), and the incoming side (`git show :3:<file>`). Remember that stage 1 is the ancestor, stage 2 is current, stage 3 is incoming, and that what "current" and "incoming" mean depends on the operation in flight; ours/theirs labels shift between merge, rebase, cherry-pick, and stash application, so name them for this operation before choosing anything. Never apply a blanket choice of one side. Use `read` with the `:conflicts` selector to enumerate the marker blocks, falling back to ranged reads for files the selector returns empty, and reach for `difft` for a side-by-side view whenever either side's intent is unclear.

Then read the primary sources behind both changes: the commit messages, the pull requests, and the original issues or tickets. State each side's intent in one sentence before editing any hunk. If neither side's commit, PR, or linked issue expresses a clear intent, stop and report the ambiguous files, asking the human to supply the missing intent; never invent an intent to drive the resolution.

## Resolve each hunk without inventing behavior

Keep both intents wherever they fit together. Where they genuinely conflict, take the side that matches the integration's stated goal, name the trade-off, and record whatever intent you discarded, because the finishing commit message must name both sides' intents and the resolution rationale. Invent no new behavior in the process, and leave no conflict markers in any resolved file.

A few shapes of conflict need extra care:

- When both sides independently rewrote the same subsystem, build a decision table from the complete original versions: each required behavior, its source evidence, the chosen implementation shape, and any discarded intent. Review history may inform the decision, but recency or number of reviews never picks the winner. Preserve compatible intents within the integration's stated goal and escalate genuinely conflicting contracts instead of inventing behavior. Inspect auto-merged code and the losing implementation's behavior tests for stale aliases, disconnected helpers, and assumptions the selected contract invalidates, while staying inside this integration's scope.
- When replaying from a synthetic or copied parent, compare the ancestor and lane versions against the actual target-base objects. Parent lines absent from the real base are suspected scaffolding, not an automatic deletion set: reconstruct the lane's intended delta on the real base and verify ordering and initialization invariants, since an imported early recovery call can break behavior outside the lane's apparent concern.
- When one side intentionally deleted a subsystem, read the removal rationale alongside the branch's distinct additions. Preserve the removal when it governs the integration, move behavior that is still required to its retained owner, and inspect cleanly merged additions and callers on the removed surface. Anything incompatible or unpreserved gets reported rather than silently dropped or left as a placeholder. When two implementations express the same intent, keep the approved contract shape and combine only distinct semantic gains. Inspect whole affected functions against both parents, including automatically merged tails, and preserve distinct test cases from both sides even when their module names collide.

## Regenerate, stage, check, and finish in that order

When a lockfile is among the conflicted files, regenerate it with the project package manager rather than hand-editing it; if regeneration fails, leave it unresolved and report the failure.

Stage each resolved file with `git add <file>` and confirm `git status` shows zero unmerged paths. A file with a failed check or an unresolvable hunk stays unstaged: leave logically incompatible hunks marked and report the hunk with its competing intent rather than staging something incorrect. If any `<<<<<<<` marker turns up after staging, stop and report its path and line range.

Run the repository's own checks in this order: type checker, tests, formatter, where each exists. The human may name a validation command; otherwise discover the project's own. Scope the runs to the resolution and fix only failures the integration introduced. A pre-existing failure stops the run with a report, never a suppression or workaround. Checks must cover the affected invariants and the relevant feature and configuration surfaces, not merely marker removal; attribute failures with revision-bound comparable evidence. A clean replay followed by red checks is a diagnostic result, not automatic API drift and not an independent reason to treat this stopped integration as a fresh trigger. And recovery never blanket-restores files carrying pre-existing or sibling edits; preserve the exact pre-resolution state before any user-requested rollback.

Finish the operation that actually stopped: committing a merge names both sides' intents and the resolution rationale including any discarded intent; a rebase continues with `git rebase --continue` until every commit is replayed with no conflict remaining; a cherry-pick continues with `git cherry-pick --continue` (committing first, then continuing, when several commits remain); a stash pop ends with `git stash drop` only after the resolved changes are committed, so the stash stays recoverable until the resolution is in history.

If two resolution attempts produce the same check failure, stop: report the conflict pair, both attempted resolutions, and the failure output. If resolving one conflict reveals further unrelated conflicts or issues, hold the line at the current merge, rebase, cherry-pick, or stash scope; do not refactor, clean up, or fix code outside the conflicted hunks.

## When to stop instead

Stop with the tree left unstaged and uncommitted, and say plainly which failure holds and where: no unmerged paths, so there was nothing to resolve; a hunk whose sides are logically incompatible without introducing incorrect behavior; a lockfile the package manager cannot regenerate; a check failure the integration introduced that you cannot fix, or a pre-existing failure blocking progress; a marker surviving after staging; an intent neither side's sources express; scope creep beyond the conflicted hunks; or two attempts converging on the same failure. If fewer than all conflicted files are resolved, the run is incomplete: do not commit, do not claim success, and report every unresolved hunk by file and line range.

## What you hand back

A per-file report listing each resolved hunk with its chosen resolution and any unresolved remainder; the lockfile regeneration result; the scoped-check outcome, pass or named failure; and the final `git status` summary showing the integration complete.
