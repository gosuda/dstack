# Autopilot: pipeline gates and the autofix-then-halt state machine

This file is the authoritative source for every phase gate, its autofix arm, and halt behavior. `SKILL.md` summarizes the process; this file defines the exact criteria, invariants, and state machine. It is self-contained: on any conflict within autopilot, this file governs both mechanics and doctrine directly. No external baseline or peer doctrine is needed to interpret or enforce these gates.

## The autofix-then-halt state machine

One generic transition runs every phase. `P` is the current phase, `gate(P)` its gate, `A(P)` its autofix arm (may be none).

```
RUN(P):        invoke the phase's skill
CHECK(P):      evaluate gate(P)
                 pass            -> ADVANCE
                 fail, A(P) none -> HALT(P)
                 fail, A(P) set  -> AUTOFIX(P)      [only if not already attempted this phase]
AUTOFIX(P):    invoke A(P) exactly ONCE; then RECHECK(P)
RECHECK(P):    evaluate gate(P)
                 pass            -> ADVANCE
                 fail            -> HALT(P)          [never a second AUTOFIX]
ADVANCE:       P := next phase in {execute, simplify, review, finalize, report}; goto RUN(P)
HALT(P):       stop the chain; collect residual findings from P; route to report with halt=P
```

Invariants the machine enforces:

- Once: `AUTOFIX(P)` fires at most one time per phase. A failing `RECHECK` always routes to `HALT`, never back to `AUTOFIX`. Looping an arm to green hides a bad plan and compounds risk across a growing surface.
- No red advance: `ADVANCE` is reachable only from a passing `CHECK`/`RECHECK`. A red gate never enters the next phase.
- Report is terminal and unconditional: Both the success tail (after finalize passes) and every `HALT(P)` route to `report`.
- Publication authority: Remote publication, pushing, pull request creation, and remote mutation require explicit human authority naming the exact target. Local work is reversible with version control as rollback; without explicit publication authority covering the exact branch and remote, the chain remains local-only.
- Local-only execution: When `git remote` is empty or `mode:local` is active, no remote is invented or contacted; finalize runs local checks and creates atomic commits locally.

## Precondition: before execute

The chain begins only when an approved plan exists: one the user approved through Claude Code's built-in plan mode (`ExitPlanMode`), or an equivalent written plan the user has approved. autopilot never produces it; "scope unknown" is not autofixable and has no arm. Fails → do not start; HALT before execute and hand off to upstream `askme` / planning, where the user must supply an execution-ready task.

## Per-phase gate definitions

The semantic phases are **execute**, **simplify**, **review**, **finalize**, and **report**. Gate names correspond directly to each gated phase: **execute**, **simplify**, **review**, and **finalize**. `grill-core` is an autofix arm attached to `execute` (for verifier failure) and `review` (for critical and high findings), not an independent phase. `report` is terminal and gateless, running unconditionally on success or halt.

| Gate | Phase / operation | Pass criteria (exact) | Autofix arm A(P) | On RECHECK still-fail |
|------|---------------|-----------------------|------------------|-----------------------|
| execute | execute (orchestrated) | Orchestrated execution covers implementation and local verification only, returning a structured summary; the plan's steps are implemented and the repo-native verifier (build / type-check / test, as the repo defines) exits clean. It must not run the simplify, review, finalize, or CI phases; autopilot owns those. | `grill-core` once, in findings/verifier-failure mode, on the failing verifier output | HALT → hand off the verifier failure and the diff so far |
| simplify | simplify | `simplify` exits `0`, `11` (empty diff), or `12` (false-positive-only); behavior preserved. | none distinct, `simplify` self-reverts a behavior regression (its exit `13`) internally | HALT on exit `14` (new bloat) or `15` (mixed-concern commit): these need a human re-plan |
| review | review | After at most one `grill-core` pass and a re-review of the changed files, no critical or high finding remains. | `grill-core` once on the review's critical/high findings, then re-review changed files only | HALT → hand off residual critical/high findings |
| finalize | finalize (local checks, atomic commits, authorized push/PR) | Finalizer report returned: checks green and PR created/updated (full mode), or commits made and push skipped (local-only). The report carries review findings, check results, publication classification, and PR URL or local-only status. | none; a finalizer refusal (push refused, checks blocked) is a deliberate safety stop, not a defect to patch | HALT → hand off the finalizer's blocked report and the unpushed commits |

`grill-core` is an autofix arm (supporting `execute` and `review`), not an independent phase, and has no separate gate. `report` is the terminal reporting phase; it evaluates no gate and always runs.

## Local-only detection

Run `git remote`. Empty output → local-only; also forced by `mode:local`.

Local-only effect:
- finalize: the finalizer runs the local check suite, makes atomic commits, and skips push and PR creation. No remote is invented. The report states `mode: local-only` with the unpushed commit list.
- report: report still runs and the report states `mode: local-only` with the unpushed commit list.

## Halt handoff format

On `HALT(P)`, the report phase emits a handoff so the next operator resumes without re-deriving state:

```
HALT at <phase> (gate <gate-name>)
reason:        <one line — what the gate measured and why it stayed red>
autofix tried: <A(P) name + outcome | none — not autofixable>
residual:      <the findings / verifier output / refusal that remain>
state:         <commits made (sha + subject), pushed? PR url?, working-tree dirty?>
next:          <the single action that unblocks: e.g. "return to plan mode for a narrower approved plan", "resolve test X", "authorize push to <branch>">
```

## Report format (success or halt)

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
