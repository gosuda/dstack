---
name: libfuzzer
description: 'Use when asked to build, run, or triage a coverage-guided C/C++ fuzz campaign on the libFuzzer or AFL++ engine. Not for harness design: use fuzzing.'
---

# libFuzzer and AFL++

This is the engine room work: compiling a harness into an instrumented binary, running a bounded campaign on it, and triaging whatever falls out. Designing the harness itself belongs to fuzzing. Your run ends with a binary that executed against its corpus and every crash artifact reproducing in the same target with identical sanitizer output or signal.

Approvals and limits first. In afl mode, ask the user before any package installation or Docker image pull. Kernel tuning that needs a reboot or degrades OS security is out of scope entirely. Otherwise this is reversible local work: the binary, corpus and output directories, crash files, and logs. Rollback is deleting them and killing campaign processes, with the afl variant spelled out at the end.

## What to have in hand

The engine, `libfuzzer` by default or `afl` when the user names AFL++, needs multi core `afl-fuzz` campaigns, or lacks a Clang libFuzzer runtime. Source or object files for the code under test. For libFuzzer, a Clang compiler (`clang++`) with the libFuzzer runtime present and one `LLVMFuzzerTestOneInput` harness function visible to the linker. For afl mode, `afl-fuzz` on the host or the `aflplusplus/aflplusplus` Docker image, plus a harness or a program that reads stdin, files, or argv.

Optional material: a seed corpus directory (it may be empty; when omitted, create `./corpus/` for libFuzzer or `seeds/` with one non-empty file for afl), a fuzzing dictionary file in the format below, libFuzzer Clang build flags (`-fsanitize=address`, `-fsanitize=undefined`, `-g`, `-O2`), libFuzzer runtime flags passed to the built binary (`-max_len`, `-dict`, `-timeout`, `-close_fd_mask`, `-fork`, `-ignore_crashes`), and for afl the run location (host or Docker, default Docker), instrumentation mode (LTO, LLVM, or GCC, default tries LTO then falls back to LLVM), core count (default single instance), and sanitizer selection (ASan, UBSan, or none, default none).

## Set up the engine

Choose the engine first. `libfuzzer` is the default, and `afl` is for the cases named above.

Then verify the toolchain before building anything. For libFuzzer, run `clang++ --version` and stop if Clang is absent, installing it before proceeding. For afl mode, verify `afl-fuzz --version` on the host or `docker run --rm aflplusplus/aflplusplus:stable afl-fuzz --version`, and request explicit approval before `apt install afl++ lld` or `docker pull aflplusplus/aflplusplus:stable`.

## Build the harness binary

For libFuzzer, compile with:

```
clang++ -fsanitize=fuzzer[,address,undefined] -g -O2 -U_FORTIFY_SOURCE <harness>.cc <target>.cc -o <binary>
```

`-fsanitize=fuzzer` links the libFuzzer runtime and provides `main`. Add `,address` for heap and stack buffer overflow, use-after-free, and double-free detection. Add `,undefined` for signed-integer overflow, null dereference, and similar undefined behavior. Add `-U_FORTIFY_SOURCE` when using ASan to avoid fortification interference. Omit `-fsanitize=address` for a faster build when only checking sanitizer-uncovered defects.

For afl mode there are two target shapes, each with one compile path.

A libFuzzer-signature `LLVMFuzzerTestOneInput` harness has no `main` of its own. Compile the harness only and let AFL++ supply the entry point. The documented recipe is the libFuzzer command with `clang++` swapped for `afl-clang-fast++`; the compiler intercepts `-fsanitize=fuzzer` and links `libAFLDriver.a` in its place:

```bash
afl-clang-fast++ -fsanitize=fuzzer -O2 harness.cc -o fuzz
```

Equivalently, link the driver library that ships built with AFL++:

```bash
afl-clang-fast++ -O2 harness.cc libAFLDriver.a -o fuzz
```

Do not compile a second `main.cc` next to the harness and do not set `-DNO_MAIN=1`; the driver owns `main`. `-fsanitize=fuzzer-no-link` only instruments objects and static libraries for a later link that supplies its own runtime: it never provides a driver or a `main`. Add `AFL_USE_ASAN=1` or `AFL_USE_UBSAN=1` when sanitizers are requested. The `-m` memory limit flag is unsupported with ASan because ASan reserves 20 TB of virtual memory; in multi-core setups run only one ASan job per 4-8 non-ASan jobs.

A program that reads stdin or files keeps its own `main` and needs no harness: compile it directly and fuzz via stdin or the `@@` file placeholder. Instrumentation mode applies on this path only: try `afl-clang-lto++` first, fall back to `afl-clang-fast++` if LTO fails to link, and use `afl-g++-fast` only when the project requires GCC (its version must match the version the AFL++ GCC plugin was built with):

```bash
afl-clang-fast++ -O2 program.cc -o fuzz
```

The binary compiles and links with the chosen instrumentation and sanitizer flags before you proceed.

## Seed and run the campaign

