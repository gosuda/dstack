---
name: commit
description: 'Use when asked to commit working-tree changes as typed atomic local commits. Not for push, PR, or remote publication: use commit-push-pr.'
---

# Git commit

Shape messages to repository conventions. Two jobs share this skill. `create` stages working-tree changes and commits them as typed atomic local commits. `rewrite` rewords the messages of `HEAD` or a short unpushed range while the tree stays byte-identical.

## Yours and not yours

This skill owns local commits, local branch placement, and message shape. It does not push, open or edit a PR or MR, compose a PR or MR body, watch CI, or resolve review threads. Push and PR or MR publication belong to `commit-push-pr` (which also owns title and body composition, including the `## Demo` / `## Screenshots` / `## Evidence` section and preserved `Related:` / `Fixes` trailers). Watching belongs to `watch-and-repair-pr`.

Everything here is reversible and local. `create` writes only the local index, one local feature branch, and local commits. `rewrite` writes only local commit messages. Rollbacks are `git reset --hard <prior-HEAD>`, `git branch -D <created-branch>`, and the reflog with original refs. No remote mutation happens in this skill.

`create` is done when each logical concern is committed with an explicit named file list and a value-communicating message, `git status` confirms success, and hashes and subjects are reported. `rewrite` is done when `git diff <old>..<new>` is empty, dates are preserved by position, and `git log` alone carries the handoff.

## Read the tree first

`create` needs the working-tree state (`git status`, `git diff HEAD`), the current branch (`git branch --show-current`), and recent history (`git log --oneline -10`). Gather each probe as its own call. Treat the result as a snapshot and re-read the staged set immediately before committing.

You also need the remote default (`git rev-parse --abbrev-ref origin/HEAD`), used only to know which branch is the default. Strip `origin/` from it. On an unresolved default or bare `HEAD`, try the forge viewer matching the verified remote (GitHub `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`, GitLab `glab repo view -F json` reading its `default_branch` field). Select the forge from the verified remote URL and never assume GitHub. When every resolver fails, report `DEFAULT_BRANCH_UNRESOLVED` and stop any step that needs the default. Never guess.

Other inputs arrive with the request. Repo commit conventions are used directly when already in context. An issue number, when one exists, is prefixed into the branch name and footer. A target platform (GitHub or GitLab) is required only when closing issues cross-repo; no forge command runs for that input, and the platform only shapes the cross-repo closing footer written into the commit message. `rewrite` needs the target (`HEAD` or `HEAD~N..HEAD`) with the intended text, plus explicit confirmation when any target is already pushed.

## Match the room's message style

Pick the convention in this order: repo conventions already in context first, then a clear pattern in recent commits, then the seven-rule fallback with conventional-commit types (`feat`, `fix`, `docs`, `test`, `build`, `ci`, `chore`, `style`, `ref` / `refactor`, `perf`, `meta`, `license`, `revert`). With conventional commits, default to `fix:` over `feat:` when ambiguous; a user override wins. The subject is imperative and names the outcome, not the file list.

## Rewording messages

`rewrite` runs only when the user asks to reword existing messages. Otherwise you are in `create` mode.

1. List the exact targets with `git log --format='%H %an <%ae> %ad %cn <%ce> %cd' <range>`. Record each target tree SHA (`git rev-parse <sha>^{tree}`) and author and committer dates by position.
2. Check `git branch -r --contains <sha>`. When any target is pushed, stop and require explicit confirmation.
3. Reword with `git rebase` plus `GIT_SEQUENCE_EDITOR` and `git commit --amend`, scoped to the range. Never create a new change.
4. Re-sign with the recorded `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` by position.
5. Verify `git diff <old>..<new>` is empty, dates match by position, and the log carries the handoff with the diff hidden. On drift, abort and restore original refs from the reflog.

## Making the commits

When `git status` shows no staged, modified, or untracked files, report nothing to commit and stop. Do not use `git diff HEAD` alone; it misses untracked files.

On detached HEAD, ask whether to create a feature branch (use the platform blocking question tool). On yes, derive a typed name as below, run `git checkout -b <branch-name>`, and re-read the branch. On no, continue detached with the commit.

