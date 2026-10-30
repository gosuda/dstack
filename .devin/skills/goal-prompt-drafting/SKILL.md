---
name: goal-prompt-drafting
description: 'Use when asked to draft copy-ready /goal objectives for long-running agents. Not for source or remote-system changes.'
---

# Goal prompt drafting

You turn a loose request into one copy-ready `/goal` line a long-running agent can terminate on. The whole job is chat output: you read the draft and any referenced context, then return a single normalized objective plus a list of whatever you could not ground. You never touch files, version control, credentials, or anything remote.

A good objective reads as one terminating condition: several elements joined with AND, never OR, because a looped agent takes the cheaper branch of every OR. Each element names an end state, scope, check, invariant, or stop bound (below). Everything in it must come from the request, the conversation, or the repository. Anything you cannot source stays out and goes on the `Missing:` list instead; a goal with an invented success condition terminates on the wrong contract.

## What a complete objective contains

- End state, not activity: write what the world looks like when the work is done ("all `legacyAuth()` call sites use `auth.verify()`"), not the activity ("migrate the auth code"). An activity can be claimed; an end state is true or false.
- Scope to read first: name the files, issue, logs, or plan the agent should read before acting, so it grounds itself instead of guessing.
- A stated check with visible output: give the exact command and its observable result ("`pnpm test` exits 0"), and tell the agent to run it and show the output. A result that never lands in the transcript does not exist to the evaluator.
- Invariants: state what must not change ("without modifying vendor/"), and always include "do not weaken, skip, or edit the checks themselves" so the agent cannot game its own gate.
- A stop bound or blocked clause: something like "or stop after 20 turns" or "if blocked, stop and report the blocker". Without one, a mis-stated condition loops forever. Note that a turn bound silently extends across session resume because the counter resets; prefer an explicit blocked clause for work that may resume.

Keep the objective small. Every constraint narrows the state space the agent can explore, so collapse to one terminating criterion when possible, move scope and definitions into a referenced file, and drop non-goals: each constraint earns its place only by closing a real easy-out. For long goals, name the final evidence (diff, report, artifact) and require a progress log file so state survives compaction and resume. The harness limit is fixed at 4,000 characters and `/goal` is one line; if the brief exceeds it, put the details in a `GOAL.md` and reference that file from the objective.

## Closing the easy-outs

Reread the drafted condition the way a lazy model would: what is the cheapest way to make every check pass without doing the intended work? Close the cheapest outs by pairing existing checks rather than adding constraints, and do not enumerate every conceivable out into a non-goal list. The recurring outs:

- Delete or stub instead of fix: "search prints nothing" also holds when the callers are gone, so pair such a check with one proving the feature still works.
- Pass on a subset: running one test file, narrowing the search path, excluding directories from the check.
- Game the gate: skipping or xfail-ing tests, hardcoding expected outputs, special-casing the test inputs, editing the check itself (covered by the invariants rule).
- Claim without running: declaring done or blocked with no check output in the transcript (covered by the show-the-output rule).

If an easy-out cannot be closed with a sane constraint, list it in `Missing:` as a warning. An invented or absurd constraint is worse than a flagged gap.

## Security research goals

These collapse to one terminating criterion: identify, trigger, and validate one high-severity vulnerability valid under a referenced threat-model file. That file, not the goal, carries scope, attacker powers, the severity baseline, and known findings to skip. Use neutral wording ("trigger and validate", not "prove this is exploitable"), require demonstrated preconditions (assumed attacker access is the most common false positive), and stop for human review after each finding rather than piling up untriaged reports. Findings get validated with a second pass by a fresh agent, never by the finder alone.

## Normalizing and returning the objective

Normalize deterministically: collapse all whitespace to one line, strip `/goal` prefixes, surrounding quotes, and code fences. Warn if no stop clause is present; do not silently ship a condition that can loop forever. If the result is over 4,000 characters, shorten it or move detail to a referenced file and rerun; never truncate the contract.

Return exactly one fenced `text` block holding the single-line objective:

```text
/goal <single normalized objective>
```

Add no prose around it except a `Missing:` list, one line per gap, when checklist elements could not be grounded. If the run is blocked or non-converged, return the formatted objective plus the `Missing:` list; never claim the done predicate holds while a contract element is ungrounded.

Example grounded result:

```text
/goal All legacyAuth() call sites use auth.verify(): `rg "legacyAuth\(" -t ts` prints nothing AND `pnpm test` exits 0 (run both, show the output), without modifying vendor/ or weakening any test. If blocked, stop and report attempted paths and the blocker, or stop after 20 turns.
```

Example with gaps (no metric or benchmark in context):

```text
/goal Make checkout faster
```

Missing:
- measurable end state: which metric and threshold count as "faster"
- verification: the benchmark or command that proves it
- stop bound: e.g. "or stop after 20 turns"
