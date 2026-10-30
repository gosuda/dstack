---
name: triage
description: 'Use when issues or external pull requests must move through a category and state machine with verification, grilling, and agent-ready briefs. Not for Slack channel reports (use issue-triage).'
disable-model-invocation: true
---

# Move issues and pull requests through triage

A maintainer points at work needing attention, and you move each item through a category and state machine with evidence behind every step: classify it, verify the claim, sharpen it when it needs sharpening, and draft the brief or notes that carry it out of `needs-triage`. A pull request is an issue with an attached diff and follows the same roles, states, and machine, with the diff deltas noted below; a GitLab merge request follows the same machine with the MR deltas in each step.

Every outbound write stays human-gated. Preview each comment, label change, close, and knowledge-base file write with its exact target and text, and proceed only with explicit approval for that write. Local reads, verification, classification, and brief drafting are reversible local work and need no approval. No credential use, no paid action, no remote mutation without approval.

Two category roles exist: `bug` for something broken, `enhancement` for a new feature or improvement. Five state roles exist: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On a pull request the same states read against the attached diff: `ready-for-agent` means a brief is attached and an agent takes the next step on the diff; `ready-for-human` means a human merges it. When state roles conflict on one item, flag it and ask the maintainer before doing anything else.

## Bind the tracker before touching anything

You need four things. The maintainer request: what to show, or which `#number` or URL to triage; resolve a bare number per the tracker configuration and never guess across trackers. The role mapping: the tracker label strings for the canonical roles, or local-only roles when no tracker is configured; the local path is complete and needs no tracker, no credentials, and no cloud service. A repository checkout with readable code, the domain glossary, ADRs, and `.out-of-scope/` records. And the provider binding: derive the forge from the verified request URL or the checkout remote, never default to GitHub. A bare `#number` is ambiguous wherever issues and MRs live in separate IID spaces, so stop and ask which item is meant. On GitLab bind host, project path `GROUP/PROJECT`, MR IID, and head SHA separately, keep the source project distinct from the target project on forks, and enumerate every list page until a page returns short.

Without a role mapping and no local-only agreement, stop before any remote write and never invent label strings.

## Show what needs attention

Query the tracker, or list the local intake when no tracker is configured, and present three buckets oldest first: unlabeled (never triaged), `needs-triage`, and `needs-info` with reporter activity since the last triage notes. Tag external pull requests `[PR]` versus `[issue]` when pull requests are in scope; discovery covers only external pull requests per the tracker configuration, while an explicitly named pull request always gets triaged regardless of author. Show counts with a one-line summary per item and let the maintainer pick. The bucket view ends when the maintainer picks an item or asks for a state overview.

On GitLab, discover MRs with `glab mr list` and explicit state flags (`-A` all, `-c` closed, `-M` merged, `-d` draft; default is open), people, branch, and label filters (`-a`, `--author`, `-r`, `-s`, `-t`, `-l`), `-P`/`--per-page` with `-p`/`--page` looped to exhaustion, and `-F json`; tag external MRs `[MR]` versus `[issue]`. An MR IID is project-scoped and is never a GitHub node ID; `opened` is the GitLab open state.

## Gather context, then recommend before acting

Read the full item: body, comments, labels, author, dates, the diff for a pull request, plus prior triage notes so resolved questions never get re-asked. Explore the codebase with the domain glossary while respecting ADRs. Run two checks: redundancy, searching for an existing implementation by domain concept rather than request wording alone and reporting where you searched; and prior rejection, reading `.out-of-scope/*.md` and surfacing any concept match. A found implementation points at an already-implemented `wontfix`.

On GitLab read the MR with `glab mr view <iid> -F json` (add `-c`, with `--resolved`/`--unresolved` for the discussion census) and record the head SHA from `sha` plus source and target branches and projects; keep `detailed_merge_status`, approvals state, and draft state as separate facts, never as GitHub statuses. Treat an item as already-implemented only on a merged MR closing reference, a default-branch commit carrying a closing keyword, or behavior verified in current code; age, an open or unmerged mention, or an assumed implementation never resolves.

Tell the maintainer the recommended category and state with reasoning plus a short codebase summary, including whether the behavior already exists, and wait for direction. This step ends when the maintainer confirms, redirects, or invokes a quick state override.

## Verify the claim before any grilling

For a bug, reproduce it from the reporter steps. For a pull request, check out the diff and run the relevant tests or commands. Report confirmed (with code path), failed, or insufficient detail, which is a strong `needs-info` signal. A confirmed verification makes a far stronger brief.

