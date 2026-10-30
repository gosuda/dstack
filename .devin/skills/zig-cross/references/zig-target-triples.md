# Zig target triples and CPU names

Use this to pick a triple and CPU that your Zig accepts. Every entry below was read from `zig targets` on Zig 0.14.1 or produced by a scratch build on it. The list on your machine is authoritative. Re-check it with `zig targets` after a Zig upgrade.

## Triple format

A triple has the form `<arch>-<os>-<abi>`. Architectures include `x86_64`, `x86`, `aarch64`, `aarch64_be`, `arm`, `armeb`, `thumb`, `riscv32`, `riscv64`, `mips`, `mipsel`, `mips64`, `mips64el`, `powerpc64le`, `s390x`, `loongarch64`, `wasm32`, `wasm64`, `avr`, `bpfel`, and `bpfeb`. Operating systems include `linux`, `windows`, `macos`, `ios`, `freebsd`, `netbsd`, `openbsd`, `dragonfly`, `solaris`, `illumos`, `wasi`, `freestanding`, `uefi`, and `other`. ABIs include `none`, `gnu`, `gnueabi`, `gnueabihf`, `musl`, `musleabi`, `musleabihf`, `eabi`, `eabihf`, `msvc`, and `android`.

There is no `thumbv7m` or `thumbv7em` architecture. The architecture is `thumb`. The `-mcpu` value selects the Cortex-M core.

## Triples with a bundled libc

These triples appear under `.libc` in `zig targets`. They link without a system sysroot.

| Triple | Notes |
|---|---|
| `x86_64-linux-gnu` | glibc |
| `x86_64-linux-musl` | musl; `-static` gives a fully static binary |
| `x86_64-linux-gnux32` | glibc, x32 ABI |
| `x86-linux-gnu`, `x86-linux-musl` | 32-bit x86 |
| `aarch64-linux-gnu`, `aarch64-linux-musl` | 64-bit ARM |
| `aarch64_be-linux-gnu`, `aarch64_be-linux-musl` | big-endian |
| `arm-linux-gnueabi`, `arm-linux-gnueabihf` | 32-bit ARM, soft and hard float |
| `arm-linux-musleabi`, `arm-linux-musleabihf` | 32-bit ARM, musl |
| `riscv32-linux-gnu`, `riscv32-linux-musl`, `riscv64-linux-gnu`, `riscv64-linux-musl` | RISC-V |
| `mips-linux-gnueabi`, `mipsel-linux-gnueabihf`, and the `musl` variants | MIPS |
| `powerpc64le-linux-gnu`, `powerpc64le-linux-musl` | POWER little-endian |
| `s390x-linux-gnu`, `s390x-linux-musl` | IBM Z |
| `x86_64-windows-gnu`, `x86-windows-gnu`, `aarch64-windows-gnu` | MinGW ABI |
| `x86_64-macos-none`, `aarch64-macos-none` | macOS |
| `wasm32-wasi-musl` | WASI (also reachable as `wasm32-wasi`) |

## Freestanding and WebAssembly triples built in this pass

| Triple | Notes |
|---|---|
| `thumb-freestanding-eabihf` with `-mcpu cortex_m4+vfp4` | Cortex-M4 with FPU |
| `thumb-freestanding-eabi` | Cortex-M without FPU; select the core with `-mcpu` |
| `riscv32-freestanding-none` | RISC-V 32-bit bare metal |
| `wasm32-freestanding` | Browser module; `-fno-entry` and `--export=` per function |
| `wasm32-wasi` | WASI runtime |

## CPU names present under `.cpus`

x86_64 carries `baseline`, `x86_64`, `x86_64_v2`, `x86_64_v3`, `x86_64_v4`, plus named microarchitectures. AArch64 carries `baseline`, `cortex_a53`, `cortex_a72`, `cortex_a76`, `neoverse_n1`, `apple_m1`, and `apple_m2`. ARM and Thumb carry `cortex_m0`, `cortex_m0plus`, `cortex_m3`, `cortex_m4`, `cortex_m7`, and `cortex_m33`. RISC-V carries `baseline`, `generic_rv32`, `generic_rv64`, and `sifive_u74`.

Append `+feature` or `-feature` to adjust features: `x86_64+avx2+bmi2` or `cortex_m4+vfp4`. Feature names are listed per CPU in the same `.cpus` section.
