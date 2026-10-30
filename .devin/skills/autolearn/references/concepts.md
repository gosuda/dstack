# `CONCEPTS.md` vocabulary contract

Owner: `compound`. `autolearn` carries a generator-owned byte-identical copy of this file. The glossary at the operating repo root is shared; this contract is its single maintenance discipline.

`CONCEPTS.md` defines words with codebase-specific meanings. It is a shared reference that `docs/solutions/` and project instructions can cite without redefining those words. Terms enter through accretion or seeding. Create the file only when the first qualifying entry exists; never scaffold an empty file.

## How terms enter

- Accretion: a learning surfaces a term whose meaning was not obvious, so it gets defined. This catches peripheral terms, because friction surfaces them.
- Seeding: a run proactively defines the core domain nouns of the area it actually investigated: the declared domain model in scope (schema, core types, primary models, top-level domain docs), never a full-codebase trawl for nouns never touched. A scoped run seeds only its area; only an explicit repo-wide bootstrap seeds the whole project.

The count comes from the source and the bar below, never a fixed quantity.

## What earns a slot

A term qualifies only when all three hold, in order:

1. Its meaning here is precise and stable enough that a future engineer needs it defined to follow conversations, tickets, or code across sessions.
2. It is not already defined there under any synonym. A hit means refresh, never a second entry.
3. It is scope-qualified to this project, not general programming or domain English, and not incidental jargon from one session.

Nothing clears the gate: write nothing. A clean no-term result is correct. Incidental jargon that happened to appear once never earns a slot, however precisely phrased.

## Per entry

- One sentence: what the term means here and what distinguishes it from neighbors.
- A second paragraph only for non-obvious behavioral rules: lifecycle, ownership, cancellation, or transition semantics. Never to restate the definition.
- Retired synonyms go directly under the definition as `*Avoid:* OldName, otherword`. When the team uses several words for one concept, pick the best and retire the rest.
- No implementation specifics: file paths, class or function names, table names, library calls. No incidental jargon: one-session words without a precise stable project meaning.
- No status fields, dates, or owners on entries.
- No current-config values that will change: specific thresholds, counts, or enum values. State the behavior, not the number.
- No links to PRs, issues, channels, milestones, or version-specific claims.

Cross-references between entries within the file are fine. When an entry leans on another project-specific term, that sibling must also be defined here.

## Organization

Cluster concepts by domain relationship: entities with their states, processes with their stages. A flat list is fine while small; reshape as it grows. When relationships carry load (ownership, cardinality, cross-entry lifecycle), capture them in a short `## Relationships` section near the top. Skip that section when entries stand alone.

Tail section `## Flagged ambiguities` records settled distinctions in one line each: `*'account' had been used for both Customer and User; these are distinct.*`

## Reconciliation

1. Locate the file (`fd -g 'CONCEPTS.md' --max-depth 2` or equivalent). Absent plus a qualifying term: create it. Absent plus nothing: write nothing.
2. Search the term and its synonyms (`git grep -ni '<term>' CONCEPTS.md` or equivalent). A hit is the concept: refresh on drift, never duplicate.
3. Add a genuinely new term in the right cluster per the shape above.
4. Read the file back and confirm no duplicate or near-duplicate heading landed.

## Refresh

In refresh scope, re-derive each in-scope definition against current code and pick one outcome: Keep (still matches; prefer no-write), Refresh (meaning drifted; rewrite to current reality), Consolidate (two entries name one concept; merge into the better name, retire the other as an alias), Delete (the concept's domain is gone from the code; age alone is never a reason). No cosmetic churn: typo or prose-polish edits are not refreshes.
