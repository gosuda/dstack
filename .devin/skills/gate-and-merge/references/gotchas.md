# Gotchas

Three pieces of evidence, each reached only by a failing branch. Load this when the listing call
fails, when `mergeStateStatus` (or GitLab `detailed_merge_status`) looks like a gate, or when a
PR/MR conflicts.

## The listing call cannot carry statusCheckRollup

Never add `statusCheckRollup` to the bulk listing. At `--limit 60` the bulk call plus
`statusCheckRollup` returns `HTTP 502: 502 Bad Gateway`, while the same call without it returns
21 KB and exits 0. This is why the checks gate reads one PR at a time:

```
gh pr view <n> --json number,headRefOid,statusCheckRollup
```

GitLab: `glab mr list` emits whole REST resources with no per-field selection, so keep the bulk
call field-light by filtering locally (`--jq`), page with `-p`/`-P` (or `glab api ... --paginate`
for raw endpoints), and enumerate every page. Never gate on a single folded value: read
`detailed_merge_status` (never the deprecated `merge_status`), the head-pipeline state, and the
approvals/discussion flags separately, one MR at a time.

A `CheckRun` entry carries `conclusion` and a legacy status context carries `state`, so read
`conclusion` and fall back to `state`. Any value outside `SUCCESS`, `SKIPPED`, `NEUTRAL` is a
finding, and the finding names the check and its `detailsUrl`. An entry whose `status` is not
`COMPLETED` is still running: `gh pr checks <n> --watch --fail-fast`, then re-read. A queue that
merges on a pending check merges red.

Diagnose a red check outside this queue. Debugging CI inside the queue stalls every PR behind it.

## Never gate on mergeStateStatus

`cli/cli` PR 14252 reported `mergeStateStatus: "BLOCKED"` with `mergeable: "MERGEABLE"`, every
`statusCheckRollup` conclusion `SUCCESS`, and `reviewDecision: "REVIEW_REQUIRED"`. The field folds
branch protection into the same value as a real defect, so gating on `BLOCKED` holds every PR in a
review-required repository.

Read `mergeable` and `statusCheckRollup` separately instead. They say what the folded field cannot.

GitLab carries the same trap in any single readiness value: one folded field cannot tell a missing
approval from a failing pipeline, an unresolved discussion, a draft flag, or a project merge policy.
Read `detailed_merge_status` plus the head-pipeline state and the approval/discussion flags
separately; never gate on the deprecated `merge_status` or on any one rolled-up verdict.

## Conflict path

Resolve on the PR/MR head branch, never inside the merge. Merge the base into the PR/MR branch and
resolve the conflict there; a resolution buried in a merge commit is a change not covered by the PR/MR review.

Check `git config --get merge.mergiraf.driver`. Where it is set, the global `merge.mergiraf.driver`
handles supported languages through gitattributes. Where it is unset, resolve the file triple by
hand:

```
mergiraf merge <base> <left> <right> -o <out> -p <path>
```

Push, then re-gate. The push moves the head SHA (`headRefOid` / MR `sha`) and restarts CI, which is why the checks gate runs
last. This path is forge-neutral and applies unchanged to MR source branches.
