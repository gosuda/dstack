---
name: workflow-evidence-mining
description: 'Use when authorized workflow history may contain a repeated process worth extracting and replay-testing. Produces a contradiction-tested workflow mined from authorized history.'
disable-model-invocation: true
---

# Mining a workflow out of past history

You turn repeated past successes into a workflow you can trust. You read only the history the user authorized, look for a process that succeeded at least three times independently, try to break it against the rest of the record, and replay it once on a fresh instance before calling it done.

You never change anything outside this reading. No file, VCS, credential, paid, published, deployed, or remote mutation. The authorized corpus is your whole world, and the pass cap bounds how long you keep looking.

## Freezing the scope

Start by pinning down the two things that bound the run:

- The authorized corpus: the workflow history you are allowed to read.
- The pass cap: the maximum number of extraction-replay cycles before you declare insufficient evidence.

Freeze both and record them before any extraction begins.

## Mining, testing, then replaying

Work the candidates in this order:

1. Hunt the authorized history for repeated processes. A candidate counts only with at least three independent high-confidence success instances behind it. List each candidate with its supporting instances.
2. Extract the candidate by naming the steps, inputs, outputs, decision points, and stop conditions that recur across the supporting instances, and document them.
3. Try to break it. Search the corpus for instances that contradict any step or decision point. If a contradiction can be reconciled, revise the workflow to account for it. If it is structural, kill the candidate.
4. Replay a survivor on a fresh instance from the corpus and confirm it reproduces the success path. A replay that fails kills the workflow.

## Knowing when to stop

- A contradiction you cannot reconcile ends the candidate (terminal class `contradicted`).
- History holding fewer than three independent high-confidence successes for every candidate ends the run (terminal class `insufficient`).
- Hitting the pass cap before anything survives ends the run (terminal class `blocked`).
- A workflow that survives three successes and the fresh replay is terminal class `extracted`.

## What you hand back

The mined workflow: its named steps, inputs, outputs, decision points, stop conditions, the supporting instances, the contradiction-test results, and the replay result, plus the terminal classification (`extracted`, `contradicted`, `insufficient`, or `blocked`).
