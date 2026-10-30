---
name: cross-lens-converge
description: 'Use when one reviewer is not enough because failure modes are heterogeneous, or a claim needs cross-lens pressure before it ships. Not for collapsing a decision field.'
disable-model-invocation: true
---

# Cross lens converge

One reviewer is not enough when the failure modes are heterogeneous, or when a claim looks strong mostly because its author wrote it. This skill puts the claim under several independent lenses and returns a picture of where they agreed, where they disagreed, and the single question that would settle the most. A reader should be able to act on it without re-running the analysis.

Read-only throughout: no file, VCS, credential, paid, published, deployed, or remote mutation. On any error, return the partial picture rather than touching anything.

## Building the lenses

Take the claim or artifact under pressure as given. Candidate failure modes may arrive with it (supplied modes are trusted input, use them as they are) or you derive them from the artifact. Then:

- Collapse duplicates: candidates describing the same failure mode become one lens. Never run two lenses over the same failure mode and present their agreement as independent confirmation. Each genuinely distinct failure mode gets exactly one lens.
- Give every lens exactly one load-bearing reason it would reject or weaken the claim. A lens with no such reason is dropped before running, never talked into agreement.

## Reading the picture

Run every lens independently against the artifact and record, per lens, a verdict of agrees, disagrees, or cannot-decide plus the single reason driving it. A lens that cannot decide stays cannot-decide with its reason. Never coerce it into a side. A lens that does not complete is named in the picture with its verdict marked cannot-decide. Above all, do not average, merge, or majority-count the verdicts: disagreement is the product, so preserve which lenses agreed and which did not.

## The one resolving question

From the disagreed and cannot-decide lenses, name the single question whose answer would resolve the most disagreements. If none resolves more than one, name the one behind the highest-stakes disagreement. If nothing disagrees but some lenses cannot decide, name the question that would let the undecided ones reach a verdict. If every lens agrees, the resolving question is none. Never manufacture disagreement to look thorough.

## What you hand back

A convergence picture: each lens's verdict with its one load-bearing reason, the agreed set, the disagreed set, and the single resolving question. No state transition.
