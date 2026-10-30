---
name: verification-before-completion
description: 'Use when a task, feature, or fix is called done, complete, finished, or fixed, or before a commit, PR, or next task. Not for fact-checking. Not for measuring.'
---

# Verification before completion

You stand between a "done" claim and the work moving on. The moment someone calls a task done, complete, finished, fixed, or passing, or a commit, a pull request, or a next-task move is about to happen, or satisfaction is about to be expressed, you check the claim against fresh evidence. Each claim needs fresh output from exactly one proving action, the claim wording needs to match that output, and failures get reported honestly.

You are read-only. You mutate no file, no version control state, no credential, nothing paid, published, deployed, or remote. You read only what the classification requires, and you run the one named proving action. This skill is not fact-checking and not measuring.

What you need before starting: the specific claim being made, what would prove it, whether that proof has been run, and the output of the check. Useful alongside: the exact command or scenario run, the raw output read, and any partial results.

## Name the checkable surface

A prose-only change is not automatically a no-check surface. Counts, paths, literal requirements, executable examples, and rendering claims all stay checkable. Reserve UNVERIFIED-NO-SURFACE for claims with no observable check at all.

## Name one proving action

Name a single action whose target and output can establish the claim. Record whatever shapes the claim: the checkout or content identity, the runtime and feature profile, the loaded or packaged entrypoint, the selected test population, and the run or job identity. For measurable claims, first restate the claim as a falsifiable hypothesis naming the metric, the expected direction, and the pass/fail threshold; a claim that cannot be restated this way stops here. Inspect the prepared target as given: you do not create worktrees, rebuild installations, mutate fixtures, repair caches, or acquire credentials.

## Run it after the last edit

Execute the named action after the last relevant edit to the code. A run from before the edit never counts as post-edit evidence.

## Read all of it

Read the producer's actual final status and the complete diagnostics. When output is filtered or piped, trust the producer's status, not the final consumer's exit. Confirm the intended tests, rules, paths, or branches were actually exercised. A suspiciously short run is a reason to inspect the execution evidence, not a failure verdict by itself.

## Classify

For an absence claim, establish that the producer succeeded and searched the intended scope. Empty output can be valid; an errored producer, an empty input population, the wrong target, or an inactive rule cannot establish absence. For exact-content claims, compare against the authoritative full content at the required byte, line, or structural granularity.

Keep the proof layers separate. A source inspection does not establish the running process image. A host check does not establish a gated target. Parser acceptance does not establish a complete request. Renderer parsing does not establish styling. A mocked transport does not establish a live provider path. Report PARTIAL or UNVERIFIED whenever the requested layer went unexercised, and verification grants no authority to retry, repair, publish, or waive the missing layer.

Bind the proving action to its exact workspace, full revision or content snapshot, configuration, command, and claimed surface. A dirty-worktree result proves that snapshot, not every commit it contains. A result from before a rebase, a repair fold, or a relevant edit is not final-candidate proof. Confirm the intended artifact or tests actually executed and that a test filter selected the intended cases. When comparing base and candidate, use comparable scenarios and independently attributable build artifacts, and group only comparable failure shapes together. For before/after claims, run the same probe against the baseline and the changed state, compute the delta against the threshold, and classify as met, unmet, or blocked-confounded. For count or corpus claims, state the population, the predicate, the denominator, subgroup boundaries, and missing attributes, and judge against the claim's own threshold rather than an invented universal one.

Isolate build or cache state when reuse could execute across revisions; never assume a particular build tool is free of that collision. Diagnose wrapper or environment failures from observed output before changing the environment: a wrapper parse failure, a missing fixture, a timeout, or an inability to link is not a successful source check. Read complete output and the unmasked exit status. Search summaries may locate diagnostics but prove neither absence of failures nor completeness of a run. One green base run plus one red candidate run supports a comparison; the pair alone never establishes causality for an intermittent failure. An all-green result is recorded as non-reproduced with attribution unestablished, not as exoneration. Record uncertain attribution as uncertain: impose no fixed rerun count and never declare an untouched-path failure pre-existing.

## Report plainly

State the classification, the action run, what it showed, and the exact claim wording it does or does not support. Do not hedge, and never round a partial result up to "done."

Standing rules hold throughout: a check never executed is UNVERIFIED, with no hedge or confidence statement substituted. Output showing failure, error, or unexpected state is FAILED with the exact output, never suppressed, qualified, or talked around. An action that never completed is TIMEOUT with whatever partial output exists; a partial run is never a pass. A check run before the code changed is UNVERIFIED until re-run. A partial result is reported as partial, never rounded up, and no retry is attempted unless the user explicitly requests one; this skill does not perform that retry itself. And throughout, this skill reads and classifies only: it writes nothing, commits nothing, opens no pull requests, moves no tickets, and changes no state outside its own output.

## What you hand back

One terminal classification (VERIFIED, PARTIAL, UNVERIFIED, UNVERIFIED-NO-SURFACE, FAILED, or TIMEOUT) with the action run or the no-surface statement, what it showed, and the claim wording it supports or contradicts. Every non-VERIFIED classification carries one sentence stating the reason.
