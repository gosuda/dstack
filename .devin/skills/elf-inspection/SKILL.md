---
name: elf-inspection
description: 'Use when examining ELF binaries with readelf, objdump, nm, or ldd: dependencies, symbols, sections, relocations, build IDs, or hardening, or when enabling RELRO, PIE, stack canaries, FORTIFY_SOURCE, CET, CFI, or seccomp filters, or checking a binary with checksec. Not for modifying binaries. Not for runtime sanitizer builds: use sanitizers.'
---

# ELF inspection

An ELF binary reports its own structure. Every question about dependencies, symbols, sections, or hardening is one `readelf`, `objdump`, `nm`, or `ldd` query away, and every hardening gap has a concrete flag set gated on the toolchain in front of you. This skill never modifies anything. It inspects binaries and hands back flag sets and verification commands for you to run. Runtime sanitizer builds belong to `sanitizers`.

Tell me the binary or library (or the build to harden in `binary-hardening` mode) and the question: dependency, symbol, size, hardening, relocation, or build identity. A symbol name or address narrows the query. The default mode answers a question about the binary. In `binary-hardening` mode I also need the toolchain (`gcc --version` or `clang --version`, `ld --version`, `ldd --version` for the libc; grounded channels are GCC 16.x, Clang 23.1.4, binutils 2.47, glibc 2.44), and optionally the target platforms (x86-64, AArch64, or both) and which mitigations the deployment actually needs.

## Identify the file before choosing tools

`file` reports architecture, linkage, and stripped state. `size` reports text, data, and bss. Knowing the type and whether the binary is stripped selects every tool that follows.

```bash
file prog
size --format=sysv prog
```

## List what the loader must find

`ldd` resolves each `DT_NEEDED` entry. A `not found` row names the deployment gap.

```bash
ldd ./prog
ldd -v ./prog          # include version requirements
```

`ldd` executes the loader against the binary, so never run it on an untrusted binary. Use `readelf -d` for those. An unexpected dependency is traced the same way: `readelf -d prog | grep NEEDED`, then follow the link map to whoever pulls it in.

## Find the symbol or prove it missing

`nm -D` reads the dynamic table, `-C` demangles, `-u` lists what the binary needs but does not define:

```bash
nm -D ./libfoo.so            # exported dynamic symbols
nm -C prog                   # demangled
nm -u prog                   # undefined symbols
nm -S --defined-only prog    # with sizes
```

Type codes read as: `T`/`t` code, `D`/`d` initialized data, `B`/`b` bss, `R`/`r` read-only data, upper case for global and lower for local, `U` undefined, `W`/`w` weak, `V` weak object. An undefined symbol at load time is a two step check: `nm -D libfoo.so | grep mysymbol` shows whether the expected provider exports it, then `ldd ./prog | grep libfoo` shows whether the loader found that provider. When `nm` prints `no symbols`, the binary is stripped, so inspect the dynamic table with `nm -D` or point the tools at the `.debug` file or an unstripped build. An `ldd` reply of `not a dynamic executable` means the binary is static or built for another architecture, so confirm with `file` and use the triplet prefixed tools for foreign objects.

## Read headers, sections, and relocations without executing

`readelf` parses any ELF and runs nothing:

```bash
readelf -h prog    # header: class, machine, type, entry
readelf -S prog    # sections
readelf -l prog    # program headers, segments
readelf -d prog    # dynamic section, raw form of ldd
readelf -s prog    # symbol tables
readelf -r prog    # relocations
readelf -n prog    # notes, build ID
readelf --debug-dump=info prog   # DWARF
```

When section names are absent the binary may be stripped of its section header table. Read it through program headers with `readelf -l` instead.

## Disassemble the code around the question

```bash
objdump -d -M intel prog
objdump -d -S prog
objdump -s -j .rodata prog   # hex dump of one section
objdump -p prog              # private headers, DT_NEEDED entries
```

`-S` interleaves source when the binary carries `-g`. You are done when the code around the address or symbol shows in the requested syntax.

## Measure the hardening that is already there

