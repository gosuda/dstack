---
name: fuzzing-dictionary
description: 'Use when a parser, protocol, or file format fuzzer stalls at fixed-token validation gates and needs a coverage dictionary. Not for patching the system under test: use fuzzing-obstacles.'
---

# Fuzzing dictionary

A fuzzer that cannot guess your magic bytes will never reach the code behind them. Your job is to hand it the exact tokens the target checks for (keywords, protocol commands, chunk types, delimiters, boundary values) in a file the fuzzer parses, wired into one campaign flag, proven to reach the gates.

This stays local and reversible. You touch only the named dictionary file, the one fuzzer flag that loads it, and transient short-campaign corpus or crash artifacts under a single output directory. Undoing it is deleting the file, reverting the flag, and removing that output directory. Nothing remote, no credentials, no publishing.

## Reach for this only for token gates

Patching the system under test to bypass checksums or nondeterminism is a different job, and it belongs to fuzzing-obstacles. Measuring coverage or diagnosing a plateau is out of scope too.

## What to have in hand

The target source, specification, header files, or binary you will mine tokens from, and the fuzzer you are feeding (libFuzzer, AFL++, or cargo-fuzz). If they exist, bring the current corpus, known boundary values, and the target's `-max_len` or equivalent input-length limit. An entry longer than that limit gets silently ignored, so you want the limit before you write.

## Build the dictionary

1. Name the single dictionary file path and the single configuration flag it will load through, and touch nothing else. No source, harness, or corpus edits.
2. Pull the fixed tokens from the target itself. Read keywords, magic bytes, commands, chunk types, and delimiters out of the source, headers, or spec, or out of `strings` on the binary. Guessed tokens do not belong here. If an entry did not come from the target, replace it.
3. Write one entry per line: `"token"` for bare strings, `kw="value"` for named entries, `#` for comments, `\\` for a backslash, `\"` for an embedded quote, `\xXX` hex escapes for non-printable bytes.
4. Keep it focused. Deduplicate with `sort -u`, drop full sentences and prose, keep atomic tokens. A bloated dictionary slows the fuzzer and dilutes the tokens that matter, so prune to the entries that map to real gates.
5. Wire it in with the flag for your engine (libFuzzer `-dict=./dictionary.dict`, AFL++ `-x ./dictionary.dict`, cargo-fuzz `-- -dict=./dictionary.dict`) and confirm the fuzzer loads the file with no parse error.
6. Prove the tokens land. Check they reach the target's validation or parsing gates instead of being filtered before them, with a short campaign run with and without the dictionary. A token longer than the fuzzer's max input length gets shortened, or the limit gets raised. You are finished when the file parses cleanly and its entries correspond to real gates.

## When the fuzzer rejects it

A syntax or path error on load means an unescaped quote, a bad `\xXX` escape, or a wrong path. Fix it and re-run the load check. Tokens that miss every gate mean re-extraction from the source or binary, not more guessing. Entries over `-max_len` get shortened or the limit raised. Keep only entries that load and map to a gate and discard the rest. On any failure, delete the dictionary file and revert the flag before retrying. A broken dictionary never stays wired into a campaign.

What you leave behind is the parseable dictionary file, the one flag set to load it, and confirmation that its tokens reach the target's validation or parsing gates.
