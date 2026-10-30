---
name: commit-push-current
description: 'Use when a human explicitly asks to commit and push to the checked-out branch with no branch creation and no pull request. Not for the default branch: use commit-push-main; not for a pull request: use commit-push-pr.'
disable-model-invocation: true
---

# Push the branch you are standing on

You ship the working tree on whatever branch is checked out, and nothing else. You never create a branch, switch branches, open a pull request, or force-push. The human's explicit request to run this skill is the authorization to commit on this branch and push it to `origin/<current-branch>`, and that authorization covers exactly one previewed push, never anything beyond it.

If the checked-out branch happens to be the default branch, treat it purely as the checked-out branch. You do not get `commit-push-main` grade pre-commit proof here. When someone wants a proper default-branch publication, send them to `commit-push-main`. When a feature branch needs a pull request, send them to `commit-push-pr`. You are done when `git status --porcelain` is empty and `git rev-list --left-right --count origin/<current-branch>...HEAD` prints `0 0`. Anything else is residue you report, not success you claim.

## Take stock of the tree and the branch

Run `git status`, `git diff HEAD`, `git branch --show-current`, `git log --oneline -10`, `git remote`, and `git rev-list --left-right --count origin/$(git branch --show-current)...HEAD 2>/dev/null || echo NO_REMOTE_BRANCH`. When `git remote` shows no `origin`, skip every push-destination check and every default-branch resolution below. You will commit and then report local-only.

`NO_REMOTE_BRANCH` means the local tracking ref is missing and the branch may be new to `origin`. The next section tells you how to tell.

Classify what you found:

- Empty branch name means detached HEAD, so there is no branch ref to push. Say so and stop before any commit. If the human actually wants a feature branch, `commit-push-pr` in no-PR mode creates one.
- Clean tree and zero on the right side of the counts means nothing to do. Say so and stop. No mutation happens.
- Clean tree with commits ahead of the push target means there is nothing to author, so skip the commit step and go preview the push. A clean tree with `NO_REMOTE_BRANCH` also skips ahead as possibly new to `origin`.
- Anything else, including a dirty tree, continues. With no `origin` you will commit and then report local-only. Otherwise you run the preflight below and then author commits. Only a clean tree skips authoring.

## Prove the destination is unambiguous before committing

This check needs no network and runs only when `origin` exists.

Run `git config --get-all remote.origin.push`. Any output line is a custom push refspec that would redirect `git push origin HEAD` somewhere unexpected, so report it and stop before any commit. Run `git remote get-url --all origin`. Failure means the fetch destination cannot be observed, and more than one line means multiple fetch destinations. Either way report and stop before any commit, and record the single line as FETCH_URL. Run `git remote get-url --all --push origin`. Failure means the push destination cannot be observed, and more than one line means multiple push destinations. Either way report and stop before any commit, and record the single line as PUSH_URL. FETCH_URL and PUSH_URL must match exactly as strings. Any difference is a triangular configuration where the fetch-side preview cannot stand for the push destination, so report it and stop before any commit.

If the push-target state is not `NO_REMOTE_BRANCH`, the branch already has a local tracking ref, so no default-branch base is needed now. Allow the commit and leave remote re-verification to the pre-push preview. If the state is `NO_REMOTE_BRANCH`, the branch may be new, so observe the remote with `git ls-remote --heads origin <current-branch>` and `git ls-remote --heads "$PUSH_URL" <current-branch>`. If either call fails, the remote cannot be observed from here. Allow the commit and let the pre-push preview stop the push if needed. Non-empty output on either means the branch already exists on the remote, so allow the commit and defer to the preview. Empty on both means the branch is truly new, so resolve `<default>` from authoritative advertisement only (`git ls-remote --symref origin HEAD` confirmed against `git ls-remote --symref "$PUSH_URL" HEAD`, then proven with `git ls-remote --heads origin <default>` and `git ls-remote --heads "$PUSH_URL" <default>`) to anchor the range `origin/<default>..HEAD`. That advertisement is the only source. Never consult an `origin/HEAD` cache or a `gh` fallback, and never guess a default branch. Missing, disputed, or unverifiable advertisement or existence proof means report and stop before any commit. An unobservable remote at this stage is the one exception, since it defers to the pre-push preview instead of blocking local commits.

## Author the commits, then handle a missing remote

Author with `commit`, following its message conventions, atomicity rules, and staging discipline (not restated here). Two of its behaviors do not carry over. Its default-branch auto-branching never applies, because invocation on this branch is explicit authorization to commit on it. Its reset and branch-deletion rollback never apply, because recovery here never uses hard reset or branch deletion. You are past this point when `commit` reports the tree committed or nothing to commit.

Then run `git remote`. If no remote named `origin` exists, do not push and do not add, invent, or guess one. Report local-only, naming the unpushed commits, and stop.

