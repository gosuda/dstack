# Coding styles and idioms

## Borrowing versus cloning

Rust's ownership model favors references (`&T`) over cloning (`T.clone()`). Borrowing inspects or uses values without allocating or duplicating backing memory.

### Legitimate uses of clone

* Modifying a copy while preserving the original value for snapshots or parallel updates.
* Incrementing handle counts on reference-counted pointers such as `Arc<T>` or `Rc<T>`.
* Transferring isolated state across thread boundaries when sharing references is prohibited.
* Supplying owned data to external interfaces that take `T` by value.

### Cloning traps

* Avoid `.map(|x| x.clone())`. Use `.cloned()` or `.copied()` directly on iterators over references.
* Cloning large collections like `Vec<T>` or `HashMap<K, V>` allocates heap memory and copies every element.
* When a function requires ownership, declare `fn process(item: Item)` rather than taking `&Item` and cloning inside. Let callers choose whether to move an existing value or clone explicitly.
* Accept `&[T]` rather than `&Vec<T>`, `&str` rather than `&String`, and `&T` rather than passing owned `T` to read-only callers.

```rust
fn process(name: &str) {
    println!("{name}");
}

let user = String::from("ferris");
process(&user);
```

```rust
fn consume_name(name: String) {
    println!("{name}");
}

let user = String::from("ferris");
consume_name(user);
```

## Value semantics and the copy trait

Not all types belong behind references. Small types whose bits can be duplicated cheaply should be passed by value. Rust exposes this through the `Copy` trait.

### When to implement copy

* The type consists entirely of fields that implement `Copy`.
* The type represents plain data without owned heap resources (no `String`, `Vec`, or file handles).
* Passing small `Copy` types by value is a heuristic rather than an absolute rule. Whether a value fits in registers or spills to stack memory depends on target architecture calling conventions, available registers, and call-site contexts; measure hot paths rather than assuming 16–24 byte values never spill.
* `Copy` combined with `Iterator` is a design hazard for mutable progression, not a compiler prohibition. Iterators track mutable progression state via `.next(&mut self)`. Deriving or implementing `Copy` on an iterator allows implicit duplication of progression state, causing distinct bindings to diverge or repeat items unexpectedly. Types representing collections should implement `IntoIterator` yielding a dedicated non-`Copy` iterator.

Arrays (`[T; N]`) provide inline storage within their enclosing allocation (on the stack if local, or on the heap if enclosed by a `Box`, `Vec`, or heap-allocated struct). Copying a large array duplicates all inline elements byte-for-byte; pass large arrays by slice (`&[T]`) to avoid duplicating element storage. For memory layout considerations, see [Performance Mindset](./performance.md).

### Primitive sizes

| Type | Size |
| :--- | :--- |
| `i8`, `u8`, `bool` | 1 byte |
| `i16`, `u16` | 2 bytes |
| `i32`, `u32`, `f32`, `char` | 4 bytes |
| `i64`, `u64`, `f64` | 8 bytes |
| `isize`, `usize` | Architecture pointer width |
| `i128`, `u128` | 16 bytes |

```rust
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Point {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Direction {
    North,
    South,
    East,
    West,
}
```

Never derive `Copy` on types containing owned heap pointers or resources:

```rust
#[derive(Debug, Clone)]
pub struct UserProfile {
    pub id: u64,
    pub username: String,
}
```

## Flow control with option and result

Rust provides expressive constructs for unwrapping and branching on `Option<T>` and `Result<T, E>`.

### Choosing pattern matching constructs

* `let ... else` flattens guard clauses when the failure case diverges via `return`, `break`, or `continue`. It keeps happy-path execution at the top indentation level.
* `match` evaluates multiple branches, handles compound patterns, or maps inner values across different types.
* `if let` handles a single variant when the alternate branch executes non-diverging logic.
* The `?` operator propagates errors to the caller when no local transformation or error handling is needed.

```rust
fn active_port(config: &ServerConfig) -> Result<u16, ConfigError> {
    let Some(port) = config.port else {
        return Err(ConfigError::PortMissing);
    };

    if port < 1024 {
        return Err(ConfigError::PrivilegedPort(port));
    }

    Ok(port)
}
```

