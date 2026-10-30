---
name: marketing-decision-map
description: 'Use when a marketing initiative is too broad for a brief and needs its decisions charted before action. Not for executing the selected strategy or tracking tasks.'
---

# Marketing decision map

Chart a marketing initiative that is too broad for a brief before anyone acts on it. You fix an observable destination, sort everything known into decided, answerable, blocked, unknowable, and out of scope, and either stop at the map or resolve one frontier decision per continuation with explicit user confirmation. The output is a map, never a task tracker or production plan.

This skill is read-only by default. It writes a map file only when the user explicitly names a writable path (`output_path`); otherwise it stays in chat. It never touches credentials, publication, outreach, or remote state, and it never executes the selected strategy, runs campaigns, or tracks production tasks. On failure there is no mutation: chat output only, unless a path was already approved for a completed map.

## What you need

- `initiative` (required): the unclear marketing effort to chart.
- `destination` (required): the observable outcome the map points at. Without one, stop and ask for it. Motion is not progress, so do not chart without it.
- `context` (optional): current user instructions and explicitly selected project material. Supplied material only, never inferred into a file. On a material conflict in the supplied context, stop, name the conflict, and do not resolve it by assumption.
- `output_path` (optional): a writable path for the map. Chat-only when omitted.

## Chart the territory

Fix the destination in observable terms and record standing constraints and notes. Then sort what is known so every item sits in exactly one bucket:

- Confirmed decisions (each recorded only on explicit user confirmation, with its basis)
- Current frontier (answerable now)
- Blocked questions (each with its missing prerequisite named)
- Fog (unknown and currently unknowable)
- Out of scope (the boundary of this map)

Apply only materially relevant lenses from this set: outcome, market, audience, problem, value, position, journey, channel, expression, economics, measurement, risk. Skip lenses with no bearing and say why. Name every lens used and every lens skipped with its reason.

## Chart mode or continue mode

In chart mode, stop before resolving the first consequential decision and present the map with its frontier untouched. In continue mode, resolve exactly one frontier decision: state the options, the evidence, and the recommendation, then ask for confirmation and record it as a decision only on explicit confirmation. At most one consequential decision is resolved per continuation, and no recommendation is ever recorded as a decision without user confirmation.

Never convert the map into a task tracker or production plan: no tasks, owners, or dates beyond decision sequencing. On a partial result, present the charted portion and mark the uncharted remainder as fog.

## What you hand back

A decision map: destination, notes and constraints, confirmed decisions (each marked user-confirmed with its basis), current frontier, blocked questions with prerequisites, fog, the out-of-scope boundary, and the single next decision when in continue mode.
