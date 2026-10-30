# RUSTFLAGS and Cargo profiles reference

RUSTFLAGS pass one-off codegen choices to rustc; Cargo profiles record the repeatable ones in `Cargo.toml`. Keep anything the whole team must share in a profile, and reach for RUSTFLAGS for local experiments and target-specific builds.

## RUSTFLAGS reference

### Codegen flags (-C)

| Flag | Values | Effect |
|------|--------|--------|
| `-C opt-level=N` | `0`-`3`, `s`, `z` | Optimization level |
| `-C target-cpu=X` | `native`, `x86-64`, `x86-64-v3`... | Target CPU |
| `-C target-feature=+X` | `+avx2`, `+bmi2`, `+aes`... | Enable CPU features |
| `-C lto=X` | `off`, `thin`, `fat` | LTO mode |
| `-C codegen-units=N` | `1`-`N` | Parallel codegen units |
| `-C panic=X` | `unwind`, `abort` | Panic strategy |
| `-C debuginfo=N` | `0`, `1`, `2` | Debug info level |
| `-C strip=X` | `none`, `debuginfo`, `symbols` | Strip output |
| `-C link-arg=X` | any linker flag | Pass flag to linker |
| `-C linker=X` | program name or path | Linker driver to invoke |
| `-C linker-flavor=X` | `gcc`, `ld`, `lld-link`... | Linker interface flavor |
| `-C overflow-checks=X` | `yes`, `no` | Integer overflow checks |
| `-C force-frame-pointers=X` | `yes`, `no` | Frame pointer emission |
| `-C embed-bitcode=X` | `yes`, `no` | Embed LLVM bitcode (for LTO) |
| `-C relocation-model=X` | `static`, `pic`, `pie` | Relocation model |
| `-C code-model=X` | `tiny`, `small`, `medium`, `large`, `kernel` | Code model |

### Emit flags (--emit)

```bash
# Multiple outputs
rustc --emit=asm,llvm-ir,mir src/lib.rs

# In cargo:
RUSTFLAGS="--emit=asm" cargo build --release
```

| `--emit` value | Output |
|----------------|--------|
| `asm` | Native assembly `.s` |
| `llvm-ir` | LLVM IR `.ll` |
| `llvm-bc` | LLVM bitcode `.bc` |
| `mir` | MIR text `.mir` |
| `metadata` | `.rmeta` crate metadata |
| `link` | Final linked artifact (default) |
| `dep-info` | `.d` Makefile dependency |

## Cargo profile options

```toml
[profile.release]
# Optimization
opt-level = 3                    # 0|1|2|3|"s"|"z"
lto = "thin"                     # false|"thin"|true|"fat"
codegen-units = 1                # integer

# Debug information
debug = 0                        # false|0|"line-directives-only"|"line-tables-only"|1|true|2|"full"
debug-assertions = false         # bool
split-debuginfo = "off"          # "off"|"packed"|"unpacked"

# Runtime behavior
panic = "abort"                  # "unwind"|"abort"
overflow-checks = false          # bool
rpath = false                    # bool

# Output
strip = "none"                   # "none"|"debuginfo"|"symbols"
incremental = false              # bool

# Build performance
build-override = {}              # Override for build scripts
```

## Profile inheritance

```toml
# Custom profiles must inherit from dev or release
[profile.production]
inherits = "release"
lto = true
codegen-units = 1
panic = "abort"
strip = "symbols"

[profile.staging]
inherits = "release"
debug = 1
strip = "none"
```

## Per-package profile overrides

```toml
# Override profile for specific dependencies
[profile.release.package.serde]
opt-level = 3

[profile.dev.package."*"]
opt-level = 1    # Optimize all deps even in dev mode
```

Pick one starting point below and change a single knob at a time; each profile names the situation it fits.

## Common configurations

### Maximum performance

Top speed for release binaries; pair with a fixed target CPU for the deployment baseline.

```toml
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
panic = "abort"
```

```toml
# .cargo/config.toml
[build]
rustflags = ["-C", "target-cpu=native"]
```

### Minimum binary size

Small distribution artifacts. Pairs with a fixed target CPU for the deployment baseline.

```toml
[profile.release]
opt-level = "z"
lto = true
codegen-units = 1
panic = "abort"
strip = "symbols"
```

### Fast CI builds

Compiles your own code fast while still optimizing dependencies once. Use for day-to-day development and CI test runs.

```toml
[profile.dev]
opt-level = 0
incremental = true

[profile.dev.package."*"]
opt-level = 1    # Compiled deps faster than test code
```

## Linker configuration

The chosen linker must be installed. The config shows mold, noted as the fastest linker, and lld.

```toml
# .cargo/config.toml

# Use mold (fastest linker, must be installed)
[target.x86_64-unknown-linux-gnu]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=mold"]

# Use lld
[target.x86_64-unknown-linux-gnu]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=lld"]
```

## x86-64 microarchitecture levels

Broadwell and newer cover most cloud VMs; Cascade Lake and newer add AVX-512. Prefer named CPUs only when the fleet is known.

```bash
# Broadwell and newer (most cloud VMs)
RUSTFLAGS="-C target-cpu=x86-64-v3" cargo build --release

# Cascade Lake and newer (AVX-512)
RUSTFLAGS="-C target-cpu=x86-64-v4" cargo build --release

# Specific CPUs
RUSTFLAGS="-C target-cpu=skylake" cargo build --release
RUSTFLAGS="-C target-cpu=znver3" cargo build --release  # AMD Zen3
```
