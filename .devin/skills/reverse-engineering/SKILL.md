---
name: reverse-engineering
description: 'Use when triaging an unknown binary, decompiling with Ghidra, scripting radare2, or diffing two builds for patched functions. Not for ELF structure basics: use elf-inspection.'
---

# Reverse engineering

Use this when someone must understand a binary without source: triage an unknown file, recover logic with a decompiler, script an analysis, identify C++ patterns or the entry point in a stripped binary, patch a copy, or find which functions changed between two builds. Work on a copy in a scratch directory named in the report, never on the original in place. Untrusted binaries belong in an isolated lab machine or VM, never on a workstation with credentials. There is no remote mutation. Each question is answered with tool output as evidence: the file type, the protections, the decompiled region or disassembly, and for diffs the list of changed functions.

Bring the binary path and the question (file identity, a function's logic, a patch location, or a between-builds comparison). The toolchain is gathered as needed: `file`, `strings`, `readelf`, `objdump`, `checksec`, Ghidra, radare2 6.2.0 (the flags below are confirmed against that installed build).

## Triage before opening a disassembler

Identify the format, protections, and readable content first:

```bash
file suspicious_binary
strings -n 8 suspicious_binary | head -50
strings -el suspicious_binary | head -20
xxd suspicious_binary | head -20
readelf -h suspicious_binary
nm -D suspicious_binary | head
checksec --file=suspicious_binary
```

| Output | Meaning |
|---|---|
| `file` fields | Architecture, static or dynamic, stripped or not |
| `strings` | URLs, paths, error messages, key material |
| `readelf -s` | Symbol table, when not stripped |
| `checksec` | RELRO, stack canary, NX, PIE, RPATH |

Record the architecture, stripped state, and protections before moving on.

## Read it in Ghidra for full understanding

Analyze headlessly, then read the decompiler. A custom script needs `-scriptPath`; `-import` adds new files while `-process` runs against a file already in the project:

```bash
analyzeHeadless /tmp/ghidra_projects MyProject -import suspicious_binary
analyzeHeadless /tmp/ghidra_projects MyProject -process suspicious_binary \
  -scriptPath /tmp/scripts -postScript ListLargeFunctions.java
```

In the GUI the order is: let auto-analysis finish, press `F` to define a function at a missed entry, open the decompiler for C-like output, rename with `L`, and search cross-references with `Ctrl+Shift+F`. A script lists the functions worth reading first:

```java
import ghidra.program.model.listing.*;
FunctionManager fm = currentProgram.getFunctionManager();
for (Function f : fm.getFunctions(true)) {
    if (f.getBody().getNumAddresses() > 100)
        println(f.getName() + " @ " + f.getEntryPoint());
}
```

Jython (Python 2.7 syntax) or native PyGhidra 3.2.0 (Ghidra 12.0+, requiring JDK 25 and CPython 3 via JPype >=1.5.2). For GUI sessions with an in-process CPython 3 console and script manager bound to `currentProgram`, launch Ghidra via `support/pyghidraRun` (`pyghidraRun.bat` on Windows). For headless automation, initialize via `pyghidra.start()` (or `pyghidra <binary> <script.py>` CLI). Because PyGhidra runs in-process via JNI/JPype, it cannot attach to an arbitrary already-running GUI process. Never silently restart or terminate an active Ghidra instance to attach (doing so loses in-flight analyst work); treat an actual need to attach to an already-running external GUI as a reported capability gap. If legacy `ghidra-bridge` (v1.0.0, Jan 2023, failing maintenance policy) is discussed for legacy setups, heed its security warning: it exposes an unauthenticated, unencrypted TCP socket (default port 48884) granting arbitrary remote code execution in Ghidra's JVM and interception; never start or expose it automatically. The target function is done when it is decompiled and renamed identifiers record the analyst's reading.

## Script it in radare2 for terminal work

Open writable only when patching, with `r2 -w`:

```
[0x00001000]> aaa          # analyze all (imports, entry, symbols, calls)
[0x00001000]> afl          # list functions
[0x00001000]> s main; pdf  # seek to main, disassemble it
[0x00001000]> iz           # strings in data sections with xrefs
[0x00001000]> VV           # visual graph mode
```

```bash
r2 -qc 'aaa; afl' suspicious_binary
r2 -i analysis.r2 suspicious_binary
```

Patching writes to the opened copy:

```
[0x00001000]> wx 9090 @ 0x401234   # write two NOPs at the address
[0x00001000]> wt patched_binary    # write the modified copy out
```

The question is done when it is answered from `pdf`/graph output, or the patched copy is written out under the scratch directory.

## C++ patterns, stripped binaries, firmware, and diffs

Read C++ binaries through their patterns. A virtual call loads the vtable pointer from the object and calls through a slot (`mov rax, [rdi]` then `call [rax+0x10]`); constructors store the vtable address first; templates appear as mangled `_Z` names with duplicated logic per type; `std::string` shows either an inline buffer or a heap pointer at offset 0. Demangle with `c++filt _ZN4Math3addEii`. Each virtual call target in the region is resolved to a vtable slot.

For a stripped binary, find `main` through the C runtime: `readelf -s binary | grep -E 'main|__libc_start_main'`, or `afl~entry` in radare2 and follow the argument passed as the first function pointer. Then anchor on string cross-references to error handlers and on `syscall` instructions for the binary's real behavior. FLIRT-style library signatures in Ghidra or Binary Ninja label the libc functions so only application code remains unknown. Done when `main` and the string-referenced handlers are identified.

For firmware, extract before analysis: `binwalk -e firmware.bin`, then open the extracted ELF for its architecture in Ghidra with the matching language (ARM versus Thumb matters; a wrong choice decodes garbage). For packed executables, unpack first (`upx -d` for UPX) and analyze the unpacked copy. Done when the extracted executable parses as the architecture stated in its header.

For a between-builds comparison, diff at the function level: `sha256sum` both files to confirm they differ, then `diff <(objdump -d v1) <(objdump -d v2)` to list changed functions, or use Diaphora or BinDiff for matched-function diffing. The changed functions are the patch; read those first when hunting a fixed vulnerability. Done when the changed function list is reported with the differing disassembly quoted.

## Cautions from hard cases

When stripped-binary analysis produces implausibly large functions or sparse discovery, compare discovered entries with available unwind metadata. FDE starts are candidate function-boundary evidence, not guaranteed complete coverage. Derive ELF-to-analysis address translation from load addresses and the tool's actual memory map, then verify known anchors before seeding analysis. Do not hardcode a rebase delta, assume every encoding has one layout, or prescribe fixed heap and timeout values. For packaged CLIs, inspect a scratch copy of the shipped bundle, embedded modules, and request-building code to recover candidate endpoints, fields, signing, and error contracts. Record artifact version and hash and distinguish static inference from observed behavior. This local-analysis authority does not authorize contacting an endpoint, supplying credentials, downloading replacements, or invoking a paid service.

## When tools mislead

| Failure | Cause | Fix |
|---|---|---|
| Ghidra decompiler output is wrong | Indirect jumps or bad types | Fix the function signature and define structs for the parameters; re-decompile |
| radare2 analysis is incomplete | Large binary | Run `aaa`, then broaden with `-AA`, and raise analysis depth before concluding a function is absent |
| Wrong instruction decoding | Architecture or mode mismatch (ARM versus Thumb, MIPS variant) | Set the arch (`-a arm`) or the Ghidra language and re-analyze |
| Patching refuses to write | The file was opened read-only | Reopen with `r2 -w` on a copy, never on the original |
| No cross-reference to a string | Position-independent code reaches it through the GOT | Follow the GOT entry or analyze at runtime with `gdb`. For dynamic behavior, use `gdb` |
| Packed binary shows no code | Unpack first and analyze the unpacked copy; entropy spikes mark encrypted sections | Unpack, then re-analyze |

Never claim a partial result as complete. If a step cannot finish, the report states which steps ran and which are blocked.

## What your report holds

An analysis report containing triage (format, architecture, stripped state, and protections with the tool output), findings (each question answered with the decompiled or disassembled evidence quoted), patched copies (paths under the scratch directory, with the addresses and bytes changed), and diff results (the changed function list for comparisons, with the differing disassembly).
