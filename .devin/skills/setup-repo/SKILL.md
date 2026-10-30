---
name: setup-repo
description: 'Use when the user asks to set up a repository: deterministic gitignore, repository-native pre-commit hooks, or REVIEW.md and CONTRIBUTE.md rules that enforce anti-slop, anti-spaghetti, and offensive-minimalism defaults. Single owner for repository setup, superseding earlier setup-* skills. Not for one-off code reviews, PR feedback, or general documentation.'
---

# Set up a repository natively

Set up the repository so clean defaults are enforced by construction: ignored paths are deterministic, pre-commit hooks execute native gates, and review and contribution rules keep code anti-slop, anti-spaghetti, and offensively minimal. Respect module boundaries and declared interfaces. Prove that each check rejects a real violation. Read the repository before choosing tools, and reuse what it declares.

This skill owns ignore setup, hook setup, and review rule setup together as one coherent repository setup, superseding earlier setup-* skills. It installs no global command interceptor; protection comes from the repository's own hook running its own gates.

## Stay inside the repository and keep every write reversible

Work only inside the repository the user names, resolved with `git rev-parse --show-toplevel`, and make that root the working directory for everything below. When no repository is found, stop and say so with nothing written.

Writes are reversible and local only: the repository `.gitignore`, hook configuration plus whatever manifest, lockfile, or effective pre-commit hook entry (resolved from `core.hooksPath` or local `.git/hooks/pre-commit`) the chosen manager or native script needs, and exactly the requested policy files `REVIEW.md` and `CONTRIBUTE.md` under the repository root. Reject any policy target outside that root with no mutation, and never substitute `CONTRIBUTING.md` or any other filename.

Preserve existing configuration and user data. Merge into what is there; never clobber grounded rules, legal notices, AI contribution policies, or user owned sections. Preview every genuinely destructive, data touching, remote, or install consequence with its exact target and proceed only with explicit approval for that write. Never make blanket global changes. Ask before replacing a live hook or changing any global or outside-repo installation not already authorized.

Read representative source before deciding: sample the code the rules will govern, trace at least one consumer path per touched surface, and cover build and test configuration, declared gates and CI checks, architecture and data boundaries, and existing policy. Record every file actually read. Never rest a rule on directory layout alone, never derive a gate command the repository does not declare, and never weaken or disable a check to get green.

## Enforce clean defaults by construction

Configure the repository so its structure, code, and interfaces remain clean by construction under three non-negotiable defaults:

First, enforce anti-slop defaults. Code must contain no dead code, unreferenced exports, commented-out blocks, placeholder or TODO residue, temporary debug logging, or duplicate implementations of the same behavior. Ground every anti-slop rule in evidence read directly from the repository, such as declared compiler warning flags for unused symbols, linter rules prohibiting console statements or debugger calls, or dead-code elimination settings. Wire checks only to commands the repository already declares, such as `cargo check`, `go vet`, `tsc --noEmit`, or declared linter suites. Never invent new linters or tools that the repository manifests do not already declare.

Second, enforce anti-spaghetti defaults. Module boundaries must be explicit, dependencies must remain strictly acyclic, and directory depth and breadth must mirror genuine domain boundaries rather than empty pass-through layers, folder-per-class habits, or artificial indirection. Ground boundary rules in the repository's established package layout, workspace member definitions, internal visibility declarations like Rust's `pub(crate)` or Go's `internal/` packages, and declared import paths. Check module boundaries using the repository's declared build topology, package dependency checks, or architecture rules that the project's own toolchain can run.

Third, enforce offensive minimalism defaults. Superseded logic, obsolete paths, compatibility shims, and deprecation aliases must be excised cleanly rather than preserved alongside new code. Every change must implement the smallest design that fully satisfies the stated requirement, with zero speculative abstraction, premature generalization, or unrequested framework scaffolding. Ground minimalism rules in evidence read from active caller paths and consumer call sites across the tree, proving that every consumer migrated cleanly. Verify clean cutovers using the repository's declared compiler and test suites, ensuring that removing an obsolete entry point produces clean passes across all remaining callers with no lingering references.

## Shape the ignore file deterministically

