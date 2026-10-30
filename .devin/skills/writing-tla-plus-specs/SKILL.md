---
name: writing-tla-plus-specs
description: 'Use when a protocol, concurrent algorithm, or design needs a model-checked TLA+ or Alloy spec, or a TLC or Apalache trace needs reading. Not for choosing when to model: use validation-first-driven.'
---

# Writing TLA+ specs

Some designs can only be trusted after a model checker has tried to break them. This skill builds that check for a distributed protocol, concurrent algorithm, or system design, then reads whatever counterexample comes back. Each named invariant and temporal property ends the run either passing under a recorded bound and configuration, or mapped through its trace to a named design defect.

Writes stay local and reversible: `.tla`, `.cfg`, `.qnt`, and `.als` files plus the tool output directories they produce (TLC's `states`, Apalache's `_apalache-out`). Rollback deletes those files. No remote system is touched.

What you need before modeling: a description of the system, its state variables, the actions that change them, and the properties that must hold. The grounded tool set is `tla2tools.jar` v1.7.4 (stable; v1.8.0 is a pre-release, and the old TLA+ Toolbox GUI is unmaintained, so work through the `tlaplus.vscode-ide` extension or the command line), Apalache v0.62.4 (fetch `apalache.zip` or `apalache.tgz` from GitHub Releases), Alloy v6.2.0 (standalone `.jar` from alloytools.org), and Quint 0.33.1 (install per https://quint-lang.org/docs/getting-started). TLC, Apalache, and Alloy all need a JVM; complete Alloy temporal checking optionally uses external NuSMV 2.7.1 or nuXmv 2.2.0 on `PATH`. Optional extras are a state-space bound, a `ConstInit` operator bounding constants for Apalache, and a Quint spec for authors who prefer its surface syntax.

## Pick the engine

TLC fits a small finite instance whose properties include liveness. Apalache fits unbounded constants or a state space too large for explicit enumeration, with safety invariants or bounded temporal checks. Alloy fits questions about data or relational structure rather than protocol steps; Alloy 6 adds `always`, `eventually`, `after`, `before`, `until`, and `releases` for temporal checks. Bounded checks (default 10 steps or `for M .. N steps`) run entirely within Alloy 6's embedded backend (SAT/SMT via Pardinus). External solvers on `PATH` are needed only for complete or unbounded model checking (`for 1.. steps`) or when chosen in Options: use either NuSMV 2.7.1 (release date unpublished; never use archive Last-Modified as release date) or nuXmv 2.2.0 (June 4, 2026). Preserve operator license and installation authority: never perform automatic downloads, as each external engine carries separate non-commercial or LGPL terms. Quint serves only as an alternate front end: it keeps TLA semantics and hands checking to Apalache or TLC through `quint verify`. Name one engine with the reason.

## Write the skeleton

A TLA+ spec declares `CONSTANTS` and `VARIABLES`, defines `Init`, one operator per action, `Next` as their disjunction, `Spec == Init /\ [][Next]_vars`, and a `TypeOK` invariant naming every variable's domain. Keep each action a conjunction of a guard with primed assignments. For Apalache, annotate every constant and variable with `\* @type: T;` (types `Bool`, `Int`, `Str`, `Set(T)`, `Seq(T)`, `<<T1, T2>>`, `T1 -> T2`, `{ f: T }`) and run `apalache-mc typecheck Spec.tla` until it prints `Type checker [OK]`. An Alloy spec declares `sig` and `fact` blocks, one `pred` per operation, and `run p for N` or `check a for N` commands, where `for` bounds each signature. The skeleton is ready when it parses and `TypeOK` holds in the initial state.

## State the properties

Put safety in invariants, one operator per claim, named for the claim (`NoDoubleSpend`, not `Inv1`). Put liveness in temporal formulas under a fairness assumption (`WF_vars(Action)` or `SF_vars(Action)`) in `Spec`; without fairness every liveness property fails on a stuttering behavior. Every property from the design brief needs its operator, and every liveness formula needs its fairness.

## Run TLC and read the trace

Write `Spec.cfg` with `SPECIFICATION Spec`, `CONSTANTS Name = Value` for each constant at a small instance (two or three processes first), `INVARIANTS TypeOK NoDoubleSpend`, and `PROPERTIES Liveness`. Run `java -jar tla2tools.jar -config Spec.cfg -workers auto Spec.tla`. Pass `-deadlock` only for a terminating system where deadlock is not a defect; otherwise TLC treats a successor-free state as an error. Take a quick random pass with `-simulate num=1000` before the exhaustive run, and use `-dfid N` for depth-first search of a deep space. TLC exits 0 with a recorded state count on success, or 11 (deadlock), 12 (invariant violation), or 13 (temporal property violation) with a trace.

Read that trace from the end. It opens with `Error: Invariant X is violated`, then `State 1:` through `State n:`, each listing every variable and the producing action. The violated invariant in the last state names the variable that went wrong; walking backward finds the first action whose guard was too weak. Use `-difftrace` to print only changed variables and `-dumpTrace json trace.json` to save the trace for diffing against the next run. Classify the cause as a spec bug (the action mis-models the system), a property bug (the invariant promises more than the design does), or a design defect. Only the third goes to the design owner as a finding.

## Scale with Apalache, or drive Quint

When TLC cannot finish, run `apalache-mc check --inv=NoDoubleSpend --length=10 Spec.tla`; `--length` bounds the step count and defaults to 10. Bound constants with `--cinit=ConstInit` where `ConstInit == N \in 2..5`. Prove an inductive invariant with two runs: `--init=IndInv --inv=IndInv --length=0` for the initial state, then `--init=IndInv --next=Next --inv=IndInv --length=1` for preservation across every step. Counterexamples land in `_apalache-out/` (overridable with `--out-dir`) as `counterexample1.tla`; `--max-error=N` collects up to N of them. Switch the backend with `--smt-solver=cvc5` when Z3 stalls. The property holds at the recorded bound, or its counterexample gets the same classification as a TLC trace.

For a Quint spec, run `quint typecheck spec.qnt`, then `quint run spec.qnt --invariant=NoDoubleSpend --max-steps=20 --max-samples=10000` for random simulation, then `quint verify spec.qnt --invariant=NoDoubleSpend --max-steps=10` for the Apalache-backed bounded check (`--backend=tlc` selects TLC). `quint run` prints `[violation]` with the trace on failure; `--out-itf` writes it as an ITF file. Record the same property classification.

Beside every property, record tool, version, configuration, bound, state count or step length, and wall time. A property checked at three processes and depth 10 is proven at that instance and nothing more, so write the bound next to the claim.

## When the check fights back

TLC exits 150 for a spec parse error and 151 for a config error: fix the reported line and rerun. On state-space explosion (exit 152, or a run that never finishes), shrink the constants, add a `VIEW` operator abstracting state, or move to Apalache; never lower the property to make the run pass. On an Apalache `Type checker [FAILED]` line, fix the `@type` annotation at the reported file and line; an untyped operator is a spec defect, not a tool limit. On a liveness violation whose trace ends in a stuttering loop, add the missing fairness condition and rerun; a design with no fair action that makes progress is itself the finding. On an Alloy `check` counterexample, read the instance in the visualizer and shrink scope to the smallest failing instance. TLAPS (`tlapm`) is a proof checker, not a path this skill drives: last stable is 1.5.0 (2022-10-04) with 1.6.0-pre marked pre-release, so a required proof means saying so and handing off. When no useful bound can be checked, report the bound reached with the reason and leave the property at full strength.

## What you hand back
Spec files (`.tla` with `.cfg`, `.qnt`, or `.als`) on disk; one result line per property naming engine, version, bound, and outcome; for each violation, the saved trace, its classification (spec bug, property bug, or design defect), and the fix applied or the defect handed to the design owner.
