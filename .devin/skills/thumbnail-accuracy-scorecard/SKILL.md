---
name: thumbnail-accuracy-scorecard
description: 'Use when thumbnail concepts need real-size, accuracy-first scoring without misleading claims. Not for generating thumbnails or declaring winners that fail the accuracy rubric.'
disable-model-invocation: true
---

# Thumbnail accuracy scorecard

You score thumbnail concepts at their real platform size with accuracy first, so no winner makes a claim the content cannot keep. You never generate thumbnails here, and you never declare a winner that fails the rubric.

## Freeze the bound and the rubric

Record the bound before anything else: platform (YouTube, Twitter/X, LinkedIn, and similar), audience, rubric definition, assets to score, and round cap. No scoring starts until the bound is frozen.

The rubric below is fixed and frozen with the bound. Each dimension scores 0 to 10 independently.

| Dimension | Weight | What a high score means |
|---|---|---|
| Claim accuracy | 0.30 | Text and imagery represent the content. No exaggerated claims, misleading titles, or false implications |
| Visual clarity | 0.25 | Subject is recognizable at the platform display size. Text legible at thumbnail dimensions, not just full resolution |
| Composition fidelity | 0.20 | Layout respects the platform safe zone constraints. No critical elements cropped or obscured by platform UI overlays |
| Color and contrast | 0.15 | Palette and contrast fit the platform and do not mislead about the content tone |
| Brand consistency | 0.10 | Thumbnail aligns with the creator or product brand identity |

The aggregate score is the weighted sum, and the threshold is 7.0. A thumbnail scoring below 5.0 on claim accuracy is disqualified regardless of aggregate, because misleading claims fail on their own. Ties break in this order: higher claim accuracy wins, then higher visual clarity wins, then both are declared runners up and no winner is selected.

You also need the exact platform pixel dimensions sourced from the platform published thumbnail specification (for example 1280x720 for YouTube). When the published specification cannot be found, stop. Never guess dimensions. Ask for asset approval before rendering, under human gating: approval granted lets you render the approved assets, while denial or silence blocks the run.

## Render, score, and rank

1. Render each asset at the real platform dimensions. Do not score at non standard sizes.
2. Score each render against the fixed rubric. Record every per dimension score, the aggregate, whether the aggregate clears the threshold, and whether claim accuracy disqualifies the entry.
3. Rank by aggregate, apply the tie breaking order, and select the winner (highest aggregate, threshold cleared, not disqualified) plus two runners up. When no entry qualifies, report that instead of forcing a winner.

Stopping states and what to report:

| Terminal | Meaning |
|---|---|
| success | One winner and two runners up clear the threshold |
| no_accurate_winner | No thumbnail clears the threshold, or every remaining entry is disqualified on claim accuracy. Report the best scores and the disqualification reasons |
| approval_blocked | Asset approval was denied or never collected. Report what approval is missing |
| budget_exhausted | The round cap or budget arrived before a winner was selected. Report the best scores obtained. An exhausted budget is never success unless it was the predeclared success predicate |

## Leave a receipt

When the outcome is durable, persist `receipt.json` under `.outline/loops/thumbnail-accuracy-scorecard/<run_id>/` with the terminal class, the bound, and the per thumbnail scorecard evidence: per dimension scores, aggregate, threshold, disqualification status, rank, and the winner and runners up or the non success terminal.
