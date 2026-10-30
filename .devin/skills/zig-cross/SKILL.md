---
name: zig-cross
description: 'Use when building Zig or C for another platform with Zig: target triples, -mcpu features, zig cc cross-compiles, multi-target build.zig, bare-metal Cortex-M, or WebAssembly. Not GCC.'
---

# Zig cross-compilation

You build a binary for a different OS or CPU than the build host, from Zig or C sources, using Zig as the cross toolchain. You work read-only: you hand the user the triple, the CPU choice, and the exact commands or `build.zig` loop in chat, and they run them. Scratch cross builds go in a scratch directory, never into the project's outputs. You are done when the triple is confirmed in `zig targets` on the installed Zig and a scratch build for that triple produces a file whose `file` line matches the target platform.

## Start with these facts

Ask for anything missing rather than guessing it:

- Zig version from `zig version`. The commands below ran on Zig 0.14.1.
- Target platform: OS or bare metal, architecture, ABI, and the exact CPU when known.
- Sources: Zig, C, or both.
- Linker script, when the target is freestanding bare metal.
- macOS SDK path, when targeting macOS with anything beyond a plain executable that needs system frameworks.

## Pick the triple from what Zig actually supports

Compose the triple as `<arch>-<os>-<abi>` using only names from the lists `zig targets` prints. That output is a ZON document: `.arch`, `.os`, and `.abi` hold the legal names, and `.libc` lists the triples with a bundled libc. Common choices:

`x86_64-linux-gnu`, `x86_64-linux-musl` (static), `aarch64-linux-gnu`, `aarch64-linux-musl`, `arm-linux-gnueabihf` (32-bit ARM with FPU), `x86_64-windows-gnu`, `aarch64-macos-none`, `x86_64-macos-none`, `wasm32-freestanding`, `wasm32-wasi`, `thumb-freestanding-eabihf` (Cortex-M with FPU; the CPU selects the M variant), `riscv32-freestanding-none`.

The triple counts only if it appears in `zig targets`. A fuller list lives in `references/zig-target-triples.md`.

## Build Zig for the target

- Direct: `zig build-exe src/main.zig -target aarch64-linux-gnu -O ReleaseFast`, or through the build system with `zig build -Dtarget=aarch64-linux-gnu -Doptimize=ReleaseFast`.
- Windows from Linux or macOS: `-target x86_64-windows-gnu` produces a `.exe`.
- macOS from Linux: `-target aarch64-macos-none` links a plain executable on its own; code that needs Apple frameworks needs the macOS SDK passed via `--sysroot` and framework paths.

The build counts when `file` reports the target's executable format.

## Choose the CPU deliberately

`-mcpu native` detects the build host and is wrong for a cross build. `-mcpu baseline` is the portable floor for the architecture. Add or remove features with `+` and `-`:

- `-mcpu x86_64+avx2+bmi2`, `-mcpu x86_64_v3`
- `-mcpu cortex_a72` (Raspberry Pi 4)
- `-mcpu cortex_m4+vfp4`
- `-mcpu neoverse_n1`, `-mcpu apple_m1`

CPU and feature names are listed per architecture under `.cpus` in `zig targets`; the choice counts only if it appears there. If Zig prints `is not a recognized feature`, that is distribution noise (Zig built against a different LLVM), not failure: the build still completes, so report it and move on.

## Cross-compile C with `zig cc`

`zig cc` needs no system cross toolchain:

- `zig cc -target aarch64-linux-gnu -O2 -o myapp-arm64 main.c`
- `zig cc -target x86_64-windows-gnu main.c -o myapp.exe`
- `zig cc -target x86_64-linux-musl -static main.c -o myapp-static`

In a Makefile, define one `CC` per platform, for example `CC_LINUX_ARM64 = zig cc -target aarch64-linux-gnu`. The artifact counts when it matches the target format.

## Serve every target from one `build.zig`

Loop over `std.Target.Query` values, resolve each with `b.resolveTargetQuery(t)`, and give each executable a distinct name:

```zig
const targets = [_]std.Target.Query{
    .{ .cpu_arch = .x86_64, .os_tag = .linux, .abi = .gnu },
    .{ .cpu_arch = .aarch64, .os_tag = .linux, .abi = .gnu },
    .{ .cpu_arch = .x86_64, .os_tag = .windows, .abi = .gnu },
    .{ .cpu_arch = .aarch64, .os_tag = .macos },
};
for (targets) |t| {
    const exe = b.addExecutable(.{
        .name = b.fmt("myapp-{s}-{s}", .{ @tagName(t.cpu_arch.?), @tagName(t.os_tag.?) }),
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = b.resolveTargetQuery(t),
            .optimize = .ReleaseFast,
        }),
    });
    b.installArtifact(exe);
}
```

This counts when `zig-out/bin` holds one artifact per target.

## Bare-metal targets need a script and an entry point

`zig build-exe src/main.zig -target thumb-freestanding-eabihf -mcpu cortex_m4+vfp4 -O ReleaseSmall -T linker.ld`. The root file supplies `pub fn panic(msg: []const u8, _: ?*std.builtin.StackTrace, _: ?usize) noreturn` and an exported entry point named in the linker script, such as `export fn _start() void`. Freestanding code cannot use std facilities that need an OS (threads, files, `std.debug.print`); when the compiler reports `Unsupported operating system freestanding`, remove the offending std call from the freestanding path. The result counts when the ELF links with the script's entry symbol.

## WebAssembly targets

- Browser: `zig build-exe src/main.zig -target wasm32-freestanding -O ReleaseSmall --export=init --export=update -fno-entry`, where each exported function is `export fn`.
- WASI: `zig build-exe src/main.zig -target wasm32-wasi -O ReleaseSafe` produces `main.wasm` for a WASI runtime.

Either counts when `file` reports a WebAssembly module.

## When the toolchain complains

- An `available architectures:` listing after `-target` means the arch name is not one Zig uses. `thumbv7em` is not an arch; `thumb` plus `-mcpu cortex_m4` is.
- `Unsupported operating system freestanding` means an std call needs an OS. Remove it from the freestanding path.
- A macOS build that needs frameworks gets the SDK via `--sysroot` and framework paths; a plain executable needs nothing.
- A build that genuinely needs a system cross toolchain (GCC triplets, sysroots, QEMU) is outside this skill. The Rust equivalent is `rust-cross`. Naming that skill never runs it.

## What you hand back

A chat report with the triple and CPU, the build command or `build.zig` loop, the bare-metal or WebAssembly specifics when they apply, and the `file` line from the scratch build proving the target format.
