---
name: typescript-best-practices
description: 'Use when TypeScript needs shaping toward narrow types, unions, exhaustive variants, and strict flags. Not for error repair: use typescript-type-hardening. Not for non-TS domains: use type-driven.'
---

# TypeScript best practices

You shape TypeScript source proactively so bad states cannot be written: narrow types, discriminated unions, readonly where mutation is forbidden, validated boundaries, and the strict flags actually turned on. This is a shaping pass, not a repair job. A concrete error report (a message, a broken inference, a generic that will not constrain) belongs to typescript-type-hardening, and language-agnostic domain modeling belongs to type-driven.

This stays local and reversible: you touch only the in-scope TypeScript files and the named `tsconfig.json`, rolled back through version control. You never touch remote state.

What you need before starting: the in-scope TypeScript source files and the target `tsconfig.json`. The scope must name a proactive shaping pass. A concrete error report routes to typescript-type-hardening instead.

Limits that hold for the whole pass:

- No new `any`, `!` non-null assertions, or `as unknown as` double assertions.
- No invented strict flags beyond the TypeScript 7 set named below.
- No blanket ban on branded types or `as`. Use an opaque type where the domain identity invariant is real and enforced, and use `as` where TypeScript narrowing is insufficient, stating the reason each time.
- No unvalidated external shape shipped or re-exported without a validating boundary.

## Read the scope first

Read every in-scope file before changing any of them. You are done with this step when all of them have been read.

## Turn on the strict set

Check the project `tsconfig.json` for exactly this set and apply what is missing:

- `noUncheckedIndexedAccess`
- `exactOptionalPropertyTypes`
- `noImplicitOverride`
- `noFallthroughCasesInSwitch`
- `noPropertyAccessFromIndexSignature`
- `noImplicitReturns`
- `allowUnreachableCode: false`
- `verbatimModuleSyntax`
- `erasableSyntaxOnly`
- `isolatedDeclarations`

Use only these flags. If a check fails for a missing flag, the recovery is applying the named flag, with version control as the rollback.

## Shape the types toward narrow and explicit

Keep `unknown` only while it is genuinely opaque, and narrow it at trust boundaries with guards, predicates, or an explicit cast where narrowing is available. Model state machines and mutually exclusive variants as discriminated unions. Mark properties `readonly` where reassignment is forbidden. Add an opaque type for domain identity only where the invariant it models is real and enforced.

## Validate every boundary and match the runtime

Put a validating parser (Zod 4, Valibot, or ArkType through the Standard Schema interface) on every trust boundary where untrusted external input enters. Never widen or re-export an unvalidated external shape past that boundary. Set module resolution to `NodeNext` for Node.js targets and `ESNext` with a bundler for SPAs.

## Prove it with the compiler

Run `tsc --noEmit` and confirm it passes. Confirm the pass introduced no `any`, `!`, or `as unknown as`. Confirm every discriminated union is exhaustively checked through the compiler's switch and match checks, adding a final otherwise branch that narrows the unknown variant to `never` where the language lacks built-in exhaustiveness.

When this step fails, the cause is one of a short list. Report it plainly and stop rather than working around it:

- A type that cannot be narrowed: report it and stop. Do not widen scope or add a placeholder cast.
- A domain with no natural discriminant: propose a tag field, and stop if the domain does not support one. Do not force a union that does not fit.
- A validation library that is unavailable: state the missing constraint and stop. Do not ship the shape unvalidated.

## What you hand back

The shaped source and `tsconfig.json`, with a clean `tsc --noEmit` run as proof: illegal states unrepresentable, variants exhaustive, boundaries validated, and none of the refused constructs introduced.
