---
name: contract-driven
description: 'Use when crossing a public API boundary, guarding complex invariants, or hardening untrusted input or integration seams. Not for remote or irreversible changes.'
---

# Contract-driven

Put explicit, testable guarantees at the boundary where two pieces of code meet, so bad input and bad state fail loudly at the edge instead of corrupting the interior. Use this whenever you cross a public API boundary, guard a complex invariant, or harden untrusted input and integration seams. It does not cover remote or irreversible changes: everything you write is local types, assertions, validators, and tests at the boundary, and rollback is deleting the added code or reverting the boundary change.

## What you need before you start

You need the requirements or specification for the operation being contracted, and the target source file or module holding the boundary, invariant, or untrusted seam. Existing tests that must keep passing come along when there are any. If a requirement you need is missing, stop and report it; never invent contracts or widen scope to fill the gap.

## Name every contract before coding

Extract PRE, POST, and INV conditions from the requirements and give each one an ID plus a one-line description, for example PRE-1: amount > 0, POST-1: balance == old(balance) - amount, INV-1: balance >= 0. Do not write any implementation until every planned contract has its ID. Drop any contract that merely restates the implementation (ensures(result == x - y) on a subtract function is contract fatigue, not a guarantee). Language-specific annotation shapes live in `references/examples.md`, and the library or idiom to express them in each stack lives in `references/libraries.md`.

## Enforce each contract at the strongest layer that can hold it

Prefer static over runtime. Size, alignment, null and type safety, and exhaustiveness belong in the static type system or static_assert; expensive O(n)+ properties belong in test assertions; internal invariants belong in debug-only checks; public API input, and always external or untrusted input, gets active runtime guards. If a property can be verified statically, do not add a runtime contract for it. Every runtime contract you add must actually run: never ship one compiled out or disabled, and never disable one to make a build pass.

When the surface is an HTTP API that returns errors, use one error shape everywhere: a machine-readable code, a human-readable message, and optional details. Map invalid client data to 400, unauthenticated to 401, unauthorized to 403, a missing resource to 404, conflict or version mismatch to 409, semantically invalid input to 422, and server failure to 500 with no internal detail. Never mix throwing, null returns, and error envelopes on one surface.

## If the enforcement point moves, re-cover every entry

Relocating a guard or narrowing an adapter re-opens the boundary, so treat the move as the risky part. Enumerate every entry that reached the protected region through the old point, including callbacks, retries, forks, resume and replay paths, and test entries; record coverage or a justified exemption for each and exercise newly covered entries directly. When an adapter narrows arguments, inventory every source field and state whether it is carried, explicitly refused, or genuinely irrelevant; a handwritten list is not automatic coverage for future fields. When validation moves earlier, preserve its applicability conditions, observable check order, and established error contract, and leave a check at the later boundary when the required early state is unavailable there. When registry keys or path representations change, use one explicit identity contract across registration, lookup, move, deletion, and busy checks, preserving public representations unless their change is authorized. For Windows paths, distinguish operational namespace paths from comparison representations and settle drive, UNC, symlink, case, and filesystem-identity semantics before normalizing; never use naive prefix containment or universal lowercasing. For provider or model migrations, keep stable identifiers, display labels, credential scope, and actual request fields separate: trace rejected fields through the current schema and request builder and prove the intended request difference offline before proposing any live call. None of this authorizes credential changes, retries, uploads, or paid services.

## Prove the boundary two ways

First, the code must compile: run the type checker, static analysis, and build with all contracts in place, and fix the contract or the implementation when they fail. Second, write one violation test per PRE, POST, and INV proving the boundary fails explicitly on bad input or bad state. Static contracts are proven by the type checker; runtime contracts by violation tests. A violation test that does not fire means the contract is not enforced at the chosen layer: re-select the layer or strengthen the check, never delete the test to get green.

## What you leave behind

Local code with every planned PRE/POST/INV implemented at its verification layer and active where runtime, one passing violation test per contract, and each contract traceable to its requirement by ID. Violations fail explicitly at the boundary.
