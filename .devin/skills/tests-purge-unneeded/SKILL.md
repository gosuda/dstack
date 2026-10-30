---
name: tests-purge-unneeded
description: 'Use when a legacy, slow, or duplicate test suite needs purging, a post-refactor sweep is due, or types cover a contract.'
---

# Purge unneeded tests

Test suites accumulate weight: stale claims about flags that no longer exist, tautologies that assert what they just constructed, duplicates that cover the same case twice. This job deletes the tests that prove nothing, keeps everything load-bearing, and proves each deletion with the cheapest evidence that settles the case. Aggression here means investigating the uncertain candidate, never deleting by assumption.

This job is reversible and local. You delete only VCS-tracked test files, and you mutate production code only temporarily, only inside the enumerated VCS-tracked production files, reverting each mutation before the next step or before reporting. Rollback is version control recovery. There is no remote, VCS-history, credential, paid, published, or deployed mutation. You show the exact deletion set before cutting.

## What you need before starting

| Input | Why it matters |
|---|---|
| Test suite root | The directory or glob identifying the test files to audit. Required. |
| Language or framework | Omitted when detectable from project config files (package.json, Cargo.toml, pyproject.toml, go.mod, pom.xml, build.gradle). Optional. |
| Scope constraint | Limits the audit to specific directories, file patterns, or changed-files-only mode. Optional. |
| Production sources under test | The files the tests exercise must be readable. If they are not readable, stop as blocked instead of guessing. Required for cold execution. |

## What you never delete

A test whose matched proof failed is load-bearing: keep it. A test whose failure mode you cannot articulate after investigation is kept pending human review. A protected boundary test (protocol compliance, error semantics, security invariants, real I/O integration, concurrency semantics, `unsafe` contracts, property invariants) leaves only through proved subsumption, where surviving coverage demonstrably preserves its required cases and detects the relevant defects. Redundant security coverage stays unless the same attack path is proved covered elsewhere. Meaningful coverage is protected, not every existing file. You never invent a mutant per deletion, never infer worthlessness from one missed mutant, never let a mutation persist past its proof step, never write strategy documents or marketing copy as part of a purge, and never expand scope beyond the declared root or constraint to resolve a finding. The proof class must match the case.

## Auditing the suite

1. Bound the scope. List every test file path under the audit root. Do not expand scope beyond the declared constraint. You are done when every path in the audit set is listed and reported.
2. Investigate each test aggressively. Read the production code it exercises and its direct callers. Check for stale claims (the asserted flag, symbol, behavior, or error path no longer exists), empty ceremony (tautology, mock-only, coverage-driven, trivial snapshot, just-in-case with no named bug), duplicated ownership (two tests cover the same case, so map them to the stronger owner), and noise (implementation-coupled private-method assertions that pin internals rather than behavior). Classify with reasons using `references/keep-vs-delete-table.md` and the language reference (`references/rust.md`, `references/typescript.md`, `references/python.md`). A constructor that only assigns parameters is direct pass-through and the compiler covers it; a constructor that validates, normalizes, defaults, transforms, or deserializes runs real logic and its test is a real-bug test no matter how trivial the result type looks. You are done when every test is classified as candidate or not, with a reason.
3. Articulate the bug and pick the proof class. For each candidate, write one sentence of the form "this test fails when ___ goes wrong", naming a concrete failure mode a real code change could plausibly introduce. If no such sentence survives reading the code, mark the test unarticulable and keep it pending human review. Otherwise select the cheapest sufficient proof class: A (compiler guarantee), B (demonstrated tautology), C (proved subsumption), or D (meaningful mutation). You are done when each candidate has a failure sentence plus a selected class, or is kept as unarticulable.
4. Guard the protected boundary. If a candidate verifies protocol compliance, error semantics, security enforcement, real I/O behavior, concurrency semantics, an `unsafe` contract, or a property invariant, deletion is allowed only through class C: name the surviving tests, map each required case to a surviving assertion, and require the survivors to detect the relevant defect class. Have a reviewer who did not build the class C mapping confirm each entry exercises the same observable behavior before deleting; return disputed entries to extension or keep.
5. Prove each case with its matched class only.

   | Class | Proof |
   |---|---|
   | A compiler guarantee | Cite the enforcing check and the language reference. No production edit. |
   | B demonstrated tautology | Show the outcome follows from the test itself and record the evidence. No production edit. |
   | C proved subsumption | Run the named surviving tests on current code (they must pass) and record a per-assertion table mapping every assertion in the deleted test to a specific surviving check. Extend the surviving suite or keep the test for anything unmatched. |
   | D meaningful mutation | Modify the VCS-tracked production file to introduce exactly the named bug, run the candidate test, record caught or survived, then revert immediately before the next step. If caught, keep and record. Never leave a mutation in the tree. Never use a second mutant to overrule a settled class A, B, or C verdict. |

   Mutation hygiene is strict. Before mutating an enumerated production file, preserve its actual pre-probe content, including uncommitted work. Apply one attributable mutation and verify it landed. Run the intended test and record the selected test population, the producer status, and the specific behavioral result. A compilation or setup failure does not show the test catches the claimed bug. Restore from the preserved pre-probe content before the next mutation or any deletion. Verify content identity against that preserved state, not merely against HEAD, and confirm the relevant tests again. Isolate or invalidate runtime artifacts when needed so the run exercises the intended source rather than stale mutant code. Do not delete unrelated caches. A caught mutation keeps the test. A survived mutation is only a deletion witness for that specific candidate, still subject to the boundary and language protections. A restoration failure stops the purge and reports the affected files; it must not be hidden by a passing suite.
6. Delete in batches. Delete only tests whose matched proof records uselessness (compiler guarantee holds, tautology demonstrated, subsumption proved, or named mutation survived). Before committing each batch, search the declared audit root and constraint for live references to each deleted path and update or remove them; annotate historical records instead of rewriting them, and stop the batch on unresolved dangling references. Each batch is an atomic commit with a rationale naming the proof class and evidence. Run the full suite after each batch. On regression, revert the batch and investigate. You are done when all proved-useless tests are deleted in atomic commits and the suite passes after each batch.

## What stops the purge

| Condition | Response |
|---|---|
| Framework not detected (no test runner or language identified) | Abort and report that manual identification is needed. No classification attempted. |
| Production sources unreadable | Block and report. No classification attempted. |
| Bug articulation failed after reading the code | Keep the test pending human review; its failure mode is unclear. |
| Static guarantee unclear (mixed codebase, `any` or `unknown`, unchecked-parse leaks, untyped mode) | Keep the test; the boundary shape may be a real-bug test. |
| Matched proof failed (mutant caught, subsumption gap found, tautology or compiler claim false) | Revert any mutation and keep the test as load-bearing. |
| Suite regressed after a batch deletion | Revert the batch via VCS. Successful batches stand; rolled-back batches do not invalidate them. |

No production mutation persists beyond its proof step.

## What you hand back

A deletion report ordering deleted tests first (file path, test name, proof class, evidence summary, batch commit hash), then kept tests (file path, test name, reason kept), then the final full suite pass/fail status.
