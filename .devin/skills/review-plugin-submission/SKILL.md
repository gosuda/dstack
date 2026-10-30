---
name: review-plugin-submission
description: 'Use when asked to review a plugin for marketplace readiness via a read-only audit of published quality gates. Not for reviewing a PR or code diff: use review.'
disable-model-invocation: true
---

# Review plugin submission

Marketplace readiness gets a read-only audit here: a plugin directory goes in, a sectioned pass/fail report with a submission recommendation comes back in chat. Files, version control state, credentials, paid actions, published artifacts, deployed targets, and remote state all stay untouched. No file is written; the report is the sole artifact. Remote reads stay limited to what the audit itself needs.

Reviewing a pull request or code diff belongs to `review`, not to this job.

You need `plugin_root` (required), the absolute path to the plugin directory under audit. You can also supply `gate_rules_path` (optional), an absolute path to a gate rules file defining the named gates, each gate's pass condition, and the exact failure message for its fail path. Without it, the audit runs three built-in default gates: manifest-present, manifest-complete, and file-valid, with no allowlist entries.

## Reading the rules and the manifest

Parse the gate rules file first when one is supplied. Record each named gate (a check, rule, or criterion block) with its pass condition and the exact failure message for its fail path. Also parse the allowlist section when present: each entry is a path prefix, and a file matches when its path relative to `plugin_root` starts with that prefix.

Then confirm the manifest. Reject with a failure report when `plugin_root/plugin.json` does not exist. Reject with a failure report when it lacks `name`, `version`, or `description`, naming the missing fields.

## Examining every file in scope

Walk every file under `plugin_root` by traversing directories and following symlinks that resolve inside `plugin_root`. Skip any symlink whose resolved target falls outside `plugin_root`. Leave binary blobs, `node_modules`, and hidden paths out of scope.

For each file in scope, verify syntactic validity for its declared format, then apply each applicable gate to its contents. A gate fails when any file violates its condition; it passes only when every in-scope file satisfies it. Keep evaluating after failures: a parse error for one file (report its path and the error) never halts the rest, and a gate violation marks that gate FAIL while the remaining gates still run.

An allowlisted violation becomes a warning, not a failure: when a violating file's path matches a parsed allowlist entry, record the file path with the matched entry. The gate still passes.

## What you hand back

A chat message carrying the complete sectioned report:

- Summary: one line naming every failing gate, with the overall recommendation (`APPROVE`, `APPROVE WITH WARNINGS`, or `REJECT`)
- Gate results: per named gate, its status (`PASS` or `FAIL`) with a one-line evidence summary
- Warnings: per allowlisted violation, the file path and the matched allowlist entry
- Recommendation: `APPROVE` when all gates pass, `APPROVE WITH WARNINGS` when all gates pass with allowlist triggers, or `REJECT` when one or more gates fail

A report containing a FAIL gate is a valid terminal output. Fabricating a passing result is never acceptable. Non-mutation holds throughout: no file write, no version control change, no credential use, no remote call beyond the reads the audit needs.
