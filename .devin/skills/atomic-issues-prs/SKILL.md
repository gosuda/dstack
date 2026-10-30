---
name: atomic-issues-prs
description: 'Use when the user says "atomic PRs" or requests one issue or PR per logical change. Don''t use for single-change pushes or uncommitted change-sets.'
disable-model-invocation: true
---

# Atomic issues and PRs

One logical change gets one issue or pull request (or merge request on GitLab): its own branch, its own base and head, its own link, its own URL. Your job is to carve a working tree into those units, publish each against the right target, and report per unit routings, branches, numbers, and URLs. A run counts only when every logical change sits on the correct base and head with links appended and URLs reported.

This skill never fires on its own. It runs only on explicit human invocation, previews the target repo and project and their consequences before creating anything, and mutates only through branches, commits, issues, and PRs or MRs on the selected forge. It never force pushes and never pushes to protected branches without explicit user authorization.

## What to have in hand

A working tree holding the change set to publish, and an authenticated forge account (`gh` authenticated for GitHub, `glab` authenticated for the GitLab host). Select the forge from the verified request URL or repository remote, never from a hardcoded public host. When the URL or remote does not clearly identify one forge, stop and ask. Never guess GitHub.

Validate the repository selector before any repo scoped call and pass the validated value to every call. GitHub `OWNER/REPO` must match `^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$`. GitLab `GROUP/PROJECT` must be a non-empty slash-separated path with no whitespace or control characters.

A per unit routing override (issue plus PR or MR versus PR or MR only) and a dependency order among units are optional, and only the user can state them.

## Prove who and where before touching anything

Authenticate first. GitHub: run `gh auth status`; if unauthenticated, stop and ask the user to run `gh auth login`. GitLab: run `glab auth status --hostname <host>` with `<host>` taken from the verified remote (self-managed hosts included, never assumed `gitlab.com`); if unauthenticated, stop and ask the user to run `glab auth login --hostname <host>` with a token carrying `api` and `write_repository` scopes. Never set `GITLAB_TOKEN=$CI_JOB_TOKEN`: it is sent as `PRIVATE-TOKEN` and fails.

Resolve the canonical (upstream) target before any permission check. Read remotes with `git remote -v` and pick the contribution target as `upstream` when present, else `origin`. GitHub: detect a fork relationship with `gh repo view <slug> --json nameWithOwner,parent,defaultBranchRef`; a non-null `parent` means the canonical slug is `parent.nameWithOwner`. GitLab: detect a fork with `glab repo view <project> -F json` and read its fork-source relationship; a non-null fork source means the canonical project is the source path. A plain fork that is merely behind upstream (shared merge base) is not ambiguity and must never prompt. Genuine ambiguity (no `upstream` remote with two or more plausible non-`origin` candidates, a fork source that disagrees with the `upstream` remote, or an `origin` that genuinely diverged from upstream with no common merge base or after re-creation, rename, or renewal) stops the run: prompt the user for the target repo or project and make no mutation.

Query permission on the canonical target. GitHub: `gh repo view <canonical-slug> --json viewerPermission`; `viewerPermission` of ADMIN, MAINTAIN, or WRITE means direct mode, anything else means fork mode. Record the canonical default base branch from `defaultBranchRef`. GitLab: read the access level from the same `glab repo view -F json` resource; Developer or higher on the canonical project means direct mode, anything else means fork mode. Record the canonical default base branch from its `default_branch` field.

## Carve the work into publishable units

Group working tree changes into atomic units by mechanism and file boundary: one concern per unit, never bundled. Commit the whole set into N atomic commits first, running the repo-native type checker and linter before each commit, so each unit becomes one self-contained commit that later branches can cherry-pick. Never re-stage a dirty tree, which would let later units swallow earlier diffs. Present the unit to commit list to the user, then proceed.

Route each unit by whether it changes observable behavior. Behavior affecting units get an issue plus a linked PR or MR, because a tracking issue gives the change a changelog and discussion anchor. Mechanical units get a PR or MR only, because a self-explanatory change needs no separate tracking. Honor an explicit per unit override when the user states one; otherwise route silently.

Record each unit's exact source snapshot, original parent boundary, intended delta, dependency, and resulting commit. For committed mixed input, reconstruct from committed blobs. For authorized working tree input, preserve the full snapshot before extracting units. Do not confuse those two input modes. For dependent dirty workspaces, preserve the base and feature snapshots first, construct the base unit, then transport only the feature delta measured from its recorded pre-integration boundary onto the resulting parent. A successful three-way application is not the postcondition: compare the reconstructed content, verify every intended repair remains, prove each unit on its own committed tree and on the actual published parent. Union green never establishes slice green.

