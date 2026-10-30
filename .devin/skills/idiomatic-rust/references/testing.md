# Automated testing discipline: invariants, isolation, and oracles

Automated tests in Rust serve as executable specifications and regression guards. A test suite must prove behavioral invariants under deterministic conditions with refactor-resilient oracles, rather than asserting on brittle incidental strings, unexamined status flags, or mock echoes.

## Structure and naming by observable behavior

Name unit tests by the action under test, the precondition state, and the expected observable invariant, such as `empty_input_fails_with_missing_identifier` or `ascii_alphanumeric_input_preserves_normalized_token`. Avoid vague names like `test_add_happy_path` or `test_parser_success`. A test name should state the exact contract that failed when reviewing test runner logs.

Group related tests into nested submodules matching logical subsystems, such as placing parsing invariants within a `parsing` module and canonicalization checks within a `normalization` module. Cargo and IDE test runners report qualified module paths, making failures immediately localizable.

## Coherent invariant verification

Testing one behavior means verifying one complete invariant or state transition, not artificially restricting a test to a single assertion macro.

When checking a postcondition, verify all interdependent properties of the state transition together. For an insertion into a collection, assert that the operation succeeded, that the length incremented, and that the inserted item is retrievable. Splitting these into fragmented tests leads to weak assertions, such as checking only `is_ok()` without inspecting the resulting state. Avoid combining unrelated behaviors into a single test function; separate failure modes and input partitions belong in distinct test functions.

## Test execution, discovery, and filtering

The standard Cargo test harness compiles and runs unit tests, integration tests, and doc-tests across the workspace:

- Substring filtering: `cargo test <filter>` executes tests whose qualified module or function path matches the filter string, such as `cargo test parsing::`.
- Doc-test execution: `cargo test --doc` compiles and runs code blocks embedded in doc comments.
- Integration test filtering: `cargo test --test <integration_name>` runs only the specified integration test binary.
- Output capture: `cargo test -- --nocapture` allows diagnostic stdout and stderr streams to bypass test runner interception.
- Ignored tests: `cargo test -- --ignored` runs tests marked with `#[ignore]`.

### Nextest execution and doc-test discovery

When using `cargo nextest` (via `cargo nextest run`), tests execute in isolated processes with per-test timeout tracking and parallel scheduling. However, `nextest` executes only unit and integration test binaries and does not discover or run documentation tests. Any CI workflow or local check relying on `nextest` must invoke `cargo test --doc` as an explicit companion command.

## Concurrency, process state, and environment isolation

Rust's standard test runner executes test functions concurrently across worker threads within a single process by default. Tests must maintain strict thread and process isolation:

- Process-global working directory: Calling `std::env::set_current_dir` modifies process-wide state, causing concurrent threads that resolve relative filesystem paths to observe unexpected directory shifts. This creates test interference and flaky path resolution races across threads, though it is not inherently a memory data race in safe Rust.
- Environment variable mutation unsafety: Mutating process-global environment variables (`std::env::set_var` or `std::env::remove_var`) in a multithreaded test harness modifies the underlying libc `environ` table. This cannot be made sound merely by wrapping write operations in a mutex: unsynchronized concurrent reader threads (calling `std::env::var`, `std::env::vars`, or third-party code calling `getenv`) read `environ` without acquiring that mutex, triggering C-level data races and undefined behavior.
- Hermetic parameter injection: Eliminate global mutation by passing configuration values, filesystem paths, and environment records explicitly into constructors and components rather than reading process-wide state within business logic.
- Isolated filesystem paths: When filesystem access is required, allocate unique temporary directories per test via `tempfile::tempdir()`. Never share hardcoded paths across concurrent tests.

## Test taxonomy: unit, integration, and documentation tests

Rust projects organize tests across three distinct tiers based on visibility, scope, and execution boundaries:

### Unit tests

Unit tests reside in the same source file as the implementation under `#[cfg(test)] mod tests`. They have access to private and package-private (`pub(crate)`) items, verifying internal invariants, mathematical identities, and algorithmic edge cases without exposing internal state to consumers.

### Integration tests

Integration tests reside in separate files in the top-level `tests/` directory and compile as external crates consuming only the public API (`pub`) of the library:

- Independent test binaries: Cargo compiles each top-level file in `tests/*.rs` as an independent test executable.
- Shared helper placement: Placing shared helpers at `tests/common.rs` creates a standalone test binary. Zero tests in `tests/common.rs` do not cause the compilation or execution to fail (the binary runs zero tests and exits successfully), but it produces wasted compilation overhead, links an unnecessary binary, and clutters runner output. Shared test helpers must be placed in a subdirectory module, such as `tests/common/mod.rs`, which Cargo recognizes as a non-test module.
- Contract validation: Integration tests verify multi-module interactions, configuration parsing, lifecycle transitions, and public crate contracts.

