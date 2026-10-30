---
name: validation-first-driven
description: 'Use when protocols, workflows, concurrency, or lifecycle state need states, transitions, and temporal properties. Not for domain models: use type-driven. Not for contracts: use contract-driven.'
---

# Validation-first development

You prove a stateful design correct before it gets built. Reach for this when the work involves explicit states, transitions, temporal properties, or lifecycle-heavy state: protocols, workflows, concurrent systems, anything where the wrong state at the wrong time is the failure mode.

Stay out when the work is stateless. A stateless endpoint, a pure data transformation, simple CRUD without lifecycle, a configuration parse, or a stateless batch process comes back unaltered, with no state machine modeling applied. Domain modeling without temporal behavior belongs to type-driven; obligation and permission contracts belong to contract-driven.

You work reversibly and locally: you write only inside the stated target, rollback is version control, and you never mutate a remote or touch files or version control outside the target. What you produce is the model and the spec plus implementation assertions and tests, with a TLA+ or Alloy spec and a model-checker run for high-risk designs.

What you need before starting: the requirements or design document, which is required. The current codebase helps when one exists. Four support notes are available and optional, since the skill stands alone without them: `references/approaches.md`, `references/examples.md`, `references/formal-tools.md`, and `references/event-sourcing.md`.

## The specification pass

Work the steps in order:

1. Confirm the work is state-heavy. If it turns out stateless, return it unaltered and stop.
2. Extract every named state, state variable, action, guard, and side effect from the requirements. Catch each temporal property in its own terms: "always eventually", "never", "until", "leads-to".
3. Choose one mechanism level, with a reason, defaulting to the strongest the language supports:

   | Level | Mechanism | Use for |
   |---|---|---|
   | Typestate | Generic type params, phantom data | Protocol APIs, builder patterns, Rust FFI |
   | Statecharts | Nested states, parallel regions | Game state, multi-modal UI, XState |
   | Flat FSM | Enum plus match/switch | Order lifecycle, connection management |
   | Actor model | Independent entities, message passing | Distributed systems, Erlang/Elixir |

4. Write the state machine specification in this shape:

   ```
   STATE MACHINE: <Name>
     STATES: S1 | S2 | S3
     VARIABLES: var1: type, var2: type
     INIT: var1 = val, state = S1
     ACTION name(args): PRE: guard -> POST: new_state, effects
     INVARIANT: condition_that_always_holds
   ```

5. Rank every invariant by enforcement strength, strongest first: type system, then state machine, then contract, then runtime check last.
6. Push every invariant the type system can express into types: typestate, sealed classes, or discriminated unions that make invalid states unrepresentable.
7. Model what types cannot express as an explicit state machine with states and transitions. High-risk designs also get a TLA+ or Alloy spec plus a model-checker run. High-risk means the design involves distributed consensus, lock-free concurrency, a protocol with liveness or safety guarantees, or multi-party state coordination. Anything below that threshold is served by the state machine spec and tests, with no model checker involved.
8. Check every transition: invariants hold after each action, matching over states is exhaustive. Block on any violation.
9. Write assertions and tests that map each temporal property to an assertion, a test, or a model-checker run, with every transition tested and every invariant carrying a verification point. Retryable state-changing operations carry an idempotency key derived from the intent, never from a fresh UUID, a timestamp, or a regenerated value: claim the key atomically, since a check followed by an act is a race; fail loudly when the same key arrives with a different payload; record intent before calling out; retain the key longer than the longest retry path including replays; and document the operation as unsafe to retry when no key can be honored.
10. Implement against the spec: one authoritative definition per state and transition, one invariant check per concern, state kept beside the behavior it governs.

## When the work blocks

A design that meets the high-risk threshold but whose TLA+ or Alloy checker cannot be installed or run comes back as exit 11 with a blocked verdict. Never proceed past that point without verification. Below the threshold no checker is needed, so its absence blocks nothing.

A specification syntax or type error returns exit 12 with the first error location, and implementation waits. A violated invariant returns exit 13 with the violating state or transition; never mask or suppress it. A test failure returns exit 14 with the failing test, and required tests gate the work. An implementation that no longer matches the spec returns exit 15 with the mismatched function or type, and finalization waits.

When any gate fails, report the highest verification gate that passed with its exit code and evidence. Never claim the work is done while a blocking gate is red. If the state space proves undecidable or the checker never terminates, stop and report the open temporal properties with no coverage.

## What you hand back

The state machine specification, the implementation with assertions for every transition and invariant, the test suite covering all states and transitions, the TLA+ or Alloy model for high-risk designs (omitted below threshold), and the exit code: 0, or the blocking gate's code.
