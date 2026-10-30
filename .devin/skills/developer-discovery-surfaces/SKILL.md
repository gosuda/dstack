---
name: developer-discovery-surfaces
description: 'Use when auditing GitHub presence or preparing curated directory submission packets for a developer tool. Not for star manipulation, automated PRs, or directory spam.'
---

# Developer discovery surfaces

You audit a developer tool's public surfaces and prepare submission packets a human can file. Use this when someone names a repository, tool, or package and asks whether it is ready to be discovered, covering GitHub presence, directory fit, or both.

This is preparation only. You read the live repository, write the audit and one packet per directory in chat, and stop. The human submits. You never submit a listing, open a directory PR, game stars or follows, or touch analytics credentials. Treat GitHub and curated directories as separate surfaces with their own rules.

## Start from the live repository

You need the repository or package under review (`repo`), in its actual current state, not how it is described but how it reads from its current files. When the caller suggests candidate directories (`directories`), use them. Otherwise propose candidates from public awesome-lists and registries that fit the artifact.

Read what is really there before recommending anything:

- README completeness
- A quickstart that runs
- Topics and description
- License clarity
- The contributing path
- Visible signs of issue and PR responsiveness

Every audit item cites the state you observed. Where the facts are unavailable, say so and mark the item unknown rather than filling it in.

## Fix up GitHub first

Recommend description, topics, README structure, and pinned material, plus profile placement where it is relevant. Each recommendation names the gap it closes, so the reader can trace every suggestion back to something you saw missing or weak.

## Check each directory's current rules

Directories drift. For every candidate, look up its current contribution rules (fit, uniqueness requirements, description constraints, maintenance expectations) and note the cited URL and date. A candidate without a rules check gets an explicit unknown, never an assumed pass. If a venue's rules forbid this listing type, drop the candidate and say why. Do not reframe the listing to evade the rules.

## Write one packet per directory, each in its own words

Every packet carries unique descriptions, never the same blurb pasted across venues, with the correct category placement and required metadata for that venue. A packet is finished when it meets its venue rules and reads differently from the others.

## Leave a recheck ledger

Close with a maintenance note: who rechecks what, and on which trigger (a release, a rule change, or a quarterly pass). Every packet needs its recheck trigger, so nothing goes stale silently.

What you hand back: the discovery audit with cited observations, GitHub recommendations traced to gaps, one submission packet per directory with unique descriptions and rules citations, and the maintenance ledger.
