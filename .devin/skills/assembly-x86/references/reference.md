# x86-64 assembly reference

Use this reference when you read or write x86-64 assembly. Sources: Intel SDM, the System V AMD64 ABI, and GCC inline asm documentation.

Operands follow AT&T order throughout: source first, destination second. `mov %rsp, %rbp` copies the stack pointer into the base pointer.

## Data movement

Use `lea` when you need the address itself. It computes the address without touching memory.

| Instruction | Effect |
|-------------|--------|
| `mov src, dst` | Copy |
| `movzx src, dst` | Copy with zero extend |
| `movsx src, dst` | Copy with sign extend |
| `lea mem, reg` | Compute the address into a register, no memory access |
| `push reg` | Push onto the stack |
| `pop reg` | Pop from the stack |
| `xchg a, b` | Exchange operands, implicit `LOCK` for memory |
| `cmpxchg a, b` | Compare and exchange, sets `ZF` |

## Arithmetic

The one-operand multiply and divide forms split the result across two registers. `inc` and `dec` leave the carry flag alone.

| Instruction | Effect |
|-------------|--------|
| `add src, dst` | `dst += src` |
| `sub src, dst` | `dst -= src` |
| `imul r/m` | Signed multiply, `rdx:rax = rax * operand` in one-operand form |
| `mul r/m` | Unsigned multiply, same two-operand split |
| `idiv r/m` | Signed divide, quotient in `rax`, remainder in `rdx` |
| `div r/m` | Unsigned divide, same split |
| `inc`, `dec` | Increment, decrement without touching `CF` |
| `neg dst` | Two's complement negate |

## Bit operations

Shifts fill from opposite ends. `shl` and `sal` are the same instruction. Rotates wrap bits around instead of dropping them.

| Instruction | Effect |
|-------------|--------|
| `and`, `or`, `xor`, `not` | Bitwise logic |
| `shl`/`sal` | Shift left |
| `shr` | Shift right, logical |
| `sar` | Shift right, arithmetic |
| `rol`, `ror`, `rcl`, `rcr` | Rotates through carry or not |
| `bsf src, dst` | Index of lowest set bit |
| `bsr src, dst` | Index of highest set bit |
| `tzcnt`, `lzcnt` | Trailing and leading zero counts, BMI or ABM |
| `popcnt` | Count set bits |
| `bt`, `bts`, `btr`, `btc` | Bit test and set, reset, complement |

## Comparison and branching

`cmp` and `test` set flags and discard the result. The branch reads the flags. Prefer the branchless `cmovcc` or `setcc` when the condition body is short.

| Instruction | Effect |
|-------------|--------|
| `cmp a, b` | Set flags from `a - b` without storing |
| `test a, b` | Set flags from `a & b` without storing |
| `jmp target` | Unconditional jump |
| `jcc target` | Conditional jump, see the table below |
| `cmovcc src, dst` | Conditional move |
| `setcc reg8` | Store the condition as 0 or 1 |
| `loop label` | Decrement `rcx`, jump when nonzero |

## rflags bits

You read these flags through the conditional jumps below. Signed comparisons use `SF` with `OF`. Unsigned comparisons use `CF`.

| Bit | Flag | Set when |
|-----|------|----------|
| CF | Carry | Unsigned overflow |
| PF | Parity | Low byte has an even count of set bits |
| AF | Adjust | Carry from bit 3 to bit 4 |
| ZF | Zero | Result is zero |
| SF | Sign | Result is negative |
| TF | Trap | Single step enabled |
| IF | Interrupt | Interrupts enabled |
| DF | Direction | String ops go downward |
| OF | Overflow | Signed overflow |

## Conditional jumps

The `l`/`g` family is for signed values. The `b`/`a` family is for unsigned values. Do not mix them.

| Instruction | Condition | Flags |
|-------------|-----------|-------|
| `je`/`jz` | Equal | `ZF=1` |
| `jne`/`jnz` | Not equal | `ZF=0` |
| `js` | Sign set | `SF=1` |
| `jns` | Sign clear | `SF=0` |
| `jc` | Carry | `CF=1` |
| `jnc` | No carry | `CF=0` |
| `jo` | Overflow | `OF=1` |
| `jno` | No overflow | `OF=0` |
| `jl`/`jnge` | Signed less | `SF!=OF` |
| `jle`/`jng` | Signed less or equal | `ZF=1` or `SF!=OF` |
| `jg`/`jnle` | Signed greater | `ZF=0` and `SF=OF` |
| `jge`/`jnl` | Signed greater or equal | `SF=OF` |
| `jb`/`jnae` | Unsigned below | `CF=1` |
| `jbe`/`jna` | Unsigned below or equal | `CF=1` or `ZF=1` |
| `ja`/`jnbe` | Unsigned above | `CF=0` and `ZF=0` |
| `jae`/`jnb` | Unsigned above or equal | `CF=0` |

## SIMD header map

Include one header for the instruction set you target. When you need several sets, include `<immintrin.h>` alone. It covers everything through AVX-512.

| Header | Provides |
|--------|----------|
| `<xmmintrin.h>` | SSE, `__m128` |
| `<emmintrin.h>` | SSE2, `__m128d` and `__m128i` |
| `<pmmintrin.h>` | SSE3 |
| `<tmmintrin.h>` | SSSE3 |
| `<smmintrin.h>` | SSE4.1 |
| `<nmmintrin.h>` | SSE4.2 |
| `<immintrin.h>` | Everything through AVX-512, use this one |

## Prologue patterns

Keep the frame pointer when you need stable frame addresses for debugging or unwinding. Omit it in optimized code and address locals through the stack pointer. Compilers omit it by default at `-O2`.

Frame pointer kept:

```asm
push %rbp
mov  %rsp, %rbp
sub  $N, %rsp
# body
leave
ret
```

`leave` restores the stack pointer from the base pointer and pops the saved base pointer. Keep the stack pointer 16-byte aligned after the allocation.

Frame pointer omitted, the default at `-O2`:

```asm
sub $N, %rsp
# body, locals addressed through rsp
add $N, %rsp
ret
```

Save each callee-saved register you use, and restore them in reverse push order:

```asm
push %rbx
push %r12
push %r13
# body that uses rbx, r12, r13
pop %r13
pop %r12
pop %rbx
ret
```

On Linux the kernel is built with `-mno-red-zone`, so kernel-mode code never relies on the 128-byte red zone.
