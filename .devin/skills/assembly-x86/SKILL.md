---
name: assembly-x86
description: 'Use when reading GCC or Clang x86-64 assembly, writing inline asm, decoding AT&T syntax, or applying System V AMD64 register rules. Not for SIMD intrinsic selection.'
---

# x86-64 assembly

GCC and Clang emit AT&T syntax by default. This skill reads that output, writes inline asm, and keeps register use inside the System V AMD64 ABI. Bring the C or C++ source, the compiler output, or the assembly fragment under discussion; also bring which compiler produced it, since AT&T versus Intel output and inline asm details follow the compiler, and which ABI applies, since System V (Linux, macOS) and the Microsoft x64 ABI use entirely different register maps.

Everything here is read-only. The skill explains and drafts; edits land through the normal coding path. Nothing mutates a remote resource. The work is done when the drafted assembly assembles with `gcc -c` or `clang -c`, or when the compiler output under discussion is explained register by register.

## Start from the compiler's own output

Read the compiler's output before writing anything. Get the disassembly of the function under discussion on screen first:

```bash
gcc -O2 -S -fverbose-asm foo.c -o foo.s
gcc -O2 -c foo.c -o foo.o && objdump -d -M intel foo.o
```

## Map every register by role

Classify each register in the fragment before interpreting what the code does:

| Register | 32-bit view | Role |
|----------|-------------|------|
| `rax` | `eax` | Accumulator, 1st return value, caller saved |
| `rbx` | `ebx` | Base, callee saved |
| `rcx` | `ecx` | 4th argument, caller saved |
| `rdx` | `edx` | 3rd argument, 2nd return value, caller saved |
| `rsi` | `esi` | 2nd argument, caller saved |
| `rdi` | `edi` | 1st argument, caller saved |
| `rbp` | `ebp` | Frame pointer, callee saved |
| `rsp` | `esp` | Stack pointer |
| `r8` to `r11` | | 5th through 8th arguments, caller saved |
| `r12` to `r15` | | Callee saved |
| `rflags` | `flags` | Condition codes |
| `xmm0` to `xmm7` | | FP and SIMD arguments and returns |
| `xmm8` to `xmm15` | | FP and SIMD scratch, caller saved |

System V argument order: integer and pointer args in `rdi, rsi, rdx, rcx, r8, r9`, then the stack; float and vector args in `xmm0` to `xmm7`. A value that disappears across a call was sitting in a caller-saved register; keep such values in `rbx`, `r12` to `r15`, or spill them.

## Keep the stack aligned and name the red-zone choice

`rsp` stays 16-byte aligned before a `call`, because the call pushes 8 bytes and the callee expects alignment. A crash right after a `call` in hand-written asm is stack misalignment until proven otherwise; re-align `rsp` to 16 before every call site. The red zone is the 128 bytes below `rsp` that leaf functions may use without adjusting `rsp`; kernel code compiles with `-mno-red-zone` because interrupts do not honor it. State the red-zone choice in every drafted prologue:

```asm
push rbp
mov  rbp, rsp
sub  rsp, 16        # keep rsp a multiple of 16 before call sites
```

## Read the recurring instruction shapes

Parse each line of the fragment against these shapes:

| Pattern | Meaning |
|---------|---------|
| `mov %rdi, -8(%rbp)` | Store the first argument to a local slot |
| `mov (%rdi), %rax` | Load 8 bytes from the address in `rdi` |
| `lea 8(%rdi), %rax` | Compute an address without memory access |
| `addq $8, %rdi` | Advance a pointer by one element |
| `push %rbp` then `pop %rbp` | Frame save and restore |
| `call func` then `ret` | Call pushes the return address, `ret` pops it |
| `leave` | `mov %rbp, %rsp` then `pop %rbp` |
| `test %rax, %rax` | Set flags from `rax == 0` cheaply |
| `cmp $0, %rax` | Same flag result, one byte longer |
| `sete %al` | Copy `ZF` into a byte register |
| `cmovne %rdx, %rax` | Conditional move, branchless select |

## Pick one syntax and stay in it

AT&T puts the source operand first and prefixes registers and immediates; Intel puts the destination first. A file that mixes syntaxes fails to build; convert against `objdump -M intel` as reference and compile with one syntax throughout.

| AT&T | Intel |
|------|-------|
| `mov %rax, %rbx` | `mov rbx, rax` |
| `mov $8, %rax` | `mov rax, 8` |
| `movb %al, (%rdi)` | `mov byte ptr [rdi], al` |
| Default in GCC | `-masm=intel` or `objdump -M intel` |

## Write inline asm with the extended syntax

The template lists outputs, inputs, and clobbers. Constraint codes: `r` general register, `a`/`b`/`c`/`d` specific ones, `m` memory, `i` immediate. Tell the compiler about memory effects with `"memory"`. A result that goes wrong at `-O2` is a missing `volatile`, a wrong constraint, or a missing `"memory"` clobber; fix the declaration, not the build flags.

```c
static inline long cpuid_leaf(long leaf) {
    long a, b, c, d;
    __asm__ volatile("cpuid"
                     : "=a"(a), "=b"(b), "=c"(c), "=d"(d)
                     : "a"(leaf));
    return a;
}
```

```c
static inline int atomic_incr(int *p) {
    int ret;
    __asm__ volatile("lock xaddl %0, %1"
                     : "=r"(ret), "+m"(*p)   // +m: read and written
                     : "0"(1));
    return ret;   // returns the previous value
}
```

The `lock` prefix needs a memory destination; a rejection means the destination is a register or the assembler is in 16-bit mode.

## Attribute vector code to its instruction set level

`<xmmintrin.h>` provides SSE, `<emmintrin.h>` SSE2, and `<immintrin.h>` everything through AVX-512. Choosing and writing intrinsics is outside this skill; name the level and stop there.

Hand back annotated assembly or inline asm with register roles, stack alignment stated, and clobbers justified. The full instruction tables, flags register map, conditional jump list, and prologue patterns live in `references/reference.md`.
