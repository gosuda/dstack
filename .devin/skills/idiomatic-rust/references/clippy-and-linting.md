# Clippy and linting discipline

Clippy provides static analysis beyond standard compiler diagnostics, identifying performance hazards, non-idiomatic constructs, redundant allocations, and subtle concurrency or safety bugs.

Verify that Clippy is installed for the active toolchain:

```shell
cargo clippy -V
```

A successful version query confirms the component is present, not that the codebase passes its lints. If the component is missing from your toolchain, install it:

```shell
rustup component add clippy
```

Official reference documentation is available at the [Clippy Usage Guide](https://doc.rust-lang.org/clippy/usage.html).

## Standard Clippy invocations

Prefer the repository's native verification gate (e.g., `cargo xtask lint`, `just lint`, or project-specific CI check scripts) whenever available to exercise the exact targets and feature flags tested in continuous integration.

When invoking Clippy directly across a workspace, the fallback command must include `--workspace` to ensure all workspace members are inspected:

```shell
cargo clippy --workspace --all-targets --locked -- -D warnings
```

- `--workspace`: checks every member package in the workspace. Invoking Clippy in a workspace root without `--workspace` only checks the root package or default workspace members.
- `--all-targets`: checks library targets, binaries, tests, benchmarks, and examples.
- `--locked`: asserts that `Cargo.lock` matches manifest requirements without modification.
- `-D warnings`: elevates all warnings to fatal compiler errors.

Feature flag considerations:
- Use `--all-features` only when all feature flags across the workspace are mutually compatible. Do not assume `--all-features` selects every workspace member by itself; it enables all features for selected packages.
- If workspace crates contain mutually exclusive features or platform-specific feature combinations, run Clippy against explicitly supported target and feature combinations rather than a blanket `--all-features`.

Optional additions for stricter verification:

- `-- -W clippy::pedantic`: enables opinionated style, documentation, and structural lints.
- `-- -W clippy::nursery`: checks experimental lints under active development.
- Automation: integrate the repo-native gate into CI pipelines, `xtask`, Justfile, or Makefile recipes.

## Critical Clippy lints

| Lint | Category | Rationale | Documentation |
| --- | --- | --- | --- |
| `redundant_clone` | Perf / Nursery | Detects unnecessary `.clone()` operations when borrowed references or ownership transfer suffice. | [redundant_clone](https://rust-lang.github.io/rust-clippy/master/#redundant_clone) |
| `needless_borrow` | Style | Detects redundant reference operators (`&`) where deref coercion or borrowing is already active. | [needless_borrow](https://rust-lang.github.io/rust-clippy/master/#needless_borrow) |
| `map_unwrap_or` / `unnecessary_map_or` | Style / Complexity | Replaces multi-step `.map(...).unwrap_or(...)` chains with direct `.map_or(...)` or pattern matching. | [map_unwrap_or](https://rust-lang.github.io/rust-clippy/master/#map_unwrap_or), [unnecessary_map_or](https://rust-lang.github.io/rust-clippy/master/#unnecessary_map_or) |
| `manual_ok_or` | Style | Suggests `.ok_or()` or `.ok_or_else()` instead of verbose `match` blocks on `Option`. | [manual_ok_or](https://rust-lang.github.io/rust-clippy/master/#manual_ok_or) |
| `large_enum_variant` | Perf | Warns when a single variant inflates the memory footprint of an enum. Suggests heap-indirection via `Box`. | [large_enum_variant](https://rust-lang.github.io/rust-clippy/master/#large_enum_variant) |
| `unnecessary_wraps` | Pedantic | Detects functions returning `Option` or `Result` where every exit branch unconditionally returns `Some` or `Ok`. | [unnecessary_wraps](https://rust-lang.github.io/rust-clippy/master/#unnecessary_wraps) |
| `clone_on_copy` | Complexity | Flags `.clone()` calls on types that implement `Copy`, where copying occurs implicitly. | [clone_on_copy](https://rust-lang.github.io/rust-clippy/master/#clone_on_copy) |
| `needless_collect` | Perf | Prevents eagerly collecting an iterator into an allocated collection (`Vec`) when intermediate consumption suffices. | [needless_collect](https://rust-lang.github.io/rust-clippy/master/#needless_collect) |
| `undocumented_unsafe_blocks` | Restriction | Enforces that every `unsafe` block is preceded by a `// SAFETY:` comment justifying why invariants are upheld. | [undocumented_unsafe_blocks](https://rust-lang.github.io/rust-clippy/master/#undocumented_unsafe_blocks) |
| `missing_safety_doc` | Style | Enforces explicit `# Safety` sections in rustdoc comments on public `unsafe fn` items. | [missing_safety_doc](https://rust-lang.github.io/rust-clippy/master/#missing_safety_doc) |

## Warning suppression discipline

Do not silence lints indiscriminately. Suppress a lint only when:

1. The underlying architectural invariant or tradeoff is understood and documented.
2. The suppression is scoped to the smallest possible item or block rather than a whole module or crate.
3. You prefer `#[expect(clippy::lint_name)]` over `#[allow(clippy::lint_name)]`. Unlike `allow`, `expect` emits a warning when the lint no longer fires, preventing obsolete suppressions from surviving unnoticed.

### Tradeoff example: large enum variants

When pattern-matching dispatch throughput outweighs stack allocation size, document the decision directly on the type:

```rust
#[expect(clippy::large_enum_variant, reason = "match performance outweighs variant footprint")]
enum Message {
    Code(u8),
    Content([u8; 1024]),
}
```

When memory efficiency is preferred, introduce heap indirection with `Box`. The variant size drops to pointer width and no suppression is needed:

```rust
enum Message {
    Code(u8),
    Content(Box<[u8; 1024]>),
}
```

### Safety documentation discipline

When `clippy::undocumented_unsafe_blocks` is enabled, every `unsafe` block must state its safety justification in a preceding `// SAFETY:` comment:

```rust
let value: u32 = 42;
let ptr: *const u32 = &value;

// SAFETY: ptr is derived from an initialized, live local variable on the current stack frame, properly aligned and non-null.
let dereferenced = unsafe { *ptr };
```

### Managing false positives

When Clippy raises a false positive:

1. Attempt to refactor the code to eliminate the ambiguity or anti-pattern cleanly.
2. If refactoring introduces unnecessary complexity, apply a localized `#[expect(clippy::lint_name, reason = "...")]` with a concise explanation.
3. Avoid crate-wide or module-wide `#![allow(...)]` declarations. Never use generic rationales like "framework architecture" to justify blanket lint suppressions; every suppression must cite a concrete, verified technical constraint and be scoped as narrowly as possible.

## Workspace and package lint configuration

Declare lints centrally in `Cargo.toml`. When configuring lints, priority determines precedence (higher numbers take precedence over lower numbers).

Lint groups (such as `all`, `pedantic`, or `nursery`) must have a lower priority than individual lint overrides so that specific rules can override group defaults. By convention, assign lower or negative priorities to lint groups (e.g., `priority = -1`) and higher priorities to specific overrides (e.g., `priority = 1` or default `0`).

Package configuration:

```toml
[lints.rust]
future_incompatible = "warn"
nonstandard_style = "deny"

[lints.clippy]
all = { level = "deny", priority = -1 }
pedantic = { level = "warn", priority = -2 }
redundant_clone = { level = "deny", priority = 1 }
undocumented_unsafe_blocks = { level = "deny", priority = 1 }
manual_while_let_some = { level = "deny", priority = 1 }
```

Workspace configuration:

```toml
[workspace.lints.rust]
future_incompatible = "warn"
nonstandard_style = "deny"

[workspace.lints.clippy]
all = { level = "deny", priority = -1 }
pedantic = { level = "warn", priority = -2 }
redundant_clone = { level = "deny", priority = 1 }
undocumented_unsafe_blocks = { level = "deny", priority = 1 }
manual_while_let_some = { level = "deny", priority = 1 }
```

Workspace members then inherit the shared configuration:

```toml
[lints]
workspace = true
```
