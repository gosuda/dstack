---
name: purge-slop-docs
description: 'Use when a human asks to purge stale docs, clean Markdown, or reorder the documentation hierarchy. Not for code debris. This skill edits Markdown prose only.'
---

# Purge slop docs

You clean up a documentation tree that has gone stale, wordy, or tangled, and you leave it smaller, truthful, and easy to enter. You edit Markdown prose only, inside the documentation tree the request bounds. Vendored trees, dependency directories, generated API output, and files or regions marked generated or do not modify are excluded. When authorship, generation status, or scope cannot be established for a target, you leave that target alone.

## What this touches and what it refuses

Whole file deletion is human gated. Preview every whole file deletion with its consequence and wait for a separate explicit approval before cutting. One explicit approval may cover one exact previewed set of documents; when the set or its consequences change, a new approval is required. Every other write is reversible local work with version control as the rollback.

Refuse the rest outright:

- Code debris and dead code belong elsewhere. This skill never touches code.
- New strategy documents, channel marketing copy, and outward publication are not this skill. Never draft, send, post, or publish on the user's behalf.
- Unbounded or uncertain scope means no changes. Return `BLOCKED` naming the unresolved boundary or authorship question.
- Deletion without a separate explicit approval covering that exact set leaves the file unchanged. Never combine approvals across different sets.
- Never touch code blocks, quoted text, frontmatter, link targets, identifiers, or any token the caller's own contract requires, unless the user names that content as the thing to fix. Preserve externally fixed machine or standard identifiers, legal notices, and numbered procedure steps.
- Never state whether text was written by a model.
- Never delete unverified or protected material by assumption. Being aggressive here means investigating uncertain candidates and completing the authorized cleanup, not cutting blindly.

## Start with a bounded file list

Your inputs are the repository or directory that bounds the Markdown tree plus an explicit human cleanup request, with an optional narrower path or stated exclusions. Work out which Markdown files are project authored and which entry document anchors the tree. Enumerate the files inside the scope, apply the exclusions, and report the resulting file count before changing anything. Never widen the scope to chase a finding.

## Name each finding by its evidence test

Inspect the included files and classify each finding by a concrete test:

- Overstatement: a benchmark lacks a number, a guarantee lacks an enforcing check, a superlative is unproved, or the repository cannot demonstrate the claimed property. Rewrite to the supported claim or remove.
- Jargon: a plainer word preserves the meaning, or a metaphorical noun obscures the mechanism. Substitute the plain term and keep established project vocabulary.
- Outdated: a named path, symbol, flag, command, or version no longer resolves. Check the reference or a safe read only form, then update to verified evidence or remove.
- Redundant: the same meaning has another owner, or prose repeats authoritative configuration. Keep one owner and replace the other with a pointer or remove it.
- Empty ceremony: puffery, trailing significance clauses, promotional adjectives, vague attribution, formulaic outlooks, chatbot openers and closers, sycophancy, process narration, manufactured thoroughness. Delete the ceremony and keep the fact.
- Tautology: a heading restated in its first sentence, a bold label restating its line, a summary repeating the piece. Delete the restatement and end on the last concrete point.
- Stale claim: a guarantee, status, date, or instruction the tree no longer supports. Verify against the repository and correct or remove.
- Duplicated ownership: two documents own the same meaning. Keep the authoritative owner and point.
- Noise: filler, forced triads, synonym cycling, dense sentences, rhythm crutch dashes, decorative emoji, bullets where two sentences read better, headers over two sentence sections. Rewrite for first read comprehension.
- Opaque label: a human-facing filename, heading, section, phase, task label, or finding label uses an opaque code or scheme such as A0, DEL1, ENG-01, DES-02, T3, or an invented letter-number code instead of a short semantic readable name describing the work. The purge detects these labels by scanning human-facing names and labels for letter-digit combinations, acronym prefixes with sequence numbers or counters, and arbitrary alphanumeric codes lacking descriptive words. Externally fixed machine or standard identifiers, legal notices, and numbered procedure steps are preserved. On a hit, replace the opaque code with the semantic name describing the work. When the semantic intent cannot be recovered from context or repository evidence, leave the label unchanged, mark the candidate as an unrecovered finding with MEDIUM certainty, and report it for human clarification.

For wording level checks use `references/slop-patterns.md`.

## Edit only what you are sure about

Grade certainty independently from severity. Apply an edit only when a deterministic check makes the finding HIGH certainty. Report MEDIUM and LOW findings without changing them. Where deterministic evidence is missing, leave the candidate unchanged, downgrade it to MEDIUM or LOW, and mention it only in the report.

## Deleting a whole document takes a separate yes

Treat a whole document as a deletion candidate only when no pointer references it and every section fails at least one evidence test. For each candidate or exact set, preview the exact files, state that no references were found and how that was established, describe the loss including required meaning and links, and ask for a separate explicit yes. A refusal or a missing answer leaves those files unchanged. A changed set or changed consequences need a new approval.

## Put each idea in one place

Within a file, co-locate the definition, rules, and caveats of each concept under one heading. Inline material every reader path needs and put branch specific reference detail behind a direct pointer. By default, every human-facing filename, heading, section, phase, task label, and finding label must use a short semantic readable name describing the work. Replace opaque schemes such as A0, DEL1, ENG-01, DES-02, T3, or invented letter-number codes with the semantic name for that purpose. Preserve externally fixed machine or standard identifiers, legal notices, and numbered procedure steps. Before any mass rename, build a link map of every inbound and outbound reference, heading anchor, and filename occurrence across the tree. Detect these labels by checking candidate strings for letter-digit sequences, phase-counter tags, or synthetic codes that lack descriptive words. On a hit where the underlying intent is clear from context or repository history, rename the item and update all mapped references. If the semantic intent cannot be recovered with certainty, leave the label unchanged, treat it as a finding that requires human clarification, and report it without guessing. Across the tree, let the entry document say what the project is and where to start while detail stays reachable through pointers. Every non entry document needs an inbound pointer; a document with none must be the entry document or an individually reviewed deletion candidate.

## Prove the pointers still work

After each move, deletion, or pointer rewrite, verify every affected Markdown link and repository path resolves. Before performing any mass rename, compile a link map covering all inbound and outbound paths, headings, and anchor targets across the tree, and update them together. When a pointer breaks, restore the pre change arrangement for that operation or repair it from verified repository evidence. If verified cleanup keeps creating new broken references or conflicting ownership, stop, leave the last verified state intact, and return `NON-CONVERGED` with the remaining findings.

## What you hand back

The cleaned documentation tree plus a terminal report with the scope, the file count, per class finding counts using short semantic names for every finding label, applied edits versus reported only findings, unrecovered opaque label candidates left unchanged, deletions with their approvals, pointer check results, and one of `DONE`, `BLOCKED`, or `NON-CONVERGED`. When a mutation is interrupted, report exactly which files changed, moved, were deleted, or remain pending. Never infer approval, hide an error, or claim completion. A broken pointer that cannot be repaired returns `BLOCKED` with the unresolved pointer, keeping unrelated already verified edits as an explicit partial result.
