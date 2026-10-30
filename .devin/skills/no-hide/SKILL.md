---
name: no-hide
description: 'Use when the user asks to detect clever-concealment patterns that obscure real code structure. Not for refactoring the concealment away: use architect.'
---

# Finding code that hides its own structure

Some code is hard to read because the problem is hard. Different problem: code that is hard to read because indirection, naming, or layout hides what it really does. Your job is to find that concealment and report it. You only report, never refactor (refactoring belongs to architect). You change nothing: read-only, no file, VCS, credential, paid, published, deployed, or remote mutation.

## Where to look

You need a target scope: a file path, directory path, module name, or diff range. Optionally the user names one concealment form; then you restrict detection to that form, otherwise you apply every applicable form.

- If the scope does not exist or cannot be read, stop. Return `{status: "target-missing", scope: <supplied>}` and do nothing further.
- If the scope holds items that are not source code, ignore them. Do not scan configuration, documentation, or generated artifacts unless the user explicitly names them.
- If the scope is too large to inspect in budget, return the confirmed findings you have and mark the unscanned remainder as `incomplete`. Partial honesty beats silent skipping.
- If the user names a form this skill does not detect, return `{status: "form-unknown", forms: <list of supported forms>}`.

## Read everything in scope

Read the full text of every reachable source file inside the scope. Skimming the exported symbols is not enough, since concealment lives in the bodies.

## The five shapes of concealment

Apply every applicable form to every file. Work through all forms across all lines of a file; finding one high-severity pattern is never a reason to stop scanning that file.

| Form | What to flag |
|---|---|
| Abstraction layering | Indirection that adds no behavior and forces the reader to reconstruct what a direct implementation would look like. One forwarding or delegation layer on a call chain is allowed. Two or more on the same chain is concealment. |
| Obscured naming | Names that describe the implementation technique instead of the domain concept, or names with inverted polarity (for example `disableSecurity()` that enables it, or `close()` that opens a resource). |
| Implicit control flow | Branching encoded in naming conventions, comment conventions, or ordering instead of explicit if/else/switch. Loops whose termination depends on mutable global state or a side effect invisible at the call site. |
| Indirection masking dependencies | Static calls, eager imports, or compile-time instantiation that hide the runtime dependency graph. Singleton accessors that bypass injection. Global mutable state reached without an explicit reference. |
| Structure serving author taste | File and module organization chosen for elegance rather than reader navigation. Depth-first directory trees where breadth-first would match the mental model. |

## How serious each instance is

Grade every confirmed instance once, at the point you report it:

- High: actively misleads or inverts meaning, so the reader will reach a wrong conclusion.
- Medium: takes extra effort to decode, with no active falsehood.
- Low: friction without meaningful misdirection.

## What you hand back

One structured report, in this order: status, findings, summary, done flag. Each finding carries file, line or range, pattern form, and severity. When nothing matches, say so explicitly instead of returning an empty report. You are done when every applicable form has touched every file in scope and every confirmed instance (or the explicit none-found statement) is in the report.
