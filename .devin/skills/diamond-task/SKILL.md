---
name: diamond-task
description: 'Use when one issue or PR is too large for a worker and partitions into disjoint write sets. Not for independent parallel tasks: use parallel-launch. No remote or irreversible changes.'
---

# Diamond task

One issue or pull request is too large or too entangled for a single worker, yet its whole writable surface splits cleanly into pieces no two workers need to touch at once. This skill turns that issue into a small production line: partition the work into disjoint write sets, run one isolated worker per set, union their diffs mechanically, and have a fresh reviewer approve the result. It is the sole generator of production task DAGs, and it works only on the local machine: named local run artifacts and declared target write sets, with the pre-run checkpoint as rollback. Nothing here reaches a remote or makes an irreversible change.

For genuinely independent parallel tasks that share no issue and no writable surface, use parallel-launch instead.

## What you need before starting

One issue or pull request with its acceptance criteria; the local target workspace, whose current bytes and metadata are the composition base; the checks each worker and the final composed result must satisfy; named local locations for the checkpoint, the isolated composition, and the run report; and any fixed ordering constraints between units of work (otherwise the partition itself decides which worker nodes are independent). The production task DAG comes from those units of work and their declared ordering constraints only. If required input, a checkpoint, isolation, or a required check is unavailable, return `blocked` without touching the target.

## Checkpointing the base

Capture the exact target base in the named checkpoint first. Then enumerate every target byte the task may create, replace, or delete: integration edits, formatting changes, and generated output the final result requires all count. An unenumerated byte is an uncovered byte later.

## Splitting the surface into worker nodes

Partition the complete writable surface into worker nodes with pairwise-disjoint write sets. Define each set by canonical target paths and, where a path is shared, by non-overlapping byte regions or insertion boundaries. Give every node its task, its allowed write set, the checks it must satisfy, the proof it must return, and only the inputs it needs. Every content byte the composer might otherwise have to author must belong to some worker node, because the composer authors nothing: it applies returned diffs by mechanical union inside the declared sets and changes nothing outside them.

Stop before running any worker if coverage is incomplete, any two sets overlap, or isolation cannot be provided. That stop is `split-falsified`: discard any isolated compositions, restore the target from the checkpoint if application began, keep the evidence, and emit no partial composition.

## Running and vetting the workers

Run every ready node in an isolated copy of the base. Each worker may change only its declared write set and must return its exact diff, its check results, and its proof. No worker approves its own result, and no worker approves the composition.

Validate each returned diff against its node contract before composing anything. An overlap, an out-of-set byte, or a failing check falsifies the responsible node: re-run only that node in fresh isolation and validate again. When the failure spans write sets or exposes missing partition coverage, the split itself is falsified instead of any one node.

## Composing without authoring

Rebuild the isolated composition from the checkpoint and union the validated worker diffs mechanically: reproduce every diff byte-for-byte, change nothing outside the declared write sets, and write no reconciling, improving, formatting, or completing content of your own. Verify the composed bytes against every returned diff and run the declared composed-result checks.

Attribute any composition mismatch or failing check to exactly one worker node, re-run only that node, then rebuild from the checkpoint and repeat validation. A mismatch that spans write sets falsifies the split. If a node repeats an equivalent out-of-set change, check failure, composition mismatch, or review finding after its isolated re-run, that node is terminally falsified (`node-falsified`): stop with the target unchanged or restored, the responsible node named, the falsifying evidence retained, and no partial composition emitted.

## The fresh review and the landing

Hand the validated composition and all proofs to a fresh isolated reviewer who was neither a worker nor the composer; only that reviewer may approve. A review finding falsifies exactly one worker node (re-run it, rebuild from the checkpoint, repeat composition, checks, and fresh review), or the split when the finding spans write sets.

After approval, apply the reviewed mechanical union to the named target and verify its bytes equal the approved composition. Record everything in the run report: the node contracts, the diffs, the proofs, the composed check results, the reviewer identity and verdict, and the final byte comparison. Never report approval unless the composed checks, the byte comparison, and the fresh-review verdict all pass in the same replay.

On success return `approved` with the applied composed local result and that run report. On a clean stop return `blocked`, `split-falsified`, or `node-falsified` with the unchanged or restored target, no partial composition, the responsible node or split, and the falsifying evidence. Report either case in run order: checkpoint → partition → run → validate → compose → attribute → review → apply.
