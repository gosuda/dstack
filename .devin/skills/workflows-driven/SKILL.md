---
name: workflows-driven
description: 'Use when work decomposes across subagents or phases: audits, migrations, research sweeps, or scale one context cannot hold. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Workflows-driven

You run work that is too big for one context by fanning it out across subagents in phases. Reach for this when the job is an audit, a migration, a broad research or review sweep, or plain scale that one context cannot hold. A quick lookup, a single edit, an ordered plan with per-task review gates, or a flat split with no phase structure stays inline: do that work directly and stop.

Everything here is reversible and local. Workers write only named local evidence artifacts, each owned exclusively by one worker, so rollback is a non-issue. There is no remote mutation, and this skill never takes on remote, credential, publish, deploy, or irreversible work.

What you need before starting: the work item, which is required, plus any existing evidence ledger at the artifact path. You do not read conversation memory or another skill's output.

## Setting up the run

Scout inline until the full work list can be named: list the files, scope the diff, find the call sites. Never spawn workers while scouting. Then order the workflow as phases, where a phase is one wave of parallel tasks plus a barrier, later phases consume earlier phases' evidence, and each phase carries an explicit name.

Each wave ships with a shared batch context: the `# Goal` (what the wave accomplishes), the `# Constraints` (rules, non-goals, permissions, verification limits), and the `# Contract` (shared interfaces, output shape, coordination rules). Every assignment in the wave is self-contained: a `# Target` (exact files, symbols, or evidence surface, plus explicit non-goals), a `# Change` (what to inspect or modify, step by step, patterns to reuse), and an `# Acceptance` (the observable result and return packet). Workers skip formatters, linters, and project-wide tests; the parent runs the shared proof once.

Give every writing worker a disjoint scope: each path is owned by exactly one worker, and shared files such as manifests, configs, and indexes are edited by the parent only. If two workers must write one file, re-cut the wave before dispatching. Workers exchange file paths and artifacts, never pasted blobs.

## Dispatching a wave

Run the full wave with workers executing independently while the parent stays idle. File overlap is necessary but not sufficient for parallel safety: also serialize on shared types and APIs, migrations, lockfiles, snapshots, and environment singletons. Cap parallel workers at about three to five.

Give each batch a success threshold and honor it as a circuit breaker. When a batch falls below its threshold, stop the workflow and rediagnose instead of spending the remaining budget on a broken playbook.

After each wave, the parent reads the returned evidence, resolves contradictions, and runs the shared proof: inspect the actual tree rather than reported paths for real collisions, and re-run collided units serially. A wave declared done without the parent's own proof pass is a red flag. Then continue to the next phase until every phase is complete and the parent's proof pass passes on each.

Detect the host environment and apply the matching fan-out primitive per `references/host-materialization.md`.

## The closing chain

Work first: complete this skill's own implementation path before any closing pass.

Then run the review/fix loop against this skill's own gates: the parent proof pass per wave and the circuit breaker. Bound it at three fix cycles per unit, then stop as blocked or non-converged. Never widen scope to unrelated code.

Simplify last, contract-first. Re-derive the general case from contracts, delete the old structure with no shims, aliases, or flags, collapse special cases, migrate every caller in the same change, one concern per change. Ask first before removing any live consumer surface, causing data loss, or taking any non-reversible act. Stay inside this skill's authority. Run this skill's verifier after each increment and revert the increment on red. Close with a simplify compression pass (dead branches, duplicated logic, one-use wrappers) with behavior preserved and checks green.

## When a wave fails

A worker that returns no evidence means diagnose whether the worker ran at all; when the scope was sound, retry once with the same contract. A batch below its success threshold means stop the workflow and rediagnose, never continue to the next phase. Two workers colliding on one file means stop the wave and re-cut the partition so each file has one owner. A failed parent proof pass means examine the returned evidence and fix the root cause before the next phase. A coverage cap means declare what was dropped and why before acting on partial evidence; never silently cap.

Evidence files from successful workers in a failed wave are kept; the workflow never deletes them on failure. The parent reads and classifies a worker's evidence and never edits it.

## What you hand back

A consolidated report per phase: evidence summary, contradictions resolved, proof pass result, and next-phase readiness. The final phase produces the workflow closure report.
