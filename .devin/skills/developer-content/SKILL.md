---
name: developer-content
description: 'Use when preparing an evidence-backed developer content package with runnable examples and accuracy checks. Not for publishing, fabricating results, or unverified performance claims.'
disable-model-invocation: true
---

# Developer content

Prepare a developer content package (tutorial, guide, comparison, troubleshooting piece, or technical announcement) that a reader can run and an author can trust. Tutorials, guides, comparisons, troubleshooting, and announcements are modes of this one skill, not separate wrappers. Preparation only: nothing is published, and drafting a piece never implies it was executed.

## What you need before starting

- `audience` (required): who the piece serves and their starting point.
- `goal` (required): the one thing the reader can do afterward.
- `material` (required): supplied code, docs, or an explicitly requested read-only research pass.
- `mode` (optional): tutorial, guide, comparison, troubleshooting, or announcement. Defaults to guide when omitted.

Formatting and design tools may be referenced as optional aids; they are never required dependencies.

## Shaping the piece

Work through these in order:

1. Fix audience, goal, and mode, then state prerequisites including imports, versions, and setup, complete enough that a reader matching them can start.
2. Build the outline with progressive complexity: concept, minimal working example, real variation, errors, tradeoffs, next steps. Each section names what the reader can do after it.
3. Prepare runnable examples with exact inputs, expected output, error handling, and troubleshooting for the likeliest failures. Every example carries its inputs, its expected output, and at least one failure path.
4. Mark every code block verified (ran against the stated versions) or unverified (not run, with what would verify it stated beside it). No block goes unmarked, and an unverified block keeps its visible status rather than being quietly kept.
5. Attach sources for every factual claim. Fictional case studies are forbidden, and no multiplier or speedup claim stands without measurement behind it.
6. Submit the package to technical-accuracy review as a checklist the author runs: versions, imports, outputs, errors, links, each ending in pass or a flagged item.

## When the material falls short

- An example cannot be verified: mark it unverified, state what verification needs, and keep it only with that status visible beside it.
- Material too thin for the goal: narrow the goal or name the missing material.

## What you hand back

A content package ready for the author to use: audience and goal, prerequisites, outline, runnable examples with expected output and error paths, tradeoff notes, source list, next steps, verification marks on every code block, and the accuracy checklist result. No fabricated result, fictional case study, or unverified speedup claim remains.
