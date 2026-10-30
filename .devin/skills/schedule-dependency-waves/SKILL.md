---
name: schedule-dependency-waves
description: 'Use when work units carrying declared dependencies must be ordered into execution waves before any dispatch, including detecting a dependency cycle. Not for partitioning one issue into disjoint write sets: use diamond-task. Not for concerns with no dependencies: use parallel-launch.'
---

# Schedule dependency waves

You turn a set of named work units and their declared dependencies into an execution order, so a dispatcher can run each wave knowing everything it needs is already done. You never invent, split, or merge units, and you never dispatch anything yourself. You only produce the order.

This skill is read only on the work tree. Its only write is the named schedule artifact, and its rollback is deleting that artifact. It makes no remote changes.

## What you need from the caller

| Input | What it is |
|---|---|
| Work units | The full set to schedule, named as the caller names them. Schedule exactly these, no more and no fewer. |
| Dependency edges | Declared edges, each saying one unit must follow another. Use only declared edges. Never infer coupling from file ownership, write sets, or guesswork. |
| Schedule artifact path | The one local file you may write. Nothing else is a valid write target. |

## Ordering the waves

These steps run in order, and each one gates the next.

1. Build the graph from supplied units and edges only. Check every edge: both endpoints must be supplied units. If any edge points at a unit that was not supplied, stop. Name the edge and its missing endpoint, write nothing, and leave the artifact path untouched. A schedule built on a silently dropped edge marks work ready that is not.
2. Check for cycles before assigning anything. If the graph has a cycle, stop. Name the participating units, write nothing, and leave the artifact path untouched. A partial schedule that hides a cycle is worse than no schedule.
3. Place each unit in the earliest wave after all its dependencies. A unit's wave is one past the highest wave of its dependencies, and units with no dependencies go in wave one. Every supplied unit lands in exactly one wave, with all its dependencies in strictly earlier waves.
4. Write the schedule artifact. List the waves in topological order, naming each wave's units and, per unit, the dependency edges that justify its placement. This artifact is the only write this skill makes.
5. Say what is ready now. Report wave one (the units with no dependencies in the supplied graph) as the ready now set.

## When there is nothing to schedule

- Empty unit set: say so and write nothing. Never emit an empty artifact.
- Unreadable or duplicated unit names: ask the caller to disambiguate first. Duplicate names would put one unit in two waves and break the exactly one wave guarantee.
- Caller repairs and re-runs: on a cycle or a rejected edge, suggest the caller fix the declared edges (supply the missing unit or withdraw the bad edge) and re-run on the corrected set.

## What you hand back

On success, the schedule artifact at the named path: waves in topological order, each wave listing its units, each unit annotated with the edges justifying its placement, plus the ready now statement naming wave one. On a cycle, an unknown endpoint edge, or an empty unit set, a failure report naming the problem units or edges, with no schedule artifact written.
