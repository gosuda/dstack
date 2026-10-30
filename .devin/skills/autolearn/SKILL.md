---
name: autolearn
description: 'Use when a verified fix yields a generalized well-abstracted invariant with enforcement or proof, or existing solution docs need bounded refresh. Not for unverified fixes, minor learnings, narrative/activity/weak-test stories, retrospective analysis, or remote migration.'
---

# Autolearn

Solved problems evaporate. Autolearn keeps the durable part: one generalized, well-abstracted invariant per write, a reusable mechanism with stated scope, real enforcement or proof, and a material consequence. Narrative choices, activity logs, trivia, tiny one-off fixes, session history, and weak-test stories (fixture snapshots, single-run green, quota-driven write-ups) never qualify, and no quota ever justifies a write. Zero output is a normal, valid result. Retrospective analysis belongs to retro; this skill keeps durable technical capture only. There is no STRATEGY.md prerequisite.

Writes stay reversible and local: the operating repo's `docs/solutions/` and repo-root `CONCEPTS.md`, staged only from surfaces this skill wrote or edited, committed locally by the repo's flow, never pushed. Publication needs a separate explicit authority. Nothing here performs remote, publish, deploy, credential, or paid mutation. The skill directory resolves from this skill's own directory: `references/schema.md`, `references/concepts.md`, `scripts/validate-record.py`, `assets/solution-template.md`. Never invoke a peer skill at runtime for these contracts.

## Route first: strip tokens, pick the job

Control tokens come off before anything else is read as context or scope. Accepted tokens are `mode:refresh [scope]`, `mode:headless`, `consent:write`, and `consent:cross-branch`. Unknown or repeated tokens are errors.

| Route | Job |
|---|---|
| Capture, the default | Document one generalized invariant from a solved technical problem |
| Vocabulary capture | Reconcile a durable reusable project term in `CONCEPTS.md` |
| Memory handoff | Surface a fact about the user, preferences, or cross-project context as a handoff candidate for the memory system, never written into `docs/solutions/` or `CONCEPTS.md` |
| Refresh | Bounded maintenance of existing docs and vocabulary, never implicit delete or migration of stored records |
| Headless, overlaying any route | Skip questions, never pause, apply safe actions, mark genuinely uncertain docs stale |

Phrases like "that worked", "it is fixed", or "tests pass now" permit evaluation without fabricating evidence and never count as admission by themselves. One run may write a learning doc, reconcile a concept, and flag a handoff candidate together.

## The gate that says no

Capture starts from rejection. Three preconditions must all hold: the problem is solved, not in progress (a finished abandoned attempt counts only when its learning is a reusable anti-pattern invariant, naming the specific failure reason plus when retrying would make sense); the solution is observed working, with actual enforcement or proof (guardrail, check, reproduction, or reference behavior), never a claimed run; and the write carries a generalized invariant, a reusable mechanism rather than an incident, project name, command, version, or path, with supported scope stated without overgeneralizing beyond the evidence and a material consequence stated (it prevents a plausible significant failure or improves a recurring decision). Being solved, verified, or non-trivial alone is never a shortcut.

Then three filters run in order: would this be forgotten without a record and reused under stated inputs; is it already covered (improving the existing invariant beats writing, since duplicating is drift); is the claim scope-qualified and no broader than the evidence. The same gate governs vocabulary: precise local meaning, not already defined, scope-qualified to this project. Anything failing the gate exits in one line with no write.

## What you need on hand

The verified fix or solved problem comes from conversation history or the codebase, and must be supplied or derivable; without it there is nothing to capture. Refresh takes an optional scope hint. Any injected auto-memory block is supplementary context, never primary evidence: tag memory-derived lines that land in a doc with `(auto memory [claude])`, and prefer code or conversation when memory conflicts with either. Headless runs need `consent:write` before writing; cross-branch consolidation needs `consent:cross-branch`.

## Research before writing

