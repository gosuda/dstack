---
name: docs-writing
description: 'Use when asked to write, restructure, or audit documentation with Diataxis types, or to draft a feature docs page or diagram source. Not for ADRs or architectural rationale.'
---

# Docs writing

Good documentation lets a reader find the right page, follow it unaided, and trust what it says. This skill produces docs that each serve one purpose (learning, doing, looking up, or understanding) and that survive a strict audit before they reach the reader.

Use it when someone asks for new docs, a restructure, an audit, a feature docs page, or a diagram source. Anything that argues why a decision was made belongs elsewhere, not here.

## What you are allowed to touch

You work only inside the named documentation directory or file set in the working repository. You never write outside that set, never touch protected files, and never mutate anything remote. Every write is a local file write, reversible through version control. If the target path sits outside the repo or on a protected file, stop and name the rejected path before writing anything.

## What you need before you start

Ask for anything missing and write nothing until you have it:

- The target directory or file set, the intent (new docs, audit, restructure, or feature draft), the subject, the intended audience, and the output format (markdown, plain text, or a diagram source).
- For feature docs, additionally the feature specification or PRD and the codebase path where the feature is implemented.
- Helpful when available: an existing Diataxis map, a scope limit naming which files are in bounds, existing docs to update, a diagram type, and a length limit.

## Bound the work first

Record the target set, subject, audience, and format. Refuse anything outside the named set. If subject, audience, or format is missing, stop and ask, because guessing any of them produces docs for the wrong reader.

## Give every doc one job

Classify each doc into exactly one Diataxis type and split or retitle anything that straddles two:

- Tutorial: learning-oriented, a guided path a beginner completes with a visible result at each step.
- How-to guide: goal-oriented, steps an experienced user follows without backtracking.
- Reference: information-oriented, facts findable in under 30 seconds, each entry shaped as name, then type, then default, then description, then example.
- Explanation: understanding-oriented, context a reader can restate in their own words.

A doc that mixes types gets split, never relabeled to dodge its check. Link the types to each other when you finish: tutorials point forward to the how-to and reference they prepare for; how-tos point to the reference and the explanation behind them; references and explanations point back to the practical pages.

## Draft from evidence, not memory

Write the prose or diagram source for the named subject and audience in the requested format, deriving the wording fresh rather than copying upstream expression. For feature docs use the section shape Overview, Prerequisites, Usage, API Reference, Configuration, Troubleshooting, and fill every section only from the spec and the code, with real code examples drawn from source or tests. Never invent APIs, flags, defaults, or behaviors. Where spec and code disagree, note the mismatch in the draft and flag it for review instead of silently picking a side.

When a diagram needs rendering, write its source and state the render command without running it unless asked.

## Audit the draft until it passes everything

Work through each lens below and fix what fails inside your scope. Anything you cannot fix stops the job: leave the docs in their last consistent state and report the unmet criterion with the file it blocks. Never claim success while any check is unmet or unverified.

### Structure

Lead with the bottom line. Put conditions before the action they gate. One idea per section, no filler sections. Tutorials carry a quick start and a procedures section. Every doc ends with next steps, and the first heading gives an overview of the doc.

### Clarity

One idea per sentence. No Latin abbreviations, no nominalizations, serial comma throughout. Prefer concrete names (real files, commands, APIs, paths) over vague nouns, and precise verbs (`configure`, not `set up`; `verify`, not `check`). Use the passive only when the actor is genuinely unknown. Every sentence must carry information no earlier sentence carried; no placeholders, no invented symbols or values. If no draft exists yet, you may scaffold section structure from the document type, but flag every missing value as a gap rather than filling it in.

### Code examples

Examples run, use named functions and realistic names, show error descriptions, and move from isolated snippets to full context with a sane code-to-context ratio, covering more than one language where the docs demand it. For CLI docs, trace every flag, default, precedence claim, and guarantee back to the current parser, resolver, constants, or observed help output; names and templates alone are not evidence. Quote help output and transcripts as verbatim and name the version or source state they describe. Never invent a transcript or claim an example was executed on the strength of reading source. Before trying any executable example, confirm the assignment authorizes its side effects, since documentation authority alone never authorizes builds, installs, network writes, or quickstart mutations. When execution is authorized, run the exact documented block, account for inherited environment and stale binaries, and record the actual exit result; otherwise mark execution unverified. Keep isolation, transactional, platform-support, and safety claims scoped to the components and phases the evidence actually covers. Invent no badges or volatile counts. Validate relative links and heading fragments, not just file existence.

### Format

Sentence-case headings; bold for UI elements and code font where each fits; descriptive link text; alt text on images; lowercase filenames; periods inside quotes; semantic HTML; parallel heading forms; consistently punctuated lists; tables with no empty cells that should hold data; a language tag on every code block.

### Voice

No anthropomorphism, no unexplained jargon, requirements language where obligation is meant.

### Hygiene

Delete outdated content, keep a docs directory, no temporal language, label experimental and retconned content, keep metadata current. When auditing currency across a named doc set, enumerate version claims by syntax class and read status tables and identity claims that carry no version number. Treat each candidate as a current-channel claim, a minimum supported version, a past event, or a machine-consumed literal before proposing any change. Re-ground current claims against their own release or support source and record the access date. Preserve historical events, version floors, exact machine literals, and simulated output, since a prose release label never belongs inside a tool readout. Check spelling variants, surrounding paragraphs, and files the first pass missed. Reconcile volatile claims with their sources before presenting; a changed or unreachable source is reported as uncertainty, never as grounded just because a date marker exists. Configuration changes, manifest bumps, commits, and remote operations stay outside this authority.

### Navigation

Every doc linked, relative paths, searchable headings, breadcrumbs that give context, no repeated navigation, limited layer depth.

### Review and scan

Verify links resolve. A check that cannot run (no resolver available) counts as unmet, not as passed. API references use a three-column layout whose entries still carry all five fields (name, type, default, description, example).

### Screenshots for feature docs

Capture or request a screenshot of the feature in action, each with descriptive alt text and a caption naming the UI state shown. Where the runtime cannot produce screenshots, leave `<!-- screenshot: pending -->` and note the gap in your report.

## Let the human read before anything is written

Present the audited draft for review and iterate in chat; nothing reaches disk until the draft is approved. A request to draft without writing files stays chat-only, still gated on review before any later write, and no file is ever created for it. If review rejects the draft, revise against the feedback and present again. An empty or invalid draft is discarded with the failure reported, never written.

After approval, write the file to the target path. If a partial write fails, delete the partial file and report the rollback. Then confirm the file exists and report its path. For a chat-only request, report instead that no file was written.

## When the job cannot finish

- Missing subject, audience, or format: stop, ask, write nothing.
- Ambiguous Diataxis type that cannot be split: report it as blocked rather than guessing.
- Type validation failure: keep the doc at its classified type and fix the failing predicate; never reclassify to pass.
- Link verification with no resolver: record as unverified, which counts as not met.
- Codebase contradicts the spec: document the discrepancy in a note and flag it; never silently align to one side.
- Generation produces empty or invalid output: discard, report, write nothing.
- Partial write failure: delete the partial file, report the rollback.

## What you hand back

The rewritten, restructured, or newly written documentation files or diagram sources in the target directory, plus a report listing each doc's Diataxis type, its audit result (pass, unmet criterion, or blocked), and each saved path.
