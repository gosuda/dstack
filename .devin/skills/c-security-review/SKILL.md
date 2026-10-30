---
name: c-security-review
description: 'Use when the user requests a userspace C or C++ security review with a threat model and severity filter and wants validated findings. Not for kernel or bare-metal code.'
disable-model-invocation: true
---

# C security review

You run a complete userspace C or C++ security review and return validated findings. The reviewed tree is never modified: your only write is a `.c-review-results/<iso-timestamp>/` run directory under the current working directory holding `units.json`, `ledger.json`, `findings.json`, `REPORT.md`, and `REPORT.sarif`. Rollback is deleting that directory. Create it first and clear any prior artifacts in it, so a failed run cannot leave stale files looking current.

Scope is native userspace C and C++ (memory safety, integer overflow, races, type confusion, daemons, services). Kernel drivers and modules, bare-metal or embedded code with no libc, and managed languages are out of scope: when the target is one of those, stop and say so before any review pass runs.

## What you need before starting

Resolve these before reviewing, inferring from free text on the invocation, then asking once for whatever stays unresolved. Never silently default a required parameter.

| Parameter | Values | How to read it from free text |
|---|---|---|
| Threat model | `REMOTE`, `LOCAL_UNPRIVILEGED`, `BOTH` | "remote" maps to `REMOTE`, "local" maps to `LOCAL_UNPRIVILEGED`. Scopes which bug classes count and which severity table each finding is scored against. |
| Worker model | Explicit name, or `inherit` | The model for every review pass; `inherit` means the session model. |
| Severity filter | `all`, `medium`, `high` | "all" or "high only" maps to the filter. Decides what reaches REPORT.md and REPORT.sarif. |

Optional: repo-relative scope directory (default `.`), which bounds both the unit list and where a finding may live; and context roots (default `.`), directories read freely for callers, build flags, and reachability. Narrow context roots to the scope directory only when the user forbids wider reading, and state that reachability confidence drops when you do.

## Cutting the tree into units

Walk the scope directory and collect every C and C++ source file (`.c`, `.cc`, `.cpp`, `.cxx`, `.h`, `.hh`, `.hpp`, `.hxx`). Cut each file into units: one function per unit, a function longer than 150 lines split at statement boundaries into slices of at most 150 lines, and file-level code outside any function as one unit per file. Every line in scope lands in exactly one unit. For each unit, count the sites each review question below is about: the writes, the arithmetic that becomes a size, the allocation calls, the `sizeof` uses, the string operations, the checked calls, the parameter mentions, the banned APIs, the macro expansions. Write `units.json` with the unit list, per-unit site counts, and the file list with line totals. The step is done when every source file in scope is in `units.json` and every line belongs to one unit. Empty scope (no source files under the scope path) stops the run: report the searched path and write no report.

## Partitioning into passes

Split the unit list into contiguous slices of about 1500 source lines per review pass, with at least 4 passes and at most 14. A trailing slice too small to be worth a pass folds into its neighbour. Location is the partition on purpose: each line has one owner, so two passes never write up the same bug. The step is done when each unit is assigned to exactly one pass and the assignment is recorded in `units.json`.

## Reviewing each pass

For each unit in the pass, read the unit and the code around it (callers, types, buffers it touches) from the context roots. Ask these ten questions of every unit that has a non-empty site count for them:

- Bounds. What bounds each write destination, and can the index or length reach past it. The high-yield shape is a size computed for one buffer and applied to another.
- Integer. Width, signedness, and wrap at every conversion and at every expression that becomes a size or an index. Unsigned subtraction below zero wraps to a value that passes every upper-bound check.
- Alloc lifetime. Single owner, freed once, never used after free, no surviving copy of a reallocated pointer, released on every error path.
- Sizeof arithmetic. Each `sizeof` is the pointee not the pointer, and the surrounding arithmetic cannot overflow before it reaches the allocator.
- Nul termination. Every string produced or consumed is terminated on every path, and byte length is not confused with character length.
- Return values. Every call whose failure matters is checked against the convention that function uses. A negative return stored in an unsigned type makes the following check unreachable.
- Caller contract. What the unit assumes of each parameter, and whether every caller guarantees it. Read the callers.
- Banned API. For each banned or deprecated API, the source of the data and the size that reaches it, and what validates between them. A bounded internal constant reaching one is a hardening note, not a vulnerability. Presence of a banned API without a data flow to it is not a finding.
- Initialisation. Every field of every out-parameter and every returned local is written on every path before it is read. `malloc` and the stack do not zero.
- Macro contract. What each function-like macro assumes of its arguments, and whether every expansion site enforces it.

Write one ledger row per unit and question pair into `ledger.json`: unit id, question, verdict (`clean`, `finding`, `needs-human`, `not-applicable`), sites accounted (the line numbers found by reading, all of them, not only the ones filed at), and evidence (what was found at those lines, including the ones not filed). The site count says when to stop looking, not what to write down: never trim a found site to match the count, and say in evidence when the two disagree. `not-applicable` is valid only when the counted population is empty. A `finding` verdict does not close the unit: a function with one bug found is likely to hold more.

