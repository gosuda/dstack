# Memory management and thread safety

Rust replaces garbage collection and manual pointer arithmetic with compile-time ownership, explicit borrowing, and static concurrency guarantees. Choosing the appropriate pointer or synchronization primitive ensures both memory safety and minimal runtime indirection.

## Thread safety invariants: Send and Sync

The Rust compiler tracks concurrency safety through two built-in marker traits:

- `Send`: indicates that ownership of the type can be safely transferred across thread boundaries.
- `Sync`: indicates that concurrent access from multiple threads via shared references (`&T`) is safe.
- Core relationship: `T: Sync` if and only if `&T: Send`.

### Concurrency and pointer safety matrix

| Type | Description | Send Condition | Sync Condition | Concurrency Semantics |
| --- | --- | --- | --- | --- |
| `&T` | Shared reference | `T: Sync` | `T: Sync` | Multiple concurrent readers; prevents direct mutation while permitting controlled interior mutability when `T` provides it. |
| `&mut T` | Exclusive mutable reference | `T: Send` | `T: Sync` | Single exclusive writer; can be transferred across threads if `T: Send`. |
| `Box<T>` | Unique heap allocation | `T: Send` | `T: Sync` | Owned heap allocation; mirrors thread traits of `T`. |
| `Rc<T>` | Reference counted (single-thread) | `!Send` | `!Sync` | Non-atomic reference counting; restricted to one thread. |
| `Arc<T>` | Atomic reference counted | `T: Send + Sync` | `T: Send + Sync` | Shared read access across threads with atomic reference counting. |
| `Cell<T>` | Value interior mutability | `T: Send` | `!Sync` | Single-threaded; value mutation without references; supports non-`Copy` via `set`/`replace`/`take`/`into_inner`; `get` requires `T: Copy`. |
| `RefCell<T>` | Dynamic borrow checker | `T: Send` | `!Sync` | Single-threaded runtime borrow checking; `borrow`/`borrow_mut` panic, `try_borrow`/`try_borrow_mut` return `BorrowError`/`BorrowMutError`. |
| `Mutex<T>` | Mutual exclusion lock | `T: Send` | `T: Send` | Synchronizes access across threads; requires only `T: Send`. Lock poisoning on panic is advisory. |
| `RwLock<T>` | Reader-writer lock | `T: Send` | `T: Send + Sync` | Concurrent readers (`T: Sync`) and exclusive writers (`T: Send`). Poisons only on writer panic, not reader panic; advisory. |
| `OnceCell<T>` | Single-assignment container | `T: Send` | `!Sync` | Write-once deferred initialization; single-thread only. |
| `LazyCell<T, F>` | Lazy single-assignment container | `T: Send, F: Send` | `!Sync` | Computes value on first access; single-thread only. |
| `OnceLock<T>` | Thread-safe single assignment | `T: Send` | `T: Send + Sync` | Thread-safe write-once initialization. |
| `LazyLock<T, F>` | Thread-safe lazy evaluation | `T: Send, F: Send` | `T: Send + Sync, F: Send` | Computes value on first thread access; thread-safe. `F` requires `Send` to run on the initializing thread; `F: Sync` is not required. |
| `*const T` / `*mut T` | Raw pointers | `!Send` | `!Sync` | Unchecked memory address; requires explicit `unsafe` blocks and verified safety invariants. |

## Pointer types and usage patterns

### Shared and exclusive references: &T and &mut T

References represent borrowed data without ownership transfer. The borrow checker enforces that any number of shared references (`&T`) or exactly one exclusive reference (`&mut T`) may exist at any program point.

Shared references prevent direct mutation by default, eliminating data races at compile time. When mutation through a shared reference is required, it must be mediated by types providing controlled interior mutability (such as `Cell`, `RefCell`, `Mutex`, `RwLock`, or atomic primitives).

```rust
fn append_metric(buffer: &mut Vec<u8>, chunk: &[u8]) {
    buffer.extend_from_slice(chunk);
}
```

### Unique heap allocation: Box<T>

`Box` provides single-owner heap storage with deterministic deallocation when the pointer goes out of scope. Use `Box` to offload large payloads from stack frames, define recursive types with finite layout, or construct trait objects (`Box<dyn Trait>`):

```rust
enum Expression {
    Literal(i64),
    Negate(Box<Expression>),
    Add(Box<Expression>, Box<Expression>),
}
```

### Single-threaded reference counting: Rc<T>

`Rc` enables multiple owners within a single thread. Cloning an `Rc` pointer performs a non-atomic integer increment, avoiding synchronization instructions:

```rust
use std::rc::Rc;

let shared_config = Rc::new(String::from("system_profile"));
let handle_a = Rc::clone(&shared_config);
let handle_b = Rc::clone(&shared_config);
```

### Multi-threaded reference counting: Arc<T>

`Arc` provides thread-safe shared ownership. Cloning increments an atomic reference count using hardware atomic instructions. Wrap shared read-only collections in `Arc<[T]>` or `Arc<str>` to minimize overhead, or combine with synchronization primitives (`Arc<Mutex<T>>` or `Arc<RwLock<T>>`) for shared mutable state:

```rust
use std::sync::Arc;
use std::thread;

let shared_data: Arc<[u32]> = Arc::from([1, 2, 3, 4]);
let worker_data = Arc::clone(&shared_data);

let handle = thread::spawn(move || {
    worker_data.iter().sum::<u32>()
});

let total = handle.join().expect("thread panicked");
```

### Interior mutability: Cell<T> and RefCell<T>

