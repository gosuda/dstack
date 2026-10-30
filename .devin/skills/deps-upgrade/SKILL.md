---
name: deps-upgrade
description: 'Use when dependency upgrades need batching for CVEs, a major release, forced compatibility, a scheduled or vulnerability-triggered sweep.'
---

# Batching dependency upgrades

This covers one job: taking a set of dependency upgrades, from CVE fixes to scheduled hygiene, and landing them so every step stays attributable and reversible. It writes only manifests, lockfiles, and compatibility code in the current repository, in concern-atomic local commits, plus a temporary lockfile snapshot outside the tree for the pre/post audit. Rollback is version control (revert the campaign commits or reset to the recorded pre-campaign head). It never mutates remotes, never does feature work, and never refactors beyond compatibility code. A major bump needs explicit human approval given at runtime.

You are done when the selected upgrades are locked, tested at the required depth, majors carry their migration guidance, license and SBOM churn are checked, and the final vulnerability scan is recorded. For a sweep, every update sits somewhere on the risk ladder as verified or deferred with a recorded reason.

## Scope and starting conditions

You need a working repository with history, toolchains for each in-scope ecosystem, and operator directives stating which ecosystems and paths are in scope, the highest tier allowed (patch, minor, or major), and any package allowlist or blocklist. Optional extras: pinned targets for specific majors, a scanner choice (otherwise the per-family canonical scanner below), a vulnerability report or advisory feed, a cadence schedule, freeze-window or deadline constraints that cap the tier ceiling.

Before the first mutation, confirm each required tool exists (`command -v`) and run the full suite on the clean tree as the baseline. Missing tools or a red baseline stop the run before anything changes, because upgrade results on a red tree are not attributable.

Refuse to start, without changing anything, when any of these holds: an active feature branch with high churn, a pre-release freeze window, a mid-incident window, or a task that is really an API-break-driven refactor rather than a dependency upgrade. Report which gate tripped.

Freeze the ecosystem list, path scope, tier ceiling, and allowlist/blocklist from the operator directives before doing anything else, and never widen them mid-run. Findings outside scope become report items, not work.

## Baseline, then inventory

Record the pre-campaign HEAD sha and snapshot every lockfile to a temporary directory. That snapshot is both the audit baseline and the rollback anchor.

Then enumerate manifests and lockfiles across the in-scope ecosystems. Canonical names are often extensionless (`go.mod`, `Gemfile`, `pom.xml`), so filter on filenames, not extensions, and note that `fd` takes one glob per call, so anchor on canonical filenames with one regex:

```sh
fd -t f '^(package(-lock)?\.json|pnpm-lock\.yaml|yarn\.lock|Cargo\.(toml|lock)|pyproject\.toml|poetry\.lock|requirements.*\.txt|Pipfile\.lock|go\.(mod|sum)|pom\.xml|build\.gradle(\.kts)?|settings\.gradle(\.kts)?|libs\.versions\.toml|gradle\.lockfile|Gemfile(\.lock)?|.*\.gemspec|.*\.opam|dune-project|opam\.locked|mix\.(exs|lock)|composer\.(json|lock))$'
```

Add ecosystem-specific names the project actually uses beyond this list (`Pipfile`, `Brewfile`, `flake.nix`, `shard.yml`, `pubspec.yaml`). Tooling mandates for the whole run: `fd` (not `find`), `difft` (not `diff`), `bat -P -p -n` (not `cat`), `git grep -n -F` (not plain `grep`).

## Scanning and batching

Scan outdated dependencies with the per-family commands and capture each report (read reports and later CHANGELOGs with `bat`, never `cat`):

| Family | Outdated scan | Upgrade command | Lockfile |
|---|---|---|---|
| Rust | `cargo outdated`, `cargo audit` | `cargo update`, `cargo upgrade` | `Cargo.lock` |
| Python (Poetry) | `poetry show --outdated` | `poetry update`, `poetry add <pkg>@latest` | `poetry.lock` |
| Python (pip-tools) | `pip list --outdated`, `pip-audit` | `pip-compile --upgrade`, `pip-sync` | `requirements.txt` |
| JS/TS (pnpm) | `pnpm outdated`, `pnpm audit` | `pnpm update`, `pnpm up --latest` | `pnpm-lock.yaml` |
| JS/TS (npm) | `npm outdated`, `npm audit` | `npm update`, `ncu -u` | `package-lock.json` |
| Go | `go list -u -m all`, `govulncheck` | `go get -u <pkg>@latest`, `go mod tidy` | `go.sum` |
| Java/Kotlin (Gradle) | `gradle dependencyUpdates` | edit `libs.versions.toml`, `gradle dependencies --refresh-dependencies` | `gradle.lockfile` |
| Java/Kotlin (Maven) | `mvn versions:display-dependency-updates` | `mvn versions:use-latest-releases` | `pom.xml` |
| OCaml | `opam list --upgradable` | `opam upgrade <pkg>`, `opam pin <pkg>.<ver>` | `*.opam.locked` |

