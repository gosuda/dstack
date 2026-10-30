---
name: exhaustive
description: 'Use when asked to prove coverage, find missing cases, or enumerate state, decision, requirement, or behavior space. Not for round-based or single-property tests: use askme, tests-practices.'
---

# Exhaustive coverage audit

You prove that nothing was missed. Given a target surface, you enumerate every cell in its space, check each one with an executable check or an explicit reasoned argument, classify all of them, and emit a coverage manifest with gaps sorted so a caller can hand them to follow-up work. You read the target source but change nothing in it. The only artifact you may write is the manifest file itself, and deleting that file rolls back the run.

Start only with a supplied target: a code area, a spec or feature, a design with open forks, or a refactor or deletion scope. A caller may also request machine-readable `exhaustive-manifest/v1` output. If the target space is unbounded or unidentifiable after one read, stop and ask one question to bound it. Do not enumerate an infinite space.

## Name the space you will cover

Choose the enumeration that fits the target and restate the choice in your output so the reader knows which space was covered:

* State space (code with lifecycle, state machines, or error paths): the State by Event by Outcome Cartesian matrix.
* Decision space (a design with open forks): the dependency-respecting set of decision axes.
* Requirement space (a spec or feature): the requirement-to-symbol map, each acceptance criterion traced to a code or test symbol.
* Behavior surface (a refactor or deletion): every exported symbol and reachable path in scope.

Enumeration is algorithmic and single-pass. It is not round-based questioning or hypothesis sampling.

## List every cell, then check each one

Enumerate the full cell list with tool-backed discovery: structural search for code constructors and match arms, reference search for symbols and callsites, direct reads for spec criteria. Every cell carries an `id` and a one-line description. The list is the universe: nothing outside it is in scope, and nothing inside it may be silently dropped.

Execute a check per cell: a programmatic check that proves coverage or exposes the gap. That means structural or reference search for code, a read for prose, or a test run where an independent invariant or adversarial test is the proof. Saved-output pins, mock echoes, and source-text assertions are never proof. A cell with no executable check gets classified by an explicit reasoned argument, never by silence.

## Classify everything and emit the manifest

Classify every cell as exactly one of `covered`, `gap`, or `deferred`, each with a one-line reason. `deferred` requires a named owner or follow-up; it is not a silent drop. Gaps and deferred cells are expected outputs, not failures.

Emit the coverage manifest: the classified cell list plus the one-line tally `covered: N, gap: M, deferred: K, total: T`. For a code state space, also assert zero wildcard catch-alls over the enumerated constructors, verifiable with structural search. Each wildcard catch-all over the enumerated constructors is a `gap` covering its unexplored arms, and the run is not done until that assertion passes.

Sort `gap` cells in dependency order so a caller can hand them to a follow-up workflow without rebuilding the space, and emit the ordered gaps. Do not run downstream question or ideation workflows yourself.

After any fix the user applies to a `gap`, re-enumerate once. Stop when a re-enumeration adds no new unclassified cell. If re-enumerations keep adding unclassified cells, stop and return the last manifest with its tally and the open `gap` list. Never swallow a check failure or pretend the done condition holds.

## When the space will not cooperate

* Unbounded space: stop after one read, ask exactly one bounding question, and mutate nothing. If it remains unbounded, return blocked naming the missing boundary, and emit no manifest as done.
* Unverifiable universe: if discovery tooling fails or returns nothing for a region, classify the affected cells `gap` with the tool failure as the reason. If the universe itself cannot be enumerated, return blocked. Never claim zero unclassified cells over an unverified universe.

What you hand back: the coverage manifest with every cell (id, description, classification, reason, executed check), the tally line, the named target space, the wildcard catch-all assertion for code state spaces, and the dependency-ordered gap list, as human-readable text or `exhaustive-manifest/v1` YAML on request.
