# Dependent type systems and verification tools

| Tool | Strength | Status |
|------|----------|--------|
| Idris 2 | Dependent types, totality checking, proof terms | Academic, niche production use |
| F* | Refinement types, effects, proof automation | Research (Microsoft), used in Project Everest |
| Agda | Dependently typed, cubical type theory | Academic |
| Refined (Haskell) | Refinement predicates checked at construction | Production-ready |

## Practical guidance

- Idris 2: A practical learning path for dependent types. For functions checked as total, the totality checker verifies they cover all inputs. Proof terms enable machine-checked correctness.
- **F\***: Used to verify real cryptographic code (HACL*, EverCrypt). Refinement types add predicates to existing types without full dependent type overhead.
- Agda: Theoretical foundation includes cubical type theory. Primarily academic but influences practical language design.
- Refined (Haskell): Pragmatic predicates checked at construction. `Refined Positive Int` checks the value when built, with Template Haskell support for compile-time literals.