A finding cites the repo-relative file and line, the enclosing function, the real code snippet copied not paraphrased, the broken invariant and what the attacker controls, the data flow from source to sink with the validation between them, the reachability chain from an entry point or the honest limit of what was traced, each mitigation looked for with the file and line where it was found or the statement that it is absent, and a severity (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) scored against the threat model with a one-line rationale. Every negative conclusion rests on the code in front of the reviewer, never on recalled knowledge of the project. Read cold error paths on purpose. A bug class the threat model rules out is not a finding. A bug outside the pass's own units is a one-line pointer (file, line, one sentence naming the mechanism), promoted to a finding later only if the owning pass never files within 12 lines of it. The step is done when every unit and question pair with a non-empty population has a ledger row and every pass's findings and pointers are recorded. A pass that produced no rows leaves its ground uncovered, not rounded away: name its files and line ranges next to the findings.

## Sweeping the silent classes

List every bug class in the threat model that received no finding in any pass. For each, enumerate its candidate sites across the whole scope tree (a grep over the pattern that class needs, then reading each hit) and either file a finding or record a ledger row with unit id `(sweep)`, the question set to the class name, empty sites accounted, and the enumerated population in evidence. A class that could not be reached gets an honest `not-searched` row, which is worth more than a skimmed one. The step is done when every silent class has a sweep row or a finding.

## Merging findings and checking coverage

Diff `ledger.json` against `units.json`: every unit and question pair with a non-empty count needs a row, and each row's sites accounted must cover the counted sites. Report coverage as checks satisfied over checks required, never as functions touched, and list every missing pair by name. Merge duplicates by rule: identical file, line, and bug class triples merge, and two findings on the same sink construct in one function within 5 lines merge. Two different constructs in one function are two bugs even when one fix covers both. Promote unclaimed pointers. Apply the severity filter. Write `findings.json` (every finding including merged duplicates, plus scope metadata and coverage numbers). The step is done when the coverage gap is named exactly, duplicates are merged, and `findings.json` holds the filtered set marked as reported. A coverage gap (a pair with no ledger row, or a row whose sites do not cover the count) leaves the run assembled and unverified: name each missing pair in REPORT.md and in the return, and never present the run as fully covered.

## Validating every finding

Take each reported finding in `findings.json` and re-read its cited lines from the source, plus the callers and the data flow it names, in a fresh read with the finding's own prose closed. Mark one verdict per finding. `confirmed` means the cited line holds the cited construct, the data flow reaches it, and no mitigation the finding declared absent is present. `refuted` means the cited line does not hold the construct, a guard the finding missed sits on every path to it, or the threat model excludes the class; record the reason in one sentence with the file and line of the disproof. `needs-context` means the verdict depends on code outside the context roots, on build configuration, or on a runtime fact the source does not settle; record what would settle it. Refuted findings stay in `findings.json` with their verdict and reason, and leave the reported set. Never downgrade a severity to avoid a refutation, and never soften a `refuted` to `needs-context` to keep a count up. The step is done when every reported finding carries `confirmed` or `needs-context`, every refutation carries its disproof line, and `validation_ran: true` with the refuted count is recorded in `findings.json`. When a cited line cannot be re-read because the file changed or the line is gone, mark the finding `needs-context` with that reason. Never modify the reviewed tree under a running review: a source edit invalidates the ledger for every unit.

## Writing the reports

Build REPORT.md (severity-grouped, the reported set only, each finding with its validation verdict, the coverage numbers, the uncovered pairs, the refuted count, and the `needs-context` findings under their own heading) and REPORT.sarif (SARIF 2.1.0, the same reported set). Both read one `reported` flag from `findings.json`; never retype a finding between them. Zero findings still produces both files, and zero findings on real C code is worth saying out loud. The step is done when both files exist and list the same findings. When a file is unreadable, record it with the error in `findings.json` under `unreadable_files`, continue, and disclose the gap in REPORT.md. When either report cannot be written, report which failed and what `findings.json` holds; never claim success.

## Returning the result

Read REPORT.md and return it. State next to the findings that each was validated by a re-read of its cited lines, that severities are the reviewer's own scored against the stated threat model, and how many findings were refuted and removed. State the coverage numbers and name every uncovered unit and question pair and every pass that failed. The step is done when REPORT.md is returned with the validation, coverage, and refutation disclosures.

## What you hand back

The `.c-review-results/<stamp>/` directory with `units.json` (unit list, per-question site counts, pass assignments), `ledger.json` (one row per unit and question, plus sweep rows), `findings.json` (every finding with validation verdict, merge history, scope metadata, coverage numbers, `validation_ran: true`, refuted count), REPORT.md (the reported set, severity-grouped and validated; start here), and REPORT.sarif (SARIF 2.1.0, same reported set). The returned text is REPORT.md plus the validation, coverage, and refutation disclosures.
