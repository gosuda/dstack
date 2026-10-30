---
name: browser-qa
description: 'Use when the user runs /browser-qa for report-only QA results without entering a fix loop. Not for remote, credential, publish, deploy, or irreversible changes.'
disable-model-invocation: true
---

# Reporting QA results without fixing anything

You run one QA verification pass and hand back report-only results. You write a single local report under the working tree and then you stop. There is no fix loop, no source edit, and no further checks after the report goes out.

You may write that one report file and nothing else. Rollback is deleting the report. No remote mutation and no source or VCS mutation.

## What you need before you start

- The working tree or change set to verify. Supply a scope (paths or diff range) to narrow the pass. Without one, verify the whole tree.
- Optionally, an ordered list of check commands to run. If omitted, run the project's configured QA checks in order: build, then tests, then lint.

## Running the pass

Bound the scope first. Use the supplied paths or diff range, or the whole tree when none is given. Do not read or change files outside that boundary.

Run each configured QA check in order (build, then tests, then lint). Capture exit status, stdout, and stderr for each one. Every check ends either run or recorded as non-runnable, with nothing skipped silently.

Write the findings to one local QA report file under the repository working tree. The report holds per-check status (what ran, what did not, exit status for each) alongside the findings tagged by check name and severity. Then return the same per-check status and findings as the result. After that point, do not apply fixes, edit files, or run more checks. This report-only variant intentionally skips the fix loop.

## When checks misbehave

- A check command is missing or non-runnable. Record the command name and error in the report and continue with the remaining checks. Do not substitute a different command.
- A check returns non-zero. That is a finding, not a skill failure. Record it and proceed to the next check.
- The report file is unwritable. Return the findings inline, state that the write failed, and do not leave a partial file behind.
- Rollback is deleting the report file. No source, VCS, or remote state is touched, so nothing else is required.
- When a requested check never ran, say so. Return a report listing which checks ran, which could not, and the findings collected. Never claim the pass is complete when a requested check never ran.
