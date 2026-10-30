---
name: docs-update
description: 'Use when documentation has drifted from code changes and the user asks to synchronize. Not for ADRs or architectural rationale. Not for writing an isolated document (docs-writing).'
disable-model-invocation: true
---

# Docs update

Bring documentation back in line with a bounded set of code changes, then deliver the result as local commits or as reviewable PRs. ADRs and architectural rationale are out of scope here, as is writing an isolated document from scratch (that belongs to docs-writing). The requested delivery decides what happens: local commit mode never pushes and never opens a PR; reviewable PR mode pushes and opens a PR only after the user approves its preview. Every other write stays local, with version control as the rollback. On the base branch in local mode, work stops before any mutation: documentation commits always require a feature branch, even where repo policy would permit a base-branch commit.

## What I need before touching anything

- Delivery: `local commit` or `reviewable PR`. If the request names neither, ask before mutating.
- Source change set: a user-supplied commit or time range; otherwise the commits ahead of the base branch when one exists, falling back to the last 24 hours.
- Repositories: the source repo, and where documentation lives separately, the documentation repo and its remote target.
- Documentation: the discovered project docs, including README, ARCHITECTURE, CONTRIBUTING, CLAUDE.md, CHANGELOG, VERSION, and TODOS files when present.

## Bind the delivery and the repos

Resolve the delivery, the source and documentation repos, the base branch, the current branch, and the source change set. In PR mode, identify the documentation repo's remote, base, and proposed head branch without creating or pushing it.

## Keep the user-facing changes, set the rest aside

Inspect every commit and its diff in the change set. Keep user-facing features, API changes, changed behavior, removals, configuration, commands, flags, endpoints, environment variables, and feature flags. Exclude refactors, test-only changes, typo-only fixes, and performance or infrastructure changes with no user impact. Classify doubtful significance conservatively and record why each commit was kept or excluded.

## Learn the docs, the platform, and the local style

Discover all relevant documentation while excluding dependency, VCS, and build directories. Detect Mintlify, Docusaurus, GitBook, Fumadocs, or generic Markdown from configuration and structure. Read the project style guide and representative files to capture voice, terminology, heading structure, frontmatter, components, and code-example conventions. Use plain Markdown only when no platform signal exists.

## Map every changed surface to its coverage

Extract each changed public surface from the kept diffs. Map its current coverage across Diataxis reference, how-to, tutorial, and explanation; mark zero-coverage and reference-only gaps. Inspect maintained ASCII, Mermaid, and other diagrams for renamed, moved, split, or removed entities and edges. Map each gap or drift item to a specific documentation change.

## Audit each document and sort edits into auto or ask

Check every discovered document against the kept diffs and its purpose. Cover setup, examples, troubleshooting, commands, project structure, workflows, component descriptions, cross-references, and navigation. Sort each needed edit:

- Auto-update: a bounded factual correction proved directly by the diff, such as a path, count, table item, command, flag, structure tree, or stale link.
- Ask: positioning or narrative, design rationale, security model, a section removal, a new section, a rewrite past roughly ten lines in one section, or any ambiguous claim.

Present each ask with one recommendation and a skip option. Apply only the approved choice; leave skipped text unchanged.

## Apply the edits in the local voice

Match the detected platform and style, preserve accurate content, and update diagrams with their surrounding claims. Keep terminology, examples, navigation, and repeated facts consistent across documents. Report a one-line factual summary for each changed file. Stop when all approved edits are applied and no changed claim conflicts with another document.

## Leave the changelog intact

If the selected diff needs no CHANGELOG edit, leave it alone. Otherwise read the whole file before editing. Score affected entries from 0 to 3: changed fact, user impact, and usage command, flag, or link. Reword entries below 2 toward user impact, and separate contributor-only details when the existing structure permits it. Preserve every entry and its order; use narrow exact-match edits, and never regenerate or overwrite the file. Ask when an entry appears incorrect or incomplete.

## Reconcile the set, the todos, and the version

Verify feature lists, commands, components, project structure, versions, and cross-references agree across documents. Confirm each document is reachable from README or CLAUDE.md and report unreachable files. Auto-fix proved factual inconsistencies; route narrative contradictions through the ask classification.

For deferred work: if a TODOS file exists, move only clearly completed items to its completed section with version and date. Ask whether to update, complete, or leave items whose referenced files changed substantially. Surface meaningful TODO, FIXME, HACK, and XXX comments introduced by the source changes and ask whether to record them. If VERSION exists, inspect its branch diff and its agreement with CHANGELOG. Ask before every bump, offering patch, minor, and skip as applicable; recommend skip for documentation-only changes. No version changes without explicit approval.

## Scan for secrets, then commit

Scan every modified documentation file for API keys, tokens, passwords, private URLs, internal hostnames, and PII, including email addresses outside legitimate attribution context. Remove or mask findings without retaining secret-shaped placeholders. If redaction would distort the documentation, leave that file uncommitted and ask.

If no documentation changed, report that the documentation is current and stop. Otherwise stage modified documentation files by explicit path and create descriptive documentation commits. In a multi-repository setup, commit only files belonging to each repository and retain links from every documentation update to the triggering source commit URL or repository-qualified commit.

## Deliver at the single fork

- Local commit: leave the scoped commits in their repositories. Do not push, publish, or create or update a PR or MR.
- Reviewable PR: preview the documentation repository, remote, base branch, head branch, files, commit summary, source-commit links, and the consequence that the branch will be pushed and a PR opened. After explicit approval of that preview, create or use the proposed head branch, push it, and open one reviewable PR per documentation repository. Request human review; do not merge.

## When I stop instead

- Delivery missing: ask the user to choose local commit or reviewable PR; do not mutate.
- Local mode on the base branch: abort before mutation and name the required feature branch.
- Missing or mismatched documentation repository: report the expected repository or path; do not guess or edit another repository.
- No significant user-facing change: report the excluded commits and stop without a commit or PR.
- Ambiguous or narrative edit: leave it unchanged until the user approves a choice; skipping is valid.
- CHANGELOG clobber risk: stop that edit and preserve the existing entries and order.
- Secret or PII remains: exclude the affected file from delivery and identify the required redaction decision.
- PR preview not approved: keep work local and create no remote effect.
- Partial result: deliver only files that passed audit, approval, consistency, clobber protection, and redaction; list every unchanged or blocked file.

## What you get back

A coverage map with Diataxis gaps and diagram drift. A per-file health summary (Updated, Current, Polished, Skipped, or Blocked, with one factual line each). Either scoped local documentation commits with no push, or reviewable PR URLs whose descriptions link each update to its repository-qualified source commit.
