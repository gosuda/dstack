---
name: rust-debugging
description: 'Use when debugging Rust binaries with GDB or LLDB, enabling pretty-printers, interpreting panics and backtraces, debugging async with tokio-console, or stepping through no_std code.'
---

# Rust debugging

You locate the fault and show the evidence. Panics, hangs, wrong output, and stuck async tasks all end with a backtrace, a breakpoint state, a variable value, or an async task trace that names the cause.

Scope stays local. This skill adds and removes temporary debug instrumentation in local source and `Cargo.toml`, runs local debuggers and builds, and writes build artifacts to `target/`. Rollback reverts the source and configuration edits and removes build artifacts. Chat also carries `dbg!`, `tracing`, `console-subscriber`, and `RUST_BACKTRACE` settings plus debugger transcripts. Nothing touches a remote.

What you need before starting:

- The symptom (required). Failing binary, panic message, wrong output, or hang.
- The build mode (required when it cannot be inferred). Debug build or release with debug symbols.
- The debugger (required). GDB, LLDB, `rust-gdb`, `rust-lldb`, or tokio-console.
- Extra setup (optional). Custom panic hook, tracing subscriber configuration, or embedded probe settings.

## Building with symbols the debugger can read

Use `cargo build` for a debug build. For release, add a `release-with-debug` profile in `Cargo.toml`. Separate debug symbols on Linux/ELF by building release, then `objcopy --only-keep-debug`, `strip --strip-debug`, and `objcopy --add-gnu-debuglink`. Move on when the binary carries symbols the chosen debugger reads.

## Loading pretty-printers

Prefer `rust-gdb <binary>` or `rust-lldb <binary>` for automatic Rust pretty-printers. Manual setup sources `gdb_lookup.py` and `lldb_lookup.py` from the `rustc --print sysroot` path. Full detail lives in `references/rust-gdb-pretty-printers.md`. Proceed when `String`, `Vec`, and `Option` render as Rust types. When printers fail to load, switch to `rust-gdb`/`rust-lldb` or source the sysroot scripts by hand.

## Stopping and inspecting

In GDB: `break myapp::module::function_name`, `run <args>`, `next`, `step`, `continue`. In LLDB: `b myapp::module::function_name`, `r <args>`, `n`, `s`, `c`. Use `break rust_panic` to stop on panic. Execution should halt at the expected location or reproduce the fault.

Read state with `p my_vec`, `info locals`, `bt` (GDB) or `p my_vec`, `frame variable`, `thread backtrace` (LLDB). The variable or call stack should explain the symptom.

## Capturing and triaging panics

Set `RUST_BACKTRACE=1` or `RUST_BACKTRACE=full`, or call `std::backtrace::Backtrace::force_capture()` in a custom panic hook. A backtrace should result and identify the panic site. When output stays incomplete, set `RUST_BACKTRACE=full` or raise the backtrace limit.

Match the message to its likely cause and decide whether the fix is bounds checking, `unwrap` or `expect` handling, overflow, or assertion logic. In release, `panic = "abort"` aborts on panic; core dump capture depends on OS and ulimits. State the root cause and the fix.

## Adding temporary tracing

Add `tracing` and `tracing-subscriber` to `Cargo.toml`, initialize a subscriber in `main`, and instrument functions with `#[instrument]`. Remove this instrumentation after use. Logs should show the execution path around the fault.

## Debugging async tasks

Add `console-subscriber` and enable the `tokio/tracing` feature, run the program, then run `tokio-console`. Inspect task states, waker activity, blocked tasks, and poll durations. The async bottleneck or deadlock should become visible. When a task stays invisible, confirm `console_subscriber::init()` runs and the tokio `tracing` feature is on.

## Debugging bare metal targets

Connect with OpenOCD and `rust-gdb` over a target remote, or use `probe-run --chip <chip> target/<triple>/debug/<binary>`. Verify the probe connection and target power. The target should halt at a breakpoint or emit probe logs; when the probe is missing, check the OpenOCD config, connection, and power.

## What you hand back

The located fault, identified panic cause, or confirmed async bottleneck; the commands and configuration used for the session; and a list of source changes made, so they can be reverted.
