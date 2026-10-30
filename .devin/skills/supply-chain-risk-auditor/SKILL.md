---
name: supply-chain-risk-auditor
description: 'Use when assessing npm, PyPI, or Go dependency supply-chain risk, with lockfile-absent paths marked unassessable. Not for remote or irreversible changes.'
disable-model-invocation: true
---

# Supply chain risk auditor

A team wants to know whether the third-party packages they depend on carry known vulnerabilities. You read their manifest, resolve the versions they actually use, ask each ecosystem's advisory source, and write two artifacts outside the audited repository: a `findings.json` file machines can check and a `report.md` file humans can act on. Every dependency ends in exactly one of three states (assessed-clean, assessed-flagged, unassessable), and remediation advice stays clearly separated from measured findings. Unavailable data is never treated as risk, and absence of data is never treated as safety.

You never install, build, import, or execute the audited project or its dependencies, and you never read dependency source. You only query advisory metadata over the network and write the two named artifacts. If either file must go away, deleting both from the output directory is the full rollback.

## What you hand it

- `Project path` (required): a directory holding a manifest file (`package.json`, `requirements.txt` or `pyproject.toml`, or `go.mod`).
- `Lockfile` (optional): when present (`package-lock.json`, `poetry.lock`, `Pipfile.lock`, `go.sum`), you resolve transitive dependencies and match advisories against exact resolved versions. When absent, direct dependencies are judged against declared version constraints and every transitive dependency is marked unassessable.
- `severity_floor` (optional, default `medium`): the lowest advisory severity shown as an actionable finding. This is the only severity floor in the skill. It applies after the three-state classification and never changes a dependency's state.
- `Output directory` (required): where `findings.json` and `report.md` go. Defaults to a directory adjacent to the audited project.

## How the audit runs

### Name the ecosystem

Identify the ecosystem from the manifest file type. With no recognized manifest, mark all dependencies unassessable and skip to writing the artifacts, where `findings.json` carries an empty dependencies array with all counts zero and `report.md` states that no recognized manifest was found.

### List the direct dependencies

Parse the manifest for direct dependencies with declared version constraints. For npm, read `dependencies` and `devDependencies` in `package.json`. For PyPI, read the `requirements.txt` lines or the `[project.dependencies]` and `[tool.poetry.dependencies]` sections of `pyproject.toml`. For Go, read the `require` blocks of `go.mod`, treating entries with `// indirect` as indirect and the rest as direct.

### Pin the exact versions

When a lockfile is present, parse it for exact versions and enumerate the transitive dependencies. For npm, read resolved versions from the `packages` section of `package-lock.json`. For PyPI, read pinned versions from `poetry.lock` or `Pipfile.lock`. For Go, confirm module integrity from `go.sum` while taking the version from `go.mod`. Without a lockfile, judge direct dependencies against their declared constraints and mark every transitive dependency unassessable with reason `no-lockfile`, since resolved versions cannot be confirmed (for Go, entries carrying `// indirect` fall in this group).

### Ask the advisory source

Load `references/ecosystem-queries.md` and use its query method for the detected ecosystem. The method named there owns the ecosystem: `npm audit --json` for npm, the OSV query path for PyPI, the `vuln.go.dev` path for Go. Never run a second scanner for an ecosystem that file already covers. A Go module path returning `404` means no known vulnerabilities, so that dependency is assessed-clean.

For each match, record the advisory ID, severity, affected version ranges, and fixed version. Each recorded advisory carries `advisory_id`, `affected_range`, `severity` (when the source supplies it or it follows from the advisory), `fixed_versions` (when supplied), and `patchable`. Then classify each direct dependency:

- `assessed-clean`: the advisory query succeeded and returned no matching vulnerability for the resolved version.
- `assessed-flagged`: the query returned one or more matching vulnerabilities.
- `unassessable`: the source was unreachable, rate-limited, or returned malformed data; the dependency has no resolved version; or it is a transitive dependency with no lockfile.

Apply `severity_floor` only after this classification. Below-floor advisories stay assessed-flagged and are counted as suppressed-by-floor rather than relabeled clean. Advisories with missing severity are never suppressed and never treated as safe. Attempt the query for every direct dependency, so each one ends with a state and none passes through silently.

### Write findings.json

Write the structure `{ dependencies: [{ name, version, ecosystem, direct, state, reason, advisories: [{ advisory_id, affected_range, severity, fixed_versions, patchable }] }], summary: { total, assessed_clean, assessed_flagged, unassessable, severity_floor, suppressed_by_floor, patchable, unpatchable } }`. The `reason` field appears when `state` is unassessable. The `patchable` and `unpatchable` counts tally advisories with and without a supplied fix, derived from the per-advisory `patchable` flags.

### Write report.md

Cover the direct-dependency findings with per-dependency state and advisory detail (advisory IDs, affected ranges, fixed versions when the source supplies them, patchable versus unpatchable status), the lockfile-wide version-matched advisories for transitive dependencies when a lockfile was available, the applied severity floor with its suppressed-by-floor count shown separately, the patchable versus unpatchable counts derived from the per-advisory flags, a coverage summary with all three state counts computed before severity filtering, every unassessable dependency with its reason, and remediation recommendations prioritized by severity and kept distinct from measured findings. A clean conclusion is permitted only for the portion whose advisory queries completed and whose exact-version coverage is assessed-clean; unassessable dependencies stay visible in the coverage section.

## When something gives

- Missing manifest: write `findings.json` with empty dependencies and zero counts, and state the absence in `report.md`.
- Network failure or rate limit: mark the affected queries unassessable with reason `network-failure`, return partial results for completed queries, and never retry with a widened scope.
- Malformed advisory response: mark the affected dependency unassessable with reason `malformed-response`, and never guess its vulnerability status.
- A step that would require execution: stop and mark the dependency unassessable. Installing, building, importing, or executing the project or its dependencies, and reading dependency source, are outside this skill entirely.
