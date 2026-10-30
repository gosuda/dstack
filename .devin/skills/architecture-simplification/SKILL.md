---
name: architecture-simplification
description: 'Use when the user explicitly asks to simplify an architecture, collapse modules or crates, or cut a dependency graph within approved boundaries. Executes an approved layout direction slice by slice. Not for single-module cleanup: use code-simplification. Not for layout planning from nothing: use architect. Not for blind re-derivation: use breaking-driven.'
---

# Architecture simplification

This skill performs the cut. The user names a subsystem and the direction it should go, directly or through a layout already approved via `architect`, and this skill re-derives the interior so fewer modules, crates, and dependency edges remain, with every in-scope caller migrated in the same motion and the product boundary preserved. It plans nothing from nothing: without an approved direction, the layout question belongs to `architect` first.

It runs only on an explicit user request to simplify, collapse, or re-derive a subsystem layout. It never starts itself from a smaller cleanup, and routing or handoff here grants no permission. Only the approved scope and recorded yeses authorize the work.

## Start from the approved scope and the contracts it must preserve

Before touching anything, write down three things and the approval covering them:

- The exact path set under review (subsystem, crate set, or layer set), plus every dependency edge entering, leaving, or crossing it, each with its owning file and line, observed in the tree.
- The consumer-visible surfaces that must survive: public APIs, re-exports, wire and on-disk shapes, configuration keys, plugin points, documented examples, and the end-to-end behavior the layout must keep working.
- The approved layout direction, whether stated by the user or carried over from `architect`. This skill executes that cut; it does not substitute its own plan.

Derive the preserved contracts from call sites, tests, signatures, wire shapes, and configuration consumers, never from the layout's own aspirations. With a missing or vague scope, stop and ask for the exact path set rather than inferring a subsystem from a symptom. Anything outside the approved set needs a new explicit scope.

## Judge every module by the decisions it hides

A surviving module earns its place by hiding exactly one family of decisions behind a contract its callers can rely on. Shared language, after Matt Pocock's codebase-design work: a **module** is anything with an interface and an implementation, at any scale; the **interface** is every fact a caller must know (types, invariants, ordering, errors, configuration, performance), not just the type-level surface; **depth** is behavior hidden per unit of interface learned; a **seam** is where behavior can be substituted or tested in isolation; an **adapter** is the concrete thing sitting at a seam. Depth buys callers leverage and maintainers locality: fix once, fixed everywhere.

Classify each in-scope module as an essential owner (keep, or merge into as the surviving owner, with a one-line reason naming the decision family) or as residue: a forwarding tier, single-use layer, duplicated owner, or dead branch of the graph, cut with a reason. Classify each edge as load-bearing, with consumer-need evidence behind it, or removable as forwarding, speculative, or superseded. Competing canonical owners are never unified on judgment alone: the survivor needs consumer-need evidence, and the losing import path migrates fully.

Run the deletion test on every suspect: imagine deleting the module. Where complexity vanishes, it was a pass-through, so name the callers that absorb it and cut it. Where complexity reappears across callers, it was earning its keep. Judge depth by leverage, never by line or branch ratios, which reward padding the implementation; and never treat an interface as just a keyword or method list, which omits the invariants and failure modes callers depend on. Simplify directory depth and width by domain cohesion and change propagation (modules that change together belong together), with no arbitrary depth or fan-out quotas and no shallow wrappers left standing.

## Treat each dependency by what varies across it

How a merged module gets tested depends on what sits behind its seam:

