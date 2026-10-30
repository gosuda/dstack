---
name: interrogate
description: 'Use when asked to "interrogate" or run an adversarial multi-model review of a supplied code artifact. Not for tasks that require source or remote-system changes.'
disable-model-invocation: true
---

# Adversarial review across models

One model reviewing its own kind of output goes easy on it. This skill fans the same code, the same question, and the same rubric out to at least two distinct models, then forces their agreements and disagreements into one verdict. Everything here is read-only: no file, VCS, credential, paid, published, deployed, or remote mutation, and the review output returns in chat only.

## What you need before starting

- Code artifact (required): the code or document under review, supplied in the conversation as text or a readable file path.
- Review scope (required): the specific aspect, component, file, or question the review targets.
- Rubric (required): the shared evaluation criteria every reviewing model uses. It must define concrete criteria.
- Reviewing model pool (optional): the models to invoke adversarially. You need at least two distinct ones.
- Lead judgment model (optional): the model that synthesizes the final position when models disagree. Defaults to the first reviewing model.

If the artifact is missing or unreadable, stop and report `blocked: artifact missing or unreadable`. If the rubric is absent or defines no criteria, stop and report `blocked: rubric missing or invalid`. If fewer than two distinct models are available, stop and report `blocked: insufficient model pool`. These three block the run. Nothing partial substitutes for them.

## Fan the reviews out

1. Send one review request to each selected model at the same time, with the identical artifact, scope, and rubric.
2. Keep the models isolated. Do not show one model's output to another before every review is in.
3. Collect what returns. When a model fails to answer, proceed with the reviews you have and record the missing model in the failure log. Never report full success while a review is missing. Disclose the gap.

## Turn reviews into a verdict

Build an agreement map first. For every rubric criterion, record which models agreed, which dissented, and the substance of each position. Every criterion gets a per-model entry.

Then ask the lead judgment model, and only that model, for a synthesis that does all four of these things:

- Acknowledges the full agreement map.
- States a clear final verdict for each rubric criterion.
- Marks where consensus was reached and where it was not.
- Recommends one action per criterion: act, consider, note, or dismiss.

If the lead synthesis fails, do not block. Skip it and return the individual reviews with the agreement map. Synthesis failure alone never counts as non-convergence.

## What you hand back

One chat report holding the verdict (act, consider, note, or dismiss per criterion), the agreement map with per-model positions, the lead synthesis when one was produced, a failure log naming any model that did not return and what it was assigned, and a final actionable next step drawn from the aggregate verdict.
