---
name: leave-only-first-principle
description: 'Use when asked to prune a design or codebase until only primitives remain, producing a first-principles map. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Leave only first principle

You take a design artifact or codebase and strip it until only primitives remain, producing a map that shows what the thing is actually made of. The human names exactly one target at invocation, with an optional trust boundary marking any section out of scope. The only thing you write is the pruning map artifact, which is deleted for rollback. Nothing here touches remotes, credentials, publishing, deployment, or anything irreversible.

## Start from one named target

Confirm the exact design artifact or codebase path. If the human named more than one target or the boundary is unclear, stop and ask for a single bounded target. The decomposition that follows is ordered, so settle this before listing anything:

1. Inventory every named component: modules, classes, functions, data structures, and abstractions. Skip nothing, including deprecated and generated sections.
2. Label each component as primitive or composite. A primitive is a language keyword, a stdlib call, a well-known third-party call with a single documented responsibility, or a human-declared irreducible building block. A composite is anything that hides a decision, delegates to another named component, or can be expressed more simply.
3. Decompose each composite into its constituents, recursing into any sub-component that is itself composite. Stop recursing at primitives, which decompose no further.
4. Write the map to `<target-name>-primitives.md` as a tree or structured list in which every leaf is a primitive. Annotate leaves that are architectural decisions rather than code units.

## Stop early instead of forcing convergence

| Situation | Marker and behavior |
|---|---|
| The decomposition circles without reaching primitives | Stop and surface the contested section with a `loop-detected` marker. |
| The human asserts a composite is primitive | Accept the assertion without reclassifying. The human outranks the taxonomy. |
| The work stops before full decomposition | Return the partial map with a `non-converged` marker. Never claim an incomplete map is complete. |

No composite survives as a leaf in a finished map. Anything short of that carries its marker honestly.
