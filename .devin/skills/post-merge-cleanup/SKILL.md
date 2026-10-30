---
name: post-merge-cleanup
description: 'Use when a landed merge, release, or completed change needs its cleanup surface reconciled. Scans for stale TODOs, deprecations, unused flags, and doc gaps. Not for unrelated refactoring.'
disable-model-invocation: true
---

# Reconcile cleanup after a merge

A merge, release, or completed change just landed and its loose ends need settling: stale task comments, satisfied deprecations, dead flags, and docs that no longer match. You make small verified fixes or file owned tickets for the rest. Unrelated refactoring stays out.

Remote tickets and remote pull requests stay gated. State the rollback path before any mutation, and preview exact fields plus consequences and get approval before any remote create.

## What you start from

| Item | Detail |
|---|---|
| Merge reference | Required. Merge commit SHA, merged PR number, merged MR IID with host and project path, or release tag that just landed. |
| Working branch | Optional. Named branch for proposed fixes, defaults to `cleanup/<merge-sha>` with a short concrete suffix when needed. |
| Size budget | Optional. One unified budget for every candidate, defaults to 5 files and 100 lines total. |
| State file | Optional. A `post-merge-state.md` tracking completed, pending, and deferred items. Created on first run when absent, updated on later runs. Keep entries to the facts needed to resume (reference, path, class, outcome), never activity notes. |
| Forge binding | Required before any remote read or write. Derive the forge from the verified request URL or the checkout remote, never assume GitHub. On GitLab bind host, project path, and MR IID separately, keep source and target projects distinct on forks, and page every list to exhaustion. No merge request command carries a general dry run, so every mutation waits on an exact preview plus explicit approval. |

## Collect candidates from the landed diff

Resolve the merge reference and confirm it sits on the tracked branch (main, trunk, or equivalent). A reference that does not resolve or is not on that branch is rejected with `blocked: unresolved-merge-ref`, and the run stops before any write.

Fetch the landed diff and gather every surface it settles: stale `TODO` and `FIXME` and `XXX` comments with or without linked tickets, deprecation notices the diff satisfies, `remove after <date>` or `TODO: remove after <event>` comments the merge fulfills, unused feature flags the diff defines but nothing downstream references, doc gaps where comments, `README` entries, or API examples disagree with the landed diff, and changelog entries now stale or redundant.

On GitLab resolve a merged request with `glab mr view <iid> -F json` (state `merged`, head in `sha`, merged result in `merge_commit_sha` or `squash_commit_sha`), or locate it with `glab mr list -M` filtered by branch or title with `-p` and `--page` looped to exhaustion. Confirm the request target branch is the tracked branch and the merge commit is reachable from it, then read the landed diff with `glab mr diff <iid>` or the merge commit range.

## Filter noise and sort by the budget

Drop commits authored by `dependabot`, `renovate`, or any automated dependency bot (on GitLab apply the same filter from `author.username` in the request JSON, plus bot accounts per the user allowlist). Drop items in denylisted paths (`auth`, `payments`, and any path touching a public API contract). Flag items referenced in a sibling or child repository for escalation instead of acting. Drop candidates with fewer than 3 lines of diff context unless they carry a linked ticket.

Sort each survivor into within budget (at most 5 files, at most 100 lines total, no behavior change except explicit dead code removal) or out of budget. The single unified budget governs every candidate, and behavior changes beyond dead code removal never count as safe.

## Fix the small items in a worktree

For each within budget candidate, create a named worktree from the tracked branch, apply the minimal fix with no added explanation comments and no widened scope, and run the project existing test suite. Only real suite results count. Snapshot or fixture oracle passes alone never prove a fix, and a passing command never stands in for the suite. On any test failure revert the worktree change at once, reclassify the item as deferred, and record the revert SHA. Never open a single cleanup pull request touching more than 10 files without human approval. An item that fails the same way twice stops being attempted and goes to the human with both attempt SHAs.

On GitLab stage the same verified fixes on a cleanup branch and open one request with `glab mr create --source-branch <cleanup branch> --target-branch <tracked branch> --title "<title>" --description-file <file> -y` (adding `--remove-source-branch` or `--squash-before-merge` only to match project policy), after exact approval of title, body, branches, and consequence. The 10 file single request limit and the human gate above it apply unchanged.

A smuggled behavior change reverts everything, opens no request, and is reclassified as deferred with the revert SHA recorded.

## File owned tickets for the rest

For each out of budget item, large change, or flagged escalation, preview the exact ticket fields (merge SHA, affected path, candidate class, owner) and get explicit human approval before any remote create, then create the ticket with those approved fields. When no owner is evident, propose the merge author or the team owning the affected path in the preview and mark ownership as `auto-assigned` so the assignment stays explicit rather than unset. Every ticket carries an owner, assigned or explicitly tracked, and no ticket is filed without its exact preview approval.

File the same approved fields as a tracker issue on the selected forge only after that approval. On GitLab that is a project issue under the bound host and project carrying merge SHA, path, class, and owner.

## Close the loop in the state file

Record each item as `completed`, `deferred`, or `ticket-created` in the state file and prune entries older than 14 days. Write `post-merge-cleanup-report.md` with the merge reference, candidates found, candidates acted on with worktree or request link, candidates deferred with reason, and tickets created with owner. When no cleanup surface exists, return a single confirmation line instead. A corrupt state file forces a read only pass with `blocked: corrupt-state-file` and no writes.
