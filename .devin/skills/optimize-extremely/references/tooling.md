# Choosing profilers and throwing together a benchmark harness

Used during target location and baseline pinning of the `optimize-extremely` campaign.
This matrix pairs profiling and location tools with benchmark harness templates.

## Which profiler and harness to reach for

| Language | CPU profiler | Memory/alloc profiler | Benchmark / differential |
|---|---|---|---|
| Rust | `samply record`, `perf record` + `flamegraph`, `cargo flamegraph` | `heaptrack`, `dhat`, `valgrind --tool=massif` | `criterion`, `iai-callgrind`, `hyperfine` |
| C / C++ | `perf record` + `flamegraph`, `valgrind --tool=callgrind`, `samply` | `valgrind --tool=massif`, `heaptrack`, `dhat` | `hyperfine`, `google/benchmark`, `criterion.rs` (C via cbindgen) |
| Python | `py-spy record --format flamegraph`, `scalene`, `cProfile` + `snakeviz` | `scalene` (memory mode), `tracemalloc`, `memray` | `pytest-benchmark`, `asv` (airspeed velocity), `hyperfine` |
| Go | `go tool pprof` (CPU profile via `runtime/pprof`), `go test -cpuprofile` | `go tool pprof` (heap), `runtime.MemStats` | `go test -bench -benchmem`, `benchstat`, `hyperfine` |
| Java / Kotlin | `async-profiler`, JFR (`jcmd <pid> JFR.start`) | JFR allocation events, Eclipse MAT on heap dump | JMH, `hyperfine` |
| JavaScript / TypeScript | Chrome DevTools, `node --prof` + `node --prof-process`, `clinic flame` | Chrome heap snapshot, `clinic doctor` | `tinybench`, `mitata`, `hyperfine` |
| OCaml | `landmarks`, `magic-trace`, `perf record` | `memtrace` + `memtrace-viewer`, `Statmemprof` | `bechamel`, `core_bench`, `hyperfine` |

Small fixed habits: `hyperfine` not `time`. `procs` not `ps`. `bat -P -p -n` not `cat`. `difft` not `diff`.
Always pass `--warmup 3 --min-runs 10` on hyperfine, and export JSON with `--export-json <path>`.
Profile in a release or optimized build, never debug. Benchmark the same binary that will ship.

---

## Borrowing a harness only when no benchmark exists

Use these when baseline pinning finds no existing benchmark harness for the hot path. The harness
is a throwaway instrument: its only purpose is to measure the hot path in isolation with realistic
inputs. Delete it after the campaign run unless the user asks to keep it as a regression guard.

### Where each toolchain expects its harness to live

- Python, TypeScript, OCaml: toolchain-agnostic runners discover files by path argument;
  write the harness directly to `.outline/optimize/<target>/` and invoke it from there.
- Rust (`cargo bench`): `cargo` discovers benches only under the project `benches/`
  directory (registered in `Cargo.toml` or auto-discovered by convention). Write the harness to
  `<project-root>/benches/bench_<target>.rs`. Run from `<project-root>` as shown. Remove after
  the run.
- Go (`go test -bench`): `go test` runs only within the package directory. Write the
  `_test.go` harness alongside the source file being benchmarked (same package directory). Run
  from that directory. Remove after the run.
- JMH (Java/Kotlin): JMH requires the benchmark to live in the standard JMH source layout
  (`src/jmh/java/` for Gradle, `src/test/java/` annotated appropriately for Maven). Write to
  that location; run the build task (`./gradlew jmh` or `mvn jmh:benchmark`) from the project
  root. Remove after the run.

The `BENCH_CMD` passed to lens agents must reflect the actual invocation path after placement.

### Rust: criterion

```rust
// <project-root>/benches/bench_<target>.rs  (toolchain-native; registered in Cargo.toml)
use criterion::{criterion_group, criterion_main, Criterion};
use <crate>::<module>::<hot_function>;

fn bench(c: &mut Criterion) {
    // Replace with realistic input that exercises the hot path.
    let input = setup_realistic_input();
    c.bench_function("<hot_function>", |b| b.iter(|| <hot_function>(criterion::black_box(&input))));
}

criterion_group!(benches, bench);
criterion_main!(benches);
```

