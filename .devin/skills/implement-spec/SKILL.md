---
name: implement-spec
description: 'Use when a ticket DAG from a complete specification needs parallel execution into a verified integration branch, with an optional green draft pull request or merge request on explicit approval. Not for a settled ticket with no spec and not for ticket decomposition.'
disable-model-invocation: true
---

# Implement spec

You take a complete specification with a finite ticket DAG and execute it into a verified integration branch using parallel workers in isolated worktrees. The default terminal state is local-only: a verified branch with passing checks and a clear review. Publication as a green draft pull request or merge request happens only when the human explicitly asks for it with an exact destination, previews the consequences, and approves.

This skill runs only on explicit human invocation. Credentials, remote publication, and cleanup deletions each need their own explicit approval bound to the exact target and consequence; every other write is reversible local work with version control as the rollback.

## What you need before starting

The complete specification; a finite ticket DAG with stable identifiers, dependencies, acceptance criteria, and owned file scopes; named TDD seams per ticket; the repository and integration base; the required check commands; and the review-clear criterion.

Publication inputs apply only when the human requests publication: the remote repository, target branch, and draft pull-request destination, or for GitLab the target project (`GROUP/PROJECT`), source and target branches, host, and draft merge-request destination, plus publication and cleanup approval when prompted. Pick GitHub or GitLab from the verified request URL or repository remote; an ambiguous destination blocks publication, never the local implementation path. Credentials are used only after that approval. The local path is complete on its own and needs no tracker, no remote, no credentials, and no cloud service.

Optional extras: ticket-specific verification commands, a pull-request or merge-request title or body, and an outside-repo path for exploration notes (default `<repo-parent>/spec-notes-<slug>/`).

## Validate first, without touching anything

Confirm every ticket traces to the specification, carries measurable acceptance criteria and a unique owned file scope, names its TDD seams, and references only existing ticket identifiers. Reject cycles, missing dependencies, overlapping ownership, and an unclean or wrong repository, all without mutation. Validate the publication destination only when publication is requested. If validation fails, make no mutation and stop as `invalid-input`.

Then record the bounded execution set, the integration base, the initial ready frontier (tickets whose dependencies are all complete), the required checks, the review-clear criterion, the publication scope (local-only by default), and the cleanup targets. Add no work outside this set and invent no missing evidence.

## Set up the branch and brief the workers

Create the integration branch from the base. Give every worker only what its ticket needs: the ticket itself, the exact specification sections and repository paths, its acceptance criteria, dependencies, owned files, named seams, and verification command. Pass results by artifact paths or commit identifiers plus context pointers to the spec, tickets, research notes, and prior commits; never duplicate unrelated context into worker packets.

When tickets need codebase or external research, run one exploration subagent first. It saves markdown notes in the outside-repo notes path, never inside the repository, so implementers share findings without polluting the tree.

## Execute the frontier in parallel

Each implementer works in its own worktree on its own branch: confirm the worktree is based on the integration branch tip and reset onto it when drifted, write the failing behavioral test first at each named seam, implement only its owned files, run its ticket verification, merge the integration branch tip into its own branch before reporting, and return the commit identifier, changed paths, verification result, and any blocker. A ticket without a passing acceptance proof stays incomplete.

Merge completed ticket commits onto the integration branch in dependency order with a merger pass. Resolve a conflict only when the specification and ownership make the intended result unambiguous; otherwise stop the affected path as blocked and preserve both commits plus the integration branch at the last verified state. After each integration, mark the ticket complete and release newly ready tickets. Keep going until every ticket is integrated or no incomplete ticket is ready; when the frontier is empty while tickets remain, return `blocked` with the unmet dependency or failed-ticket evidence. Never bypass the DAG, and preserve failed ticket worktrees with their commit evidence while blocking dependents.

## Check, review, and correct to green

Run all required checks on the integrated branch: the TDD cadence evidence (failing-first seam tests), the required check commands, and a full review of the integrated change against the specification, acceptance criteria, ownership boundaries, and repository safety. When the destination is a GitLab MR, the pipeline used as proof must match the MR head SHA; a missing, skipped, or unrelated successful pipeline is not proof, and a head change invalidates prior check evidence.

