---
name: tests-adversarial
description: 'Use when hardening error handling, validating boundary behavior, or hunting silent failures. Not for feature development: use tests-practices. Not for test deletion: use tests-purge-unneeded.'
---

# Adversarial test authoring

Most suites prove the happy path works. This job proves the sad paths fail loudly. You write tests that attack inputs, ordering, timing, state, resources, and impossible cases, and you fix any silent failure they expose so every failure path produces a descriptive error.

This job is reversible and local. You write only test files, local artifacts, and the minimal production changes needed to make silent failures signal. Rollback is reverting the commit or deleting the added files. There is no remote mutation.

## What you need before starting

| Input | Why it matters |
|---|---|
| Code under test | The source files, modules, or functions to harden. Required. |
| Language runtime and sanitizer toolchain | The compiler, test runner, and available sanitizers (ASan, TSan, MSan, Miri, `-race`, or equivalent). Required. |
| Existing suite | Prior tests, so you avoid duplication and can see the gaps. Optional. |

Three lines you do not cross: never commit with an unresolved sanitizer warning, never commit while silent failures remain, and never commit while documented assumptions lack violation tests. A gate that fails stops the work at that gate.

## Recording what the code assumes

Read the code for what it actually does, not what its documentation claims. For each function or module, record the assumptions that touch error paths, boundary behavior, or silent failures. Cover these six categories and skip correct-path behavior the existing suite already proves:

| Category | What to record |
|---|---|
| Inputs | Types, nullability, ranges, empty collections, boundary values, encoding |
| Ordering | Argument order, sequence dependencies, lifecycle ordering, concurrent call interleaving |
| Timing | Timeouts, premature delivery, clock skew, token expiry mid-operation |
| State | Half-initialized state, shared-state corruption during operation, post-error recovery, double-close |
| Resources | File descriptor exhaustion, disk full, permission revocation, allocation failure, connection pool saturation |
| Impossible cases | Concurrent modification during iteration, recursive re-entry, self-referential data, deep nesting overflow |

Each assumption becomes a named, executable check with a unique identifier. You are done with this pass when every error-surface assumption is named.

## Writing one violation per assumption

Name each test after the violation it proves, such as `test_rejects_negative_quantity` or `test_recovers_from_mid_write_crash`. Test through the public API only. If triggering a failure needs private access, record that as a finding. You are done when every documented assumption has at least one violation test.

## Throwing the standard attacks

Run these attack families against every applicable assumption:

- Data: zero, negative, MAX_INT, NaN, Infinity, negative zero, empty string, null bytes, multi-byte Unicode (emoji, RTL, ZWJ), empty, single, and capacity-sized collections, encode-corrupt-decode.
- State: double-close, use-after-dispose, read-after-error, concurrent mutation during iteration or serialization, half-written interrupted state, out-of-state-machine events.
- Environment: file not found, permission denied, disk full, read-only filesystem, network timeout, connection reset, DNS failure, partial write, clock jumps, OOM during cleanup.
- Protocol: out-of-order messages, duplicate delivery, missing acknowledgment, partial writes (truncated JSON or protobuf), version mismatch, request after close, response after timeout.

## Testing the boundaries from both sides

If the limit is N, test N-1, N, and N+1. If the limit is 0, test -1, 0, and 1.

## Keeping negative tests honest

A negative-path test must witness entry into the protected path and assert the intended rejection or recovery. A shared error code, an empty result, or an elapsed timeout is not proof. Reject empty assertion populations and malformed fixtures that never reach the behavior under test.

| Test kind | What honesty requires |
|---|---|
| Checker and inventory tests | Start with a valid fixture, introduce one defect per scenario, and demand its specific diagnostic. Check required inventory against the independently settled contract, not only manifest-tree agreement. Cover missing required items, unmanifested items, and altered generated results when those are in scope. A missed defect is a coverage finding, never automatic permission to delete the checker. |
| Default and literal tests | Classify default references as expectations, invalid inputs, or explicit alternatives before changing them. Keep the pinned product requirement as text and state the check as an independent property. Use literals as input data only, never as the verdict. For producer-consumer agreement, compare the actual producer against the composed consumer segment, exercise every relevant composition path, and fail if a pointer lacks its owner there. Do not widen the bundle merely to make the assertion pass. |
| Shared-state and concurrency tests | Build a causal poison-before-victim or held-operation scenario, witness the protected state, assert the guard-specific result, and release or cancel deterministically. Choose cleanup hooks from the actual lifecycle. Redundant hooks need a joint explanation rather than invented independent necessity. |
| Subprocess tests | Derive the test budget from the product contract and an explicitly named test bound. Witness actual spawn and route reachability, use a fake that obeys the real argument and result-channel contract, and test required cancellation or signal threading per distinct route. Observe owned-child termination and reaping. Never infer success from a fail-open return that could occur before spawning. |
| Target and harness tests | Exercise the claimed minimum runtime, the actual parser, the package entrypoint, or the real substrate when that is the boundary under test. Keep instrumentation-compatible containment. Do not remove resource protection solely from an unvalidated environment heuristic. Publish executable fixtures completely before launch and isolate packaged artifacts from development fallbacks. |

Temporary production mutations used to establish causal test coverage need a separately authorized regression-proof workflow. The authority to fix discovered silent failures below is not blanket authority to mutate arbitrary production guards.

## Fixing the silent failures you find

Every failure path must produce a descriptive error. Silent corruption and generic messages are failures. When a test exposes one, apply the minimal production fix that makes the path signal: add an error return, raise a typed exception, or log and propagate. Do not refactor unrelated code or widen scope.

## Running the sanitizer gates

Pick sanitizers by failure class and language, at most two per run to keep the gate tractable:

| Situation | Sanitizer |
|---|---|
| Memory safety in C or C++ | ASan, plus MSan when uninitialized reads are in scope |
| Data races in concurrent languages | TSan (C, C++, Swift), `-race` (Go) |
| Rust unsafe code | Miri |
| Java | No ThreadSanitizer exists for standard Java toolchains. Record the gap and use the available checks. |

If the project toolchain does not support a selected sanitizer, record the gap and proceed with the available one. Run the full suite under each selected sanitizer, since tests that pass without sanitizers can hide undefined behavior. You are done when everything passes with zero warnings, or the unsupported gaps are recorded.

## Committing the work

Stage and commit once all gates pass, with a message naming the assumptions violated, the silent failures fixed, and the sanitizer results. No commit happens until every gate passes, so no rollback is ever needed.

## Reading the exit codes

| Code | Meaning |
|---|---|
| 0 | All clear: assumptions documented, violations tested, errors meaningful, sanitizers pass |
| 1 | Untested assumptions remain |
| 2 | Silent failures remain |
| 3 | Crashes or panics |

Report the code with its meaning. A sanitizer warning or a crash blocks the commit until it is resolved or documented as a defect. An unavailable sanitizer is recorded as a gap in the commit message and never excuses a failure in one that ran.