PIE on an executable means the header type is `ET_DYN`. Full RELRO needs `GNU_RELRO` plus `BIND_NOW`. A nonexecutable stack means `GNU_STACK` with flags `RW`, not `RWE`.

```bash
readelf -h prog | grep 'Type:'
readelf -l prog | grep GNU_RELRO
readelf -d prog | grep BIND_NOW
readelf -l prog | grep GNU_STACK
nm prog | grep __stack_chk_fail     # stack protector
```

`checksec --file=prog` runs the same checks in one call, and `checksec --dir=/usr/bin` measures every binary in a directory at once. It is a separate install. In `binary-hardening` mode, run it first and record every row before changing anything:

| Protection | Good | Concern |
|---|---|---|
| RELRO | Full RELRO | Partial or none |
| Stack canary | Canary found | None |
| NX | NX enabled | Disabled |
| PIE | PIE enabled | None |
| FORTIFY | Yes | No |

Every row gets a measured value for the binary, and only then do the hardening steps below apply.

## Rank what makes the binary big

Rank symbols by size, then sections. For per object contribution, rebuild the link with `-Wl,--print-map` or run `bloaty`, a separate install.

```bash
size --format=sysv prog | sort -k2 -nr | head
nm -S --defined-only prog | sort -k2 -nr | head -20
```

You are done when the largest contributors are named with numbers. An oversized binary is then a choice between stripping debug info, removing sections, or restructuring data.

## Quote the build ID before comparing builds

```bash
readelf -n prog | grep 'Build ID'
```

The ID names the exact build for `debuginfod` lookups and pairs the binary with its `.debug` file. When two builds disagree, compare build IDs before comparing anything else. A mismatch means the inputs differ.

## Close the gaps with flags the toolchain supports

In `binary-hardening` mode, apply this baseline:

```bash
CFLAGS="-O2 -pipe \
  -fstack-protector-strong \
  -fstack-clash-protection \
  -fcf-protection \
  -D_FORTIFY_SOURCE=3 \
  -D_GLIBCXX_ASSERTIONS \
  -fPIE \
  -Wformat -Wformat-security -Werror=format-security"

LDFLAGS="-pie \
  -Wl,-z,relro \
  -Wl,-z,now \
  -Wl,-z,noexecstack \
  -Wl,-z,separate-code"

gcc ${CFLAGS} -o prog main.c ${LDFLAGS}
```

Shared libraries compile with `-fPIC` instead of `-fPIE` and link with `-shared`. Clang takes the same hardening defines in place of the `gcc` call, and `-D_GLIBCXX_ASSERTIONS` applies whenever libstdc++ headers are in use. Gate each flag on the toolchain: `_FORTIFY_SOURCE=3` needs GCC 12 or newer, or Clang 9 or newer, plus glibc 2.34 or newer headers, and older toolchains fall back to level 2. The build should compile clean and checksec should show the new values.

What each mitigation buys:

| Flag | Protection |
|---|---|
| `-fstack-protector-strong` | Canary on functions with local arrays or address-taken locals |
| `-fstack-clash-protection` | Stack-heap collision on huge allocations |
| `-fcf-protection` | x86 CET markers (IBT plus shadow stack) |
| `-D_FORTIFY_SOURCE=2` / `=3` | Bounds-checked libc calls; 3 adds dynamic object sizes |
| `-fPIE` + `-pie` | Address-space layout randomization for the executable |
| `-Wl,-z,relro` | GOT read-only after relocation |
| `-Wl,-z,now` | Eager binding; with relro, Full RELRO |
| `-Wl,-z,noexecstack` | Non-executable stack |

Every flag in the set traces to a row here and no flag is cargo culted. Gate further: `-fstack-clash-protection` needs GCC 8 or newer or Clang 11 or newer, `-fcf-protection` needs GCC 8 or newer, and Clang `-fsanitize=safe-stack` is an optional extra that changes the ABI. The stricter link set adds `-Wl,-z,nodlopen`, `-Wl,-z,nodump`, and `-Wl,--as-needed`.

