---
name: frontend-fidelity-rebuild
description: 'Use when an authorized reference surface needs a clean-room frontend reconstruction across static, motion, and responsive fidelity. Not for styling or component work without a reference surface.'
---

# Frontend fidelity rebuild

You rebuild an approved reference surface from scratch (no peeking at its source) and prove the copy matches the original in layout, motion, and responsive behavior. Every number that decides pass or fail is frozen before you build, and every claim ends with comparison evidence.

## Get permission first

This work starts with one harness ask or question call confirming the reconstruction is authorized. State the reference surface and the authorized scope in that call. Prose consent, invocation consent, a prior run's consent, and anything discovered after the run starts do not count as approval. If approval never arrives, stop before touching anything and write a blocked receipt naming the missing approval. You write only to named local reconstruction artifacts, never to a remote, and version control is your rollback. If the scope drifts after approval, end the run.

## Freeze what counts as done

Before any reconstruction, name and freeze four things: the viewport set (for example 375px mobile, 768px tablet, 1440px desktop), the timeline set (the animation or interaction sequences you will measure, such as page load, hover transitions, scroll effects), the per-gate tolerances (static: pixel-difference percentage or visual-regression threshold; motion: timing deviation in milliseconds and property delta; responsive: layout shift at each breakpoint), and the round cap (the maximum rebuild-and-measure cycles before the run ends at its bound). Nothing gets built until all four are fixed.

## Capture the reference, then rebuild without its source

For each declared viewport, capture a full-page screenshot and the rendered DOM. For each declared timeline, capture a video or frame sequence of the animation or interaction. Record the capture tool, browser, and version alongside. If any declared viewport or timeline cannot be captured, the run is blocked: report which capture failed and why.

Build the reconstruction from those captures, never from the reference source code. Match the static layout, the motion timing, and the responsive behavior until the rebuild renders at every viewport and plays every timeline.

## Measure all three gates and stop honestly

Compare each viewport's reconstruction screenshot against its reference screenshot with a visual regression tool and record the pixel-difference percentage. Compare each timeline's motion against the reference and record timing deviation and property delta. Compare each viewport transition and record layout shift, marking whether each gate passes its frozen tolerance.

Stop when all three gates pass, when a terminal failure is reached, or when the round cap is hit. If repeated attempts stop improving the scores, the run is stalled: report the plateau and the attempts. If the cap arrives first, the run is capped: report the best per-gate results. Reaching the cap is never success unless the predeclared success predicate said so.

## Leave a receipt

When the outcome is durable, write `receipt.json` under `.outline/loops/frontend-fidelity-rebuild/<run_id>/`. It is immutable and carries the terminal class (success, capped, stalled, or blocked) plus the full per-gate evidence: static pixel difference, motion timing deviation, responsive layout shift, the tolerances each was judged against, and whether each gate passed.
