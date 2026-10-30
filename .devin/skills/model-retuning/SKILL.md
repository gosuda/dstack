---
name: model-retuning
description: 'Use when asked to run /model-retuning to retune a skill corpus for a new model, measurement-first. Static audits are out of scope here.'
disable-model-invocation: true
---

# Model retuning

Measurement decides what changes. Given a target model or symptom, this job retunes a skill corpus through small surgical passes until a pre-registered bar clears: a fixed number of consecutive clean runs, written down before anything changes. Each pass fixes one problem class across disjoint file ownership and lands as its own commit, so any pass reverts independently with `git revert`. Only named local corpus files and measurement artifacts are touched; nothing remote mutates. When the bar will not clear, the run reports the exact claim it could not support instead of presenting activity as success.

Invoke as `/model-retuning [target model or symptom] [corpus path] [bar:<n> consecutive clean runs]`. The target model or symptom is required: it names what the corpus degrades on. The corpus path is optional and defaults to `./skills`. The bar is required and registered in writing before any change exists; a bar chosen after seeing results is not a bar. A benchmark harness able to run two builds of the corpus side by side is required. Refuse the run without it, and never present a static audit as retuning.

## Confirming the measurement foundation

Three things must exist before any work starts. A run archive (or a harness that produces one) carries per-run tool-call traces, terminal markers, token counts, and final messages. A build selector points a run at a specific corpus checkout so two builds stay comparable under one runner. A repeatable task exercises the corpus end to end. Name whichever is missing and stop.

## Mining the archive before spending a run

Files already on disk cost no model calls, so read them first. From the corpus's own workflow order, derive a phase-marker map with one observable marker per phase: a tool call or a file that exists, never a phrase in prose. Build the extractor only after the map exists. Extract one row per run by script, never by hand, with at least run id, model, settings, session and child ids, ordered phase trace, terminal marker present, output tokens, wall clock, helper dispatch count, max parallel dispatch, and the verbatim final message.

Score `task_done` (the deliverable exists) and `process_followed` (every required phase appears in required order) independently. One never implies the other, and the marker stands in for neither. Outcomes score first-match-wins in this order:

- `blocked`
- `running`
- `timeout/halt`
- `task-done-shortcut` (`task_done` true, `process_followed` false)
- `done` (both true)
- `unclear`

Each row scores exactly once; unscored rows wait until they classify.

## Setting the noise floor

Run the harness with two identical copies of the corpus at the same commit on both sides. Whatever difference appears is the floor every later claim must clear. Contended runs prove nothing about latency: run arms serially within an arm and interleaved across arms with nothing else running, since contention destroys wall-clock-derived metrics and can manufacture a timeout that reads as a halt. A contended run supports no latency claim and counts as no halt.

## Auditing from two independent sides

One agent per skill directory proposes cuts; a second per skill defends the existing prose. Budget the defense as first-class work, since the removals are the phase's product as much as the proposals. Both passes need independent contexts. Where the host offers no way to run them as separate agents, report that as a blocker and stop the audit rather than arguing both sides in one context.

## Cutting in surgical passes

Fix one problem class per pass, never bundled. Fan out by disjoint file ownership, never by item: one agent owns one skill directory and applies the class everywhere inside it. Ownership forms a checkable filesystem partition with every path in exactly one manifest row. Before dispatch, find byte-identical duplicated assets, assign every copy to exactly one owner who propagates the edit to all copies in the same pass, and list those copies as forbidden for everyone else. For rewrites whose strings cross-reference each other, author the canonical mapping (old string to new string, exact) serially first, then fan out verbatim application. An uncovered occurrence signals a contract gap for serial resolution, not a variant to improvise. Reconcile every cross-reference before the pass closes.

## Letting the failure choose the next fix

Progress has a shape: a failure reaching a later phase names the next target, a failure at the same site means the fix missed, and a run completing the task while skipping the workflow is a different defect from a halt, visible only because the two metrics stayed separate. Probes cannot fail in phases they skip, so audit the phases the instrument never reaches; a green streak certifies only what it exercised. Loop cutting and measuring until the registered bar clears, then stop. Report the paths still unmeasured and what measuring them would take. One clean run proves nothing.

Every fan-out follows the same discipline: pass large context by path plus a short gist, never inlined contents; decide each artifact's path before the phase that writes it and keep artifacts together; give aggregation targets a schema; budget the serial tail and name serial segments separately when reporting elapsed time; state what the fan-out skipped (units queued past the cap, units skipped, files outside every owner's set).

Ship each pass as its own commit with a message saying what changed and why. Keep the measurement artifacts. Write the finding where the next person will hit it: the mechanism, before and after, the measured numbers, and the hypotheses that died, since dead ends stop the next attempt from re-running them.

Recovery follows the fault. A missing measurement foundation stops the run with the missing piece named; no static audit substitutes. Collapsed audit contexts stop the audit as a reported blocker. A shared-asset parity break (a per-unit agent edited its own copy of a byte-identical file) recovers by assigning all copies to one owner and propagating in one pass; note that a parity failure surfacing in a later pass will misattribute until ownership is fixed. An over-cut (a removed mandate handed a required decision to the model) recovers by naming the new decider and restoring the gate where the decider may not decide. Non-convergence leaves partial results standing as a ranked hypothesis list with measured numbers, never as a passing suite.

## What you hand back

A retuned corpus whose measured behavior on the target model clears the pre-registered bar, each removal attributable to a named problem class with a per-pass commit. With it, a written finding covering mechanism, before and after, measured numbers, and dead hypotheses. Where the bar did not clear, a report naming the specific unsupported claim and the unmeasured paths.
