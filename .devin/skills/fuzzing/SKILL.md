---
name: fuzzing
description: 'Use when planning an end-to-end fuzzing program for a project: engine and target selection, corpus management, and CI or nightly wiring. Harness design follows the step 1 contract inline (function of arbitrary bytes; no filtering or early return; deterministic re-runs). Not for engine operation or triage: use libfuzzer. Not for sanitizer flag reference: use sanitizers.'
---

# Fuzzing

A fuzzing program turns a parser, deserializer, codec, or API boundary into a machine that eats arbitrary bytes for hours and tells you exactly which bytes broke it. Your job covers the whole arc: a harness the fuzzer can trust, an engine built with the right sanitizers, a seeded and minimized corpus, reproduced and minimized findings, and a CI or nightly plan that keeps regressions from merging.

This stays local and reversible. You write fuzz binaries, corpora, dictionaries, findings, and logs under the project tree, and rollback is deleting those directories. No remote mutation.

## What to have in hand

The library or entry point to fuzz, ideally a parse or I/O boundary. Known good inputs from tests or real traffic, when they exist, because real seeds cut time to coverage sharply. A toolchain with Clang for libFuzzer or AFL++ installed for fork mode fuzzing (grounded channels are Clang 23.1.4, where libFuzzer ships inside, and AFL++ v5.03c, which is AGPL 3.0+ since v5.00c with mixed licensing in the repo). And a time budget, seconds for CI regression runs or hours for nightly work.

Running a campaign day to day, or triaging what one found, belongs to libfuzzer. Sanitizer flag questions belong to sanitizers.

## Write a harness the fuzzer can trust

The target is a function of arbitrary bytes, and the harness owns every guarantee:

```c
// fuzz_parser.c
#include <stdint.h>
#include <stddef.h>
#include "myparser.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    MyParser *p = parser_create();
    if (p) {
        parser_feed(p, (const char *)data, size);
        parser_destroy(p);
    }
    return 0;
}
```

Return 0 for uninteresting input instead of exiting, and never call `abort` or `exit`. Never read or write outside `[data, data + size)`. Keep no state between calls. Stay fast, since the fuzzer calls the harness millions of times. Feed converted input directly to the target with no filtering, normalization, or early return. Seed random sources, disable clocks and timeouts on the harness path, and isolate global state so repeated runs reproduce. Move on when the harness passes review against each of these rules. Harness templates and the full flag tables live in `references/targets.md`.

## Build, seed, and run

Build with libFuzzer and the sanitizer set. `-fsanitize=fuzzer` links libFuzzer and supplies `main`, so the target must not define one:

```bash
clang -fsanitize=fuzzer,address,undefined -fno-omit-frame-pointer -g -O1 \
    fuzz_parser.c myparser.c -o fuzz_parser
```

The binary links cleanly with no duplicate `main` and runs `-help=1` without error before you proceed.

Seed and run:

```bash
mkdir -p corpus
cp tests/inputs/* corpus/          # real seeds sharply cut time to coverage
./fuzz_parser corpus/ -max_len=65536 -timeout=10
./fuzz_parser corpus/ -max_total_time=3600
./fuzz_parser corpus/ -jobs=4 -workers=4
```

Defaults worth knowing: `-max_len` is 4096 when unset, `-timeout` is 1200 seconds, `-rss_limit_mb` is 2048, `-error_exitcode` is 77, `-len_control` is 100. Workers default to half the core count when unset. Proceed when the run consumes the corpus and reports new coverage.

Add AFL++ where process level isolation or non library targets are needed:

```bash
afl-clang-fast -g -O1 -o prog_afl main.c myparser.c
afl-fuzz -i afl-input -o afl-output -- ./prog_afl @@    # @@ = input file path
afl-fuzz -i afl-input -o afl-output -- ./prog_afl       # stdin target: drop @@
```

Persistent mode avoids a fork per input and raises throughput for library targets, and `__AFL_LOOP(1000)` bounds each iteration batch. Scale out with `-M main` plus one `-S name` instance per spare core, and read status with `afl-whatsup afl-output`. Proceed when at least one AFL++ instance reports stable cycles with new paths.

## Treat the corpus as an asset

Merge runs down to the coverage unique subset and keep the corpus in version control or CI cache:

