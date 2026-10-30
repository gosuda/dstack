# Shape signals: triage aid for routing

This file used to be a verbatim detector prompt for an old diff-only pass. That pass is gone: simplify now routes each cut to its owning skill. What survives here is the pattern list, repurposed as triage signals. A signal suggests where to look and which owner probably fits; the owning skill decides, using its own contract.

## How to use these signals

Match what you see in and around the change against the list below, then confirm the level with the inspection in `orchestration.md` (callers, boundaries, edges) before dispatching. Never treat a signal as a finding on its own.

## The signals and their likely owners

- Redundant state (mirrored variables, effects that could be direct calls): `code-simplification` when it spans a module interior; `minimalism-driven` when it is an addition still taking shape.
- Parameter sprawl (functions gaining parameters instead of generalizing): `minimalism-driven` at authoring time, `code-simplification` once the sprawl is established structure.
- Copy-paste blocks with slight variation: `code-simplification`, folded into the general case.
- Leaky abstractions (internals exposed across a respected boundary): `code-simplification` for a single module; `architecture-simplification` when the boundary itself is misplaced and the layout must move on an explicit human ask.
- Stringly-typed code (raw strings where a constant, enum, or closed type exists nearby): `code-simplification`.
- Redundant structural nesting (containers adding nothing over a single child): `code-simplification`; leave any wrapper whose purpose is unconfirmed rather than flattening on a guess.
- Nested conditionals three or more deep: `code-simplification`, reshaped into guards, early returns, or a lookup.
- Comments explaining what the code does: `no-comments`, relocating the knowledge before removing the comment. Comments explaining why (hidden constraints, subtle invariants, workarounds) are never signals.
- Dead code, unused imports, unused exports: `code-simplification` inside one artifact class; `guillotine` when the dead weight spans artifact classes; `refactor-break-compat` when the dead surface is consumer-facing and needs a confirmed demolition.

## What never counts

Safety checks are not signals: input validation at trust boundaries, error handling that prevents data loss, security checks, and accessibility affordances stay even when they look like ceremony. Fewer lines is not the goal; faster comprehension with contracts intact is.
