---
name: docs-update
description: 'Use when documentation has drifted from code changes and the user asks to synchronize it. Delivers the fixes as local commits or as a reviewable PR after preview approval. Not for ADRs, architectural rationale, or writing an isolated document (use docs-writing).'
disable-model-invocation: true
---

# Docs update

Bring documentation back in line with a bounded set of code changes, then deliver the result as local commits or as a reviewable PR. To write a single new document, use `docs-writing`. For a read-only report on how far plans and docs have drifted from code, use `drift-detect`. ADRs and architectural rationale are out of scope.

## Delivery modes and safety

The user picks the delivery mode, and it decides every remote effect:

| Mode | Remote effect |
|------|---------------|
| Local commit | None. Commits stay local; never push, publish, or open or update a PR or MR. |
| Reviewable PR | Push and open a PR only after the user approves a preview. Never merge. |

If the request names neither mode, ask before changing anything. Every write besides the approved push stays local, with version control as the rollback.

Documentation commits always go on a feature branch. In local commit mode on the base branch, stop before any change and name the feature branch to create, even if repo policy would allow a base-branch commit.

## Inputs

- Delivery mode: `local commit` or `reviewable PR`.
- Change set: the commit or time range the user gives; otherwise the commits ahead of the base branch; otherwise the last 24 hours.
- Repositories: the source repo and, when docs live separately, the documentation repo and its remote.
- Documentation: everything discovered in the project, including README, ARCHITECTURE, CONTRIBUTING, CLAUDE.md, CHANGELOG, VERSION, and TODOS when present.

Resolve the base branch, current branch, and change set. In PR mode, also identify the documentation repo's remote, base branch, and proposed head branch, without creating or pushing anything yet.

## Filter the change set

Read every commit and its diff. Keep user-facing changes: features, API changes, changed behavior, removals, configuration, commands, flags, endpoints, environment variables, and feature flags. Exclude refactors, test-only changes, typo fixes, and performance or infrastructure work with no user impact. When significance is doubtful, keep the commit. Record why each commit was kept or excluded.

If nothing user-facing remains, report the excluded commits and stop without a commit or PR.

## Learn the docs and their style

Discover the documentation, skipping dependency, VCS, and build directories. Detect the platform (Mintlify, Docusaurus, GitBook, Fumadocs, or plain Markdown when no signal exists) from config and structure. Read the project style guide and a few representative files to capture voice, terminology, heading structure, frontmatter, components, and code-example conventions.

## Map changes to coverage

For each changed public surface in the kept diffs, map where it is covered across the Diataxis types (reference, how-to, tutorial, explanation). Mark surfaces with no coverage or reference-only coverage. Check maintained diagrams (ASCII, Mermaid, others) for renamed, moved, split, or removed entities and edges. Tie each gap or drift item to a specific doc change.

## Audit and classify edits

Check each document against the kept diffs: setup, examples, troubleshooting, commands, project structure, workflows, component descriptions, cross-references, and navigation. Sort every needed edit:

| Class | Covers | Handling |
|-------|--------|----------|
| Auto | A bounded factual correction proved by the diff: a path, count, table row, command, flag, structure tree, or stale link | Apply directly |
| Ask | Positioning or narrative, design rationale, security model, removing or adding a section, rewriting more than about ten lines of one section, or any ambiguous claim | Present one recommendation plus a skip option; apply only the approved choice |

Skipped text stays unchanged.

## Apply edits in the local voice

Match the detected platform and style, keep accurate content, and update diagrams together with the claims around them. Keep terminology, examples, navigation, and repeated facts consistent across documents. Write a one-line factual summary for each changed file.

## Protect the changelog

Leave CHANGELOG alone unless the kept changes need an entry. Before editing, read the whole file. Score each affected entry from 0 to 3, one point each for a changed fact, user impact, and a usage command, flag, or link. Reword entries scoring below 2 toward user impact, and split out contributor-only detail when the existing structure allows it.

Keep every existing entry and its order. Use narrow exact-match edits; never regenerate or overwrite the file. If an edit risks clobbering entries, drop that edit. Ask when an entry looks wrong or incomplete.

## Reconcile the set

- Feature lists, commands, components, project structure, versions, and cross-references agree across documents. Auto-fix proven factual mismatches; route narrative contradictions through the ask class.
- Every document is reachable from README or CLAUDE.md. Report any that are not.
- TODOS: move only clearly completed items to the completed section with version and date. Ask about items whose referenced files changed substantially. Surface meaningful TODO, FIXME, HACK, and XXX comments added by the source changes and ask whether to record them.
- VERSION: check it against its branch diff and against CHANGELOG. Never bump without explicit approval; offer patch, minor, or skip, and recommend skip for documentation-only changes.

## Scan for secrets

Scan every modified file for API keys, tokens, passwords, private URLs, internal hostnames, and PII, including email addresses outside legitimate attribution. Remove or mask findings without leaving secret-shaped placeholders. If redaction would distort the doc, leave that file uncommitted and ask.

## Commit

If no documentation changed, report that the docs are current and stop. Otherwise stage modified documentation files by explicit path and write descriptive commits. In a multi-repo setup, commit only each repo's own files, and link every documentation update to its triggering source commit by URL or repository-qualified hash.

## Deliver

- Local commit: leave the commits in place. Done.
- Reviewable PR: show a preview with the documentation repo, remote, base branch, head branch, files, commit summary, source-commit links, and a plain statement that the branch will be pushed and a PR opened. After explicit approval, create or reuse the head branch, push it, and open one PR per documentation repo. Request human review and do not merge. Without approval, keep everything local.

## Stop conditions

| Condition | Action |
|-----------|--------|
| Delivery mode missing | Ask local commit or reviewable PR; change nothing |
| Local mode on the base branch | Stop before any change and name the feature branch needed |
| Documentation repo missing or mismatched | Report the expected repo or path; do not guess or edit another repo |
| No user-facing change | Report the excluded commits; no commit or PR |
| Ask-class edit without approval | Leave the text unchanged; skipping is valid |
| CHANGELOG clobber risk | Drop that edit; keep existing entries and order |
| Secret or PII remains | Exclude the file from delivery and name the redaction decision needed |
| PR preview not approved | Keep work local; no remote effect |
| Partial result | Deliver only files that passed audit, approval, consistency, changelog protection, and redaction; list every unchanged or blocked file |

## What you hand back

- A coverage map with Diataxis gaps and diagram drift.
- A per-file status (Updated, Current, Polished, Skipped, or Blocked) with one factual line each.
- Either the local commits, unpushed, or the PR URLs, whose descriptions link each update to its repository-qualified source commit.
