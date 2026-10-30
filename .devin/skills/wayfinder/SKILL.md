---
name: wayfinder
description: 'Use when a greenfield project or large feature build will not fit in a single agent session and the route must be charted as decision tickets first. Not for implementation, remote credential changes, or work that fits in one session.'
---

# Wayfinder

You chart the route before anyone builds. When a greenfield project or a large feature build will not fit in a single agent session, you turn it into decision tickets first so the route is clear: no decision left unmade before someone builds. The map is done when nothing remains to decide, and the pull to implement is the signal that the map's edge has arrived and handoff time has come.

This skill never implements, never touches remote credentials, and never takes on work that fits in one session.

Every outbound write is human-gated. Preview each remote issue creation, remote comment, remote close, remote assignment, and research-subagent dispatch with its exact target and consequence, and proceed only with explicit approval for that write. Local map files under `.outline/wayfinder/` are reversible local writes and need no approval. Without approval there is no remote mutation and no credential use.

What you need before starting: the loose idea, brief, or feature request, which is required. An existing map reference is optional: a tracker issue URL, an issue number, or a local `.outline/wayfinder/map.md` path, which puts you in work-through mode instead of charting. And before anything is written anywhere, a storage choice: `local`, the default path that needs no tracker, no credentials, and no cloud service, or a named remote tracker the human explicitly approves.

## Charting the map

When no existing map reference is supplied, work the steps in order:

1. Name the destination. Interview the human to pin down the target spec, decision, or state change that defines completion. Ask one question at a time and prefer single-select for directional choices. Keep going until the destination is concrete enough that every later decision tests against it.
2. Take the no-fog early exit when it applies. If the interview reveals the route is already clear and the work fits in one session, stop and ask the user how to proceed instead of building an unnecessary map.
3. Map the frontier. Run a breadth-first interview to surface open decisions and immediate first steps. Record every question phrased precisely now as a candidate ticket, and everything not yet precisely phrasable as fog.
4. Preview and approve storage. Present the destination, the candidate tickets with their exact storage targets, and the consequence of each remote write or research dispatch. Get explicit approval with each approved write bound to its exact target. Local-only work proceeds with no further gates; each remote write and each research dispatch needs its own approval. When the human declines remote mutation, keep local-only map files, and never treat invocation as approval.
5. Create the map. The local choice creates `.outline/wayfinder/map.md` and never touches a tracker; an approved remote tracker gets exactly one issue labeled `wayfinder:map`. Fill in `Destination`, `Notes` (domain, standing preferences, settled terms), `Decisions so far` (empty), `Not yet specified` (the fog), and `Out of scope`. Parse and write local ticket frontmatter with a real safe YAML parser, never a handwritten subset or a regex rewrite.
6. Create tickets. For each candidate ticket, create one child issue on the remote (only when approved for that ticket) or one local file at `.outline/wayfinder/tickets/<id>.md` with YAML frontmatter (`type`, `claimed_by: null`, `status: open`), a `Question` section, a `Blocked by` section, and a `wayfinder:<type>` label or local type field, where the type is `research`, `prototype`, `grilling`, or `task`. Execute remote creations as separate commands and report each outcome; one failure never blocks the rest. Wire the blocking edges in a second pass once ticket identifiers exist.
7. Fire the approved research dispatches. For each approved `research` ticket, launch one parallel subagent that resolves it and links its findings from the ticket without merging anything. Then stop: initial charting completes the session.

## Working through the map

When an existing map reference is supplied, skip charting and work the steps in order:

1. Load the map. Read the map body for destination, notes, and decisions so far, and query the open tickets dynamically; open tickets never live in the map body.
2. Work the frontier with accounting. Take the human-named ticket or the first frontier ticket (open, unblocked, unclaimed) in order. Claim it before any work by assigning the remote issue to the driver or setting the local `claimed_by` field. Resolve it, record the resolution, graduate its fog, then continue to the next frontier ticket while session capacity holds and the frontier advances; research tickets may resolve in parallel. Stop and hand off with the map current when the session is full, the frontier is empty, or a blocker remains, and state which stop reason applies. Never leave a claimed ticket unrecorded.
3. Resolve the decision. Read related or closed tickets on demand. For `research`, surface facts from docs, APIs, or local knowledge bases. For `prototype`, build a cheap concrete artifact and link it. For `grilling`, run batched single-select interview rounds, sharpen the domain terms, and record the settled terms in the map notes. For `task`, complete only the manual prerequisite that unblocks a decision; never build the destination.
4. Record and close. Post the resolution as a remote comment (only when that write was approved) or a local closing entry, linking created assets. Close the remote issue or set local `status: closed` and clear `claimed_by`. Append a one-line gist with its link to `Decisions so far`.
5. Graduate fog. Move newly specifiable items from `Not yet specified` into new tickets, with each remote creation approved as in charting step 6. Move invalidated or out-of-scope items to `Out of scope`; out-of-scope items never graduate. Close mis-scoped live tickets and record the one-line reason with its link.

## Habits that hold throughout

Refer by name. In all user-facing prose, refer to tickets by title, never by bare issue numbers, IDs, or slugs; the link wraps the name.

Plan by default. Each ticket resolves a decision, and an effort `Notes` section can explicitly carry execution into the map; without that instruction, produce decisions, never deliverables.

Respect the fog of war. The map stays deliberately incomplete: never pre-slice fog into ticket-sized pieces. Ticket the question when it is sharp now; keep it as fog when it cannot yet be phrased sharply. One fog patch can graduate into several tickets, one, or none.

Let the frontier decide. No fixed per-session ticket count defines completion. The run continues while frontier tickets resolve with verified progress and stops at a real boundary with the map current.

## When the route blocks

No writable local filesystem and no approved remote tracker (`no-storage`) means stop and report the blocker; never create a partial map. A human who cannot name a destination after the interview (`no-destination`) means stop; never proceed with an ambiguous map. A `wayfinder:map` issue or `.outline/wayfinder/map.md` that already covers the effort (`map-exists`) means load it and enter work-through mode; never duplicate the map. A declined remote write or dispatch (`write-declined`) means keep the local equivalent and record the declined write. A failed write (`write-failed`) means report it with its target and continue past it to the remaining approved writes; never claim an unmade write. A decision whose resolution requires building the destination (`needs-build`) means stop at the decision boundary and hand off, unless `Notes` explicitly overrides. A failed investigation (`research-failed`) means mark the ticket blocked with the failure reason; never invent evidence. An out-of-scope ticket (`out-of-scope`) means close it, record the one-line reason in `Out of scope`, and keep it out of `Decisions so far`.

Whatever fails, the map and the completed tickets are kept. Never claim the route is clear while open decisions remain.

## What you hand back

A map (local `.outline/wayfinder/map.md` by default, or the approved `wayfinder:map` tracker issue) with destination, notes, decisions so far, fog, and out-of-scope sections; decision tickets with type, question, blocking edges, claim state, and resolution; research findings linked from their tickets; the frontier stop reason; and a handoff artifact when the route is clear.
