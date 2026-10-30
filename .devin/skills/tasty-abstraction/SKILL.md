---
name: tasty-abstraction
description: 'Use when a user wants to design an abstraction boundary that collapses a complex implementation into a simpler interface without leaking internal state. Not for implementation.'
---

# Tasty abstraction

Some surfaces are too raw to use directly: too many concepts, too many ways to break, too much expert knowledge per call. This job designs a boundary that collapses that complexity into one simpler interface, and it documents exactly where the raw surface still shows through. It stops at the design. Nothing here gets implemented.

This job is read-only. It creates no files, changes no code, and touches no credentials, remotes, or paid systems. Its only product is a specification delivered as chat output.

## What you need from the user

| Input | Why it matters |
|---|---|
| Target problem | The concrete complexity, repetition, or leak the abstraction must address. |
| Raw form | The current unabstracted surface the user works with directly. |
| Failure modes | The ways the raw form breaks, surprises, or requires expert knowledge. |

All three are required. Without them there is nothing to design against.

## Mapping the raw surface

List every operation, concept, and escape hatch the user touches today, plus every supplied failure mode. If the raw form turns out to have no meaningful complexity, say so and stop. No problem means no specification.

## Proposing the collapsed boundary

Propose one boundary that meets all three of these constraints:

1. It collapses at least two raw-form concepts into one interface operation.
2. It exposes every escape hatch the raw form offers, either as a direct pass-through or as a named override.
3. It introduces no concept that does not already exist in the raw form.

If no boundary can meet all three without leaking the very problem it exists to hide, report which leak breaks the boundary and write no specification.

## Mapping the escape hatches

For every point where the user must reach past the abstraction, state whether that hatch is sealed, exposed as configuration, or documented as a known seam. Leave none unclassified.

## Naming what still leaks

Every point where the abstraction can break, surprise, or demand raw-form knowledge is a leak. For each one, state the trade-off: what the abstraction gains by leaking here, and what the user must still understand. An abstraction with no documented leaks is an abstraction you have not examined closely enough.

## Writing the specification

The specification contains the abstraction name, the boundary definition, a table comparing raw-form concepts to abstraction concepts, the escape-hatch mapping, the leak inventory with its trade-offs, and a usage contract stating when to use the abstraction, when to bypass it, and what raw-form knowledge the user still needs. Deliver it as chat output.

A failed step means no specification at all. Partial results are never delivered as artifacts.
