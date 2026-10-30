---
name: c-hardening-baseline
description: 'Use when C code is written or audited and needs a pure-C baseline: standard, undefined behavior, integer and buffer safety, sanitizers, fuzzing, build flags. Not for C++.'
disable-model-invocation: true
---

# C hardening baseline

This skill produces a pure-C hardening policy as a chat report. It writes nothing: no source or build file is modified, and no remote resource is touched. It never prescribes a C++ idiom (RAII, destructors, smart pointers, lock guards, containers) as C practice; any C++ prescription found in a source or a prior draft is dropped from the report and listed under dropped prescriptions.

Bring the C source or build files under review. Also bring the compiler vendor and version (for example GCC 16.2 or Clang 23.1.0) and the active C standard (the `-std=` value or the project-agreed standard) whenever they cannot be read from the build files. Existing warning, hardening, sanitizer, and fuzzing configuration (`CMakeLists.txt`, `meson.build`, `Makefile`, CI job files) sharpens the report when available.

The work is done when the report names the C standard with the supporting compiler, the undefined-behavior catalog with the sanitizer that traps each entry, the integer and buffer rules with their checked-arithmetic form, the hardening flag set the identified compiler accepts, the sanitizer and fuzzing jobs for CI, and the findings the audit checklist produced. No partial result counts as complete: when a step cannot finish, the report states which steps succeeded and which are blocked.

## Pin the compiler and the C standard

Identify the compiler, its version, and the active standard from the build files or the supplied inputs, and record whether C++ appears anywhere in the tree. When the compiler or standard cannot be determined, report the ambiguity with the evidence examined and stop; guidance stays blocked until both are named. C++ files in the tree are out of scope and reported as such; this baseline applies to the C files only.

C23 (ISO/IEC 9899:2024) is the current published standard. Pin `-std=c23` when the compiler accepts it; GCC 16.2 and Clang 23.1.0 both do. On an older toolchain fall back to `-std=c17` and list which C23 controls the fallback loses (`<stdckdint.h>`, `static_assert` as a keyword, `nullptr`, `[[nodiscard]]` and the other standard attributes), with the C17 replacement for each (`__builtin_*_overflow` for `<stdckdint.h>`, `_Static_assert` for `static_assert`). Use `-std=c23` or `-std=c17`, not the `gnu` spellings, unless the code needs a GNU extension and a comment names it.

## Catalog the undefined behavior

Undefined behavior is not implementation-defined and not "works on my machine": it is permission for the optimizer to assume the program never does the thing. A single instance on a reachable path can delete a bounds check or miscompile a loop, and a clean debug build proves nothing. Scan for the high-frequency classes and report each occurrence with `file:line`:

- Signed integer overflow. `INT_MAX + 1` is UB, so the compiler may assume `x + 1 > x` and remove the overflow check. Unsigned overflow wraps by definition and is not UB, but a wrap that feeds a size is still a bug.
- Out-of-bounds access, including one past the end for a dereference.
- Read of an uninitialized automatic variable. Initialize at declaration.
- Null, misaligned, or invalid pointer dereference. The optimizer may delete null checks that follow a dereference.
- Strict aliasing violation: access to an object through a pointer of an incompatible type. Type-pun through `memcpy` or through a union; `char` and `unsigned char` may alias anything.
- Data race: concurrent access to a non-atomic object with at least one writer and no happens-before relation. Use `<stdatomic.h>` or a mutex.
- Invalid shift: by a count at or past the width, or by a negative count.
- Modification of a `const` object, a call through a function pointer of the wrong type, and an infinite loop with no side effects.

## Apply the integer and buffer rules

Report each violation with `file:line` and its replacement:

