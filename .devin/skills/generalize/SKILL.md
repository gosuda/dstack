---
name: generalize
description: 'Use when asked to derive the general rule a request carries as examples instead of a stated rule, then bound it. Not for ambiguity in a stated request: use askme. Read-only.'
---

# Generalize from cases

Sometimes the ask arrives as examples instead of a rule ("do it like this one", "fix these three the same way", a pasted log with "you figure it out"). Your job is to state the rule those examples carry, draw its boundary, and hand the contract back for someone else to apply. You never apply the rule here, and you change nothing: no file, version control, credential, paid, published, deployed, or remote mutation.

Reach for askme instead when the request itself is ambiguous but no examples are on the table. The split is simple: examples present means generalize, bare ambiguity means askme.

## Gather the case set first

List every positive (instances pointed at approvingly or asked to be repeated) and every negative (anything named "not that", including an earlier attempt the user rejected). A rejected attempt is the most informative case in the set because it kills hypotheses no positive can. State the set size in your output so the reader knows how much evidence stands behind the rule.

Two variants change the shape of this step:

- With no negatives the hypothesis space is wide, so the probe step below carries the whole result.
- A data drop (a pasted log, dump, folder, or link with no stated ask) is a case set where every item counts as positive. Read the shape of what was handed over as the case set, and your deliverable becomes a stated inferred intent handed back as a proposal to confirm.

## Split features, then write rival rules

Break each case into features, meaning observable attributes (subject, location, shape, trigger, wording, scale). Attributes, never impressions: "returns early on nil" is a feature, "is clean" is not.

Then mark each attribute as candidate invariant (present in every positive, absent from every negative) or incidental (varies across positives). With a single positive this step decides nothing, so every attribute stays candidate invariant and the probe does the work.

Now write 2 to 4 rival rules, ordered from narrow to broad, one sentence each with a weight from 0 to 1. Every candidate must reproduce all positives and exclude all negatives. A candidate that misses a supplied case is dead: drop it and name the case that killed it. If the filter leaves exactly one candidate, the induction is settled and you go straight to bounding.

A rule built from one hypothesis without rivals is a guess wearing a method, so this step is mandatory unless the filter already reduced the field to one.

## Probe with a real item

Find something in the user's own material (another file, row, sibling call site, neighboring paragraph) that the surviving candidates classify differently. That item is the discriminator.

Resolve it from evidence first using search, read, language server output, or a scout subagent. If the material shows the probe already follows one candidate's rule, that candidate wins and the question dies. Ask the human only when evidence cannot settle it, as one single-select question showing what each reading would do to the probe item, with a recommended default. Never ask a probe the material already answers.

## Bound the rule and hand it off

A rule is not stated until its edge is. Name what it covers, what it deliberately excludes, and the nearest excluded neighbor (the closest thing a reader might expect to be swept in that will not be). "Everything similar" is not a boundary.

Your output is the generalization contract: the case set with each case marked positive or negative, the surviving rule, the invariant attributes it rests on, the incidental attributes discarded, the boundary with its nearest excluded neighbor, and the probe with its basis and how it resolved. For a data drop, add the inferred intent as a proposal to confirm. On a structured output request, render the same contract as a fenced `generalization/v1` YAML block. Then stop. Acting on the rule belongs downstream.

If the probe cannot be resolved from evidence and the human does not answer, emit the surviving candidates with the probe marked open and unresolved. Never swallow an open probe or pretend the rule is settled. On any failure, leave all source material unchanged and return whatever partial contract you have.
