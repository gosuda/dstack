---
name: research
description: 'Use when researching a named library, framework, SDK, API, or service, or finding a migration guide. Not for codebase-internal research. Dispatch a scout agent.'
---

# Research command

Answer a question about a named external library, framework, SDK, API, CLI, or service with a cited artifact written to disk. Codebase-internal questions do not belong here; hand those to a scout subagent. This job never mutates anything remote and never takes a paid action. Its product is one Markdown file, and returning without writing it fails the run.

To start you need the subject, pulled as a canonical name from the request, plus an optional pinned version such as `pydantic@2.7`. Without a stated version, record "latest stable" and resolve it from official docs. The artifact lands under a preferred target path when given, otherwise under `docs/research/` when that directory exists and `.outline/research/` when it does not, filed under a slug of the subject name.

## Send one worker that owns the artifact

Dispatch a background subagent through `task` with self-contained instructions covering subject, version, source-ladder requirements, and target path. That worker owns completion: it climbs the ladder, cites its claims, and writes the file. You record the outcome as artifact-on-disk or as `BLOCKED` with a named failure class. A partially successful run still returns the artifact path with its specific gaps listed.

## Climb the source ladder in order

Inside the worker, resolve the canonical name from official docs, then probe these tiers in priority order, moving on only when a tier fails hard (source unavailable, no results, non-authoritative), and recording every skipped tier:

| Tier | Priority | Source type |
|------|----------|-------------|
| 1 | Highest | Official docs: library and framework documentation sites, SDK reference pages |
| 2 | High | API refs: reference pages, repository README and docs folders, source code |
| 3 | Medium | Books and papers: RFCs, academic papers, vendor whitepapers, standards documents |
| 4 | Low | Tutorials: tutorial articles, blog posts, vendor how-to guides |
| 5 | Lowest | Community: repository issues and discussions, forums, Q and A threads |

The ladder is done when every tier is probed, or (in primary-source-only mode) when the first authoritative match is found and recorded, or when a hard failure stops it.

## Cite every claim honestly

Every factual claim carries at least one source URL or doc path. Anything drawn solely from training data carries the label `[Speculative — training data only]`. For each load-bearing claim, test both stances against external sources (the surprising case that it holds, the settled case that it fails) and record both results; where no authoritative source is reachable, label the claim unverified and assert nothing from intuition.

## When only primary sources count

Some tasks need primary-source reading. Then the ladder shrinks to Tier 1 official docs plus Tier 2 API refs, README and docs folders, and source code, stopping after the first authoritative match without probing lower tiers. Every claim links to its owning primary source URL or file path, with one citation owning each claim. A claim no primary source can support is written with `[Unverified — no primary source available]` and left unfilled; never close the gap with a community, tutorial, or other non-authoritative source. An unreachable primary source gets one retry, not a drop to a lower tier. If the target write fails, delete any partial file before reporting.

## When the ladder fails

Name what happened and stop rather than pretending the artifact is complete:

- `ladder-exhausted`: nothing authoritative through Tier 5, so surface every attempted tier plus partial findings.
- `invalid-output`: the artifact is missing required fields, unparsable, or not at the target path.
- `task-dispatch-failed`: the subagent never started or returned nothing.
- No writable outcome at all: return `BLOCKED: <failure class>` with the specific reason.

The finished file holds the subject id, the claims each with citations and confidence labels (Verified for Tiers 1 and 2, Probable for Tiers 3 and 4, Unverified for Tier 5, Speculative for training data only), and the open questions with attempted tiers, in that order.
