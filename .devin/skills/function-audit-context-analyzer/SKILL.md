---
name: function-audit-context-analyzer
description: 'Use when asked for audit-context analysis of one function, or to build audit context across codebase before vulnerability hunting. Local write only. Not for vulnerability finding or severity rating.'
disable-model-invocation: true
---

# Function audit context analyzer

You build the factual record a later hunt will reason from: how the code is put together, what must always be true for it to work, and what it takes on faith. You never name vulnerabilities, suggest fixes, write exploits, or rate severity. Those belong to the hunting phase that runs after this one.

Two shapes, one method. Single function mode writes one prose record to a caller given path. Multi function mode writes one record per function plus an assembled dossier under `audit-context/`. Both follow the same core method below: read the code, walk every callee path, cite lines for every claim, and record what is unclear.

This skill writes only the caller specified analysis path (single function) or beneath `audit-context/` (multi function). Rollback is deleting those files. No remote, credential, publish, deploy, or irreversible changes.

## What to take in

Single function mode:

* Required: the target function (name and file path with line range) and the per function analysis path to write.
* Optional: the source tree root for reading callees. When a callee source is unavailable, treat it as a black box per the method below.

Multi function mode:

* Required: a target path (codebase root, or a set of functions or files to analyze). The target must span more than one function; a single function uses single function mode.
* Optional: domain or language hints (smart contract, C/C++, decompiled firmware, web service) to decide what counts as a call whose interior cannot be seen. Optional prior findings or orienting notes, carried forward as context only; this skill produces no verdicts.

Vulnerability names, fixes, proofs of concept, and severity ratings are neither inputs nor outputs.

## The shared method

Read the target function in full. Scope is structure, invariants, and assumptions. If a draft would use the words vulnerability, exploit, or severity, restate the observation as the structural fact it rests on.

Read every callee the function depends on and walk every path through each callee, not only the path that returns successfully. A precondition established on three paths out of four is an assumption, not an invariant, and the fourth path is the interesting one. Look for an output parameter left unwritten on an early return, a check that sits behind a conditional, and a loop that can exit before it validates.

When a callee source is unavailable, treat it as a black box. Record what is sent to it, what is assumed about it, and the outcomes not excluded: failure, a hostile return value, an unexpected state change, reentry into the caller before its own writes land.

For every assumption, name the line that establishes it. When nothing establishes it, write "nothing found". That is a finding, not a failure.

Cite a line for every structural claim. If no line can be cited, do not assert the claim; record it in open questions as "unclear; need to inspect X". Never infer behavior from a name. When new evidence contradicts something written earlier, correct it in place and say what changed. Cut hedge words: "probably", "seems to", and "should be" each resolve to either a cited claim or an open question.

When two records disagree, quote both instead of reconciling them. Record the disagreement as a fact about the code, not a flaw in the analysis.

Adapt orientation to the target domain using `references/domain-adaptations.md` (smart contract, C/C++, decompiled binary, and web service mappings). Record which adaptation was applied.

## Single function record

Write the prose analysis to the given path in this fixed format, one document per function, sections in order separated by `---`:

* Header: `## functionName in path/to/file.ext (L40-L88)`
* Purpose: its role in the system and what breaks without it.
* Inputs and assumptions: each parameter with type, trust level (untrusted, semi trusted, trusted), implicit inputs (state read, caller identity, environment, clock), and preconditions with what establishes each.
* Outputs and effects: returns, state writes, events or messages, external interactions, postconditions.
* Block by block: each code block labeled with language and line range, followed by What, Why here, Assumes, Establishes, and Depended on by.
* Cross function dependencies: each callee labeled internal, external source available, or external black box with what the function depends on it to establish and on which paths; callers and what they assume; shared state; invariant couplings.
* Open questions: each as "unclear; need to inspect X".

Cite lines as `L45` or `L98-L102`. Spend words where the code earns them: branches, external calls, and state mutations earn analysis; a three line block that copies a value earns three lines. Leave a section out only when it is genuinely empty, and say so ("No external calls.") so "none" is distinguishable from "never checked". A short record whose claims each cite a line is worth more than a long one padded to fill a template.

Then return the compact record: a short index into the prose, not a summary of it. It holds the invariants, the assumptions and what establishes each, the callees and what the caller depends on them for, and the open questions. It exists so the orchestrator never has to load the prose.

Failure handling: if the function is not found or the line range is wrong, stop, write no file, and report the mismatch and what was searched. The prose file is written only when every section is complete; if it cannot be, report what is missing as open questions inside the file, or write nothing when the function itself is wrong. Finishing with open questions written down is a complete analysis. Finishing with questions never written down is not.

## Multi function dossier

1. Bound scope. Confirm the target path is readable. Create `audit-context/` and `audit-context/functions/`. Write nowhere else; edit, move, or delete no source. If the target is not found or unreadable, stop, report the path and the error, and write no dossier.
2. Orient. Read entry points, module boundaries, and the call graph. Identify the actors (callers and privilege boundaries), the persistent state (storage, globals, caches, files), and the full list of functions in scope. Record the function list and entry points in the dossier skeleton.
3. Analyze each function in an isolated pass and write its record to `audit-context/functions/<name>.md` before starting the next. Dispatch each pass to a subagent to isolate its context; do not hold every function detail in a single context, only compact records return to the orchestrator. Each record states what must always be true (with the source line), what the function takes on faith (with whatever establishes it), which functions it calls and what it needs from each, and anything still unclear.
4. Assemble `audit-context/DOSSIER.md` from the per function records: entry points; actors and who can reach what; persistent state; cross function invariants (rules spanning several functions); unenforced assumptions marked `nothing found`; disagreements with both sides quoted; coverage (which functions were analyzed and which paths were followed); and open questions carried forward.
5. Name no vulnerabilities, suggest no fixes, write no proofs of concept, rate no severity. When the code counts on something that nothing checks, record that fact and move on. A dossier covering N of M functions is valid only if the uncovered functions are listed under coverage with the reason; otherwise the run is blocked.

## What you hand back

Single function mode: the prose analysis at the given path (the deliverable) and the compact record returned to the caller (an index into it). Multi function mode: `audit-context/DOSSIER.md` plus one file per analyzed function under `audit-context/functions/`.