Prepare the corpus. For libFuzzer, create `<corpus_dir>/` and optionally seed it with valid example inputs for the target format. For afl mode, create `seeds/` with at least one non-empty file; for real projects gather representative inputs from example files, the project test suite, or minimal valid inputs for the target format.

Run the campaign. For libFuzzer:

```
<binary> [-max_len=<N>] [-timeout=<S>] [-dict=<dict_file>] [-close_fd_mask=3] [-fork=1 -ignore_crashes=1] [-jobs=<N> -workers=<N>] <corpus_dir>/
```

`-max_len` caps per-input byte size (twice the minimal realistic input is a reasonable start; omit it to let libFuzzer grow dynamically). `-timeout` aborts test cases exceeding that many seconds. `-dict` passes a fuzzing dictionary for format-aware mutation. `-close_fd_mask=3` closes stdout and stderr for a speed boost when the target writes to them. `-fork=1 -ignore_crashes=1` continues after a crash rather than exiting. `-jobs` and `-workers` run parallel jobs sharing the corpus.

For afl mode, set the environment that matters: `AFL_TMPDIR=/dev/shm` always (tmpfs improves performance and avoids SSD wear), `AFL_FAST_CAL=1` for slow targets (slower than 10 ms per exec), `AFL_TESTCACHE_SIZE=100` on all instances, `AFL_FINAL_SYNC=1` on the primary `-M` instance only (needed for later `afl-cmin`), `AFL_EXIT_ON_TIME=3600` or `AFL_EXIT_WHEN_DONE=1` for CI or automated runs, `AFL_NO_UI=1` for headless environments. Single core:

```bash
AFL_TMPDIR=/dev/shm afl-fuzz -i seeds -o out -- ./fuzz
```

Useful flags are `-G 4000` (max input length), `-t 1000` (per-case timeout in ms), `-m 1000` (memory limit in MB, never with ASan), and `-x ./dict.dict` (dictionary). Multi-core means one primary instance and one secondary per available core, all sharing the same `-o state` directory:

```bash
AFL_TMPDIR=/dev/shm AFL_FINAL_SYNC=1 AFL_TESTCACHE_SIZE=100 afl-fuzz -M primary -i seeds -o state -- ./fuzz 1>primary.log 2>primary.error </dev/null &
AFL_TMPDIR=/dev/shm AFL_TESTCACHE_SIZE=100 afl-fuzz -S secondary01 -i seeds -o state -- ./fuzz 1>secondary01.log 2>secondary01.error </dev/null &
```

The `</dev/null` redirect is required. A backgrounded process that reads the terminal receives `SIGTTIN` and stops without it. List running jobs with `jobs` and stop all with `kill $(jobs -p)`. For CMPLOG and RedQueen constraint solving, build with `AFL_LLVM_CMPLOG=1` and run one secondary with `-c0`. The campaign runs with the configured environment and core count before you call this stage complete.

## Read the output

For libFuzzer:

| libFuzzer line | Meaning |
|---|---|
| `INITED` | Initialization complete, corpus loaded |
| `NEW cov: N` | New coverage edge found; input added to corpus |
| `stat::cov: N` | Running coverage edge count |
| `exec/s: N` | Executions per second |
| `libFuzzer: deadly signal` | Crash: signal received (SEGV, ABRT, etc.) |
| `AddressSanitizer: <type>` | ASan violation: heap, stack, or global buffer overflow, use-after-free, double-free, or leak |
| `UndefinedBehaviorSanitizer: <type>` | UBSan violation: signed-integer overflow, null dereference, etc. |

For afl mode, read `fuzzer_stats` fields instead: `execs/sec`, `cycles done`, `corpus count`, `saved crashes`, `stability`.

The harness every campaign is built on looks like this:

```
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < <minimum>) return 0;      // reject undersized inputs
    // parse or pass data to target
    return 0;                            // always return 0
}
```

Do not call `exit()`, join all threads before returning, keep execution fast (hundreds to thousands of executions per second is the target), stay deterministic (no `rand()`, no reading from `/dev/random`), and reset global state between calls. AFL++ accepts the same harness as a persistent-mode entry point through the `libAFLDriver.a` link above; the driver runs the persistent loop itself, so the harness needs no `__AFL_LOOP`.

The dictionary is one quoted string per line with `#` marking a comment line:

```
"\\x89PNG"
"GET"
"Content-Type"
```

Generate entries from headers with `grep -o '"[^"]*"' <header.h>`, from binary strings with `strings ./binary | sed 's/^/"/; s/$/"/'`, or from man pages with `man <cmd> | grep -oP '^\s*(--|-)\K\S+' | sed 's/[,.]//g' | sed 's/^/"/; s/$/"/' | sort -u`. Pass the file with `-dict=` (libFuzzer) or `-x` (afl).

## Reproduce, minimize, and report

