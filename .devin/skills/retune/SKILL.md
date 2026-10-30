---
name: retune
description: 'Use when a skill corpus degrades on a new model and needs measurement-first retuning against a registered bar. Not for word-reduction passes, single-skill edits, or static audits presented as retuning. Explicit request only; never auto-invoked.'
---

# Retune a corpus for a new model

Behavior is the contract here. Prose edits with no measured effect are not repairs, and word reduction is not a goal. Leanness is a separate program; report completion, not word counts. This skill runs only on an explicit user request to retune, never unprompted and never as headless self improvement.

You may measure freely and edit the named corpus, but nothing else. Never weaken a test to get a green suite, never invent harness output and present it as behavior proof, and never publish, mutate remote state, spend money, touch credentials, or destroy data.

## Fix the target, corpus, and bar before touching anything

Settle three facts in writing before any edit exists. First, the target model and the symptom: what got worse, on which model. Second, the corpus path: the checkout you are allowed to edit, which defaults to `./skills` only when the invocation names no other corpus. Third, the acceptance bar: consecutive clean runs or an equivalent bar with its count. A bar chosen after results is not a bar. A green test suite alone is never the bar; the bar is measured behavior on the target model.

## Prove the harness can measure before claiming anything

Require all three of these, then stop and name the missing piece when any one is absent. There is no fallback audit.

| Requirement | What counts |
|---|---|
| Run archive or harness | Produces per run tool call traces, terminal markers, and final messages |
| Build selector | Lets one runner compare two corpus checkouts |
| Repeatable task | The corpus executes end to end through it |

Never present a static audit as retuning. Mine history before spending runs, then establish the noise floor by running the harness against two identical corpus copies at the same commit. The observed difference is the floor every later claim must clear.

## Argue both sides in separate heads

Audit adversarially with independent contexts: one worker per skill proposes cuts while a separate worker defends the existing prose. When no independent worker facility exists, report that as a blocker and stop the audit rather than arguing both sides in one context.

Cut in surgical passes, one problem per change, fanning out by disjoint file ownership and never by item. Never edit a test to make a suite green: a removed string a test pins is a finding to report, not a test to weaken. Sort every stop by who is on the other side before touching it. Workflows that exist to stop and ask are the product, not the defect.

## Let the failure choose the next fix

Measure after each pass and let the failure choose the next fix until the registered bar clears, then stop. Report what stayed unmeasured: a cleared bar never implies coverage it does not have. If the bar does not clear, report the failing sites and the next fix they select rather than claiming success. If an explicit limit is reached, stop incomplete with the evidence and remaining scope; limit exhaustion is not convergence.

Ship the corpus change with each commit stating what it preserves and what it removes, so every removal stays attributable. Keep the bar, the floor, and the measurement evidence with the result.

## What you hand back

Return the target model, the harness found, the floor and the bar, the passes with attributable removals, the measurement evidence per pass, the unmeasured scope, and the cleared or blocked verdict. Never report prose reduction as behavior proof.
