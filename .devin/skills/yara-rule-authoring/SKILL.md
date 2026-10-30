---
name: yara-rule-authoring
description: 'Use when writing, reviewing, optimizing, validating, or migrating YARA or YARA-X malware-detection rules, including CRX or DEX rules. Not for network IDS or memory-forensics rules.'
disable-model-invocation: true
---

# YARA-X rule authoring

You write malware detection rules that match their family, stay silent on clean files, and scan fast. Static analysis needing disassembly, dynamic sandbox analysis, network IDS rules, memory forensics, and plain hash list detection stay out of scope.

Only the rule files change on disk. Everything else (sample scans, goodware scans, lint, atom analysis) reads the rule and corpus without altering them. Credential access, publishing, and deployment stay out of bounds. Report syntax, style, atom, match, timing, and skipped validation results as separate signals. Keep them distinct instead of collapsing them into one verdict.

What you need before starting:

- Rule source or specification (required): an existing rule to review, optimize, or migrate, samples to write against, or IOC and threat intel to convert.
- Positive sample corpus: files the rule must match. Optional to start, required before the rule counts as done.
- Goodware corpus: clean files proving zero false positives. Same status as above.
- Target platform (optional, defaults to Windows PE): macOS Mach-O, JavaScript/npm, Chrome extension, Android DEX, or Office document.

## Picking the target and pulling candidate strings

Name the malware family and platform, then assemble several variants. Single sample rules stay brittle, so gather more variants when they exist. Packed samples (entropy above 7.0, few readable strings, known packer) call for rules against the unpacked payload or the packer itself, never the packed layer. Extract candidates with yarGen (`yarGen.py -m samples/ --excludegood`) or FLOSS (`floss sample.exe` for obfuscated or stack strings). Most of that output gets discarded in the next pass, so expect roughly four fifths to fail. This step is done when the family, platform, and sample set are fixed and candidates are extracted from every available sample.

Test every candidate and reject it on the first failure:

| Test | Why it fails | Do instead |
|---|---|---|
| Under 4 bytes | No atom generated | Find a longer string |
| Repeated bytes (0000, 9090) | Weak atom | Add surrounding context |
| Common API name (VirtualAlloc, CreateRemoteThread) | Every packer and installer calls it | Hex pattern of the call site plus a unique marker |
| Appears in Windows system files | Guaranteed false positives | Find something family specific |
| Common path (C:\Windows\, cmd.exe) | Ubiquitous | Find malware specific paths |
| Appears in other malware families | Not identifying this family | Combine with a family specific marker |

Choose string types from confirmed evidence. Exact ASCII or Unicode text suits known strings (`ascii wide` only with confirmed encoding evidence). Fixed byte sequences suit hex. Variable bytes suit hex wildcards (`??`). Structured patterns like URLs and paths suit bounded regex. Unknown encodings suit the XOR modifier. Never use `nocase` or `wide` speculatively: `nocase` doubles atom generation and `wide` doubles string matching. Fixed bytes belong in hex rather than regex. Rank survivors by value: mutex names rank gold, C2 paths silver, error messages bronze. Stack strings run almost always unique. Needing more than 6 strings signals over fitting. This step is done when every candidate passed all tests or was rejected with its reason, and the survivors are ranked.

## Writing the rule for speed and precision

Name rules `{CATEGORY}_{PLATFORM}_{FAMILY}_{VARIANT}_{DATE}` (example: `MAL_Win_Emotet_Loader_Jan25`). Categories: `MAL_`, `HKTL_`, `WEBSHELL_`, `EXPL_`, `SUSP_`, `GEN_`. Platforms: `Win_`, `Lnx_`, `Mac_`, `Android_`, `CRX_`. Every rule carries `description` (starting with "Detects"), `author`, `reference`, and `date`.

Order the condition so cheap tests short circuit first: `filesize <` (instant), magic bytes (nearly instant), strings (cheap), modules (expensive). Conditions longer than 5 lines split into multiple rules.

Magic byte checks demand attention to endianness. `uintNN()` reads little endian, so write the constant bytes reversed or switch to `uintNNbe()` in file order. A ZIP or OOXML file opens with bytes `50 4B 03 04`, so `uint32(0) == 0x04034B50` matches while `uint32(0) == 0x504B0304` compiles and never fires. A Mach-O universal binary on disk reads `CA FE BA BE`, so `uint32(0) == 0xCAFEBABE` stays dead and `uint32be(0) == 0xCAFEBABE` works. Confirm each magic byte check with `yr scan` against one known good sample.

