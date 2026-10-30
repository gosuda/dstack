---
name: watch-for-harness-mode
description: 'Use when a proven watch pattern should become a reusable harness artifact with configurable inputs. Not for remote, credential, publish, deploy, or irreversible changes.'
disable-model-invocation: true
---

# Watch for harness mode

You turn a watch pattern that has already proven itself into a reusable harness artifact with configurable inputs. The harness file is the only thing you write, and deleting or reverting it is the rollback. No version control commits, no remote calls, no credential use, no published artifacts.

## What you need from the caller

| Input | What it is |
|---|---|
| Watch transcript | The proven pattern: a session transcript, run log, artifact, or notes documenting the watch target, interval, evaluation logic, completion predicate, and observed success. Required. A failed or non converged watch does not qualify. |
| Harness name | A slug for the harness artifact file, with no path separator characters. Required. |
| Harness description | One sentence saying what the harness checks and when it succeeds. Optional, defaults to "Reusable harness derived from a proven watch pattern." |
| Default poll interval | Polling interval in seconds. Optional, defaults to the interval observed in the transcript, or 60 when the transcript states none. |
| Default deadline | Maximum polling duration in seconds. Optional, defaults to the deadline observed in the transcript, or 300 when the transcript states none. |
| Adoption confirmation | The user explicitly confirms or declines the finished harness. Required at the end, never assumed. |

## Building the harness

These steps run in order.

1. Check the inputs. Reject a transcript with no observable target, completion predicate, or evaluation logic, and reject a transcript whose watch failed or never converged: without documented observed success there is nothing proven to reuse. Also reject a missing harness name or one containing path separators. Stop on any of these, writing nothing.
2. Confirm the scope is clean. The harness artifact is the only write target. When a file with the harness name already exists in the working directory, stop and report the collision. Never overwrite it.
3. Pull the mechanism out of the transcript: the target surface watched, the completion predicate that determined success, the evaluation logic that applied the predicate, the poll interval, and the deadline. When any of the five is missing, stop and name the missing element. Partial extraction is not enough.
4. Write the draft harness as `{harness-name}.md` (or the user's preferred extension). It carries the harness name, the description or its default, the extracted target, completion predicate, and evaluation logic, plus configurable input fields for target, completion predicate, poll interval, and deadline with their extracted defaults, and the adoption confirmation step.
5. Show the draft to the user and ask for an explicit confirmation or declination. Do not assume adoption.
6. Close it out by what the user says. On confirmation, mark the harness adopted and report success. On declination, delete the artifact and report withdrawal; that outcome is terminal, not a failure, so do not retry or re-prompt. On a modification request, record the requested changes and stop. This skill produces an initial draft, not an iterative editor.

## What you hand back

One terminal result: adopted (the harness artifact exists and the user confirmed, with name and path), withdrawn (the user declined, the artifact is deleted, no harness exists), or blocked (input validation failed or the transcript was insufficient, with the blocking reason named).
