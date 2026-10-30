# Surveying and ranking shallow modules

Depth signals and two-axis scoring for the brownfield survey pass. Reads with the shared words from `../SKILL.md`: module, interface, depth, seam, adapter.

## Depth signals

For each public module (directories with an entry point, packages, or namespaces exposing types and functions consumed by other modules), note:

- Surface size: distinct types, functions, and constants on the public surface.
- Internal abstraction: private types, helper modules, or sub-namespaces holding logic separate from the entry point.
- Coupling: whether the public surface delegates to other modules or holds all logic inline.
- Width: whether the surface covers many unrelated responsibilities.

A shallow module has a broad public surface with few internal abstractions, logic sitting directly on the surface rather than behind internal seams.

## Two-axis ranking

Order shallow modules by:

- Refactoring effort: how many call sites or dependents would need to change. Lower effort ranks higher.
- Architectural gain: how much hidden behavior the module would gain from deepening. Higher gain ranks higher.

## Handoff shape

These entries travel in the reply, never in a file unless the user asks for one. Lead with the ranked list, one line per candidate (location, verdict, effort, gain). Give the full entry only for the top candidate: files and modules, concrete problem, deletion-test result, dependency category, plain-language solution without a premature interface, expected locality and testability change, smallest before-and-after sketch, strength (`Strong`, `Worth exploring`, `Speculative`), and any decision-record conflict worth reopening, plus a one-paragraph reason it ranks first and the seams it would need. Where the top candidate cannot be deepened without breaking a hard invariant or triggering a cascade, say so with the specific invariant or cascade: that rejection is load-bearing.
