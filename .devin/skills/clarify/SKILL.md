---
name: clarify
description: 'Use when the user says "clarify", "what is ambiguous here", or when a prompt or spec reads as under-specified before planning. Not for exploring intent with questions: use askme.'
---

# Clarify

An under specified request answered confidently is still the wrong answer. This skill scans a prompt or spec for ambiguity before anyone plans against it, looks up everything the repo itself can settle, and brings back only the questions a human genuinely needs to answer. It reads everything and writes nothing: the deliverable is chat text, and no file, credential, deployment, or remote state changes.

## Pick the target

Scan one target, chosen by strict precedence: an explicit argument (`clarify <text-or-path>`) first, else the most recent user request when it reads as a spec or task, else the open conversation context. When one read of the context yields no identifiable target, stop and ask exactly one question naming what to scan. Scanning nothing is a failure, not an empty result.

## Restate it before you scan

Write the target back as a single paraphrased instruction, including what it does not ask for, and compare that restatement against the target. A mismatch is the first finding and outranks every other finding, because a correct answer to a misread request is still wrong. When the restatement matches, it stays silent unless a fork survives later; the report below is the deliverable, not the restatement.

## Look facts up before asking

Pre scan the facts before surfacing anything to the user. Resolve every ambiguity that is actually an environmental or codebase fact by direct lookup (search, read, or a subagent); never ask the user for something the repo can answer. Each resolved fact is recorded as tier `auto` with its basis, reported compactly, and never becomes a question. A lookup that fails or stays inconclusive is not an `auto` finding; it falls through to normal tiering below. Never guess a fact to avoid asking.

## Sort every finding by certainty

Give each remaining finding exactly one tier:

*   `auto`: an unambiguous project convention resolves it. Record the resolution and basis, then proceed.
*   `gated`: a reasonable default exists. Surface it as a recommendation that locks unless the user overrides it.
*   `manual`: evidence cannot settle genuine intent. Surface a non locking recommendation based on the least irreversible standard choice, then ask.
*   `fyi`: worth noting, never worth blocking on. List it and never ask about it.

Then enforce MECE over the set: merge or drop findings that ask the same thing as, or overlap, another finding, so nothing asks twice.

## Report, then ask only what you must

Emit a findings report grouped by tier with `manual` last. Each finding carries one block with these fields:

*   `id`
*   `quote` (the exact ambiguous span)
*   `tier`
*   `recommendation` (an em dash for `fyi`)
*   `basis` (the fact or convention supporting it)

`gated` recommendations are marked locked unless overridden; `manual` ones are non locking; `auto` resolutions appear compactly with their basis. On explicit request for structured output, follow the report with one fenced `clarify-findings/v1` block holding a YAML list of the per finding fields.

Then ask only the `manual` tier: one single select question per `manual` finding with its non locking recommendation marked, at most four questions per fire. At zero `manual` findings there is nothing to ask; the report alone is the result.

After the user's overrides, re scan the target once and stop when the re scan adds no new `manual` finding. Record every settled finding as overridden, answered, or discharged as a non issue with a one line reason; open `manual` findings left unanswered mean the work is incomplete, so state that and list their ids rather than claiming completion. A span that was unreadable or unreachable means emitting what was found, naming the excluded span, and not claiming the scan is done.

List any project specific term the user settled during clarification as a CONCEPTS.md candidate in the report. Record the candidate; write no files.
