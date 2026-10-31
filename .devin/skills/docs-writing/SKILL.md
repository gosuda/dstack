---
name: docs-writing
description: 'Use when asked to write, restructure, or audit documentation with Diataxis types, or to draft a feature docs page or diagram source. Not for ADRs or architectural rationale.'
---

# Docs writing

Good documentation lets a reader find the right page, follow it unaided, and trust what it says. This skill produces docs where each page does one job (learning, doing, looking up, or understanding), drafts them from evidence, audits them, and writes nothing until a human approves the draft.

Use it for new docs, a restructure, an audit, a feature docs page, or a diagram source. Content that argues why a decision was made belongs in an ADR or design record, not here. To resync existing docs after code changes, use `docs-update`.

## Scope and safety

- Writes go only to the named documentation directory or file set inside the working repository, as local file writes that version control can revert.
- Never write outside that set, touch protected files, or mutate anything remote.
- Builds, installs, network writes, commits, manifest bumps, and configuration changes are outside this skill's authority unless the assignment grants them explicitly.
- If a target path sits outside the repo or on a protected file, stop and name the rejected path before writing anything.

## Inputs

Ask for anything missing and write nothing until you have it.

| Input | Required | Notes |
|-------|----------|-------|
| Target directory or file set | Yes | Defines the write boundary |
| Intent | Yes | New docs, audit, restructure, or feature draft |
| Subject and audience | Yes | Guessing either produces docs for the wrong reader |
| Output format | Yes | Markdown, plain text, or a diagram source |
| Feature spec or PRD, and the implementing code path | For feature docs | The only allowed sources for feature content |
| Diataxis map, scope limit, existing docs, diagram type, length limit, project style guide | Optional | Use when available |

## Give every doc one job

Classify each doc as exactly one Diataxis type:

| Type | Serves | Passes when |
|------|--------|-------------|
| Tutorial | Learning | A beginner completes a guided path with a visible result at each step |
| How-to guide | A goal | An experienced user follows the steps without backtracking |
| Reference | Lookup | A fact is findable in under 30 seconds; each entry gives name, type, default, description, and example |
| Explanation | Understanding | A reader can restate the idea in their own words |

A doc that straddles two types gets split or retitled, never relabeled to dodge a check. If a doc cannot be split cleanly, report it as blocked.

Link the types when you finish. Tutorials point forward to the how-to and reference they prepare for. How-tos point to the reference and the explanation behind them. References and explanations point back to the practical pages.

## Draft from evidence

Write fresh prose or diagram source for the named subject, audience, and format; do not copy upstream wording.

Never invent APIs, flags, defaults, behaviors, or values. Each claim traces to a source you read. If no source exists yet, you may scaffold the section structure from the doc type, but mark every missing value as a gap.

For feature docs, use the sections Overview, Prerequisites, Usage, API reference, Configuration, and Troubleshooting. Fill each one only from the spec and the code, with examples taken from source or tests. Where spec and code disagree, note the mismatch in the draft and flag it for review instead of picking a side. Capture or request a screenshot of the feature with descriptive alt text and a caption naming the UI state shown; if the runtime cannot produce one, leave `<!-- screenshot: pending -->` and report the gap.

For a diagram that needs rendering, write its source and state the render command. Run it only when asked.

## Audit the draft

Work through every lens and fix failures inside your scope. A check that cannot run counts as unmet, not passed. If a criterion stays unmet, stop: leave the docs in their last consistent state and report the criterion and the file it blocks. Never claim success while any check is unmet or unverified.

The project's own style guide wins over every default below. Where it says nothing, apply the defaults.

### Structure

- [ ] The first heading or paragraph gives an overview, and the bottom line comes first.
- [ ] Conditions come before the action they gate.
- [ ] One idea per section, with no filler sections.
- [ ] Tutorials include a quick start and a procedures section.
- [ ] Every doc ends with next steps.

### Clarity

