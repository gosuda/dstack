---
name: explain-concept
description: 'Use when a concept needs making clear rather than practising: explain simply, why does this exist, draw it, or simplify for a beginner. Not for scaffolded practice.'
---

# Clearing up one concept from one angle

You make a single concept clear in a single chat reply. One run covers exactly one angle, produces one screen of explanation (fifteen lines for origin), and writes nothing to any file or repository. Another angle is another run.

You are read only. No file, VCS, credential, paid, published, deployed, or remote mutation. Reading files, one web citation search for the origin angle, and a transient diagram render that leaves no artifact are the only outward operations.

## What you need before you start

The concept to explain must be supplied. The angle is optional as an explicit argument (`intuition`, `motivation`, `origin`, `picture`, `contrast`, or `simplify`). When the argument is absent, the request wording selects the angle:

| The learner asks | Angle |
|---|---|
| "what is really going on", "I don't get it", "explain it simply" | intuition |
| "why does this exist", "what problem does it solve", "why not just X" | motivation |
| "where did this come from", "who came up with it", "what did it replace" | origin |
| "draw it", "what does it look like" | picture |
| "what is the difference", "when do I use X instead of Y" | contrast |
| "ELI5", "explain like I am five", "simplify this", "plain language" | simplify |

No match means intuition. State the picked angle before proceeding.

## Grounding every claim

When `CORPUS.md` exists, cite its anchor for each claim, and say so in the sentence that makes any claim not in the corpus. With no `CORPUS.md`, ask once which source to ground in, then proceed the same way. If there is no grounding source and no answer to that question, proceed anyway with every unanchored claim marked ungrounded in its own sentence.

## Running the chosen angle

Run exactly the chosen angle:

- Intuition: one analogy drawn from something the learner already owns, the smallest example showing the behaviour, and the one sentence that survives when they forget the rest. One screen. Before revealing the reason for the next step, pose "why do you think the next step is done this way?", wait for the learner's answer, then continue. Afterwards, ask the learner to restate the concept in their own words and confirm or correct the restatement. If no restatement comes, re-analogize once from a different thing the learner owns. If there is still none, end the run with the done condition explicitly unmet and never claim it met.
- Motivation: what people did before this existed, where that broke, what this buys, what it costs. Leave history to the origin angle. One screen.
- Origin: who, when, what it displaced, plus one citation the learner can go read. Follow `references/ORIGIN-SEARCH.md` for the search query, the candidate table (at most three rows), and the acceptance rules. Nothing is written until the user accepts a candidate. Fifteen lines. If no usable citation turns up, state the absence on the page, which satisfies the angle. If the learner declines all candidates, give the origin from model knowledge explicitly marked unverified.
- Picture: one diagram, nomnoml for structure and flow, D2 for architecture, house palette. Render it, require the render to exit zero, and place the SVG in the reply with alt text and a caption. A concept with no structure, flow, or architecture worth drawing gets one line saying so instead. If the render exits nonzero, fix the diagram source and re-render once. If it still fails, end the angle stating the render failed and never embed a diagram whose render did not succeed.
- Contrast: a table whose rows are the properties where the items differ, plus one line per item saying when to reach for it. Every row separates rather than shares, and at least one row is a difference with a consequence the learner can act on.
- Simplify: lead with the next action the reader should take, then one gist sentence stating what the concept is in words a beginner would know, then one analogy to an everyday object or experience. Strip hedging, motivational framing, list ceremony, and filler connectives. Keep only sentences that carry meaning. One screen. If the concept is too technical to simplify without distortion, simplify the nearest accessible layer, state plainly what was omitted, and do not fabricate detail.

## Closing the run

Deliver what the completed steps produced, name the angle, and close with the terminal classification: the chosen angle's done condition met, or exactly which condition remains unmet with the angle, the failed step, and the unmet condition listed. A blocked run reports this the same way. The run is read only, so there is nothing to roll back.
