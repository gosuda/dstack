---
name: code-simplification
description: 'Use when a named module, file set, or dependency slice needs less code and structure without losing required behavior. Covers dead code, unused settings, and redundant wrappers. Use simplify to choose the right level of work, architecture-simplification to reorganize modules, tests-purge-unneeded to remove weak tests, and refactor-break-compat for an approved public-interface change.'
---

# Code simplification

Someone names a module, file set, or dependency slice and wants it structurally smaller with its promises intact. That is the whole job: the complete authorized surface gets smaller, every consumer keeps working, and nothing load-bearing is lost.

Every remaining element earns its place. A module hides decisions behind its contract, and migrating the affected callers is part of the cut, never someone else's follow-up.

Work aggressively by default. The scope is the complete authorized module or dependency surface: every module, file, and edge in scope gets classified and challenged, not just lines touched recently. Shallow layers (forwarding tiers, single-use layers, pass-through modules, depth with no decision boundary) are challenged first and collapsed into their surviving owners. Real invariants (protocol, error, security, persistence, and compatibility contracts) are retained, and cuts at the boundary need an explicit recorded yes.

Two shapes share this job. `module` takes one named scope and reduces its interior. `dependency` takes one named slice plus its dependency edges and reduces both the slice and the edges it forces. Both preserve the consumer contract and real invariants, and both stop at the boundary gate.

## What you may touch

You write only VCS-tracked paths inside the named scope, plus proven internal callers and their test references and doc pointers when migration requires it. Rollback is version control through atomic commits. Anything beyond the named scope plus proven callers needs a new explicit scope. No remote mutation, ever.

When you finish, residue is deleted, special cases are folded into the general case, condemned shallow layers are collapsed into their surviving owners, single-use indirection is inlined and deleted, and all in-scope callers and pointers are migrated in the same change. No shim, alias, tombstone, dual path, or deprecated wrapper survives. The scoped consumer contract holds, every divergence is classified essential or residue, residue resolves to nothing under search, and the narrowest applicable verifier is green. Line delta is reported evidence only, never the predicate. No percentage or count target is accepted.

## Start from the consumer's side

List the exact paths in scope plus the observable surfaces they expose, covering the complete authorized surface rather than recently touched lines. Derive the consumer contract from call-site usage, existing tests, and public signatures, never from the target's internals. Name the real invariants that must survive (protocol, error, security, persistence, compatibility) and how each will be checked. For `dependency` mode, also list every dependency edge entering or leaving the slice (imports, re-exports, feature flags, build edges) with its owning file and line. You are done with this part when the path set, the edge set where applicable, the exposed surfaces, the contract, and the invariants with their checks are all written down.

Your raw material is the target the user named (file, module, function, directory, or slice; the working surface is the complete authorized surface, never a touched-lines subset), the consumer contract and invariant sources above, and a verifier: the compiler or typechecker first, then the repository's own test command.

## Call everything either load-bearing or residue

Walk the old shape function by function and branch by branch. Each divergence is essential (fold it into the general case with a one-line reason) or residue (cut it with a one-line reason).

Challenge shallow layers first: forwarding tiers, single-use layers, pass-through modules, and depth without a decision boundary are residue unless a named invariant requires them, and collapse into their surviving owners. Further residue covers dead state, forwarding-only wrappers, single-use generics with one concrete use, factories with one real implementation, always-on or always-off flags whose losing branch is deletable, and redundant nesting with no behavioral cause. A swappable-implementation contract counts only when more than one real implementation ships today. Single use or zero branching alone never proves a wrapper is unnecessary. A live invariant never counts as residue even when it looks like ceremony. You are done when nothing reachable in scope is unclassified and every shallow layer has a keep-with-invariant-reason or a collapse target.

Dead weight takes a few recurring shapes, and each carries its own proof before it may be cut. A field or member is dead only when it is written but never read afterward; constructor-only writes with no later read are the tell, and the search must cover the language's self form (`self.x`, `this.x`, or the package's receiver name in Go). A flag, environment variable, default, or branch is dead only when every environment agrees it lost: always-on flags inline the winning branch, always-off flags delete the gated branch with the flag, and stale infrastructure keys (unused Terraform variables, Helm values, Docker args, retired CI matrix entries) go by the same proof. A wrapper is redundant only when its body is a single forwarding call with no validation, error mapping, instrumentation, retry, or semantic naming, and it bridges no real boundary; even a small error-remapping step is real work and keeps the wrapper. Comment residue means isolated commented-out code blocks, trailing whitespace outside Markdown, and mixed indentation normalized to the file's dominant style, plus debug leftovers that were never the product (prints and debug macros in non-CLI code). Required safety justifications, public documentation, module invariants, and any comment carrying load-bearing evidence stay; comment weight beyond that residue belongs to `no-comments`, never to a deletion quota.

An import, re-export, feature or build edge, or package dependency is dead only when zero consumers remain: no static reference, no dynamic or reflective load, and no plugin registration reads it. Drop the dead edge with its wiring together, and keep anything dynamically reachable without strong proof of disuse.

Absence in one search never proves death. Every candidate is confirmed across code, tests, docs, configs, environment and deployment wiring, error messages, and log lines, and for config also across infrastructure definitions, dashboards, alerts, and runbooks where a key can be read without appearing in source. Reflective readers (serialization derives, dependency-injection wiring, framework annotations) are invisible to static search: a field under such a marker is unprovable-dead by grep alone and needs an explicit allowlist or scope exclusion before deletion. Types crossing a process boundary and keys partners or customers configure are published contracts, not cleanup, and hand to `refactor-break-compat`. A wrapper with dozens of callers may be earning its keep as a cohesion point even when thin: pause and name the reason before inlining. Anything with an unverified consumer, a migration still in flight, a date-gated flag, or a maybe-live behavior stays; never remove to find out.

