---
name: fuzzing-obstacles
description: 'Use when asked to identify and bypass checksums, nondeterminism, or validation barriers that block fuzzing coverage. Not for dictionary creation: use fuzzing-dictionary. Local writes only.'
---

# Fuzzing obstacles

Some checks stand between the fuzzer and the code you want tested. A checksum that rejects every mutated input, a clock seeded random generator that makes runs unrepeatable, a validator that throws away all but one input in a million. Your job is to find the check that actually blocks coverage, bypass it only in fuzz builds, and show the coverage gain with an honest price tag on the divergence.

The boundary is absolute. Production behavior never changes. Every edit sits behind an explicit fuzzing build flag, and removing the conditional block (or the fuzz build configuration that defines the flag) restores the original behavior with no production side change. Nothing remote, no credentials, no publishing.

## Reach for seeds before patches

Building a dictionary for fixed-token gates belongs to fuzzing-dictionary. Measuring coverage or plateau analysis on its own is out of scope. And a better seed corpus or dictionary always comes before a patch. You only cut code when you have confirmed seeds cannot clear the obstacle.

## What to have in hand

The system under test source tree and its build system, plus a fuzzer harness and coverage tooling already producing a baseline report. If a seed corpus or dictionary exists, bring it, because you will try those first.

## Bypass one obstacle at a time

1. Find the real blocker. Run the fuzzer, inspect coverage for unreachable code, and look for checksum or hash verification ahead of deeper processing, calls to `rand()`, `time()`, or `srand()` with system seeds, validation functions that reject most inputs, or global state initialization that differs across runs. Confirm a better corpus or dictionary cannot clear it before you touch source.
2. Wrap the obstacle behind the fuzzing build flag so production still enforces it and only the fuzz build skips it. C and C++ use `FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION` (the libFuzzer, AFL++, LibAFL, and honggfuzz convention). Rust uses `cfg!(fuzzing)` (cargo-fuzz and libFuzzer). The per language bypass shapes live in `references/patch-patterns.md`.
3. Cut narrowly. Bypass one obstacle per patch and keep the cheap validation that guides the fuzzer at low cost (magic bytes, size checks). Skip only the specific check that blocks coverage.
4. Feed downstream code what it assumed. If code past the skipped check depends on a validated property (a divisor that is nonzero, a config that passed validation), supply a safe fallback value on the fuzzing branch instead of skipping wholesale. The safe default pattern is in `references/patch-patterns.md`.
5. Prove the gain. Rebuild with fuzzing instrumentation, run the fuzzer briefly, and compare line, basic block, and function coverage plus corpus diversity against the unpatched baseline. New code paths must be reachable, or the patched check was not the real blocker. In that case revert the conditional block and hunt for the next obstacle. Never stack unverified patches.
6. Price the lie. For each patch, decide whether skipping the check creates states production can never reach. Ask whether downstream code assumes validated properties, whether the skip could cause crashes impossible in production, and whether implicit state dependencies exist. Classify the risk as LOW, MEDIUM, HIGH, or MITIGATED with a rationale. A HIGH risk means narrowing the patch or restoring validation with safe defaults, not pressing on.
7. Write each patch down so the fuzzing versus production divergence stays visible to future maintainers.

What you leave behind is the set of conditional compilation patches (each gated, each documented), a coverage delta showing improved reachability over the unpatched baseline, and a per patch risk classification with rationale. An obstacle whose coverage never improves, or whose risk cannot be reduced to an acceptable level, ships as unresolved with its evidence. It is never marked done.
