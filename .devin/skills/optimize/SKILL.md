---
name: optimize
description: 'Use when one named path or performance symptom needs a single measured fix. Not for read-only hot-path hypotheses: use fastopt. Not for a full measured-floor campaign: use optimize-extremely.'
---

# Optimize

This skill fixes one named path or one performance symptom with a single measured change: latency, allocations, bundle weight, query cost, or a frontend performance metric. A supplied benchmark does not turn the job into a campaign. Everything stays local and reversible: the named target, necessary in-scope correctness coverage, one explicitly bounded local measurement instrument, and one authorized regression guard. Nothing remote, no credentials, no deployment, no paid services, no inferred infrastructure changes, and no automatic optimization commit. The work is done when the named bottleneck is measurably improved past noise, required behavior and repository checks pass, a regression guard holds the metric, and every kept or reverted attempt has a ledger entry.

Discover facts from the tree before asking the user for missing information. You need a resolvable target and symptom or metric, representative measurement conditions, and discoverable repository-native verification. If the request is really a full campaign, name `optimize-extremely` as the owner instead of widening this workflow.

## Settle the target and the yardstick

1. Resolve the target, the measurement method, and the exact write surface before editing. Record existing user changes on the target so this run never discards them. Move on once the target, the method, and the write surface are stated and user changes are preserved.
2. Establish a measured baseline: the metric, its units, the tool, the input, the conditions, the result, and the available noise evidence. A symptom is not proof of its cause. Move on once all seven baseline facts are recorded, or stop as blocked.
3. Name the specific bottleneck from relevant evidence: a query plan, CPU trace, heap profile, bundle analysis, or frontend measurement. Move on once the bottleneck is named with the evidence that selects it.

When instrumentation cannot separate a stage's useful work from dispatch overhead, first estimate whether removing that stage entirely could meet the target. If mutation is authorized, disable only that stage in an isolated, temporary experiment under the same workload and measurement protocol. Label the result an attribution bound, never a correct implementation or a shippable speedup, and restore the experiment without overwriting unrelated changes. Before rebuilding a reverted design, measure the dominant operation across input sizes and distinguish write-only staging that can be deleted from state coupled to live behavior. For synchronous regex prescreens, measure adversarial inputs at the supported size limit and check both complexity and match semantics after a rewrite. A timeout on the same blocked execution thread is not an interruption mechanism. Oversized input must follow the documented safety posture. Never truncate away a risky suffix.

## Make one change and measure it twice

4. Apply one complete targeted change. A cache, an index, a pagination strategy, or a memoization layer are examples only: each needs its own evidence and preserved semantics. Move on once the one change is fully coded.
5. Re-measure with the same metric, method, workload, and conditions. One change at a time. Move on once the after-measurement under identical conditions is recorded.
6. Keep only an improvement distinguishable from measured noise, with required behavior and repository checks passing. Revert neutral results, regressions, and wins obtained by dropping required work. Correctness gates the metric. Move on once the change is kept past noise and green, or reverted with its reason.

## Hold the gain and write the ledger

7. Hold the metric with a guard inside authority. Use an existing effective guard, or add an authorized synthetic CI performance budget or field-monitor definition for the primary metric. Never deploy a monitor or add CI outside authority. Move on once a guard holds the metric, or report the missing guard as the completion blocker without declaring success.
8. Write a ledger entry for each kept or reverted attempt: hypothesis, baseline, result, metric, tool, noise assessment, correctness result, and verdict. Move on once every attempt has its entry.

## What this pass never does

This owner does not use five candidates, floor arithmetic, a 5 percent hotspot threshold, a universal 1.05x win rule, cold-list grading, or atomic campaign commits. Those belong to the campaign. Broader read-only hot and cold analysis is `fastopt-extreme`, hypothesis-only hot-path design is `fastopt`, and a full measured-floor campaign is `optimize-extremely`. Naming a peer never executes its procedure.

## If it stalls

- Baseline unavailable: measurement tools or the codebase cannot produce the metric. The result is blocked. Never proceed without baseline evidence.
- No bottleneck found: profiling shows no measurable code-level cause. Report the uncertainty and whether environmental or statistical noise is suspected.
- Fix inside noise: the gain sits within the baseline noise band. Revert. Neutral is a revert.
- Correctness regression: tests fail or behavior changes. Revert immediately.
- Beyond authority: the fix needs unavailable credentials, remote mutation, deployment, paid services, or infrastructure changes. Document the requirement and stop without widening authority.

Reverted code leaves no trace. Kept ledger entries remain so discarded ideas are not re-profiled.

## What you hand back

The code change with before and after measurements under identical conditions, plus one ledger entry per attempt stating hypothesis, baseline value, result value, metric name, tool, noise assessment, correctness result, and verdict. On failure, return the exact blocked or reverted state, the measurements obtained, and the precise blocker.
