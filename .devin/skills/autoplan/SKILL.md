---
name: autoplan
description: 'Use when the user runs /autoplan on a plan or idea. Reviews, amends, and derives purpose-named tasks with a final human approval gate. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Autoplan

An idea or plan goes in; an amended plan and an appended task ledger come out, presented at a final approval gate where you stop for the human decision. Nothing here executes, publishes, or reaches the network. All effects are reversible local artifacts, discarded to recover the pre-run state.

## What goes in

The one required input is a plan or idea to develop, supplied as a file path or inline text. A file path is read; inline text is used directly. With no plan or idea supplied, stop before any write and report that. An existing `tasks/autoplan-ledger.jsonl` may ride along to extend. When absent, it gets created.

## The ledger and task naming

`tasks/autoplan-ledger.jsonl` carries the task list. Create it when missing. Otherwise append new tasks to the end, never overwriting or truncating existing entries. Each run appends only the tasks it produces.

Internally, preserve existing stored ledger `id`, `description`, and `phase` fields and values, and never migrate user records. Each ledger line is a JSON object with `id`, `description`, and `phase` keys. For internal sequencing and tracking, each task ID joins its reviewing phase prefix (`CEO`, `DES`, `DX`, `ENG`) to a zero-padded sequence number within that phase:

| Phase prefix | Internal ledger IDs |
|---|---|
| CEO review | `CEO-01`, `CEO-02`, and so on |
| Design review | `DES-01`, `DES-02`, and so on |
| DX review | `DX-01`, `DX-02`, and so on |
| Engineering review | `ENG-01`, `ENG-02`, and so on |

Sequence numbers continue from the existing ledger. For each phase prefix, scan the file for the highest existing sequence number and increment from there, starting at `01` when the prefix has no prior entries. Tasks increment in the order identified. The same plan evaluated the same way against the same ledger produces the same internal IDs. A phase with no tasks leaves its prefix unused.

For human presentation, plans, tasks, headings, and TODOs must use the actual purpose, never phase+counter labels (`CEO-01`, `DES-01`, `DX-01`, `ENG-01`), parenthesized opaque IDs, or decorative coded task prefixes. Always display the semantic description of what the task accomplishes. Genuine fixed external metadata IDs (such as internal ledger fields) remain intact internally, but human labels name the concrete work directly.
## How the review runs

Read the supplied plan or idea. Then run the four review phases: CEO, design, DX, and engineering. Each phase judges the idea against clarity, impact, audience, risk, sequencing, and reversibility, recording its decisions in the register. A phase that cannot reach a decision records the open question and the remaining phases continue. The plan is amended with the consolidated decisions from all four phases.

From the four phases come implementation tasks. Assign internal deterministic IDs per the rules above, append one JSON line per task to the ledger, and update TODOs to reflect the aggregated tasks using their actual purpose and semantic description.

Present the amended plan and aggregated tasks at a final approval gate, naming tasks and headings by their actual purpose without opaque coded labels. Stop there for the human decision. Do not proceed to execution.

## When the run stops instead

A missing input stops everything before any write. An undecided phase never blocks the others: its open question lands in the register, the rest continue, and the question surfaces at the approval gate. A ledger write failure discards the partial append, and the result is reported as blocked with the phase reached rather than done. Until the approval gate is reached and presented, the outcome is blocked, never done.
