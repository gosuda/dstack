---
name: final-grain
description: 'Use when asked to push an already-working artifact to finished composition, texture, and feel. Not for remote or irreversible changes. Not for hygiene cleanup.'
disable-model-invocation: true
---

# Final grain

This skill finishes an artifact that already works: its composition, texture, and feel. It never repairs broken behavior and never substitutes for hygiene cleanup. The human asks for it by name, and only the human fires it, which is why model invocation stays disabled.

Everything here is local and reversible. Only the named artifact is written, and rollback runs through version control. Nothing touches VCS state, remote systems, credentials, or paid resources. The work is done when the artifact sits at the named path with visible polish applied and its original functionality confirmed intact.

## Confirm the targets before touching the file

Confirm the artifact path and that it is working as delivered. Classify what it is (document, code file, config, spec, report, or other) so the polish fits the form.

When the human named the polish targets, adopt them. Otherwise propose three dimensions (structural coherence, compositional refinement, and presentational polish) and wait. Either way, obtain explicit human confirmation of the targets before mutating any file. When confirmation is withheld or withdrawn, stop without mutation and return a blocked outcome.

## Polish a copy, then prove it still works

Before mutating, settle the rollback source. When the artifact is tracked in version control, note its current committed version. When it is not tracked, require the human to supply an existing recovery source first. Without one, stop as blocked.

Copy the artifact and apply polish to the copy along the confirmed dimensions only, leaving implementation correctness unchanged. Verify the polished copy preserves the original functionality, running a smoke test where one applies. Only then replace the original with the polished copy at the named path.

When polish breaks the artifact, restore it from its VCS version or the human-supplied recovery source, and return a rollback outcome with a report of what broke. When refinement oscillates or degrades without progress, stop after three cycles and return a non-converged outcome, producing no artifact under it.

Hand back the polished artifact at the named path with one paragraph saying which dimensions were refined and which choices were made in each.
