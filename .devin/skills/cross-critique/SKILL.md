---
name: cross-critique
description: 'Use when independent proposals on a contested decision need cross-critique before choosing, reusing the original authors. Not for parallel multi-stance investigation: use council.'
---

# Cross critique

Use this when a contested decision already has two or more independent proposals on the table and their authors need to pressure-test each other before anyone chooses. Round one produced the proposals in isolation; round two reuses the same authors so each proposal gets attacked by people who did the homework.

The round stays conversational and read-only: no repo, file, or remote mutation. If the proposals already strongly agree, or the question has an objective answer verifiable directly, stop and say so. A second round would then spend latency and tokens to resolve no real disagreement.

## What must already exist

- At least two proposals from an independent first round: the authors did not see each other's work. Without that independence the diversity round two needs is already lost, so require a fresh independent round instead of proceeding.
- The contested decision question and its decision criteria.
- Access to the same subagents that wrote round one, so each keeps its investigation context. If one is unavailable, seed a replacement with that proposal's context and flag the reduced fidelity in the synthesis.

## Circulating the proposals

Boil each proposal down to its core recommendation and reasoning (not full transcripts) and label them neutrally (Proposal A, B, C), anonymizing authorship where practical so confidence of tone does not turn into bandwagon bias. Send each author only the other proposals, never their own.

## Collecting the critiques

Ask each author to assess every alternative on four points: what it gets right and where it beats the author's own approach; its risks, edge cases, hidden costs, and wrong assumptions; whether it changes the author's recommendation and why; and a final ranking with confidence. Insist on both pros and cons, because a critique that credits a rival's strengths is worth more than a reflexive defense. If a critique comes back thin or unsupported, follow up with that same author; if a second attempt still yields nothing substantive, mark that contribution non-convergent and proceed with the rest, noting the gap.

## Synthesizing by survival

Weigh evidence quality, not vote count. Lead with the recommendation, then show where authors converged after seeing each other's work (round-two convergence is a strong signal), the most incisive objection raised against each option, why the recommended option best survives critique against the decision criteria, and what disagreement, confidence limits, and material unknowns remain. Never present the round as converged while objections stand unresolved.

## What you hand back

A conversational synthesis with the recommendation; where authors converged or changed their minds after seeing alternatives; the strongest objection raised and whether it is decisive; why the recommended option survives critique against the decision criteria; and remaining risks, unknowns, and confidence. No repo mutation.