Resolve the push URL once, by URL and not by remote name, to avoid undefined targets and remote name collisions. GitHub direct mode: push URL is `https://github.com/<canonical-slug>`. GitHub fork mode: fork owner is `gh api user --jq .login` and fork slug is `<login>/<repo>`. When `origin` already points to a prior personal fork whose owner is neither the canonical owner nor the authenticated login, print a non-blocking warning noting the account mismatch; do not stop the run. When the fork does not exist, create it with `gh repo fork <canonical-slug> --clone=false` and note the fork slug in the output. GitHub push URL is `https://github.com/<fork-slug>`. GitLab: build the push URL from the verified host, never hardcoded `gitlab.com` (direct mode `https://<host>/<canonical-project>`; fork mode `https://<host>/<fork-path>` after `glab repo fork <canonical-project> --clone=false` when the fork does not exist).

## Publish each unit in dependency order

For each unit:

1. Create the branch and cherry-pick the unit commit. Independent unit: `git branch <branch> <canonical-default-base>` then `git cherry-pick <unit-commit>`; the PR or MR bases on `<default>`. Dependent unit in direct mode: the parent ref is the prerequisite unit's already pushed branch, the PR or MR bases on that branch (a stacked PR or MR), and only this unit's commit is cherry-picked so no prerequisite is lost. Dependent unit in fork mode: cross-fork stacking cannot be expressed (a GitHub fork PR base must be a branch in the canonical repo; a GitLab MR targets one branch in one target project), so flatten onto `<canonical-default-base>` and prefix the body with a warning line naming the prerequisite unit and noting the dependency was flattened. The compromise is never silent.
2. Push with `git push <push-url> <branch>:refs/heads/<branch>` (same form on both forges and modes; only the URL differs).
3. Open the PR or MR. GitHub: `gh pr create --repo <canonical-slug> --body-file <tmp>`. Direct mode adds `--base <parent-ref> --head <branch>`; fork mode adds `--base <default> --head <fork-owner>:<branch>`; capture PR `#M`. GitLab: `glab mr create --repo <canonical-project> --title "<summary>" --description-file <tmp> --source-branch <branch> --target-branch <parent-or-default> -y`, adding `--head <fork-path>` in fork mode; capture MR `!M` (project-scoped IID; address every MR by IID, never by global id). Note `--head` selects the head repository while the branch travels in `--source-branch`, unlike `gh --head <user>:<branch>`. `glab mr create` has no general dry run: run the exact previewed command only after the user approves the title, branches, and project.
4. For units routed to issue plus linked PR or MR: GitHub `gh issue create --repo <canonical-slug> --title "<summary>" --body-file <tmp>` with a body that references PR `#M`; capture `#N`. GitLab: `glab issue create --repo <canonical-project> --title "<summary>" --description-file <tmp> -y` after approval, with a description that references MR `!M`; capture `#N` (project-scoped IID). Creation and update use body files and non-interactive flags (`-y` or `--yes`) only after exact user approval.
5. Amend the body by appending `Closes #N` to the existing body, which closes the linked issue on merge on both forges. Reuse the body file from step 3 (append the line and rewrite the file) or fetch the current body first: GitHub `gh pr view <M> --json body` then `gh pr edit <M> --repo <canonical-slug> --body-file <amended-tmp>`; GitLab: read the description from `glab mr view <iid> -F json` (whole-resource output; select the description locally) then `glab mr update <iid> --repo <canonical-project> --description-file <amended-tmp> -y` after approval. Body file writes replace the whole body, so never write a bare `Closes #N` as the entirety of it.
6. Emit the issue and PR or MR URLs, then move to the next unit.

For PR or MR only routed units (no issue filed in step 4), skip the issue create and body amend steps entirely. No dangling `Closes`.

In direct stacking, publish a dependent unit against its already published prerequisite. In fork mode flattening, include the prerequisite content required for the unit to work and disclose the flattened dependency in the PR or MR body. Verify the remote base and head and the complete compare range after creation. Existing human invocation, target preview, protected-branch, and no-force rules remain unchanged throughout.

## When publication fails

| Signal | Response |
|---|---|
| Unauthenticated | Stop before any mutation; ask the user to run `gh auth login` (GitHub) or `glab auth login --hostname <host>` (GitLab). No partial result. |
| Ambiguous upstream | Stop and ask the user for the target repo or project; do not guess. No mutation performed. |
| Ambiguous forge | The URL or remote does not clearly identify GitHub or GitLab; stop and ask. Never guess GitHub. No mutation performed. |
| Insufficient permission with no fork path | Stop; report the canonical slug or project and the missing permission. No push or object created. |
| Push rejected | Report the rejection and the branch and URL; do not force push. Leave prior successfully published units in place. |
| Partial publish failure mid-loop | Already published units remain; report each unit's status (published URL or failure) so the user can retry the failed units. Never swallow the error or pretend the run is done. |
| Non-converged | When any unit could not be published, the terminal result names the failed units and the reason; the run is not done. |

The run report lists, per unit, the routing (issue plus PR or MR versus PR or MR only), the branch, the push URL, the PR or MR number (IID on GitLab) and URL, and (when filed) the issue number and URL.
