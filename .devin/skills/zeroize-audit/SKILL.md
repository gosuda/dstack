---
name: zeroize-audit
description: 'Use when auditing C, C++, or Rust secret-handling code to verify zeroization survives compiler optimization. Not for test vectors.'
---

# Zeroize audit

You check that secret wiping code still wipes after the optimizer runs. C, C++, and Rust code handling keys, passwords, tokens, PII, or other secrets is in scope. The target repository stays read only throughout. All working material (emitted compiler artifacts, generated PoCs, findings, the final report) lands in one dedicated temporary audit directory, so rollback is deleting that directory.

What you need before starting:

- Target repository path (required): root of the codebase under audit.
- Build context (required): path to `compile_commands.json` for C/C++ or `Cargo.toml` for Rust.
- Scope (optional): files or directories narrowing the audit. Defaults to the full repository.

Without a parseable build context, halt with `missing-build-context` and name the missing prerequisite. Never proceed past that gate.

## Finding the secret paths and pinning optimizer evidence

Search the repository for secret handling identifiers (key, password, token, secret, PII), cryptographic operations (encrypt, decrypt, sign, derive), and explicit wiping calls (memset, explicit_bzero, SecureZeroMemory, zeroize, Zeroize). Record each candidate with file path and line range. Discovery is complete when every candidate secret-handling file is recorded with its path and line range.

For each candidate unit, emit the compiler output at the optimization level the project actually uses (typically `-O2` or `-O3`). C and C++ units compile from their `compile_commands.json` entries with `-emit-llvm -S`. Rust crates emit MIR (`--emit=mir`) and assembly (`--emit=asm`). Running those captured compilation, cargo, and LLVM/MIR/assembly emission commands is part of the work; only the repository itself is never written. Log the exact invocation, flags, and optimization level per unit. Units that fail to compile become coverage gaps carrying the compiler error; the audit continues with the units that built. Never touch the target repository to fix a build. Emission is complete when every compilable unit has artifacts with its invocation, flags, and level logged, and every uncompilable unit is recorded as a coverage gap with its compiler error.

Analyze each artifact for six questions. Do the wiping calls still emit their stores in optimized output. Did dead store elimination remove a store to a stack slot never read again (compare against `-O0` output to spot the removal). Did sensitive values spill from registers to the stack, and does the spill slot get zeroed before return. Does heap memory get zeroed before free, or does the deallocator zeroize itself. Does zeroing happen on only some branches and leave others dirty. Do copies or moves retain the secret somewhere unzeroed. Every artifact gets checked on all six. Analysis is complete when every artifact carries a verdict on all six.

## Proving residues with a safe PoC

Write a minimal program per finding that shows the missing or eliminated wipe without invoking undefined behavior. A valid PoC reads residual memory from a stack or heap location after the function returns but before reuse or deallocation, only through pointers to memory the program still owns. Compile it with the same toolchain and flags as the target, run it, and capture the output. Some findings cannot be demonstrated this way; mark those `unsupported` with the reason (`requires-undefined-behavior` stays the most important one) and lean on the compiler artifact evidence instead. A PoC that fails to compile is marked `unsupported` with the compiler error text; a PoC that compiles but fails at runtime is marked `failure` with the runtime error text, and the finding keeps its source and IR evidence at downgraded confidence. Ambiguous wipe presence gets reported as uncertain with the exact ambiguous evidence quoted. Never assert presence or absence beyond what the evidence shows. The PoC stage is complete when every finding has its source, compile command, runtime output, and verdict, or an explicit unsupported or failure status with its reason.

Assemble the record last. `findings.json` holds one entry per finding with id, severity, file, line range, description, evidence class (source, IR, MIR, assembly), confidence (high, medium, low), PoC status (pass, fail, unsupported, failure), coverage gap flag, and recommendation. `final-report.md` holds the executive summary, per finding detail with the optimization level where wiping was eliminated or retained, coverage gaps for units that could not compile or be analyzed, compiler version and flags, and prioritized remediation recommendations. The audit is done when both records exist with every required field per finding.

What you hand back: `findings.json` (schema valid, every finding carrying evidence class, confidence, and PoC status) and `final-report.md` (summary, per finding detail with optimization level evidence, gaps, compiler info, remediation), both under the temporary audit directory alongside intermediate evidence and PoC sources.
