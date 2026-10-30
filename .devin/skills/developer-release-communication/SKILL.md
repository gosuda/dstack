---
name: developer-release-communication
description: 'Use when writing factual release notes or upgrade notices from a release diff or changelog. Not for promotional copy, commits, releases, or publishing.'
---

# Developer release communication

Write the factual record of a release from material the user supplies (a diff, a changelog, or an explicit change list with source links). You draft in chat only: no commits, no releases, no publishing, no sending, and no invented performance results. The notes you produce are the source of truth the user can hand to `release-promotion` for channel-shaped copy; promotion must stay consistent with them, not the other way around.

## What you need before you start

- `changes` (required): the release diff, changelog entry, or supplied change list with source links.
- `audience` (optional): operators, integrators, or end developers affected. When omitted, write for integrators.

If the user asks for notes but supplies no source, stop and ask for one. Never reconstruct changes from memory.

## From diff to notes

1. Extract every change from the supplied material only, keeping each item traceable to a supplied line or link.
2. Sort the items into Added, Changed, Deprecated, Removed, Fixed, Security. Leave out empty sections, and put nothing in the wrong one.
3. Fill in the fields that make each sensitive item actionable (next section), then check the whole set for invention before handing it over.

## Breaking changes, deprecations, removals, security fixes

A breaking change is not finished until it states who breaks and how, plus the migration action with commands or config where applicable. Deprecations carry their timeline and replacement, removals their last-supported version, security fixes their severity and upgrade urgency. Where a required field is genuinely unknown, say so explicitly rather than leaving a silent gap.

## Staying honest

Every claim traces to the diff or a supplied source with a link; every gap is marked as a gap. No performance result, adoption claim, or cause appears unless the supplied material shows it. When the diff is genuinely ambiguous, present both readings with the question for the author instead of picking one silently.

## What you hand over

Factual release notes using the six sections, breaking-change impacts with migration actions, a source link per claim, and a short verification note stating what was checked and what remains unknown.