### Documentation tests

Documentation tests are executable examples embedded in doc comments (`///`) and executed via `cargo test --doc`:

- Setup line hiding: Lines prefixed with `# ` execute during testing but are omitted from rendered documentation, keeping API presentations focused on the interface.
- Execution attributes:
  - `no_run`: Compiles the example to verify type safety and API compatibility without executing the binary, appropriate for examples requiring external network services or hardware.
  - `should_panic`: Verifies that the code block triggers a deliberate panic under invalid input.
  - `compile_fail`: Verifies that invalid usage is rejected by the compiler.
  - `ignore`: Omits both compilation and execution. Valid Rust examples should not use `ignore`; unexecutable syntax belongs in non-Rust code blocks.
- Paired compiler boundary verification: A `compile_fail` test passes if compilation fails for any reason, including unrelated syntax errors, invalid imports, or typos. To prove that `compile_fail` tests the intended language or invariant boundary (such as borrow lifetimes, private visibility, or trait rejections), it must be paired with an equivalent positive test case verifying that the valid baseline construct compiles cleanly.

## Invariant assertions over incidental format pins

An assertion is an executable contract stating preconditions, postconditions, and state invariants against real state.

Reject weak test oracles:
- Never assert bare boolean status: Calling `assert!(result.is_ok())` without validating the resulting state, or calling `assert!(result.is_err())` without classifying the exact error variant, leaves tests blind to functional regressions.
- Reject string-matching oracles: Do not match formatted error strings (such as `err.to_string() == "invalid input"`) or check that an output buffer is non-empty (`assert!(!output.is_empty())`). Formatting is presentation, not semantics. Formatting assertions break on cosmetic wording updates while failing to verify structured error payloads or causal error chains.
- Variant matching with `std::assert_matches!`: In modern Rust, import `assert_matches` via `use std::assert_matches;` to pattern match enum variants and bind payload fields directly, asserting variant classification and inner data in a single step.

### Reference invariant testing pattern

Rather than duplicating production code or inventing artificial token parsers with blanket mutation claims, refer within the bundle to the self-contained `divide` and `DivisionError` example in [Error modeling and resilience](./errors-and-resilience.md). That example demonstrates:

- Independent invariant selection: Invariants are evaluated against external mathematical identities (such as the algebraic inverse relation between multiplication and division) rather than mirroring internal implementation logic or hardcoding expected return literals.
- Adversarial input selection: Input vectors systematically cover boundary cases, including positive and negative zero divisors (`0.0`, `-0.0`), extreme numerator magnitudes, and diverse divisor signs, probing fault-prone transition edges rather than arbitrary values.
- Covered fault classes: The suite exercises three specific fault classes: omitting the zero divisor guard, negative-zero guard handling (catching naive zero checks that miss `-0.0`), and inverted or corrupted operands that violate the algebraic reconstruction bound.
- Refactor resilience: Internal optimizations or algorithmic adjustments that maintain the mathematical contract pass cleanly without breaking on incidental changes, while faults that violate algebraic correctness fail deterministically.

## Snapshot testing boundaries and verification oracles

Snapshot testing tools (such as `cargo insta`) capture serialized data, terminal outputs, or rendered markup to snapshot files for human review of presentation changes. Snapshots must never serve as automated correctness oracles:

- Snapshots are not proofs: Matching a recorded snapshot proves only that output has not changed; it does not prove that output is correct.
- Blind approvals codify regressions: Running snapshot review commands to accept modified output risks overwriting reference baselines, turning regressions into accepted truth.
- Independent domain assertions: Test passing verdicts must be determined by assertions checking domain invariants, parsed records, round-trip equality, and semantic predicates. Use snapshots strictly for diffing complex rendered views with unstable fields (such as timestamps and UUIDs) redacted.

## Adversarial branch execution and collision proofs

A passing test does not prove that a rare collision branch, retry loop, or fallback mechanism actually executed. Tests covering error recovery and retry policies must arrange preconditions deterministically and require an observable branch witness:

- Observable execution witnesses: When testing collision retry loops or cache eviction fallbacks, inspect an observable indicator (such as an atomic retry counter, an explicit event emission, or a distinct error variant) in addition to verifying the eventual outcome.
- Process ID collision and exec semantics: When verifying components that derive resource identifiers from process IDs (such as PID-derived socket names or lockfiles), note that `exec` preserves the PID of the replaced process, whereas `spawn` allocates a new child PID. Tests proving collision resilience must establish deterministic PID collisions in an isolated namespace, verify that the retry loop detects the occupied resource, and prove that a fresh identifier is allocated.
- Deterministic cleanup: Ensure all test artifacts, temporary directories, and sockets are managed through RAII drop guards (such as `tempfile::TempDir`) so resources are unlinked and cleaned up even when tests panic.