Detect language template keys from regular files at repository relative depth 0 through 2, excluding `.git/`, applying every matching row below, deduplicating, and sorting lexicographically. An empty result is valid and means no network template is requested.

| Evidence filename | gitignore.io key |
|---|---|
| `tsconfig.json`, `tsconfig.*.json` | `node` |
| `package.json` | `node` |
| `pyproject.toml`, `requirements.txt`, `setup.py`, `setup.cfg`, `Pipfile` | `python` |
| `Cargo.toml` | `rust` |
| `go.mod` | `go` |
| `dune-project`, `dune`, `*.opam` | `ocaml` |
| `pom.xml`, `build.gradle`, `build.gradle.kts` | `java` |
| `settings.gradle.kts` with Kotlin source files | `java,kotlin` |
| `CMakeLists.txt` | `cmake,c++` |
| `Gemfile`, `*.gemspec` | `ruby` |
| `composer.json` | `composer` |

Capture the current state first: the exact `git status --short --untracked-files=all` entries beginning `?? ` excluding `.gitignore`, with before and after counts reported at the end. When a `.gitignore` already exists, read its exact bytes and copy it to `/tmp/gitignore-snapshot-<UTC-YYYYMMDDTHHMMSSZ>.bak` before modifying it; when that snapshot fails, stop without writing.

Group the untracked paths by top level directory, grouping root files by lowercase extension with extensionless root files as `(no extension)`, show every path in each group, and ask the user which exact directory (`name/`) or extension (`*.ext`) patterns to add. Normalize confirmed patterns to repository relative slash form, reject `..`, absolute paths, and patterns matching `.gitignore` itself, then sort and deduplicate. The user declining empirical additions yields an empty empirical block, never cancellation of the rest.

When the key list is non-empty, fetch `https://www.toptal.com/developers/gitignore/api/<comma-separated-keys>` with `curl -sf --max-time 10`, using the response verbatim after normalizing line endings to LF and stripping trailing blank lines. When the request fails, report the keys with the network error and stop leaving `.gitignore` unchanged; there is no silent fallback. An empty key list means an empty language block with no request.

Assemble four managed sections in this exact order, each opened by its exact anchor line followed by its normalized body and one blank line except the final block.

| Order | Anchor | Body |
|---|---|---|
| 1 | `# === LANGUAGE TEMPLATES ===` | The fetched body, or empty |
| 2 | `# === AI TOOLING ===` | `.claude/settings.local.json`, `.cursor/`, `.windsurf/`, `.aider.chat.history.md`, `.aider.input.history` |
| 3 | `# === IDE / EDITOR ===` | `.idea/`, `.vscode/*` plus the four `!.vscode/extensions.json`, `settings.json`, `tasks.json`, `launch.json` keeps, `*.swp`, `*.swo`, `*~`, `.DS_Store`, `Thumbs.db` |
| 4 | `# === EMPIRICAL ===` | The confirmed patterns, one per line |

A non-comment, non-blank pattern line duplicates when its exact trimmed text already appeared in preserved user content or an earlier managed section; first occurrence wins, and API supplied comment lines are preserved.

Merge without touching user content: with no existing file the candidate is the four sections; otherwise require each of the four exact anchor lines to occur zero or one time, replace each existing managed block from its anchor through the line before the next managed anchor, append missing blocks in canonical order, preserve all other bytes exactly, normalize only generated blocks to LF, and end with exactly one terminal newline.

Show the complete before and candidate diff with any available local renderer and write the candidate atomically to the repository root `.gitignore` only on approval; on decline leave the file unchanged. Then re-run detection, fetch, build, and merge in memory against the new bytes with the same confirmed empirical inputs and require a byte identical second candidate, otherwise restore the snapshot (or remove a newly created file) and report the second pass diff. Recount untracked entries with the same command and report both counts plus every remaining path.

## Wire one hook manager or native hook to the repository's own gates

