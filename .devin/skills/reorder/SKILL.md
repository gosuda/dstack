---
name: reorder
description: 'Use when asked to reorder a drifted listing under one stated principle, moving items only and rewording nothing. Not for deliberately ranked listings.'
---

# Putting a jumbled list back in order

A catalog, index, table of contents, enum, or menu can drift until its order is arbitrary. This skill puts one such listing back under a single stated principle: related items sit together, clusters follow the principle, and every word stays exactly as it was. It moves only and rewords nothing.

## Scope

Use it when the user asks to reorder a listing, or when a listing's order has clearly gone arbitrary.

Leave deliberately ranked listings alone: this skill does not preserve explicit ranks, so it does not touch them. Rewording, adding, or removing content is refused, as is any remote, credential, publish, deploy, or irreversible change. The only write is the named local artifact, and version control is the rollback path.

## Inputs

- The listing, supplied or identified from context.
- One ordering principle.

## Choosing the principle

Name the principle before moving anything. The user's own words win. Next comes whatever the existing sequence was reaching for. Failing both, use a default such as workflow sequence, dependency order, grouping by kind, severity, frequency, or alphabetical order.

## Reordering in place

1. Pin the listing: identify the ordered set in focus and count its items so the full scope is fixed before anything moves.
2. Confirm every item belongs in that scope, and note any mirrored copies that must carry the same order.
3. Group related items so they sit together, then order the clusters by the principle, keeping each cluster's internal order as it was.
4. Move items without rephrasing labels, descriptions, or metadata. Never blend two incompatible sorts to force a tidy look.
5. Apply the identical order to every mirrored copy.

A pass that finds nothing to improve changes nothing.

## Done when

A reader can name the ordering principle, every item is still present, related items are adjacent, and mirrored copies carry the identical order. Leaving the original unchanged because nothing needed reordering also counts as done.

## Stop conditions

- The listing boundary or item set is unclear: ask the user to identify or supply the exact target.
- The items are of mixed types with no shared principle: ask which subset to reorder or which principle to apply.
- The principle is unknown: state the best guess and wait for explicit confirmation before moving anything.
- The principle fits some items but not all: order the compatible subset and report the rest as out of scope.
- A move corrupts or loses content: restore from version control. The working tree is the only mutation surface.
