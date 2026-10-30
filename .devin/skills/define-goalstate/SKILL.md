---
name: define-goalstate
description: 'Use when the user wants the finished-system contract for a piece of work: behavior, protocols, allowed, forbidden, and impossible states with a state-space proof. Not for runtime verification.'
---

# Define goalstate

Before building, write the finished-system contract: what the system must do, the protocols governing it, which states it may occupy, which it must never reach, and which it structurally cannot reach, plus a concrete proof that the classification holds and a checkable predicate for success. Downstream wayfinding consumes this document, so make it precise enough to test decisions against.

The skill's only write is the named local contract document itself (reversible by deleting or overwriting it), and nothing is written until the user approves the draft. No remote mutation, no other file touched.

## What the user must supply

The intended finished system: the behavior it must exhibit and the protocols governing its interactions, stated concretely. The user also classifies the states; you never invent states they did not name.

## Three kinds of state

- Allowed: a concrete, observable configuration the finished system may legitimately occupy while honoring the contract.
- Forbidden: a concrete, observable configuration that violates the contract. Every forbidden state is paired with an explicit terminal failure behavior (halt, rollback, bounded retry, degrade-to-safe-mode) named without ambiguity about what the system observably does.
- Impossible: a configuration the design, protocol, or environment structurally excludes. Each one must name the invariant or boundary that makes it unreachable; "unlikely" or "undesired" is not enough. If no invariant can be named, reclassify the state as forbidden or allowed. Never accept "impossible" as a wish.

## Building the contract with the user

1. Elicit the behavior and protocols as concrete statements.
2. Enumerate allowed states: at least one, each concrete and reachable through a named protocol step or input from an initial allowed state.
3. Enumerate forbidden states: for each, the concrete violation, the boundary it breaches, and the terminal failure behavior the system exhibits on observing it.
4. Enumerate impossible states: for each, the structural invariant or boundary that makes it unreachable, or stop and reclassify.
5. Prove the partition over the state space. For each allowed state, show the protocol-step sequence reaching it from an initial allowed state. For each forbidden state, show the allowed-step sequence that could reach it, then the boundary or failure behavior that intervenes. For each impossible state, show that no allowed protocol sequence can reach it because of the named invariant.
6. Write the success predicate: a concrete, checkable condition true if and only if the system satisfies the contract. Test it mentally (true for at least one allowed state, false for at least one forbidden state). If it cannot tell allowed from forbidden apart, reject the draft and ask the user to sharpen it.
7. Present the complete draft (behavior, protocols, all three state classes with invariants, proof, predicate, and failure behaviors) for approval. On approval, write it to the named local document; on rejection, revise per feedback and re-present. Never persist a rejected or unapproved contract.

## The document you hand back

A local finished-system contract in this order: behavior, protocols, allowed states, forbidden states, impossible states with the invariant or boundary behind each, the concrete state-space proof, the falsifiable success predicate, and terminal failure behavior for every forbidden state.
