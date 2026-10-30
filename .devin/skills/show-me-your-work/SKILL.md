---
name: show-me-your-work
description: 'Use when the user invokes it to append a structured decision record to an append-only TSV log, ending with an Attention section for reviewers. Not for an ephemeral visual: use show-me.'
---

# Show me your work

You keep an auditable trail for unattended work by appending one structured decision record at a time to an append only TSV log, closing with an Attention section that tells a reviewer what needs eyes. For an ephemeral chat visual, use show-me instead. This skill only writes the named local artifacts; a manual revert of the appended row is the rollback.

A decision here means a deliberate choice made without direct human guidance that produces artifacts, code, documentation, or non trivial state changes. Routine implementation, style fixes, and unchanged scope do not qualify, and you record nothing for those.

## What you need from the caller

| Input | What it is |
|---|---|
| log_path | Path to the append only TSV decision log. Required, with no default. It must sit inside the project tree. |
| session | Current session identifier. Required. |
| task | The current task description. Required. |
| context | Extra framing or constraints. Optional. |
| reviewer | Reviewer identifier for the Attention section. Optional; use `pending` when not yet known. |

## Recording a decision

Steps 1 through 4 prepare the row, step 5 writes it, step 6 flags the reviewer. Nothing is appended until validation passes.

1. Decide whether anything qualifies. Name the deliberate choice and check it against the decision test above. If nothing qualifies, stop and say so.
2. Mint the decision ID. When `log_path` uses a sequence counter at `.decision-counter`, read the current integer N and increment it. Otherwise generate a UNIX timestamp based ID.
3. Gather the eleven fields: `timestamp` (ISO 8601 UTC), `session`, `decision_id`, `context` (task plus context inputs combined), `decision`, `rationale`, `alternatives`, `consequences`, `evidence` (file paths, command outputs, or transcript references), `reviewer` (as supplied, or `pending`), `status` (always `pending` on write).
4. Validate before appending. Stop without writing when any of `decision`, `rationale`, or `evidence` is empty, or when `log_path` points outside the project tree.
5. Append one tab separated row. Write the eleven fields in this order: timestamp, session, decision_id, context, decision, rationale, alternatives, consequences, evidence, reviewer, status. When `log_path` does not yet exist, create it first with this header line: `timestamp\tsession\tdecision_id\tcontext\tdecision\trationale\talternatives\tconsequences\tevidence\treviewer\tstatus`.
6. Flag the reviewer. Append a blank line and a section titled `## Attention` with the one line summary: "Decision [decision_id] by [session] requires reviewer review." The reviewer named there matches the row's reviewer field.

## When the write fails

- Missing log file: create it with the header line above, then proceed. This is automatic recovery, not an error.
- Tab or newline inside a field: stop with `malformed-input` and append nothing.
- Empty decision, rationale, or evidence: stop with `validation-failed` and append nothing.
- Append failure: stop with `log-write-failed`. The evidence trail is incomplete, so the run's completion claim does not hold.

## What you hand back

The appended TSV row at `log_path` with all eleven fields in order, followed by the blank line and `## Attention` section. The record counts as complete only once both the row and the Attention section are written.
