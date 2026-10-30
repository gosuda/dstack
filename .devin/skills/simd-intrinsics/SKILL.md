---
name: simd-intrinsics
description: 'Use when reading auto-vectorization reports, writing SSE2, AVX2, or NEON intrinsics, or fixing vectorization failures. Not for reading the asm itself: use assembly-x86.'
---

# SIMD intrinsics

Let the compiler vectorize first and write intrinsics where it cannot. Every intrinsic code path needs a runtime feature check and a scalar fallback, because the binary runs on CPUs the build machine never saw.

This skill explains and drafts. It is read-only: edits land through the normal coding path, and nothing touches remote. The job is done when the vector path is guarded by a compile-time target and a runtime feature check, the scalar fallback exists, and the speedup is measured on the target machine.

## What you need up front

- The hot loop or kernel. Required.
- The compiler and flags. Required, because vectorization reports differ between GCC and Clang.
- The deployment CPU range. Required before choosing the ISA level.

## Ask the compiler first

1. Check whether the loop vectorizes already. Clang prints remarks with `-Rpass`, `-Rpass-missed`, and `-Rpass-analysis`; GCC prints with `-fopt-info-vec`, `-fopt-info-vec-missed`, and `-fopt-info-vec-optimized`. Move on once the loop has a verdict with the reason.

```bash
clang -O2 -march=native -Rpass-missed=loop-vectorize src.c
gcc -O2 -march=native -fopt-info-vec-missed src.c
```

2. Fix the loop before reaching for intrinsics. The usual blockers and their fixes:

| Blocker | Fix |
|---------|-----|
| Loop-carried dependency | Restructure so iteration `i` reads only `i-1` or earlier |
| Early exit or data-dependent break | Move the exit into a mask or split the loop |
| Non-contiguous memory | Gather, scatter, or restructure to stride one |
| Possible aliasing | Add `__restrict` to the pointers |
| Unknown trip count | Keep a scalar tail loop |

```c
void addf(float *__restrict dst,
          const float *__restrict a, const float *__restrict b, size_t n) {
    for (size_t i = 0; i < n; i++)
        dst[i] = a[i] + b[i];
}
```

## Dispatch on the running CPU

3. Detect CPU features at runtime before any intrinsic path runs. Move on once dispatch selects the widest ISA the running CPU supports.

```c
#include <stdbool.h>

bool have_avx2(void) {
    return __builtin_cpu_supports("avx2");
}
```

For finer control, use `__cpuid` with `__builtin_cpu_supports` covering the common cases, and check `xgetbv` state through the compiler builtin for OS AVX support rather than reading registers by hand.

## The x86 kernels

4. Write the x86 paths. SSE2 moves four floats per `__m128`; AVX2 moves eight per `__m256`. Unaligned loads on modern x86 cost little, so use them unless profiling proves otherwise. Move on once each path compiles under its own feature guard and the tail stays correct.

```c
#include <immintrin.h>

#ifdef __AVX2__
void sum8_avx2(float *dst, const float *a, const float *b, int n) {
    int i = 0;
    for (; i + 8 <= n; i += 8) {
        __m256 va = _mm256_loadu_ps(a + i);
        __m256 vb = _mm256_loadu_ps(b + i);
        __m256 vc = _mm256_add_ps(va, vb);
        _mm256_storeu_ps(dst + i, vc);
    }
    for (; i < n; i++)
        dst[i] = a[i] + b[i];
}
#endif
```

FMA combines multiply and add and needs its own feature, so guard it:

```c
#if defined(__FMA__)
    __m256 vsum = _mm256_fmadd_ps(va, vb, vacc);
#endif
```

Compile the AVX2 translation unit with `-mavx2 -mfma`, or mark the single function:

```c
__attribute__((target("avx2,fma")))
void kernel_avx2(float *dst, const float *a, const float *b, int n) { }
```

## The ARM kernel and the final choice

5. Write the NEON path for ARM. NEON is baseline on AArch64, so no runtime check is needed there. Move on once the NEON path builds for `aarch64` and the 128-bit vector shape matches.

```c
#include <arm_neon.h>

void sum4_neon(float *dst, const float *a, const float *b, int n) {
    for (int i = 0; i + 4 <= n; i += 4) {
        float32x4_t va = vld1q_f32(a + i);
        float32x4_t vb = vld1q_f32(b + i);
        vst1q_f32(dst + i, vaddq_f32(va, vb));
    }
}
```

6. Decide between intrinsics and compiler builtins. Reach for intrinsics when the code needs shuffles, gathers, or horizontal reduction that auto-vectorization will not find, or when the report from step 1 names a pattern the compiler refuses. Prefer compiler auto-vectorization plus builtins like `__builtin_popcount` for element-wise arithmetic. Move on once the choice is written next to the kernel.
7. Mind alignment where it matters. Heap buffers can be aligned with `aligned_alloc(32, ...)` for AVX2, and `posix_memalign` covers POSIX builds. Unaligned loads are correct everywhere and nearly free on recent x86, so pay for alignment only with a measurement. Move on once alignment claims carry the measurement that justifies them.
8. Measure on the target machine. Compare against the scalar baseline with the real data size and record the counters or timing. Move on once the speedup number exists and names the machine and build flags.

## When it breaks

- Illegal instruction on an older CPU: the intrinsic path ran without its feature check, or the file was compiled with a global `-mavx2`. Restore the dispatch and scope the flag to the function.
- Auto-vectorization still refuses the loop: read the analysis remark. It names the memory dependence or the exit, so fix the named cause before writing intrinsics.
- Results differ from the scalar path: reassociation or FMA changed rounding. Compile with the intended FP contract and state it, or keep strict scalar for that kernel.
- NEON path fails on 32-bit ARM: AArch32 NEON types differ. Use the `aarch64` types only under `__aarch64__` and provide an AArch32 variant.
- No speedup on the target: memory bandwidth may be the wall. Measure with the cache counters before tuning the vector code further.

## What you hand back

The guarded vector kernel with its scalar fallback, the dispatch check, and the measured speedup with the build flags and machine named. The intrinsic lookup tables, type maps, and feature guard reference live in `references/intel-intrinsics-guide.md`.
