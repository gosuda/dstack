---
name: contraint-driven
description: 'Use when no quality bar is written down, when setting up constraints, or when implementing under non-negotiable budgets, limits, or API rules. Not for one-off spikes or remote, credential, publish, deploy changes.'
---

# Constraint-driven development

Write the quality bar down as measurable checks, then implement under it so the delivered change verifiably satisfies every constraint without regressing anything else. Use this when no bar is written down, when setting one up, or when working under non-negotiable budgets, limits, or API rules. It is the wrong tool for one-off spikes, and it never touches remotes, credentials, publishing, or deploys: everything it writes is a local constraints record plus local code, and rollback is undo.

## What you work with

You need the non-negotiable constraints, each stated as a measurable predicate with a target value and a checkable condition. Prose without a measurable form must be converted to one before any code is written; never proceed on prose and never substitute a self-invented target for a missing number. You may also start from an existing constraints record or from user-supplied target numbers; otherwise measure the current state and hold the line.

## Learn the tree before asking anything

Read the target tree once to learn its language, stack, test runner, and any existing constraints record. Report what you found in two lines, then ask only what is left; never ask for what is readable. In CI or autonomous runs with no live user to interview, apply the floor only, note that choice, and flag the rest for a human.

## Ask at most four questions, each with a usable default

Ask which dimensions beyond the floor matter, whether a mid-task failure blocks or warns, whether to measure today and hold the line or adopt a supplied number, and what slowest check is tolerated before handoff. Every question carries a default so that no answer still yields a working config. Then stop at four.

## Write the bar down in one CONSTRAINTS.md at the repo root

The file is canonical; any scripts you add later are convenience wrappers that must mirror it, and on drift the file wins. It carries four parts:

- A floor that is always enforced without setup: no new suppression comments, no unimplemented stubs, no skipped or deleted tests without a reason in the commit message, no secrets in source, and the file itself is never weakened to make a change pass.
- An enforced table with one row per dimension carrying Dimension, Rule, Checked by, and Runs at. Every row names the command that produces the verdict; a dimension with a number and no command is an aspiration, not a constraint.
- A measured table with today value and direction for ratchets.
- An exceptions table with ID, Rule, Path, Reason, Owner, and Expires.

Then point the project instructions at the file with one line: read CONSTRAINTS.md before writing code and do not weaken it to make a change pass. The bar is written when every number has a stated reason and every enforced row names its check command.

## Install only what each chosen dimension needs

Reuse the project existing config and de facto checkers: types, lint, coverage on changed lines, secrets scanning with redaction, code and dependency security scanning, page performance against a running URL, bundle budgets, accessibility scanning, architecture boundary checks, and mutation on touched files where the budget allows. Wire the project own scripts so checks reproduce without an agent: a fast check after an edit, a task check when done, and a full check in CI. Lighthouse and axe need a running URL and belong against a preview deploy or a started local server; when the project has no URL to hit, drop the dimension rather than inventing a check that cannot run. Scope expensive checks to the diff: read coverage from the already-written suite output intersected with the diff instead of running the suite twice. Each chosen dimension ends with a runnable mechanism or is explicitly dropped as inapplicable.

Starting numbers with their reasons: changed-line coverage at least 80 percent, high enough to force a test and low enough to allow a config line; project coverage holds its today value; mutation at least 60 percent to start; dependencies nothing at high or above; LCP at most 2500ms and CLS at most 0.1 per Core Web Vitals good; accessibility zero critical or serious axe violations; exception lifetime 90 days; ratchet tolerance 0.5 percent. State the number and the reason together.

## Bound the scope and capture the baseline before mutating

List the files the work will touch; constraints apply to the diff, not the whole tree, unless a constraint is explicitly project-wide. Run each constraint checked-by command against the current tree and record the measured value. That baseline is the floor: the delivered change must not produce a worse value for any constraint.

## Implement, checking fast after each edit

Make the change, running the fast subset of checks scoped to the touched files after each edit.

## Validate against both guards

Re-run every checked-by command on the delivered change and compare against the baseline: tightening is silent, loosening is a violation. Watch the diff for the five cheap roads to green: a moved threshold, an eased test, a silenced checker (including istanbul ignore, Stryker disable, nosemgrep, and gitleaks allow), unfinished work standing in for implementation (a stub, an empty catch, a TODO), and a new exceptions row. Compare CONSTRAINTS.md against its branch-point state; loosening must be loud. Rank checks by circularity: external checks encode outside facts, project checks encode human-owned rules, and the project own suite is the only genuinely circular kind, so keep at least one external check in the bar. Adapt the bundled floor-guard reference in `references/floor-guard.md` rather than inventing a second checker. The change validates when every constraint is re-measured with none worsened and no bar-weakening move remains in the diff.

A constraint that cannot be re-measured after the change is unverified: do not treat the change as clean; report that the guard could not run and hold the change for a human. A constraint that fails at task end is fixed in the code, not the constraint; relaxing a threshold is a separate human decision recorded as an exception, not a side effect of implementation. A baseline-guard violation is fixed in the code or routed through a tracked exception with an owner and an expiry; the constraints record is never weakened to make a change pass.

## Run the full set to finish

Run every checked-by command against the complete change plus the project test suite, scoping expensive checks to the touched files. Deliver only the subset of changes for which every constraint verifiably holds and revert the rest; never claim completion for work that was not checked.

## What you leave behind

CONSTRAINTS.md naming each invariant with its check and baseline value, the delivered code change in which every constraint holds without regression, and a check-run report stating which constraints passed, which baseline-guard violations were flagged (none on success), and any constraint that could not be checked and why. The record verifies when the file exists, every number has a stated reason, every enforced row names its check, exceptions carry owner and expiry, instructions point at the file, and a trial run on the current branch produces no failures the user disagrees with. When checks outgrow a shell script, escalate from written-only to scripted checks in the edit hook and CI, then to a dedicated runner; a first run may be floor-only with no installs.
