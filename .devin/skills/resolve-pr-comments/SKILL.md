---
name: resolve-pr-comments
description: 'Use when handling GitHub PR or GitLab MR review threads, top-level comments, or review bodies on one named PR/MR in a single batch: enumerate completely, judge against current code, repair valid findings at the root, and post only explicitly approved replies and resolutions. Not for repeated review loops, merge policy, or merge conflicts.'
---

# Resolve PR and MR comments

Work one batch of review feedback on one named pull request or merge request to completion: enumerate every actionable item, judge each against the code as it stands, fix what is valid at the root, and post only the replies, resolutions, and pushes a human explicitly approved. Repeated coordination across batches belongs to the caller, landing policy belongs to the gate, and stopped-hunk mechanics belongs to conflict resolution. This skill has no aliases.

Intake and judgment are read-only. Repairs are local, reversible source edits with targeted proof. Every outward write (reply, thread or discussion resolution, push of repair commits to the named ref) waits on exact-text human approval; a configured remote alone authorizes nothing, and a timeout or auto-selection is never consent. There is no merge, base change, history rewrite, reopen, credential change, or publication beyond the approved set. Before any verdict you record the provider plus owner and repo (GitHub) or host and project path (GitLab), the PR number or MR IID, open state, the full 40-hex head OID and ref, base repository with ref and OID, and the code revision read for judgment. Afterward every verdict cites code evidence at that revision, every outward write carries a parsed receipt plus read-back, silence or exit zero or a green run never counts as proof of handling, and the observed open set matches the intended one with new findings returned as next-batch input.

Full node IDs are the identity on GitHub; on GitLab the identity is project path plus MR IID plus discussion and note IDs, never a GitHub node ID. Subjects, paths, positions, markers, prefixes, suffixes, and vendor counts are hints only. An empty or failed search proves nothing.

Derive the provider from the verified request URL or repository remote, never by guessing: a GitHub URL or `gh`-backed remote takes the GitHub path, a GitLab URL (including self-managed hosts) or `glab`-backed remote takes the GitLab path. If the forge is ambiguous, stop and ask which one owns the target. Never assume the default `gitlab.com` host for a self-managed remote. Fork work binds source project, target project, host, IID or number, and head SHA separately on either provider.

To start you need the target (blank for the current branch PR or MR, a PR number or MR IID, or a comment, thread, or note URL for targeted scope; on GitLab the target is host plus project path plus IID, and the IID is project-scoped), a checkout at the recorded head OID or the exact file revision read per verdict, working `gh` or `glab` access, the approved mutation set (exact reply bodies, resolution choices, exact repair commits with push destination ref, expected full head OID, acting account), and the proof command used per repair. For GitLab MR CI state, check head-pipeline matching with `python3 scripts/inspect_mr_checks.py --host <host> --project <GROUP/PROJECT> --mr <IID> --json`, which verifies the head pipeline SHA equals the recorded head.

## 1. Bind the target and confirm freshness

Record one target identity and one full head OID, then confirm the working checkout equals the recorded head with `git rev-parse HEAD`. Resolve a blank target from the current branch inside the target repository. Resolve a comment URL before judging (on GitHub with `scripts/get-thread-for-comment`, on GitLab with `python3 scripts/gitlab-mr.py --host <host> --project <GROUP/PROJECT> --mr <IID> thread --note <NOTE_ID>`). On GitLab also record source and target projects for forks, and source and target branches. A merged or closed PR, or a merged or closed MR, is not an active fix branch: report its state and stop without recreating its head or opening a follow-up.

## 2. Enumerate the whole batch before judging anything

Keep resolved threads and discussions in the accounting census. Run the census fetch once: on GitHub `scripts/get-pr-comments <PR> [OWNER/REPO]`, whose action view is `review_threads` (unresolved threads with `isOutdated` intact), `pr_comments` (non-author top-level comments), and `review_bodies` (non-empty non-author review bodies), and whose completeness signal is the same output's `coverage` object (`threads_complete` true, `truncated_comment_threads` empty) with `all_review_threads` plus per-thread `totalCount` as the census. The bundled helper retains full node IDs for every source (comment nodes carry `id` on threads and top-level comments, review-body nodes carry `id`), and the caller needs those IDs for identity and per-item output. On GitLab run `python3 scripts/gitlab-mr.py --host <host> --project <GROUP/PROJECT> --mr <IID> list` once, whose action view is unresolved discussions (positioned diff notes keep their position for outdated hunks) plus ordinary top-level notes, with the resolved-inclusive output plus its `coverage` record as the census proving every discussion and note page was enumerated. GitLab has no review-submission object, so there is no review-body category; an MR description finding is an ordinary top-level note. The helper addresses the MR by IID in project scope with the host on every read, and any head-SHA movement across the census fails instead of returning a mixed snapshot. Feed pages from files through `jq`, never through argv.