## Ask before touching anything someone else depends on

Interior (every caller in-tree, nothing persisted, shipped, configured in someone else's deployment, or promised against a version) is demolished without asking once the scope is named. Boundary (public API, wire or on-disk format, configuration running in someone else's deployment, plugin point, documented example consumers import, anything a version was promised against) needs a recorded yes before cutting. On silence or no, keep it permanently as contract and hand the compat cut to `refactor-break-compat` with file, line, contract evidence, and reason. Never cut a boundary surface on silence, and never cut a real invariant to make the structure smaller. You are done when every boundary surface has a yes or a no, every invariant has its check, and nothing protected is cut on silence.

## Cut and carry the callers with you

Delete residue. Collapse special cases into the general case and condemned shallow layers into their surviving owners. Inline single-use indirection at every call site, then delete the wrapper. Migrate all in-scope callers, test references, and doc pointers in the same change: imports, call sites, fixture wiring, renamed symbols, module doc pointers, navigation entries. Never leave a caller on a removed surface, and never leave a shim, alias, tombstone, dual path, or deprecated wrapper behind. You are done when residue search returns nothing and no reference to a removed surface remains.

## Prove it still works

Run the narrowest applicable verifier before each atomic commit (compiler or typechecker first, then the repository's own test command), plus every invariant check named at the start. If the scoped baseline fails, stop before cutting and report the failure. If an edit regresses, restore the last verified scoped state and record the failing check.

Test edits come in two kinds. Mechanical migration to the new internal contract, and assertion updates strictly where an approved contract change requires them, each with a recorded reason, are permitted. Deleting tests (route those to `tests-purge-unneeded` with mutation proof), suppressing, skipping, or weakening assertions to force green, and adding parser exceptions or duplicate-resolution logic to fit the cut, are forbidden. You are done when the verifier and all invariant checks are green on the migrated tree with no forbidden edit.

Then sweep for ghosts: grep code, tests, docs, configs, environment variables and deployment wiring, error messages, and log lines for string references to every removed concept. For config also check infrastructure definitions, dashboards, alerts, and runbooks. You are done when zero survivors remain, or the candidate is reclassified not-dead with its reason.

## Hand this job to someone else when it stops being yours

This skill covers one named scope with the consumer contract and real invariants preserved: aggressive reduction of the complete authorized surface with all in-scope caller migration in the same change. No blind re-derivation, no contract rewrite. It never renames itself into a rebuild to avoid a handoff:

- `breaking-driven` owns it when the module is bloated enough to derive blind from call-site evidence and audit every old behavior as essential-or-residue. Route there when the divergence walk shows the old structure reproducing itself under fresh names. Human-explicit overhaul, rebuild, or rewrite-from-scratch intent is handled through the same contract-first replacement with boundary approval, never self-initiated from this skill.
- `guillotine` owns it when residue spans more than one artifact class (code plus docs, tests, config, workflows, or generated sources) with the observable boundary unchanged. Route there when the cut crosses artifact classes; it requires a candidate ledger plus bidirectional consumer proof.
- `architect` owns crate, module, or dependency-graph layout planning across scopes. This skill executes an approved slice at a time; `architect` owns the plan.
- `deps-upgrade` owns dropping or upgrading a third-party dependency for semantic, version, or policy reasons.
- `tests-purge-unneeded` owns any test deletion, and is the only owner with a mutation-proof contract.
- `purge-slop-docs` owns doc-only purges, hierarchy reorders, and whole-doc deletion (separate yes per file).
- `refactor-break-compat` owns any consumer-facing surface cut, on explicit recorded yes only.

## When it goes wrong

- Red baseline: stop before cutting and report the failing tests. Never cut on unproven ground.
- Regression after an edit: revert that edit immediately, record the edit and the failing check, and continue with other candidates only while the baseline stays green.
- Already at floor: every module, file, and edge in the complete authorized surface is classified essential with invariant reasons and no residue remains that preserves behavior and invariants. Report the floor with the classified list and invariant checks. Do not force cosmetic or taste-only edits past clear and maintainable, and do not claim the floor from a touched-lines subset.
- Boundary cut attempted on silence: restore from version control and record the surface, the missing yes, and the handoff.
- Invariant violation: revert the edit that broke it, record the invariant and the failing check, and continue only with invariant-preserving candidates.
- Ghost references remain: incomplete. Remove the survivors or roll back the cut that left them.
- No verifier available: every fix is unverified, the limitation is stated, and the done predicate is not claimed.
- Partial result: keep applied changes that preserve behavior and invariants, report rejected changes with reasons, and never claim done while behavior or invariants are unverified or callers dangle.

## What you hand back

The simplified scope plus a report: the mode (`module` or `dependency`), the stated consumer contract and invariants with their checks, the essential-or-residue classification with one-line reasons (shallow layers first), applied cuts with their atomic commits, all migrated in-scope callers and pointers, reverted edits with failing checks, boundary decisions (every yes or no with its evidence), the ghost-sweep result, final verifier and invariant results, and the reported line delta. Terminal classification: simplified, already-at-floor, or blocked with the exact missing scope, yes, invariant check, or prerequisite.