Inventory the repository manifests, lockfiles, declared gate scripts, hook configuration, and the effective pre-commit hook path. Check effective `core.hooksPath` (via `git config --get core.hooksPath` or local repository config) alongside `.git/hooks/pre-commit` so existing custom or shared hooks are never silently replaced. Note existing package managers and toolchain manifests: `package-lock.json`, `pnpm-lock.yaml`, `bun.lock`, legacy `bun.lockb`, `yarn.lock`, `uv.lock`, `poetry.lock`, `Pipfile.lock`, `go.mod`, `Cargo.toml`, and `dune-project`. When an existing native pre-commit hook (such as an executable shell script in the effective hooks directory) already functions and directly executes the repository's declared gates, keep that native functioning hook; do not install or force an external hook manager when no manager is needed. When one hook manager already exists, extend it; when several managers could fire on the same commit, stop and report every firing path with the smallest clean cutover, removing nothing observable without the user's approval. Ask before replacing any live hook or changing any configuration outside the repository.

When no functioning hook exists and a manager is required, make detection authoritative: reuse the existing package manager, manager toolchain, checker versions, and actual declared commands. Pick the smallest native manager matching repository evidence (e.g. Lefthook for pnpm, Bun, or Go projects; prek for Python, Rust, or OCaml; or the manager already present in manifests or task runners), asking the user only when two choices remain equally supported. Install through the current project toolchain locally only (e.g. `pnpm add -D lefthook && pnpm exec lefthook install` in a pnpm repository, `bun add -d lefthook && bun x lefthook install` in a Bun repository, local dev-dependencies in Cargo/npm/etc.). Never introduce a second package manager (e.g. no pnpm in a Bun repo). Never execute hidden global installations (`go install ...@latest`, `uv tool install ...`) that alter environments outside the repository root. Never introduce ESLint, Prettier, Biome, Ruff, Pyright, Black, isort, mypy, or any formatter, linter, or type checker the repository did not already declare; no language-wide command bundle is injected blindly (no Biome on Go/Rust or undeclared JS/TS, no Ruff/Pyright on Python unless declared). Where a fresh repository genuinely lacks checks, propose the smallest suitable native stack to the user and declare dependencies, configuration, and lockfile changes explicitly before using them; retain the user's authorized setup scope, and never invent pins or thresholds.

Configure only commands the repository can execute and actually declares in its manifests, scripts, `Makefile`, `justfile`, or toolchains, reusing existing checker versions and invocations: with `pass_filenames: false` on whole repository commands and parallel independent read only checks only where their tools do not edit the same files. Hook wiring strictly mirrors declared gates: run the repository's declared test, lint, format-check, and type-check scripts (e.g. the declared `npm test` / `bun run check`, `cargo test`, `go test ./...`, `dune runtest`), preserving declared flags. If the repository declares only tests, wire only tests; if it declares a linter or formatter, reuse that specific declared tool with its existing configuration. Include the declared strict checks, complexity limits, and dependency boundaries the repository already states; never invent pins or thresholds.

Run the hook's all-files entry point, such as `lefthook run pre-commit`, `prek run --all-files`, or the native hook script. If a declared formatter changes files, inspect its changes and repeat until the check passes without edits.

Prove enforcement without creating history. Introduce one temporary, reversible violation of a declared check in an owned scratch file that the hook includes. Use a syntax error, type violation, or lint defect covered by that check. Require a nonzero exit or an automatic repair with an observed diff. Restore the scratch file and require a clean pass. If no safe injection is possible, or the check only examines committed history, report proof unavailable. A successful run or a harmless blank-line change does not prove enforcement. Keep the check unchanged during the probe.

Confirm that one executable pre-commit entry remains at the effective hook path, `core.hooksPath` or `.git/hooks/pre-commit`. It must delegate to the native script or chosen manager. Confirm that the worktree matches its pre-probe state. Commit only when the user separately asks.

## Write review and contribution rules from evidence

Read the existing `REVIEW.md` and `CONTRIBUTE.md` when present alongside the source, consumer, configuration, gate, boundary, and policy evidence above. Admit a candidate rule only when it states a material repository specific invariant a future reader must obey, grounded in a file actually read or explicitly tagged human supplied; reject templates, universal stack claims, and anything derivable by reading the repository. Write a file only when admitted invariants justify it; when none exist, write neither file and say so.