```rust
fn handle_event(event: Option<Event>) -> StepAction {
    match event {
        Some(Event::Terminate) => StepAction::Halt,
        Some(Event::Message(payload)) if payload.is_empty() => StepAction::Ignore,
        Some(Event::Message(payload)) => StepAction::Process(payload),
        None => StepAction::Wait,
    }
}
```

Avoid redundant pattern matches when dedicated combinators exist:

```rust
let opt: Option<u32> = result.ok();
let res: Result<u32, &'static str> = opt.ok_or("missing value");
```

Avoid calling `.unwrap()` or `.expect()` in non-test code where errors represent normal external conditions (I/O, network, user input). Reserve `.expect()` for invariants guaranteed by earlier program logic, with an assertion message stating why the invariant holds.

## Lazy evaluation and allocation prevention

Eager fallback methods (`unwrap_or`, `ok_or`, `map_or`) evaluate their arguments unconditionally. When the fallback allocates memory or executes non-trivial logic, prefer lazy variants (`unwrap_or_else`, `ok_or_else`, `map_or_else`) or `unwrap_or_default`.

Calling `unwrap_or` evaluates the argument eagerly, allocating on every invocation:

```rust
let config_entry: Option<String> = None;
let value = config_entry.clone().unwrap_or(String::from("default"));
```

Calling `unwrap_or_else` defers execution, allocating only when the fallback is needed:

```rust
let config_entry: Option<String> = None;
let value = config_entry.unwrap_or_else(|| String::from("default"));
```

To inspect an error before propagating it, chain `inspect_err`:

```rust
let bytes = std::fs::read("config.toml")
    .inspect_err(|err| eprintln!("Failed to read configuration: {err}"))?;
```

## Iterators and loops

Rust provides both imperative `for` loops and lazy iterator pipelines.

### Selecting iterators or loops

* Prefer `for` loops when execution requires early exits (`break`, `continue`, `return`), complex side effects across iterations, or imperative mutation that becomes convoluted inside iterator closures.
* Prefer iterator pipelines for declarative transformations, composing multiple steps (`filter`, `map`, `enumerate`), collection aggregation (`sum`, `collect`), and windowed inspection (`windows`, `chunks`).

```rust
let even_squares_sum: u64 = (0..=10)
    .filter(|&x| x % 2 == 0)
    .map(|x| x * x)
    .sum();
```

```rust
fn find_prefix<'a>(lines: &'a [&'a str], prefix: &str) -> Option<&'a str> {
    for line in lines {
        if line.starts_with(prefix) {
            return Some(line);
        }
    }
    None
}
```

### Iterator rules

* Iterators are lazy: adapters do not execute work until driven by a terminal consumer (`collect`, `sum`, `for_each`, or a loop).
* Avoid intermediate allocations: do not `.collect::<Vec<_>>()` simply to iterate over the collected result immediately afterward. Chain iterator adapters directly.
* Prefer `.iter()` when inspecting elements, `.iter_mut()` for in-place modifications, and `.into_iter()` only when taking ownership of the collection.
* `Copy` combined with `Iterator` is a design hazard for mutable progression, not a compiler prohibition. Iterators track mutable progression state via `.next(&mut self)`. Copying an iterator duplicates progression state, causing distinct bindings to diverge or repeat elements silently. Implement `IntoIterator` on collections instead, returning a dedicated non-`Copy` iterator.
* Prefer `.sum()` over `.fold(0, |acc, x| acc + x)` because specialized adapters expose optimization hints to the compiler.

## Code structure and comments

Types, naming, and module decomposition carry the primary narrative of a codebase. Code should express intent directly through type signatures and focused function scopes rather than narrative commentary.

### Legitimate comments

* Every `unsafe` block requires an explicit `// SAFETY:` comment proving that callers or preconditions uphold the compiler's safety requirements and memory safety invariants.
* Public API items document contracts, preconditions, and return guarantees via doc comments (`///`).

