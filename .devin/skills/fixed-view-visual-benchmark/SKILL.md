---
name: fixed-view-visual-benchmark
description: 'Use when a visual needs repeatable fixed-view rendering and independent rubric scoring. Not for free-form visual review or subjective critique.'
disable-model-invocation: true
---

# Fixed-view visual benchmark

This skill renders one frozen view repeatedly and scores each render against a frozen rubric. It never offers free-form review or subjective critique. The human asks for it by name, and only the human fires it, which is why model invocation stays disabled.

Rendering needs explicit human consent, and everything else stays local and reversible: only the named local artifacts are written, rollback is undo, and nothing mutates a remote. The run ends in one named terminal class: success (the saved render clears the frozen rubric threshold), stalled (repeated renders stop improving), blocked (the rig cannot render through the specified interface), or capped (the budget runs out before the threshold clears). Budget exhaustion counts as success only when the predeclared success predicate says so. A sub-threshold render is never presented as clearing the rubric.

## Freeze the rig, the rubric, and the budget

Bind all three before any mutation and freeze them there:

| Element | What freezing means |
|---|---|
| Fixed view rig | Camera position and orientation, scene definition, and render settings (resolution, samples, lighting, post-processing) are named. Every parameter affecting the output is fixed. |
| Rubric and threshold | Scoring dimensions (for example composition, lighting accuracy, material fidelity, geometric correctness) carry weights summing to 1.0 with a 0 to 10 scale per dimension, plus the minimum weighted-sum aggregate that defines a pass. |
| Render budget | The maximum render attempts or time allowed, declared before work begins. |

## Render with consent, score independently

Ask for and record explicit human consent before rendering. Then render the fixed view through a specified rendering interface with reproducibility controls. The interface must accept the frozen rig parameters and produce a reproducible output under the frozen rig and the declared seed or averaging strategy: same camera, same scene, same settings, same strategy, same comparable result. Record the interface name, version, and the exact parameter set used. When the interface is non-deterministic (stochastic sampling, temporal effects), declare the seed or averaging strategy that makes repeated renders comparable before scoring. Renders without a declared strategy are not comparable, so never compare them.

Score each render against the rubric criteria, never against the previous render. Record per-dimension scores, the weighted-sum aggregate, and the threshold. Stop at success (the aggregate clears the threshold), at any non-success terminal, or at the bound, and name the terminal class reached.

Persist the run record under `.outline/loops/fixed-view-visual-benchmark/<run_id>/`, emitting `receipt.json` before return with the saved render path, per-dimension scores, aggregate, threshold, and terminal class. Hand back the terminal classification with the saved render, its per-dimension scores, the aggregate, the threshold, and the run receipt. When the run yields only a partial result, emit the best render and score obtained.
