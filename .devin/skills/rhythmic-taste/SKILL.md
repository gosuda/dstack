---
name: rhythmic-taste
description: 'Use when the user says "give this rhythm", "vary the structure", or "the sections all read the same". Not for judging an artifact''s overall taste: use taste.'
disable-model-invocation: true
---

# Rhythmic taste

You keep a reader moving by varying how a document's sections are built. Rhythm here means the pattern of length, density, pacing, and nesting across sections, and the deliberate breaks in that pattern that keep attention awake. Sections that all come out the same length, the same shape, the same cadence flatten a document no matter how good each section is on its own.

Use this when the user says give this rhythm, vary the structure, the sections all read the same, or asks for section or layer rhythm variation. Document mode is the default and needs no external inputs beyond the document itself; seeded constraint mode is optional and runs only when the user supplies a seed and asks for random variation.

This skill never judges an artifact's overall taste (for that use taste). It is read-only: no file, VCS, credential, paid, published, deployed, or remote change, only a rhythm constraint returned in chat. That constraint is a creative scaffold for shaping sections, never a factual authority on anything it names.

What you need before starting: the document or section list, which is required in document mode: the sections, layers, or structural units to vary, supplied directly or read from the artifact in scope. Seeded constraint mode needs two more things: a random seed the user discloses openly, any number, word, or phrase, plus the user's chosen random inputs, any titles, words, or items in any count from any random source the user picks.

## Read the current rhythm (document mode)

Receive the document or section list. Where sections were not supplied outright, derive them from the artifact's headings, layers, or structural breaks.

Measure each section as it stands: its relative length, its sentence or paragraph density, its pacing from tight to expansive, and its nesting depth.

Name the pattern those measurements add up to (steady pulse, monotone, crescendo, decrescendo, syncopated) and say where variation is missing, which sections collapse to the same shape.

## Set a new rhythm (document mode)

Pick a target pattern that serves the document's purpose, not the one closest to what is already there: alternating long-short, crescendo from short to long, decrescendo from long to short, syncopated with irregular gaps, or steady pulse.

Turn that pattern into per-section assignments: relative length or density for each section, pacing drawn from the chosen pattern, and nesting wherever the content calls for sub-sections. Shape the assignments so no two adjacent sections collapse to identical structure.

Present the result as a structured list of section assignments with pacing, density, and nesting instructions, preceded by the diagnosed current rhythm and the chosen target pattern.

## Vary it from a seed (seeded constraint mode)

This is seeded constraint mode, optional. Enter it only when the user supplies a seed and asks for random variation. Run the read above first, through measuring the document's own sections, then work the seed.

Convert the seed to a deterministic numeric value, a hash or ASCII sum. Use that value to permute the user's random inputs and to choose the primary rhythm pattern from the same set above.

Measure each random input in the permuted order: its syllable or word count, whether it carries a parenthetical or disambiguation suffix, and whether it names a person, place, concept, or event.

Map those measurements to section or layer instructions: assign each input to a section, set relative length or density from its count, and set pacing from the chosen pattern. Inputs with parenthetical suffixes create nested or parenthetical sub-sections; inputs naming persons or events take higher narrative density; inputs naming concepts or places take wider spacing.

Present the result as a structured list of section assignments with pacing, density, and nesting instructions, stating plainly that the constraint is a creative scaffold derived from random inputs, not a factual or authoritative source about those inputs.

## When the rhythm will not come

No document or sections supplied and none derivable from the artifact means stop and ask for the document or section list; never invent sections.

A derivation that yields no usable constraint (every section collapses to identical structure and no variation is possible) means say so, present the raw measurements, and ask for replacement sections or a different target pattern.

Seeded variation missing its seed or its random inputs means ask for whichever is missing; never substitute or generate defaults.

## What you hand back

An ordered list of section or layer assignments, each with its pacing direction, relative density, and nesting rule, preceded by the diagnosed current rhythm and the chosen target pattern. In seeded variation, preceded additionally by the disclosed seed and followed by a one-line disclaimer that the constraint is a creative tool derived from random inputs, not factual authority on those inputs. A complete constraint is the minimum deliverable; there are no partial results.
