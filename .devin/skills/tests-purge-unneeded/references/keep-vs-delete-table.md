# Keep vs. delete: language-agnostic decision rubric

Always ask what real bug in the production code this test would catch. If no answer survives reading the code, the test does not earn its keep. Aggression means investigating the uncertain candidate, not deleting it by assumption.

Critical scoping rule: the compiler proves types and layouts, not semantic mapping. A constructor that takes `(id, name)` and assigns `self.id = id` and `self.name = name` with no other logic is direct pass-through and the compiler covers it. A constructor that validates, normalizes, defaults, transforms, or deserializes runs real logic; the test of that logic is a real-bug test no matter how trivial the result type looks. Read every Delete row below as conditional on the operation being direct, no-logic pass-through.

## Decision table with matching proof class

| Test pattern | Static-typed (Rust, TS-strict, Kotlin, Java, C++, OCaml) | Dynamic (Python, JS, Ruby) | Proof class when deleted |
|---|---|---|---|
| Constructor that only assigns parameters, no logic | Delete | Keep as boundary shape, runtime can drift | A compiler guarantee (static); C subsumption if dynamic and a stronger shape test survives |
| Constructor that validates, normalizes, defaults, transforms | Keep, testing logic | Keep | No deletion; if duplicated, C subsumption to the stronger test |
| Identity passthrough (`f(x) == x`, no transform) | Delete; function is dead code, inline it and the test deletes itself | Delete; test the transform if `f` transforms | B demonstrated tautology |
| Function returns the declared type, no logic | Delete | Keep at I/O boundaries; otherwise consider strict typing first | A compiler guarantee (static only) |
| Mock returns fixture, assert returns fixture | Delete | Delete | B demonstrated tautology |
| Derived default or generated default | Delete | N/A | A compiler or generator guarantee |
| Hand-written custom default or factory with non-obvious logic | Keep | Keep | No deletion; if duplicated, C subsumption |
| Direct field-copy assembly, no logic | Delete | Keep if dynamic field manipulation is plausible | A compiler guarantee (static only) |
| Assembly with mapping, filtering, defaulting | Keep | Keep | No deletion; if duplicated, C subsumption |
| Deserialization and parsing (`from_str`, `serde`, `Zod`, `pydantic`) | Keep, runtime boundary | Keep | No deletion |
| Re-export forwarding (`pub use foo::bar`) | Delete | Delete | A module-system guarantee |
| Parser rejects malformed input | Keep | Keep | No deletion except by C with case-by-case mapping |
| Error-variant semantics | Keep | Keep | No deletion except by C with case-by-case mapping |
| HTTP status and response shape | Keep | Keep | No deletion except by C with case-by-case mapping |
| Authn and authz enforcement (401 and 403 paths) | Keep, security invariant | Keep, security invariant | No deletion except by C proving the same attack path is covered |
| Input validation (length, format, range) | Keep | Keep | No deletion except by C with case-by-case mapping |
| Rate limiting and throttling | Keep | Keep | No deletion except by C with case-by-case mapping |
| Real DB transaction commit plus rollback | Keep | Keep | No deletion except by C with case-by-case mapping |
| File I/O paths, permissions, atomic writes | Keep | Keep | No deletion except by C with case-by-case mapping |
| Network retries, timeouts, partial failures | Keep | Keep | No deletion except by C with case-by-case mapping |
| Concurrency close, deadlock, race semantics | Keep | Keep | No deletion except by C with case-by-case mapping |
| `unsafe` block contract | Keep | N/A | No deletion |
| Property-based invariant | Keep, high signal | Keep, high signal | No deletion |
| Mutation-validated load-bearing test | Keep | Keep | No deletion |

Protected rows protect meaningful coverage, not every file. A redundant protected test may be removed only when surviving coverage demonstrably preserves its required cases and detects the relevant defects. One missed mutant never proves worthlessness; one killed mutant never proves a whole file is load-bearing.

## Proof classes

| Class | When it settles deletion |
|---|---|
| A compiler guarantee | The static checker proves the property. Name the guarantee and the language reference. No production edit. |
| B demonstrated tautology | The test outcome follows from the test itself. Show why no production change except deleting the test changes the outcome. No production edit. |
| C proved subsumption | Surviving tests preserve every required case. Name each survivor and map each case. Run the survivors; they must pass. |
| D meaningful mutation | The named bug the test claims to catch is injected, the test is run, the mutation is reverted immediately. Use only when A through C do not settle the case. |

## Tiebreakers

1. Can a bug be named that the test catches? If yes after reading code, select the matching class. If no, keep pending human review.
2. Does the test fail only when the test itself changes? Then it pins the test, not behavior; class B candidate.
3. Is the test the only cover for this behavior? Keep it; prefer writing a stronger test over deleting the only one.
4. Is the path security-sensitive? Keep even when redundant unless class C proves the same attack path is covered.

## Anti-patterns to delete with class B

| Anti-pattern | Why it is worthless |
|---|---|
| Tautology tests | Asserting a value immediately after constructing it with that value |
| Implementation tests | Asserting which private methods ran instead of what public behavior resulted |
| Coverage-driven tests | Written to hit a line, not to catch a bug |
| Snapshot or saved-output pins | The verdict repeats a saved output instead of checking an independent property; any deliberate change requires updating the pin anyway |
| Just-in-case tests | Written without a named failure mode they would catch |
