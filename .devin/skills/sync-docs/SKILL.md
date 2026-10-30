---
name: sync-docs
description: 'Use when a behavioral diff may have left docs or CHANGELOG stale, or when tidy targets stale code comments. Applies only safe fixes. Not for roadmap drift: use drift-detect.'
---

# Sync docs

Behavioral changes rot documentation quietly: a renamed export, a bumped version, a missing changelog entry. This job finds where the docs disagree with the code and fixes the small mechanical part, leaving every judgment call to a human.

## Where you may write

This job is reversible and local. You write only the named local doc files and the fix ledger, and rollback means reverting the edited files to their pre-edit content. There is no remote mutation of any kind.

You work read-first. In `report` mode you change nothing. In `apply` mode you touch only the two safe fixes described below. Anything else you flag with evidence and walk away from.

## Telling me what to look at

You need a scope and a base before you start.

| Setting | Meaning |
|---|---|
| Mode | `report` (default) or `apply`. Even in `apply`, you edit only safe-fix issues. |
| Scope | `recent` (changed files from the current branch or last few commits), `before-pr` (branch diff against the PR base), or `all` (all tracked code and docs). |
| Base | An explicit base ref is preferred. Without one, resolve the default branch, then fall back to `HEAD~5` for `recent`. |

Stop before doing anything if there is no diff or the scope is empty. Report the resolved base and scope rather than inventing drift. If the base ref is ambiguous, list the candidate refs and ask. When the user expects PR readiness, refuse an ambiguous review scope outright.

In DStack tool mode, use `bash` only for git commands. Use `find`, `search`, `read`, `lsp`, `ast_grep`, and `edit` for everything else.

## Finding what changed in code

Build the changed-code list from the diff, keeping only source, config, and package files that can actually affect docs. Leave out pure docs, vendored or generated paths, lockfiles (unless version docs mention package-manager output), and deleted files that were never public.

For each changed file, derive its coupling terms: the filename stem, the full path, import strings taken from the diff, and exported or public symbols, via codegraph where indexed and syntax extraction otherwise. If codegraph is unavailable, say so and treat symbol-dependent claims as MEDIUM certainty at best. The full detection recipe lives in `references/doc-issues.md`.

## Finding the docs that should care

Search the live doc surfaces (`README.md`, `CHANGELOG.md`, `docs/**/*.md`, root `*.md`) for every coupling term, recording the doc, line, term, and reference type for each hit. Confirm the occurrence pass with a second, different search pattern or symbol index before classifying anything, and fold in any occurrences the first pass missed.

Then classify each finding as HIGH, MEDIUM, or LOW using the severity taxonomy in `references/doc-issues.md`. Skip generated docs unless explicitly in scope, plus vendored docs, changelog append-only entries, and versioned snapshots unless in scope.

## What you may fix, and what you only flag

There are exactly two safe fixes, and both need HIGH-certainty evidence:

1. Stale version number. Replace the exact semver in docs with the manifest version, but only when the line clearly labels it as the product or package version. Get the manifest field per ecosystem from `references/detection-recipes.md` (package.json `version`, Cargo.toml `package.version`, pyproject.toml `project.version`; Go tag-derived versions are never auto-fixed). Years, dates, protocol or API versions, port numbers, and third-party image tags are never safe fixes. If a manifest fails to parse, skip its version bump and flag the file as MEDIUM with the reason.
2. Missing changelog entry. Insert a minimal bullet under `## [Unreleased]`, creating that section directly below the title if absent, citing the commit or file evidence. Never touch historical release sections, and never write changelog prose that needs product judgment.

Everything else is flag-only, no matter how certain: removed or renamed exports, import-path changes, stale examples, undocumented exports, docs describing dead code or wrappers, doc-drift or dead-doc suspicion. Those need human intent. After applying a safe fix, re-read the edited lines. On mismatch, revert the edit and reclassify the issue as flag-only with its `reasonFlagOnly`.

Two judgment rules apply while flagging. When two sources contradict each other on the same fact, surface both with their evidence and stop for a human ruling. Never resolve the conflict silently. For stacked parse-versus-enforce changes, inspect the code and docs at each tip. A base that stores a field without enforcing it must not claim enforcement, so flag the precise qualification the base tip needs and the restoring wording the enforcing tip needs, keeping semantic prose flag-only unless separately approved.

Sort the final report by severity, then file path.

## What you hand back

A JSON fix ledger with `opCell`, `scope`, `base`, `changedCode`, `relatedDocs`, `fixesApplied`, and `flagged`. Every edit records `file`, `line`, `type`, `before`, `after`, and its evidence source. Every flag-only item records `reasonFlagOnly`. You are done when safe fixes are applied or explicitly unavailable, and all remaining drift is flagged with file:line evidence and reasons. A clean report with no edits is valid only after the diff-to-doc mapping and taxonomy pass actually ran.

If some coupling terms resolve and others do not, report what resolved and flag the rest. Never widen scope to compensate for missing evidence. Reverting means restoring every edited file to its pre-edit content. The ledger before/after pairs make that possible.
