---
name: memory-model
description: 'Use when choosing memory orderings for C++ or Rust atomics, reasoning about happens-before, writing lock-free patterns, or diagnosing data races. Not for lock-based design.'
---

# Memory model

An atomic without a stated ordering is a guess. C++ and Rust share one model: pick the weakest ordering that still proves the happens-before edge your algorithm needs, and write that edge down next to the operation. This skill is read-only guidance (it explains and drafts, and any code change lands through the normal coding path). You are finished when every atomic in the reviewed code carries an ordering justified by its edge, or a race is named with the edge that is missing.

To work you need the concurrent code or design, and which language it is in. The orderings map one to one between C++ and Rust. Bring the target architectures only when barrier cost matters.

## The five orderings, weakest first

Weaker ordering costs less on weakly ordered machines and costs nothing on x86 for load and store shapes.

| Ordering | C++ | Rust | Guarantee |
|----------|-----|------|-----------|
| Relaxed | `memory_order_relaxed` | `Ordering::Relaxed` | Atomicity only, no ordering |
| Acquire | `memory_order_acquire` | `Ordering::Acquire` | No later read or write moves before this load |
| Release | `memory_order_release` | `Ordering::Release` | No earlier read or write moves after this store |
| AcqRel | `memory_order_acq_rel` | `Ordering::AcqRel` | Both, RMW operations only |
| SeqCst | `memory_order_seq_cst` | `Ordering::SeqCst` | One total order every thread agrees on |

## Prove happens-before before trusting a read

A release store that an acquire load reads creates the edge: every write before the store is visible after the load, and edges compose transitively. State the edge as the correctness argument, not intuition.

```cpp
std::atomic<int> data_ready{0};
int data = 0;                      // plain, guarded by the edge

void producer() {
    data = 42;                                      // 1) plain write
    data_ready.store(1, std::memory_order_release); // 2) release
}
void consumer() {
    while (!data_ready.load(std::memory_order_acquire)) {}  // 3) acquire
    assert(data == 42);                             // 4) guaranteed by the edge
}
```

## Match the ordering to the pattern

Each site in the code should map to one row:

| Pattern | Ordering |
|---------|----------|
| Statistics counter | Relaxed everywhere |
| Reference count | Relaxed on increment, AcqRel on the decrement that may free |
| Publish flag and data | Release on the store, Acquire on the load |
| Lock-free queue first cut | SeqCst, then weaken one edge at a time with a re-run of the tests |
| Sequence-number check | Release plus Acquire |
| Mutex internals | AcqRel on the RMW that takes and gives the lock |

## Fences are for edges no single operation can carry

A fence orders without touching one variable (typically when several writes must land before one flag flips). The flag still carries its own ordering.

```cpp
// publish several writes, then flip the flag
data1 = 1;
data2 = 2;
std::atomic_thread_fence(std::memory_order_release);
flag.store(true, std::memory_order_relaxed);
// consumer pairs with an acquire fence after reading the flag
```

Keep SeqCst for the cases that need a single global order. Two flags each read after waiting on the other is the store-buffering case where weaker orderings let both readers miss both writes. Either keep SeqCst on the participating operations or carry a written proof that weaker orderings suffice.

## The same model in Rust names

| C++ | Rust |
|-----|------|
| `memory_order_relaxed` | `Ordering::Relaxed` |
| `memory_order_acquire` | `Ordering::Acquire` |
| `memory_order_release` | `Ordering::Release` |
| `memory_order_acq_rel` | `Ordering::AcqRel`, RMW only |
| `memory_order_seq_cst` | `Ordering::SeqCst` |
| `atomic_thread_fence(order)` | `std::sync::atomic::fence(order)` |

Rust signs the intent in the type: `AtomicBool`, `AtomicUsize`, and friends, with `compare_exchange` returning the previous value and the failure ordering taken explicitly.

Respect the CAS rules. The failure ordering of a compare-exchange is a load, so it may not be Release or AcqRel, and it may not be stronger than the success ordering. Use `compare_exchange_weak` in retry loops, where spurious failure costs one iteration.

```cpp
int expected = 0;
while (!val.compare_exchange_weak(expected, 42,
                                  std::memory_order_acq_rel,   // success
                                  std::memory_order_acquire)) {
    expected = 0;   // reset when the caller reuses the variable
}
```

If the compiler rejects the failure ordering, it was Release or AcqRel, so drop it to Acquire or Relaxed. If a CAS loop live-locks, it is losing every race under contention: add backoff or restructure to fewer writers.

## Platform cost and the classic mistakes

x86 is TSO: stores drain in order, so plain Acquire and Release compile to plain loads and stores, and SeqCst needs a full fence or a locked operation. ARMv8 and RISC-V are weakly ordered: acquire and release map to load-acquire and store-release instructions, and a full fence needs an explicit barrier instruction. Name the architecture whenever you claim an ordering is cheap.

| Mistake | Fix |
|---------|-----|
| Relaxed used to publish data | Release on the store, Acquire on the load |
| SeqCst everywhere by fear | Keep SeqCst only where a total order is the argument; justify the rest |
| Plain reads of shared data beside atomics | The edge from the atomic pair must cover them, or the data must be atomic too |
| `volatile` used for threads | `volatile` orders nothing across threads; use atomics |
| Two values assumed consistent with no edge between them | Add one atomic carrying the edge, or SeqCst on both |
| Lock-free pop frees nodes the readers still hold | Add a reclamation scheme; the ABA and reclamation problem is separate from ordering |

When TSan reports a race, one side of the pair is not atomic or the edge is missing, so name the two accesses, then supply the release and acquire pair that orders them. When a test passes but the reasoning is unclear, the ordering may be right by luck of the architecture: write the edge as a comment and re-derive it rather than weakening blindly. When weakening SeqCst breaks a stress test, restore SeqCst, because the code needed the total order.

## What you hand back

A per-site ordering review: each atomic operation, the edge it creates or needs, the chosen ordering, and the platform cost note where relevant. The happens-before diagram, the CAS variants, and the lock-free stack sketch live in `references/cpp-memory-ordering.md`.
