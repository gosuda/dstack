# Trying several interfaces before committing

When the user wants competing options for a chosen deepening candidate, run parallel passes and compare. The first idea is rarely the best, so demand at least two.

Reads with the shared words from `../SKILL.md`: module, interface, seam, adapter.

## Frame the problem first

Before spawning passes, write a short explanation of the problem space for the chosen candidate:

- The constraints any new interface must satisfy.
- The dependencies it relies on, with each category from `deepening.md`.
- A rough illustrative sketch to ground the constraints: not a proposal, just something concrete. Use the codebase's primary language; for cross-language reviewers a parallel sketch in a second language family helps.

Show this to the user, then start the passes. The user reads while the passes run.

## Run competing passes

Spawn two or more passes in parallel; two is the floor. Add a third pass, designed around ports and adapters, when a seam crosses a process or team bound. Each pass must produce a radically different interface for the deepened module. Give each pass its own brief (file paths, coupling detail, dependency category, what sits behind the seam) and a different design constraint:

- Cut the interface down: fewest entry points, most behavior per entry point.
- Cover the most ground: support many uses and extensions.
- Serve the common caller: make the default case trivial.
- Third pass, only with a cross-bound seam: design around ports and adapters.

Each pass returns the interface (types, methods, params, plus invariants, ordering, error modes, in the codebase's language), a usage example showing how callers use it, what the implementation hides behind the seam, the dependency strategy with adapters, and trade-offs naming where the interface pays off and where it stays thin.

## Present, compare, recommend

Present designs one at a time so each can be absorbed, then compare in prose on depth (behavior per unit of interface), locality (where change concentrates), and seam placement. Give an opinionated recommendation: which design is strongest and why. When elements from different designs combine well, propose a hybrid. The user wants a read, not a menu.
