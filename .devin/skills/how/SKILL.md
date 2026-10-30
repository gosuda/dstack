---
name: how
description: 'Use when the user asks "how does X work" and wants an architecture walkthrough of the code path or subsystem, including its gotchas. Don''t use for tasks that require source or remote-system changes.'
---

# How a code path really works

Someone asks how a piece of this codebase works and wants the truth as it runs, not as the docs wish it were. Your job is a read-only walkthrough: entry point, control and data flow, the seams where it leaves its own code, and the surprises a newcomer would trip over. You change nothing (no file, VCS, credential, paid, published, deployed, or remote state). Your only side effect is the chat report.

## Start from what they named

You need two things:

- The specific target: path, function, module, class, or subsystem.
- The user's full phrasing, because the phrasing sets the scope.

Pin the target down before reading further. If the name fits more than one place, ask which one they mean and wait. Never walk several candidates at once. If it fits nothing in the tree, stop and say so plainly as `no-evidence`, naming exactly what you looked for instead of guessing a nearby location.

## Walk the path without skimming the tree

Find the entry point with structural reads (declaration summaries and line-range reads that identify the primary file and its direct dependencies). Resist opening every file that looks related.

Then trace from the entry point in execution order: which functions, classes, or modules run, in what order, under what conditions, and what data moves between them. Call out every architectural seam: delegation to an external library, a system call, a process or network crossing, any I/O, plus what that seam costs the caller (latency, failure modes, hidden coupling).

Ground each key claim in a concrete file and line range. Describe the code as it exists.

## Name what would surprise a caller

For each major step, record the behaviors signatures do not advertise: implicit assumptions, edge cases handled silently, global state the step leans on, error paths that diverge from the happy path, and performance characteristics that are not obvious from the signature. A walkthrough without these is just a symbol list.

## When the evidence runs out

Sometimes the target sits behind something you cannot see through: a binary blob, generated code with no source, an external service. Say the evidence is unavailable and end with `inconclusive` rather than reconstructing behavior from names.

## What you hand back

A chat report with the entry point and control flow, the data moving through it, the seams and their consequences, and the gotchas. It ends with `done`, or with the honest terminal state: `no-evidence` when the target is not there, `inconclusive` when it sits behind an opaque boundary.
