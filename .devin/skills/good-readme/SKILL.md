---
name: good-readme
description: 'Use when the user asks to create, rewrite, review, or polish an open-source README. Produces one evidence-backed README.md in a fixed section order and checks it with five gates. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Good README

A README decides in seconds whether a stranger keeps reading. This skill writes one that says what the project does and why it differs, shows a runnable taste, and gets the reader from a clean machine to a working result. Every claim in it comes from the repo, the user, or a measurement.

## Scope and safety

- Writes: only `README.md` in the local working copy. Create it if it does not exist. Version control or editor history is the rollback.
- Reads: any project file, plus read-only HTTP GET or HEAD requests to check external links and badge URLs.
- Never: push, publish, deploy, touch credentials, or mutate anything remote.
- Commands from the README run only locally. A command that would need credentials, a network write, or a system-wide change is not run; its gate result is blocked with the reason.

If a write partially fails, restore the file to its pre-write state before reporting the failure.

## Gather evidence first

Read the existing README if there is one, the package manifest (`package.json`, `go.mod`, `Cargo.toml`, `Package.swift`, `pyproject.toml`, `*.xcodeproj`, or the equivalent), the source entry points, the license file, and any benchmark or size data. List which facts are present (differentiators, numbers, sizes, supported platforms) and which are missing.

A fact the repo lacks and the user cannot supply stays out of the file. Never estimate a number or invent a differentiator. When a differentiator or number is missing, ask the user for it or for how to measure it.

Resolve intent before drafting. When the primary audience, project phase, or emphasized section is unclear, ask one question. If intent stays unresolvable, stop with `blocked: unresolvable-intent`.

## Pick the archetype

Infer the project archetype from its structure or from user-supplied metadata: library or package, CLI tool, web application or service, or desktop app. The archetype decides which core sections appear; `references/section-templates.md` lists them. If the structure matches no archetype and the user supplies none, ask; without an answer, stop with `blocked: unknown-archetype`.

## Follow one section order

Every README uses this order. Archetypes change only the core sections.

| Position | Section | Contents |
|----------|---------|----------|
| 1 | Title block (no heading of its own) | Project name, one-line tagline, optional badge row, opening paragraph, facts list, short example |
| 2 | Install | Copy-pasteable commands to add the project to a machine or an existing project |
| 3 | Quick start | The shortest path from installed to a working result |
| 4 | Core sections | Features and Usage first, then the archetype-specific sections from `references/section-templates.md` |
| 5 | Development | Local setup, test, and build, with a Contributing subsection (or a link to `CONTRIBUTING.md`) |
| 6 | License | License name and a link to its full text |

No top-level section goes before Install or after License. Install, Quick start, Features, Usage, Contributing, and License are never omitted. Features lists what the reader can do, beyond the few facts in the title block; Usage shows real use. When the project takes no outside contributions, the Contributing subsection says so in one line. Add a table of contents after the title block when the file runs past about two screens.

## Write the title block

The title block answers "what is this" before any heading, in four short parts:

1. Tagline: one line under the project name.
2. Opening paragraph: what the project does, how the reader benefits, and what differs from the alternatives. Source differentiators from the repo or the user.
3. Facts list: a few bullets, each led by one or two bold keywords and backed by concrete evidence such as a benchmark number, an exact size, a comparison with the closest alternative, or a screenshot or diagram that replaces a paragraph.
4. Example: 4 to 10 lines of usage with the output shown in a comment, so the reader sees the result without running anything. It illustrates; Install and Quick start do the real setup.

Put the badge row between the name and tagline line and the opening paragraph, following `references/badges.md`. Keep a badge only when project files prove its repository, workflow, registry package, license, or coverage integration, and prefer a plain statement of fact over a badge that says the same thing.

## Write Install and Quick start

Derive installation from project files: manifests, release configuration, build scripts. If no install path can be derived, stop and report `no-install-path` with the files checked.

Write every step as a copy-pasteable command; leave none implied. Then validate the path by following it from scratch as if the project were unfamiliar, and fix every gap. When a missing step or failing command cannot be resolved, mark the guide incomplete and stop.

Fill the core sections and Development from project files. Summarize and link to source locations rather than copying large blocks of code.

## Format for skimmers

- Headings carry the hierarchy, with consistent levels.
- Lists replace dense paragraphs.
- Bold appears in two places only: the keywords leading each facts bullet, and at most one or two must-not-miss lines elsewhere (a blockquote also works for those).
- Every code block names its language.

Reading only the headings and the bold text should still tell the story.

## Check quality, then run the gates

Work through `references/quality-checklist.md` and fix every failure. Skip an item only when the README claims no such surface.

Then run the five gates. Each gets pass, fail, or blocked, with a concrete finding for every non-pass.

1. Commands: every command in Install and Quick start runs against the current project. A command that cannot run (missing binary, no network, needs credentials) is blocked with the reason.
2. Code: every code sample typechecks or compiles against the current API.
3. Links: every relative link and heading fragment resolves in the repo. Every external link answers a read-only GET with a non-error status. Every badge URL returns HTTP 200 and not the shields "invalid" card.
4. Versions: no hardcoded package version, stale minimum, or "coming soon" for a shipped feature contradicts the manifest.
5. Order: the sections follow the fixed order, with nothing before Install or after License.

Claiming done while any gate fails or stays blocked is rejected. Report partial passes as partial passes.

## What you hand back

- The edited `README.md`.
- The gate table with a finding for each non-pass.
- A terminal classification: `done` (passed on first check), `done-with-fixes` (passed after fixes), or `non-converged` (a gate still fails or is blocked), or one of the stop codes `no-install-path`, `blocked: unresolvable-intent`, `blocked: unknown-archetype`.
- When not done, the list of unsourced claims and the unresolved setup gaps.