Merge admitted rules into each existing target without clobbering: keep grounded rules, legal notices, and AI contribution policies intact, flag direct conflicts to the user instead of overwriting, and create no unrequested third policy file.

Hold `REVIEW.md` to evidence backed, firm review in natural human prose with no scaffolding. Every finding names the actual bug or invariant violation, the affected consumer and its consequence, the code path, quoted evidence, and severity in plain semantic words. Enforce clean defaults directly in review: flag slop defects including dead code, commented-out blocks, placeholder or TODO residue, debug statements, and duplicate logic; flag spaghetti defects including breached module boundaries, circular dependencies, and vacuous pass-through layers; and flag non-minimal additions including compatibility shims, deprecation aliases, and speculative abstractions where a clean cutover was required. Tie each finding to a check or test the repository can run. Proof is a powerful test that fails on the fault, with reusable inputs allowed and saved output pins and source text assertions rejected; weak tests are never admitted under any circumstances. Never weaken a lint or drop proof for a line-count or percentage goal, and never flag a load-bearing clause identifier, evidence row, or measured fact its consumer still needs as redundant. No fabricated findings, no unearned approval, no filler. The tone is direct and firm, attacking defects and never people.

Hold `CONTRIBUTE.md` to clean contract first contributions that keep the repository natively anti slop, anti spaghetti, and minimal by replacement rather than accretion. Every change migrates all its callers and leaves no obsolete path, shim, alias, or deprecated route. Code reads through names, types, and control flow with no comment crutches and no commented out code, keeping only the narrow evidence floor: a minimum SAFETY comment where an actual unsafe block would otherwise fail undocumented_unsafe_blocks, a necessary public rustdoc or module invariant with no equivalent type or contract home yet, and a load-bearing clause identifier, evidence row, or measured fact its consumer still needs. Tests are invariant or adversarial oracles, each detecting a distinct plausible fault, never weak coverage padding. No unnecessary docs, plans, specs, or ADRs accompany a change. Names are always semantic; opaque codes, numbers, and sequence prefixes are rejected, except a genuine externally fixed clause identifier which stays with a human label. No defers, stubs, placeholders, or excuses ship. Stated authority, security, and data boundaries stand, with no implicit publish or deploy step. No blanket permission for documentation comments, and no invented lint requirements.

Re-read each written file and verify every rule against all of the above, removing any rule that lacks grounding, restates repository derivable fact, or depends on a private anchor list or peer runtime. Write no generated manifests, registries, or YAML.

## Stop instead of pushing through

Stop with nothing further mutated and a plain `blocked` report naming the exact cause and what was left untouched or restored: an unresolvable repository root or an out of repository target; no grounded repository specific invariants; a conflicting existing rule, leaving the conflicted region unchanged; a failed snapshot, unreachable template source, rejected empirical pattern, duplicated or out of order managed anchors, declined write, failed write with the snapshot restored or partial file removed, or a non-identical second candidate; missing repository native gates; competing hook managers; an install failure with manifest, lockfile, hook config, and hook entry restored from baseline; a probe that does not trip, meaning the hook is not load bearing (or proof was unavailable because no safe defect could be injected, where a green normal run alone never counts as proof of enforcement); leftover probe residue, restoring the scratch path first; or a write or verification failure with pre-write contents restored where possible. When a probe fails, tell hook wiring faults (the hook did not fire, fired the wrong command, or missed the file, fixed here) apart from check content faults (the check reported a real issue, reported to the user without editing check logic). Never swallow an error and never claim completion while any check failed.

## What you hand back

The written `.gitignore` with before and after untracked counts, remaining paths, and the snapshot path when an existing file was merged; the selected hook manager (or confirmed native hook) with changed config and manifest paths, the effective hook path, the passing all files command and output with no formatter residue, the failing probe evidence showing a block and the passing probe evidence showing zero (or the explicit proof unavailable report when no safe defect could be injected), and the rollback command; the written `REVIEW.md` and `CONTRIBUTE.md`; and a report listing every file actually read, the human supplied rules as tagged, applied merges, flagged conflicts, and the rollback path. Otherwise hand back the exact `blocked` classification with partial state or rollback detail.
