# Sanitizer flags reference

Use this when you need the exact build flag or runtime option for a sanitizer run. Sanitizers ship with the compiler. You enable them with `-fsanitize=`. The entries below were checked against GCC 16.x and Clang 23.1.4.

## Quick table

| Sanitizer | Flag | GCC | Clang | Note |
|---|---|---|---|---|
| ASan | `-fsanitize=address` | yes | yes | |
| UBSan | `-fsanitize=undefined` | yes | yes | |
| TSan | `-fsanitize=thread` | yes | yes | Own build; never with ASan or MSan |
| MSan | `-fsanitize=memory` | no | yes | Every linked object must be instrumented |
| LSan | `-fsanitize=leak` | yes | yes | Standalone or included with ASan |
| CFI | `-fsanitize=cfi-*` | no | yes | Requires `-flto` |
| HWASan | `-fsanitize=hwaddress` | no | yes | arm64; newer x86-64 with LAM |
| MemTag | `-fsanitize=memtag-stack` | no | yes | AArch64 with `+memtag` march |

## Recommended flags for sanitizer builds

Recommend these three flags for each sanitized build. They keep stacks readable, add source locations to reports, and keep optimization representative while still finding bugs.

```bash
-fno-omit-frame-pointer
-g
-O1
```

## Recovery control

Abort on the first error in CI. Log and continue only when you need to collect several findings in one interactive run.

```bash
-fno-sanitize-recover=all
-fno-sanitize-recover=undefined
-fsanitize-recover=all
```

`-fno-sanitize-recover=all` aborts on the first error from each recoverable check. `-fno-sanitize-recover=undefined` aborts only on UBSan errors. `-fsanitize-recover=all` logs each recoverable error and continues. ASan errors always terminate; recovery mode does not apply to them.

## UBSan check selection

`-fsanitize=undefined` covers the undefined behaviors. Named checks extend or narrow that set.

`signed-integer-overflow` belongs to the undefined group. `unsigned-integer-overflow` is not undefined behavior, so enable it only when you explicitly want it.

```bash
-fsanitize=signed-integer-overflow
-fsanitize=unsigned-integer-overflow
-fsanitize=float-divide-by-zero
-fsanitize=float-cast-overflow
-fsanitize=null
-fsanitize=alignment
-fsanitize=bounds
-fsanitize=vptr
-fsanitize=pointer-overflow
-fsanitize=builtin
```

`bounds` covers array indexing with known bounds. `vptr` covers C++ virtual-call type checks. Clang groups several integer checks under `-fsanitize=integer`. GCC has no such group, so spell the checks out in portable builds.

## ASan-specific flags

`-fsanitize-address-use-after-scope` detects use-after-scope. `-fsanitize-address-use-after-return` detects use-after-return but runs slowly, so enable it only when you suspect that bug.

```bash
-fsanitize-address-use-after-scope
-fsanitize-address-use-after-return
```

## Runtime option variables

Set options as `ASAN_OPTIONS=key=value:key2=value2 ./prog`. The same colon-separated form applies to `UBSAN_OPTIONS`, `TSAN_OPTIONS`, and `LSAN_OPTIONS`.

### ASAN_OPTIONS

| Key | Default | Effect |
|---|---|---|
| `detect_leaks` | 1 | LeakSanitizer on |
| `abort_on_error` | 0 | `abort()` instead of `_exit()`; enables core dumps |
| `exitcode` | 1 | Exit code on error |
| `log_path` | stderr | Write reports to a file |
| `symbolize` | 1 | Symbolize; needs `llvm-symbolizer` in PATH |
| `fast_unwind_on_malloc` | 1 | Set 0 for accurate allocation stacks |
| `quarantine_size_mb` | 256 | Freed-memory quarantine before reuse |
| `handle_segv` | 1 | ASan intercepts SIGSEGV |
| `print_stats` | 0 | Memory statistics at exit |
| `check_initialization_order` | 0 | Static init order bugs |

### UBSAN_OPTIONS

| Key | Effect |
|---|---|
| `print_stacktrace=1` | Add the stack to each report |
| `halt_on_error=1` | Stop on the first error |
| `suppressions=file` | Suppression file |
| `log_path=file` | Write reports to a file |

### TSAN_OPTIONS

| Key | Effect |
|---|---|
| `halt_on_error=1` | Stop on the first race |
| `suppressions=file` | Suppress reviewed races |
| `report_signal_unsafe=0` | Quiet signal-handler warnings |

### LSAN_OPTIONS

| Key | Effect |
|---|---|
| `suppressions=file` | Suppress reviewed leaks |
| `report_objects=1` | Print leaked object addresses |
| `max_leaks=N` | Cap reported leaks |
