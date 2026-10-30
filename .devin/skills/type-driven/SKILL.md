---
name: type-driven
description: 'Use when modeling a domain, encoding a state machine, hardening APIs, making invalid states unrepresentable, or parsing instead of validating. Not for TypeScript: use typescript-best-practices.'
---

# Making invalid states unbuildable

Domain mistakes should fail at compile time, not in production. This skill encodes the domain as types, parses untrusted input once at the boundary, and matches state transitions exhaustively.

It fits modeling a domain, encoding a state machine, hardening an API boundary, making invalid states unrepresentable, or parsing instead of validating. For TypeScript style and strictness specifics, use typescript-best-practices instead. Skip this approach entirely and report when the language lacks sum types (ADTs, sealed hierarchies, or an equivalent). Per-language constructor and check commands live in references/patterns.md, with worked constructors in references/examples.md and dependent-type background in references/formal-tools.md.

## Work from the domain inward

1. State the domain in one paragraph. List all valid states, all invalid states, and every operation with preconditions and postconditions. Mark partial operations as partial.
2. Design types first, before bodies. For each invalid state, choose a compiler-enforced shape (ADTs, phantom types, branded types, newtype wrappers, sealed hierarchies, opaque types, whichever the language supports). Leave bodies unwritten until all types compile and every invalid state is unrepresentable.
3. Parse at every untrusted edge. External data, deserialization, FFI, and user input each get a `parse` constructor returning the new type. Never return `bool` and defer validity to callers. No scattered post-hoc validation remains outside the parse layer.
4. Encode state machine transitions as exhaustive `match`/`switch`/`visit` over the sum type. Treat incomplete-arm warnings as failures. Add the missing variant to the type; never add a wildcard arm to silence the checker, and never add runtime guards to cover a type-design failure.
5. Run the language strict type checker and exhaustiveness check, then the full target build. When the checker reports an illegal state is still representable, fix the type design rather than the implementation. Complete or remove every hole (`todo!()`, `any` casts, `TODO()`, `...` bodies, and equivalents in references/patterns.md) before proceeding.

Local reversible writes only: domain types, public signatures, and affected callers and tests, with rollback through version control or undo. No remote mutation. Finished work means every algebraic constructor is present, invalid states are unconstructible, matches are exhaustive, boundaries parse, and the target build passes.
