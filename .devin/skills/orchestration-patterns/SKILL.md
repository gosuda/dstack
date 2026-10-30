---
name: orchestration-patterns
description: 'Use when work decomposes across subagents or role panels and needs coupling-based orchestration. Not for cloud-agent task-graph orchestration.'
---

# Orchestration patterns

You coordinate work split across subagents or role panels: parallel research, review waves, staged handoffs. Your job is picking the coordination mechanism that fits how the pieces couple, then owning verification and synthesis. You write only the reconciled synthesis to named local artifacts (rollback is undo), spawn subagents as needed, and never mutate anything remote.

## Match the mechanism to the coupling

First classify each task by its coupling:

- Independent: no ordering constraint or shared mutable state, and the task benefits from an isolated context.
- Ordered: the task requires a prior task's output.
- Adversarial: another role must challenge its evidence or conclusion.

Then apply the first matching row. The mechanism in the right column is the complete move, not a pointer to another skill or command.

| When the work looks like | Do this |
|---|---|
| Several independent tasks produce mergeable results | Spawn one subagent per task in the same orchestrator turn, require a named artifact from each, then inspect and reconcile all artifacts. |
| Tasks are ordered | Spawn only the first ready task. Inspect its artifact, extract the exact input the next task needs, then spawn that next task. Stop at any failed handoff. |
| Independent tasks each consume a large input but return a small digest | Give each subagent only its assigned source slice and a fixed digest schema; keep source text out of the orchestrator context, then reconcile the returned digests. |
| One task needs one perspective and one artifact | Spawn one subagent with that goal, inspect its artifact, and use it directly after verification. |
| The same independent role must process several units | Spawn one isolated subagent per unit in the same turn; require the same output schema from all units and reconcile only after every unit verifies. |
| Roles must challenge one another | Spawn independent advocate and critic roles from the same evidence in one turn; require claim-evidence-objection records, then resolve each objection against the cited evidence yourself. |

## Check before fanning out

Before spawning more than one subagent, confirm all four: the concurrent tasks have no ordering dependency and do not write the same target; each role or unit has a distinct bounded assignment and named output; the returned artifacts fit in your remaining context for verification and synthesis; and parallel execution materially reduces elapsed time or preserves context enough to justify the extra runs. If any check fails, drop to one ready subagent at a time using the ordered handoff above.

Keep orchestration depth at one: only you spawn subagents, and every subagent gets an explicit prohibition on spawning another agent. A subagent with follow-up ideas records them in its artifact for you to decide after verification.

For concurrent work, issue every subagent call in one orchestrator turn; for ordered work, issue one call, verify its artifact, and only then issue the dependent call. Every subagent gets its role, bounded input, concrete goal, allowed tools, forbidden writes, output path or schema, and done predicate.

## Verify every artifact yourself, then reconcile

Inspect each actual artifact rather than trusting a reported path or summary, and confirm all six: it exists, it covers the assigned input, it follows the required schema, it stays within authority, it cites evidence for factual claims, and it satisfies the task's done predicate. A missing or invalid artifact is a failed unit.

Resolve overlaps and disagreements against cited evidence, and give every verified unit a material disposition in the synthesis: accepted, superseded with reason, or rejected with reason. Do not synthesize while any spawned unit lacks a disposition. Then write only the reconciled synthesis to the named local artifact and remove any partial synthesis created during the run. Subagent artifacts may remain only when the synthesis cites them as evidence; otherwise discard them after reconciliation. If you started a synthesis before all artifacts verified, remove it, keep the verified source artifacts, and resume at verification.

When a unit fails (it loops, returns no artifact, exceeds its bounded assignment, or fails verification), stop dependent work, name the failed unit and the failed criterion, and do not write a synthesis. When some units verify and some do not, report both sets and preserve the verified artifacts as evidence, but never present a partial synthesis as complete. When two assignments target the same mutable artifact, cancel the colliding parallel plan before accepting either write, restore the named local target to its pre-run state, then rerun the units one at a time with separate artifacts. When artifacts conflict and their citations do not resolve it, return the conflicting claims and the missing evidence; do not invent a deciding fact. When verified artifacts will not fit reconciliation, replace each unstarted large-input unit with the bounded digest mechanism above; if already-returned artifacts still cannot be reconciled, stop without synthesis and report the unprocessed set.

## Pausing for review

If the assignment changes mid-run to review-only or approval-gated analysis, stop authorizing writes and ask active writers to stop after their current atomic operation. Preserve partial state; do not finish, format, revert, or commit it merely to make the pause tidy. Bind review evidence to a stable version: confirm the writer stop, record the covered paths and content identities, and use immutable local evidence artifacts when needed. A read-only review does not authorize source repairs or execution outside the review's tool permissions. Before reporting, establish whether the reviewed source version stayed unchanged; if it drifted, identify the affected scope rather than presenting the old review as current. Report implementation status separately from review coverage, and never treat automated notices, timeout defaults, or reviewer results as user approval to resume writes.

## Closing the run: work, review loop, simplify

Complete this skill's own coordination path before any closing pass. Then run its own review and fix gate (verify every artifact, then reconcile) to green, bounded at 3 fix cycles per unit before stopping as blocked or non-converged, never widening scope to unrelated code. Finally simplify offensively: re-derive the general case from contracts, delete old structure with no shims, aliases, or flags, collapse special cases, migrate every caller in the same change, one concern per atomic commit. Ask first before removing any live consumer surface, stay inside this skill's authority, run its verifier after each increment and revert on red, and close with a compression pass over dead branches, duplicated logic, and one-use wrappers with behavior preserved and checks green.

## What you return

One reconciled synthesis artifact at the supplied local path, citing every contributing subagent artifact and recording a disposition for every spawned unit. On failure, the named failure class, affected units, failed criteria, and rollback state, with no partial synthesis.
