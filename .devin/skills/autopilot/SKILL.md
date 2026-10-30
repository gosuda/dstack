---
name: autopilot
description: 'Use when a human has an approved delivery plan and wants the full chain run under phase gates. Not for planning, open-ended debugging, or single-step execution.'
---

# Autopilot

You run an approved delivery plan from first edit to observed close-out, under phase gates that halt the chain the moment something is unproven or unauthorized. You never write the plan. An approved plan is the entry ticket, and without one you stop before touching anything and send the work back to planning.

## Start only with an approved plan

You need a feature description, an approved execution plan, the repository, acceptance criteria, and a close-out condition. Scope limits, an assigned executor, the target branch, remote and PR destination, required checks, and shipping instructions ride along when given. When something optional is missing you may fill it in only if repository evidence gives exactly one safe answer.

Read the plan first and reject contradictions, naming the conflicting pair. If the invocation names an executor that is not available, stop and say so. Then confirm approval: plan-mode approval (`ExitPlanMode`) or an equivalent written approval the user has given. With no approval record there is no implementation and no delegation. Route to planning instead.

## Bind every step to the repository

Before changing anything, gather enough repository evidence to tie each plan step to a concrete artifact (a file, directory, or remote target) and to the behavior, verification, and remote destination behind it. State the scope boundary plainly: what is inside the campaign and what is excluded from it. Everything after this point stays inside that boundary.

## Keep dangerous consequences human-gated

Some consequences always need the human's explicit cover: credentials, paid actions, changes to data at rest, publication, deployment, remote bulk mutation, and irreversible deletion. Preview the exact target and consequence first, and continue only when this invocation covers it. Everything else is reversible local work with version control as the rollback. You push or publish only when the invocation covers that exact target, otherwise you leave changes local. An ambiguous target or absent authority stops the run.

When an iteration loop waits on a human gate, name the smallest gate that unblocks it: the exact action, the signal it contributes, where that signal lives, and the observable condition that permits the next iteration. A gate comes out only through the narrowest existing mechanism, which is one of an invokable command with a deterministic exit status or structured response, a named persisted log file, a read-only metrics or log query yielding an explicit pass, fail, or warn with retained values, or an executable assertion of the observable completion condition. Never introduce a credential, payment, publication, deployment, remote mutation, data-at-rest mutation, or irreversible action to close a gate. Every gate that remains is either one outer-loop human approval before autonomous iteration, or a discrete handoff stating the required action, inputs, and return artifact.

## Follow the chain in order

The chain runs execute, then simplify, then review, then finalize, then report. Report always runs, for success and halt alike. The exact gate mechanics and invariants live in `references/pipeline-gates.md` and that file is binding. On any conflict within autopilot, it governs directly.

Each phase follows the same state machine: run the phase, check its gate, advance on pass. A failing gate fires its autofix arm at most once, then rechecks. A failing recheck halts the chain, never a second autofix. A red gate never advances to the next phase.

- execute: Execute the bounded plan against acceptance criteria, constraints, repository evidence, and the required verifier, and record an implementation summary with local verification evidence. This phase covers implementation and local verification only, never the simplify, review, finalize, or CI phases, which autopilot owns. On verifier failure, `grill-core` runs once in findings and verifier-failure mode on the failing output, then one recheck. A second failure halts with the verifier output and diff recorded.
- simplify: Simplify the completed diff with behavior preserved. A `simplify` exit of `0`, `11` (empty diff), or `12` (false-positive-only) passes. A behavior regression (exit `13`) is self-reverted inside `simplify`. New bloat (exit `14`) or a mixed-concern commit (exit `15`) halts the chain for a human re-plan, with the cause recorded.
- review: Review the in-scope change for critical and high findings, unhandled error paths, scope creep, and stubs. When critical or high findings occur, `grill-core` runs once as the autofix arm on those findings, followed by a re-review of the changed files only. Zero critical and zero high findings remain, or the chain halts with the residual findings listed. `grill-core` is an autofix arm for `execute` and `review`, never an independent phase.
- finalize: Finalize the reviewed change: run the required checks, create atomic commits, and only with explicit shipping authority covering the exact branch, remote, and PR destination push or create-or-update the PR. Otherwise leave changes local. A finalizer refusal (push refused, checks blocked) is a deliberate safety stop, not a defect to patch. When `git remote` is empty, or `mode:local` is set, run local-only: local checks, atomic commits, no push or PR creation, no invented remote, and the report states `mode: local-only` with the unpushed commit list.
- report: Emit the handoff on a halt or the finalization report on success, always.

After close-out is authorized and observed, route any supported in-scope fix through execution again, repeat the gates its mutation could disturb, and finalize each authorized update. Never merge, deploy, or publish elsewhere without matching authority.

## A halt hands off, never hides

Stop on a missing approved plan, contradictory input, an unavailable executor, an ambiguous target, absent authority, a failed gate, non-converging review, a rejected remote mutation, or incomplete close-out. Preserve successful in-scope work and observed remote state. Undo only mutations this run made, using reversible repository or hosting operations. Never discard unrelated work.

Every halt produces a handoff in the binding format from `references/pipeline-gates.md`:

```
HALT at <phase> (gate <gate-name>)
reason:        <one line — what the gate measured and why it stayed red>
autofix tried: <A(P) name + outcome | none — not autofixable>
residual:      <the findings / verifier output / refusal that remain>
state:         <commits made (sha + subject), pushed? PR url?, working-tree dirty?>
next:          <the single action that unblocks>
```

Return `BLOCKED` carrying the failed stage, the exact reason, the autofix result, partial artifacts, remote mutations, proof state, recovery state, and the single concrete requirement to resume. Never claim a rollback, publication, or close-out you did not observe.

## The run ends one of two ways

There is exactly one terminal result. `DONE` delivers the behavior, the changed artifacts, verification evidence, the branch and PR, the complete finalization report (checks, commits, push or PR status), and the close-out state quoted as observed in repository or remote state:

```
autopilot report
mode:          <full | local-only> [+ headless]
task:          <one line>
phases:        execute <✓ | HALT> · simplify <✓ | HALT | skipped> · review <✓ | HALT | skipped> · finalize <✓ | local-only | HALT | skipped> · report ✓
autofix:       grill-core <ran once in <execute | review> | skipped, gates clean>
gates:         <execute simplify review finalize pass/fail, with the autofix arm noted where it fired>
commits:       <sha + subject per commit>
remote:        <pushed branch / PR url | local-only, not pushed>
outcome:       <shipped | HALT at <phase> (gate <gate-name>), see handoff above>
```

`BLOCKED` carries the halt handoff above: what failed, why, what survives, and the one action that unblocks it.
