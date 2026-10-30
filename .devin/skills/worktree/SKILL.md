---
name: worktree
description: 'Use when work needs an isolated git worktree: new work, an existing ref, a gated feature workspace, a manifest-tracked loop run, or a candidate patch captured without touching the current checkout. Not for plain branches: work in the current checkout.'
---

# Give the work its own isolated checkout

Some work cannot share the current checkout: a fresh task that needs isolation, an existing ref worth inspecting on its own, feature work that deserves a gated workspace with setup and a baseline suite, a loop run tracked in a manifest, or a candidate patch that must be captured without touching what is checked out now. Your job is to place that work where the harness can see and manage it, with nothing phantom and nothing clobbered. Single task work that belongs on a branch stays in the current checkout; no worktree is needed for it.

Everything here is reversible and local: the worktree directory, `.worktrees/` or `.loop-worktrees/` entries, the gitignore entry, symlinked hooks, manifest bookkeeping, or a fresh temporary worktree plus a binary safe patch. Rollback is removing the worktree and reverting those entries. Capture mode never writes the original checkout. Loop runs never pass `--force` to `git worktree remove`. There is no remote mutation.

This skill owns isolation placement, gitignore tracking, hook linkage, loop manifest discipline, and ephemeral capture. It does not choose branch semantics, author commits (`commit`), push or open PRs (`commit-push-pr`), or watch PRs (`watch-and-repair-pr`).

## Name the mode and its inputs first

Five modes cover the work. `new-work` (the default when no ref, gate, lifecycle, or capture is requested) starts fresh. `isolate-existing-ref` checks out a PR or MR head, branch, or commit. `feature-gate` adds setup and a baseline suite to the workspace. `loop-run` tracks worktrees in a status manifest. `capture-isolated-patch` runs one command in an ephemeral worktree and returns a patch, leaving the original checkout untouched.

Inputs per mode:

- Mode (required), one of the five above.
- Ref to isolate (`isolate-existing-ref` only): PR or MR head, branch, or commit.
- New branch name (optional): derived from the work description when omitted.
- Base branch (optional): origin default branch, else `main`.
- Setup command (`feature-gate`, optional): for example `pnpm install --frozen-lockfile`. When omitted no setup runs.
- `runId` (`loop-run`, required): single path segment, used verbatim as path segment and branch suffix.
- `pattern` (`loop-run`, required at create): short label kept on the manifest entry.
- Status for mark (`loop-run`, required): exactly `active`, `rejected`, `escalated`, `merged`, or `stale`.
- Cleanup set (`loop-run`, optional): status CSV default `rejected,escalated`, plus optional age cutoff `<n>s|m|h|d`.
- Command (`capture-isolated-patch`, required): shell command producing the candidate change; runs with the ephemeral worktree as its working directory.
- Base ref (`capture-isolated-patch`, optional): defaults to current `HEAD`.
- Repo path (`capture-isolated-patch`, optional): defaults to the current working directory.

## Capture an ephemeral patch without touching the checkout

Verify `repo-path` is a work tree and `base-ref` resolves, both scoped to `repo-path`: `git -C <repo-path> rev-parse --is-inside-work-tree` and `git -C <repo-path> rev-parse --verify <base-ref>`. Stop and name the failing check before creating anything when either fails.

Create an ephemeral worktree at a fresh temp path with `git -C <repo-path> worktree add --detach <tmp-path> <base-ref>`; record the path and report the git error when creation fails. Run `command` inside it, capturing stdout, stderr, and exit code; do not commit, push, or merge. After it returns run `git -C <tmp-path> add -N .`, compute `git -C <tmp-path> diff --binary <base-ref>`, and write that binary safe diff to a patch file under the worktree parent temp directory. A non zero command exit still extracts the patch. On success remove the worktree with `git -C <repo-path> worktree remove --force <tmp-path>` and return the patch path, exit code, and outputs; on extraction failure preserve the worktree and return its path plus the reason. The original checkout stays untouched and the run stops here.

Bad capture input, creation failure, non zero exit, or extraction failure are all handled in this section with the original checkout unchanged.

## Check for existing isolation before creating any

Compare the resolved absolute git dir against the resolved absolute common git dir: `git rev-parse --absolute-git-dir` and `(cd "$(git rev-parse --git-common-dir)" && pwd -P)`. Equal means a normal checkout, so continue to placement below. Different means possible isolation, so run `git rev-parse --show-superproject-working-tree`. A non empty result means a submodule: in feature gate mode stop and report that isolation must run from the superproject; otherwise treat it as a normal checkout and continue. An empty result means already isolated: report `git rev-parse --show-toplevel` and the current branch, work in place, and in isolate existing ref mode check the named ref out here unless already current. Never nest a worktree inside the harness managed tree, and for two checkouts of the same work never double check out one branch: when git reports the ref already checked out elsewhere, report that path and stop rather than forcing a second worktree.

## Place the worktree where the harness can see it

Prefer the harness native worktree primitive (for example `EnterWorktree`, `WorktreeCreate`, a `/worktree` command, or a `--worktree` flag) and continue to the mode steps. A behind the back `git worktree add` creates phantom state the harness cannot see or clean up.

When no native tool exists and the checks above found no existing isolation, follow `references/git-fallback.md` from the repo root: choose a meaningful branch name from the work description, never an opaque generated name; ensure `.worktrees/` is gitignored with the trailing slash probe `git check-ignore -q .worktrees/` before creating anything; best effort refresh the base with `git fetch origin <from-branch>` and continue with the local ref when no origin or a differently named remote exists; create per mode, new work with `-b`, an existing branch or tag directly, a PR via `git fetch origin pull/<n>/head:pr-<n>` then `git worktree add .worktrees/pr-<n> pr-<n>` on a local branch (never a detached `FETCH_HEAD`; for push tracking back to the PR create detached then run `gh pr checkout <n>` inside, which is fork safe); when git reports the ref is already checked out elsewhere report that path and stop rather than forcing a second worktree; then `cd` into it and report path and branch.

