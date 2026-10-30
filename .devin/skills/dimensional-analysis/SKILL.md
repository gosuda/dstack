---
name: dimensional-analysis
description: 'Use when code mixes units, fixed-point precisions, scaling factors, rates, prices, shares, or conversions. Not for type-level unit modeling: use type-driven.'
---

# Tracing mixed units through the code

Some codebases do arithmetic where the numbers carry hidden dimensions: token precisions, scaling factors, rates, prices, shares, currency conversions. Get one factor wrong and money moves. This skill walks such a codebase end to end, annotating every numeric quantity with its dimension in comments, propagating those dimensions through the arithmetic, and validating that both sides of every operation balance. Anything that does not balance is a finding, not an explanation.

The work is comment-only. It writes dimensional annotations into the in-scope source files plus three artifacts in the project root: `DIMENSIONAL_SCOPE.json`, `DIMENSIONAL_UNITS.md`, and a findings report. Executable code, types, and logic never change. Rollback is version control for the comments, or deleting the three generated files. You are done when every in-scope file has a terminal annotation, propagation, and validation status, no PENDING entries remain anywhere, blocked files reconcile exactly with the report, only comments changed, and confirmed and refuted mismatches are listed separately.

For genuine type-level unit modeling (newtypes, phantom types, compile-time dimension checking), use type-driven instead. That changes code; this only annotates it.

## Inputs you take

The project root path, which is required. You may reuse a pre-existing `DIMENSIONAL_UNITS.md` and `DIMENSIONAL_SCOPE.json`, but only when their `project_root` matches this repo and they carry the required structure; otherwise discard and regenerate. There is no mode argument: the full four-phase pipeline below always runs end to end, never a subset. Never substitute ad-hoc dimensional reasoning for a skipped or unlaunched phase, and never invent evidence.

## Bounding scope and vocabulary

First, confirm the project root and find every file doing numeric arithmetic with mixed units, precisions, scaling factors, rates, prices, shares, or conversions. Prioritize each as CRITICAL, HIGH, MEDIUM, or LOW, then write `DIMENSIONAL_SCOPE.json` to the project root with `project_root`, `in_scope_files` (all priorities), `discoverer_focus_files` (narrowed to CRITICAL/HIGH only when more than 50 arithmetic files turn up), `recommended_discovery_order`, and every in-scope file initialized to `step2: "PENDING"`, `step3: "PENDING"`, `step4: "PENDING"`. If no arithmetic files exist, write an empty manifest and skip to the final report with zero findings.

Next, read that manifest as the source of truth and infer the vocabulary from naming, interfaces, constants, and decimal scaling: base units, derived units, precision prefixes. Write `DIMENSIONAL_UNITS.md` to the project root with `Base Units`, `Derived Units`, and `Precision Prefixes` sections (the same empty headings when nothing is in scope). If nothing is in scope after this step, skip to the final report with zero findings.

If either artifact arrives stale or malformed, the phase that owns it reruns it (the scanner owns the scope manifest, the discoverer owns the vocabulary). Discard, do not patch.

## Annotating anchors

For every file in `in_scope_files`, add dimensional comments at the anchor points (state variables, struct fields, function parameters, return values, inline arithmetic) using the vocabulary and the `D{decimals}{dimension}` format. Work in batches: 10 or fewer files go in one batch; 11 to 30 go in one batch per category; more than 30 go in one batch per category with any category larger than 10 files split into sub-batches of about 8. Process categories in `recommended_discovery_order`: math libraries first, then oracles, then core logic, then the peripheral. Set `step2 = "PENDING"` for every in-scope file before launching and persist the manifest.

After each batch, persist exactly one status per file: `ANNOTATED`, `REVIEWED_NO_ANCHOR_CHANGES`, or `BLOCKED`, with `step2_reason` and `step2_retry_count` on every `BLOCKED` entry. Retry each blocked file once with a focused prompt. Never advance while any `step2` is still `PENDING`. A phase that cannot clear PENDING after its one retry makes the run non-converged: report every blocked file with reason and retry count and do not claim completion.

## Propagating dimensions

With every file holding a non-pending `step2` status, set `step3 = "PENDING"`, persist, and extend the annotations through arithmetic, function calls, and assignments using dimension algebra (multiplication combines dimensions, division inverts, addition requires matching dimensions). Use the same batching and category order as annotation. After each batch, persist exactly one status per file: `PROPAGATED`, `REVIEWED_NO_PROPAGATION_CHANGES`, or `BLOCKED`, with `step3_reason` and `step3_retry_count` on blocked entries, and retry each blocked file once. Aggregate the annotations by confidence (`CERTAIN`, `INFERRED`, `UNCERTAIN`), mismatches with severities, and coverage gaps that could not be inferred. Do not advance while any `step3` is `PENDING`.

## Validating and reconciling

With every file holding a non-pending `step3` status, set `step4 = "PENDING"`, persist, and validate every file in priority order without skipping lower tiers: first files with CRITICAL or HIGH step 3 mismatches, then remaining CRITICAL and HIGH scanner-priority files, then remaining MEDIUM and LOW files. Validate one file per unit, running in waves of roughly 10 to 30 files. Reject rationalizations of mismatches: a dimension that does not balance is a finding. After each wave, persist exactly one status per file: `VALIDATED` or `BLOCKED` (with `step4_reason` and `step4_retry_count`), retrying each blocked file once.

Deduplicate the findings as you go. Confirmed step 3 mismatches keep their original IDs and severities, refuted step 3 mismatches are noted as false positives and excluded from final counts, and genuinely new findings receive new `DIM-XXX` IDs.

Then reconcile. Derive `coverage.unprocessed_files` from the terminal `BLOCKED` entries as `{ "path": "...", "blocked_step": "step2|step3|step4", "reason": "...", "retry_count": 1 }`. If the final report and `DIMENSIONAL_SCOPE.json` disagree, keep processing or reconcile the report until they match. Completion is decided by manifest coverage and final reported statuses, not by intent.

## What the run produces

A structured summary in the project root carrying mode, project_root, vocabulary (base_units, derived_units, precision_prefixes), annotations (total_added, by_file), findings (critical, high, medium, details), uncertainties_resolved, and coverage (in_scope_files, anchor/propagation/validation reviewed ratios, annotated functions and variables, unprocessed_files matching the terminal BLOCKED set), with confirmed and refuted mismatches separated and a list of modified files when edits occurred, ordered bound, discover, annotate, propagate, validate, reconcile.
