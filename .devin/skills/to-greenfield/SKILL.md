---
name: to-greenfield
description: 'Use when the user says greenfield this or rescue this codebase, names a field (dark, red, blue, or brown), or diagnoses a subsystem. Not for specs. Not for remote or irreversible changes.'
---

# Rescuing a subsystem toward greenfield

You diagnose one troubled subsystem and land the first real fix. Read first, mutate once, and report what changed and what comes next.

Use this when the user says "greenfield this", "rescue this codebase", names a field color, or asks for a subsystem diagnosis. Do not use it for writing specs, for remote changes, or for anything irreversible.

## Bound the work before you touch anything

One invocation covers one subsystem: name it and the paths it covers. A larger repository gets one pass per subsystem, never a single undifferentiated sweep. A second subsystem is a second invocation. If no identifiable subsystem or region exists, stop, report the blocker, and change nothing.

Diagnosis is read-only: file reads, symbol and path searches, and the project's own verifier for the scoped subsystem. If the user named a field color, treat it as a hypothesis to confirm or refute with evidence, never as authority. If no verifier command was supplied, read it from the project's configuration or task runner; never invent one. State the rollback path (version control or undo) before any mutation.

## Name the field from evidence

Pick exactly one field, citing exactly one fact. Red comes first, then dark, then blue, then brown, and a broken blue setup counts as red until it is green.

- Red: the verifier fails, regressions are active, CI is red, or the build is broken. Evidence is the verifier output.
- Dark: no tests and no docs, structure unclear, nobody can say what a change would break. Evidence is the missing-tests-and-docs observation tied to the mapped paths.
- Blue: two coexisting implementations of one concern (old/new directories, migration flags, `v2` suffixes, TODO-migrate markers). Evidence is the named dual-implementation pair.
- Brown: green and working, but compat shims, legacy patterns, and dead weight. Evidence is the shim and legacy-pattern list.

If the signals support no single field, report the observed facts and the competing fields, execute no action, and end blocked. Never invent evidence. If the user-named field is refuted, report the refuting fact and proceed with the evidence-supported field.

Greenfield itself needs no action: when a re-diagnosis assigns no color to any scoped subsystem, the subsystem is already there.

## Land one clean replacement

Execute exactly one first corrective action for the diagnosed field, and make it a scoped clean replacement by default: replace the broken structure rather than patching around it, absorb its special cases into the canonical path, migrate all in-scope callers onto the replacement, delete the obsolete mechanism the replacement supersedes, and preserve essential behavior, validation, and proof. Never break live consumers, destroy data, or take a nonreversible step without explicit user approval. When the replacement needs such an act, stop and propose it instead.

- Red: fix the single highest-priority verifier failure with a replacement that turns that check green. A flaky check gets named in the report as quarantined, never silently deleted.
- Dark: map the subsystem (structure, entry points, dependencies) and write one newcomer doc as a local artifact. Every doc claim must trace to a mapped path.
- Blue: record the concern's canonical and legacy paths with their remaining callers, then migrate all remaining callers onto the canonical path so every migrated caller resolves against the canonical path only.
- Brown: add one behavior-pinning characterization test where coverage is thinnest. The new test must pass as written. A failing one refutes the diagnosis.

At most one edit or one artifact is ever in flight. Verify the action in the field's own terms: red reruns the single failing verifier and confirms green; dark checks every doc claim against a mapped path; blue confirms all migrated callers resolve canonically; brown requires the new test to pass. If the action fails (verifier stays red, a migrated caller breaks, the doc or test cannot be validated), revert the touched change to its prior state completely, report the failure, the unchanged field state, and the next action, and end non-converged. Never swallow the error or claim success.

## Report so the next step is obvious

Reply in chat with the field, its one-fact evidence, the action executed, files touched, the rollback path, the verification result, and the next action for that field. Darkfield additionally leaves the one newcomer-doc artifact. One diagnosis and one first action per invocation.
