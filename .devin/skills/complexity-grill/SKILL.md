---
name: complexity-grill
description: 'Use when a user wants to identify the true sources of complexity qualitatively before counting metrics. Not for source or remote mutation.'
---

# Complexity grill

Name what makes a region of code hard to live with before anyone reaches for a number. The output is a ranked qualitative report of where the complexity lives and what effort each source forces. Metrics may confirm the ranking afterward; they never set it.

## Stay read-only

Read the named code region or design surface and nothing else. No file, VCS, credential, paid, published, deployed, or remote mutation. If you catch yourself reaching for an edit, stop and report the read-only breach; no partial mutation is retained.

## Name what hurts before counting anything

Enumerate candidate complexity sources qualitatively. For each, state where it lives and what effort it forces: coupling that blocks independent change, hidden state that must be tracked by hand, leaky abstractions, special-case proliferation, accidental concurrency, premature generality, or indirection that exceeds the complexity it hides. You are done when every candidate source is named with its location and forced effort.

The user may weight the pass toward a named concern (coupling, hidden state, leaky abstraction, special-case proliferation, accidental concurrency, premature generality, indirection exceeding what it hides). No metric input is accepted before the qualitative ranking is settled.

## Rank by pain, roots above symptoms

Rank candidates by the real cognitive or maintenance effort they force, not by any numeric metric. Break ties by root cause: a source that produces other sources ranks above a symptom it creates. You are done when candidates are ranked by effort with root-cause tie-breaking.

Only after the ranking is settled, optionally attach a metric to confirm a ranked source. Metrics confirm; they never discover, reorder, or lead the ranking. If no metric is available, the ranking stands on its qualitative evidence alone.

## When it goes wrong

- Metrics-first: if a numeric metric is introduced before the ranking is settled, discard it, return to the ranking, and re-rank qualitatively.
- Symptom-as-root: if a ranked source is itself produced by a deeper source, demote it, promote the deeper source, and re-rank.
- Unbounded scope: if the region cannot be read in one pass, narrow to a named sub-region and state the narrowing. Never widen scope to force a result.
- Boundary breach: if any edit or mutation is attempted, stop and report the read-only breach. No partial mutation is retained.

## What you hand back

A ranked complexity-source report: ordered root causes, each naming its location, the effort it forces, and whether a deeper source produces it. Any metric appears only as a confirmation footnote after the ranking.