Scan any injected memory block for related entries and carry matches as labeled supplementary context. Then dispatch three read-only researchers that write nothing: a Context Analyzer picking the track (bug versus knowledge), `problem_type`, category directory, and slug filename (human-readable semantic `[sanitized-problem-slug].md`, no date, serial, or hash noise) plus a frontmatter skeleton with no invented enums; a Solution Extractor pulling the invariant substance: incident details may inform extraction of root cause and frontmatter metadata but never ship as a session diary or incident retelling; the durable body extracts only the invariant mechanism (what must always or never hold, never an incident retelling, project name, command, version, or path), supported scope (where the invariant holds and where it does not, stated without overgeneralizing beyond evidence), material consequence (what fails when violated: plausible significant failure prevented or recurring decision improved), enforcement or independent proof (concrete guardrail, check, or test that exercises the invariant and fails on violation; never a mock echo or fixture snapshot), and necessary counterexample or limits (concrete violation conditions, boundary cases, or known limits where the invariant does not apply), stating the mechanism without overgeneralizing beyond evidence and keeping the body semantic invariant rather than a fixture snapshot oracle (references clear the extreme test bar or stay out); and a Related-Docs Finder grepping `docs/solutions/` frontmatter on keywords, reading frontmatter of candidates, fully reading only strong matches, and scoring overlap across problem, cause, solution, references, and prevention as High (4 to 5), Moderate (2 to 3), or Low (0 to 1). Without subagents, run the same pass inline and record the degraded coverage. Wait for all three before assembling.

## Write it and prove it

The overlap gate decides the shape: High overlap updates the existing doc (keeping its path, adding `last_updated`); Moderate creates normally and notes a consolidation candidate; Low creates normally. Read `assets/solution-template.md` and assemble the doc with only invariant, supported scope, material consequence, enforcement or independent proof, and necessary counterexample or limits. Incident details may inform extraction but never ship as a session diary. Read rationale records for overlap only; never rewrite one into the solution schema. Write frontmatter per the local `references/schema.md`, quoting values the validator requires quoted, keeping provenance as metadata only, making no claim the evidence does not support. Never change the stored record schema or field shapes. Write to `docs/solutions/<category>/<slug>.md` (category from the schema map, slug human-readable semantic, no date, serial, or hash noise), then validate from the skill directory:

```bash
python3 scripts/validate-record.py docs/solutions/<category>/<slug>.md
```

Quote, rewrite, and re-run until exit 0. A non-zero exit blocks the write. Read the file back to confirm it landed as intended. When a durable term surfaced that clears the gate, reconcile `CONCEPTS.md` per its local concepts contract.

## Refresh only what the new learning disturbs

Recommend a narrow bounded refresh only when the new invariant contradicts or supersedes an older doc, the work invalidated references (refactor, migration, rename, dependency bump), or the finder surfaced strong candidates. Otherwise capture first and skip refresh explicitly.

`CONCEPTS.md` at the operating repo root is the shared glossary with compound as co-writer. Follow the bundled concepts contract: locate or create only when a term clears the gate, search before adding, add one well-shaped entry, read back to confirm no duplicate heading. Never scaffold an empty file.

## Maintain the shelf

Refresh scope covers every `.md` under `docs/solutions/` except `README.md`. A `[scope]` hint narrows in order: subdirectory name, frontmatter `module`, `component`, or `tags` match, filename partial, content keyword. No match reports the miss and exits. With no candidate docs at all, report it and point at create mode.

Classify every candidate into exactly one outcome:

| Outcome | When | Action |
|---|---|---|
| Keep | Generalized invariant still accurate, material, enforced or proven | No edit; say why it stays trustworthy |
| Update | Core invariant mechanism correct, references drifted | Evidence-backed in-place edits |
| Consolidate | Two or more docs overlap heavily, all correct | Merge unique content into the canonical doc, repoint references, delete the subsumed doc only with explicit authority |
| Replace | Old guidance misleads, better invariant answer known | Write a validated successor, then delete the old file |
| Delete | Domain gone, fully redundant, inbound references absent or decorative | Delete only with explicit authority; never archive into `_archived/` |

Evidence beats scorecards; prefer the no-write Keep; no low-value churn (typo or polish-only edits are not refreshes); age alone is never stale; rewriting the Invariant section is Replace, not Update. Only invariants may be newly recorded on refresh. Before Delete, grep repo markdown for citations: decorative citations may be cleaned, substantive citations force Replace, unclear citations force a stale mark. Consolidation requires identical `record_kind` values (rationale with rationale, solution with solution); preserve every input's `origin_records` as the ordered union and drop no input tuple. Cross-branch conversion needs `consent:cross-branch` plus a complete lossless field and body mapping; without both, leave both inputs unchanged and report the consolidation as blocked. After every write, update, consolidation, or replacement, run the bundled validator until exit 0 and read the file back; preserve `origin_records` unchanged on refresh edits.

