---
name: rustc-basics
description: 'Use when selecting RUSTFLAGS, configuring Cargo profiles, tuning release builds, reading assembly or MIR output, understanding monomorphization, or diagnosing compilation errors.'
---

# rustc basics

rustc is driven through Cargo profiles and `-C` codegen flags. The right answer is a profile entry or a flag, verified against the installed toolchain, and that is what you hand back: a chat-output recommendation or explanation, never a source edit.

What you need before starting: the goal (build mode, profile tuning, output inspection, binary size, or error triage). The `rustc --version` output and target triple when they cannot be inferred, plus the workspace Cargo.toml profiles and `.cargo/config.toml` when they exist.

## Naming the goal and the toolchain

Read `rustc --version`, the target triple, and any existing profile or rustflags configuration. The step is done when the goal and toolchain are named.

## Picking the build mode

Use `cargo build` for debug, `cargo build --release` for optimized, `cargo check` for the fastest type check pass, and `--target` for cross builds. The step is done when the mode matches the goal.

## Tuning the profile

Profiles apply only in the workspace root Cargo.toml. Per-member profiles are ignored, so when a profile key seems to have no effect, check where it lives before anything else.

```toml
[profile.release]
opt-level = 3          # 0-3, "s" for size, "z" for aggressive size
debug = false          # true, 1 for line tables, 0 for none
lto = "thin"           # false, "thin", or true for fat LTO
codegen-units = 1      # 1 for maximum optimization, higher for faster compiles
panic = "abort"        # "unwind" (default) or "abort" for a smaller binary
strip = "symbols"      # "none", "debuginfo", or "symbols"
```

| Setting | Effect |
|---|---|
| `lto = true` | Fat LTO: best optimization, slowest link |
| `lto = "thin"` | Parallel LTO: near-fat optimization, faster link |
| `codegen-units = 1` | Best inlining, slower compile |
| `panic = "abort"` | Drops unwind tables; smaller binary, panics cannot be caught |
| `opt-level = "z"` | Aggressive size reduction |

The step is done when the recommended profile block is complete.

## Setting RUSTFLAGS for one build

`-C` flags apply per build. Persist them in `.cargo/config.toml` only when they should be permanent.

```bash
RUSTFLAGS="-C target-cpu=native" cargo build --release
```

```toml
# .cargo/config.toml
[build]
rustflags = ["-C", "target-cpu=native"]
```

`target-cpu=native` ties the binary to the build machine. For a binary that ships elsewhere, recommend a named microarchitecture level such as `x86-64-v3` instead, and warn that a native-tuned binary may fault on older CPUs. The step is done when the flags come with their persistence story.

## Seeing what the compiler produced

| Wanted output | Command |
|---|---|
| Annotated assembly for one function | `cargo install cargo-show-asm`, then `cargo asm --release 'myapp::module::function'` |
| Whole-crate assembly | `rustc --emit=asm -C opt-level=3 src/lib.rs` (`.s` assembly) |
| Mid-level IR | `rustc --emit=mir -C opt-level=3 src/lib.rs` (MIR text) |
| Low-level IR | `rustc --emit=llvm-ir -C opt-level=3 src/lib.rs` (LLVM IR) |

The step is done when the command produces the requested representation. When rustc writes an `--emit` artifact somewhere unexpected, look next to the input or under `target/`; for locating a single function, `cargo-show-asm` is the easier path.

## When generics bloat the binary or slow the build

Each concrete instantiation of a generic produces separate code (monomorphization). Measure with `cargo llvm-lines --release`, then mitigate with `dyn Trait` type erasure or a non-generic inner function that does the work behind a thin generic wrapper. The step is done when the measurement command and one mitigation are given.

## Slimming the binary for size

```toml
[profile.release]
opt-level = "z"
lto = true
codegen-units = 1
panic = "abort"
strip = "symbols"
```

Measure with `cargo bloat --release --crates` for per-crate size and `cargo bloat --release -n 20` for the largest functions. The step is done when the profile and the measurement commands are given.

## Reading a compilation error

| Error | Cause | Fix |
|---|---|---|
| `cannot find function in this scope` | Missing `use` or wrong module path | Import the item |
| `the trait X is not implemented for Y` | Missing impl or wrong generic bound | Implement the trait or fix the bound |
| `lifetime may not live long enough` | Borrow outlives its owner | Add or fix lifetime annotations |
| `cannot borrow as mutable` | Overlapping borrows | Restructure so borrows do not overlap |
| `use of moved value` | Value moved earlier | Borrow or clone |
| `mismatched types` | `String` vs `&str` and similar | Convert at the boundary |

Use `rustc --explain E0382` for the long form of any error code. The step is done when each error maps to a row. An error that matches no row gets reported verbatim with the closest class, never an invented fix.

## Verifying against the installed toolchain

Check every recommended flag with `rustc -C help`, `rustc --print target-list`, `rustc --print target-features --target <triple>`, and `rustc --print cfg`. No recommended flag goes out unverified: a flag the toolchain rejects gets dropped with the rejection noted.

## What you hand back

A recommendation report with the profile block, RUSTFLAGS, or inspection commands, each verified against the installed rustc. The full `-C` flag table, profile inheritance, per-package overrides, and linker configuration live in `references/rustflags-profiles.md`.
