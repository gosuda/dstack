---
name: parallel-launch
description: 'Use when work splits into independent sub-tasks or cross-domain research. Not for durable scope ownership with per-scope review: use partition-scopes-to-subagents.'
---

# Parallel launch

You have one request that breaks into pieces with nothing shared between them, and you want every piece worked at the same time. This skill is that coordination: split the request, launch one agent per piece together, then stitch the pieces into a single checked result. It creates no file of its own. Anything agents change stays inside the local targets the request or the briefs name, and nothing touches a remote system. Every write is reversible local work, so before any mutation you hold each target's prior content or an exact undo for it.

If instead each piece needs durable ownership with its own review, you are in the wrong place: use partition-scopes-to-subagents.

## What you need up front

Take the request, its acceptance criteria, and enough source context that each piece can be done with no shared agent memory. For implementation work the request must name every local target agents may change. Output format, domain-specific agent choice, and ordering constraints are welcome when the caller gives them.

## Splitting the work

A concern earns its own agent only when it shares no mutable target and has no ordering dependency with any other concern. Do not split just to raise the agent count; with fewer than two independent concerns, do the request yourself directly.

1. Carve the request into independent concerns by that test. Dependent concerns go into later batches, each batch naming its prerequisites.
2. Before any mutation, list every batch's named local targets and capture the prior content or exact undo operation for each one.
3. Brief one task-specific agent per concern: complete context, bounded objective, named writable targets, acceptance criteria, concrete result format. No agent may rely on memory or output from another agent running alongside it.
4. Launch everything in the current independent batch together in one concurrent dispatch, and hold dependent work until its batch's prerequisites finish.

## Putting it together and checking it

Merge finished results where they do not conflict. Where they overlap, reconcile against the request itself; if the evidence does not settle a trade-off, report it openly rather than picking silently.

Then have an independent reviewer check the composition against the original request and acceptance criteria: every concern covered, outputs consistent with each other, claims supported, nothing beyond scope. For implementation work the reviewer also checks specification compliance and code quality.

Hand back the composition only when that review passes.

## When something goes wrong

- The split was unsafe: shared mutable targets or a hidden ordering surfaced. Do not launch that batch. Repartition into sequential work, or return `blocked` naming the conflicting targets or the dependency.
- An agent fails or comes back incomplete: keep every independently usable result untouched and return `blocked` with the failed concern, the observed error, the missed acceptance criterion, and one targeted follow-up.
- Results conflict and the supplied evidence cannot settle it: return `non-converged` with both positions, the unresolved fact, and the targeted check that would settle it.
- The review fails: do not present the composition as complete. Return `non-converged` with the failed review criteria, the usable partial results, and a targeted follow-up.
- Something mutated without authorization, or only partly: stop dispatching. Restore every changed local target from its captured prior content or exact undo, then report what was restored and anything that could not be. Never hide the error or claim completion.

## What you hand back

One reviewed composition mapping each concern to its result with review passage recorded. On failure instead: the usable partial results, the terminal classification (`blocked` or `non-converged`), the exact gap, the observed error or conflict, restoration status, and one targeted follow-up.
