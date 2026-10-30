---
name: code-review
description: 'Use when a named diff or pull request needs review for bugs, regressions, tests, and standards. Not for reviewing requirements or plans, handling feedback already left on a PR, or shipping the change.'
---

# Code review

A review hides no defect behind familiarity: every finding names its evidence. Judge the change against intended behavior and project requirements, not a preferred rewrite; a small diff can carry a serious defect, and an adequate change needs no findings. This skill is read only by default. It reports a verdict with findings and coverage, and it touches code only when the invocation carries an explicit apply authorization, only inside the reviewed scope.

No review here pushes, opens a PR, files a ticket, switches a branch, or checks out a working tree to reach its scope. Uncommitted work is reviewed only from the checkout that holds it.

## Settle scope before reading code

Pin down the reviewed scope first: an explicit revision range, a branch with a determinable base, or a PR identity. Resolve the base from explicit input or PR, upstream, or remote default evidence; never guess the base. Record what is in scope and what is explicitly out. Note the scope mode and depth signals too: full or focused, from the size, risk, and touched surfaces. Depth follows risk, never a fixed count. An unresolvable or unreadable scope means returning blocked with the missing identity or path, never dispatching a review at an unreachable target.

## Choose lenses from risk

Always cover correctness, regressions, tests, and the applicable standards for the touched surfaces. Add conditional lenses only on evidence, and name each selected lens with a one line reason:

*   Security: trust boundaries, data handling, or auth are touched.
*   Concurrency: shared state is touched.
*   Migration: schema, wire, or persisted shapes change.
*   Performance: only for measured hot paths, never on suspicion.
*   Control (agent or AI feature surfaces): the agent could act irreversibly. Check for an approval gate where one is needed, an escape hatch to interrupt or redirect, and visible confidence, escalation, and uncertainty signals; each finding cites the missing gate or signal with its consequence.

## Review against evidence

Every finding cites file and line, the offending code, the requirement or behavior it violates, and the consequence that justifies action. No invented issues and no style only findings. Check claims against the whole change and project facts; reviewer suspicion is not a finding until verified. Name the single fact the change's safety depends on; when no such fact exists, assess each risk independently. Trace consumers beyond symbol search, including library sources with pinned versions and local patches, scheduling and lifecycle ordering, and wire shapes, flags, and cross language readers up to three hops downstream, marking each path reachable with evidence or unreachable with the search that showed it. Record each risk with likelihood, cost, and exact file and line, and state plainly any caller or API not found in the tree. A lens with insufficient evidence is marked limited in coverage, not failed; nothing is invented to fill it.

## Report verdict, findings, and limits

Deliver the verdict, findings ordered by consequence, and explicit coverage: what was examined, which lenses ran, and the limits (unreadable paths, unavailable evidence, deferred surfaces). Note uncertainty rather than stopping to ask: this skill never blocks on questions. An adequate change gets the clean verdict with coverage, never manufactured findings.

## Corrections only on explicit orders

Report only is the default; a nested workflow later owns any repair. An explicit apply authorization in the invocation permits local corrections inside the reviewed scope with the narrowest applicable checks. Report the corrected files with their check results. An apply request without authority, or reaching beyond scope, is refused with the boundary stated.

## What you hand back

The verdict, findings with file and line evidence and consequences, coverage and limits, and, when apply ran, the corrected files with check results. No machinery narration follows, and no downstream action follows a report only review.
