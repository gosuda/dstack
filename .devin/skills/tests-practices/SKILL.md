---
name: tests-practices
description: 'Use when developing a fix or feature test-first, plan a TDD build, or work red-to-green in slices. Every test is invariant-based or offensive: it states a quantified property or an attack with an independent oracle, detects a named realistic fault, and survives behavior-preserving refactors. Not for hardening: use tests-adversarial. Not for deleting weak tests: use tests-purge-unneeded.'
---

# Offensive-first test practices

Classic agent TDD rots in a known way: the red test is written as a polite specification, the implementation drifts, and the agent, without noticing the drift, bends fixtures, weakens assertions, and patches contracts with ad hoc changes until green appears. The work is paid for twice and the suite proves nothing. This skill inverts the stance. Red is an attack, not a description: before any implementation, write the tests that try to break the contract, through boundary raids, invariant violations, error-path probes, and adversarial orderings. Green means the attacks failed to break the code, never that a saved output was matched.

This job is reversible and local. You write only named test and source files, and rollback is VCS revert of the implementation commit. There is no remote mutation. Tests and implementation never change in the same repair step.

## What you need before starting

| Target and requirement | The observable behavior or invariant to build or fix, and the confirmed public seam where it is observed. The seam is confirmed with the user before any test exists at it. When the existing specification, types, or requirements are already adequate, state the invariant directly; no separate contract file or detached workflow is required. Required. |
| Contract source | The spec, caller evidence, worked literal, interface definition, or stated invariant the attacks derive from. Never the implementation's own logic. Required. |
| Test framework | The project runner. If it is absent and not discoverable, stop and report. Never install one unasked. Optional when discoverable. |

## Which tests earn their place

Every test in the suite is admitted only when it states all five of the following, in the test name or its leading lines:

- Property under attack: the quantified invariant, semantic pre- or postcondition, or behavioral clause being broken, not a scenario label.
- Scope and seam: the confirmed public seam under test. No test exists at an unconfirmed seam.
- Independent oracle: the source of the expected value, derived without running the implementation and without reading a saved output. Reusable input data and setup helpers are allowed. Saved expected outputs, snapshots, recomputed implementation rules, and inline incidental wording pins (such as matching declarative `Display` formatting) are never oracles. An oracle being inline rather than in a fixture file does not make it strong.
- Distinct fault: one plausible consumer-visible fault this test detects, named concretely (off-by-one bound, inverted branch, dropped error, lost update under reorder, truncated write accepted as complete).
- Negative control: red evidence that the test fails for the predicted mode against absent or faulted code, not just any failure. An attack that passes against absent code is tautological. Discard it and write a sharper one.

Two further rules admit no exception. Each test binds the public seam only and must survive behavior-preserving refactors such as renames, restructures, and internal reimplementations. Distinguish semantic laws (formal preconditions, postconditions, state transitions, conservation laws, algebraic invariants, and error classifications) from shape or wording pins (superficial formatting, snapshot files, or declarative formatter phrasing). Semantic laws are the mandatory target of tests; shape or wording pins are banned as proof. A test that breaks under a refactor which preserved observable behavior is implementation-coupled: delete it, never repair it by coupling the code back to it. And there is no weak-test escape: history, coverage count, green status, prior approval, or single-occurrence regression fear never admits a test that fails this bar.

## Lines you do not cross

Never weaken an assertion, bend a fixture, skip a test, or loosen a behavioral contract to reach green. Any such edit during a green phase is a stop-the-line violation: revert it, then either fix the implementation or declare a contract change and re-attack from red. Never edit a test and its implementation in the same repair step; test-fixing and code-fixing are separate cycles, each with a named justification. Never accept a tautological attack (expected value recomputed the way the code computes it) or an implementation-coupled one (mocks internals, tests private methods, asserts call counts or order, reads storage around the interface). Attacks fire at confirmed public seams only. Banned as proof are fixture oracles (saved expected outputs), contract snapshots, output format pins (matching serialized shapes or declarative formatter prose), naive fixed single-path regressions unsubsumed by a quantified property, and coverage, history, or count-driven retention. Reusable inputs stay allowed. Oracles stay independent.

