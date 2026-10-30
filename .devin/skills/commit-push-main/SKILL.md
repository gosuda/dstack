---
name: commit-push-main
description: 'Use when a human explicitly asks to commit and push directly to the default branch, with no feature branch and no pull request. Not for another checked-out branch: use commit-push-current.'
disable-model-invocation: true
---

# Ship the default branch directly

This skill puts the working tree on the default branch of the repository. The push target is the resolved default branch, and any other branch is refused. Branches are never created or switched here. Explicit human invocation authorizes both the commits and the push on the default branch. The work is done when `git status --porcelain` is empty and `git rev-list --left-right --count origin/<default>...HEAD` prints `0 0`.

## Confirm the destination before touching anything

Run `git status`, `git diff HEAD`, `git branch --show-current`, `git log --oneline -10`, and `git remote`. A missing `origin` ends the skill before any commit, because the default branch cannot be verified and nothing could be pushed. Remotes are never added, invented, or guessed.

Otherwise prove the push destination first. Run `git config --get-all remote.origin.push` and stop before any commit on any output line, since a custom refspec would redirect `git push origin HEAD`. Run `git remote get-url --all origin`, stopping before any commit on failure or on more than one line, and record the single fetch line as FETCH_URL. Run `git remote get-url --all --push origin` the same way to record PUSH_URL, refusing an ambiguous push the same way. FETCH_URL and PUSH_URL must match exactly as strings. A triangular configuration cannot stand as its own preview, so report it and stop before any commit.

Resolve the default from authoritative advertisement only. Run `git ls-remote --symref origin HEAD` and take the branch named by the first `ref: refs/heads/<name>` line. Failure or a missing ref line means `DEFAULT_BRANCH_UNRESOLVED`, so report and stop before any commit. Confirm the same branch through `git ls-remote --symref "$PUSH_URL" HEAD`, and report any disagreement with the push destination before any commit. Prove the branch exists on both destinations with `git ls-remote --heads origin <default>` and `git ls-remote --heads "$PUSH_URL" <default>`. Empty output on either means the default is absent there, so report and stop before any commit without creating it. A failed call means the remote is unobservable, which also stops the skill. The `origin/HEAD` cache and any `gh` fallback stay unused. Guessing is never allowed.

Read `git rev-list --left-right --count origin/<default>...HEAD 2>/dev/null || echo NO_REMOTE_BRANCH`. On `NO_REMOTE_BRANCH`, materialize the proven ref with `git fetch --no-tags origin refs/heads/<default>:refs/remotes/origin/<default>` and read the counts again. A failed fetch stops the skill before any commit.

## Stay on the default branch with work worth shipping

Refuse anything but the resolved default. A different checked-out branch or a detached HEAD ends the skill before any commit, with no branch created or switched. Point the human at `commit-push-current` for the checked-out branch or `commit-push-pr` for a feature branch.

Classify the work. A clean tree with zero on the right side of the counts means nothing to do, so report and stop. A clean tree with commits ahead of the target skips authoring and goes to the preview. Anything else continues to `commit`.

Author with `commit`, following its message conventions, atomicity rules, and staging discipline (not restated here). Its default-branch auto-branching does not apply, because invocation here already authorizes committing on the default. Its reset and branch-deletion rollback does not apply either, because recovery here never uses hard reset or branch deletion. Past this point when `commit` reports the tree committed or nothing to commit.

Run `git remote` again. Without a remote named `origin`, report local-only with the commit list and stop. Remotes are never added or guessed.

## Preview the exact push and wait for approval

Refresh the tracking tip with `git fetch --no-tags origin refs/heads/<default>:refs/remotes/origin/<default>`, stopping without pushing on failure. Prove the preview tip is the push tip: `git ls-remote origin refs/heads/<default>` and `git ls-remote "$PUSH_URL" refs/heads/<default>` must each return one line with the same non-empty SHA. Missing, failed, or disagreeing output means divergence or an unobservable destination, so report and stop without pushing. The earlier URL match plus this SHA check proves the same repository state, not just the same branch name.

List the full set with `git log --oneline origin/<default>..HEAD`. A non-zero left count means the remote holds commits HEAD lacks. Name them in the preview, because the push will be rejected until they are integrated. Show the target, the matched URLs, the matched tip SHA, and the commit list, then wait for the human to approve the exact mutation set (platform blocking question tool, chat fallback). Silence or refusal stops with nothing pushed. On approval, re-resolve both tip SHAs and require the same identical SHA. Any difference gets a fresh preview and another wait.

Push with `git push -u origin HEAD`. Force-push is never used.

Verify with `git status --porcelain` (empty) and `git rev-list --left-right --count origin/<default>...HEAD` (`0 0`). Report residue instead of claiming done.

## When to stop instead

- Checked-out branch is not the default, or HEAD is detached. No commit is created.
- Nothing to do. No mutation occurs.
- Custom refspec, unobservable or multiple URLs, or fetch-push divergence. Never authorize an ambiguous or triangular push.
- Default unresolved, push-side name disagreement, or existence unproven on either destination. Report `DEFAULT_BRANCH_UNRESOLVED` or the disagreement and stop. The remote branch is never created by this skill.
- Push-side tip missing, unobservable, or disagreeing with the preview tip. Approval never covers another tip set.
- Tracking-tip refresh failed before the preview. Report and stop without pushing.
- No `origin` remote. Report local-only. Remotes are never invented.
- Push rejected on a diverged branch. Report the rejection with the counts and leave resolution to the user. Silent pull or rebase repairs are out of scope.
- Verification residue. Report the files or commits left over.

## What you hand back

The committed tree on the default branch, the one push to `origin/<default>`, and a report naming the branch, the matched URLs, the matched tip SHA, the pushed hashes and subjects, and the verification result. Without `origin`, a local-only report naming the commits left unpushed.
