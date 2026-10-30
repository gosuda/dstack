# Simplify routing runbook

Read alongside `../SKILL.md`. This file carries the mechanics: base resolution, the inspection that precedes every route decision, exact dispatch conditions, sequencing, and the proof gates each route inherits. It never overrides the skill.

## Base resolution from evidence

Resolve in this order; never guess `main` or `master`:

1. Explicit override: `simplify against <ref>` diffs against that revision directly.
2. Pull-request evidence: the base branch the branch was opened against, via `git merge-base HEAD <pr-base>`.
3. Upstream evidence: the upstream tracking branch, when `@{upstream}` resolves.
4. Remote-default evidence: the remote-advertised default branch reference.

Otherwise stop and ask for an explicit base. Never fall back to a working-tree-only diff on a branch with committed history but no resolved base. Unborn HEAD means user-named files only; a root commit means the working tree is the scope with that noted. Empty after all valid resolutions is exit 11.

Untracked work: enumerate `??` entries from status output. Read authorized untracked files (user-named or explicit full-sweep authorization) alongside the tracked diff. Never delete an untracked file. Report meaningful unauthorized untracked files as out-of-scope remaining work with paths.

## The inspection that precedes routing

The diff is entry evidence, not scope analysis. Before dispatching, establish for each touched region:

- Callers: who calls the touched code, inside and just outside the hunks. Forced in-tree callers a survivor needs to land clean travel with the cut; callers beyond the forced set stay out and route as candidates.
- Boundaries: which module, contract, or artifact-class boundary the region sits on, and whether any surface is public, persisted, configured elsewhere, or version-promised.
- Dependencies: import, re-export, feature-flag, build, config, and generated-surface edges entering or leaving the region, with owning files.

Done when every region has its callers, boundaries, and edges recorded, or is gapped by name with the reason.

## Dispatch conditions

Send each disjoint scope to exactly one owner:

- Still being written, or deciding whether a helper, wrapper, config key, branch, or dependency earns its place: `minimalism-driven`.
- The weight is comments explaining what code already says: `no-comments`, with legal, mechanical-directive, and public-documentation homes protected.
- One named module, file set, or dependency slice shrinking inside its contract: `code-simplification`, module or dependency mode as the edges dictate.
- The module layout or dependency graph itself must collapse: `architecture-simplification`, only on an explicit human ask with an approved path set; never auto-promoted from a smaller cleanup.
- Residue crossing artifact classes under one unchanged observable boundary: `guillotine`, with its candidate ledger and bidirectional proof; stop for approval at any observable API, stored data, or untracked target.
- A consumer-facing surface must go: `refactor-break-compat`, with the demolition manifest previewed and explicit human confirmation before the atomic cutover.

Anything matching none of these, or matching two with no evidence to decide, is emitted as a candidate with file, line, evidence, and reason rather than forced into a route.

## Sequencing and integration

Dispatch disjoint scopes together; sequence dependent rewrites so interior cuts land before the boundary-gated cuts that depend on them. `refactor-break-compat` cutovers and `architecture-simplification` slices run after the `code-simplification` and `minimalism-driven` reductions they assume. Simplify is the single integration owner: every routee result returns through it, one concern per atomic commit with a capitalized imperative subject, and mixed-concern commits split before merge (exit 15).

## Proof gates every route inherits

Red baseline stops all cutting; report the failing tests first. After each increment run the narrowest applicable verifier, then the repository's own test command; revert the increment on red (exit 13) and keep prior green commits. Test edits are mechanical migration to the new contract with recorded reasons; no deletion, suppression, skipping, or weakening of tests to force green. Close with the post-fix audit and ghost sweep: no new bloat in the simplify chain itself (exit 14 on a hit, whole chain reverted), and no surviving string reference to any removed concept.

## Exit summary

Matches `SKILL.md`: 0 clean; 11 empty diff; 12 empty survivor set with report; 13 regression auto-reverted; 14 chain reverted on new bloat; 15 mixed-concern commit. Autopilot G2 passes on 0, 11, 12, absorbs a self-reverted 13, and halts for human re-planning on 14 and 15; these meanings are unchanged, so that caller needs no migration.
