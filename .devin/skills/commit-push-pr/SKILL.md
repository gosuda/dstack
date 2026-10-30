---
name: commit-push-pr
description: 'Use when asked to commit and push a feature branch, with or without a pull request or merge request. Description-only and description-update modes draft or refresh the body without committing.'
---

# Commit, push, and open the pull request

Commit the working tree and push the feature branch to `origin`. In pull-request or merge-request mode, open or update the PR (GitHub, `gh`) or MR (GitLab, `glab`); in no-PR mode stop after the push. Description-only and description-update modes compose or refresh the body without committing. Commit authoring belongs to `commit`; title and body composition (evidence section, preserved `Related:` / `Fixes` trailers, diff taken against the resolved base) is owned here. This skill adds branch placement, PR/MR-target resolution, evidence placement, the push, and the `gh` / `glab` call.

## Yours and not yours

This skill owns branch placement, the push-set statement, PR/MR-target choice, title and body composition, the push, and PR/MR create and edit plumbing. It does not invent message conventions (`commit`) and does not watch CI (`watch-and-repair-pr`).

Everything remote is human-gated: local commits, at most one local feature branch, and one push to `origin/<branch>`; pull-request or merge-request mode also creates or edits one PR through `gh` or one MR through `glab`. No remote action happens without an exact preview and approval. Rollbacks are `git reset --hard <prior-HEAD>`, `git branch -D <created-branch>`, and `gh pr close` / `glab mr close` or a body-restoring edit. Never force-push. No `STRATEGY.md`, no `Compound` config layers, no guessed default branch, no guessed forge.

No-PR mode is done when `git status --porcelain` is empty and `git rev-list --left-right --count origin/<branch>...HEAD` prints `0 0`. Pull-request or merge-request mode adds the GitHub `gh pr view --json url,title,state` returning `OPEN`, or the GitLab `glab mr view <iid|branch> -F json` returning state `opened`, with the previewed title and matching head SHA. Description-only is done when a drafted title and body are returned (applied only when asked). Description-update is done when the existing body is refreshed after approval.

## Four ways to run

The mode is `pull-request` (the default full workflow, also covering GitLab MRs), `no-pull-request`, `description-only`, or `description-update`. A stack is an opt-in modifier only when the user explicitly asks for stacked PRs or MRs. Never propose a stack for one logical change.

Other things you need: the working tree, branch, history, remotes, remote default, existing PR/MR, and `gh` / `glab` auth (gathered by you, see below). The forge (GitHub or GitLab) comes from the verified request URL or remote URL, never assumed; ambiguity stops the run, so never guess GitHub. GitHub open state is `OPEN`, GitLab is `opened`; GitLab IIDs are project-scoped, never global node IDs, and GitHub status names do not apply to GitLab. User-supplied evidence (URL, embed, path) is optional. Human decisions cover detached HEAD, unpushed default-branch commits, ambiguous target, and description rewrite approval. The PR/MR target (origin versus upstream, base, head) is required in pull-request mode.

## First, see exactly what exists

Gather context, each probe as its own call: `git status`, `git diff HEAD`, `git branch --show-current`, `git log --oneline -10`, `git remote`, `git rev-parse --abbrev-ref origin/HEAD 2>/dev/null || echo DEFAULT_BRANCH_UNRESOLVED`. On GitHub in pull-request modes also run `gh pr view --json url,title,state 2>/dev/null || echo NO_OPEN_PR` and `gh auth status >/dev/null 2>&1 || echo GH_NOT_AUTHENTICATED`; on GitLab run `glab mr view 2>/dev/null || echo NO_OPEN_MR` and `glab auth status >/dev/null 2>&1 || echo GLAB_NOT_AUTHENTICATED`. `glab` emits whole REST resources as `-F json` with no field selection, so filter with `--jq`. Self-managed hosts need explicit `--hostname` / GITLAB_HOST config with per-host auth, and older instances may lack newer commands, so verify each command against the installed `glab --help` first. When no `origin` exists, skip remote-default and PR/MR-target resolution; after any detached-HEAD decision, commit on the current branch and end with a local-only report. Otherwise strip `origin/`; on unresolved try `git ls-remote --symref origin HEAD`, then the verified forge viewer (`gh repo view --json defaultBranchRef` on GitHub, `glab repo view -F json` reading `default_branch` on GitLab). When every resolver fails, report `DEFAULT_BRANCH_UNRESOLVED` and stop; never guess. Description-only and description-update with a pasted PR/MR ref skip working-tree gating and resolve that ref directly.

