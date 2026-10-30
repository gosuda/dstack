---
name: code-generation-and-backends
description: 'Use when reading llc output, tracing IR through legalization and instruction selection, or scoping a new LLVM target. Not for IR-level passes.'
---

# Code generation and backends

LLVM IR becomes machine code through the backend pipeline, and this skill traces that path: which stage produced an instruction sequence, why the legalizer inserted extra operations, why `llc` and `clang` disagree, what an `llc` failure at instruction selection means, and what porting to a new architecture costs. It does not narrate IR-level passes; a symptom at the IR level is out of scope and gets no codegen cause invented for it.

Bring the source file, LLVM IR (`.ll`), or bitcode (`.bc`) under discussion, the target triple and CPU features whenever they cannot be read from the build (for example `aarch64-linux-gnu`, `riscv64-unknown-elf`, `thumbv7em-none-eabi` with `+neon` or `+crc`), and the observed symptom: the assembly region, the `llc` error text, or the pipeline question. The skill gathers the installed LLVM version itself (`llc --version`); tool flags below are confirmed against LLVM 23.1.4. Never guess a triple: when it is unknown and not inferrable from the build, report the ambiguity with the evidence examined and stop.

Everything runs in a scratch directory named in the report. Only bitcode and assembly files land there; project files are never modified, and rollback is deleting that directory. Nothing touches a remote resource. The work is done when the report names the stage behind each observed sequence or failure, the triple and feature set in effect, and the fix or expansion path for every failure. When a step cannot finish, the report states which steps ran and which are blocked instead of claiming a partial result as complete.

## Name the owning pipeline stage

Per function, LLVM runs IR legalization of types and operations the target lacks, then `SelectionDAGBuilder`, `LegalizeTypes` and `LegalizeOps`, instruction selection by TableGen pattern match, pre-register-allocation scheduling, register allocation, prolog and epilog insertion, and `AsmPrinter` to assembly or object. Attribute the symptom to exactly one of these stages before doing anything else.

## Reproduce with llc under the build's own triple

```bash
clang -c -emit-llvm -O2 -o foo.bc foo.c
llc -mtriple=aarch64-linux-gnu -O2 foo.bc -o foo.s
llc -mtriple=riscv64-unknown-elf -O2 foo.bc -o foo-rv.s
llc -mtriple=thumbv7em-none-eabi -mattr=+dsp foo.bc -o foo-m7.s
```

`llc --version` lists registered targets; `llc -mattr=help -mtriple=<triple>` lists feature names; `llc -mcpu=help -mtriple=<triple>` lists CPU names. When the target is not registered in the installed `llc`, report the `llc --version` target list and stop; a rebuilt LLVM with the target enabled is a prerequisite, not something to work around. When the bitcode comes from a different LLVM major than `llc`, report both versions and regenerate the bitcode with the matching `clang`; bitcode is not stable across majors.

When `llc` output and `clang` output differ, suspect the triple and feature set first. `clang --target=arm-none-eabi -c -O2 foo.c` bakes the triple into the bitcode, and passing a different `-mtriple` or `-mattr` to `llc` changes legalization and selection. Rerun both tools with the same triple, CPU, and attributes; the difference is either gone or explained by a flag.

## Read unexpected instructions as legalization

A type the target has no register for (an `i64` on a 32-bit core, a vector type with no matching unit) is split, promoted, or expanded into a libcall; an operation with no pattern is expanded into a sequence. Tie each unexpected sequence to the type or operation the target cannot represent directly. The fix is either a target feature that makes the type or operation legal, or an IR change that avoids it.

A `Cannot select` fatal error names an IR operation and type. Choose one of three paths and state it with the operation and type: mark it legal in the target (a backend change), add a custom lowering hook in `TargetLowering`, or rewrite the IR so the operation is not produced.

## Check the ABI for soft-float and calling-convention faults

For wrong soft-float or calling-convention behavior, check the ABI in the triple (`gnueabi` versus `gnueabihf`) and the float ABI flag passed to `clang`. The target's calling convention lives in TableGen (`CC_AArch64`, `CC_X86_64`) and is selected by the triple, so the triple and float ABI must match what the linked objects use. For the ABI rules themselves, use `abi-and-calling-conventions`.

## Treat spill-heavy output as register pressure, not a backend defect

A large stack frame or spill-heavy assembly means pressure that survived to allocation. Reduce live ranges at the IR or source level; the diagnosis is confirmed when the spill count moves with the source change.

## Scope a new target as four parts plus a starting point

Adding a target means defining register classes and instruction formats in TableGen `.td` files, implementing lowering hooks in `TargetLowering`, implementing the `AsmPrinter` and the MC layer with relocations, and implementing the calling convention and the object writer for the target format. Patterns such as `Pat<(add i32 GPR:$a, GPR:$b), (ADD32rr GPR:$a, GPR:$b)>` map DAG nodes to machine instructions. Start from the in-tree backend closest to the architecture. A TableGen syntax error is reported by `llvm-tblgen` with the `.td` line.

Hand back a codegen report with the pipeline stage owning each observed sequence or error, the effective triple, CPU, and feature set with any `clang` versus `llc` mismatch found, the chosen fix path per failure with its operation and type, and the scratch directory holding the generated `.bc` and `.s` files.
