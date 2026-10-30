---
name: recall
description: 'Use when asked to recover prior work and current status before resuming. Not for handoff snapshots: use handoff. Not for source or remote-system changes.'
---

# Recall

Pick up where an earlier session left off: figure out what it actually did, check that against the tree as it stands now, and name the single next thing worth doing. This job is read-only from start to finish, so no file edits, no version-control moves, no credentials, and no paid or remote actions. Its only product is a chat reply.

To start you need the session to recover, as an ID or session directory path, and the working directory it ran in. A scope hint (a file, module, or task tag) narrows the recovery. Leave it out and you recover the whole session. Handoff snapshots belong to the handoff skill, not this one.

Find the session's state file or transcript first. If there is none, answer `session-not-found` with the identifier and stop. Never invent work, artifacts, or actions that are not in the record. If the transcript will not parse, answer `transcript-parse-failure` with the parse error and stop rather than reasoning from partial data. If it parses but holds no identifiable work, answer `no-recoverable-state`.

Mine the transcript for discrete work records: completed actions, emitted artifacts, tool results, and navigation events, each with its outcome. Then hold every record up against the live tree by reading each file and version-controlled target the transcript names and confirming the record still matches. Anything that does not match becomes a `divergence` flagged on the record. Divergences stay visible in the result, since a capsule that hides them to look complete is a fabrication.

Tag every record `completed`, `in-progress`, `blocked`, or `diverged`, then choose one concrete next move: the highest-priority actionable item from the in-progress and blocked records that is not stuck behind an unresolved divergence. Return the capsule with `session_id`, `records` (each carrying action, outcome, status, and divergence note), `next_move`, and `divergences`, in that order. When some records verify and others diverge, return both together, verified records with their divergence flags. Nothing was mutated, so there is nothing to roll back.
