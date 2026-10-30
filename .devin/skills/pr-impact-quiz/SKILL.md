---
name: pr-impact-quiz
description: 'Use when the user invokes this skill to generate targeted questions proving the author understands the change''s codebase effect. Not for reviewing the change: use review.'
disable-model-invocation: true
---

# Quizzing what a change really touches

This skill does not review the change (that belongs to review). It tests whether the author understands what the change does to the existing codebase, by writing three questions only the person who traced the blast radius could answer well. Everything here is read-only: no file, VCS, credential, paid, published, deployed, or remote mutation, and the questions return in chat only.

## What you work from

All material is author-supplied. You never call out to any forge, because provider ambiguity never justifies a remote read.

- PR or MR description (required): the authored description of the change, including motivation, scope, and expected behavior.
- Diff or change summary (required): the diff itself or a structured summary of what changed.
- Codebase context (required): language, primary modules, and key patterns in the affected area.
- MR context (GitLab only, optional): source and target branch names plus draft state. When present, one question must probe target-branch compatibility. For fork MRs, bind source and target projects separately.

When the description or diff is absent or empty, state what is required and generate nothing. When the diff contains no changed lines, state that no changes are present and generate nothing. No partial output counts: when the completion bar below is not met, no questions go out.

## How the three questions earn their place

Read the description and the diff, then map what the change touches: the primary modules, interfaces, and data flows, and the possible effects on callers, downstream consumers, and shared state. From that map write exactly three impact questions with these properties:

- Each question targets a specific area of this codebase, not a generic concern.
- Each question demands a concrete answer. Anything answerable with yes, no, or "I checked" fails the bar and is rewritten or dropped.
- The three questions probe different impact axes: call-site behavior, data invariants, backward compatibility (or the target-branch compatibility probe when GitLab MR context is present).

When the draft questions are generic, redundant, or yes-or-no answerable, stop. Do not present them. The run is non-converged and the done bar below does not hold.

## What you hand back

Three concrete, non-generic impact questions in chat, each aimed at a distinct area of effect on this codebase. Nothing else is the deliverable: no review verdict, no fix list, no remote write.
