---
name: guillotine
description: 'Use when dead, duplicate, superseded, or generated residue must leave more than one artifact class of a repo or subsystem, preserving behavior. Not for a single enumerated record set with no cross-artifact consumers.'
---

# Guillotine

Some code is wrong. This skill is for code that is merely heavy: dead paths nobody calls, the same fact owned in two places, an old implementation the active path already covers, or generated copies checked in beside their generator. When that weight spreads across more than one kind of artifact (code plus docs plus tests plus config plus workflows), cut it here. If the mess is a single enumerated record set with no cross-artifact consumers, this is the wrong tool.

Everything you do stays inside version-tracked files, and version control is your rollback. You never touch remote state, rewrite history, migrate stored data, handle credentials, or delete anything untracked or critical. Interior debt with a proven-unchanged boundary needs no second approval; anything reaching an observable surface needs explicit authority first.

## Name what must not change

Before anything else, name the subsystem or repository region under the knife and write down its observable boundary: the commands, public routes, generated outputs, or user scenarios that must behave identically after the cut. Also pin down the repository-native gate command that defines "passes" (required, or discoverable in the repo).

If no boundary can be named, stop before editing. An unprovable boundary means an unprovable cut.

## Build the ledger, then classify it

Walk every artifact class the weight touches (code paths, documents, tests, dependencies, configuration entries, workflows, generated files) and give each candidate one ledger entry: the job it claims, its live callers or readers, its source of truth, and which kind of residue you suspect it is.

Then classify every candidate into exactly one of these five:

| Category | Meaning |
|---|---|
| Dead | No live caller, route, import, loader, build step, or documented consumer. |
| Duplicate | Another artifact owns the same fact or operation, and all consumers can move to it. |
| Superseded | The active path covers the required contract and no supported path selects the old one. |
| Generated residue | The repository generator reproduces the required output and does not select this copy. |
| Keep | The evidence still names a live job, even if the artifact is ugly. Ugly is not dead. |

No candidate goes unclassified, and nothing gets two labels.

## Prove the cut from both directions

For each candidate, search outward from the candidate to its consumers, then inward from each required consumer back to its owner. Where static references cannot settle necessity, run a focused behavioral, mutation, build, or generation probe and let it decide.

A cut proceeds only on bidirectional proof: both search directions agree with the classification, or a probe settled the ambiguous case.

## Stop and ask when the cut reaches a live surface

If the proposed cut touches an observable API, a user command, stored data, history, remote state, an untracked file, a credential, or a critical target, stop. Show the exact consequence and offer a recoverable alternative, then wait for explicit authority. Name the target, the evidence, and the recovery path. Nothing proceeds on implication.

## Cut one closed slice at a time

Work in dependency-closed slices: move every live consumer to the single surviving owner first, then delete the obsolete implementation, the tests that protected only obsolete behavior, dependency entries, configuration, workflow steps, and generated copies together. Leave no aliases, shims, dual paths, tombstones, or "deprecated" wrappers behind, so that every required consumer resolves to one live owner.

Then regenerate every repository-owned surface the cut touched. If the generator recreates the removed residue, the generator's source selection is the bug; fix it there instead of hand-deleting its output again.

## Prove the boundary held

Exercise every named boundary element and run the repository-native gate. Then re-run the route, import, registration, and source-of-truth searches: the old path must be absent everywhere, and every required consumer must resolve to one live owner.

When something fails, restore the smallest failed slice from version control, correct its ledger classification, and continue with the remaining proven cuts. A classification error is reported, not hidden.

## When the evidence turns against a candidate

- A candidate still has a live consumer: reclassify it as keep, or widen the slice so that consumer moves inside it.
- Two artifacts both look canonical: stop cutting and establish one owner before deleting either copy.
- A test fails only because it asserts obsolete internals: prove the observable contract elsewhere first, then delete or rewrite the test. Never weaken a real boundary test to make the cut pass.
- A dependency looks unused but participates in loading, build, or delivery: keep it until a real package or artifact probe proves removal safe.

## What you hand back

The candidate ledger with a cut-or-keep verdict per entry, the removed paths grouped by artifact class, the surviving owner of each moved consumer, the observable-boundary evidence, the native gate results, and any approval-gated remainder left for explicit authority.
