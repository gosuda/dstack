---
name: possible-worlds
description: 'Use when a design dispute has at least two live interpretations and the caller wants worlds made explicit or a plain-language recommendation. Not for selecting a design or source/remote changes.'
---

# Possible worlds

This skill lays out a design dispute as a set of live possible worlds and ends with one suggestion for what to examine next. It leaves the design unselected and the dispute open. Nothing is decided, recorded, or authorized here.

It is read-only. It reads no file, repository, card, or external state, and it modifies nothing (no file, version control, credential, payment, publication, deployment, remote, or downstream state, on success paths or failure paths).

## When it applies

The caller supplies a design dispute with at least two live interpretations, plus whatever premises, axes of disagreement, or distinguishing evidence is available. If the subject is not a design dispute, if fewer than two interpretations are still live, or if the dispute statement is ambiguous or missing, the skill stops before emitting anything. It reports that the dispute does not meet the two-interpretation threshold, or asks the caller to state the dispute. It never invents interpretations to reach the threshold.

## How it builds the worlds

It pulls out the shared premises and the axes where the interpretations vary, treating unsupported claims as premises rather than inventing evidence. Then it constructs one possible world per live interpretation, keeping shared premises fixed and naming the premise delta that reaches each world. Every world must be internally consistent. If the worlds cannot be built without invented premises, it returns `blocked: dispute cannot support internally consistent alternative worlds without invented premises`, and starts over only after the caller supplies a corrected dispute or the missing premises. When the caller wants a quick recommendation without the full worlds analysis, the paragraph may be produced directly from the dispute without requiring world construction.

## How it writes the paragraph

The whole output is one prose paragraph, atomic and complete. Partial paragraphs are never emitted. The paragraph follows these constraints:

- It presents the worlds neutrally, not as failure-only scenarios, and claims no exhaustiveness.
- It is written at a five-year-old abstraction level, using familiar objects, simple actions, and direct cause and effect, with plain words and no jargon or framework names.
- It ends with exactly one non-binding recommendation about which disputed premise or piece of evidence to examine next. The recommendation leaves the design unselected and the dispute open. If no single recommendation follows from the dispute, the skill stops and reports that no one recommendation follows instead of forcing a selection.

The paragraph is returned only after confirming it holds at least two live worlds, one final recommendation, no decision record, and no authorization to change anything.
