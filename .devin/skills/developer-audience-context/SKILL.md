---
name: developer-audience-context
description: 'Use when grounding developer marketing in a confirmed audience profile of persona, pains, alternatives, and trust signals. Not for inventing quotes, benchmarks, or audience facts.'
---

# Developer audience context

Ground developer marketing in what you can observe about the audience: who they are, where they gather, what hurts, what else they use, and the words they use. The result is an evidence profile delivered in chat. It stores nothing and invents nothing.

## When this applies, and what it never does

This applies when the user asks to define, update, or apply a developer audience profile for marketing work. The work is read-only: chat output only, with optional reads of public sources. No file writes, no canonical store, no credentials, no outreach, no publication.

There is no canonical audience store, and this skill never creates one. Every other marketing skill accepts supplied sources directly and must never require anything produced here.

Voice discipline matters: this skill records only observed audience evidence (how the audience speaks). How the brand should speak is prescribed by the `copywriting` voice work, not here. `TONE.md` or `VOICE.md` may be read as completed input, but never written.

## What you need before starting

- `product` (required): what is offered, in the user's own words or supplied docs.
- `evidence` (required): supplied docs, READMEs, issues, docs pages, or an explicitly requested read-only research pass. Mentions of tooling such as search consoles, rank trackers, or listeners are optional evidence inputs, never required dependencies.

## Building the ten-dimension profile

Work through these in order; each dimension is finished only when filled from evidence or explicitly marked unknown:

1. Collect all ten: product, persona, places, problems, alternatives, differentiators, verbatim language, trust signals, conversion actions, voice observations.
2. Give every item provenance: source and observation date. Verbatim language must be exact quotes with sources; never put a paraphrase inside quotation marks.
3. Check each trust signal against something real: docs quality, examples that run, error coverage, maintenance signs, license clarity. Each one cites the artifact observed.
4. State conversion actions as observed or plausible paths, each naming its evidence or flagged as an assumption. Never present them as guaranteed funnels.
5. Keep voice observations descriptive of the audience. No brand-voice prescription may appear.

## Thin evidence and tempting fictions

- Evidence too thin for a dimension: deliver the profile with the unknown explicit, and name the smallest evidence that would fill each gap.
- Fictional example material supplied as a format reference: borrow its shape only. Never copy its testimonials, numbers, or names as facts.
- Numeric claims you cannot verify (audience sizes, conversion benchmarks): mark them `UNVERIFIED` or omit them. Never let them stand as defaults.

## What you hand back

An audience profile in chat covering all ten dimensions, with per-item provenance, explicit unknowns, and exact verbatim quotes with sources. It is one optional input among supplied sources for other work; no other skill requires it. No file is created and the working tree stays untouched.
