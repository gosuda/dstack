---
name: propose-issue
description: 'Use when the user asks to propose an issue, file or open a bug report, or turn a reported defect into a tracked issue. Not for fixing the defect, triaging existing issues, or reviewing PRs.'
disable-model-invocation: true
---

# Propose a tracked issue

A human asks you to turn a reported symptom into one public issue. You investigate what the code actually does, prove the defect is real and not yet tracked, draft a tight report, and create at most one GitHub issue with `gh`. Filing is the last step and always waits on an explicit approval of the exact redacted text.

Fixing the defect, triaging existing issues, and reviewing pull requests are out of scope.

## What you start from

The reported symptom or suspected defect is required. The target repository is optional and otherwise resolves from the current checkout. Source files and history needed to investigate must be readable. Authenticated `gh` access is needed only for tracker search and issue creation. Reproduction details, affected versions, and configurations are useful supporting evidence and are never invented when absent. A missing repository, unreadable source, or unavailable search input is an honest block, never something to work around with guesses.

Before any authenticated GitHub command, preview the resolved repository, the consequence of creating one public or repository visible issue, and the fact that no other remote state will change. An ambiguous repository stops the run before any remote touch.

## Work the defect in order

1. Resolve the target repository from the explicit target or the current checkout, with the preview above. Stop on ambiguity.
2. Locate the reported behavior in source opened during this run. Attach a `path:line` citation read in this run to every factual claim planned for the issue. A user reported symptom that cannot be located stays in the draft only as an explicitly attributed and unconfirmed report, never as fact. No claim may rest on a file not opened during this run.
3. Separate mechanism from symptom. Name the causal mechanism the cited source supports, set the affected callers, versions, and configurations the available evidence supports, and reproduce the defect. When reproduction is impossible, record the exact reason in one line instead of claiming a result. Unsupported observations stay as attributed and unconfirmed reports.
4. Search all issue states before drafting with `gh issue list --repo <target> --state all --search "<mechanism and symptom terms>"`. Record `no match` or the matching issue number. The same mechanism counts as a duplicate even when wording differs. The same symptom from a different mechanism does not. On a match, stop without creating anything and report the existing URL or number. A failed search never becomes an assumed `no match`; it blocks the duplicate gate and the run stops with no remote change.
5. Draft a title that states the defect rather than a proposed fix. Draft the body with exactly these headings in this order: `Summary`, `Reproduction`, `Evidence`, `Expected vs actual`, and `Scope`. Include only claims supported by the steps above.
6. Preview the final target repository, title, complete body, and creation consequence. Scan the draft for secrets, credentials, private identifiers, and any content not approved for publication, then show the redacted form with the redaction list and proceed only after explicit approval of that form. Mark each gate below explicitly as pass or fail. Any failure or any withheld redaction approval stops filing with no remote change.

| Gate | Pass means |
|---|---|
| Citations | Every factual claim carries a `path:line` citation read during this run |
| Defect | The report is a defect, not a preference or style opinion |
| Mechanism | The supported mechanism is named, not only the symptom |
| Duplicates | The duplicate search ran and found no match |
| Title | The title states the defect rather than the fix |
| Sources | No claim relies on a file not opened during this run |

7. Only when all six gates pass, run `gh issue create --repo <target> --title <title> --body <body>` once. Accept success only when the command confirms creation with an issue URL. Never retry a result that may have created the issue until the tracker has been checked for that exact title and body. On an ambiguous create result, search the target for the exact title and body first. With exactly one match report its URL. With none or more than one, do not retry and return a blocked result naming the ambiguity. With a confirmed creation failure and proof nothing was created, make no further remote change and return the error with the retained final draft.

## What to hand back

Return exactly one terminal classification. A filed result carries the target repository and the confirmed issue URL. An aborted result carries the target repository when known, the retained draft or duplicate match when available, and the specific failed or blocked criterion. Never return both. No failure path claims completion; partial evidence and drafts may be returned, but the terminal result stays an abort until the issue URL is confirmed.