Split each body into distinct items, including body-only review and top-level findings that never became threads. Drop only non-actionable wrappers, approvals, badges, and status summaries with a stated reason, and keep actionable bot findings. A prior reply suppresses rework only when its content addresses the same finding and its evidence still holds at the recorded head. Deduplicate only on complete finding plus location or symbol, failure preconditions, requested contract, and disposition, keeping all original IDs as aliases. If the census never ran or `coverage` reports truncation, report the gap explicitly and never claim a complete result.

## 3. Judge each item against the current code

Read the referenced file at the recorded revision, recompute numbers, check guards and caller effects, and weigh severity against the governing contract rather than the comment summary. Re-anchor moved code with one same-file anchor search; when the anchor is gone, mark `not-addressing` with the search evidence, or `needs-human` when intent is unclear. Distinguish approved decisions from proposals and governing requirements from descriptive text. For branch attribution, inspect the merge-base delta, relevant changes on both sides, and candidate behavior, since path presence or absence in branch history alone proves nothing.

## 4. Give every item exactly one verdict

Assign one of `fixed`, `fixed-differently`, `replied`, `not-addressing`, `declined`, or `needs-human`. A question needing no code change is `replied`. A missing premise with search evidence is `not-addressing`. An item needing an author decision the PR or MR has not made is `needs-human`: it stays open with no closing claim.

## 5. Repair what is valid at the root, locally

`fixed` and `fixed-differently` change the general case so the reported case is absorbed; an input-specific conditional is not a repair. Work directly in this batch with no second repair fleet and no numeric batch or cycle caps. Where a biting regression proof can discriminate, add or update one: state the failing behavior without the fix and the required behavior with it. Run the targeted proof per repair, then one combined proof after all edits. A failure in an untouched file is not automatically pre-existing; attribute it with the same scenario and comparable configuration on base and candidate. Never suppress a verifier or count a zero-matched selection as proof.

## 6. Stage the authorized set and get explicit approval

Record exact reply bodies quoting each finding and outcome, exact resolution choices, the exact repair commits and push destination ref, the expected full head OID, and the acting account. Approval covers exact bytes and the exact push ref, so any body edit, commit change, or head movement needs renewed approval. A reply grant never implies resolution or push authority, and a push grant covers only the listed commits to the listed ref. `needs-human` items are approved as left-open.

## 7. Validate everything before the first write

Confirm full thread and comment IDs (discussion and note IDs on GitLab), target repository and PR or host, project and MR IID, current head equal to the approved head, thread and discussion ownership, disposition, listed commits and push ref when pushing, and current evidence. Compare full OIDs, never prefixes. After any rewrite, re-anchor every cited commit with full objects, compared patches or trees, and current repair behavior; squashed, split, dropped, or reworded repairs need explicit re-anchoring and renewed exact-text approval.

## 8. Post only approved writes and verify each receipt

Thread helpers reject GraphQL errors and emit structured receipts, but a successful process exit alone never proves the intended thread changed, so caller-side validation and read-back stay required for every write. For a GitHub reply confirm the helper output parses as JSON, carries no `errors` object, and contains the reply comment `id` and `url`. For a GitHub resolution confirm no `errors` with the returned thread `id` equal to the expected thread ID and `isResolved == true`. For a push confirm the local head still equals the approved head, push only the approved refspec, then confirm the accepted remote OID and ref update from transport output, never from exit status alone. Bodies travel file-backed: write the body to a temp file and pipe it on stdin (`--body-file` for `gh pr comment`); never expand page JSON or bodies into argv. Retain each ID and URL and read the posted body back under the acting account with the census fetch. Reply first; resolve only after that reply is confirmed and resolution was authorized.

