---
name: first-load-byte-reduction
description: 'Use when a first screen needs lower transfer bytes without visual or behavioral change. Not for visual redesign or behavioral changes.'
disable-model-invocation: true
---

# Shrinking first-load bytes without changing a pixel

The job is narrow on purpose: a named first screen must transfer fewer compressed bytes while looking and behaving exactly as before. Anything that alters the visuals or the behavior belongs elsewhere (a visual redesign or a behavior change is a different engagement, never a side effect of this one). The work is local and reversible through version control, confined to the named screens and their asset pipeline, and you ask before adding or upgrading any dependency.

You need three things named and frozen before any mutation: the exact pages or routes to reduce, the browser, device, or network condition that defines the measurement context, and the target compressed byte count or percentage reduction. Work stops at success (fewer bytes with pixel identity and passing tests), at any non-success terminal below, or when the declared budget runs out.

## Baseline first

For each named screen, measure the compressed transfer bytes in the target environment from a network waterfall or a build-output size report, and record the per-resource breakdown: HTML, CSS, JavaScript, images, fonts, other. At the same time, capture what identity means here: a full-page screenshot at the target viewport plus the rendered DOM structure. No baseline, no optimization: without both halves recorded, later claims about savings or sameness are ungrounded.

## Reduce inside the bound

Apply only optimizations that preserve visual and behavioral identity: compress and resize images to their display dimensions, subset fonts to the used glyphs, tree-shake unused JavaScript, split bundles by route, inline critical CSS, defer non-critical resources, compress text assets with Brotli or gzip. Ask before adding or upgrading a dependency. You are past this stage when the reduced screen transfers fewer compressed bytes than the baseline.

## Prove sameness, then classify the run

Render the reduced screen at the same viewport as the baseline and compare the full-page screenshots pixel by pixel. Static content must show zero pixel difference; animated or lazy-loaded content must reach the same final rendered state. Run the test suite to confirm no behavioral regression. Only pixel identity plus passing tests counts as success: never present a screen that lost identity or failed tests as done. Emit the best reduction obtained even when the run does not succeed.

Every run ends in exactly one terminal class, named honestly:

- Success: fewer bytes with pixel identity and passing tests.
- Stalled: no byte reduction preserves pixel identity. Report what was attempted and why identity broke.
- Blocked: the environment or pipeline cannot be exercised. Report the blocking condition.
- Capped: the declared budget ran out before the byte target was met. Report the best reduction achieved. Budget exhaustion is never success unless it was the predeclared success predicate.

## The receipt

When the run is durable, persist the record to `.outline/loops/first-load-byte-reduction/<run_id>/` including `receipt.json`, and return the receipt content in every run. The receipt carries the terminal classification (`success`, `capped`, `stalled`, or `blocked`), the before and after compressed byte counts with per-resource breakdown, the pixel-identity confirmation, and the test result. (`receipt.json` on disk exists only when the run is persisted; the content is returned regardless.)
