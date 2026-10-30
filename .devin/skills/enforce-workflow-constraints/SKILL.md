---
name: enforce-workflow-constraints
description: 'Use when any bounded workflow starts or reaches an action, path, proposal, or merge boundary. Refuses rather than default-allow on an unreadable constraint set.'
---

# Enforce workflow constraints

A bounded workflow moves only inside its constraint set. Your job is to stand at each boundary, check the pending step against the constraints loaded first, and permit, narrow, or refuse it in chat. The one rule that governs everything: an unreadable constraint set produces refusal, never default-allow. You change no files, state, or remote targets here.

## Load the constraint set before anything moves

Before the first action, load the constraint set that bounds the workflow. You need it supplied or locatable, and you need it enforceable. If it is unreadable, missing, or too ambiguous to enforce, refuse the workflow, record the refusal reason in chat, and stop. Do not default-allow.

Two validations come before any evaluation. When the constraint set declares a fixed action set, accept only that set. On any other value, stop with the invalid value and the accepted set, and run no evaluation. When a gate configuration bounds the decision, validate its shape first: require the pinned version value, require typed deny and allow lists, and require a finite numeric limit where one is declared. On any schema failure, stop with the field and the violated constraint, and evaluate nothing. A failed validation is an error verdict, never a silent allow.

## Judge each boundary the same way

Re-evaluate the loaded constraints at every action, path, proposal, and merge boundary against whatever is pending there. Permit the step when it satisfies every constraint. Narrow it to a compliant form when a narrower step would satisfy them. Refuse it and record the refusal reason when no compliant form exists. No partial permit exists: an action is permitted only when every constraint is satisfied, otherwise it is refused or narrowed.

Where deny rules, size caps, and allow rules all apply, evaluate deny rules before size caps before allow rules, with the first hit deciding. Match a star segment against dot-names. Treat an empty path set as trivially satisfying allow rules.

Record every refusal with its reason in chat output. If the constraint set may have changed since the last load, reload it before re-evaluating. Never proceed on a stale or unread constraint set. If no narrowing satisfies the constraints, the terminal result is refusal with the reason recorded. The refused action itself does not proceed or complete, so its own done condition does not hold; this skill's done condition holds because the refusal was recorded.

What you hand back: for each evaluated boundary, a chat verdict (permit; narrow with the narrowed form stated; or refuse with the reason recorded), with the verdict sequence proving constraints were loaded before the first action, re-evaluated at every boundary, and that an unreadable constraint set produced refusal rather than default-allow.
