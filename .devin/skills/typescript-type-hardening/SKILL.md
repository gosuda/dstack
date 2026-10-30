---
name: typescript-type-hardening
description: 'Use when TypeScript has type errors, failing inference, or needs type mechanism repair (generics, infer, mapped, branded). Not for strict flags or proactive shaping: use typescript-best-practices.'
---

# TypeScript type hardening

You repair a concrete TypeScript type problem: an error message, an `any` to eliminate, a generic that will not constrain, a branded type to design, an inference chain that breaks. A proactive shaping pass with no error report belongs to typescript-best-practices, and creating or fixing `tsconfig.json` strict flags belongs there too. This skill never creates or modifies `tsconfig.json`.

This stays local and reversible: you edit only the named TypeScript source and type-test files, rolled back through version control. You run `tsc` as the proof. You never touch remote state.

What you need before starting:

- Target TypeScript file or directory. Required.
- `tsconfig.json` path. Required, and it must already exist. If it is missing, stop and report it. Creating it is the job of typescript-best-practices or the project setup.
- The specific type problem: the error message, the desired generic shape, or the branded type contract. Required.
- Existing type tests, if you are extending coverage. Optional.

## Record the baseline before touching anything

Run `tsc --noEmit` and capture the full error output before any edit. If the baseline already carries errors unrelated to your target, run a scoped `tsc --noEmit` over the target files as well, and keep both lists. You are done when the exact baseline is recorded, because every later claim of "no new errors" is measured against it. When the baseline is dirty with unrelated errors, Done is relative to the scoped baseline, and you report the pre-existing errors separately.

## Apply the narrowest mechanism for each item

Classify each error or requested improvement into one of these mechanism classes, then apply the narrowest fix in that class. Never widen a type to silence an error (never fall back to `object` or `{}` as a stand-in, never loosen a constraint to make the message go away).

- Missing annotation or `any` elimination: add explicit annotations. Replace `any` with `unknown`, then narrow with guards, discriminated unions, or assertion functions.
- Incorrect narrowing: fix tags, `typeof` / `in` / `instanceof` guards, assertion functions, or control flow, with `never` checks for exhaustiveness in switch or default branches.
- Generic design: add type parameters with explicit `extends` constraints. Use defaults only when the consumer should not supply them. Prefer `const` type parameters (TS 5.0+) for literal inference.
- Conditional or infer extraction: branch with `T extends U ? X : Y`. Extract with `infer R` inside `extends` clauses (arrays, promises, return types, tuple positions), chaining `infer` for nested extraction.
- Mapped or template-literal transform: reshape with `{ [K in keyof T]: ... }`. Remap string keys with template literals plus `Uppercase`, `Lowercase`, `Capitalize`, or `Uncapitalize`.
- Branded or opaque types: build with `declare const __brand: unique symbol` and `type Branded<T, B> = T & { readonly [__brand]: B }`. Provide constructor and guard helpers, and never expose the raw intersection.
- Utility-type derivation: compose from `Partial`, `Required`, `Pick`, `Omit`, `Record`, `Readonly`, `ReturnType`, `Parameters`, `InstanceType`, and `Awaited`. For recursive structures, use conditional types with `infer` and recursive references.
- Function overloads: write one signature per call pattern with the implementation signature last on a union parameter type. Every overload must be assignable to the implementation.
- Builder-pattern typing: chain generics (for example `Builder<Step>`) with branded step types or literal parameters so each method returns a builder limited to valid next steps.
- Array or index access: take element types with `T[number]`. Use `as const` or `satisfies` for readonly tuple inference and variadic tuples (`[...T, U]`) for push or prepend.
- Deep inference: recurse with conditional types for nested structures, bounding depth with a counter parameter so you do not hit instantiation-depth errors.

After each individual edit, re-run `tsc --noEmit` scoped to the changed files. If the edit adds errors outside the recorded baseline, revert it and try a narrower fix.

## Cover each mechanism with type tests

For every mechanism you applied, write or update type-test files with a positive case (the accepted shape now compiles: the narrowed type, the constraining generic, the branded value admitted, the derived utility shape) and a negative case with `// @ts-expect-error` proving the rejected shape fails (the `any` source, the unbranded value, the wrong generic argument).

## Run the full pass and report it

Run `tsc --noEmit` on the full project. Confirm zero new errors against the recorded baseline, confirm all consuming call sites of the changed types still compile (updating call sites to the new contract rather than weakening the type), and confirm zero new `any` by a defined detection rule: compiler-level diagnostics such as `noImplicitAny` output, or an AST scan for `: any`, `as any`, and `<any>`. A three-pattern textual grep is not sufficient; use the compiler or a real parser.

Report in this order: baseline count, final count, `any` eliminated, mechanisms applied, scoped per-edit run status, full-project run status. When the work cannot proceed, say so directly:

- A mechanism that fails: revert the edit and report the exact error, what was tried, and why it did not resolve.
- Call-site breakage outside your scope: revert and report which sites broke and what contract change they need, then wait for scope approval.
- Instantiation depth exceeded: simplify toward a depth-limited recursion with a counter generic. If the structure genuinely needs deep recursion, report the limit and propose a runtime fallback.

## What you hand back

Modified source files, type-test files with positive and `// @ts-expect-error` negative cases, and a terminal report ordered baseline count, final count, `any` eliminated, mechanisms applied, and both tsc statuses (scoped per edit, then full project).