This skill is not for hardening existing code with no behavior change (that is tests-adversarial) or for deleting weak tests (that is tests-purge-unneeded).

## Working a slice

Work one vertical slice at a time, in this order:

1. State the invariants and behavioral clauses under attack. From the spec, callers, and independent literals, write the clauses the code must honor: valid behavior, boundaries, invariants, error semantics. Where a clause quantifies over inputs, state it as a property (for all valid inputs the relation holds; for all invalid inputs the rejection holds and prior state is unchanged) rather than as one worked path. When the codebase spec, interface, or user requirements are already adequate, state these invariants directly in the test suite or plan without requiring a separate contract file or dedicated workflow. Confirm the seam with the user. You are done when the clauses are listed with an independent truth source each, and the seam is confirmed.
2. Attack first. For the current slice, write the breaking suite before any implementation: for each clause, the boundary raid, the invalid input, the invariant violation, the error-path probe, the adversarial ordering that would expose a sloppy implementation. Prefer one quantified property per clause over a pile of fixed paths. Fixed paths survive only as documented members of a stated property, never as standalone proof. Run the suite. Every attack must fail red for the right reason, asserting the failure mode and not just any failure. You are done when the suite is red with each failure matching its predicted mode.
3. Implement until the attacks stop breaking it. Write only enough real code to survive the suite: no speculative features, no unrelated refactors. Rerun until green. If green cannot be reached, revert the implementation and try a different minimal approach. The attacks do not move. You are done when the suite is green with tests byte-identical to their red state.
4. Grill the green. Diff every test and fixture file (and any specification artifact, if one was explicitly created) against its red-phase state. No separate contract file is required when the spec is already adequate, but any test surface drift is a violation: revert it, then classify the change (implementation bug means fix the code; genuine contract change means declare it, update the clause list, and return to step 2). Drift that introduces a saved-output oracle, a snapshot, an incidental wording pin, or a weakened property is rejected outright, never declared as a contract change. You are done when the diff over test surfaces since red is empty, or every change is a declared contract change with its own re-attack.
5. Probe the suite teeth. Mutate the implementation once: flip the fix, invert a branch, shift a bound by one, and confirm at least one attack catches it. Then revert the mutation. A suite that survives its mutation probe proves nothing and returns to step 2 for a sharper attack. You are done when the probe was caught and the revert is clean.
6. Advance by vertical slice. Commit the slice (attack suite plus implementation, one commit naming the behavior), then take the next clause or seam from step 2. Multi-step work runs from a plan document listing one attack entry per requirement, ordered by dependency. The plan only execution mode is offensive-first. There is no implementation-first option. You are done when all agreed seams are exhausted and every test in the tree maps to a confirmed seam.

When a step fails, the rule is simple: a green reached by test-bending means revert the test edit, keep the red, and fix the code or declare the contract change aloud. An oracle violation means discard the oracle, re-derive it from the independent source, and if none exists, stop and report the missing prerequisite. An attack that cannot be written (unclear requirement, unconfirmed seam, no framework) means stop and report; never proceed to implementation on an unattacked contract. An implementation that cannot survive within the slice means revert the implementation, keep the attacks, and try a different minimal approach or stop and report. A mutation probe that survives means sharpen the attack before touching more implementation. An existing suite that breaks means revert and narrow the change until only the new slice behavior moves. Completed slices stand; a blocked cycle never invalidates prior green slices and never claims the done state. A partial result is the red suite plus its output, never a weakened green.

## What you hand back

Per slice, in order: attack files, red run output with failure modes matched, green run output, mutation-probe evidence, and the implementation commit SHA. Multi-step work prepends the plan document path.
