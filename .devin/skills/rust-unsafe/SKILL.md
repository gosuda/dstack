---
name: rust-unsafe
description: 'Use when writing, reviewing, or auditing unsafe Rust, or understanding raw pointers, transmute, UnsafeCell, and safe abstractions over unsafe code.'
---

# Rust unsafe

You review unsafe Rust and say exactly which invariants each block depends on and where the proof is missing. The `unsafe` keyword unlocks five capabilities, and everything starts by matching the code against them. You never change source files: the result is a chat-output guidance report with pointers into `references/unsafe-patterns.md`.

What you need before starting: the unsafe Rust code or diff under review. An audit focus (raw pointers, transmute, `UnsafeCell`, FFI, `Send`/`Sync`, or safe abstraction) and whether to plan a Miri run are optional and narrow the review.

## The five things unsafe unlocks

| Capability | Example |
|---|---|
| Dereference raw pointers | `*const T`, `*mut T` |
| Call unsafe functions | `extern "C"` functions and `unsafe fn` |
| Access or modify mutable statics | `static mut X` |
| Implement unsafe traits | `unsafe impl Send for MyType` |
| Access union fields | `union` field access |

Name every capability the code uses before auditing any of them. The identification step is done when each `unsafe` capability in the code has been named.

## Checking raw pointer dereferences

For each dereference, confirm the pointer is non-null, aligned, points to initialized memory, does not violate aliasing, and stays valid for the reference lifetime. The step is done when all dereferences carry documented invariants. When a pointer violates aliasing, restructure to avoid simultaneous `&` and `&mut`, or use `UnsafeCell` with a documented ownership scheme.

## Checking unsafe functions and traits

Verify each `unsafe fn` carries a `/// # Safety` contract, each `unsafe trait` impl upholds the trait invariants, and each `unsafe impl Send`/`Sync` is justified by real thread safety. The step is done when all unsafe items have documented contracts. A contract that only says the function is unsafe is not a contract: write down every precondition the caller must uphold. Calls to `alloc`, `alloc_zeroed`, or `dealloc` require a non-zero-size `Layout`; a zero-length buffer must take no allocator path and `Drop` must skip `dealloc` when nothing was allocated. A manual `Send`/`Sync` impl that cannot prove thread safety gets removed or gets a Miri or concurrency test behind it. When an `unsafe` block covers too much, split it so each `unsafe` operation has its own safety comment.

## Checking transmute and UnsafeCell

Confirm source and target types share a size, the value is valid for the target type, and `UnsafeCell` uses are protected against concurrent mutation. The step is done when transmute and interior mutability uses are justified. A transmute that can produce an invalid value becomes a safe conversion instead (`TryFrom`, `f32::from_bits`, `u32::from_ne_bytes`, or similar).

## Running the audit checklist

Apply the checklist from `references/unsafe-patterns.md` to every `unsafe` block and mark each item. The step is done when the checklist is complete for the whole review.

## Planning Miri tests

Suggest `cargo +nightly miri test` for the unsafe code, with `MIRIFLAGS="-Zmiri-strict-provenance"` for pointer-heavy code. The step is done when a test plan names its commands.

## What you hand back

A structured report naming each unsafe operation, its invariants, and missing documentation; a checklist result per `unsafe` block; a test plan naming Miri or sanitizer commands; and pointers to `references/unsafe-patterns.md` for raw pointer, `NonNull`, transmute, and stacked borrows patterns.