Headless runs attempt safe actions, mark genuinely uncertain docs `status: stale` with `stale_reason` and `stale_date`, and record failed writes as Recommended rather than retrying into a mess. Emit Applied versus Recommended sections with per-file path, classification, evidence, and action.

For execution shape, see `references/refresh.md`, which defers to this skill for scope, delete authority, citation checks, validation, provenance, and headless stale marking. Prefer the lightest path: Focused (1 to 2 files) means investigate then recommend; Batch (up to about 8 mostly-independent docs) means grouped recommendations; Broad (9 or more, ambiguous, or repo-wide) means triage first (inventory frontmatter, cluster by area, spot-check whether referenced files still exist), then investigate in batches. Investigators are read-only subagents returning path, evidence, recommended action, confidence, and open questions; they never write. Deletes, commits, and frontmatter metadata stay with the orchestrator; even for Replace, the orchestrator validates the successor, deletes the old file, and commits. Most Updates and Consolidations apply directly without asking; ask only when the right action is genuinely ambiguous, about to Delete without explicit authority, about to Consolidate with no clear canonical, or about to Replace, one question at a time with a recommended option first. A doc that grew to cover several genuinely independent problems is a split candidate. A Replace successor needs the old doc's full content, an investigation-evidence summary (what changed, what the code does now, why the old guidance misleads), the target path and category, and the contents of `references/schema.md` plus `assets/solution-template.md` (never invented from memory); the successor states only the invariant mechanism with supported scope, material consequence, enforcement or independent proof, and necessary counterexample or limits, with optional `supersedes: [old-filename]`. Tag memory-sourced findings `(auto memory [claude])`.

## Move house only on purpose

Migration is explicit and approved, never incidental and never part of capture or refresh. Bind the exact source set, destinations, and window first. Classify each source per `references/schema.md` (canonical, `legacy-autolearn-v0`, `legacy-compound-v0`, explicitly scoped `legacy-keep-why-v0`, `unmigrated`, `ahead-blocked`). Convert autolearn shapes to `record_kind: solution` and compound shapes to `record_kind: rationale`; never force either branch's fields onto the other. Preserve dates (missing or invalid dates stay `unmigrated`), preserve tags and body meaning, move legacy body detail into body sections, and attach complete `origin_records` digested from original bytes. Never silently change the `odin-learning/v1` shape. All-or-nothing per set: any `unmigrated` source leaves the whole set unchanged. Only named files are in scope; undiscovered external stores get reported, never read or migrated. The pre-migration commit is the restore point; without version control, block rather than inventing a backup store. Publish atomically; on failure restore every touched file.

## Commit like a guest

One learning per commit on capture; one concern per commit on refresh, with the DStack `Op:` trailer in the refresh body. Stage only surfaces this skill wrote or edited, never unrelated dirty files. Commit locally by the operating repo's flow and skip when nothing changed. Never push.

## What can still go wrong

Validation failure means quoting the named field, rewriting, and re-running until exit 0; never declare success while failing. Overlap collision resolves to updating the existing doc, since duplicating is drift. Insufficient evidence for Replace means marking `stale` in place rather than guessing a successor. A late-discovered substantive citation reclassifies off Delete. Partial refresh failure records as Recommended without retrying into a mess. Rollback reverts the local commit or restores the file from history, since all writes stay under version control.

## What you leave behind

One validated generalized invariant doc at `docs/solutions/<category>/<slug>.md` (or an improved existing doc), optionally a `CONCEPTS.md` entry and a handoff candidate, or a one-line qualification failure. Each doc states a reusable mechanism with supported scope, material consequence, enforcement or independent proof, and necessary counterexample or limits: no incident retellings or session diaries, no speculative universal truths, no quota-driven output. In refresh mode, a bounded report classifying every in-scope doc into Keep, Update, Consolidate, Replace, Delete, or stale with applied and recommended actions; refresh records only invariants and never implicitly deletes or migrates stored records.

This procedure extends the prior `dstack-knowledge` autolearn flow (evaluation gate, three read-only researchers, overlap discipline, Bug and Knowledge tracks, refresh loop, memory provenance and handoff, local commits) onto the canonical `odin-learning/v1` union owned by compound. Upstream MIT attributions remain in `licenses/NOTICE`.
