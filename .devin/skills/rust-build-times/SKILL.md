---
name: rust-build-times
description: 'Use when profiling slow Rust builds with cargo --timings, configuring sccache, selecting the Cranelift dev backend, splitting a workspace for parallelism, or tuning LTO and the linker.'
---

# Rust build times

Compile time is a measurement problem first. You profile before changing anything, apply one change at a time, and keep only measured wins.

This skill never reaches beyond the local project. It edits only the project's `Cargo.toml` and `.cargo/config.toml`, with version control as the rollback. Toolchain component and system package installs are reported as commands for the user, never executed. There is no remote mutation. The work is done when a baseline `cargo build --timings` report exists, each applied change is measured against it, and only measured wins remain in the configuration.

What you need before starting:

- The slow build command (required). Something like `cargo build`, `cargo test`, or `cargo build --release`.
- The workspace layout (required when it cannot be inferred). Single crate or workspace, member count, and dependency graph.
- The toolchain (required). Stable or nightly; the Cranelift backend needs nightly.
- The constraints (optional). CI environment, cache storage (local disk or S3), and whether runtime performance may regress.

## Measuring the baseline

Run `cargo build --timings` (add `--release` when release is the slow path) and read the HTML report for long serial chains, crates that dominate the timeline, and proc macro crates blocking downstream work. Run `cargo llvm-lines --release` to find monomorphization heavy functions. This step is done when the top offenders are named.

## Caching repeated builds with sccache

sccache wraps rustc and caches compiled artifacts locally or in S3:

```bash
export RUSTC_WRAPPER=sccache
sccache --show-stats
```

```toml
# .cargo/config.toml
[build]
rustc-wrapper = "sccache"
```

For CI, the S3 backend is configured through `SCCACHE_BUCKET` and `SCCACHE_REGION`. This step is done when `sccache --show-stats` reports hits on a rebuild. When it reports no hits, check that `RUSTC_WRAPPER` or `rustc-wrapper` is set in the right config file and that the cache directory is writable. When `--timings` produces no report, the Cargo is too old; record the toolchain version and fall back to per-crate timing from `cargo build -vv` output.

## Speeding dev builds with Cranelift

When nightly is allowed, select the Cranelift backend for dev builds. Cranelift compiles faster than LLVM and produces slower code, so it belongs in the dev profile only:

```toml
# .cargo/config.toml (nightly only)
[unstable]
codegen-backend = true

[profile.dev]
codegen-backend = "cranelift"
```

The component is `rustc-codegen-cranelift-preview` on the nightly toolchain; report the `rustup component add` command for the user to run. This step is done when the dev profile uses Cranelift and release stays on LLVM. When Cranelift rejects a crate (some intrinsics and SIMD paths are unsupported), keep that crate or profile on LLVM.

## Splitting the workspace for parallelism

One large crate compiles serially; independent crates compile in parallel. Break circular dependencies first, move proc macros into their own crate, and isolate frequently changed code so edits invalidate less. Inspect the graph with `cargo tree`. This step is done when the timing report shows parallel compilation where a serial chain ran before. When a split hits a dependency cycle, extract the shared types into a common crate both sides depend on.

## Tuning LTO per profile

LTO trades link time for runtime performance: `false` for dev, `"thin"` for most release builds, `true` (fat) only when runtime performance is measured to matter. `codegen-units = 1` maximizes optimization and serializes codegen:

```toml
[profile.release]
lto = "thin"

[profile.dev]
codegen-units = 16
```

This step is done when each profile carries the LTO setting its purpose needs.

## Switching to a faster linker

The link step often dominates large projects. mold is the fastest option on Linux; lld is the portable fast option. Both are selected through the clang driver:

```toml
# .cargo/config.toml
[target.x86_64-unknown-linux-gnu]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=mold"]   # or =lld
```

Report the system package install command for the user rather than running it. This step is done when the configured linker appears in the build log and link time drops.

## Applying the smaller wins

`debug = 1` in the dev profile emits line tables only; `split-debuginfo = "unpacked"` shrinks linker input on platforms that support it; `CARGO_INCREMENTAL=0` can win on clean CI builds. Each candidate is measured, not assumed.

## Keeping only what measures faster

Re-measure after every change. Compare each timing report against the baseline and keep only changes that measurably help this workload. A change that regresses the build gets reverted; the baseline report is the arbiter. Configuration edits already made remain in place, and the final report names the unmeasured or reverted changes.

## What you hand back

A measurement report with baseline timing, the named bottleneck crates, and per-change before and after numbers; plus the final `Cargo.toml` and `.cargo/config.toml` edits that survived measurement.