- Validate ranges before the arithmetic that feeds an allocation size, an array index, a `memcpy` length, or a loop bound. Overflow into a small allocation followed by a large copy is the classic remote code execution shape.
- Use checked arithmetic: `ckd_add`, `ckd_sub`, and `ckd_mul` from `<stdckdint.h>` under C23, or `__builtin_add_overflow`, `__builtin_sub_overflow`, and `__builtin_mul_overflow` on GCC and Clang under C17.
- Use `size_t` for sizes and indexes. Guard the order of an unsigned subtraction: `a - b` wraps when `b > a` and the result passes every upper-bound check.
- Compile with `-Wconversion -Wsign-conversion` and fix narrowing and sign changes at the source.
- Pass a length with every pointer and check it. Prefer `snprintf` and explicit length checks over unbounded copies. Never compute `ptr + n` from an attacker-controlled `n` before comparing `n` against the real remaining length.
- Check every allocation return. `realloc` returning `NULL` must not overwrite the original pointer, or the block leaks. Use a temporary.
- Pair every `malloc`, `calloc`, or `realloc` with exactly one `free` on every exit path, and every `fopen` with `fclose`. Use the goto-cleanup idiom, a single exit label that releases what was acquired, so an early error return cannot skip a release.
- Do not trust an embedded length field from the wire or from a file. Cap it against the remaining buffer before use.
- Replace banned functions on sight: `gets` (removed in C11; use `fgets`), `strcpy` and `strcat` (use `snprintf` or `strlcpy` where the platform provides it), `sprintf` and `vsprintf` (use `snprintf` and `vsnprintf`), `scanf("%s")` without a width (add a width or parse by hand), `system` and `popen` with interpolated input (use `posix_spawn` or `execve` with an argument vector), `strtok` (use `strtok_r`), `alloca` and a VLA sized from input (use the heap with a checked size), `atoi` and `atol` (use `strtol` with range and `errno` checks).
- Never pass user data as a format string. `printf(user)` reads and writes memory through `%n`. Write `printf("%s", user)` and compile with `-Wformat -Wformat=2 -Werror=format-security`.
- Never use `rand` or `random` for keys, tokens, IVs, or salts. Use `getrandom(2)` or `arc4random_buf` where the platform provides it, or a vetted library.
- Zero secrets after use with a wipe the compiler cannot elide (`explicit_bzero` or `memset_s` where available). A plain `memset` before a `free` can be optimized away.
- `assert` is compiled out under `-DNDEBUG`, which the common release presets set. A bounds or validation check written as `assert` does not exist in the shipped binary. Write it as an explicit `if` that returns or aborts, and keep `assert` for internal invariants.
- Canonicalize paths with `realpath` before checking them, prefer `openat` with `O_NOFOLLOW`, and operate on file descriptors to avoid check-then-use races.

## Recommend the hardening flags the compiler accepts

Report the flags the identified compiler accepts, split by compiler where support differs. Do not edit build files. Both GCC 16.2 and Clang 23.1.0 accept:

- Warnings: `-Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Wshadow -Wcast-align -Wnull-dereference -Wdouble-promotion -Wimplicit-fallthrough -Wformat=2 -Wshift-overflow=2 -Wvla -Wbidi-chars=any -Wtrampolines`, with `-Werror` in CI. A clean `-Wall -Wextra` build is the floor, not the goal.
- Fortification and stack: `-O2 -D_FORTIFY_SOURCE=3 -fstack-protector-strong -fstack-clash-protection -fstrict-flex-arrays=3 -ftrivial-auto-var-init=zero`.
- Control flow on x86-64: `-fcf-protection=full`.
- Position independence and link: `-fPIE -pie -Wl,-z,relro -Wl,-z,now -Wl,-z,noexecstack`, and `-Wl,-z,nodlopen` for an executable that no one loads with `dlopen`.
- Reproducibility: `-ffile-prefix-map=<src>=.` and `SOURCE_DATE_EPOCH`, so a path or timestamp does not leak into the binary. Keep `-g` and ship split debug symbols.

GCC only: `-fhardened` (an umbrella that enables a subset of the above; verify the subset against the GCC version in use) and `-fzero-init-padding-bits=all`. Clang rejects both; omit any flag the compiler rejects, name the rejecting compiler, and recommend the subset that compiles cleanly. Missing hardening flags on a network-facing or setuid binary is a HIGH finding.

## Recommend the sanitizer and fuzzing matrix

Sanitizers ship inside GCC 16.2 and Clang 23.1.0 under `-fsanitize=`. They are for test and CI builds, never production; production uses the flag set above.

