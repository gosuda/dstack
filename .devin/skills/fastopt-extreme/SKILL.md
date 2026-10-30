---
name: fastopt-extreme
description: 'Use when estimating hot paths and proposing complexity-neutral cold simplifications while refusing complexity theater. Not for hypothesis-only hot paths: use fastopt. Not for measured-floor campaigns: use optimize-extremely.'
---

# Fastopt extreme

The user wants two things at once for one named code region: estimated hot paths, and cold path simplifications that add no complexity. Your job is to produce hot path hypotheses with benchmark designs, plus cold path simplification proposals, while refusing anything that buys speculative speed with new machinery. This skill is read-only: no file, VCS, credential, paid, published, deployed, or remote change. Everything leaves as chat output. Hypothesis-only hot path design belongs to `fastopt`, and a full measured campaign belongs to `optimize-extremely`; naming a peer never runs it. Broader means more analytical categories inside the named region, never a repository-wide sweep.

## Bound the region first

Work only in the named code region or module the user supplies. Do not widen to unrelated code or drift into a repository-wide survey. If no code is supplied, request the target region before proceeding; never guess or analyze from memory.

## Estimate hot paths, and call them hypotheses

Estimate from call frequency, loop depth, allocation density, and I/O or syscall blocking. State the basis for each estimate, and label every one a hypothesis, never a measured fact.

## Design the benchmark that could kill each hypothesis

Every hot path hypothesis gets a benchmark design stating the metric, the baseline measurement if available, and the falsification condition under which the hypothesis is rejected. A baseline you do not have is explicitly unmeasured, never invented.

## Propose only complexity-neutral cold simplifications

A cold path candidate qualifies only if the change adds no new abstraction, wrapper, configuration flag, caching layer, or indirection: the result must be no more complex than the original. For example, removing a redundant intermediate collection qualifies when removal preserves behavior, reduces allocations, and adds no branch, wrapper, cache, flag, or indirection. Each accepted candidate states its specific simplification and why it adds no complexity. Every accepted item is a proposal only, with no edit and no measured-savings claim. If a path cannot be classified as hot or cold from available evidence, label it unclassified and exclude it from proposals.

## Refuse complexity theater

Reject any proposed optimization that introduces a new abstraction, wrapper, flag, caching layer, or indirection whose complexity cost exceeds the gain it claims. For example, adding a cache, configuration flag, wrapper, or extra indirection to buy speculative microseconds on a cold path. Each refusal states the complexity cost and the claimed gain. A refused proposal is recorded as refused, never emitted as a valid optimization.

## What you hand back

A chat report with hot path hypotheses (each a labeled hypothesis with a benchmark design giving metric, baseline status, and falsification condition), complexity-neutral cold path simplification proposals (each with its simplification and complexity justification), explicit refusals of complexity theater (each with cost and claimed gain stated), and unclassified paths marked as excluded. Partial results are emitted with every unclassified or refused item marked explicitly, so the report never pretends to be complete when it is not.
