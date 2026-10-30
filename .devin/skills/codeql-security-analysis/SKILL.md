---
name: codeql-security-analysis
description: 'Use when building or reusing a CodeQL database, running CodeQL security analysis, or modeling project-specific sources and sinks. Not for manual vulnerability review: use security-review (mode: confirmed).'
---

# CodeQL security analysis

You run CodeQL taint and data flow analysis against a real database built from project sources, and you leave a complete evidence trail behind. A clean result counts only when the database passes its quality gate, the query suite resolves to something real, and every skipped language or path gets named. Never touch target project source. Every artifact you create lives in one dedicated output directory, and deleting that directory undoes everything.

What you need before starting: the target project root, plus either the primary languages to analyze or a path to an existing reusable CodeQL database. Compiled languages also need the real build command, because CodeQL extraction must run under the actual build. Optionally take an explicit query suite or ruleset selection, project specific source and sink models to author as data extensions, an output directory defaulting to a dedicated directory under the project root, and user authority for any target project dependency or query pack installation.

## Keep every artifact in one dedicated directory

Create the output directory first (for example `<project-root>/.codeql-out`) and write nothing anywhere else. Database, log, extension, suite, and SARIF files all land there. Deleting this directory is the complete rollback, and target source stays unmodified.

## Resolve or build the database

When a reusable database path was supplied, resolve it with `codeql database resolve` and confirm it targets the requested language. Otherwise build with `codeql database create`, using the real build command for compiled languages or source only `--overwrite` extraction for interpreted ones. Record the exact build command and its exit status as build evidence in the output directory. A database that cannot resolve or build stops here with its build evidence recorded.

## Pass the quality gate before analyzing

Inspect extraction warnings and source file coverage with `codeql database resolve` and source location inspection. When the database fails the gate (missing source files, zero extracted files, build errors, unresolved language), stop and report the failure class. A failed database never gets analyzed.

## Resolve an explicit query suite with nonzero queries

Select an explicit suite or ruleset and resolve it with `codeql resolve queries --queries=<suite>`. Confirm the resolved query count is nonzero. A suite that resolves to zero queries stops the run; report the suite path instead of analyzing with nothing.

## Model project specific sources and sinks when asked

When custom source or sink modeling was requested, author the CodeQL data extension YAML under the output directory and include it through `--search-path` or `--additional-packs`. Validate every extension against the CodeQL data extension schema before use. An invalid extension gets rejected and stops the run. Never analyze with an unvalidated model.

## Run the analysis and keep the raw evidence

Run `codeql database analyze <database> <suite> --format=sarif-latest --output=<output>/raw.sarif`, passing any data extension search path. Capture stdout and stderr as an analysis log in the output directory. Tune `--threads` to available cores and memory, preferring `--threads=0` only when memory allows it. When analysis errors out, preserve the partial log and any partial raw SARIF, report the error, and classify the result as blocked. A partial result never presents as done.

## Shape the final SARIF and explain the coverage

De duplicate the raw SARIF, apply severity filtering, attach the ruleset selection metadata, and write the final SARIF to the output directory with the recorded ruleset and suite selection. Then explain the coverage basis: with zero findings, or when a language or path was skipped (for example a language that was never built), state explicitly why. An unexplained zero is not a success. A clean result always states what was actually covered.

## When anything fails

Report the exact failure class, the evidence captured, and the step that stopped: build failure with errors, missing toolchain, or failed extraction; quality gate failure with the gate output; zero query resolution with the suite path; invalid data extension with the schema violation; analysis runtime error with the preserved partials. Recovery from a build failure is to fix the build and rebuild in the output directory. Target source stays unmodified, so rollback is always deleting the output directory. Never swallow an error or present a blocked run as complete.

## What you hand back

The output directory holds the database, build evidence, resolved query suite and ruleset, data extension models, analysis log, raw SARIF, and final SARIF. Every run ends classified as done or blocked with its named failure class and evidence.
