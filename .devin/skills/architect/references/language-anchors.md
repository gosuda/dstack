# How modules map onto each language

Each language draws the module line with its own constructs. Pick the row for the target language when naming the interface, the seam, and the adapter, and use its boundary mechanism when enforcing entry-point rules from `../SKILL.md`.

## TypeScript

A module is a package under the packages root. Its interface is the exported types, function signatures, documented invariants, error shapes, and config the root files expose. The seam is the package's root files. The adapter is the concrete file behind the root export. Enforce first with the package's `exports` map, which restricts which subpaths importers can reach, then with dependency-cruiser entry-point rules keyed on path depth (root files public, any subfolder private) plus a no-circular rule, run in the repo's own verification. Public versus private follows depth, so adding a folder never needs a config change. Proof limit: the compiler does not reject deep imports; the repo check does.

## Python

A module is a package (a directory with `__init__.py`, or a namespace package). Its interface is what `__init__.py` re-exports plus documented invariants, exceptions, and config. The seam is the package's top-level namespace. The adapter is the concrete submodule behind it. Enforce with import-linter contracts (forbid imports reaching past the top level into private submodules), run in the repo's own verification. Tests import through the top-level namespace like any other caller. Proof limit: Python has no compiler-enforced private imports; the contract check, not the interpreter, is what bites.

## Rust

A module is a crate or a module path. Its interface covers trait bounds, lifetime constraints, error enums, and `#[must_use]`. The seam is a trait-object bound or a generic parameter. The adapter is the concrete `impl Trait for Type`. Enforce with visibility: `pub` at the crate root for the interface, `pub(crate)` or private for internals, so reaching past the root fails at compile time.

## Go

A module is a package. Its interface covers the named interface type, package error sentinels, and the context-cancellation contract. The seam is the interface declaration site. The adapter is the concrete struct with method receivers. Enforce with package layout plus `internal/` directories: code outside the parent tree cannot import `internal/` paths, and cross-package use goes through the package's exported names only.

## OCaml

A module is the `.ml`/`.mli` pair. Its interface is the `.mli` plus invariants encoded by the abstract type `t`. The seam is the signature consumed by a functor. The adapter is the functor argument module. Enforce with the `.mli`: anything absent from the signature is unreachable, so narrowing the `.mli` narrows the interface with compiler proof.

## Java / Kotlin

A module is a package or a build module. Its interface covers the `interface` or `sealed interface`, checked exceptions, and documented invariants. The seam is the interface. The adapter is the implementation wired through the DI container or service loader. Enforce with module descriptors (JPMS `exports`, or Gradle module boundaries) plus package-private visibility for internals.

## When no checker exists yet

Add the narrowest static boundary check the toolchain supports and fold it into the repo's own verification; that check is the enforcement, and the temporary-violation proof in `../SKILL.md` applies to it. Until it lands, a search for imports reaching past the public names is only an interim tripwire that proves nothing, and the boundary rule stays recorded next to the scope it guards.