`Cell` and `RefCell` provide interior mutability, allowing data behind a shared reference (`&T`) to be mutated within a single thread. Neither type implements `Sync`.

- `Cell<T>` operates on values without reference borrowing, avoiding runtime borrow tracking overhead. It supports non-`Copy` types through `set` (replaces value, dropping the old one), `replace` (replaces value, returning the old one), `take` (replaces value with `Default::default()`), and `into_inner` (consumes the cell). Reading the contained value via `get()` requires `T: Copy`.
  ```rust
  use std::cell::Cell;

  struct Counter {
      invocations: Cell<usize>,
  }

  let counter = Counter {
      invocations: Cell::new(0),
  };
  counter.invocations.set(counter.invocations.get() + 1);
  ```

- `RefCell<T>` dynamically enforces borrowing rules at runtime via an internal counter. Calling `borrow()` returns a shared `Ref<'_, T>` and panics if the value is currently mutably borrowed. Calling `borrow_mut()` returns an exclusive `RefMut<'_, T>` and panics if the value is currently borrowed in any form. For fallible checks without panicking, use `try_borrow()`, which returns `Result<Ref<'_, T>, BorrowError>`, or `try_borrow_mut()`, which returns `Result<RefMut<'_, T>, BorrowMutError>`.
  ```rust
  use std::cell::RefCell;

  let buffer = RefCell::new(Vec::new());
  buffer.borrow_mut().push(42);
  ```

### Concurrent synchronization: Mutex<T> and RwLock<T>

`Mutex` and `RwLock` provide thread-safe interior mutability:

- `Mutex<T>` guarantees mutual exclusion: only one thread holds the lock at a time.
- `RwLock<T>` allows multiple concurrent readers, but exclusive access for writers.
- Lock poisoning:
  - If a thread panics while holding an exclusive lock, the lock becomes poisoned to alert subsequent callers that protected invariants may be compromised.
  - `RwLock<T>` poisons only on writer panic; panics while holding a shared read lock do not poison the `RwLock`.
  - Mutex and RwLock poisoning is advisory rather than a memory safety proof. Memory remains safe and uncorrupted at the language level. Subsequent threads can recover access to the inner guard via `PoisonError::into_inner()` if invariant restoration is viable.
- Locks release automatically when their RAII guard drops out of scope.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let shared_counter = Arc::new(Mutex::new(0usize));
let worker_counter = Arc::clone(&shared_counter);

let handle = thread::spawn(move || {
    let mut guard = worker_counter.lock().expect("lock poisoned");
    *guard += 1;
});

handle.join().expect("thread failed");
```

### Thread-safe initialization: OnceLock<T> and LazyLock<T>

Standard library primitives provide thread-safe initialization without external crates:

- `OnceLock<T>` allows write-once initialization via `get_or_init()` or `set()`:
  ```rust
  use std::sync::OnceLock;

  static RUNTIME_ID: OnceLock<u64> = OnceLock::new();

  fn runtime_id() -> u64 {
      *RUNTIME_ID.get_or_init(|| 42)
  }
  ```

- `LazyLock<T, F>` evaluates an initialization closure on first thread access:
  ```rust
  use std::collections::HashMap;
  use std::sync::LazyLock;

  static ROUTING_TABLE: LazyLock<HashMap<&'static str, u16>> = LazyLock::new(|| {
      let mut map = HashMap::new();
      map.insert("health", 8080);
      map.insert("metrics", 9090);
      map
  });
  ```

### Raw pointers: *const T and *mut T

Raw pointers bypass borrow checker invariants. They can be null, dangling, unaligned, or aliased. Every dereference must occur within an `unsafe` block and explicitly verify the required safety conditions:

1. **Non-null**: The pointer must not be null.
2. **Alignment**: The pointer must be properly aligned for `T`.
3. **Validity and initialization**: The pointer must point to an initialized instance of `T` within a live allocation that has not been deallocated.
4. **Aliasing rules**: No mutable raw pointer may alias active references or concurrent accesses that violate exclusivity.
5. **Safety rationale**: Precede every `unsafe` block with an explicit `// SAFETY:` explanation detailing why these invariants hold, satisfying `clippy::undocumented_unsafe_blocks`.

```rust
let value: i32 = 100;
let raw_pointer: *const i32 = &value;

// SAFETY: raw_pointer is derived from a live, initialized local variable on the
// current stack frame, is properly aligned for i32, is non-null, and no concurrent
// mutable access exists during dereference.
let inspected_value = unsafe { *raw_pointer };
```

## References

- [The Rust Reference: Send and Sync Traits](https://doc.rust-lang.org/reference/special-types-and-traits.html#send-and-sync)
- [The Rust Standard Library: std::sync::LazyLock](https://doc.rust-lang.org/std/sync/struct.LazyLock.html)
- [The Rust Standard Library: std::cell::Cell](https://doc.rust-lang.org/std/cell/struct.Cell.html)
- [The Rust Standard Library: std::cell::RefCell](https://doc.rust-lang.org/std/cell/struct.RefCell.html)
- [The Rust Standard Library: std::sync::RwLock](https://doc.rust-lang.org/std/sync/struct.RwLock.html)
- [The Rust Standard Library: std::sync::Mutex](https://doc.rust-lang.org/std/sync/struct.Mutex.html)
- [The Rustonomicon - The Dark Arts of Unsafe Rust](https://doc.rust-lang.org/nomicon/)
- [Rust Atomics and Locks](https://marabos.nl/atomics/)
