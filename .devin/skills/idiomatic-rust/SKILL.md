---
name: idiomatic-rust
description: 'Use when writing, reviewing, or refactoring Rust code. Routes the task to handbook chapters on idioms, lints, errors, testing, generics, and pointers under the edition 2024 and current-stable pins.'
---

# Idiomatic Rust

You give Rust work its idiomatic answer. When code is being written, reviewed, or refactored, or a design choice about borrowing, error handling, dispatch, or testing needs settling, you route to the right handbook chapters, apply their conventions, and prove the result with the toolchain. You write only the Rust source and project files the invoking task already touches (version-control restore is the rollback), and chapter guidance plus verification output goes to chat. The job is done when the code or review follows the conventions below, the routed chapters were actually consulted, and the toolchain verification ran clean or its failure is reported with its cause.

What you need before starting:

- Rust task, required: code to write, a diff to review, or a design question.
- Crate or workspace root, required when it is not the current directory: supplies `Cargo.toml`, `rust-toolchain.toml`, and the edition pin.
- Toolchain pin, optional: defaults to the grounded pin named below.

## Pinning the toolchain

The grounded pin is Rust 1.99.1 stable ([released 2026-10-15](https://blog.rust-lang.org/2026/10/15/Rust-1.99.1/)) on edition 2024. Rust ships a rolling six-week stable train with no LTS channel, so current stable is the maintained target. When the project pins an older toolchain or edition, work inside that pin and note the delta. Name the effective toolchain and edition. The handbook's per-feature and library claims need their own evidence; the headline pin does not verify them.

## Finding the right chapters

Read every chapter the task touches in the same turn:

- `references/coding-styles-and-idioms.md` for borrowing versus cloning, `Copy`, `Option` and `Result` handling, iterators, comments, and when to extract a function.
- `references/clippy-and-linting.md` for Clippy configuration, key lints, and workspace lint setup.
- `references/performance.md` for profiling, redundant clones, stack versus heap, and zero-cost abstractions.
- `references/errors-and-resilience.md` for `Result` versus panic, `thiserror` versus `anyhow`, and error hierarchies.
- `references/testing.md` for test naming, one assertion per test, and snapshot testing.
- `references/generics-and-dispatch.md` for static versus dynamic dispatch and trait objects.
- `references/type-state-pattern.md` for compile-time state safety with the type-state pattern.
- `references/comments-versus-documentation.md` for when to comment, doc comments, and rustdoc.
- `references/pointers-and-thread-safety.md` for thread safety, `Send` and `Sync`, and pointer types.
- `references/retention-contracts.md` for admission, ownership, and retained memory bounds for caches and decoded representations.
- `references/json-boundaries.md` for JSON representation migration, raw tagged decoding, and lossless value preservation at service boundaries.

This step is done when each relevant chapter is loaded.

## Writing it the idiomatic way

Apply each convention that fits the task:

- Borrowing and ownership: prefer `&T` over `.clone()` unless ownership must move; take `&str` over `String` and `&[T]` over `Vec<T>` in parameters; use `Cow<'_, T>` when ownership is ambiguous.
- `Copy` types: passing a small `Copy` type by value is a heuristic, not a rule. The handbook threshold is about two to three machine words, roughly 24 bytes on a 64-bit target, because the copy avoids a pointer indirection. The real cutoff depends on the target register and calling conventions, so measure when the path is hot. A measurement always beats the heuristic; a heuristic states a default, not a law.
- Error handling: return `Result<T, E>` for fallible operations and keep `panic!` for unrecoverable bugs. Use `thiserror` for library error types and `anyhow` for application binaries, and propagate with `?`. Keep `unwrap()` and `expect()` out of production paths; tests and examples may use them.
- Performance: benchmark with `--release`, run `cargo clippy -- -D clippy::perf` for hints, avoid cloning in loops, and prefer iterators over intermediate `.collect()` calls.
- Dispatch: prefer generics (static dispatch) on hot paths, use `dyn Trait` for heterogeneous collections, and box at API boundaries rather than internally.
- Type state: encode valid states in the type system when invalid transitions must fail at compile time.
- Documentation: prohibit ordinary why, workaround, rationale, and TODO comments; keep only required SAFETY justifications where repository lints require them, compiler directives, and necessary public or module invariants in doc comments. Honor existing repository documentation lints rather than newly mandating missing_docs across every library.

## Proving it with the toolchain

Run `cargo fmt --check`, `cargo clippy --all-targets --all-features --locked -- -D warnings`, and `cargo test`. All three pass, or each failure is reported with its cause. A lint that must be suppressed uses `#[expect(clippy::lint)]` with a justification comment, never a bare `#[allow]`, because `expect` warns once the lint stops firing and the suppression cannot go stale. When `cargo clippy` is missing, install it with `rustup component add clippy`, since clippy ships as a rustup component in lockstep with rustc rather than as a separately versioned package. When the project pins an older toolchain, work inside that pin and report which conventions need a newer one.

## What you hand back

Rust code or review feedback that follows the conventions above, with the toolchain verification results or the blocking failure named.
