# Error modeling, classification, and resilience

Rust treats fallibility as a domain state expressed through the type system. Rather than relying on out-of-band sentinel values, global errno flags, or implicit runtime unwinds, functions communicate potential failure by returning `Result<T, E>`. How errors are modeled, classified, and tested determines whether a codebase remains resilient and composable or becomes brittle and difficult to debug.

## Model fallibility with Result instead of panics

When an operation can fail during normal execution due to invalid input, network disconnection, or external system state, return `Result<T, E>`. Reserve `panic!` strictly for unrecoverable programmer bugs, internal invariant violations that indicate corrupted memory or impossible logic states, and test assertions.

```rust
#[derive(Debug, PartialEq)]
pub enum DivisionError {
    DividedByZero,
}

pub fn divide(x: f64, y: f64) -> Result<f64, DivisionError> {
    if y == 0.0 {
        Err(DivisionError::DividedByZero)
    } else {
        Ok(x / y)
    }
}
```

Use `unreachable!` only for a state that an established invariant excludes. It panics if that invariant fails. Return a typed error for supported failure paths; do not ship unfinished branches.

## Handle recoverable failures explicitly

`unwrap()` and `expect()` panic on `Err` or `None`. With unwinding enabled, Rust unwinds the stack and runs destructors. An aborting panic strategy terminates the process without that cleanup.

Use `expect` when earlier logic establishes the invariant and failure means a defect. State that invariant in the assertion message, not an implementation comment. Tests still need an independent postcondition or fault oracle after setup succeeds. Return contextual errors for recoverable input, I/O, and startup failures.

Replace `unwrap` and `expect` with structured control flow:

* Guard clauses with `let-else` flatten function bodies by handling failure with an early return or break:
```rust
let Ok(payload) = serde_json::from_str::<Payload>(&input) else {
    return Err(ServiceError::InvalidPayload);
};
```

* Branch recovery with `if-let` recovers or selects an alternative path when an error occurs:
```rust
if let Ok(cached) = cache.get(key) {
    return Ok(cached);
} else {
    fetch_from_upstream(key).await
}
```

* Fallback combinators provide deterministic fallbacks using `unwrap_or`, `unwrap_or_else`, or `unwrap_or_default`:
```rust
let timeout = configured_timeout.unwrap_or(Duration::from_secs(30));
let port = env_port.unwrap_or_else(|| default_port_for_scheme(&scheme));
```

* Converting `Option` to `Result` creates explicit domain errors using `ok_or` or `ok_or_else`:
```rust
let session_id = request.headers().get("x-session-id")
    .ok_or(AuthError::MissingSessionHeader)?;
```

## Define structured library errors with thiserror

In libraries and reusable crates, error types are public API contracts. Callers must be able to branch on failure modes programmatically. Derive `std::error::Error` and `Display` using `thiserror` to define strongly typed, enumerated errors without manual boilerplate:

```rust
use std::path::PathBuf;

#[derive(Debug, thiserror::Error)]
pub enum StorageError {
    #[error("file not found at {path:?}")]
    NotFound { path: PathBuf },
    #[error("permission denied for user {uid} on {path:?}")]
    PermissionDenied { uid: u32, path: PathBuf },
    #[error(transparent)]
    Io(#[from] std::io::Error),
    #[error(transparent)]
    Serialization(#[from] serde_json::Error),
}
```

Keep error variants semantic:
* Provide structured fields (`path`, `uid`) so programmatic consumers can inspect details without parsing formatted strings.
* Use `#[error(transparent)]` when an error variant simply forwards an underlying error's `Display` and `source` implementations unchanged.

## Layer error hierarchies and preserve causal chains

Avoid monolithic top-level error enums that pool every error across an entire system. Instead, scope errors to cohesive modules and wrap lower-level subsystem errors at architectural seams using `#[from]`:

```rust
#[derive(Debug, thiserror::Error)]
pub enum DatabaseError {
    #[error("connection pool exhausted")]
    PoolExhausted,
    #[error("query execution failed: {0}")]
    Query(#[from] sqlx::Error),
}

#[derive(Debug, thiserror::Error)]
pub enum ApiError {
    #[error("database failure: {0}")]
    Database(#[from] DatabaseError),
    #[error("invalid input: {field}")]
    Validation { field: &'static str },
}
```

Preserve causal chains across layers so diagnosing tools and logging infrastructure can inspect root causes via `std::error::Error::source()` or downcast to concrete subsystem types:

```rust
if let Some(db_err) = err.source().and_then(|s| s.downcast_ref::<DatabaseError>()) {
    log::error!("Underlying database failure: {db_err}");
}
```

## Restrict anyhow to application entry points

The `anyhow` crate provides a dynamically typed error container (`anyhow::Error`) optimized for applications, CLI binaries, daemon entry points, and test harnesses. It enables attaching diagnostic context via `.context(...)` or `.with_context(...)` without defining custom error enums:

```rust
use anyhow::{Context, Result};

fn run_worker(config_path: &str) -> Result<()> {
    let raw = std::fs::read_to_string(config_path)
        .with_context(|| format!("failed to read configuration file: {config_path}"))?;
    let config: AppConfig = toml::from_str(&raw)
        .context("failed to parse TOML configuration")?;
    start_service(&config)?;
    Ok(())
}
```

Reserve `anyhow` strictly for:
* Binary entry points (`main.rs`) and CLI dispatch.
* Top-level async daemon dispatch where errors are logged or rendered for humans.
* Integration and end-to-end tests where precise variant matching is unnecessary.

Do not use `anyhow::Result` or `Box<dyn std::error::Error>` in public library interfaces. Type erasure prevents consumers from handling specific error variants programmatically and forces callers to depend on string matching or unreliable downcasting.

## Bubble errors with ? and handle recovery explicitly

Propagate errors across call stacks using the `?` operator. This automatically applies `From::from` conversions defined on the caller's error type:

```rust
fn process_payload(raw: &[u8]) -> Result<ProcessedRecord, IngestionError> {
    let uncompressed = decompress_frame(raw)?;
    let parsed = parse_record(&uncompressed)?;
    let validated = validate_schema(parsed)?;
    Ok(validated)
}
```

When handling errors at intermediate boundaries:
* `inspect_err`: Perform side effects such as metric emission or diagnostic logging without modifying the error or intercepting control flow.
* `map_err`: Translate an unmapped foreign error type into an appropriate domain error when an automatic `From` conversion is not defined.
* `or_else`: Attempt alternative recovery strategies or fallback operations upon encountering an error.

## Verify error semantics and state invariants in tests

Unit tests for fallible operations must verify the semantic error contract: variant classification, structured payload values, causal propagation, and state invariants upon failure.

Reject string-based error assertions:
* Never assert on `err.to_string()` or `format!("{err}")` as proof of correctness.
* Never assert merely that error strings are non-empty (`assert!(!err.to_string().is_empty())`).
* String formatting reflects human presentation, not machine contracts. String assertions fail refactor resilience by breaking on harmless wording adjustments while failing to catch dropped causal links or misclassified error variants.

When error types do not implement `PartialEq` or `Eq`:
* Use `std::assert_matches!` (stabilized in Rust 1.96+, imported via `use std::assert_matches;`) or `matches!` to assert variant classification and extract structured fields.
* Verify causal chain preservation by querying `.source()` and downcasting via `source.downcast_ref::<E>()`.
* Assert state invariants to prove that a failed operation left external state unmutated or successfully rolled back transactions.

The following self-contained division test suite demonstrates invariant verification without fixture files or string-matching oracles:

```rust
use std::assert_matches;

#[derive(Debug)]
pub enum DivisionError {
    DividedByZero,
}

pub fn divide(x: f64, y: f64) -> Result<f64, DivisionError> {
    if y == 0.0 {
        Err(DivisionError::DividedByZero)
    } else {
        Ok(x / y)
    }
}

#[test]
fn zero_divisor_is_classified_as_divided_by_zero() {
    let numerators = [-1.0e6, -42.0, -1.0, -0.0, 0.0, 1.0, 42.0, 1.0e6];
    let zero_divisors = [0.0, -0.0];

    for &x in &numerators {
        for &y in &zero_divisors {
            assert_matches!(divide(x, y), Err(DivisionError::DividedByZero));
        }
    }
}

#[test]
fn finite_bounded_nonzero_division_satisfies_inverse_algebraic_relation() {
    let numerators = [-1.0e6, -1234.56, -42.0, -1.0, 0.5, 1.0, 10.0, 100.0, 1.0e6];
    let divisors = [-8.0, -3.0, -0.125, 0.125, 2.0, 3.0, 7.0, 78.9];

    for &x in &numerators {
        for &y in &divisors {
            let quotient = divide(x, y).expect("division by finite nonzero divisor must succeed");
            let reconstructed = quotient * y;
            let diff = (reconstructed - x).abs();
            let bound = x.abs() * f64::EPSILON * 2.0;
            assert!(
                diff <= bound,
                "reconstruction diff {diff} exceeded bound {bound} for x={x}, y={y}"
            );
        }
    }
}
```

### Real faults detected by invariant testing

This invariant test suite catches real implementation faults:
* Removing the guard check `if y == 0.0` produces `Ok(inf)`, `Ok(-inf)`, or `Ok(NaN)`, which immediately fails the zero-divisor assertion.
* Checking bits naively via `y.to_bits() == 0` misses IEEE 754 negative zero (`-0.0`, where the sign bit `1 << 63` is set), which the test catches with `-0.0`.
* Inverting operands (`y / x`) or swapping guard conditions violates the algebraic reconstruction bound $|(x / y) \cdot y - x| \le 2\epsilon|x|$.
* Arithmetic sign inversion or operator replacement causes large reconstruction errors that fail the bounded delta check.

### Behavior-preserving refactors survived

The tests remain green across valid structural and algorithmic refactors:
* Reordering internal branches, replacing `if-else` with pattern matching, or introducing early returns.
* Rewording docstrings, modifying presentation formatting, or altering `Display` messages.
* Note that reciprocal multiplication (`x * (1.0 / y)`) does not yield exact IEEE 754 equivalence to direct division (`x / y`) due to compounded rounding error. However, testing algebraic reconstruction against an explicit bound ($|(quotient \cdot y) - x| \le 2\epsilon|x|$) verifies numerical stability and functional correctness without demanding false bitwise identity across compiler optimization levels.

## Single-failure domains and custom error structs

When an operation can only fail in a single, well-defined way or requires rich context fields rather than an enumeration of variants, use a custom error struct:

```rust
#[derive(Debug, thiserror::Error, PartialEq, Eq)]
#[error("HTTP request failed with status {code}: {reason}")]
pub struct HttpError {
    pub code: u16,
    pub reason: String,
}
```

This avoids creating single-variant enums while preserving typed introspection and clear error formatting.

## Async errors and runtime thread safety

Asynchronous runtimes (such as Tokio) execute futures and tasks across multi-threaded thread pools. Errors that cross task spawn boundaries, channel sends, or `.await` suspension points must implement `Send + Sync + 'static`:

```rust
pub async fn execute_task<F, T>(job: F) -> Result<T, Box<dyn std::error::Error + Send + Sync + 'static>>
where
    F: std::future::Future<Output = Result<T, Box<dyn std::error::Error + Send + Sync + 'static>>> + Send + 'static,
    T: Send + 'static,
{
    tokio::spawn(job).await?
}
```

When implementing custom error types for async libraries, ensure they derive or implement `Send` and `Sync` by avoiding thread-bound interior mutability types (such as `Rc` or `RefCell`) in error fields.