```bash
./fuzz_parser -merge=1 corpus_min/ corpus/ run1/ run2/
afl-cmin -i afl-output/default/queue -o corpus_min -- ./prog_afl @@
./fuzz_parser corpus/ -runs=0 -print_coverage=1     # coverage of the corpus
```

You are done here when one minimized corpus exists and reproduces the union of coverage.

## Guide mutation past tokens and headers

When the format has tokens, hand the fuzzer a dictionary:

```c
# parser.dict
kw1="<"
kw2=">"
null_byte="\x00"
magic1="\x89PNG"
```

```bash
./fuzz_parser corpus/ -dict=parser.dict
afl-fuzz -i corpus/ -o out/ -x parser.dict -- ./prog_afl @@
```

For structured formats that checksum or length prefix, implement `LLVMFuzzerCustomMutator` and repair the invariant after `LLVMFuzzerMutate`, or the fuzzer never passes the header. Move on when deep paths are reached without human crafted inputs.

## Reproduce and minimize every finding

Artifacts land as `crash-<hash>`, `oom-<hash>`, or `timeout-<hash>` in the artifact prefix directory:

```bash
./fuzz_parser crash-abc123                 # reproduce
./fuzz_parser -minimize_crash=1 -max_total_time=60 crash-abc123
```

Re-run the minimized case under gdb (`gdb --args ./fuzz_parser crash-min`) to name the faulting frame. A finding counts when one small input reproduces the bug deterministically. A harness fault is fixed in the harness, never in the target. A target crash keeps its input, stack trace, and environment verbatim and is reported without suppressing or repairing it in the harness.

## Wire CI as a fixed time regression

```yaml
- name: Build fuzz target
  run: |
    clang -fsanitize=fuzzer,address,undefined -g -O1 \
      fuzz_parser.c myparser.c -o fuzz_parser
- name: Fuzz regression (60 seconds)
  run: |
    ./fuzz_parser corpus/ -max_total_time=60 -error_exitcode=1 \
      -artifact_prefix=artifacts/
- name: Reproduce known crashes
  run: |
    for f in known_crashes/*; do ./fuzz_parser "$f" || exit 1; done
```

Open ended runs do not belong in pull requests. Longer campaigns go to scheduled jobs with `-max_total_time=3600` or to OSS-Fuzz infrastructure. The gate holds when a pull request cannot merge with a target that regresses.

## Cover the other language boundaries

Python targets go through Atheris, and Zig targets through the built-in fuzzer (Zig 0.14.0 and later):

```python
import atheris, sys

with atheris.instrument_imports():
    import myparser

def TestOneInput(data: bytes) -> None:
    fdp = atheris.FuzzedDataProvider(data)
    try:
        myparser.parse(fdp.ConsumeString(sys.maxsize))
    except myparser.ParseError:
        pass

if __name__ == "__main__":
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()
```

```bash
zig build test --fuzz
```

Each language boundary gets its own target or a recorded decision not to fuzz it.

## When the run misbehaves

| Failure class | Behavior |
|---|---|
| Fuzzer finds no coverage growth | The harness or sanitizer set blocks depth. Check that `-fsanitize=fuzzer` is in the build and seeds are real inputs. |
| Crash does not reproduce | The bug depends on corpus state or is flaky. Re-run the single input ten times; check for uninitialized reads (initcheck) or a race. |
| OOM artifacts flood the run | Lower `-rss_limit_mb`, cap `-max_len`, or bound allocations inside the harness. |
| AFL++ target dies at startup | Memory limit too low for the target. Raise `-m` or add `-t` for slow inputs. |
| CI run too slow | Shrink `-max_total_time`, run `-workers=$(nproc)`, and cache the corpus between runs. |
| Fuzzer slows to a crawl mid-run | The target leaks or retains state between calls. Audit the harness against the step 1 rules. |
| Harness fault versus target crash | Fix the harness, never the target, for harness faults; preserve each target crash with its input, stack trace, and environment verbatim and report it without suppressing or repairing it in the harness. |

What you leave behind is the built targets, the seeded and minimized corpora, the crash reproduction commands, and the CI configuration, with every finding carrying its minimized artifact and the sanitizer report that explains it.
