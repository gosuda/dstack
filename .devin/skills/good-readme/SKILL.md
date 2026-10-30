---
name: good-readme
description: 'Use when the user asks to create, rewrite, review, or polish an open-source README, including shop-window READMEs. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Good README

A README decides in seconds whether a stranger keeps reading. This skill turns it into a short, evidence-backed introduction: what the project does, why it differs, a runnable taste, and a setup guide that works from a clean machine.

It edits only README.md in the local working copy, with rollback through version control or editor history. It never touches remotes, credentials, publishing, or deploys.

## Start from what the repo proves

Read the existing README if one exists, plus the package manifest, the source entry points, and any benchmark or size data. Record which facts are present (differentiators, numbers, sizes, supported platforms) and which are missing. A README may not exist yet; create it in that case.

Any fact the repo lacks and the user cannot supply stays out of the file. Never estimate a number or invent a differentiator. A README with sourced content and named gaps is a partial result, reported as such, never claimed as done.

For shop-window READMEs, open with the project name, a one-line tagline, a one-sentence description, and a visual separator. Pick section templates from `references/section-templates.md` to match the project type (library, CLI, web app, or the general minimum). Each project ships at minimum Installation, Quick Start, Features, Usage, Contributing, and License. Fill every section from project files, summarizing and linking to source locations rather than copying code out of them. When installation cannot be derived from project files, stop and report `no-install-path` with the files checked. When the primary audience, project phase, or an emphasized section is unclear, ask one question to resolve it; when intent stays unresolvable, stop and return `blocked: unresolvable-intent`.

## Keep only badges that prove something

Prefer plain statements of fact over badges. A badge stays only when its repository, workflow, registry package, license, or coverage integration is proven by project files, using the URL patterns and limits in `references/badges.md`. Replace every angle-bracket variable with a derived value and place the row below the project title and tagline.

Every kept badge must render dynamically (HTTP 200, not the shields "invalid" card). Omit any badge whose value cannot be proven. Use flat-square or flat style, keep the row to one line (a second line only when more than five badges are proven), and use a semantic color (green for passing, red for failing).

## Write the four parts in order

### Opening

Write one plain-language paragraph that answers three things: what the project does, how the reader benefits, and what differs from alternatives. Source differentiators from the repo or the user; when they are missing, ask before writing.

### Facts

Add a scannable list right after the opening. Lead each bullet with 1-2 bold keywords backed by concrete evidence from the repo: real benchmark numbers, exact sizes, a side-by-side comparison with the closest alternative, or a screenshot or diagram that replaces a paragraph. Every number comes from the repo, the user, or a measurement. Ask the user for anything missing or how to measure it.

### Example

Add a usage example of 4-10 lines that shows its output in a comment, so the reader sees the result without running anything. This illustrates; the real setup comes next.

### Getting started

Add explicit copy-pasteable commands for adding the tool to an existing project, with every step present. Validate the guide by following it from scratch as if the project were unfamiliar, and fix every gap found. When a missing step or failing command cannot be resolved, mark the guide incomplete and stop.

## Format for skimmers

Use headings for hierarchy, bold for key points, lists over dense paragraphs, and horizontal rules between layers. Put must-not-miss lines in blockquotes or bold. When the file exceeds roughly two screens, add a table of contents after the opening. Skimming only headings and bold text must still tell the story.

## Check quality before finishing

Evaluate the draft against every applicable item in `references/quality-checklist.md` and fix each failure. An item that does not apply to the detected project type may be omitted only when the README claims no such surface. The checklist covers structure (project name and tagline, visual separator, Installation, Quick Start, Features, Usage, Contributing, License), content (accurate installation, copy-pasteable quick start, features that describe user capability not implementation, real tested examples, contributing workflow, license named and linked), accuracy (no non-standard tools beyond Installation, no hardcoded paths that contradict the project, no versions that contradict the manifest, no claims about features the project lacks), and presentation (badge images load, no broken relative links, language tags on code blocks, no overlong paragraphs, consistent heading levels).

## House standard and the five gates

A public README that must match the house standard follows a fixed section order: What is this, Install, Quick start, core sections, Development, License. No extra top-level sections appear before Install or after License. Per-archetype templates (CLI tool, npm library, Swift package, macOS app, web service) define which sections follow Quick start and Development; infer the archetype from project structure (`package.json`, `go.mod`, `Package.swift`, `*.xcodeproj`, `Cargo.toml`) or from user-supplied metadata, and stop when the structure matches no known archetype and none was supplied.

Run all five gates before shipping:

1. Every command in Install and Quick start runs against the current project. A command that cannot run (missing binary, no network) is marked blocked with the reason stated.
2. Every code sample typechecks or compiles against the current API.
3. Every relative link resolves to an existing file in the repo. Every external link returns HTTP 200 non-404. Every badge URL returns HTTP 200 and not the shields "invalid" card.
4. No hardcoded package versions, stale minimums, or "coming soon" for shipped features, checked against `package.json`, `go.mod`, `Package.swift`, or the equivalent.
5. The section order matches the fixed order, with no extra top-level sections before Install or after License.

Each gate gets a pass, fail, or blocked verdict with a concrete finding for every non-pass. Claiming done while any gate fails or stays blocked is rejected; report partial passes as partial passes. When a write partially succeeds, restore the file to its pre-write state before reporting the failure. The terminal classification is `done`, `done-with-fixes`, or `non-converged`.

## What you hand back

The edited README.md, structured as opening block, facts list, 4-10 line example with output, and getting-started guide, formatted for skimmers, with every claim sourced from the repo, the user, or a measurement. When blocked, the partial README plus a report naming the unsourced claims and the unresolved clean-machine setup gaps.
