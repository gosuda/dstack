---
name: cargo-workflows
description: 'Use when managing Cargo workspaces, feature flags, build scripts, CI caching, dependency auditing, or Cargo.lock with Rust.'
---

# Cargo workflows

You keep the Cargo side of a Rust project honest: workspaces that resolve, features that stay additive, build scripts that rerun only when inputs change, CI caches that actually hit, test runs under nextest, audits with no surprises, and a lockfile that matches what was intended. You write only local files the user names (`Cargo.toml`, `build.rs`, `Cargo.lock`, CI workflow files, report files), which rollback covers through `git checkout --`, `git reset`, or `rm` for new reports. Nothing here mutates anything remote. The job is done when the requested workflow builds or runs cleanly, or when the failing command and its cause are reported.

What you need before starting:

- Project path, required: the workspace root or member crate.
- Task, required: workspace setup, feature flags, build script, CI caching, `cargo nextest`, dependency audit, or `Cargo.lock` management.
- Rust version, optional: defaults to 1.99.1 with edition 2024.
- Target crate or feature names, optional: used for scoped builds, tests, and updates.
- CI platform, optional: GitHub Actions, GitLab CI, or local runner.

## Finding the toolchain and the workspace root

Run `rustc --version` and `cargo --version`, then locate the workspace root by finding the `Cargo.toml` that holds `[workspace]` or the root package. This step is done when the toolchain version and the workspace root are known.

## Setting up workspaces and feature flags

For workspace setup, create or edit the root `Cargo.toml` with `[workspace]`, `members`, `resolver = "2"`, `[workspace.dependencies]`, and `[workspace.package]`, and have members inherit with `version.workspace = true` and `edition.workspace = true`. Pattern details live in `references/workspace-patterns.md`. This step is done when `cargo check --workspace` succeeds. When the workspace will not build, check the `members` paths, the resolver, and missing `Cargo.toml` files, fix, and rerun.

For feature flags, configure `[features]` in the member `Cargo.toml`, keep features additive, use `dep:optional_dep` syntax for optional dependencies, and set `resolver = "2"`. Verify with `cargo check --no-default-features` and `cargo check --all-features`. This step is done when the requested feature combinations build cleanly. When feature unification leaks across the workspace, confirm `resolver = "2"`, split dev and prod feature edges, and inspect with `cargo tree -e features`.

## Writing build scripts that rerun only when they should

Add or edit `build.rs` at the crate root, emitting `cargo:rerun-if-changed=...`, `cargo:rustc-link-lib`, `cargo:rustc-link-search`, `cargo:rustc-cfg`, `cargo:rustc-env`, and `cargo:warning` directives. This step is done when `cargo build` reruns the script only when inputs change and the crate links or generates correctly. When the script reruns too often, add a `cargo:rerun-if-changed` line for every input file and environment variable.

## Caching CI and running nextest

For CI caching, configure `Swatinem/rust-cache@v2` or `actions/cache@v6` (Node 24 runtime; self-hosted runners need 2.327.1 or newer) to cache `~/.cargo/registry` and `target/`, and set `[profile.release] incremental = false` when release builds must stay deterministic. This step is done when CI logs show cache hits and build times are stable. On cache misses, verify the cache keys include `Cargo.lock` and that both `target/` and `~/.cargo` are restored.

For test execution, install `cargo-nextest 0.9.150` and run `cargo nextest run`, adding a `nextest.toml` with profiles for CI and local runs. This step is done when the tests pass under the chosen profile.

## Auditing dependencies and managing the lockfile

For dependency auditing, run `cargo audit` from `cargo-audit 0.22.2`, `cargo deny check` from `cargo-deny 0.20.2`, or `cargo machete`, with `deny.toml` configured for licenses, duplicate versions, and banned crates. This step is done when the tool reports no blocking findings or names each one. When an audit blocks the build, address the advisory, add a rationale to `deny.toml`, or switch to an allowed license.

For lock management, keep `Cargo.lock` in version control for applications and binaries and omit it for libraries, using `cargo generate-lockfile`, `cargo update`, and `cargo update -p <crate> --precise <version>`. This step is done when the lockfile matches the intended dependency versions. When an update touches unexpected crates, preview with `cargo update --dry-run` and scope with `cargo update -p <crate>`.

For one-off commands, run the matching `cargo build`, `cargo test`, `cargo tree`, `cargo expand`, or `cargo package` invocation for the requested crate and features. This step is done when the command output confirms the requested state.

## Diagnosing the real paths before blaming the build

Record the effective Cargo configuration and environment before diagnosing build placement. When resource errors name a different filesystem from the expected target directory, inspect the actual intermediate, target, temporary, and wrapper-owned paths supported by the installed Cargo and tool versions. Diagnose capacity and inode exhaustion separately. Redirect only the implicated run-owned paths and never disable a wrapper without evidence it preserves the failing environment. Never delete another user's or another run's caches. For cross-crate signature changes, enumerate reverse consumers, tests, feature combinations, and target-gated callers, since owner-crate success alone never establishes workspace compatibility. For new-warning attribution, compare complete diagnostics from matched revisions, toolchains, features, targets, and lint settings without mutating the tree under validation. Compare diagnostic identity and meaning despite shifted locations, and include affected callers, macros, and generated code rather than only textual hits in touched files.

## What you hand back

- A configured `Cargo.toml`, workspace, `build.rs`, or CI file matching the task.
- A `Cargo.lock` when needed, with deterministic dependency versions.
- A `nextest.toml` or `deny.toml` configuration when requested.
- A chat report naming the commands run and any remaining advisories or cache metrics.
