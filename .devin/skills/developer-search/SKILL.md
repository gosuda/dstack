---
name: developer-search
description: 'Use when mapping technical search opportunities by exact query, intent, and source evidence. Not for inventing search volume, rankings, or time-to-result promises.'
---

# Developer search

Map which technical queries are worth targeting and what page each one needs. This is read only. Work from public search evidence and any console or rank data the user supplies, which stays optional throughout. Rank trackers and consoles are evidence sources only, never the work itself. This skill does not deploy SEO, build pages, run vendor-automated campaigns, or promise ranks.

## What you need before you start

- `queries` (required): candidate exact queries, or a topic the user authorizes for query discovery from public sources.
- `evidence` (optional): Search Console exports, rank-tracker data, or docs analytics the user supplies. When absent, proceed on public evidence and mark rows accordingly.

## Reading each query

1. Record each exact query verbatim and give it one intent class: error-message, how-to, implementation, comparison, or reference. Intents stay distinct because each needs a different page type.
2. Attach source evidence to each query: observed discussions, docs gaps, competing answers, or supplied console data with dates. A query with no evidence stays on the map as a candidate with its gap named, or is dropped at the user's choice.
3. Recommend one page type per query (error reference, tutorial, comparison brief, API reference section) and name the competing answer it must beat fairly.

## Freshness and success signals

Give every row a freshness trigger (release cadence, API change, new error text) and a measurable success signal (indexed page, docs click-through on a real path, resolved-question rate). A row without both is unfinished.

## Numbers you may not invent

Volumes, rankings, traffic forecasts, and timelines appear only with an authoritative source and date. Anything else is marked `UNVERIFIED` or left out. Read the finished map once for unsourced numbers before handing it over.

## What you hand over

A search opportunity map in chat: exact queries, intent classes, evidence, page types, named competing answers, freshness triggers, success signals, and a verification note covering every number. Nothing else changes.
