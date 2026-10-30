---
name: architect
description: 'Use when non-trivial code needs a design, codebase architecture needs improving through survey and deepening, or one module needs targeted interface narrowing, seams, or testability. Not for rendered visual artifacts, deploy, or irreversible changes.'
---

# Architect

Design work before code: sketch a new unit cleanly, survey a grown codebase for shallow modules and deepen the best candidate, or narrow one module's interface until it earns its keep. Read-only until the request clearly allows edits, and then only inside the named files. Nothing here rewrites history, touches credentials or payment, publishes, deploys, or reaches a remote.

## When this fits, and when to walk away

Reach for this skill when the design is non-trivial and under-specified: a new code unit with real callers and failure paths, a codebase with suspected pass-through modules, a seam that needs placing, or code that resists testing. Say `no-design-needed` and change nothing when the request is trivial or already fully specified. Ask which branch applies when the request does not distinguish designing something new, surveying what exists, or fixing one named module.

## Words used here

These terms stay fixed so designs, reviews, and follow-ups mean the same thing. Do not swap in near-synonyms.

- Module is anything with an interface and an implementation, at any scale: a function, class, package, crate, or tier-spanning slice.
- Interface is every fact a caller must know: types, invariants, ordering, errors, configuration, and performance behavior. Never just the type-level surface.
- Implementation is what the interface hides.
- Depth is behavior hidden per unit of interface learned. A deep module gives high leverage through a small interface.
- Seam is a place where behavior can be substituted or tested in isolation without editing it in place.
- Adapter is a concrete implementation used at a seam. A small adapter can hold a large implementation and a large adapter a small one.
- Leverage is capability gained per unit of interface learned. Locality is change, bugs, and knowledge concentrating at one maintenance site.

## Designing something new

Bound the unit first: name the code, its callers, inputs, failure paths, and trust boundary. Sketch the usage surface before any implementation talk: the call plan, types, call sites, data shapes, invariants, and observable errors. Produce at least two competing sketches that each satisfy that surface and differ in structure or tradeoff, and test each against hidden complexity, leaky interfaces, unbounded scope, speculative generality, missing error and edge handling, seam placement, and testability. When every sketch has a blocking flaw, return to the usage surface and sketch again; stop once one coherent sketch has no blocking flaw. State the choice, what it costs, and which alternatives were rejected, then derive the plan: modules, interfaces, control flow, failure paths, migration, and what proof the implementation will need. Implement only when the request and authority permit; otherwise hand over the design package.

## Surveying what exists

This pass reads only. When the user names a direction, scan there first. Otherwise let recent-change hotspots pull attention, and when changes scatter with no defensible hotspot, widen the scan and record why. Read the applicable glossary and nearby decision records before judging module names or responsibilities, and record the chosen scope with the evidence that selected it.

List every public surface in scope: entry points, packages, namespaces, exported surfaces consumed by another module. For each, note surface size, internal abstraction, coupling, and responsibility width; see `references/survey-ranking.md`. Judge depth by leverage, not line counts, and run the deletion test on every suspect: if deleting the module makes complexity vanish, it was a pass-through, and the verdict must name the callers that would absorb the complexity. Rank by architectural gain against refactoring effort: more hidden behavior and stronger locality gain rank higher, fewer affected callers and cheaper migration rank higher, and a hard invariant or cascade that blocks deepening lowers the recommendation. Hand back the ranking in the reply, never in a file unless the user asks for one: one line per candidate with location, verdict, and effort and gain, plus one full entry for the leading candidate per `references/survey-ranking.md`. Write no temp HTML, load no CDN, open no browser, and propose no concrete interface before a candidate is selected. When no candidate is defensible, return `no-candidate` and change nothing.

## Deepening the chosen candidate

Read the selected scope first: files, callers, tests, glossary, decision records, and confirmed dependencies. Classify each dependency per `references/deepening.md` (`in-process`, `local-substitutable`, `remote-but-owned`, `true-external`); what cannot be classified is treated as `true-external` with an injected port.

Keep seams honest: one adapter is a hypothetical seam, so introduce no interface for hypothetical variation; two justified adapters, typically production plus test, make a real one. Present the candidate before mutating: files, problem, deletion-test result, plain-language solution, expected gain, dependency treatment, and the bounded file set. Edit only the candidate the user selects. Resolve one dependent decision at a time with a recommended answer each, bound the file set before mutation, and record established domain terms in the local glossary. Offer a decision record only when the reason is load-bearing for a future explorer who might re-suggest the same candidate; skip ephemeral or self-evident reasons.

Replace rather than layer: state the new interface contract, absorb in-scope special cases into it, migrate every scoped caller, delete the replaced shallow path with its obsolete mechanisms and tests once equivalent interface tests exist, and never keep the old path as a compatibility alias unless the user explicitly scoped it in. Essential behavior, validation, and proof carry over to the new contract. Stop for approval before any live-consumer break, data loss, or non-reversible act. Exercise the changed behavior through the same interface callers use, and confirm invariants, error modes, relevant adapters, and the final file set against the bound scope.

When alternatives are wanted, follow `references/interface-design.md`: frame constraints and dependency categories, produce at least two radically different interfaces, compare depth, locality, and seam placement, and recommend one, including a hybrid when elements combine well.

## One module under the microscope

Name exactly one target, confirm its source reads, and survey its interface surface, implementation, and crossing callers and tests. When depth cannot be judged inside this scope, stop and name the missing evidence. Judge deep or shallow by leverage with evidence, run the deletion test, and narrow the interface in order: fewer methods, simpler parameters, more complexity hidden, keeping the form that gives callers leverage and maintainers locality.

