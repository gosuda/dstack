# Performance Engineering

Performance optimization requires empirical measurement. Speculative optimizations introduce architectural complexity without guaranteed latency or throughput gains. Profile before modifying code, and verify each change against reproducible baselines.

## Empirical Measurement and Profiling

Establish reproducible measurement practices before altering code structures:

- Always benchmark and profile in release mode (`--release`). Debug builds omit inlining, dead code elimination, and loop optimizations, generating misleading execution profiles.
- Run `cargo clippy -- -D clippy::perf` to catch static performance hazards such as accidental copies and suboptimal collection patterns.
- Benchmark with `cargo bench` or dedicated benchmarking harnesses such as Criterion. Measure statistical distributions across multiple iterations rather than single execution timings. Accept performance refactors only when statistically significant improvements are demonstrated.
- Use dedicated profilers:
  - Linux and Unix targets: `cargo-flamegraph`, driving `perf` or `dtrace`.
  - macOS targets: `samply`, an interactive sampling profiler with browser-based timeline inspection.

## Profiling with Flamegraph

`cargo-flamegraph` samples program execution and generates SVG flamegraphs showing CPU utilization across the call stack.

Install the tool:

```shell
cargo install flamegraph
```

Run flamegraph across different targets:

```shell
# Profile the default binary in release mode
cargo flamegraph

# Profile a specific binary target
cargo flamegraph --bin stress_target

# Profile unit tests within a crate
cargo flamegraph --unit-test crate_name -- test_filter

# Profile an integration test
cargo flamegraph --test integration_suite

# Profile a Criterion benchmark harness
cargo flamegraph --bench benchmark_name -- --bench

# Profile a workspace example
cargo flamegraph --example workflow_example
```

### Interpreting Flamegraphs

- Vertical axis (Y-axis): represents call stack depth. The entry point of the thread sits at the bottom, and called functions stack upward toward leaf executions at the top.
- Horizontal axis (X-axis): represents sample proportion across the total execution time. The width of a box is proportional to the CPU time spent in that function and its callees. Functions are sorted alphabetically rather than chronologically.
- Box coloration: colors are randomized for visual separation and carry no semantic or performance meaning.
- Analysis heuristics:
  - Broad top plateaus indicate leaf functions consuming significant CPU cycles directly.
  - Wide mid-stack blocks indicate excessive coordination overhead, repetitive formatting, serialization loops, or intermediate allocations.

## Ownership, Borrowing, and Allocation

Unnecessary allocations and deep clones degrade cache locality and increase allocator lock contention. For foundational borrowing idioms and lint detection, see [Coding Styles and Idioms](./coding-styles-and-idioms.md) and [Clippy and Linting Discipline](./clippy-and-linting.md).

### When Ownership Transfer is Appropriate

Pass data by value when:

- The receiver must store the value in a persistent collection, thread channel, or background worker.
- Implementing consuming operator traits:
  ```rust
  use std::ops::Add;

  #[derive(Debug, PartialEq, Eq)]
  struct Accumulator {
      count: usize,
      total_bytes: usize,
  }

  impl Add for Accumulator {
      type Output = Self;

      fn add(self, rhs: Self) -> Self::Output {
          Self {
              count: self.count + rhs.count,
              total_bytes: self.total_bytes + rhs.total_bytes,
          }
      }
  }
  ```
- Enforcing state machine transitions where prior state representations must be invalidated at compile time.
- Cloning cheap reference-counted handles (`Arc<T>`, `Rc<T>`), where the operation only increments an atomic or non-atomic counter.
- Distributing handles across client connection pools.

### When to Avoid Ownership Transfer

- Accept borrowed slices (`&[T]`, `&str`) in public APIs instead of owned containers (`Vec<T>`, `String`) when data is only read.
- Iterate over collections by reference (`&collection`) instead of cloning the collection.
- Mutate existing buffers in place via `&mut T` rather than allocating replacement values.

### Copy-on-Write with `Cow`

Use `std::borrow::Cow` when data is frequently read without transformation, but occasionally requires mutation or owned allocation:

```rust
use std::borrow::Cow;

fn sanitize_identifier(input: &str) -> Cow<'_, str> {
    if input.chars().all(|c| c.is_ascii_alphanumeric() || c == '_') {
        Cow::Borrowed(input)
    } else {
        let sanitized: String = input
            .chars()
            .map(|c| if c.is_ascii_alphanumeric() || c == '_' { c } else { '_' })
            .collect();
        Cow::Owned(sanitized)
    }
}
```

## Stack and Heap Memory Management

Stack allocation provides constant-time allocation and cache locality. Heap allocation provides flexible lifecycles and arbitrary sizing at the cost of allocator overhead and pointer indirection.

### Allocation Guidelines

- Place small, fixed-size data structures on the stack.
- Avoid transferring large types (>512 bytes) by value across call boundaries. Passing large structures by value generates multi-word memory copies across stack frames. Pass them by reference (`&T`, `&mut T`).
- Break infinite size in recursive data structures with `Box`:
  ```rust
  enum OctreeNode<T> {
      Leaf(T),
      Branch(Box<[OctreeNode<T>; 8]>),
  }
  ```
- Avoid allocating large fixed arrays on the stack before boxing. A call such as `Box::new([0u8; 65536])` can materialize the array on the stack frame before copying it to the heap. Construct the heap buffer directly:
  ```rust
  let heap_buffer: Box<[u8]> = vec![0u8; 65536].into_boxed_slice();
  ```
- Use small-vector optimization libraries (`smallvec`, `arrayvec`) when collections contain few elements in the common case, remaining stack-allocated until capacity thresholds spill to the heap.

### Function Inlining Strategy

- Inlining within a single crate is determined automatically by compiler optimization passes.
- Functions called across crate boundaries cannot be inlined unless marked with `#[inline]` or compiled with Link-Time Optimization (LTO).
- Apply `#[inline]` to small, performance-critical accessor functions and generic abstractions across crate boundaries.
- Avoid speculative `#[inline(always)]` annotations without profiling proof; forcing inlining can bloat code size, causing instruction cache misses.

## Zero-Cost Abstractions and Iterators

Rust iterators are evaluated lazily and compile into tight loops equivalent to or faster than manual indexing:

- Prefer iterator pipelines over indexed `for` loops. The compiler eliminates bounds checking during sequential iterator consumption.
- Avoid creating intermediate collections. Chaining `.map()`, `.filter()`, and `.take()` does not allocate. Do not call `.collect::<Vec<_>>()` unless an explicit intermediate allocation or indexed random access is necessary.

```rust
fn compute_total(records: &[u32]) -> u32 {
    records
        .iter()
        .copied()
        .filter(|&val| val % 2 == 0)
        .map(|val| val * 2)
        .sum()
}
```
