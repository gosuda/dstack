---
name: docs-practices
description: 'Use when deciding whether a durable document, ADR, plan, or spec is needed, or when checking its invariant quality, scope, and naming. Not for drafting prose or restructuring agent-consumed documents.'
---

# Docs practices

Decide whether a durable record is warranted, then hold it to invariant quality. The default answer is no new document. This covers proposed, drafted, or under-review durable documents, ADRs, plans, and specs for scope, naming, and lasting value. Drafting, ghostwriting, or restructuring prose on request is out of scope: judge need, scope, and naming only.

## What you need

You need the proposed or existing document path, or the claim that needs a durable home, plus the invariant the record would protect stated in one sentence. Existing sources already covering the topic, with the enforcement and proof each provides, come along when they exist.

## Keep a record only for a material invariant

Protect with a durable record only a material generalized invariant that future readers must obey or rely on. Notes about what happened, what was decided when, and what was learned once do not qualify. Lacking such an invariant means rejecting the proposal outright.

Before writing, search for a sufficient existing home and read the candidate sources. Reuse the sufficient source and add a pointer when it covers the invariant; write anew only when none suffices. Activity records, decision diaries, meeting notes, status logs, mini-learnings, and jargon never belong in durable records. Code comments never substitute for a missing record: fix the record or leave the gap explicit. Placeholders, deferred sections, follow-up promises, and excuses never ship as content.

## Scope, enforcement, and proof must be explicit

Each kept record states its scope of application, what enforces it, and what proof shows a violation. Remove material that applies once, applied in the past, or restates configuration the source of truth already owns. Accept only independent or adversarial evidence that detects a plausible material fault and survives equivalent refactors. Fixture inputs and setup are permitted; saved-output pins, literal snapshots, mock echoes, and source-text assertions are rejected. Weak tests are never admitted under any circumstances. Never weaken a lint or drop proof to meet a length or percentage goal; load-bearing clause identifiers, evidence rows, and measured facts stay where their consumer still needs them.

## Name everything a stranger can understand

By default, human-facing doc names, headings, sections, phases, and labels use short semantic readable names. Never name them with opaque codes such as A0, DEL1, ENG-01, or DES-02, bare numbers, coded prefixes, random letters, hashes, date prefixes, or Roman numerals. Replace each opaque label with a short semantic name describing the work. Require a link map before mass renames to track every affected link, pointer, and reference to its new target. Useful numbered procedure steps, quoted historical evidence, legal notices, and externally fixed machine or standard identifiers stay unchanged. A genuine externally fixed clause identifier stays with a human-readable label beside it; never invent new opaque codes for organization. The tree passes when no opaque label remains and every affected link resolves; a rename that breaks a link gets restored or repaired from verified evidence, then every affected link is re-verified.

Legal notices, license text, required attribution, and quoted evidence stay intact throughout. Never generalize a time-bound fact into a timeless rule. Missing authority or prerequisites stay reported as blocked with the exact missing item; finish reachable narrowing and renaming, then stop rather than inventing coverage. Uncertain ownership or scope means changing nothing in the uncertain region and reporting the boundary question as blocked. When repeated narrowing creates new broken references or ownership conflicts, keep the last verified state and return the remaining findings.

## What you report

A verdict per record: kept with its invariant, scope, enforcement, and proof, or rejected with the sufficient existing source or the reason no record applies. Plus the narrowed or renamed tree and a terminal report with kept, rejected, and blocked counts, every rename with its link map and updated links, and the link-check result. Whole-document deletion needs separate explicit approval for that exact set; rollback is version control or undo, and nothing is published, installed, or committed.
