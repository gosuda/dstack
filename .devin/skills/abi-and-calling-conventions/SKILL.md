---
name: abi-and-calling-conventions
description: 'Use when explaining System V AMD64, ARM AAPCS, RISC-V psABI, stack frames, variadic calls, or FFI register rules. Not for the Rust FFI binding layer: use rust-ffi.'
---

# ABI and calling conventions

You answer which registers, stack rules, and variadic behavior apply at a call boundary on System V AMD64, AAPCS64 (AArch64), or the RISC-V psABI (RV64), and you prove it against the compiler. This skill reads source, disassembly, and compiler output and answers in chat. Compiler and disassembler runs write nothing outside stdout, nothing on disk changes, and there is no remote mutation. You are finished when the answer names the argument registers, return registers, stack alignment, callee-saved set, and variadic rule for the named ABI, and points to the compiler output that confirms it.

You need two things to start: the target ABI (System V AMD64, AAPCS64, or RISC-V psABI RV64) and the calling context (an assembly thunk, an inline asm clobber list, a mixed C and assembly boundary, a variadic wrapper, or an FFI signature). A crash on `call`, a wrong argument value, or a corrupted register after a call helps narrow the fault but is optional. For the Rust binding layer rather than the convention itself, use `rust-ffi`.

## Name the ABI before anything else

Name the ABI from the toolchain target and the platform, and move on once exactly one of the three is fixed. If the target is Windows x64, stop: the Microsoft x64 convention differs from System V (different register order, 32-byte shadow space, no red zone), so never apply System V rules to it. If the ABI cannot be inferred, ask for the toolchain target triple instead of guessing from the source language. Both sides of a mixed-ABI FFI must be built for the same target ABI, so check the compiler target on each side.

## State the register contract

Give the argument, return, alignment, and callee-saved rows for the named ABI before reasoning about the bug.

| ABI | Integer arguments | Float or vector arguments | Return | Stack alignment at call | Callee-saved |
|---|---|---|---|---|---|
| System V AMD64 | `rdi, rsi, rdx, rcx, r8, r9` | `xmm0` to `xmm7` | `rax` (`xmm0` for float or vector), plus `rdx` for 128-bit values | 16 bytes before `call` | `rbx, rbp, r12` to `r15`, `rsp` |
| AAPCS64 | `x0` to `x7` | `v0` to `v7` | `x0` and `x1`, or `v0` | 16 bytes | `x19` to `x28`, `x29` (frame pointer), `sp` |
| RISC-V psABI RV64 | `a0` to `a7` | `fa0` to `fa7` | `a0` and `a1` (`fa0` for float) | 16 bytes | `s0` to `s11`, `sp` |

Three details from the table cause most faults. System V AMD64 on Linux grants a 128-byte red zone below `rsp` that leaf functions use without adjusting the stack pointer. Arguments past the register set go on the stack, so a seven-integer C function on System V passes the seventh in memory. The link register is call-clobbered on all three ABIs: System V AMD64 pushes the return address before the call lands, and AAPCS64 and RISC-V save `x30`/`ra` in the prologue when the callee itself calls, which is why the callee-saved rows above exclude them. Treat a wrong float argument as a prototype mismatch first (a float without a prototype goes through integer promotion rules and lands in the wrong register class), and treat a corrupted callee-saved register as a clobber fault (the inline asm or thunk used one without saving it, so list it in the clobber list or save and restore it).

## Picture the stack frame

Draw the frame from the top down: return address, then saved frame pointer, locals, spill slots and alignment padding, and outgoing arguments at the lowest addresses next to the stack pointer. Move on once the user can place each item relative to the frame pointer. When the crash is on `call` itself, check that `rsp` is 16-byte aligned at the call instruction; the pushed return address leaves the callee entry at 8 mod 16.

## Cover the variadic rule where it applies

When the context has `...`, state the System V AMD64 rule: the caller sets `al` to the count of vector registers used, and `va_start` needs the register save area the prologue writes. Recommend typed wrappers over raw `va_arg` at FFI boundaries, and cast every `va_arg` type to its promoted form. Contexts without a variadic call skip this entirely.

## Prove it against the compiler

Confirm the stated rule against compiler output showing the argument moves and the `.cfi_*` directives that match it:

```bash
gcc -O2 -S -o - foo.c          # argument moves and .cfi_* directives
objdump -d -M intel ./a.out    # the same after linking
```

The finished answer is a chat reply with the register table row for the named ABI, the stack frame picture, the variadic rule where relevant, and the compiler or disassembler command that confirms the rule on the user toolchain. For the assembly side of each target, use `assembly-x86` or `assembly-arm`. For symbol and relocation views, use `elf-inspection`. For AArch32 Thumb interworking, note that a function pointer to Thumb code carries its low bit set.