Name the branch `<type>/[issue-]<description>`: lowercase, hyphens, under 50 chars, with the type matched to the work.

Split into one concern per commit, by mechanism and never by file alone. When one file carries two mechanisms, write the filtered patch from `git diff -- <file>`, keep one mechanism, and stage with `git apply --cached <patch>`. A lint, format, or whitespace sweep is its own commit. Order commits so each leaves the tree building.

Partition by contract dependency, not file count or line distance. Tables joined by a boot-time registry guard, signature changes with their callers, and mutually dependent repair hunks belong together when either half alone breaks the tree. Each published slice must be coherent without its successor. A green dirty union does not prove the staged tree or individual commits.

Generate real unified or binary-safe patches with the external diff disabled on the diff subcommand. Use a smaller context or explicit content reconstruction only when needed to isolate a concern. Re-read the candidate hunks after each commit or base change; regenerate rather than blindly rewriting stale offsets. Inspect the staged content, not merely its stat or rendered display. Preserve the intended final tree across a split with exact object and tree comparison.

Keep a standalone formatting sweep separate, but attribute repair-required formatter changes to the owning concern when constructing an explicitly authorized unpublished series. Do not put all formatting in the last commit by default. Folding, recutting committed blobs, or rewriting a published series needs authority covering that history operation; create mode and message-only rewrite mode do not silently grant it.

On a default branch with work, automatically create a feature branch first. Before creating it, verify the base resolves, the name is unused (`git branch --list <branch-name>` must be empty), and the working tree is clean or its dirty files are surfaced for user decision; a blocked check changes nothing. Then run `git checkout -b <branch-name>` and confirm with `git branch --show-current`. Do not ask; committing on the default branch is not an option. A default branch with no work means nothing to do: report that and stop.

Gate each group before staging it: run the repo-native typechecker or linter for that group. A failing group is not ready; skip it and name the failure. Skip silently when neither is configured.

Stage and commit each group with named files only. Never `git add -A` or `git add .`. Honor `exclude:<paths>`: those files stay uncommitted and are named in the report. Write the full message (subject, blank line, optional body) to a file outside the repo with the file-write tool, then run two calls per group:

```bash
git add file1 file2 file3
```

```bash
git commit -F <message-file> -- file1 file2 file3
```

The `-F` file avoids shell quoting for `$`, quotes, backticks, and multiline bodies. The trailing path list is required: a bare `git commit` would sweep anything already staged. Never include customer names, emails, secrets, PII, a Claude signature, AI attribution, or a `Co-authored-by` trailer for an AI agent. When the commit carries someone else's ported work, end with one `Co-authored-by: Name <email>` trailer per credited person, copied exactly from their commits or patch trailers; when no email is recorded, name them in the body instead of guessing.

Before changing a shared index, establish exclusive ownership and record existing staged paths, modes, and blob identities. Leave foreign staged entries unchanged; an ordinary commit without pathspec includes the whole index, so do not commit while unapproved staged entries remain in that index. Use an isolated construction index or workspace when necessary, without racing the real index.

Run `git status` after the commit and report hash and subject.

## When it goes wrong

- Clean tree: report nothing to commit. No mutation.
- Declined branch on detached HEAD: stop. No commit.
- Gate failure: that group stays unstaged. Committed groups remain; report the failing gate.
- Sensitive or unrelated file in scope: exclude by naming files. Never broaden to `add -A`.
- Breaking change stated only in body: add `!` or a `BREAKING CHANGE:` footer.
- Pushed target in rewrite without confirmation: stop. Do not rewrite.
- Tree drift or date slip in rewrite: abort, restore original refs from the reflog, and report.
- Partial result: committed groups are real. Name uncommitted groups and the reason.

Preserve recoverable original content before reconstruction, including tracked, staged, unstaged, and relevant untracked files. Never use add-all as a final sweep over shared work. A failed split remains uncommitted; that is not permission for blanket restore, reset, or force publication.

## What you hand back

For `create`: local commits on a typed branch plus a report of hashes, subjects, excluded paths, and confirming `git status`. For `rewrite`: rewritten messages over the exact range with empty tree diff, dates preserved by position, and verification results.