## Re-prove the destination, preview the exact push, and wait

Re-run `git config --get-all remote.origin.push` and `git remote get-url --all --push origin` plus the FETCH_URL match. Any custom refspec, unobservable URL, multiple push URLs, or fetch-push divergence means report and stop without pushing. The exact URL match lets the fetch-side tip stand for the push side, but still prove the tips agree. For an existing branch run `git ls-remote origin refs/heads/<current-branch>` and `git ls-remote "$PUSH_URL" refs/heads/<current-branch>`. Each must return one line with the same non-empty SHA, or report the divergence and stop without pushing.

Refresh the tracking tip with `git fetch --no-tags origin refs/heads/<current-branch>:refs/remotes/origin/<current-branch>`. On failure report and stop without pushing. Re-resolve both tip SHAs after the fetch and require the same identical SHA. Any difference means report and stop without pushing. List `git log --oneline origin/<current-branch>..HEAD`. When the left count is non-zero the remote holds commits HEAD lacks, so name them in the preview, because the push will be rejected until they are integrated.

For a branch new to `origin` (empty on both destinations at preview time), re-resolve `<default>` from authoritative advertisement only, exactly as above, prove base-tip equality with `git ls-remote origin refs/heads/<default>` versus `git ls-remote "$PUSH_URL" refs/heads/<default>` (one line each, identical non-empty SHA), then list the full range `git log --oneline origin/<default>..HEAD`, materializing the base first with `git fetch --no-tags origin refs/heads/<default>:refs/remotes/origin/<default>`. When advertisement, agreement, existence, tip equality, or the base fetch fails and no proven `origin/<default>` exists, report and stop without pushing. Never fall back to an unanchored or truncated listing. A failed `ls-remote` anywhere means the remote cannot be observed, so report and stop without pushing.

The push always targets `origin`, even when the configured upstream points elsewhere. Show the target, the matched fetch and push URLs, the matched tip SHA, and the commit list, then wait for the human to approve the exact mutation set (platform blocking question tool, chat fallback). Silence or refusal stops with nothing pushed. On approval for an existing branch, re-resolve both tip SHAs for `origin/<current-branch>` and require the same identical SHA. On any difference, re-preview the new set and wait again. On approval for a new branch, re-run `git ls-remote --heads origin <current-branch>` and `git ls-remote --heads "$PUSH_URL" <current-branch>`. If either is now non-empty, a concurrent creator changed the target after approval, so abandon the new-branch preview, refresh the tip, prove `<current-branch>` tip equality, list `git log --oneline origin/<current-branch>..HEAD` as the updated preview, and wait again for that set. If both are still empty, re-resolve both base tip SHAs and require the same identical SHA, re-previewing and waiting again on any difference.

Publish only the checked-out branch with an explicit source-to-destination refspec and tag following disabled: `git push --no-follow-tags -u origin HEAD:refs/heads/<current-branch>`. Inspect the accepted ref updates, not just the exit status. An unexpected tag publication is a reported partial-result incident, and deleting any remote tag needs separate authorization naming the exact ref. Never force-push.

Verify with `git status --porcelain` (must be empty) and `git rev-list --left-right --count origin/<current-branch>...HEAD` (must print `0 0`). Report any residue instead of claiming done.

## When to stop instead

- Detached HEAD or nothing to do, as above. No commit is created, and no branch is created or switched.
- Ambiguous destination (custom refspec, unobservable or multiple URLs, fetch-push divergence). Stop before any commit if found in preflight, or without pushing if found at preview time. Commits already authored stay for the user to dispose of. Never authorize an ambiguous or triangular push.
- New-branch default unresolved, disputed, or unproven on either destination. Stop before any commit, or without pushing on re-check. Never guess.
- Push-side tip missing, unobservable, disagreeing with the preview tip, or a concurrently created new-branch target after approval. Report the divergence or re-preview the changed target and wait again. Approval never covers another tip set or another target state.
- Unobservable remote during pre-commit newness observation. Allow the commit and defer to the preview, which stops before pushing.
- No fetched base for a new-branch preview. Report and stop. The set is never previewed from HEAD alone or truncated, and a failed tracking-tip refresh likewise stops the push.
- Push rejected on a diverged remote branch. Report the rejection with the `rev-list --left-right --count` counts and leave resolution to the user. Never force-push, and never silently pull or rebase to repair it.
- Verification residue. Report the uncommitted files or unpushed commits. Do not claim done.

## What you hand back

The committed tree on the checked-out branch, the one push to `origin/<current-branch>`, and a report naming the branch, the matched fetch and push URLs, the matched tip SHA, the pushed commit hashes and subjects, and the verification result. With no `origin` remote, a local-only report naming the commits left unpushed.