Tune canary coverage as a recorded choice, not a default. `-fstack-protector` guards functions with `alloca` or large buffers, `-strong` adds local arrays and address-taken locals, `-all` guards everything at a runtime cost. Verify presence with `readelf -s prog | grep stack_chk`.

Check FORTIFY coverage in the output binary: `objdump -d prog | grep __.*_chk` counts fortified calls. Fedora 38 and later build distribution packages with level 3, so query your own toolchain with `dpkg-buildflags --query` or `rpm --eval "%{build_cflags}"` instead of assuming. Fortified call sites should exist, or the reason they cannot should be stated. When FORTIFY=3 silently lands below level 3, the toolchain or glibc is too old: verify with the `_chk` count and fall back to level 2 explicitly.

Add Clang CFI where the codebase can absorb LTO. CFI checks indirect and virtual call types and requires LTO plus hidden visibility:

```bash
clang -fsanitize=cfi -fvisibility=hidden -flto -O2 -fPIE -pie main.cpp -o prog
# Narrower checks: -fsanitize=cfi-vcall, cfi-icall, cfi-derived-cast, cfi-unrelated-cast
# Across shared libraries: add -fsanitize-cfi-cross-dso and build everything with LTO
```

The link should succeed with LTO, or the incompatible code is identified. A CFI link failure means non-LTO objects or visibility leaks in the build, so fix the object set before enabling cross-DSO.

Deploy CET when hardware and kernel allow it. Build with `-fcf-protection=full`, verify the notes with `readelf -n prog | grep -E 'SHSTK|IBT'`, and expect `endbr64` landing pads in the disassembly. Runtime shadow stack needs a CPU with CET, Linux 6.6 or newer with `CONFIG_X86_USER_SHADOW_STACK=y`, glibc 2.39 or newer, and opt-in through tunables. It is off by default. `ld -z shstk` and `ld -z ibt` stamp the corresponding GNU property notes directly. Check CPU support with `grep -m1 user_shstk /proc/cpuinfo`. The notes should be present and the runtime chain confirmed, or the gap named. When SHSTK is absent at runtime, a layer below the binary lacks support, so check the CPU flag, the kernel config, and the glibc version in that order.

On AArch64, use `-mbranch-protection=standard` for BTI plus return address PAC (ARMv8.3 or newer for PAC), and verify with `readelf -n prog | grep -E 'BTI|PAC'`. For MTE capable ARMv8.5 or newer hardware, Clang instruments stacks with `-fsanitize=memtag-stack` together with `-march=armv8a+memtag` (or `armv9a+memtag`). The flag errors out on non-ARM targets. MTE tags 16 byte granules with 4 bit tags and faults on mismatch. The notes should verify and the hardware claim should be checked, or the feature is deferred.

Restrict syscalls with libseccomp after all initialization, since the filter is irreversible once loaded:

```c
#include <seccomp.h>

void apply_seccomp_filter(void) {
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL_PROCESS);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(brk), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(mmap), 0);
    seccomp_load(ctx);
    seccomp_release(ctx);
}
```

Build the allowlist from measurement, not guesswork: `strace -c ./prog` counts the syscalls actually used, and `strace ./prog` confirms nothing dies with SIGSYS after the filter lands. The program should run its real workload under the filter. When it dies with SIGSYS, the allowlist is incomplete, so read the strace count and add the missing syscall deliberately.

A rejected flag is not a failure: drop the flag, record which toolchain refused it, and ship the rest. When checksec disagrees with the build flags, the link stage dropped a mitigation, so confirm `-pie` and the `-Wl,-z` flags reached the final link.

Hand back a quoted answer report: the tool command, its relevant output lines, and the conclusion drawn from them. In `binary-hardening` mode, hand back a protection report instead: the checksec reading, the applied or recommended flag set with per flag toolchain support, verification command outputs, and the seccomp allowlist where one applies, each claim naming the compiler, binutils, and libc versions it assumes. The command table, symbol type list, and section map live in `references/cheatsheet.md`.