Collect crashes as they happen. With libFuzzer, when the binary exits with a deadly signal or sanitizer report, libFuzzer writes an artifact named `crash-<SHA1-hash-of-content>` in the current directory; record the artifact path and the sanitizer output. With afl mode and no TTY, `afl-fuzz` writes status to the log and to `state/<instance>/fuzzer_stats`; check status with `afl-whatsup state/`. Read `execs/sec` (higher is better), `cycles done`, `corpus count`, `saved crashes`, and `stability` (near 100 percent; below 85 percent indicates non-deterministic behavior). Coverage plots come from `afl-plot state/default out_graph/` (needs `gnuplot` on host; the Docker image ships `gnuplot-nox`). Crash files live in `state/default/crashes/` with the signal encoded in the filename (`sig:06`); hangs live in `state/default/hangs/`.

Reproduce each crash directly. libFuzzer: `<binary> ./crash-<hash>`. afl mode: `./fuzz state/default/crashes/<id>`. The same sanitizer error or signal must recur. When it does not, suspect non-determinism in the harness or target (remove random-number generators and uninitialized-memory reads). A crash counts as reproduced only with identical sanitizer output or signal, or with non-determinism identified as the cause.

Minimize and report. In afl mode, minimize the corpus to unique coverage with `afl-cmin -i state/default/queue -o minimized_corpus -- ./fuzz @@`, then stop all campaign processes with `kill $(jobs -p)`. An `afl-cmin` or `afl-cmin.bash` target must be given `-` for stdin or `@@` for file input even when `afl-fuzz` runs it with no argument in shared-memory mode. The report states the artifact path, the sanitizer violation type or signal, and whether reproduction succeeded. In afl mode it also covers the campaign output directory contents (`queue/`, `crashes/`, `hangs/`, `fuzzer_stats`, `plot_data`), a status summary (execs per second, cycles done, corpus count, saved crashes, stability), and the minimized corpus path when `afl-cmin` ran.

## When the campaign misbehaves

| Failure class | Diagnosis | Recovery |
|---|---|---|
| `no-clang` | `clang++ --version` fails or reports GCC | Install LLVM/Clang; re-run the build step |
| `link-error` | Undefined references to target symbols | Verify all source and library objects are passed to the compiler |
| `sanitizer-violation` (expected) | Deadly signal or sanitizer report during fuzzing | Artifacts written to `./crash-*`; reproduce per the step above; report type and artifact path |
| `hang` | No output for longer than the timeout interval | Increase `-timeout`; check whether the target enters an infinite loop or blocking I/O |
| `no-coverage` | Fuzzer runs but `stat::cov` never increases | Add seed corpus inputs; supply a dictionary; verify the harness calls the target; use `-runs=0 <corpus_dir>/` to exhaust the static corpus first |
| `non-reproducible` | Crash artifact does not reproduce | Remove non-determinism from harness and target; rebuild without `-fsanitize=fuzzer-no-link` |
| `corpus-exhausted` | `stat::cov` plateaus, no new coverage for extended runtime | Extend corpus, add dictionary, improve seed inputs, run coverage analysis |
| `afl-build-failure` | LTO link error | Fall back to LLVM mode (`afl-clang-fast++`); use `afl-g++-fast` only when the project requires GCC. Never proceed with an uninstrumented binary; it produces no coverage data |
| `afl-gcc-plugin-mismatch` | GCC plugin version mismatch | Match the system GCC to the AFL++ plugin build; install `gcc-<version>-plugin-dev`. Do not patch around the mismatch |
| `afl-low-stability` | `stability` below 85 percent | The target is non-deterministic; switch to stdin or file-input fuzzing or fix the non-determinism. Do not report done |
| `afl-low-throughput` | `execs/sec` below 1k | Use a persistent-mode `LLVMFuzzerTestOneInput` harness for 10-20x speedup, or set `AFL_TMPDIR=/dev/shm` |
| `afl-no-crashes` | Campaign finds nothing | Recompile with `AFL_USE_ASAN=1` or `AFL_USE_UBSAN=1`; memory corruption often does not crash without a sanitizer |
| `afl-asan-m-flag` | Memory limit exceeded with ASan | Remove `-m`; ASan reserves 20 TB of virtual memory |
| `afl-job-stopped` | Backgrounded job shows "Stopped" | The `</dev/null` redirect is missing; restart the job with it to avoid `SIGTTIN` |
| `afl-docker-tty` | Docker reports "input device is not a TTY" | Omit `-t` for non-interactive runs; for the interactive UI run in host mode in a terminal |

A campaign that finds no crash in its bounded run is a partial result, not a failure. Report the final coverage count and `non-converged`. In afl mode, an early-stopped campaign still leaves valid `queue/`, `crashes/`, and `fuzzer_stats` under `state/` or `out/`; report what was captured rather than discarding it.

Rollback for libFuzzer is deleting the compiled `<binary>`, the `<corpus_dir>/` contents, and any `crash-*` files. For afl mode, run `kill $(jobs -p)`, then remove `out/` or `state/`, log files, and the compiled binary. The target source is unchanged beyond compilation.

The terminal report classifies the run as `non-converged` (binary exits zero or no sanitizer violation, with final coverage count), crash found (artifact path, sanitizer violation type or signal, reproduction result), compilation failure (compiler error message), or a failure class name with diagnostic message.