For an MR use `glab mr checkout <iid> [-b <branch>] [-R GROUP/PROJECT] [--worktree <path>]`, which is fork safe and resolves the source project head; a manual fallback is `git fetch <remote> merge-requests/<iid>/head:mr-<iid>` then `git worktree add .worktrees/mr-<iid> mr-<iid>` on a local branch, never a detached `FETCH_HEAD`. Derive the forge from the verified request URL or the checkout remote and never guess across forges; on forks bind source and target projects separately (including self managed hosts) and fetch from the source project remote when checking out by hand. For push tracking back to the MR, create detached then run `glab mr checkout <iid>` inside. The already checked out rule holds exactly as with a PR.

In feature gate mode, when creation fails fall back to in place work on the current branch and report the reason. On sandbox or permission failure report it and ask with the platform blocking question tool whether to work in the current checkout or stop; never proceed without explicit confirmation and never retry silently.

## Gate the feature workspace before calling it green

Once the worktree exists (or in place after fallback), first confirm ignore coverage: when the worktree directory is not already ignored, add it to `.gitignore` without committing and report the pending change. Then symlink the worktree hooks directory to the parent hooks found via `git rev-parse --git-common-dir`, reporting and continuing without hooks on failure. Run the supplied setup inside the worktree, surfacing non zero output and stopping; then run the project baseline suite inside the worktree, surfacing failures with a proceed or investigate question. A stop here means no green workspace is claimed.

For a linked worktree submodule problem, inspect the superproject gitlink and the available local module store before any network workaround. When using that store, obtain a locally available ref containing the required object and verify the checkout equals the pinned gitlink. Never stage a gitlink change unless requested.

## Track loop runs in the manifest

Under `.loop-worktrees/`: bind the root with `git rev-parse --is-inside-work-tree`; the manifest is `.loop-worktrees/manifest.json` shaped exactly `{"version":1,"worktrees":[]}` and the mutex is `.loop-worktrees/.manifest.mutex`; on any other existing shape stop without rewriting; add `.loop-worktrees/` to `.gitignore`. Serialize each read modify write with exclusive mutex create, clearing a mutex older than 30 seconds and retrying to a 30 second deadline, releasing on every path; pure reads take no mutex. Create refuses a non single segment `runId` and an already `active` id, runs `git worktree add -b loop/<runId> .loop-worktrees/<runId> <base>`, replaces any prior same id entry and appends the new record, writing tmp then rename. Mark rejects any status outside the five value set and writes tmp then rename without deleting entries. Cleanup selects only requested statuses (never `active`) older than any cutoff, runs `git worktree remove .loop-worktrees/<id>` without `--force`, records refusals as skipped, and rewrites without removed ids. Reconcile compares `git worktree list --porcelain` against the manifest, reports orphans and removes only on explicit instruction still without `--force`, and drops entries whose directories no longer exist. A manifest write failure after a successful add rolls back with `git worktree remove` then `git branch -D loop/<runId>`.

An unusual submodule checkout shape is not permission for forced worktree deletion. Loop cleanup continues to refuse force; no source lesson broadens that rule.

## Keep comparison and reuse proofs honest

When the isolated workspace will support a comparison or regression proof, record its resolved path, base revision, and actual source state. A revision name alone does not identify uncommitted test or generated input overlays; enumerate those separately under the caller existing authority. Keep independently compared checkouts build and runtime scratch separate unless the build system safe reuse is established. Record artifact directories and prerequisites for each target. Prefer new owned scratch over deleting a shared cache. When an existing checkout is synchronized, verify the intended inputs, including required generated files, and establish that its executable or imported artifact corresponds to those inputs using the build system own evidence. Never infer stale output from elapsed time alone, require recompilation when a verified content addressed artifact is valid, or restore a pinned reference from an arbitrary HEAD. Missing isolation, unresolved artifact identity, or an unavailable prerequisite blocks the affected proof. Preserve the active mode cleanup rules: never remove unrelated caches, force remove a dirty comparison worktree, or discard caller changes to obtain a clean proof; report retained paths and why they remain.

Before reuse or cleanup, bind a workspace to its exact registered path, gitdir, common object store, current full OID, branch or detached state, owner, and dirty state inventory. Matching commit subjects do not prove its work merged: inspect unique commits and content equivalence together with staged, unstaged, and untracked state. A file introduced after a stale workspace base is not evidence the stale workspace intentionally deleted it. Preserve abandoned or parked work before removal; applying a retained stash or patch without conflict does not prove semantic restoration against a newer anchor, so compare the intended content and contract, and retain the recovery object until its content is verified.

## When to stop instead

Stop or refuse with the exact cause and the inspected paths: failing capture input or creation; already isolated (report the existing path and proceed in place or check the named ref out there); ref already checked out elsewhere; worktree already exists or cannot be removed while current (switch to it, remove it, or `cd` out first, then remove); sandbox or permission failure without confirmation; submodule in feature gate; setup or baseline failure; loop manifest, mutex, id, branch, or status violations; non converged isolation with no confirmed fallback (return blocked with the exact error and inspected paths).

## What you hand back

Capture mode: patch path, exit code, and outputs, or the preserved worktree on extraction failure, with the original checkout unchanged. Other modes: absolute path, branch, mode, and creation method (native tool or git fallback); feature gate adds setup and baseline status; loop run adds manifest rows and cleanup or reconcile lines. Each mode counts as done only when its own predicate holds.
