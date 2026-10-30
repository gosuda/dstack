---
name: rust-cross
description: 'Use when building Rust binaries for a different target architecture or OS, using cross or cargo-zigbuild, configuring .cargo/config.toml, or targeting embedded bare-metal.'
---

# Rust cross-compilation

You get Rust building for a different CPU, OS, or ABI and prove the output matches. Triples, linkers, runners, and verification all live here.

Authority stays local. This skill edits `.cargo/config.toml`, `Cross.toml`, and `Cargo.toml`, installs `rustup` targets, and writes `target/` build directories (plus Docker images when `cross` is used). Rollback reverts the edited files, runs `rustup target remove <triple>` for targets it added, and removes build artifacts. Nothing mutates a remote. The work is done when the chosen target builds with the selected driver and the output matches the intended triple and linking mode.

What you need before starting:

- The target triple (required). CPU, vendor, OS, and ABI (for example `aarch64-unknown-linux-gnu` or `thumbv7em-none-eabihf`).
- The host tool state (required when it cannot be inferred). Installed `rustup` targets from `rustup target list --installed`.
- The cross driver (required). `cargo`, `cross`, `cargo-zigbuild`, or direct `rustc` with a system cross-linker.
- The C library and linker needs (optional). glibc, musl, MSVC, `zig cc`, or a system cross-linker.
- The embedded runner (optional for bare metal). Probe, emulator, or `qemu` command.

## Picking and installing the triple

Match CPU, vendor, OS, and ABI to the platform. Look the triple up in `references/cross-targets.md` when the platform is unfamiliar. Install it with `rustup target add <triple>` and confirm it in `rustup target list --installed`.

## Choosing the driver

Three routes cover the common cases:

- `cross build --target <triple>` for hermetic Docker based builds; add a `Cross.toml` when the image needs extra packages.
- `cargo zigbuild --target <triple>` to avoid a system cross-linker; this needs `cargo-zigbuild` and a Zig toolchain.
- `cargo build --target <triple>` with a linker set in `.cargo/config.toml` for direct builds.

The driver is settled when a sample command runs without linker errors. A GNU Windows target is not MSVC coverage. For `cargo-xwin`, check the installed driver interface and prerequisites first and get owner acceptance of the SDK/CRT license before any download.

## Configuring linker and runner

Add a `[target.<triple>]` section in `.cargo/config.toml` with `linker`, `runner`, and `rustflags` as needed. A static musl build sets `rustflags = ["-C", "target-feature=+crt-static"]`. Bare metal sets the default target and runner. Gate helper definitions and tests to their actual use-site configurations, and check that required tests stay selected instead of hiding failures with cfg or lint suppression.

## Verifying the artifact honestly

Build, then confirm with `file <binary>` or `readelf -h <binary>` (ELF machine type and linking mode; `file` or `objdump -f` for Windows or macOS targets). Record host, exact target and ABI, driver, feature set, native dependencies, and the level actually verified: type checking, linking, or execution. A cross check is not native filesystem or runtime proof. Report output locations from the effective Cargo configuration. When native execution is unavailable, keep that gap explicit. Never manufacture parity through a substitute target or quietly skip a failing platform fixture.

## When the build fails

| Signal | Response |
|---|---|
| Target not installed | Run `rustup target add <triple>` and retry |
| Linker not found | Install the system cross-linker or switch to `cargo-zigbuild` |
| `cross` fails on a C dependency | Add a `pre-build` step to `Cross.toml` for the target package |
| glibc version mismatch with `cargo-zigbuild` | Append the version to the triple, for example `aarch64-unknown-linux-gnu.2.17` |
| Embedded binary does not run | Verify runner, default target, memory layout, and probe or emulator configuration |

## What you hand back

A built artifact for the requested target; updated `.cargo/config.toml` and optionally `Cross.toml` or `Cargo.toml` profiles; and a short report with the build command, verification output, and any extra configuration.
