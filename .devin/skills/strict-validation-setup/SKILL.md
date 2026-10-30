---
name: strict-validation-setup
description: 'Use when a user invokes a strict-mode validation or verifiable-goals loop setup. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Strict validation setup

A user goal becomes a strict tooling config, a per-task GOALS.md scaffold with observable criteria, and one deliberately failing test per criterion. Everything lands as a single atomic, reversible local write set. Config-only or GOALS-only partial results never satisfy this skill, and project-wide commands never run here. The run ends after one verification pass. It does not stay resident.

Nothing in this skill touches remotes, credentials, deployed state, or irreversible changes. Rollback is version control.

## Refusals that stop the run before writing

| Condition | Behavior |
|---|---|
| `no-supported-manifest` | Name the supported manifests. Write nothing. |
| `multiple-ecosystems` | Name all detected primary manifests. Require one explicit project scope. Write nothing. |
| `unsupported-ecosystem` | Name the detected ecosystem and stop without a false reference claim. C++, Java, Kotlin, Spring Boot, Nest-specific, and React-specific setups are unsupported. |
| `config-conflict` | Name the path, key, current value, and required value. Require explicit overwrite authorization naming that key. |
| `config-shape-unsupported` | Name the manifest or config shape that cannot merge without a partial or destructive rewrite. Write nothing. |
| `goal-not-observable` | Ask for the missing observable outcome before writing. |
| `test-framework-missing` | Name the supported frameworks for the ecosystem. Add no dependencies or generic tests. |
| `task-test-location-unsupported` | Explain why the existing runner cannot execute `.agent-tasks/<id>/tests`. Write nothing rather than claim failing tests are in place. |
| `agents-task-content` | Name the task-specific AGENTS.md lines. Write nothing until the user chooses how to separate them. |
| `task-path-conflict` | Name each unrelated or conflicting task file. Overwrite nothing. |
| `write-failed` | Restore every prior target byte for byte and remove only newly created files. |
| `verification-mismatch` | Restore the complete write set. Report expected and actual path or key, or expected and actual criterion. |

## What the run needs

The user goal is required, and it must carry enough observable behavior to derive at least one pass or fail criterion. Without that, stop and ask for the missing outcome.

The task ID is optional. When absent, derive it as `task-` plus the first 12 lowercase hexadecimal characters of SHA-256 over the exact UTF-8 goal text. A supplied ID must match `^[a-z0-9][a-z0-9-]{0,63}$`. Overwrite authorization is optional and narrow: it permits replacing one named conflicting non-strict config value, never unrelated configuration or whole files. The project root is required and must contain exactly one supported primary ecosystem. TypeScript counts with `package.json` alongside as one ecosystem.

This skill reads or creates `AGENTS.md` for a single purpose: ensuring one stable pointer line, `Per-task goals live in .agent-tasks/<task-id>/GOALS.md.` Task-specific criteria never go there. `CLAUDE.md` is never read or edited.

## Detect the ecosystem, merge its strict config

Detect exactly one supported primary ecosystem at the project root. TypeScript comes from `tsconfig.json`. Python comes from `pyproject.toml`. Rust comes from `Cargo.toml`. Go comes from `go.mod`. OCaml comes from `dune-project` or a root `*.opam` file. Treat `package.json` without `tsconfig.json` as unsupported JavaScript, not TypeScript.

Zero or several primary ecosystems stops the run before any write, with the exact manifests reported.

Load `references/<ecosystem>.md` (`typescript.md`, `python.md`, `rust.md`, `go.md`, or `ocaml.md`) for the exact config keys, values, and merge shape. Parse the existing config format instead of appending text blindly. Preserve unrelated keys and formatting wherever the parser or editor permits. A required key already at its required value stays untouched. A missing key gets inserted. A conflicting value is `config-conflict` unless overwrite authorization names that key.

## Point AGENTS.md at the task, derive criteria, scaffold GOALS.md

Read `AGENTS.md` when it exists. Create it with the single pointer line when absent. Leave an equivalent stable pointer unchanged. Stop with `agents-task-content`, naming the lines, when it holds task-specific goals or success criteria. Never move or delete those lines without explicit user direction.

Translate the goal into the smallest ordered list of observable criteria, each identified by a meaningful slug and stated by its observable purpose. Coded labels such as `SC-01` or `SC-02`, phase-and-counter prefixes, and parenthesized IDs are forbidden as human labels; criteria and headings name their actual purpose directly with no decorative prefix. Each criterion names an input or setup, an observable behavior, and an expected result. Subjective, circular, and implementation-only criteria are out.

