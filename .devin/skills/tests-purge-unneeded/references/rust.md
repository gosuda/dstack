# Rust, cargo test deletion patterns

Rust checks ownership and lifetimes, requires exhaustive matching, and has no implicit conversions or null. **A test that asserts a plain struct has the fields the compiler proved it has, without validation or fallible work in construction, catches nothing.** The compiler is the test for structure; `cargo test` is for behavior at boundaries.

## Delete

### Struct field initialization

```rust
#[derive(Debug, PartialEq)]
struct User {
    id: u64,
    name: String,
}

#[test]
fn user_constructor_sets_fields() {
    let u = User { id: 1, name: "alice".into() };
    assert_eq!(u.id, 1);
    assert_eq!(u.name, "alice");
}
```

The compiler proves that `User { id: 1, name: "alice".into() }` constructs a `User` with those exact fields when construction only assigns the given fields without validation, fallible conversion, or logic that can panic or return `Err`. The test is a tautology. When field construction can panic, return `Err`, or run validation, keep the test as a real-bug test.

### Identity or passthrough functions

```rust
fn wrap(n: u64) -> u64 {
    n
}

#[test]
fn wrap_returns_input() {
    assert_eq!(wrap(42), 42);
}
```

If `wrap` is genuinely identity, it is dead code, `let n = n;` should be inlined and the function deleted. The test then deletes itself.

### Pure type-check tests (no runtime work, no panic surface)

```rust
#[test]
fn http_client_typestate_compiles() {
    // Only declarations, no method calls that could panic, no I/O, no Result-bearing work
    let _: PhantomData<HttpClient<Configured>> = PhantomData;
}
```

Delete this kind of test only when the test's *sole* purpose is type-checking AND it has no meaningful runtime behavior, no method calls that could panic, no `unwrap`/`expect`, no I/O, no fallible operations. Such tests should live in `trybuild` UI tests rather than the regular test runner.

### Bare no-assert or no-panic tests

```rust
#[test]
fn parser_does_not_panic_on_empty_input() {
    parse(""); // no assert: catches only panics, ignoring wrong outputs or silent failures
}
```

Delete bare execution tests that lack an independent assertion or invariant oracle. Observing that an execution path completes without panicking does not prove correctness; an empty parser returning an unvalidated dummy tree or swallowing errors passes this check. Reject the smoke test exception. Either delete the test, or upgrade it to assert against an independent invariant or explicit contract outcome (such as `assert_eq!(parse(""), Ok(AST::Empty))` or `assert!(matches!(parse(""), Err(ParseError::UnexpectedEof)))`).

A runtime assertion (`assert_eq!(get_id(&item), 7)`) tests the *behavior* of `get_id` or `HasId for Foo`, not just the type. That is a real-bug test (a refactor could swap fields, change the implementation, etc.); see the Keep section below.

### Default::default trivial assertion

```rust
#[derive(Default)]
struct Config {
    debug: bool,
    timeout_ms: u64,
}

#[test]
fn config_default() {
    let c = Config::default();
    assert_eq!(c.debug, false);
    assert_eq!(c.timeout_ms, 0);
}
```

`#[derive(Default)]` generates exactly this. Asserting the derived behavior tests the compiler, not your code. Delete unless the `Default` impl is hand-written and *non-obvious*.

## Keep

### Deserialization rejection path with failure classification

```rust
#[test]
fn deserialize_rejects_missing_required_field() {
    let json = r#"{"name": "alice"}"#;  // missing required "id"
    let err = serde_json::from_str::<User>(json).unwrap_err();
    assert!(err.is_data(), "expected missing field data error, got {err:?}");
}
```

JSON parsing is a runtime boundary, but a bare `assert!(result.is_err())` is weak because unrelated syntax errors, malformed braces, or I/O failures also produce an error. Classify the failure (such as verifying `err.is_data()` or asserting the specific error variant) to prove the contract rejected the input for the expected reason. Keep with failure classification.

### Error-type variants

```rust
#[test]
fn validate_returns_invalid_email_for_no_at() {
    match validate_email("alice") {
        Err(ValidationError::InvalidEmail) => {}
        other => panic!("expected InvalidEmail, got {:?}", other),
    }
}
```

Tests the *semantics* of the error variant: what failure produces what error. This is a real-bug surface because a refactor could silently return a different variant. Keep.

### Trait impl behavior at boundary

```rust
#[test]
fn user_repo_persists_to_real_postgres() {
    let pool = test_pool();
    let repo = PgUserRepo::new(pool.clone());
    let user = User { id: 1, name: "alice".into() };
    repo.save(&user).unwrap();
    let found = repo.find(1).unwrap();
    assert_eq!(found.name, "alice");
}
```

Real DB, real transaction, catches schema mismatches, query bugs, sqlx type-mapping errors. Keep.

### Unsafe invariant

```rust
#[test]
fn from_raw_parts_handles_zero_length() {
    let v: Vec<u8> = unsafe { Vec::from_raw_parts(std::ptr::NonNull::dangling().as_ptr(), 0, 0) };
    assert!(v.is_empty());
}
```

Tests the contract of `unsafe` code at its boundary, exactly where the compiler stops helping. Keep.

### Concurrency invariant

```rust
#[test]
fn channel_drops_remaining_messages_on_close() {
    let (tx, rx) = std::sync::mpsc::channel();
    tx.send(1).unwrap();
    drop(tx);
    assert_eq!(rx.recv(), Ok(1));
    assert!(rx.recv().is_err());
}
```
The type system enforces Send and Sync, but it does not enforce the runtime semantics of concurrent operations. In this case, `assert!(rx.recv().is_err())` is valid because `RecvError` is the sole failure mode of `mpsc::Receiver::recv()`, identifying that the channel was disconnected and drained. Do not blanket-ban syntax when the error type itself proves the invariant. Keep.