- Job one: `-fsanitize=address,undefined -fno-sanitize-recover=all -fsanitize-address-use-after-scope`, then the full test suite. Any abort is a CRITICAL or HIGH finding. Set `ASAN_OPTIONS=detect_leaks=1:strict_string_checks=1` and `UBSAN_OPTIONS=print_stacktrace=1`.
- Job two, for threaded code: `-fsanitize=thread`. ASan and TSan cannot run in one binary.
- Clang only: add `-fsanitize=integer` to catch defined-but-suspicious unsigned wrap. `-ftrapv` is the blunter GCC and Clang alternative for signed overflow.
- Valgrind Memcheck is the no-recompile fallback for a binary that cannot be rebuilt. It misses the stack and global overflows ASan catches; when a sanitizer is unavailable on the platform, name it, recommend Memcheck, and state what it misses.
- Do not fix a UBSan report by casting the diagnostic away. Fix the arithmetic or the access.
- Fuzzing: any code that parses untrusted bytes (network, file formats, decoders) gets a fuzz target. Prefer AFL++ v5.03c for a new target. libFuzzer ships inside Clang 23.1.0 via `-fsanitize=fuzzer` and receives bug fixes only, so an existing libFuzzer target stays supported but a new one belongs on AFL++. Pair every fuzz build with ASan and UBSan. Keep a seed corpus and a regression corpus in the repository. A new crash is a CRITICAL finding.
- Static analysis: `clang-tidy` with `bugprone-*`, `cert-*`, `clang-analyzer-*`, `misc-*`, `performance-*`, and `portability-*`, committed in `.clang-tidy`, and GCC `-fanalyzer` in a CI job. Commit a `.clang-format` and enforce it with `clang-format --dry-run --Werror`.
- Dependencies: one manifest and one lockfile, pinned versions, a generated SBOM, and the standard library preferred over a dependency.

## Run the audit checklist

Every pattern below is `grep -rnE` over `*.c` and `*.h`. Report each hit with `file:line` and severity, CRITICAL first:

- Banned functions, HIGH or CRITICAL: `\b(gets|strcpy|strcat|sprintf|vsprintf|scanf|system|popen|strtok|atoi|atol)\s*\(`.
- `alloca` and VLAs sized from input, HIGH: `\balloca\s*\(`, plus a build with `-Wvla` to list every VLA, then read each hit for the source of its size.
- Format string with a non-literal first argument, CRITICAL: `(printf|fprintf|snprintf|syslog|err|warn)\s*\([^"]*\)`.
- Overflow-prone size arithmetic, HIGH: `(malloc|calloc|realloc|alloca)\s*\([^;]*[*+][^;]*\)`, then check for `ckd_` or `__builtin_.*_overflow` in the same function.
- Check-then-use on paths, HIGH: `\b(access|stat|lstat)\s*\(`, then check whether the following open uses the checked name.
- Insecure randomness for secrets, HIGH: `\b(rand|random|srand)\s*\(`.
- Timing leak, MEDIUM: `memcmp` on a buffer named like a MAC, token, secret, or digest.
- Unchecked allocation, HIGH: each `= (malloc|calloc|realloc)\(` hit not followed by a `NULL` check.
- Missing hardening in the build, HIGH on a network or setuid binary: no `_FORTIFY_SOURCE`, `stack-protector`, `relro`, `fcf-protection`, or `PIE` in the build files.
- Missing sanitizer or fuzz job in CI, HIGH for input-parsing code: no `fsanitize`, `afl`, or `fuzzer` in the CI configuration.

## Verify every recommendation before reporting

Drop a flag the named compiler rejects and record the drop. Drop every C++ prescription and list it under dropped prescriptions. The report carries these sections: C standard (with the compiler and version behind the choice and the controls a C17 fallback loses); undefined-behavior catalog (each class found, with `file:line` and the sanitizer that traps it); integer and buffer rules (each violation with its replacement); hardening flags (per compiler, every rejected flag named); sanitizer and fuzzing matrix (CI jobs, fuzz targets, static analysis configuration, dependency policy); audit findings (each hit with `file:line` and severity); dropped prescriptions (every C++ idiom cut because it does not apply to C).