| Platform | Magic bytes | Prefer | Avoid |
|---|---|---|---|
| Windows PE | `uint16(0) == 0x5A4D` | Mutex names, PDB paths | API names, Windows paths |
| macOS Mach-O | `uint32(0) == 0xFEEDFACF` (64-bit), `uint32be(0) == 0xCAFEBABE` (universal) | Keylogger artifacts (CGEventTapCreate), persistence paths (~/Library/LaunchAgents), credential theft (security find-generic-password) | Common Obj-C methods |
| JavaScript | (none) | Obfuscator signatures (_0x, eval+atob), Ethereum function selectors ({ a9 05 9c bb }), specific C2 domains | require, fetch, axios, Buffer, crypto, process.env alone |
| npm packages | (none) | Suspicious package names, exfil URLs, postinstall hooks | postinstall, dependencies alone |
| Chrome extensions | Use `crx` module | Permission abuse, manifest anomalies | Common Chrome APIs |
| Android apps | Use `dex` module | Obfuscated classes, suspicious permissions, DexClassLoader reflection | Standard DEX structure |
| Office docs | `uint32(0) == 0x04034B50` | Macro auto-exec, encoded payloads | VBA keywords |

Group strings by confidence for graduated requirements. Prefix groups such as `$a*` for library indicators, `$b*` for behavioral, `$c*` for C2 let the condition require evidence from several categories (`any of ($a*) and any of ($b*)`). Reserve `any of them` for strings each individually unique to the malware. Reserve `all of them` for strings that are common alone but suspicious combined.

Reach for modules only when byte checks fall short. `uint16` and `uint32` cover magic bytes and simple offsets with no module overhead. The PE module covers imphash, rich header, authenticode, and section names. The `crx` module covers extension permissions. The `lnk` module covers LNK target paths. When `uint32()` answers the question, skip the module.

Bound every expensive construct:

- Anchor each regex to a 4+ byte literal prefix. Unanchored regex evaluates at every file offset.
- Bound each quantifier: `.{0,30}`, never `.*`.
- Bound loops by filesize: `filesize < 100KB and for all i in (1..#a) : ...`. Bare `#a` can reach thousands.
- Prefer hex over regex where bytes stay fixed.

Version gated syntax stays available by version: `private $helper = "pattern"` matches without appearing in output (v1.3.0+); `// suppress: slow_pattern` silences one warning inline (v1.4.0+); `filesize < 10_000_000` numeric underscore syntax (v1.5.0+); `$_unused` suppresses unused string warnings. The rule is done when naming, metadata, the short circuiting condition, correct endianness, confidence grouping, and bounded performance all hold.

Reviewing an existing rule, migrating from legacy YARA, CRX module rules, DEX module rules, structural pivots when strings fail, and rationalizations to reject live in `references/branches.md` and apply on those branches only.

## Validating syntax, lint, atoms, and corpora

Run the checks in this order:

```
yr check rule.yar
yr fmt -w rule.yar
```

Fix every error at its reported line. Treat `yr check --relaxed-re-syntax` as a diagnostic: fix the regex, then verify clean without relaxed mode. Both commands pass before moving on.

```
uv run yara_lint.py rule.yar
uv run atom_analyzer.py rule.yar
```

These catch mechanical faults: short strings, false positive prone substrings, unbounded quantifiers, expensive terms ahead of cheap ones. Report findings by code (E002, W009) so each one stays lookable up. Aim judgment where scripts cannot reach: whether the strings identify this family, and whether the condition can fire on generic strings alone. Move on once both scripts ran and every finding is reported by code.

```
time yr scan -s rule.yar corpus/
```

Match all target samples. Coverage under 50% of known variants runs too narrow. Then scan the goodware corpus with zero matches required. One or two goodware hits mean investigate and tighten. Three to five mean find different indicators. Six or more mean start over. The corpus step is done when the rule matches every target sample and zero goodware, or the gap is reported with its cause.

Close by reporting each category on its own: syntax and format pass or fail with line numbers; linter findings by code; atom quality per string; positive sample match count and timing; goodware match count; validations skipped plus the reason. Partial results stay partial: report performed and unperformed validations separately. The run is done when every category above is reported on its own.

| Failure | Detection | Recovery |
|---|---|---|
| Syntax error | `yr check` reports line and message | Fix at the reported line; re-run until clean |
| Format inconsistency | `yr fmt --check` reports deviation | Run `yr fmt -w` |
| Linter defect | `yara_lint.py` emits a code (E/W) | Fix per the code description; re-run |
| Atom weakness | `atom_analyzer.py` flags short or FP prone strings | Replace or enrich flagged strings; re-run |
| False positive on goodware | `yr scan` matches a clean file | 1-2: investigate and tighten or add an exclusion. 3-5: find different indicators. 6+: restart with different strings. |
| Too narrow | Under 50% of known variants match | Broaden the condition or add variant strings; re-validate against goodware |
| Performance regression | `time yr scan` shows excessive time | Anchor regex to a 4+ byte literal; bound all quantifiers; prefer hex; add a filesize guard to loops |
| Wrong endianness | Magic byte check compiles but matches zero known good samples | Switch between `uintNN()` and `uintNNbe()`; verify with `yr scan` against one known good sample |
| Packed sample | Entropy above 7.0, few readable strings | Target the unpacked payload or the packer itself |
| Validation not performed | Tool or corpus unavailable | Name exactly what was skipped and why; never present it as clean |

What you hand back: the new or modified YARA-X rule file on disk with proper naming, metadata, short circuiting condition, and bounded performant patterns; a validation report with the separated signals above; and when migrating, a migration report naming legacy issues, fixes, and post fix verification without relaxed mode.