A family whose scan tool is missing leaves scope and gets reported. A missing CVE scanner is different: it blocks the run, because the done state requires the final scan, so the run ends blocked, never done with the scan skipped.

Bin every candidate as patch, minor, or major against the tier ceiling; candidates above the ceiling are report-only.

- Patches go as one batch. Confirm the diff is lockfile-only, run the full suite, and commit everything including the lockfile diffs as `chore(deps): patch sweep`. Floating ranges that skip the lockfile commit produce non-reproducible builds, so the lockfile diff is always committed.
- Minors go together. Read each minor CHANGELOG, run a smoke test (minors can shift behavior), and commit as `chore(deps): minor sweep`.
- Majors go one per commit, and each one starts with reading, not writing. Read the upstream `CHANGELOG.md` / `MIGRATION.md` / release notes (a major without primary-source review is forbidden), identify removed, renamed, behavior-changed, and default-changed APIs, check for an upstream codemod or migration tool and prefer it, search direct usage of each changed API with `git grep -n -F '<symbol>'` and `ast-grep -p '<pattern>'`, and verify the peer-dependency and runtime-version matrix, the license (no blocking-direction change), and that the SBOM diff will match the expected tree change. Then apply the migration guidance (codemod or manual edits, confined to compatibility code), run the full suite plus adversarial tests with deprecation warnings as errors, validate any hot path with `hyperfine` against the previous commit, and commit `chore(deps)!: bump <pkg> <old>→<new>`. Never disable a deprecation or audit signal to make a gate pass; a warning that cannot be fixed now becomes follow-up debt.

A major whose migration would propagate API breaks across the codebase beyond compatibility code is not started: it is reported. The same restraint applies to evidence. For a held upgrade, record the exact blocking requirement, its declaring package and version, and the resolved and installed environments the evidence applies to. A lock edit does not update installed metadata, latest-release claims need a current registry check, and a mitigation-retirement claim must be verified against the installed mechanism and the guarded failure (a nearby or similarly named upstream fix is not enough). Before removing an apparently unused dependency, inspect feature unification, macro expansion, package and import aliases, build metadata, and runtime loading; a text scan or one green build is not exhaustive evidence. Keep lock churn concern-atomic and aligned with the target manifests, never moving a lockfile onto a different manifest set without resolving and verifying that target. And never preserve a gate's old counts by suppressing newly real defects.

## Audit, re-scan, and the final report

Compare the pre- and post-campaign snapshots with `difft` (lockfiles are machine-generated and coarser diffs misread them). Watch the transitive churn: a surface can look clean while a transitive bump carries the CVE fix, or a new transitive CVE. Then run the CVE scanner again per family (`cargo audit`, `pip-audit`, `pnpm audit` / `npm audit`, `govulncheck`), read the output, and record it. Auto-fix flags that bypass reading (`npm audit fix --force`) are forbidden. New CVEs the re-scan surfaces are recorded, not remediated, inside this campaign. For a cadence-driven or vulnerability-triggered sweep, every update gets one disposition in the sweep report: classified, verified, or deferred with a reason.

When a patch or minor batch fails its tests, restore the last green state (`git revert` the batch commit if committed, otherwise `git restore` the touched paths), then re-run the batch one package at a time to isolate the offender, or drop that package and record it. Never leave a partial bin failing or uncommitted. A failed major is reverted and recorded with its migration blockers; a missing migration guide or a failing codemod gets the same treatment (revert and record, never improvise an unreviewed migration). A major without explicit approval is deferred with a recorded reason, not applied. If the test suite cannot run at all, every unverified update is deferred as non-converged with a recorded reason; the done state is not claimed. Every committed bin is a green, self-consistent state, so recovery always lands on a bin boundary, and operator work outside campaign commits is never discarded. A blocked result reports the failing gate, the SHA reverted to, and the remaining unprocessed candidates.

The final report is a terminal done or blocked statement with sections in order: concern-atomic commits, per-package tiers and versions, checks per bin, major migration notes, license and SBOM churn, lockfile audit, post-upgrade CVE scans, sweep dispositions, follow-up items. The working tree holds only verified updates; deferred majors stay unapplied.
