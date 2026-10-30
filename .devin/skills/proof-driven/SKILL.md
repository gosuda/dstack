---
name: proof-driven
description: 'Use when property-based testing, theorem proving, or formal proof tactics require zero unproven properties. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Proof driven

You prove a target correct and leave it correct. The policy is zero unproven properties: every planned property passes, none is skipped or pending, line coverage reaches at least 80 percent, every counterexample found along the way keeps a permanent regression test, and every definition the proof covers is total. Your writes stay inside the agreed target: named local property tests, proof artifacts, regression tests, and only the implementation remediation a demonstrated failure requires. No remote state, credentials, deployments, or unrelated files change. Rollback is restoring the touched files from version control or their pre run copies.

To start you need the target implementation and its test command, the requirements or contracts the properties come from, the exact writable file scope, and a line coverage command that can measure the target. When model based testing is claimed, a reference model is required. Existing input fixtures, regression tests, generators, invariants, formal specifications, and a configured property testing or theorem proving framework come along when they exist. Treat requirements, generated values, and external models as untrusted until their types, domains, preconditions, and termination assumptions are explicit.

## Set the boundary first

Bound the writable scope to the supplied target, the property and proof files, the regression test files, and the remediation files. Record the commands that will run the properties and measure coverage. If any required command or framework is unavailable, stop there.

## Say what should hold before you touch code

Derive the properties from the requirements before changing any implementation. Enumerate the correctness, safety, invariant, and termination obligations, then arrange them as one main property with supporting properties and edge cases, so no assumption stays implicit.

## Give each property a fair oracle

Pick the simplest independent oracle for each obligation: postcondition, invariant, idempotence, inverse or round trip, model equivalence, commutativity, or a metamorphic relation. For stateful code define the commands, a reference state model, the transition preconditions, and the invariants across command sequences. Never restate the implementation as its own oracle.

## Match a proof tactic to each property

Choose the strategy that fits: simplification, constructor or boundary case analysis, induction for recursive or sequential behavior, contradiction, construction, model checking, or empirical property exploration where no formal proof is available. Check numeric bounds and complexity arithmetic mechanically with the project's own tooling rather than unsupported mental calculation.

## Write the properties before you run anything

Create every planned property test or formal proof obligation before the first verification run, one concern per property. Generate domain valid normal, boundary, empty, zero, negative, maximum, overflow, and invalid cases wherever the contract permits them. Retain known concrete cases as input fixtures evaluated against independent invariants or adversarial oracles; delete tests that pin status quo behavior without an independent contract.

## Run everything and keep the smallest failure

Run every property and proof obligation. Reject vacuous properties, framework self tests, discard rates that prevent meaningful exploration, nonterminating definitions, and skipped or pending obligations. For each failure use the framework's invariant preserving shrinker when one exists and keep the smallest reproducible counterexample.

## Turn each failure into a regression test, then fix

Convert every minimal counterexample into a deterministic regression test before remediating. Fix the demonstrated defect inside the bounded scope, rerun the regression test and the affected property, and iterate. Never delete, weaken, skip, or broaden a failing obligation just to get a pass.

## The bar for calling it proven

Finish only when the full property and proof set, the retained regression tests and concrete invariant checks, and line coverage all pass together: all green, skipped and pending counts at zero, coverage at least 80 percent, every counterexample represented by a regression test, the target matching the proven model, and the termination obligations holding.

## Exit codes and what they mean

- 0: success. Report the created or changed property and proof files, the deterministic regression tests for all counterexamples, the bounded remediation files, the commands run, the passing property and proof counts, the zero skipped and pending counts, the line coverage percentage, and the requirement to property hierarchy.
- 11: framework unavailable. Change no implementation. Report the missing executable, package, configuration, or prover and the attempted command.
- 12: no properties created. Claim no success. Report the requirement or oracle information that is missing.
- 13: property failure or incomplete proof. Preserve the minimized counterexample and any valid passing artifacts, but classify the run as non-converged. Revert any remediation that introduced regressions by restoring only the bounded files, then report the failing property, the seed or proof goal, the smallest counterexample, and the last verified state.
- 14: coverage or property gap. Report the uncovered requirement and the measured coverage. Never mark an obligation proven from execution that did not reach it.

Out of scope remediation stops before writing: return a blocked result naming the required file or authority expansion. Never invent a proof, suppress an error, discard a counterexample, or claim completion from partial results.