Do not classify a nonzero aggregate auth status exit as no authentication without reading which account failed and which is active, on either forge. When needed, verify the intended active API identity with a read-only authenticated identity query. Public repository visibility proves neither authentication nor write permission; API authentication proves neither Git credential-helper behavior nor permission to push the intended ref.

## Find the open PR or MR, or prove there is none

On GitHub run `gh pr list --head <branch> --state open --json number,url,title,body,state,isDraft,headRefName,headRepositoryOwner` only when the branch name is non-empty; on detached HEAD skip it until a branch exists. On GitLab run `glab mr list --source-branch <branch> -F json` (default scope is open; page with `-P` / `--per-page` and `-p` / `--page` and enumerate all pages before concluding). Exit 0 with `[]` means no open PR/MR. Non-zero means unknown (missing CLI, unauthenticated, offline): never treat it as none; resolve auth or connectivity and stop until presence is known. On a GitHub fork checkout target the base with `-R <base-owner>/<repo>` and pass the branch name only; `--head <owner>:<branch>` silently returns `[]` and opens a duplicate. On a GitLab fork select the head repository with `-H <head-group>/<head-project>` (glab takes the head repo while the branch travels via `--source-branch`; `--head <owner>:<branch>` syntax does not exist). With results, match the head owner and name and head ref to the current head; on an ambiguous multi-fork match stop and show candidates.

## Decide where the PR lands

The branch always pushes to `origin`; this step decides only where the PR/MR is filed. With an `upstream` remote the target is `upstream`. On GitHub otherwise read `gh repo view <origin-slug> --json nameWithOwner,parent,defaultBranchRef`; a non-null `parent` is the target candidate. On GitLab bind source project, target project, host, and base as separate values from the verified remotes: file the MR with `-R <target-group>/<target-project>` and, on a fork checkout, the head repo with `-H <head-group>/<head-project>` (without a local clone every input must be a flag; `--push` and `--fill` need the clone). Ask only when no single target is clear (no upstream and two or more non-origin candidates, parent disagrees with upstream, or origin shares no merge-base with the target). A fork that is only behind its parent is not ambiguous. For an organization-owned origin where `gh --head` cannot file, push then report the compare URL and stop.

## Sort out the branch

Detached HEAD: ask whether to create a branch; on yes create and continue, on no stop. Default branch with no work: stop. Default branch with work: create a feature branch from a fresh default tip (`git fetch --no-tags origin refs/heads/<default>:refs/remotes/origin/<default>`, then `git checkout -b <branch> <base>`; on uncommitted-overwrite refusal stash, checkout, pop; on fetch failure stop rather than branching from HEAD). Never silently carry foreign commits: when `git log origin/<default>..HEAD` is non-empty, ask whether to carry them or base on `origin/<default>`. Feature branch: continue.

## Commit, then state the push set

Author commits with `commit`. Its atomicity, staging discipline, named-file commit, and message-file rules apply; they are not restated here. Description-only and description-update skip this step.

State the push set. New to origin (`git ls-remote --heads origin <branch>` empty): list `git log --oneline origin/<default>..HEAD`, materializing the tracking ref first when this skill created the branch. Existing: refresh the tracking tip (`git fetch --no-tags origin refs/heads/<branch>:refs/remotes/origin/<branch>`; on failure stop without pushing) and list `git log --oneline origin/<branch>..HEAD`. On no `origin`, report local-only with the commit list and stop. On failed fetch with no fetched base, stop; never preview from HEAD alone.

## Put evidence in the body

User-supplied artifact goes into the body as `## Demo`, `## Screenshots`, or `## Evidence` by kind. User asked but supplied none: ask for it or tell them to capture it; do not invent it. No observable behavior (internal plumbing, type-only, pure refactor, inert docs): skip without asking, classified by runtime purpose, not extension. Otherwise add a concise validation note of what was exercised and its result, or state plainly why no run was possible. Never label test output `Demo` or `Screenshots`. Do not block the PR/MR on a missing visual.

## Write the title and body against the right base

Compose the title and body here against the base resolved above so the diff is taken against the right base. The title names the outcome; the body carries the evidence section plus the validation note, and preserves any existing `Related:` or `Fixes` trailer on rewrite. Description-only: compose against the pasted or resolved PR/MR ref and print the draft; apply only when asked. Description-update: resolve the open PR/MR, compose against its current body, preview, confirm, then apply with `gh pr edit` or `glab mr update [<iid>|<branch>]` (`-t`, `-d` / `--description-file` from a body file; `-y` only after approval; `--draft` / `--ready` for draft transitions; labels via `-l` / `-u`).

