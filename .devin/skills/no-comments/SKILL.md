---
name: no-comments
description: 'Use when asked to remove source comments by replacing them with clear code or accessible documentation. Not for deleting legal notices, required tool directives, or public documentation contracts without an equivalent home.'
---

# No comments

Remove the dependence on comments, then remove the comments. Preserve the knowledge and behavior that still matter. Nothing should remain that the code or its documentation does not already carry. A comment describing a hidden decision moves into the module, its contract, its test, or its design record.

## When this applies

Use this when asked to clear source comments by replacing them with clear code or reachable documentation. It never covers deleting legal notices, required tool directives, or public documentation contracts without an equivalent home for them.

## What you may touch

You need the target files, directory, or code surface named before you start.

An implementation request authorizes reversible local changes to the target code and to the callers, tests, and documentation needed to preserve its contracts. An audit-only or plan-only request authorizes findings and proposed edits, never source changes.

Honor explicit user exclusions. Leave generated or managed sources unedited and point at their authoring source instead. Do not publish, change credentials, delete user data, or cross a public compatibility boundary without explicit authorization for that action and its consequence.

## Covering the targets

Read the repository instructions and the relevant code, including surrounding control flow and consumers. Learn the languages, documentation conventions, and documentation consumers from the repository itself. Record unreadable files, generated sources, and uncertain spans as coverage gaps by name. Never treat them as silent exclusions. Coverage is complete when every target is accounted for or gapped by name.

## Counting every comment

Inventory comments with a language-aware method that keeps comment tokens and source spans intact. A bare syntax tree may silently drop comments, so lexical analysis carries this step. Tell comments apart from strings, regular expressions, raw literals, template contents, and embedded languages by their lexical state. A text search may surface candidates but it never decides what gets deleted. Record each comment with its location, the code it attaches to, and its purpose, including documentation comments and commented-out code. Treat docstrings and other runtime-visible documentation by their real language semantics (including introspection surfaces such as `__doc__`), not as disposable comment tokens. Where no reliable tool exists for a language, read its lexical forms by hand. Where classification stays uncertain, leave the span untouched and report the exact gap. Never run a naive strip. The inventory is complete when every real comment in reachable scope is recorded and every uncertain span is gapped.

## Keeping what the law and the tools require

Preserve license, copyright, attribution, and other required legal notices. Preserve directives consumed by compilers, interpreters, build tools, formatters, linters, coverage tools, documentation generators, and code generators, including placement-sensitive annotations and delimiters. Identify the consumer before judging any directive obsolete. An ordinary explanation of a business rule is not automatically a legal notice. Carry the rule itself into the implementation, its invariants, its tests, or its documentation. Never weaken or disable a lint, and never drop a proof or check, to reach a line-count or percentage goal. This step is complete when every legal and mechanical comment is identified with its consumer and excluded from removal.

## Moving meaning before deleting words

Read what each remaining comment compensates for, then take the smallest action that fully preserves it:

- A comment that carries zero information beyond its attached code (an empty comment, repeated punctuation or whitespace ornament, narration that restates the code token for token with no reason, constraint, history, or contract, genuinely dead commented-out code holding no design knowledge worth keeping) is deleted with no destination. Record it as no-information with its one-line justification.
- Every other removable comment needs a destination before its source text goes: make intent visible through precise names, direct control flow, existing domain types, or a named constant, extracting a function only when it gives a real operation a useful boundary. Express a required invariant in the code where that preserves the contract, or add or update a focused test where the constraint is behavioral, without adding runtime assertions, allocations, or abstractions just to replace prose. Move irreducible design rationale, specification references, and incident knowledge into the repository's existing design-record or technical-documentation home, keeping the decision, its reason, and its link to the affected code. Resolve an actionable TODO inside the authorized scope; otherwise keep its useful obligation in the existing issue or task record before removing the marker, and never open a remote issue without approval. Never silently erase unfinished work.
- A misleading comment gets corrected only by establishing the actual behavior and the intended contract first. Never change working behavior to match an unsupported comment.
- A comment's category, length, or obscurity is never by itself a reason to keep it.

This step is complete when every removable comment is either deleted under the no-information exception with its justification, or relocated to its destination and then removed.

## Treating public documentation as a contract

Before relocating API documentation, identify the documentation generator, the packaged output, the symbol association, the examples, the links, and any runtime documentation consumers. Relocate the content only when those consumers can still discover and use equivalent documentation. Update navigation, cross-references, generation inputs, and affected examples together. Keep a mechanically required attachment comment when the established documentation system needs it. Where equivalent discoverability or compatibility cannot be kept, retain the affected documentation and name the exact constraint. Never turn comment removal into an unapproved documentation-system migration. This step is complete when relocated documentation is discoverable through its established consumers, or the blocking constraint is named and the comment retained.

## Clearing what remains
Delete every remaining removable comment in scope. Keep only explicit user exclusions, legal or mechanical necessities, comments whose useful contract cannot yet be preserved safely, and the narrow evidence floor: a minimum SAFETY comment where an actual unsafe block would otherwise fail undocumented_unsafe_blocks, a necessary public rustdoc or module invariant with no equivalent type or contract home yet, and a load-bearing clause identifier, evidence row, or measured fact its consumer still needs. Give each retained exception a specific reason tied to a consumer, an invariant, a compatibility mechanism, or an approval. Vague helpfulness and bare design-decision claims are not sufficient. No blanket permission for documentation comments, and no invented lint requirements. No-information deletions from the previous step stand as completed removals with their justifications. They do not retroactively need destinations. This step is complete when every target comment is removed, relocated with its content preserved, removed under the no-information exception with justification, or retained with a specific reason.

## Checking the result honestly

Re-inventory the final source with the same language-aware method. Recheck affected behavior, directive consumers, and documentation discovery wherever they changed. Use the repository's existing checks rather than inventing a parallel verification system. A lower comment count alone proves nothing about correctness. Where verification is prohibited or unavailable, state the unproved claims and the precise restriction instead of calling them verified. The work is complete when the final inventory, the behavior evidence, and the documentation evidence all support the reported result.

## When something goes wrong

- A target is unreadable or its syntax uncertain: finish the reachable files independently, preserve the uncertain spans, and report the uncovered scope. Do not claim complete removal.
- A directive's consumer is unknown: investigate its configuration and use before deleting the directive. Keep it where its necessity cannot be established safely.
- Useful knowledge has no safe replacement: retain the comment and name the missing invariant, documentation home, compatibility mechanism, or approval.
- An edit or verification fails: repair the source. Where recovery means undoing one of your own edits, preserve unrelated and intervening user changes. Never restore an entire stale file over them.
- The work would require changing a public contract: request approval for the exact change before crossing that boundary.
- Verification is prohibited or unavailable: state the unproved claims and the precise restriction. Do not label them verified.

## What to hand back

The implemented change, or the requested read-only proposal, with the target coverage and any uncovered files or spans, the structural changes and where useful knowledge went, the no-information deletions with their one-line justifications, the retained comments with their legal, mechanical, contractual, or explicit-exclusion reasons, and the evidence obtained with any remaining blocker. Completion means every target comment is accounted for, every removable comment is removed or relocated, useful contracts are preserved, and the evidence supports the reported result. No persistent ledger and no per-comment approval round is required for authorized local implementation. Audit-only scope, explicit exclusions, and compatibility boundaries keep their approval gates.
