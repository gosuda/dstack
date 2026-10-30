---
name: diagnose-loop-health
description: 'Use when a configured loop misbehaves, produces unexpected results, or its setup soundness is questioned. Not for tasks that require source or remote-system changes, not for loop design.'
---

# Diagnose loop health

A configured loop is misbehaving, or someone asks whether its setup is sound. Your job is to look, not to fix: inspect the loop's directory read-only, decide how bad things are, and name the most impactful next actions. You never change source code, touch version control, use credentials, spend money, publish, deploy, or reach a remote system, and you never redesign the loop itself.

## What you need from the caller

Ask for the loop directory to inspect. If it is not named, stop and ask; do not infer one, guess one, or create one. Nothing in this skill creates or writes a file.

## Reading the four files

Bound yourself to read-only inspection of that directory: no writing, creating, renaming, deleting, or moving anything. Locate and read the four files that define a loop's health:

- the charter file, stating what the loop is for and its cadence;
- the state file, recording where the loop stands;
- the gate file, carrying the gate thresholds;
- the budget file, carrying the budget limits.

For each file record presence and freshness. A file that is absent is missing. A file whose content no longer matches the loop's declared cadence, gate thresholds, or budget limits is stale. If any required file cannot be read at all, permission denied or parse error alike, you are already done classifying (see below): never skip it silently, never mutate it, never swallow the error, and never claim the loop is fine while a file sits unread.

## Calling the severity

Place the loop on one rung of the ladder:

- **healthy** when all four files are present and current;
- **warning** when a file is missing or stale but the loop can still run;
- **blocked** when a required charter or state file is absent or unreadable.

Where both warning and blocked conditions hold, take the higher rung. No partial verdicts: one unreadable required file escalates the whole report to blocked. A missing loop directory is itself blocked: name the absent directory and stop.

## What you hand back

A severity report with the matching exit code: 0 for healthy, 1 for warning, 2 for blocked. For warning or blocked, add at most three prioritized actions ordered by impact, each naming the exact missing or stale file by path and by class (charter, state, gate, or budget). Healthy carries no actions. The report reads in the order you worked: directory obtained, scope bounded, files read, severity classified, actions emitted, exit code.
