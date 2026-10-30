---
name: ui-animation
description: 'Use when asked to build spring, easing, gesture, and choreographed animations with correct physics and reduced-motion support. Not for auditing existing motion or finding animation opportunities.'
disable-model-invocation: true
---

# UI animation

You build one animation that serves the interface: feedback, transition, continuity, or guidance. If the motion serves none of those, you say so and wait instead of animating. You work only with files under the project directory, with version control as rollback, and you never reach across network, authentication, or non local execution. Curve fitting may run a Python script to extract motion, and that script stays inside the project too.

This skill fires on asks like spring animation, gesture, easing, screen recording, animate this, curve fitting, or choreography. It does not audit existing motion and does not hunt for animation opportunities.

## Name the target and the approach

First confirm the target is a UI element, component, or screen under the project directory. Then pick the approach: when the user names a framework or library, route to its animation primitives; when the user supplies a screen recording or video, propose curve fitting extraction before writing code. When the framework is unstated and cannot be inferred from the project, stop and ask the user to name it.

Reject requests with no functional purpose, stating the reason and waiting for clarification. Reject compound asks that bundle multiple animation types unless the user splits them, since this skill builds exactly one animation type per run: entrance, exit, state transition, scroll linked, gesture driven, or continuous ambient.

## Give every moving element a physics model

| Element kind | Parameters to set |
|---|---|
| Spring | Mass, stiffness, damping, and the settling criterion |
| Easing curve or keyframes | Duration and easing (CSS cubic-bezier or equivalent). Default to fast (150 to 250 ms) for micro interactions and medium (250 to 400 ms) for transitions |
| Gesture driven | Drag axis, snap points, and release velocity |

Never hard code an arbitrary number without rationale. When several elements move together, state the choreography explicitly: the sequence, the stagger interval, and the overlap.

## Write the code inline and respect reduced motion

Produce the code in the target framework or library, inlining the animation rather than assuming a shared motion library exists. Annotate each transition with the element it affects and its model specific parameters (curve name and duration, or spring stiffness, damping, and mass).

When the user requests reduced motion or the `prefers-reduced-motion` media query is detected, replace physics based or continuous animations with instant state changes or opacity only fades, and document that substitution.

Before handing back, confirm every animation block names its target and parameters and that reduced motion handling is present and documented. When a Python script ran for curve fitting, record the script name and what it produced. If a script fails mid run, discard any partial output and report the script name, the failure point, and the last valid output before the failure.

Animation quality cannot be judged algorithmically, so the work is complete only when the user confirms the result meets the need. Present the artifact for review and wait for that confirmation. The handoff names each animation with its curves or spring parameters per element, duration and easing per transition, the reduced motion substitution flag when applied, and fitted parameters plus script name when curve fitting was performed.
