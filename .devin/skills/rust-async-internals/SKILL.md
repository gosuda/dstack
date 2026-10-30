---
name: rust-async-internals
description: 'Use when understanding the Rust Future poll model, Pin and Unpin, tokio scheduling, async stack traces, waker leaks, or select!/join! behavior.'
---

# Rust async internals

You explain how Rust async actually runs and fix the places it stalls. When someone asks how `.await` works, hand-rolls a `Future`, fights a `Pin` error, watches a slow task in `tokio-console`, or trips over `select!` and `join!`, you trace the poll and wakeup loop down to the concrete call that misbehaves and name the fix.

This skill never touches anything remote. It writes only local Rust source, `Cargo.toml` instrumentation, and diagnostic reports; rollback is `git checkout --` or `rm` for new files, and chat carries the guidance and findings.

What you need before starting:

- The Rust code or runtime behavior at issue (required). The async function, the runtime builder, or the tokio-console output.
- The task (required). Explain the poll model, implement a `Future`, diagnose `Pin`/`Unpin`, debug with `tokio-console`, or fix blocking and `select!`/`join!` trouble.
- The runtime version (optional). Defaults to `tokio` on Rust 1.99.1.

## Tracing poll and wakeup

First pin down the executor: run `rustc --version` and `cargo tree -i tokio` and confirm whether the project runs on `tokio` or something else. Then describe the `Future` trait the way it executes (`poll` returning `Poll::Ready` or `Poll::Pending`, the `Context` waker the executor parks, the loop that re-polls on wakeup) so the reader can map every `.await` to poll calls and wakeups.

When asked for a custom `Future`, write a type that holds its state, returns `Poll::Pending` until its event arrives, and clones and wakes the waker to schedule the re-poll. It is done when it compiles and runs under `cargo test` or the example binary.

## Pinning self-referential futures

Async state machines borrow across suspension points, so they cannot be moved once polled. State that `Pin<P>` prevents moving the value behind `P`, and reach for `Box::pin` for heap futures, `std::pin::pin!` for stack futures, or a pinned trait object as the shape demands. The reader should finish able to pick the right pinning method for each case. When an `await` point complains about `Pin`, look for a self-referential borrow and pin before awaiting.

## Spawning without blocking the runtime

Tokio tasks are cooperative: `tokio::spawn` for async work, `tokio::task::spawn_blocking` for blocking I/O or heavy CPU, `tokio::task::yield_now` to surrender cooperatively, and `tokio::task::LocalSet` for `!Send` futures. Choose by workload, because blocking calls never stay on a runtime thread. Concretely, replace `std::thread::sleep` with `tokio::time::sleep(...).await`, `std::fs` reads with `tokio::fs`, and heavy CPU with `spawn_blocking`; the task is fixed when it no longer blocks a runtime thread.

For a factory that starts background work before returning, define who owns cleanup while construction is pending and after success or failure. Keep the cleanup guard armed across every fallible or cancellable suspension and disarm only after ownership transfers successfully. Cleanup in `Drop` must not await or block. Prove pending cancellation, successful transfer, and failure through the actual construction seam, then establish that the public factory uses that seam (a guard-only test does not prove factory wiring). If termination is required, observe task completion or a drop witness after a rendezvous proving the task started; a cancelled token alone is insufficient. Record killed and surviving mutations separately, and do not claim the wiring closed while a bypass survives.

## Watching live tasks

When asked, add `console-subscriber` to `Cargo.toml`, initialize it before the runtime starts, build with `RUSTFLAGS="--cfg tokio_unstable" cargo run`, and run `tokio-console` in another terminal. It is working when task lists and poll times appear. If no tasks appear, the subscriber was initialized too late or `tokio_unstable` is missing.

## Surviving select and join

`select!` completes when the first branch wins and drops the rest; `join!` waits for all of them. `biased;` changes polling order, and a future polled repeatedly across loop iterations needs `Fuse` or re-creation inside the loop (polling a completed future without it is the classic stall). When a dropped branch needs cleanup, accept the cancellation semantics or guard the cleanup with the select and a drop guard, and rewrite the branch or loop so the cancellation point is explicit.

## When async stalls or misleads

A runtime blocked by synchronous work means moving the call to `spawn_blocking` or swapping in the async equivalent. A future that cannot be polled after completion means `Fuse` or fresh construction per iteration. A `Pin` error at an `await` means checking self-referential borrows and pinning with `Box::pin` or `pin!` first. An empty `tokio-console` means confirming subscriber initialization order and the `tokio_unstable` flag. A `select!` branch vanishing mid-work is cancellation semantics, handled with an explicit guard. Never pretend the branch survived.

## What you hand back

An explanation of the poll model, `Pin`, or tokio task model as requested; instrumented source or `Cargo.toml` with `console-subscriber` when diagnostics were needed; and a chat report naming the blocking call, waker leak, or `select!`/`join!` fix.
