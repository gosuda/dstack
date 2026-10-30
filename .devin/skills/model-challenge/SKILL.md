---
name: model-challenge
description: 'Use when a user requests an independent Codex or Gemini review of uncommitted code, a branch diff, or a specific commit. Do not use for unconfirmed or unattended review sends, or source mutation.'
disable-model-invocation: true
---

# Second opinion external review

You send a selected code diff to an independent external reviewer, Codex or Gemini or both, and return structured findings with exact locations and confidence where supported. When both reviewers run, you also summarize where they agree and disagree. The run is complete when each selected reviewer has returned findings on the complete diff or is explicitly reported unavailable, with empty and oversized scopes handled before anything is sent.

This skill changes nothing locally. The only mutation is sending data to an external reviewer, which cannot be undone once the user confirms it, so there is no rollback; unconfirmed or unattended sends are out of scope, and so is mutating source.

Sending the diff costs money through a paid API and moves code outside the local environment, so it needs explicit human invocation. Before credentials, data-at-rest changes, paid actions, publishing, deployment, remote bulk mutation, or irreversible deletion enter the picture, you preview the target and consequence and proceed only with approval.

## What you send

Two inputs are required: the code diff or commit reference (uncommitted changes, a branch diff, or a specific commit SHA), and the reviewer selection (Codex, Gemini, or both). An optional focus area narrows the lens (security, performance, error handling, or general), and optional project guidance adds codebase context or review priorities to the reviewer prompt.

Resolve the diff from the supplied reference first. For uncommitted changes, capture the working-tree diff. For a commit or branch diff, resolve the full diff against the merge base. Either you hold a single diff string whose range matches the reference, or you report that the reference could not be resolved and stop.

Then validate scope. An empty diff means stop and report that there is nothing to review. A diff larger than the selected reviewer's context window means stop, report the size, and ask the user to narrow scope. Nothing is sent in either case. Record any focus area and project guidance, or confirm both absent, so the reviewer prompt can be assembled without another round trip.

## Confirming the send

Before anything leaves the local environment, present a preview: which reviewer or reviewers will run, what diff content will be sent, and the fact that this is a paid external action with data leaving locally. Proceed only on explicit confirmation. When the user declines, nothing is sent.

## Running the reviewers

Invoke each selected reviewer. Codex runs in a read-only sandboxed environment; collect its structured findings response. Gemini headless invocation may auto-approve extension tool calls, so the invocation itself needs explicit user authorization; collect its structured findings response. Never substitute one reviewer for another without user approval: when a reviewer is unavailable or returns an error, report that reviewer explicitly. When one reviewer succeeds and the other fails, include the findings you have and note the failure. When both are unavailable, report both and stop.

When more than one reviewer ran, synthesize: list the agreements (both reviewers flag the same issue) alongside the per-reviewer findings behind them, and the disagreements (one flags what the other does not). A single-reviewer run skips this step.

Compile the final report with one section per reviewer that ran (exact file paths, line numbers, confidence levels where supported), the synthesis section when more than one ran, and an explicit note for each reviewer that was unavailable. Scope limits and partial results are noted as they are: whatever was returned is reported, partial findings are never suppressed, and a completed review is never claimed where the run fell short.

| Situation | What you do |
|---|---|
| Empty diff | Stop before invocation and report that there is nothing to review |
| Oversized diff | Stop before invocation, report the diff size, and ask the user to narrow scope |
| Reviewer unavailable | Report that reviewer explicitly, without silent substitution |
| User declines the preview | Stop and send nothing externally |
| Reviewer returns an error | Report the error for that reviewer, keep the other reviewer's findings when they exist |
| Partial results | Report whatever was returned, never as a complete review |

## What you hand back

A structured review report: per-reviewer findings with exact file paths, line numbers, and confidence where supported; multi-reviewer synthesis of agreements and disagreements when more than one reviewer ran; and notes on unavailable reviewers, scope limits, and partial results.
