---
name: rhythmic-taste
description: 'Use when the user says "give this rhythm", "vary the structure", or "the sections all read the same". Not for judging an artifact''s overall taste: use taste.'
disable-model-invocation: true
---

# Rhythmic taste

Rhythm is the pattern of length, density, pacing, and nesting across a document's sections, plus the deliberate breaks that keep attention awake. Sections that all share one length, shape, and cadence flatten a document however good each one is alone. This skill diagnoses that pattern and returns a rhythm constraint: per-section instructions for varying it.

Use it when the user asks to give a document rhythm, vary its structure, or vary section or layer rhythm. It does not judge an artifact's overall taste; use `taste` for that.

The skill is read-only: no file, VCS, credential, paid, published, deployed, or remote change. The constraint is returned in chat and is a creative scaffold for shaping sections, never a factual authority on anything it names.

## Inputs

Document mode, the default, needs only the sections, layers, or structural units to vary, supplied directly or read from the artifact in scope.

Seeded mode is optional and runs only when the user supplies a seed and asks for random variation. It needs two more inputs:

- A seed the user discloses openly: any number, word, or phrase.
- The user's random inputs: titles, words, or items in any count, from any source the user picks.

## Document mode

1. Collect the sections. When they were not supplied, derive them from the artifact's headings, layers, or structural breaks.
2. Measure each section: relative length, sentence or paragraph density, pacing from tight to expansive, and nesting depth.
3. Name the current pattern (steady pulse, monotone, crescendo, decrescendo, or syncopated) and point out which sections collapse to the same shape.
4. Choose a target pattern that serves the document's purpose, not the one nearest the current state: alternating long-short, crescendo from short to long, decrescendo from long to short, syncopated with irregular gaps, or steady pulse.
5. Assign each section a relative length or density, a pacing drawn from the target pattern, and nesting wherever the content calls for sub-sections. No two adjacent sections may end up with identical structure.

## Seeded mode

Run document mode through step 2 first, so the document's own sections are measured. Then:

1. Convert the seed to a deterministic number, such as a hash or ASCII sum.
2. Use that number to permute the random inputs and to choose the primary pattern from the same set as document mode.
3. Measure each input in permuted order: its syllable or word count, whether it carries a parenthetical or disambiguation suffix, and whether it names a person, place, concept, or event.
4. Map each input to a section. Its count sets relative length or density, and the chosen pattern sets pacing. A parenthetical suffix creates a nested or parenthetical sub-section. A person or event takes higher narrative density; a concept or place takes wider spacing.

## Failure handling

- No sections supplied or derivable: stop and ask for the document or section list. Never invent sections.
- No usable constraint, because every section collapses to identical structure and no variation is possible: say so, show the raw measurements, and ask for replacement sections or a different target pattern.
- Seeded mode is missing the seed or the random inputs: ask for whichever is missing. Never substitute or generate defaults.

## Output

An ordered list of section or layer assignments, each with its pacing direction, relative density, and nesting rule, preceded by the diagnosed current rhythm and the chosen target pattern.

In seeded mode, the disclosed seed also comes first, and a one-line disclaimer follows the list: the constraint is a creative tool derived from random inputs, not factual authority on those inputs.

A complete constraint is the minimum deliverable; there are no partial results.
