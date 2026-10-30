---
name: heaptrack
description: 'Use when tracking heap allocations on Linux with heaptrack: allocation hotspots, peak heap, temporary allocations, leaks, or a diff of two runs via heaptrack_print. Not for heap errors.'
---

# heaptrack

heaptrack (1.5.0 on the grounding host) intercepts `malloc`, `free`, `realloc`, and the C++ allocation operators through `LD_PRELOAD` or injection, records a backtrace per allocation, and compresses the trace to one file. `heaptrack_print` reads that file into four rankings: most calls, peak consumption, most temporary allocations, and leaks. It needs no rebuild and runs far faster than Valgrind's Massif.

## When this is the right tool

Reach for heaptrack when a program uses too much memory, allocates too often, or leaks, and you need the allocating call stacks, or when two builds must be compared for allocation behavior. On a platform without heaptrack, Valgrind's Massif answers the same heap questions at a much higher slowdown. When the only question is leaks with no profiling cost, LeakSanitizer (see `sanitizers`) is the cheaper path. Heap errors (overruns, use-after-free) are never a heaptrack job.

Everything heaptrack writes is reversible local state: data files (`heaptrack.<prog>.<pid>.zst`, or the `-o` target you name), `heaptrack_print` output files, and the test binary in the working directory. Rolling back is deleting them. It never mutates anything remote. The one cost to name up front is slowdown: the traced program runs slower while every allocation is unwound and logged.

## What you need before recording

- A target binary with debug info (`-g`, or a `RelWithDebInfo` CMake build) so backtraces carry function names and source lines. Keep the optimization level as in production.
- A representative workload. heaptrack records allocation counts, so the workload must exercise the suspected path or the rankings describe the wrong program.
- For Rust, the binary must use the system allocator (`#[global_allocator] static A: std::alloc::System = System;`) so the interposed `malloc` sees every allocation.
- For a comparison, two recorded data files.

## Record, read, compare

1. Record. `heaptrack ./myapp args` writes `heaptrack.myapp.<pid>.zst` in the current directory and prints the analyze command on exit. `heaptrack -o run1 ./myapp` names the file `run1.zst`. `heaptrack -p <pid>` attaches to a running process by injection, and `--record-only` skips the automatic analysis launch. Move on once the `.zst` file exists and heaptrack has printed its summary lines (`calls to allocation functions`, `temporary allocations`).
2. Print the summary and rankings with `heaptrack_print -f run1.zst`. In order come `MOST CALLS TO ALLOCATION FUNCTIONS`, `PEAK MEMORY CONSUMERS`, `MOST TEMPORARY ALLOCATIONS`, and a summary block:

   ```text
   total runtime: 2.34s.
   calls to allocation functions: 145234 (62064/s)
   temporary allocations: 89123 (38087/s)
   peak heap memory consumption: 45.23M
   peak RSS (including heaptrack overhead): 78.45M
   total memory leaked: 2.34M
   ```

   Each ranking entry reads `N calls to allocation functions with X peak consumption from` followed by the stack, leaf first. Toggle sections with `-p 0` (peaks), `-a 0` (allocation counts), `-T 0` (temporary), and `-l 1` (leaks, off by default). `-n 20` widens the reported peaks from the default 10; `-s` limits sub-peak backtraces. `-t 1` shortens template identifiers and `-m 1` merges backtraces (both on by default). Move on once all four rankings and the summary are captured.
3. Read each summary line against the code. `calls to allocation functions` high relative to work done means many small allocations, so pool or reserve. `temporary allocations` (freed before the next allocation) as a large share of calls means churn in a hot loop, so hoist the buffer. `peak heap memory consumption` is the live-heap maximum to hold against the memory budget. `peak RSS` includes heaptrack's own overhead and non-heap mappings, so compare peak heap between runs, never RSS. `total memory leaked` is bytes never freed at exit; the `-l 1` ranking names the stacks. Move on once each non-trivial line is tied to a call stack.
4. Draw the allocation flamegraph: `heaptrack_print -f run1.zst -F stacks.folded --flamegraph-cost-type peak` writes folded stacks (cost types `allocations`, `temporary`, `leaked`, `peak`), then `flamegraph.pl --countname bytes --title "Peak heap" stacks.folded > heap.svg` from `flamegraphs`. Move on once the SVG opens and the widest frame matches the top ranking entry.
5. Compare two runs with the built-in diff: `heaptrack_print -f after.zst -d before.zst` prints every ranking as the delta of `after` minus `before`, so a positive peak entry is a regression and a negative one an improvement. Move on once the top positive and top negative deltas are named with their stacks.
6. Export to Massif format only when a Massif-reading tool is already in the workflow: `heaptrack_print -f run1.zst -M run1.massif`, then `ms_print run1.massif`. Move on once `ms_print` renders the timeline.
7. Suppress known leaks from third-party code: write a suppression file with one `leak:<function pattern>` line per pattern and pass `--suppressions leaks.supp`. `--print-suppressions 1` lists the matches and the suppressed byte total, and `--disable-builtin-suppressions` reveals what heaptrack hides by default. Stop once the leak ranking holds only owned code.

## When the output looks wrong

- Stacks show only addresses: no debug info. Rebuild with `-g`; for Rust add `debug = true` to the profile.
- A Rust program records almost nothing: a custom global allocator bypasses `malloc`. Switch to `std::alloc::System` for the profiling build.
- `total memory leaked` is large but the program frees on exit paths: an exit through `_exit` or `quick_exit` skipped destructors. Read the leak stacks. A still-referenced global at exit is not a bug, and a suppression records that decision.
- The data file is huge: an allocation-heavy workload. Shorten the workload, or record only the phase under suspicion by attaching with `-p` after startup.
- `heaptrack -p` fails to attach: ptrace is restricted. Run as the process owner or propose `CAP_SYS_PTRACE`; otherwise start the program under heaptrack.
- A comparison shows every stack changed: different workloads, or non-deterministic addresses in symbols. Use identical inputs and `-m 1`, and compare peak heap totals first.

## What you hand back

An allocation report with the summary block, the top stacks by peak, by call count, and by temporary allocations, the leak records, the flamegraph path when one was drawn, the per-stack deltas when two runs were compared, and the data file paths. A finished report always names the top call stacks by peak bytes, by call count, and by temporary allocations, lists the leak records with their stacks, and, for a comparison, the per-stack delta between the two runs.
