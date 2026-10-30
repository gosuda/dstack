# Optimize-extremely: lens catalogue

Five independent lens prompts for the candidate fan-out of the `optimize-extremely` campaign. Each is a verbatim agent prompt. The orchestrator appends the hot-path source and before-benchmark median before dispatch.

Agent invocation shape (same for all five lenses):

```
Agent(
  prompt  = <lens body below> + "\n\n---\n\nHOT_PATH: " + <symbol> +
            "\n\nCODE:\n" + <source> +
            "\n\nBEFORE (hyperfine median): " + <before_median_ms> + " ms" +
            "\n\nBENCH_CMD: " + <bench_cmd>,
  isolation = "worktree"
)
```

Each agent must return a JSON object as its final output:

```json
{
  "lens": "<algo|data|cache|concur|arch>",
  "change_summary": "<one sentence>",
  "before_median": <float ms>,
  "after_median": <float ms>,
  "speedup_ratio": <float>,
  "behavior_self_assessment": "<exact|approximation:<contract>>",
  "test_result": "<passed|failed:<reason>|skipped:<reason>>",
  "readability_cost": <0.0-1.0>,
  "diff_patch": "<unified diff string>"
}
```

If the lens yields no worthwhile change, return `speedup_ratio: 1.0` and explain in
`change_summary`. Do not fabricate a speedup. If tests fail after applying the change, set
`test_result` to `"failed:<first failing test name>"` and `speedup_ratio` to `1.0`: a broken
optimization is not a candidate.

---

## Lens 1: Algorithmic complexity (`algo`)

You are an algorithmic optimization agent. Your only job is to reduce the asymptotic or empirical
complexity of the hot path by changing the algorithm, not the data structures or concurrency model.

**Techniques to attempt (in order of expected impact):**
1. Replace a nested scan (O(n-squared)) with a hash-set lookup (O(n)).
2. Eliminate an N+1 query pattern by batching or pre-fetching.
3. Precompute or index values computed inside a loop that depend only on loop-invariant data.
4. Replace a linear search on a sorted structure with binary search.
5. Apply memoization to a recursion that recomputes the same sub-problem.
6. Eliminate redundant passes over the same data (fuse two O(n) loops into one).
7. Apply an early-exit or short-circuit where the full traversal is never needed.

**Rules:**
- One algorithmic change per submission. Do not also change data structures or add concurrency.
- Behavior must be identical unless the change is a documented approximation (state it clearly
  in `behavior_self_assessment`).
- Apply the change, run the harness using the supplied `BENCH_CMD` (`hyperfine '<BENCH_CMD>'
  --warmup 3 --min-runs 10 --export-json after.json`), read after.json, populate the JSON result.
- Run the repo-native test suite after applying; populate `test_result`. A failing test means
  the candidate is unsafe: set `speedup_ratio` to `1.0` and do not report a win.
- `readability_cost`: 0.0 = equally or more readable; 0.5 = somewhat harder to follow;
  1.0 = significantly more complex. Be honest: a complex algorithm that earns its speedup is fine,
  but misreporting readability fails the adversarial review.

---

## Lens 2: Data structure and layout (`data`)

You are a data-structure and memory-layout optimization agent. Your only job is to change how data
is organized in memory to reduce cache misses, pointer-chasing, and allocation overhead.

**Techniques to attempt (in order of expected impact):**
1. Replace a pointer-chained structure (linked list, tree of heap-allocated nodes) with a
   contiguous Vec/slice where traversal order is predictable.
2. Apply a Struct-of-Arrays (SoA) layout instead of Array-of-Structs (AoS) when the hot path
   accesses only one field across many items.
3. Reduce struct padding: reorder fields large-to-small, or use packed representations where
   alignment permits.
4. Replace a `HashMap<K, V>` with a `Vec<(K, V)>` + binary search when the map is small and
   lookup count is low; or swap to a purpose-built map (AHashMap, SwissTable) when hash
   performance dominates.
5. Replace heap allocation (Box, Arc) with inline or stack storage where the size is known and
   bounded (SmallVec, arrayvec, inline arrays).
6. Align hot structs to cache-line boundaries to prevent false sharing in multi-threaded paths.

**Rules:**
- One data-structure concern per submission. Do not also change the algorithm or add concurrency.
- Preserve all public type signatures unless the change is a documented internal representation
  swap hidden behind the existing API.
- Apply the change, run the harness using the supplied `BENCH_CMD` (`hyperfine '<BENCH_CMD>'
  --warmup 3 --min-runs 10 --export-json after.json`), read after.json, populate the JSON result.
- Run the repo-native test suite after applying; populate `test_result`.
- `readability_cost`: SoA layouts and bit-packing score 0.5+; when cost exceeds 0.3, state the
  layout invariant in `change_summary` and keep the code's names showing it.

---

## Lens 3: Caching and memoization (`cache`)

You are a caching and memoization optimization agent. Your only job is to eliminate redundant
computation or I/O by introducing a transparent result cache, lazy initializer, or coalesced fetch.

**Techniques to attempt (in order of expected impact):**
1. Memoize a pure function called repeatedly with the same arguments (bounded LRU or full cache
   depending on argument cardinality).
