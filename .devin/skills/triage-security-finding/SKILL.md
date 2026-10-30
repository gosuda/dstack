---
name: triage-security-finding
description: 'Use when exactly one concrete security finding with a source anchor needs a verdict before PoC work. Not for projecting batches of findings onto a graph: use project-findings-onto-graph.'
---

# Triage a security finding

The work is reversible and local: you write only a single-candidate evidence packet file with optional graph annotations on the target, never mutate anything remote, and deleting the packet file reverses the packet while graph annotations are removed independently. You are done when exactly one verdict (Promote, Needs manual review, Deprioritize, or Blocked) goes out with its binding, reachability, boundaries, blast radius, manual review targets, and limitations.

## What you hand it

- Required: one finding with a bindable source anchor. A SARIF result, reviewer annotation, suspicious function name, or report excerpt qualifies once it resolves to a file and line range in the working tree.
- Optional: existing graph annotations on the target function or file, and graph evidence from prior runs.

## Refusals that protect the verdict

- Never triage more than one finding per invocation.
- Never guess or widen the search when the anchor will not resolve; emit Blocked.
- Never pick one anchor from several candidates without human input; emit Blocked.
- Never promote a finding beyond its source status.

## How the triage runs

1. Normalize the input. Pull the source anchor (file path, line range, function name) from the finding. When the anchor will not resolve to a concrete location in the working tree, emit `Blocked` with reason `unresolvable-anchor` and stop.
2. Bound the scope. Identify the single function, method, or code block holding the anchor. Expand past it only when the finding itself references cross-boundary behavior such as taint flow or a call chain.
3. Collect binding evidence. Read the anchored source and record the exact code, the function signature, the containing module or class, and any direct callers or callees visible in the same file.
4. Assess reachability. Decide whether external input (public API, request handler, CLI entry, exported function) reaches the anchored code, and record the path; otherwise mark it `internal-only`.
5. Identify boundaries. List the trust boundaries the finding touches (input validation, authentication, authorization, serialization, file I/O, network I/O, privilege transitions) and record whether the finding's path crosses each one.
6. Estimate blast radius. Classify it as `function`, `module`, `service`, or `system` by the scope of code affected if the finding confirms, and record why.
7. Identify manual review targets. List every code path, configuration, or dependency needing human judgment, each with the exact question the reviewer must answer.
8. Record limitations. List the assumptions, unread code, unobserved dynamic behavior, and untraced dependencies that bound the verdict.
9. Emit the verdict. Choose exactly one: `Promote` for strong binding, clear reachability, defined boundaries, and a plausible attack surface (proceed to PoC work); `Needs manual review` where partial evidence needs a human ruling on one or more review targets first; `Deprioritize` for weak binding, unreachable code, or negligible blast radius (record the reasoning and stop); `Blocked` where unresolvable anchors, missing context, or analysis limits prevent triage (record the blocker and stop).

## When something gives

- Unresolvable anchor: emit `Blocked` with reason `unresolvable-anchor`. Do not guess or widen the search.
- Ambiguous finding: emit `Blocked` with reason `ambiguous-anchor` and list all candidates. Do not choose one without human input.
- Missing evidence: record the gap under limitations. When the gap prevents a verdict, emit `Blocked` with reason `insufficient-evidence`.
- Partial result: when interrupted after the binding-evidence step, emit what was collected with verdict `Needs manual review` and reason `incomplete-analysis`.

The evidence packet reads in this order: verdict, binding (source anchor, file, line range, function), reachability, boundaries, blast radius, review targets, limitations.