Keep one interface per module. The external seam carries it; internal seams used only by the implementation's own tests stay private. Every seam sits where something varies across it. State the intent explicitly: seal the dependency behind the seam, or deliberately expose it as a configuration key, module seam, or override hook. Choose by caller knowledge, locality, variation, and deletion-test evidence, never by a line or branch ratio. Migrate every in-scope caller to the chosen seam, keep the exact pre-change text for rollback, and re-verify callers and tests still cross the same seam.

Callers and tests cross the same seam: a test that must reach past the interface means the module is the wrong shape. Reject depth-as-line-ratio framing, which rewards padding the implementation, and reject interface-as-keyword-or-method-list framing, which drops invariants, ordering, errors, configuration, and performance facts. Anchor terms in the target language per `references/language-anchors.md`, inferring the language from source when unstated. Deliver the recommendation in the fixed vocabulary; when restructuring is in scope, keep edits inside the bounded module while every caller and test keeps crossing the same seam.

## Seams, testability, and guardrails

Locate each seam where a caller can substitute an alternate implementation or inject a test double; where none exists, propose the smallest interface introduction that creates one without widening the public surface. Make code testable by naming the concrete dependencies that block isolated testing and proposing seams that make them substitutable: prefer accepting dependencies over constructing them internally, returning results over mutating hidden state, and keeping the surface small. Harden only with guardrails tied to a protected invariant, such as type constraints, boundary checks, lint rules, analysis, or interface-level tests, naming the invariant each guardrail protects. Without implementation authority, stop at recommendations and mark anything not grounded in read code as inference.

## Keeping module boundaries honest in any language

A deep module needs its boundary enforced by the language's own visibility and import machinery, not by convention alone. Apply these rules with the mechanism in `references/language-anchors.md` for the target language:

- Code outside a module reaches it only through its public surface, the entry points named for the target language in `references/language-anchors.md`, never its internals.
- A module's own files import each other freely.
- A module's tests exercise it through its public surface like any other caller: they may import any module's entry points plus their own fixtures, never any module's internals, not even their own.
- Test fixtures are reachable only from tests; nothing else imports them.
- No dependency cycles.

Choose package tiers from owner and change-reason boundaries with navigation and change costs; the usual outcome is one tier of packages under the root, which keeps the module unit unambiguous, while a package's internals nest as deep as the domain needs. Nest a package inside another only when the inner unit has its own owner or change reason and its own enforced boundary; otherwise the nesting is bureaucracy, not depth. Expose several small entry points rather than funneling everything through one giant barrel that re-exports a whole subtree. Layering, which packages may depend on which, is a separate opt-in concern recorded alongside the boundary rules, not folded into them. Size depth and width from the domain and from navigation and change costs, never from an arbitrary cap; no empty layer towers, no folder-per-class bureaucracy.

Wire the boundary check into the repo's own verification: use the existing checker and config where one exists (merge the rules in and say what was added, never overwrite blindly), add the narrowest static boundary check the language supports where none exists, and fold it into the same umbrella command that already runs typecheck or tests. Prove the check bites on the real tree: run it clean, introduce a temporary deep import, observe it fail on the entry-point rule, revert, and run clean again. If the violation does not fail, the wiring is wrong, so fix it before finishing. One interface-hiding rule set covers how to import; layering rules cover which packages may depend on which.

## When to stop instead of pushing through

- `blocked`: code, callers, tests, glossary, decision records, or required behavioral evidence cannot be read; report what is missing and stop.
- `blocked-by-decision`: a decision record, user decision, or scope boundary conflicts with the candidate and no reopening is accepted; preserve the record and stop.
- `scope-drift`: the work widens past the named module, candidate, or file set; report the widening and change nothing outside the named artifacts.
- `ambiguous-mode`: the request does not distinguish designing new, surveying, or fixing one module; ask before proceeding.
- `unbounded-target`: one module cannot be isolated, or judging it needs evidence outside scope; stop before editing and name the missing evidence.
- `pass-through`: the deletion test shows the module hides no useful complexity; report it as shallow with its absorbing callers rather than rewriting it.
- `non-converged-interface`: the interface cannot narrow without changing caller-visible behavior beyond the bound; report the conflict and stop.
- `failed-edit`: restore every touched file to its captured pre-change contents and report the failure; when exact restoration cannot be proved, stop with `recovery-required` and list each affected file with its pre-change source.
- `missing-proof`: the design names no interface-level checks for its invariants, errors, or relevant adapters; stop before claiming completeness.
- `missing-dependency-treatment`: an external dependency cannot be classified; treat it as `true-external` with an injected port.
- `incomplete-survey`: the scan scope or recent-change evidence is insufficient; report the missing evidence, not a whole-codebase conclusion.
- `partial-result`: return the finished survey or analysis with unresolved decisions listed, and do not claim implementation or proof is complete.

## What gets handed back

Hand back, in the reply rather than a file unless the user asks for one, a design package with the bounded scope; the usage surface or candidate findings with the smallest visual; competing sketches or the targeted-module recommendation; depth, deletion-test, seam, adapter, dependency, and testability findings; the chosen design and rejected alternatives; implementation sequence, failure paths, migration, and proof requirements; changed-file bounds and rollback; and one terminal label: `done`, `no-design-needed`, `no-candidate`, `blocked`, `blocked-by-decision`, `failed-edit`, `non-converged-interface`, or `partial-result`.

Record only material that a future reader needs to reuse or avoid repeating the work: established domain terms in the local glossary, and a decision record only when the rejection reason is load-bearing. Never invent a mandatory report or log for its own sake.
