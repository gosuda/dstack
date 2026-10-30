# Generics, static dispatch, and dynamic dispatch

Rust supports two models of polymorphism: compile-time generics resolved through static dispatch, and runtime trait objects resolved through dynamic dispatch.

Static dispatch generates specialized machine code for each concrete type through monomorphization. This permits cross-function inlining and compiler optimizations across call boundaries, though optimizations and vectorization are compiler heuristics rather than guarantees. Dynamic dispatch routes invocations through a virtual method table (vtable), sharing code across types and enabling heterogeneous collections. The compiler may devirtualize calls when concrete types are statically provable. The trade-offs in compilation time and binary footprint depend on instantiation counts and optimization passes, requiring empirical measurement.

## Generics and compile-time polymorphism

Generics parameterize functions, structs, and enums over types. The compiler monomorphizes generic definitions by emitting specialized machine code for each concrete type used at call sites.

Monomorphization permits direct function calls and inlining across function boundaries, which in turn enables dead-code elimination and loop optimizations. The trade-off is compilation overhead: instantiating large generic functions across many distinct types increases compilation time and can expand binary code size.

Trait bounds restrict generic parameters to types implementing specific interfaces, enabling relational constraints across parameters. For modeling compile-time state transitions through type bounds, see [Type state pattern](./type-state-pattern.md).

## Static dispatch with trait bounds

Static dispatch is expressed via trait bounds on type parameters, either using angle bracket syntax `<T: Trait>` or the `impl Trait` shorthand in argument positions. The compiler validates at every call site that the concrete type fulfills the declared bound.

Choose static dispatch when:

* Concrete types are fixed at compile time.
* Execution sits on a hot path where call inlining and direct function calls matter.
* Functions return unnameable or complex concrete types such as closures or iterator chains.

```rust
pub fn total_bytes(items: impl IntoIterator<Item = impl AsRef<[u8]>>) -> u64 {
    items.into_iter().map(|item| item.as_ref().len() as u64).sum()
}
```

The compiler specializes `total_bytes` for each iterator and item type passed to it, enabling direct calls and inlining across the iterator chain.

## Dynamic dispatch with trait objects

Dynamic dispatch operates behind pointers or references: `&dyn Trait`, `&mut dyn Trait`, `Box<dyn Trait>`, or `Arc<dyn Trait>`.

In current rustc implementations, a trait object pointer is represented as a fat pointer consisting of two words: a pointer to the underlying data, and a pointer to a vtable (which stores function pointers to method implementations alongside size, alignment, and drop glue). However, trait-object layout is an internal compiler implementation detail, not a stable ABI guarantee. Rust does not guarantee fat pointer layout, vtable representation, or ABI stability across compiler versions or targets.

Choose dynamic dispatch when:

* A single collection must store heterogeneous implementations of a trait.
* Systems require runtime component substitution, such as pluggable backends selected by configuration.
* Signatures need interface abstraction without exposing internal implementation types.
* Mitigating compilation overhead and binary expansion when a large function would otherwise be instantiated across many distinct types.

```rust
use std::io::{self, Write};

pub fn broadcast(writers: &mut [Box<dyn Write>], data: &[u8]) -> io::Result<()> {
    for w in writers {
        w.write_all(data)?;
    }
    Ok(())
}
```

## Trade-off analysis

| Property | Static dispatch (`impl Trait` / `<T>`) | Dynamic dispatch (`dyn Trait`) |
| :--- | :--- | :--- |
| Resolution | Compile-time monomorphization | Runtime virtual table lookup (devirtualization possible when types are statically proven) |
| Performance | Direct calls and inlining opportunities | Indirect calls through vtable pointer unless devirtualized |
| Compilation time | Increases with instantiation count across distinct types | Shared single implementation, compile time depends on crate dependencies |
| Binary size | Scales with instantiation count; requires measurement | Single machine code implementation, plus vtable metadata; requires measurement |
| Storage | Homogeneous collections only | Heterogeneous collections supported |
| Interface visibility | Concrete types visible in generics (`<T>`), hidden in return position (`-> impl Trait`) | Concrete types erased behind trait object pointer |

In argument position, `impl Trait` is syntactic sugar for a generic parameter `<T: Trait>`. In return position, `-> impl Trait` returns an unnameable concrete type chosen by the function body (an existential type), hiding the concrete type from caller signatures while preserving compile-time static dispatch.

Start with static dispatch for internal algorithms and computational kernels. Introduce trait objects when runtime heterogeneity or interface boundary erasure is required.

## Type erasure and boundary design

Exposing trait objects at public boundaries hides implementation details and decouples caller signatures from internal dependencies:

* Decouple public interfaces: Public APIs can accept or return trait objects (such as `Box<dyn Write>`) to decouple caller signatures from internal storage or engine types. However, dynamic trait boundaries do not guarantee that callers avoid recompilation: Rust crates are compiled within Cargo's dependency graph, so rebuilding upstream crates or changing trait declarations still triggers dependent recompilation.
* Avoid premature internal boxing: Do not store `Box<dyn Trait>` inside internal data structures if a generic parameter `T: Trait` works without complicating caller code.
* Box at the outer boundary: Convert concrete types to trait objects where external systems interact, keeping inner processing pipelines generic and inlinable.

## Dyn compatibility and ergonomics

A trait can be instantiated as a trait object (`dyn Trait`) only if it satisfies dyn-compatibility rules (formerly referred to as object safety). The normative specification is defined in the [Rust Reference on Dyn Compatibility](https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility).

A trait is dyn-compatible when:

1. All supertraits are also dyn-compatible.
2. The trait does not require `Self: Sized` (`Sized` is not a supertrait).
3. The trait defines no associated constants.
4. The trait defines no generic associated types (GATs).
5. All associated functions either:
   * Are dispatchable methods:
     * Must have a receiver whose type dereferences to `Self` (`&self`, `&mut self`, `Box<Self>`, `Rc<Self>`, `Arc<Self>`, or `Pin<P>`).
     * Must not declare generic type parameters.
     * Must not use `Self` in argument types or return types (outside the receiver).
     * Must not return `impl Trait` or use `async fn` (unless desugared under stabilized dyn-compatible forms).
   * Or carry an explicit `where Self: Sized` bound.

Attaching `where Self: Sized` to a specific non-dispatchable method (such as a constructor `fn new() -> Self where Self: Sized`) excludes that method from the trait object's vtable, allowing the remaining methods to participate in dynamic dispatch on `dyn Trait`.

```rust
pub trait StreamSource {
    fn read_chunk(&mut self, buf: &mut [u8]) -> usize;

    fn is_empty(&self) -> bool
    where
        Self: Sized,
    {
        false
    }
}
```

Ergonomic considerations for trait objects:

* Prefer `&dyn Trait` or `&mut dyn Trait` over `Box<dyn Trait>` when reading data or calling methods without transferring ownership, avoiding unnecessary heap allocations.
* Use `Arc<dyn Trait + Send + Sync>` when sharing trait objects across threads.
* Use `where Self: Sized` method bounds to preserve dyn compatibility when utility methods require `Self` by value or generic parameters.