```rust
// SAFETY: The caller guarantees `src` and `dst` are valid for reads and writes
// of `count` elements, properly aligned, and do not overlap.
unsafe {
    std::ptr::copy_nonoverlapping(src, dst, count);
}
```

### Decomposing functions over commentary

Long functions with sequential narrative comments explaining distinct steps indicate missing modular boundaries. Extracting well-named functions clarifies responsibilities and allows independent invariant testing:

```rust
pub fn parse_header(line: &str) -> Result<(&str, &str), HeaderError> {
    let (key, value) = line.split_once(':').ok_or(HeaderError::MissingDelimiter)?;
    let key = key.trim();
    let value = value.trim();
    if key.is_empty() {
        return Err(HeaderError::EmptyKey);
    }
    Ok((key, value))
}
```

Tests should verify real domain invariants and boundary conditions rather than trivial echoes:

```rust
#[test]
fn header_without_delimiter_returns_missing_delimiter_error() {
    let result = parse_header("invalid_header_line");
    assert!(matches!(result, Err(HeaderError::MissingDelimiter)));
}
```

For guidelines on test isolation and living documentation, see [Testing](./testing.md). For documentation standards, see [Comments Versus Documentation](./comments-versus-documentation.md).

## Organizing import declarations

Group `use` declarations into distinct blocks to clarify dependencies:

1. Standard library (`std`, `core`, `alloc`)
2. External third-party dependencies (`Cargo.toml`)
3. Workspace crates
4. Internal crate modules (`crate::`, `super::`)

```rust
use std::collections::BTreeMap;
use std::sync::Arc;

use serde::{Deserialize, Serialize};
use tokio::sync::mpsc;

use shared_types::UserId;

use super::protocol::Message;
use crate::storage::SessionStore;
```

To automate consistent imports across a repository, configure `rustfmt.toml`:

```toml
reorder_imports = true
imports_granularity = "Crate"
group_imports = "StdExternalCrate"
```

Setting `group_imports` currently requires a nightly toolchain (`cargo +nightly fmt`).

## Function extraction and abstraction boundaries

Splitting long functions improves readability, but deduplicating code purely because fragments look similar creates brittle abstractions.

### The rule of three and coincidental duplication

* The rule of three advises waiting until a pattern occurs in three distinct call sites before extracting a helper. Early extraction locks in premature abstractions based on incomplete requirements.
* DRY applies to system knowledge and business rules, not incidental syntactic symmetry. Two blocks of code that happen to look alike today often evolve under completely different forces. Merging them introduces artificial coupling.

### Avoiding flag arguments

Extracting a helper across divergent call sites often forces a boolean flag parameter to control behavior. This leaks caller distinctions into the helper:

```rust
fn write_entry(out: &mut String, key: &str, value: &str, quote: bool) {
    if quote {
        out.push_str(&format!("{key}=\"{value}\"\n"));
    } else {
        out.push_str(&format!("{key}={value}\n"));
    }
}
```

Callers should instead perform straightforward operations directly, or select explicitly typed behaviors:

```rust
fn write_plain(out: &mut String, key: &str, value: &str) {
    out.push_str(key);
    out.push('=');
    out.push_str(value);
    out.push('\n');
}

fn write_quoted(out: &mut String, key: &str, value: &str) {
    out.push_str(key);
    out.push_str("=\"");
    out.push_str(value);
    out.push_str("\"\n");
}
```

When multi-mode selection is required, an enum clarifies call sites and avoids Clippy's `fn_params_excessive_bools` lint.

### Unwinding leaky abstractions

When an abstraction accumulates conditional branches and configuration flags, unwind it systematically:

1. Re-inline the helper's body into each call site.
2. Specialize each call site to its actual needs.
3. Observe what genuine shared knowledge remains before re-extracting.

### Testing and duplication

In tests, clarity beats deduplication. Tests must read as independent, self-contained specifications:

* Shared fixtures and input setup functions are encouraged.
* Test assertions and actions must remain inline.
* Avoid abstract test helpers that bundle loops or assertions: a failure in an abstraction obscures which invariant failed and couples unrelated tests.
