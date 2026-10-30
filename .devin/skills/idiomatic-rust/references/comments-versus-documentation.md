# Code commentary and documentation standards

Clear code expresses its own structure through types, naming, and semantic function boundaries. Ordinary implementation comments (whether explaining why, documenting workarounds, offering rationale, or tracking TODOs) are prohibited. There is no `// CONTEXT:` or `// TODO:` exemption. Implementation comments are restricted to the minimum required `// SAFETY:` justifications where actual repository lints require them, and necessary compiler directives. Public documentation (`///` and `//!`) forms the published interface contract, defining necessary public and module invariants and caller safety obligations. Rustdoc checks link resolution and doc-test code, not the truth of prose explanations; documentation warnings must be fatal in the repository's configured docs gate, as plain `cargo doc` does not guarantee failure on warnings.

## Distinction between comments and documentation

| Dimension | Implementation comments (`//`) | Public documentation (`///` and `//!`) |
|---|---|---|
| Primary purpose | Prohibited for ordinary reasoning, workarounds, rationale, or TODOs; restricted to minimum required // SAFETY: justifications where lint-mandated, and compiler directives | Document public API contracts, necessary module/type invariants, error conditions, and caller safety obligations |
| Tooling verification | Unchecked by compiler; fragile and subject to drift | Rustdoc checks links and compiles doc-tests, but cannot verify the truth of prose; documentation warnings must be fatal in the repository's configured docs gate |
| Scope | Private implementation details | Public interfaces across crates and modules |
| Target audience | Maintainers modifying internal implementation | Consumers using the crate interface via `cargo doc` |

## Safety justifications for unsafe code

Where actual repository lint policies (such as `clippy::undocumented_unsafe_blocks`) require it, unsafe blocks must carry the minimum necessary `// SAFETY:` comment establishing why the operation is sound, grounded in concrete evidence rather than speculation. Public `unsafe fn` declarations must document caller safety obligations under `# Safety`. Rely on semantic code structure, types, and invariants to ensure safety boundaries:

- Pointer validity: State why raw pointers are non-null, properly aligned, and point to valid, initialized memory of the expected size.
- Bounds and capacities: State why slice lengths, offsets, capacities, and memory allocations are strictly respected.
- Aliasing and concurrency: State why no data races, concurrent mutable aliases, or lifetime violations can occur.
- Caller obligations and contract verification: Ensure public `unsafe fn` declarations document caller obligations exhaustively under `# Safety`. Where feasible, verify preconditions with `debug_assert!` checks prior to the unsafe block to catch contract violations during test runs.

## Elimination of ordinary implementation comments

Ordinary implementation comments that narrate logic, explain why, justify workarounds, provide rationale, or track TODOs add noise and drift out of synchronization with code changes. There is no exemption for architectural context (`// CONTEXT:`) or issue tracking (`// TODO:`).

Ordinary implementation comments are prohibited in production code, keeping only the minimum required `// SAFETY:` justifications where actual repository lints require them, and necessary compiler directives. When code feels complex enough to demand narrative commentary, refactor the semantic structure instead:

- Extract self-contained logic into small, descriptive helper functions.
- Replace raw primitive flags, magic numbers, and loose tuples with domain-specific structs and enums.
- Replace procedural, comment-heavy flows with pattern matching and iterator combinators.

For guidance on balancing function extraction against code locality, see [Coding styles and idioms](./coding-styles-and-idioms.md).

## Public and module documentation discipline

Do not impose automatic per-item documentation boilerplate or demand mandatory template sections across every public item. Trivial constructors, obvious getters, and self-explanatory types do not benefit from formulaic checklists that restate identifiers.

Retain the minimum necessary public and module contract documentation:

- Behavioral invariants: State the domain guarantees and state properties upheld by the type, trait, or function across operations.
- Fallible conditions (`# Errors`): When a function returns `Result`, document the concrete conditions that produce each error variant.
- Panic conditions (`# Panics`): When a function can deliberately panic, document the exact failure conditions and unsatisfied caller preconditions.
- Caller safety contracts (`# Safety`): Mandatory on all public `unsafe fn` declarations, exhaustively detailing every precondition and memory invariant callers must uphold to avoid undefined behavior.
- Executable examples (`# Examples`): Provide executable doc-tests where usage is non-obvious, demonstrating realistic construction, fallible invocation, and error handling. Trivial operations do not require redundant example boilerplate.

## Module-level and crate-level documentation

Rust provides module and crate doc comments (`//!`) placed at the root of `lib.rs`, `main.rs`, or module files:

- Subsystem architecture: Explain module responsibilities, boundary relationships, and system invariants at the module boundary rather than scattering fragmented explanations across individual private functions.
- Quickstart workflows: Provide a high-level usage flow demonstrating how the exported types integrate into a complete operational sequence.
- Boilerplate hiding: Lines prefixed with `# ` in doc-test blocks execute during `cargo test --doc` but are omitted from rendered documentation, keeping examples concise while ensuring end-to-end type safety and compilation.

## Alignment with repository lint policies

Do not impose blanket new documentation mandates or automatic per-item section boilerplate across items that do not require them. Honor real repository lint requirements, such as enabling `#![deny(missing_docs)]` on library crates where required by crate policy.

Ensure documentation enforcement focuses on genuine soundness and contract requirements:

- Library crate APIs: Satisfy `#![deny(missing_docs)]` where mandated by repository configuration without generating tautological, low-value filler comments.
- Safety contracts: Enforce `clippy::missing_safety_doc` on `unsafe fn` declarations to ensure caller obligations and memory invariants are never omitted.
- Application and internal crates: Retain the minimum necessary public and module invariants, errors, and safety conditions rather than introducing unmandated documentation rules.

## Documentation verification and review

Review public interfaces to ensure documentation reflects actual runtime behavior:

- Enforce fatal documentation warnings in CI: Documentation warnings must be fatal in the repository's configured docs gate (e.g., `RUSTDOCFLAGS="-D warnings" cargo doc --no-deps`). Plain `cargo doc` does not fail on warnings and cannot guarantee clean documentation.
- Tooling verification boundaries: Rustdoc checks link targets, syntax, and doc-test code compilation via `cargo test --doc`, but does not check the truth of prose explanations. Rely on semantic code structure, tests, and types to prove invariants.
- Focus review on invariant accuracy: Ensure documented error conditions match real `Result` variants, safety sections exhaustively cover caller obligations and undefined behavior risks, and structural refactoring preserves public contracts without leaving stale commentary.
