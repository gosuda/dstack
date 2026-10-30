---
name: refactor-break-compat
description: 'Use when modernizing APIs, removing compat shims, killing feature flags, or rewriting a subsystem cleanly. Not for additive refactors that must preserve the old path.'
---

# Breaking refactors

Tear out an old API shape and move every caller to its replacement in one clean cutover, leaving no shim, flag, or adapter behind. This skill demolishes the old path, so if the old path must survive, use a regular additive refactor instead. Everything here is local: writes touch only version-tracked refactor targets, rollback is version control, and nothing reaches the network. The demolition owner migrates every consumer in the same cutover and never hands migration work to consumers or keeps a compatibility alias behind.

You need the old surface (compat shims, legacy adapters, feature flags, version gates, backward-compatible interfaces) and the new contract every caller must adopt. An optional file or module scope bounds the work; without one, the blast-radius map sets the boundary, and nothing outside the approved manifest gets touched no matter what a review finding suggests.

## Name the replacement contract and its proof

Before touching code, write down the consumer contract the replacement must satisfy and the behavior proof suited to this target (a test, a check, whatever actually exercises it). If that proof does not exist, stop and name the missing proof in the blocked result. Also confirm there is no known behavior the old shape covers that the replacement cannot reproduce; if such a gap is known, stop before destroying anything and name the consumer plus the unreproduced behavior.

## Map everything the old shape touches

Enumerate every file, module, and caller of the old shape with `ast-grep` or `rg`. This demolition manifest is the scope: every file and caller that will be deleted or rewritten, every test that will change, every flag or config key going away.

## Show the demolition and wait for a yes

Present the manifest and its consequences to the human and wait for explicit confirmation. Nothing is deleted on an assumed or timed-out yes. A rejection or silence ends the run with the tree untouched.

## Cut over atomically: delete, then migrate

Remove the compat layers, adapters, legacy branches, and flags used only by the old path. Delete means delete, never comment out. Spare any flag that also controls the replacement or another live path. Treat this deletion and the caller migration below as one atomic unit: if a gap surfaces mid-cutover, either finish inside the approved scope or restore the whole affected cutover to the pre-change baseline. A half-migrated tree is never shipped and never reported as success.

Migrate every reference from the manifest to the new contract. After each batch, run the strongest static enumerator the project has (compiler or typechecker, including opt-in `mypy`, `pyright`, `tsc --checkJs`, Sorbet). A clean static pass is never sufficient on its own, because no static pass sees reflective, dynamically dispatched, string-constructed, or generated references, nor code excluded from the build. Enumerate those by hand and name them in the report.

## Rewrite the tests to the new truth

Update assertions to the new behavior and delete tests whose entire purpose was the old behavior. Where the new contract is now thinly covered, add tests that prove its independent behavior rather than snapshotting output. A suppressed check or a zero-matched selection counts as no proof at all.

## Exterminate ghosts and dead weight

Grep for string references, config keys, env vars, doc links, error messages, and import paths naming the old API until the search returns nothing. Then remove the imports, packages, dependencies, types, and dead files that only the old path needed.

## Prove zero residue

Search for every old symbol, flag, and format name. Anything found sends you back to migration. Where this target exposes metrics, logs, or dependency-analysis channels, corroborate through them that no consumer still uses the old shape after the cutover. The report names the commit range that reverts the removal and, where such channels exist, the post-removal watch set confirming no consumer regressed (otherwise it records those channels as not applicable).

## What failure looks like

Residue survivors, a broken build, or a stalled half-migration all fail the run, and partial results are never reported as success. Fix forward only inside the approved scope; otherwise restore the whole affected cutover to baseline, name the exact blockers, and stop with the matching exit: 1 for residue, 2 for broken build, 3 for stalled migration. Zero is a clean demolition only: every caller on the new contract, tests asserting the new behavior with old-behavior tests gone, and the zero-residue search empty.

Report the blast-radius manifest, the deleted artifacts, the caller-migration checklist (naming any pre-destruction blocked consumer and its unreproduced behavior), the test-rewrite summary, the zero-residue result with revert range and watch set, and the exit code, in that order.