Settle on one existing project test framework before scaffolding. TypeScript supports `vitest`, `jest`, or `node:test`. Python supports `pytest` or `unittest`. Rust and Go use their built-in harnesses. OCaml supports `alcotest`, `ounit2`, or Dune cram tests. Infer the framework only from existing manifest dependencies, configuration, or existing tests.

Create `.agent-tasks/<task-id>/GOALS.md` with no placeholders:

```markdown
# <task-id>

## Goal
<exact user goal>

## Success criteria
- [ ] <observable criterion purpose>
- [ ] <observable criterion purpose, if any>

## Verification
- <meaningful-slug>: `.agent-tasks/<task-id>/tests/<meaningful-slug>.<language extension>`, `<existing targeted test command>`
- <meaningful-slug>: `.agent-tasks/<task-id>/tests/<meaningful-slug>.<language extension>`, `<existing targeted test command>`

## Boundaries
- Project-stable rules remain in project configuration.
- Task-specific goals and criteria remain under `.agent-tasks/<task-id>/`.
```

Substitute every angle-bracket form with its resolved value and emit only as many criterion and verification lines as exist. Success criteria state observable purpose directly, and verification lines map each meaningful slug to its test file without decorative coded prefixes. Preserve the user goal verbatim under Goal. Never mention or point from AGENTS.md.

## Write one failing test per criterion, commit atomically, verify once

Each test file is named with a meaningful slug reflecting the criterion purpose instead of `sc-01.*`, joined to the framework extension. Test names state the actual criterion purpose directly without `SC-NN:` prefixes or decorative codes. The deliberate failure executes unconditionally when that test runs. Task implementation replaces it later. Skip, xfail, todo, `pass`, empty bodies, and generic assertions never count.

Per-framework patterns:

- TypeScript with Vitest: `import { expect, test } from "vitest"; test("criterion purpose", () => { expect.fail("Unmet: criterion purpose"); });`. Jest: `test("criterion purpose", () => { throw new Error("Unmet: criterion purpose"); });`. `node:test`: `import test from "node:test"; test("criterion purpose", () => { throw new Error("Unmet: criterion purpose"); });`. Use `<slug>.test.ts` for Vitest and Jest, and for `node:test` only when the existing runner transpiles TypeScript. Otherwise use `<slug>.test.mjs`.
- Python pytest: `def test_<slug>() -> None:\n    raise AssertionError("Unmet: criterion purpose")`. unittest: a `unittest.TestCase` method named `test_<slug>` calling `self.fail("Unmet: criterion purpose")`. Use `test_<slug>.py`.
- Rust: `<slug>.rs` with `#[test]\nfn <slug>() { panic!("Unmet: criterion purpose"); }`, placed under `.agent-tasks/<task-id>/tests/`. Without a project mechanism compiling tests from that directory, stop with `task-test-location-unsupported`.
- Go: `<slug>_test.go` in package `tests` only when the existing module and test command include `.agent-tasks`. Otherwise stop with `task-test-location-unsupported`. Body: `func Test<SlugCamel>(t *testing.T) { t.Fatal("Unmet: criterion purpose") }`.
- OCaml Alcotest: a case calling `Alcotest.fail "Unmet: criterion purpose"`. OUnit2: `assert_failure "Unmet: criterion purpose"`. Cram: `<slug>.t` with the established project command followed by an intentionally mismatched expected output line `[Unmet: criterion purpose]`. Require an existing Dune stanza or cram directory rule. Otherwise stop with `task-test-location-unsupported`.

Escape criterion text per the target language string-literal rules.

Retain exact bytes of every existing target config, GOALS file, and criterion-test path before changing files. Refuse a task directory containing unrelated files that would be overwritten. Apply the config merge, GOALS.md, and all tests as one reversible set. Any write failure restores prior bytes and removes only files created by this run.

Verify the frozen result a single time. Parse the written config and require every strict key and value from the merge step. Recompute the merge and require byte-identical output. Re-read GOALS.md and require the exact layout, goal, criteria, and test links. Re-read every test and require its meaningful slug identity, quoted criterion purpose, and unconditional deliberate failure. Confirm `AGENTS.md` carries the stable pointer with no task-specific content from this run, and confirm this run never read or modified `CLAUDE.md`. Then stop.

## What exists afterward

The ecosystem strict config merged idempotently at its exact path. `AGENTS.md` holds the stable GOALS.md pointer and no task-specific criteria. `.agent-tasks/<task-id>/GOALS.md` holds the complete goal, observable criteria, and test links. `.agent-tasks/<task-id>/tests/` holds one executable, deliberately failing test per criterion. No `CLAUDE.md`, support reference, compatibility alias, or unlisted file gets created.