| Dependency | Treatment |
|---|---|
| In-process (pure computation, in-memory state, no I/O) | Merge freely and test through the new interface directly; no adapter needed. Keep separate only when owners or change reasons differ. |
| Local-substitutable (a local stand-in exists, such as an in-memory filesystem or a containerized service in the test suite) | Deepen when the stand-in exists; the seam stays internal and no port appears at the external interface. |
| Remote but owned (the team's own services across a network boundary) | Define a port at the seam: the deep module owns the logic, transport arrives as an injected adapter, tests use an in-memory adapter, production uses the real transport. |
| True external (third-party services the team does not control) | Take the dependency as an injected port and test with an adapter that asserts observable outcomes through the interface, not a mock echo. A dependency that cannot be classified counts as true-external. |

One adapter means a hypothetical seam; two justified adapters, typically production plus test, make a real one. Never introduce a port for a hypothetical variation (a single-adapter seam is just indirection). Internal seams used only by the module's own tests stay private; never widen the external interface just because tests use them.

## Never cross the product boundary on silence

Interior layout (every caller in-tree, nothing persisted, shipped, externally configured, or version-promised) is re-derived without further asking. Boundary surfaces (a public API, a crate-root re-export an external example or downstream crate imports, a wire or on-disk format, live configuration, a plugin point, a version promise) need a recorded yes immediately before removal, relocation, or migration. Pause before each such cut and ask the user; proceed only on an explicit yes for that surface. On silence or no, keep the surface permanently as contract and hand the compatibility cut to `refactor-break-compat` with file, line, evidence, and reason. A boundary cut attempted on silence is restored from version control, with the surface, the missing yes, and the handoff recorded. Routing, prior approval of the interior, or a handoff from another skill never substitutes for that yes.

## Collapse, move, and migrate in the same cut

Collapse the condemned modules and edges into their surviving owners; move code to its justified owner; update every affected internal caller, test reference, example, and doc pointer in the same commit series, one slice per atomic commit. Never leave a caller on a removed module or edge, and never leave a shim, alias, tombstone, re-export stub, dual path, or deprecated wrapper behind as a convenience. Enumerate config-selected, environment-selected, and build-variant-selected references by exact token search, not by assuming them absent. The cut stays incomplete while exact-token search for any removed module, edge, or re-export still finds a survivor (or the hit is reclassified as not-dead with its consumer evidence). A hidden consumer found mid-cut stops that surface until its exact tokens are enumerated and migrated, or a no is recorded.

## Prove the layout holds

After each atomic commit run the narrowest verifier (compiler or typechecker first, then the repository's own test command) and finish with the applicable end-to-end check for the subsystem. A red baseline stops all cutting and is reported first with the failing tests and end-to-end state; never cut on unproved ground. A regression reverts that slice, with the failing check recorded, while prior green slices stand.
Where a boundary rule already exists as a compiler or linter import boundary, enforce the surviving edges through it and show the rule bites. Never invent weak directory-shape tests, and never write tests that restate the new layout: each check must prove an invariant or stand as adversarial proof against a plausible fault, and must survive equivalent refactors.

Permitted test edits are mechanical migration to the new layout (imports, paths, fixture wiring, renamed symbols) plus assertion updates strictly required by an approved contract change, each with a recorded reason. Forbidden: deleting, suppressing, skipping, or weakening tests to force green. Test shrinkage belongs to `tests-purge-unneeded` under mutation proof; doc-only purges belong to `purge-slop-docs`. Without a verifier or end-to-end check, state exactly which claims are unproved instead of claiming done.

## Stop conditions and recovery

- Vague or missing scope: ask for the exact path set; infer nothing.
- Red baseline: report the failures; cut nothing.
- Slice regression: revert the slice, record the check, keep prior green slices.
- Boundary cut on silence: restore, record, hand off.
- Hidden consumer: stop that surface, enumerate tokens, migrate or record no.
- Ghost references remain: remove the survivors or roll back the slice.
- No verifier or end-to-end: name the unproved claims.
- Partial result: keep green slices, report rejected slices with reasons, and never call the layout done while callers dangle or residue stands.

## What you hand back

The re-derived layout, plus the record of how it got there: the approved scope and plan anchor, module and edge classifications with reasons, applied slices with atomic commits and migrated callers, boundary decisions with yes or no evidence, the ghost-sweep result, verifier and end-to-end results, and the structural deltas (crate, module, and edge counts) as observed evidence, never as targets. The work ends in one of three states: simplified, already-at-floor, or blocked with the exact missing scope, yes, prerequisite, or hidden consumer named.