## Preview, approval, push, create, verify it landed

Preview the exact remote mutations and wait for approval. Show push target plus commit list; in pull-request mode add forge, host, target project, base, head, title, and the first two sentences of the body. No MR command has a general dry-run mode, so this preview is the dry run. On refusal stop with nothing pushed and no PR/MR created or edited. On approval re-run the push-set listing; on any difference re-preview and wait again. Then push with `git push -u origin HEAD`, never force-push. Write the body to a temp file and pass `--body-file` (`gh`) or `--description-file` (`glab`), never inline `--body` / `-m` or stdin. New same-repo PR: `gh pr create --base <default> --title "<TITLE>" --body-file "$BODY_FILE"`. New upstream PR: add `--repo <upstream-slug> --base <default> --head <fork-owner>:<branch>`. New same-project MR: `glab mr create --source-branch <branch> --target-branch <default> --title "<TITLE>" --description-file "$BODY_FILE"` (`--draft` / `--wip` for draft; `--push` only with a local clone). New fork MR: add `-R <target-group>/<target-project> -H <head-group>/<head-project>`. Existing PR: pushed commits are already on it; ask whether to rewrite the description, then `gh pr edit --title "<TITLE>" --body-file "$BODY_FILE"` (add `--repo` for upstream). Existing MR: pushed commits are already on it; ask whether to rewrite the description, then `glab mr update [<iid>|<branch>] --title "<TITLE>" --description-file "$BODY_FILE" -y` (add `-R` for a non-local target). Escape `"`, backticks, `$`, and `\` in the title. Re-verify PR/MR presence immediately before create with the presence reads above on the active forge: a matching item takes the existing path, exit-0 `[]` creates, non-zero blocks. After create, read back the complete body and target identity (`gh pr view --json body` or `glab mr view <iid> -F json`); a matching phrase or URL alone is not verification. When empty or mismatched, re-apply from the same body file and confirm with a fresh read.

## Confirm it is really up there

No-PR needs empty porcelain and `0 0` counts. Pull-request or merge-request additionally needs the previewed title on an open item with a matching head SHA: GitHub `OPEN`, GitLab `opened` (the IID is project-scoped, not a global node ID). Report branch, hashes, subjects, PR/MR URL, created versus updated, and verification. Approvals, unresolved discussions, draft state, project merge policies, and pipeline-to-head-SHA matching are distinct gates this step does not prove; the watch path owns them. When MR pipeline state is needed, `python3 scripts/inspect_mr_checks.py --host <host> --project <GROUP/PROJECT> --mr <IID> --json` reports it keyed by head SHA.

## When it goes wrong

- `gh` / `glab` missing or not authenticated in pull-request or merge-request modes: stop before any commit; instruct install or `gh auth login` / `glab auth login --hostname <host>`.
- Clean tree with nothing to push: report nothing to do; no mutation.
- Detached HEAD declined, preview declined, ambiguous target unanswered, commit list changed since approval: stop with nothing pushed.
- Fetch, tracking-refresh, or no-base failures: stop before the push; never fall back to an unanchored listing.
- No `origin`: local-only report; never add or guess a remote.
- Diverged push rejection: report counts; never force-push.
- PR/MR create failure after push: report the exact `gh` / `glab` error; the branch stays for retry.
- Empty or mismatched body after create: re-apply from the same body file and confirm with a fresh read; never leave a silent empty body.
- Transport failure: retain the exact approved body and target. Before retrying over an equivalent path, confirm the prior write did not already land and that the response is a transport or endpoint issue, not an explicit rate-limit, abuse restriction, or permission denial; never switch transports to bypass such restrictions. Read back the complete body and target identity. On an uncertain outcome preserve the draft and report partial-result without a compensating overwrite. (`glab mr create --recover` is EXPERIMENTAL persistence for a failed create; it does not replace read-back.)

On a push failure, retain the sanitized exact remote error and distinguish authentication, authorization, protection policy, divergence, local resource denial, and unresolved transport evidence. Do not display tokens, change accounts or credential helpers, pool credentials, invent a fork, or retry mutation to test access. Report the precise missing permission or user-side authentication action supported by the observed error. A local-path remote is identified as such, not silently replaced.

## What you hand back

No-PR: pushed branch plus verification report. Pull-request or merge-request: pushed branch plus created or updated PR/MR with verification. Description-only: drafted title and body with no remote mutation unless asked. Description-update: refreshed body after approval with verification. Local-only or declined paths report commits left unpushed.
