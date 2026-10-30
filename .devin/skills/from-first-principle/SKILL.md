---
name: from-first-principle
description: 'Use when a user wants to rebuild a design, organization, or API from primitives. Not for a perspective take: use from-perspective.'
---

# From first principle

When the current shape of something has accumulated too much history to reason about, stop patching it and rebuild it from what it cannot exist without. You take a design, an organization, or an API, strip it down to its irreducible primitives, derive the structure those primitives force, and write the result as a local specification (including an honest diff against what exists today).

This rebuilds from primitives; it does not strip an existing structure down. A perspective take on a question belongs to from-perspective. Restarting from a blank greenfield belongs to fromzero. Nothing here touches anything remote, and the existing target stays read-only throughout: the only thing you write is one named local rebuild specification, and rolling back means deleting that file.

## What you start with

The target to rebuild (a design, an organization, or an API) with access to its current form for read-only comparison. Optionally, the user may insist on the primitives to start from; when they do not, you derive the primitives from the target itself.

## Rebuild in order

1. Name the target and say which of the three kinds it is. Move on once the target type is stated.
2. Enumerate the irreducible primitives: the concepts, data, or operations the target cannot exist without, none of them derivable from something smaller inside this target. Move on once every primitive is listed and confirmed irreducible. If the target will not reduce to stated primitives, stop here and report which concept resists reduction, and never invent primitives to fill the gap.
3. Derive the structure from those primitives alone, rejecting anything not forced by a primitive or a necessary composition of primitives. Move on once every surviving element traces back to a primitive or a composition.
4. For each derived element, record the primitive or composition that forces it. Anything with no primitive basis is an open assumption, not a derivation, so label it as such and never present an underived element as primitive-forced.
5. Write the rebuild specification to the local artifact: the enumerated primitives, the derived structure, each derivation step, and the open assumptions. If some section cannot be completed honestly, emit the artifact with the finished sections and the open assumptions listed; never plug a gap with a plausible but underived element.
6. Diff the rebuilt structure against the existing target inside the same artifact, marking what changed and what was dropped as non-primitive.

## What you hand back

The local rebuild specification, in this order: enumerated primitives, derived structure, per-element derivation steps, the change-and-elimination diff against the existing target, and the open assumptions.