Top-level review-body and conversation items go through `gh pr comment <PR> --repo OWNER/REPO --body-file <file>` with the recorded OWNER/REPO and PR, which has no helper-side receipt, so its proof is the author-inclusive re-enumeration delta: exactly one new comment ID under the acting account with the exact posted body, absent from that post's immediate pre-snapshot, under complete paginated coverage from a paginated unfiltered `gh api graphql --paginate` query over `comments(first: 100, after: $endCursor) { nodes { id author { login } body } pageInfo { hasNextPage endCursor } }` (or the equivalent paginated REST `gh api --paginate` issue-comments enumeration), paginated until the last page reports `hasNextPage == false` with no errors or missing data. An incomplete enumeration cannot support the exactly-one-new-ID claim, and that receipt is uncertain, never verified.

On GitLab, post discussion replies with `python3 scripts/gitlab-mr.py --host <host> --project <GROUP/PROJECT> --mr <IID> reply --discussion <DISCUSSION_ID> --body-file <file> --expected-head <approved-head-SHA>` and resolve with `python3 scripts/gitlab-mr.py --host <host> --project <GROUP/PROJECT> --mr <IID> resolve --discussion <DISCUSSION_ID> --expected-head <approved-head-SHA>`; both mutating subcommands require `--expected-head <approved-head-SHA>` bound to the surveyed and adjudicated approved revision (never fetch a new head merely to satisfy the flag; a changed head stops publication for re-adjudication). Both helpers validate the returned note identity or resolved state and read the discussion back, under the same parsed-receipt plus read-back discipline. Ordinary top-level MR notes prove the same way as GitHub top-level comments: exact-text approval in a body file, with the receipt as the author-inclusive re-enumeration delta showing exactly one new note ID under the acting account with the exact posted body, absent from the immediate pre-snapshot under complete paginated coverage. No GitLab MR command has a general dry run, so approval always precedes the mutation. This skill never creates, updates, merges, closes, approves, or changes draft state on an MR; approval state, unresolved discussions, draft status, head-pipeline matching, and project merge policy stay distinct gates owned by the caller.

On any uncertain or failed write, stop remaining writes and inspect live receipts before any retry. When the same approved body already exists under the acting account on the exact thread or discussion, report and verify it rather than duplicating it. Respect rate-limit and abuse signals.

## 9. Reconcile and report one batch

Rerun the census fetch (`scripts/get-pr-comments <PR> [OWNER/REPO]` on GitHub; the `list` operation on GitLab) and compare the action view plus resolved-inclusive census against the intended open set, then separately re-enumerate top-level state with the same author-inclusive source used for top-level receipts. Explain every retained pending or intentionally open item, including resolved threads kept for accounting and body-only items. New findings and changed-head evidence are next-batch input for the caller, not an internal loop.

## What stops the batch

| Failure | Behavior |
|---|---|
| Empty action view with complete census | Return `No actionable comments` and change nothing. |
| Incomplete pages or missing census | Report the exact missing surface. Never claim zero items. |
| Target merged or closed | Report state and stop. No head recreation or follow-up without a separate grant. |
| Inaccessible code | Mark `needs-human` with the exact access failure. No guessed verdict or repair. |
| Identity unmapped | Stop the affected scope and report the exact unresolved ID. Never guess an ID or swap a GitHub node ID for a GitLab discussion or note ID. |
| Remote unauthenticated or no remote (`gh`/`glab`) | Report and stop. No credential repair. |
| Head moved after approval | Stop writes, re-evaluate at the new head, seek renewed exact-text approval. |
| Fix fails validation | Re-fix or revert locally. Never post, resolve, or push an unvalidated repair. |
| Receipt missing or mismatched | Stop remaining writes, report exactly which writes landed, retry only on a concrete transient signal with identical bytes. |
| Write without explicit approval | Refuse and record the blocked attempt. |
| User rejects preview | Post nothing, resolve nothing, push nothing, report the rejection. |

Report one record per item in order (item and thread or discussion IDs plus source, file and line or anchor, verdict, code evidence at the recorded head OID, repair and proof for the two fixed verdicts, exact reply body and receipt URL for posted replies, resolution receipt, push ref and accepted remote OID, held reason for `needs-human`), plus batch totals, approved and observed head OIDs, the resolved-inclusive census comparison or its reported gap, commit SHAs if pushed, observed versus intended open sets, and new findings as next-batch input. No remote change lands beyond approved receipts.
