---
name: perspective-complete-review
description: 'Use when one named review viewpoint must run fix cycles until a fresh reviewer finds nothing. Not for multi-viewpoint review or remote, credential, publish, deploy, or irreversible changes.'
disable-model-invocation: true
---

# Reviewing one viewpoint until it goes quiet

A review that lists findings and stops leaves the author guessing whether the fixes worked. This skill picks one viewpoint (logic, races, panics, vulnerability, or another single perspective the user names), then runs review and fix cycles until a fresh reviewer looking at the current code finds nothing from that seat. It is the only one of your five owned skills that writes: only the reviewed artifact, its fix patches, a baseline snapshot, and one review report for this viewpoint. Rollback is restoring the recorded baseline. Nothing remote, no VCS history rewrite, no credential, paid, published, or deployed mutation. No file outside the declared review scope is touched, and you never edit an out-of-scope file to make a fix fit.

## Set the run up

You need:

- Reviewed artifact (required): one local file, diff, or directory. It must exist and be writable before the run starts.
- Viewpoint (required): exactly one named seat. A run covering two viewpoints is invalid.
- Acceptance checks (optional): commands or test invocations proving the artifact still works. When none are supplied, every verdict is reported as reviewer-verified only, which is a weaker claim than check-verified. Say which one each result is.
- Cycle budget (optional): maximum review cycles before the run stops. Default 5.
- Baseline (optional as a supplied input, mandatory as a step): version control state or a file copy from before the first fix. When the user supplies neither, the run creates a file copy.

Bound the scope before mutating anything. Confirm the artifact is local and writable and exactly one viewpoint is named. When the artifact is missing, not local, or zero or several viewpoints were named, stop before any write and return `blocked`, naming the missing or conflicting input.

Then record the baseline (version control state or file copy) and run the acceptance checks once to capture the starting result. Record `no checks supplied` when none were given.

## State what this seat sees

Write the viewpoint charter at the top of the review report: the viewpoint name, what it examines, what it ignores, and the ownership split. Findings about logic, races, panics, and vulnerabilities are machine-owned and fixable here. Findings about taste, architecture, and problem choice are human-owned: record them as questions only, never fix them.

## Run the cycle

1. Review with a fresh reviewer. Each cycle starts from an isolated context: the reviewer sees the current artifact state and the viewpoint charter only, never earlier cycle reports, fix justifications, or debate history. When more than one model family is available, run the reviewer on a different family than the one applying fixes. With only one family, keep the isolation and mark the cycle `same-family`. Record which family each cycle used.
2. Return each finding as location, concrete defect, evidence, and a minimal fix proposal. Drop findings outside the viewpoint charter or outside the artifact; list the out-of-scope ones under human questions instead of fixing them.
3. Apply fixes one at a time. For each machine-owned finding inside scope, apply the minimal patch, re-run the acceptance checks, and record the patch (file, location, change, check result) in the report. Revert any fix whose checks fail or whose completion would need edits outside the artifact, and record it as unresolved with the evidence.
4. Repeat from step 1. The viewpoint is quiet only when a complete fresh-reviewer cycle returns zero findings. Stop with `non-converged` when the cycle budget runs out without a zero-finding cycle, or earlier when the same defect is re-reported after its fix was applied and check-verified. A quiet claim comes only from a zero-finding cycle, never from exhausting the budget.

## When the run breaks down

- A review cycle errors out or no reviewer is available: stop the campaign, keep fixes already applied and check-verified, and return `blocked` with the report showing the last completed cycle. Never substitute an unrun cycle with an assumption of quiet.
- A fix fails its acceptance checks or needs out-of-scope edits: revert that patch immediately, record it as unresolved with evidence, and continue with the remaining findings.
- The user rejects the result: restore the baseline so the artifact returns to its pre-run state and mark the report reverted.
- Nothing is swallowed: every error, revert, and unresolved finding appears in the report, and the terminal classification reflects the state that actually held at stop time.

## What you hand back

One review report next to the reviewed artifact (`<artifact-basename>.<viewpoint>-review.md`, or a user-supplied path) holding the viewpoint charter, the per-cycle log with model family, every applied fix patch with its check result, human-owned questions, unresolved findings, and the terminal classification. The artifact itself carries the check-verified fixes, or the restored baseline when the user rejected the result.
