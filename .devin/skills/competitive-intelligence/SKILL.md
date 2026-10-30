---
name: competitive-intelligence
description: 'Use when mapping the competitive landscape and battlecards for a developer product from authoritative sources. Not for per-feature changelog research or unsourced market predictions.'
---

# Competitive intelligence

You map the competitive landscape for a developer product and turn it into battlecards a team can argue from. Every fact links to an authoritative source with an observation date, wins and losses are stated with their conditions, and unknowns stay visible instead of being papered over with predictions.

Per feature or changelog depth is out of scope here. This skill owns the broader landscape and battlecard context.

## What the map is built from

- `product`: the product being positioned.
- `scope`: which alternative classes to cover and which competitors are in scope.
- `sources` (optional): user selected authoritative sources. Without them, use public docs, pricing pages, and reputable coverage.

## How the map gets built

1. Fix scope first. List the in scope competitors across direct, indirect, DIY, and platform classes, plus explicit exclusions.
2. Build the landscape matrix over the features that matter, pricing model, positioning, content strength, and community signals. Every cell traces to one source link with an observation date, or is marked unknown.
3. Write one battlecard per alternative: when the alternative wins, when this product wins, the decisive conditions, and the proof behind each.
4. Record unknowns and freshness triggers (what would change the map, and what to recheck).
5. Purge unsourced trajectory claims such as market size futures or share predictions. A prediction stays only when the user supplies an authoritative source for it, cited verbatim.

## When the evidence runs out

- A material cell has no authoritative source: mark it unknown and name the source that would fill it. Never fill it from model knowledge.
- Scope is too wide to map well: map the top tier fully and list the remainder as deferred scope.

## What you deliver

A dated landscape matrix with per cell sources and dates, battlecards with win and lose conditions, an explicit unknown list, and recheck triggers. Everything stays in chat. This skill is read only: public and supplied sources only, with no credentials, outreach, or remote changes.
