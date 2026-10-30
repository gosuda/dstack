---
name: make-pr-easy-to-review
description: 'Use when a human explicitly asks to reshape or annotate one pull request for review. Don''t use for pushing the rewritten branch or mutating any remote.'
disable-model-invocation: true
---

# Make a pull request easy to review

A human hands you one pull request and asks for a review surface a stranger could walk through: what it is for, where the risk sits, and a commit story that reads in order. You work on the named local branch only. You never push, publish, touch credentials, or change any remote.

Rewriting history is optional and always gated. If a clear annotation already tells the story, stop there and change nothing.

## What you start from

You need the pull request or local branch, its base ref, and the review outcome the human asked for. Both refs must resolve locally, and the working tree must hold no uncommitted changes that could mix into the pull request. History work additionally needs explicit consent to an exact preview. Annotation alone never needs that consent.

## Map the change before touching it

Resolve the named branch and base ref first, then record the branch tip, the merge base, the commit range, the changed paths, and the final tree identifier. If any of those stay ambiguous, or the base is missing, or stray working tree changes are present, stop with `blocked` and name the unresolved input. No mutation happens on an unclear target.

Read the full diff and the full commit sequence. Assess each risk area and tie what you find to paths and evidence, without inventing either:

| Risk area | What to look for |
|---|---|
| Behavior | What the change does differently |
| Data and migration | Stored data, schema, or migration effects |
| Trust boundary | Security or permission crossings |
| Concurrency and lifecycle | Ordering, races, startup and shutdown effects |
| Compatibility | Breaks for callers, formats, or supported versions |
| Tests and evidence | Which tests or measurements cover each risk above |

Claims with no supporting evidence stay marked unverified. A passing command alone never proves a review is complete.

## Write the review surface

Draft the purpose of the pull request, put the riskiest areas first, map each risk to its paths and the evidence you actually have, and call out unresolved or unverified claims by name. This draft is the product whether or not history gets rewritten. Keep commit messages and section names short and concrete so the ordering survives on its own.

## Reshape history only with consent

When annotation alone already gives an accurate surface, return the proposed title, description, review order, and risk notes, and change nothing. That outcome reports as `annotated`.

When reshaping would materially help, design a sequence where each commit has one coherent purpose, dependency order is preserved, and each change carries the tests or evidence that belong to it. Then preview the exact source commit range, the proposed sequence, the local branch to rewrite, the recovery ref you will create, and the fact that commit identifiers will change.

Without explicit human consent to that exact preview, make no history change. Return the annotation result plus the declined rewrite preview and classify the rewrite as `not-authorized`.

With consent, create a recovery ref at the original tip and perform only the approved rewrite. Never widen the changed path set or alter the intended final content while splitting, reordering, or combining commits. If the rewrite stops partway, restore the original tip from the recovery ref and report `blocked` with the failed operation and the recovery state. A partial sequence is never presented as complete.

## Prove the tree survived

Recompute the rewritten final tree identifier and compare it byte for byte with the one recorded before the rewrite. Inspect the rewritten range to confirm its order and messages match the approved sequence.

| Outcome | Response |
|---|---|
| Identifiers match | Keep the recovery ref, report the old and new tip identifiers with the identical tree identifier, return the risk oriented review surface, and report `ready-local`. Do not push the branch. |
| Identifiers differ | Restore the original tip from the recovery ref and report `tree-mismatch` with both identifiers. |

Dirty worktree input also stops with `blocked` and the affected paths, before any mutation.

## What to hand back

Return the proposed pull request title and description, an ordered reviewer path, and a table mapping each risk to its paths and evidence. For an approved successful rewrite add the original and rewritten tip identifiers, the recovery ref, the identical pre and post rewrite tree identifier, and `ready-local`. For annotation work return `annotated`. For failure return exactly the applicable `blocked`, `not-authorized`, or `tree-mismatch` result with recovery status.

## Provider note

This skill makes no forge call. It reads only the local branch and base refs, so it stays provider neutral by construction and needs no merge request counterpart operation. Its title and description feed creation or update steps owned elsewhere. On GitHub that is `gh pr create` or `gh pr edit`. On GitLab that is `glab mr create --source-branch <branch> --target-branch <base> --title <title> --description-file <file>` or `glab mr update --description-file <file>` with a body file plus `-y`, only after the exact write preview is approved (`glab mr create` has no general dry run flag). Bind the GitLab host, project, and IID from the verified remote or request URL. On a fork the head and target projects differ. Any ambiguity stops before any forge command.