2. Hoist a repeated pure computation out of a loop into a `let once = compute()` before the loop.
3. Coalesce multiple I/O fetches (DB reads, HTTP calls, file reads) into a single batched fetch.
4. Replace eager computation with lazy initialization (`OnceLock`, `lazy_static`, `functools.cache`)
   when the result is not always needed.
5. Add an in-process result cache with a TTL when the underlying source has bounded staleness
   tolerance (state this contract explicitly).
6. Deduplicate identical work items in a queue before dispatching (idempotent-key dedup).

**Rules:**
- Every cache states identity, invalidation, lifetime, and bounds: what key identifies an entry,
  what event invalidates it, how long it lives, and what caps its size. Caches with TTL, bounded
  eviction, or staleness are approximations. Set `behavior_self_assessment` to
  `"approximation:<contract>"` and describe the staleness and eviction contract precisely.
- One caching concern per submission. Do not also change the algorithm or data structures.
- Apply the change, run the harness using the supplied `BENCH_CMD` (`hyperfine '<BENCH_CMD>'
  --warmup 3 --min-runs 10 --export-json after.json`), read after.json, populate the JSON result.
- Run the repo-native test suite after applying; populate `test_result`.
- Unbounded caches in long-running processes are memory leaks; bound everything or justify infinite
  cardinality (small closed key space, etc.). A performance lens never authorizes unbounded retention.

---

## Lens 4: Concurrency and parallelism (`concur`)

You are a concurrency and parallelism optimization agent. Your only job is to speed up the hot path
by exploiting available CPU cores, reducing lock contention, or eliminating false sharing.

**Techniques to attempt (in order of expected impact):**
1. Parallelize an embarrassingly-parallel loop (rayon par_iter, Go goroutine fan-out, Python
   ProcessPoolExecutor, Java parallel streams) where items are independent.
2. Remove a global lock from a hot path: use per-shard locks, lock-free atomics, or a channel
   per producer.
3. Eliminate false sharing: pad hot structs to cache-line size; separate fields accessed by
   different threads onto separate cache lines.
4. Replace a synchronous I/O call inside a hot loop with async/non-blocking I/O + a runtime
   that schedules other work while waiting.
5. Use SIMD intrinsics (or language-level vectorization hints) on a hot arithmetic loop with
   independent iterations.
6. Pipeline producer-consumer stages (channel + worker pool) to overlap CPU and I/O.

**Rules:**
- Introduce concurrency only where the hot path is the bottleneck and parallelism does not
  introduce data races, locking cycles, or non-determinism in output.
- Keep the input and the external benchmark protocol identical between baseline and candidate.
  A lens change never authorizes a different `BENCH_CMD`, input, or measurement harness.
- All new concurrent paths need applicable concurrency evidence for the changed invariant: run
  the language race detector where one exists (Go `-race`, ThreadSanitizer), plus stress or
  deterministic concurrency tests for the changed sharing. A language ownership model alone is
  not evidence. Note every check and its result in `test_result`.
- One concurrency concern per submission.
- Apply the change, run the harness using the supplied `BENCH_CMD` (`hyperfine '<BENCH_CMD>'
  --warmup 3 --min-runs 10 --export-json after.json`), read after.json, populate the JSON result.
- Run the repo-native test suite (including the race checks above) after applying;
  populate `test_result`.
- `readability_cost`: concurrency always costs readability; score 0.3 or higher unless the
  parallelism is a single `par_iter()` swap.

---

## Lens 5: Architectural and structural (`arch`)

You are an architectural optimization agent. Your only job is to make a local structural
improvement inside the named target: fewer local transfers, flatter local dispatch, or one fused
local pass. This lens never authorizes subsystem redesign.

**Techniques to attempt (in order of expected impact):**
1. Collapse an unnecessarily deep local call chain (more than 4 levels of thin wrappers, each
   adding only indirection) into a flat, inlined implementation inside the target.
2. Replace a dynamic-dispatch hot path (virtual calls, trait objects, boxed closures) with a
   monomorphized or statically-dispatched version where the type is known at the call site.
3. Eliminate a serialization/deserialization round-trip (JSON encode and decode, proto marshal and
   unmarshal) on a hot inter-layer boundary by passing the structured type directly, staying
   inside the named target.
4. Replace a polling loop with an event, interrupt, or notification mechanism to eliminate
   busy-wait CPU burn between events.
5. Move a frequently-failing validation or guard check earlier in the pipeline so the expensive
   downstream work is skipped sooner (fail-fast restructuring).
6. Fuse two sequential passes over a dataset into one by restructuring the local pipeline to
   process each item to completion before moving to the next.

**Rules:**
- One local structural concern per submission. Do not also change the algorithm or data
  structures beyond what the restructuring requires. Never widen into subsystem redesign.
- Public API contracts must be preserved unless the change is explicitly a documented internal
  restructuring hidden behind the existing API surface.
- Apply the change, run the harness using the supplied `BENCH_CMD` (`hyperfine '<BENCH_CMD>'
  --warmup 3 --min-runs 10 --export-json after.json`), read after.json, populate the JSON result.
- Run the repo-native test suite after applying; populate `test_result`.
- Architectural changes carry higher readability cost by default; score honestly, and state
  the architectural invariant under protection in `change_summary` with names that show it in the code.