- [ ] One idea per sentence, and every sentence adds information.
- [ ] Concrete names (real files, commands, APIs, paths) instead of vague nouns.
- [ ] Precise verbs (`configure` over `set up`, `verify` over `check`) and verbs over nominalizations.
- [ ] Active voice unless the actor is unknown.
- [ ] No placeholders and no invented symbols or values.
- [ ] Jargon is defined on first use; requirement words (must, should) appear only where obligation is meant.
- [ ] No anthropomorphizing software.

### Code examples

- [ ] Examples use realistic names, show expected output and error messages, and build from small snippets to full context.
- [ ] Examples cover each language the docs promise to support.
- [ ] Every CLI flag, default, precedence rule, and guarantee traces to the current parser, resolver, constants, or observed help output. Names and templates alone are not evidence.
- [ ] Quoted help output and transcripts are verbatim and name the version or source state they describe. No transcript is invented, and reading source never counts as having run an example.
- [ ] An example is executed only when the assignment authorizes its side effects. When it is, run the exact documented block, account for the inherited environment and stale binaries, and record the real exit result. Otherwise mark it unverified.
- [ ] Isolation, transaction, platform-support, and safety claims stay scoped to the components and phases the evidence covers.

### Format

- [ ] Sentence-case headings in parallel form.
- [ ] Code font for code, commands, and paths; bold for UI labels.
- [ ] Every fenced code block has a language tag.
- [ ] Descriptive link text and alt text on every image.
- [ ] Lists punctuated consistently; tables have no empty cells that should hold data.
- [ ] Lowercase filenames.
- [ ] House defaults such as the serial comma or punctuation placement around quotes follow the project style guide; if none exists, pick one convention and apply it consistently.

### Currency

- [ ] Outdated content is deleted, not annotated. No temporal language ("new", "recently", "currently").
- [ ] Experimental and changed behavior is labeled, and page metadata is current.
- [ ] No invented badges or volatile counts.
- [ ] Each version claim is classified before you change it: current-channel claim, minimum supported version, past event, or machine-consumed literal. Re-ground only current-channel claims against their own release or support source, and record the access date.
- [ ] Historical events, version floors, exact machine literals, and simulated tool output stay unchanged; a prose release label never goes inside a tool readout.
- [ ] Across a doc set, search by syntax variant, read status tables and identity claims that carry no version number, and recheck the surrounding paragraphs and any files the first pass missed.
- [ ] A source that changed or is unreachable is reported as uncertain, even when the doc carries a date marker.

### Navigation and links

- [ ] Every doc is linked from somewhere, using relative paths.
- [ ] Relative links and heading fragments resolve, not just the target files.
- [ ] Headings are searchable, breadcrumbs give context, navigation is not repeated, and nesting stays shallow.
- [ ] API reference tables keep all five fields (name, type, default, description, example) for each entry.

## Review before writing

Present the audited draft in chat and iterate there. Nothing reaches disk until the draft is approved.

- If review rejects the draft, revise against the feedback and present it again.
- A request to draft without writing files stays chat-only; no file is created for it, and any later write still needs approval.
- An empty or invalid draft is discarded and the failure reported, never written.

After approval, write the file to the target path and confirm it exists. If a write fails partway, delete the partial file and report the rollback.

## Stop conditions

| Condition | Action |
|-----------|--------|
| Subject, audience, or format missing | Ask; write nothing |
| Target outside the named set or on a protected file | Name the rejected path; write nothing |
| Diataxis type ambiguous and the doc cannot be split | Report blocked; do not guess |
| Doc fails its type check | Fix the failing predicate; never reclassify to pass |
| No link resolver available | Record links as unverified, which counts as unmet |
| Code contradicts the spec | Note the discrepancy in the draft and flag it |
| Empty or invalid draft | Discard, report, write nothing |
| Partial write failure | Delete the partial file and report the rollback |

## What you hand back

- The approved docs or diagram sources at their target paths, or the draft in chat for a chat-only request with a note that no file was written.
- A report listing each doc's Diataxis type, its audit result (pass, unmet criterion, or blocked), and each saved path.