On GitLab check out the head with `glab mr checkout <iid>` (fork-safe; `-R GROUP/PROJECT` selects the target project) or an equivalent MR-head worktree, then run the relevant tests or commands against the recorded head SHA. This step ends when the verification outcome is recorded.

## Grill only when the request needs it

When the request needs fleshing out, grill it into shape one question round at a time, sharpening domain terms and updating `GLOSSARY.md` or ADRs inline as decisions land. Skip grilling on a quick state override; when moving to `ready-for-agent` without grilling, ask whether the maintainer wants a brief written. This step ends when the request is sharp or the override path is taken.

When a term resolves while updating the glossary inline, record it at once with exactly three parts: the canonical term, a one-or-two-sentence definition of what the term is, and rejected synonyms on an `_Avoid_` line. Offer an ADR only when the decision is hard to reverse, would surprise a future reader without context, and resulted from a real tradeoff with genuine alternatives; otherwise record why no ADR was written. Continue the detected ADR directory, filename scheme, and headings without adding numbering where none exists; a new ADR directory uses semantic filenames with no numeric prefix; never delete an ADR file. Reverse a decision by writing a new ADR that supersedes the old and marks the old accordingly.

When prior triage notes exist, read them first, check reporter answers against outstanding questions, present the updated picture, and continue without re-asking resolved questions.

## Apply the outcome, one approved write at a time

Preview each write with its exact target and text and execute only after approval:

- `ready-for-agent`: post the agent brief per `references/agent-brief.md`.
- `ready-for-human`: same brief shape, plus why it cannot be delegated (judgment calls, external access, design decisions, manual testing).
- `needs-info`: post triage notes, what is established so far plus specific actionable questions for the reporter, never a bare request for more information:

```markdown
## Triage Notes

**What we have established so far:**

- point 1
- point 2

**What we still need from you (@reporter):**

- question 1
- question 2
```

- `wontfix` already implemented: comment pointing where the behavior lives and close. Never write built behavior to `.out-of-scope/`.
- `wontfix` rejected bug: polite explanatory comment, then close.
- `wontfix` rejected enhancement: write or append the `.out-of-scope/` concept file per `references/out-of-scope.md`, link it from the comment, then close.
- `needs-triage`: apply the role, with an optional comment on partial progress.

Every comment or issue posted to a shared tracker during triage starts with:

```text
> *This was generated by AI during triage.*
```

On GitLab every write below runs only after exact-target-plus-text approval, as a separate command with per-action reporting. No MR command carries a general dry run, so the preview is the gate, not a flag:

- Brief, triage notes, or disclosure-prefixed comments: `glab mr note create <iid> -m "<text>"` (long bodies travel on stdin, never interpolated into argv; diff-positioned notes add `--file` with `--line`/`--old-line`); thread replies go through `glab api projects/<GROUP%2FPROJECT>/merge_requests/<IID>/discussions/<DISCUSSION_ID>/notes --input <file>` (the body file carries the exact approved text as JSON; read the discussion back to confirm the reply landed).
- State roles: `glab mr update <iid> -l/--label` and `-u/--unlabel` against the pre-agreed role mapping; never invent label strings.
- `wontfix` close: post the closing note first, then `glab mr close <iid>` (`close` carries no comment flag; `glab mr reopen <iid>` reverses). Closing keywords in an MR description (`Closes #N`) auto-close linked issues on merge.
- `ready-for-human` on an MR means a human merges it. Triage never merges; merging belongs to the merge owner under its own authority.

## When to stop instead

Stop and ask the maintainer before anything else on a role conflict or an ambiguous item: a bare number matching an issue and a pull request, a bare number colliding across GitLab issue and MR IID spaces, or an unknown tracker or host. Never guess across trackers or forges. Keep the local classification and drafted brief when a write is declined, record the declined write, and never treat invocation as approval. Report a failed write with its target and continue past it to remaining approved writes. Record what could not run when verification is blocked, and treat that as insufficient detail rather than confirmation.

Local classification, verification evidence, and drafted briefs survive any write failure or declination. Never claim triage is complete while an in-scope item still sits in `needs-triage` without a role or next step.

## What you hand back

Per item: exactly one category role and one state role, the verification outcome with code path or failure evidence, the posted brief or notes (with the disclosure line on tracker posts), any `.out-of-scope/` concept record, and the per-write execution ledger. For an overview request: the three-bucket summary with counts.