Run: `cargo bench --bench bench_<target> -- --save-baseline before`

### Python: pytest-benchmark

```python
# .outline/optimize/<target>/bench_<target>.py
from <module> import <hot_function>

def test_<hot_function>(benchmark):
    input_data = setup_realistic_input()
    benchmark(<hot_function>, input_data)
```

Run: `pytest .outline/optimize/<target>/bench_<target>.py --benchmark-json before.json`

### Go

```go
// <pkg-dir>/bench_<target>_test.go  (alongside the source file under test, same package)
package <pkg>  // same-package: no import needed, call unexported functions directly

import "testing"

func Benchmark<HotFunction>(b *testing.B) {
    input := setupRealisticInput()
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        <HotFunction>(input)  // direct call, no package qualifier
    }
}
```

For exported-API-only hot paths, swap `package <pkg>` for `package <pkg>_test` and add
`import "<module>"`, then call `<module>.<HotFunction>(input)`.

Run: `go test -bench=Benchmark<HotFunction> -benchmem -count=10 .`
Diff: `benchstat before.txt after.txt`

### Java / Kotlin: JMH

```java
// src/jmh/java/BenchHotHotPath.java (Gradle) or src/test/java/ with @Fork (Maven)
@State(Scope.Thread)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@Warmup(iterations = 3)
@Measurement(iterations = 10)
public class BenchHotPath {
    private InputType input;

    @Setup
    public void setup() { input = setupRealisticInput(); }

    @Benchmark
    public ResultType bench() { return HotClass.hotFunction(input); }
}
```

Run: `./gradlew jmh` or `mvn jmh:benchmark`

### JavaScript / TypeScript: tinybench

```typescript
// .outline/optimize/<target>/bench.<target>.ts
import { Bench } from "tinybench";
import { hotFunction } from "<module>";

const bench = new Bench({ iterations: 100, warmupIterations: 10 });
const input = setupRealisticInput();

bench.add("<hotFunction>", () => { hotFunction(input); });

await bench.run();
console.table(bench.table());
```

Run: `npx tsx .outline/optimize/<target>/bench.<target>.ts`
Or via `hyperfine 'npx tsx bench.<target>.ts'` for wall-clock comparison.

### OCaml: bechamel

```ocaml
(* .outline/optimize/<target>/bench_<target>.ml *)
open Bechamel
open Toolkit

let test =
  Test.make ~name:"<hot_function>" (fun () ->
    let input = setup_realistic_input () in
    Staged.stage (fun () -> <Module>.<hot_function> input))

let () =
  let cfg = Benchmark.cfg ~limit:100 ~quota:(Time.second 5.) () in
  let ols = Analyze.ols ~bootstrap:0 ~r_square:true ~predictors:[| Measure.run |] in
  let results = Benchmark.all cfg [ test ] in
  let analysis = Analyze.all ols results in
  Bechamel_notty.Unit.run Fmt.stderr analysis
```

---

## Keeping measurements honest

- Standard deviation below 20 percent of median is the single acceptance condition. Above it,
  stop and fix measurement noise before proceeding.
  Causes: CPU frequency scaling, background load, cold cache, OS jitter.
  Fixes: `cpupower frequency-set -g performance`, `nice -n -20`, warm-up runs, pin to a core
  (`taskset 0x1`), disable turbo boost (`echo 1 > /sys/devices/.../no_turbo`).
- Always measure what ships. Optimize and benchmark the release build; debug builds have
  different inlining, bounds-check overhead, and optimization levels.
- Re-measure end to end at the integrated benchmark gate. A worktree win sometimes
  vanishes after integration due to changed inlining decisions, link order, or PGO profile
  invalidation. The integrated re-measure on the main tree before commit is the ground truth.
- Report variance, not just median. Commit body format: `After: <median> plus or minus <stddev>`.
  A 10 percent speedup with 15 percent stddev is noise; a 10 percent speedup with 1 percent
  stddev is a win.