Turn each actionable finding into a bounded correction on the owning ticket branch, verify it, reintegrate it, and repeat checks and review until clear. Continue while each correction shows verified progress against a distinct finding. Stop as `non-converged` when a finding repeats without progress, results oscillate, checks are unavailable, or correction would widen the bounded scope. Never apply a fixed cycle count as the stopping rule, and never widen scope to unrelated code.

## Publish only with approval, then clean up only with approval

Local-only is the default: stop with the verified integration branch, report its name, head commit, checks, and review-clear evidence, and never touch a remote. Invocation is never publication approval.

For GitHub publication (only when the human explicitly requests it with an exact destination): preview the integration branch, commits, remote, target branch, draft pull-request title and body, and publication consequences; after explicit human approval, publish with the approved credentials, then verify the remote pull request points to the reviewed commit and reports the required checks. For GitLab MR publication (only when the human explicitly requests an MR with an exact destination): preview the source project and branch, target project and branch, host, title, body file, draft state, and publication consequences; no MR creation command has a general dry-run, so the preview is computed locally and nothing is submitted before approval. After approval, create with body-file and non-interactive flags (`glab mr create --repo <target GROUP/PROJECT> --head <source GROUP/PROJECT> --source-branch <branch> --target-branch <branch> --title <title> --description-file <body-file> --draft -y`), then verify by read-back that the MR IID exists with `state` opened, `draft` true, and `sha` equal to the reviewed integration head commit, plus `detailed_merge_status`, `blocking_discussions_resolved`, approval state, and a head pipeline matching the MR SHA with required checks green (GitLab check evidence via the bundled helper `python3 "<path-to-skill>/scripts/inspect_mr_checks.py" --host <host> --project <GROUP/PROJECT> --mr <iid> --json`). Fork MRs bind source and target projects separately. A failed publication stops as `publication-failed` with the local branch preserved; a declined one stops as `publication-declined` with the local-complete result standing.

Preview the exact temporary worktrees and branches eligible for cleanup. After explicit human approval, remove only those whose commits are reachable from the verified integration branch. Preserve any target holding unintegrated or uncommitted work and report it; if anything is uncertain, stop as `cleanup-blocked` with every uncertain target preserved.

## One approved feature instead of a DAG

When the specification is a single approved feature described by a product spec and a tech spec (for example `PRODUCT.md` and `TECH.md`), the DAG holds exactly one ticket. Run the same flow with that single ticket: validate it traces to both specs, execute it in one worktree, and integrate. Two extra rules apply only here: when implementation reveals that intended behavior or design should change, update the checked-in spec in the same change (product spec for user-facing behavior and success criteria, tech spec for architecture and validation strategy), keeping staged spec updates, code, and tests together so specs and code never diverge. When either spec file is absent, stop and report the missing file before writing code. The draft pull request or merge request still follows the publication rule above: local integration is the default terminal state.

## Closing the run: work, review loop, simplify

Complete this skill's own implementation path before any closing pass. Then run its native review and fix gate (required checks plus review-clear on the integrated branch) to green, continuing while each correction shows verified progress against a distinct finding and stopping as blocked or `non-converged` on repeats, oscillation, unavailable checks, or scope widening. Finally simplify offensively: re-derive the general case from contracts, delete old structure with no shims, aliases, or flags, collapse special cases, migrate every caller in the same change, one concern per atomic commit. Stay inside this skill's authority (the bounded execution set and each ticket's owned file scope), ask first before removing any live consumer surface, run the native gate after each increment and revert the increment on red, and close with a compression pass over dead branches, duplicated logic, and one-use wrappers with behavior preserved and the gate green.

## What you return

On success: the ticket-to-commit ledger, the empty frontier, the integrated branch name and commit identifier, passing check evidence, review-clear evidence, the cleanup result, and either the draft pull-request or merge-request URL and head commit (publication approved and verified) or the local-complete statement (no remote touched). On failure, exactly one terminal classification (`invalid-input`, `blocked`, `ticket-failed`, `integration-conflict`, `check-failed`, `review-blocked`, `non-converged`, `publication-declined`, `publication-failed`, or `cleanup-blocked`) with the partial-result ledger (completed tickets, remaining frontier, commits, checks, findings, publication scope and remote state, retained worktrees) and the next human-resolvable blocker. Never discard unintegrated work, swallow an error, or claim done while findings or tickets remain open.
