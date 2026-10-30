---
name: run-smoke-tests
description: 'Use when asked to run smoke tests or verify a local build, applying only minimal unblocking fixes. Not for iterative bug fixing.'
disable-model-invocation: true
---

# Run smoke tests

You confirm the local build still breathes. When a human explicitly asks for end-to-end smoke verification, you run the project's conventional smoke target, classify the result honestly, and allow yourself at most one minimal unblocking fix before reporting. The run is done when the check set has a stable result with an honest flake-risk classification.

This skill writes only named local artifacts plus minimal fixes in project source files, and it states the rollback path before mutating anything. Rollback is deleting added artifacts and reverting the source fix. It never mutates remote state, version-control history, credentials, payments, publications, or deployments, and it never turns into iterative bug fixing.

What you need before running: a working directory holding a runnable build and test suite, which is required, and network access, which is required whenever the build or tests fetch remote artifacts. A named smoke-test command or target is optional and defaults to the project's conventional smoke target.

## Run the smoke target

Record the current version-control state, branch and HEAD commit, as the rollback anchor. If the workspace is dirty, stop and report the dirty state before going further.

Find the smoke target in the build manifest (Makefile, package.json scripts, Cargo.toml, pyproject.toml, or equivalent), or take the user-supplied target name when one was given. Confirm the target exists and is executable before running it; when it is absent, stop with `target-missing` and say which manifests were checked.

Execute the smoke target and capture stdout, stderr, and the exit code. When the build step itself exits non-zero, stop there and do not proceed to test.

## Call the result what it is

Known flaky candidates are tests or targets named in the project's flake manifest, quarantine list, skip file, or the user-supplied input. Where nothing is declared, treat every non-zero exit as a failure and mark flake-suspect unknown:

- Exit 0 with no stderr: `pass`.
- Exit 0 with stderr warnings: `pass-with-warnings`.
- Non-zero exit touching a known flaky candidate: `flake-suspect`.
- Non-zero exit with no known flaky candidate: `fail`.

## One small fix, then honest rollback

When the result is `fail` or `flake-suspect` and the failure has one recognizable cause such as a missing import, a typo, a broken symlink, or a wrong env var, you may apply that minimal correction directly and re-run the smoke target exactly once. Do not refactor, add features, or widen scope, and do not let the fix attempt grow beyond its single cause.

When the second run still fails, revert every change from the fix attempt before reporting. When two successive runs disagree or a fix attempt widened scope, treat the run as `non-converged`: revert and report the honest flake risk.

The final classification is the classification of the last run. Claim `pass` only when the final run exits zero, no matter what earlier runs showed; a fix stays in the workspace only when the re-run went green.

## What you hand back

A `SMOKE <classification>` block: the classification, the run count, the rollback anchor (HEAD from the first step), applied diffs, and a reverted flag.
