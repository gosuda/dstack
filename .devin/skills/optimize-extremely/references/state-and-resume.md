# Picking up a crashed optimize-extremely run without redoing work

Run state lives on disk, not in context. The single run-state file,
`.outline/optimize/<target>/log.jsonl`, is one JSON object per line, append-only: a record is
written the moment its fact is known and never rewritten. It sits beside the `agent-*` worktree
dirs but is not matched by the landing cleanup glob (`agent-*`), so it survives the run.

A five-lens fan-out can crash mid-benchmark. Every benchmarked candidate is already a durable
line, so resume re-dispatches only the lenses with no `candidate` record. Benchmarked work is
never repeated.

## What each record means

Last `run` record wins for overall status.

| record | written | key fields |
|---|---|---|
| `run` | candidate fan-out start (`in-progress`), landing (`done`) | `status`, `run_id`, `target`, `started_at`, `fingerprint`, `stop` config, `exit_code` |
| `baseline` | baseline pinning | `median_ms`, `stddev_ms`, `bench_cmd` |
| `candidate` | as each agent returns, including failures | `lens`, `after_median_ms`, `speedup_ratio`, `behavior_self_assessment`, `test_result`, `readability_cost`, `status` |
| `rank` | scoring | `winner`, `runner_up`, `composite` |
| `gate` | behavior gate, each pass | `candidate`, `passed`, `failure_scenario`, `iteration` |
| `integrated` | integrated re-measurement | `median_ms`, `integrated_speedup` |

## Telling a crash apart from a clean stop

Once the candidate fan-out `in-progress` marker is written, every clean terminal exit (0, 12,
13, 14, 16, 17) appends a `done` marker carrying its `exit_code`. An `in-progress` marker as the
last record therefore means a genuine crash. Only that offers resume; a clean non-zero exit does
not.

Failed and error attempts are recorded durably with a failed status that distinguishes them from
reusable completed candidate results. A completed failed candidate is never automatically
retried unchanged on resume; changing nothing and re-running a known failure is not progress.

## How the run knows its numbers are still valid

`fingerprint` is `{source_rev, bench_cmd, target}`, where `source_rev` is HEAD plus a hash of
the uncommitted diff over the target files. It pins the base the recorded numbers were measured
against. Candidate diffs are regenerated fresh each run and never cached, so a per-candidate hash
buys nothing. The run-level fingerprint plus the resume baseline re-check are the only staleness
guard needed.

## Resuming without repeating benchmarked work

Target resolution reads the target log if present. A terminal `done` marker means start
fresh (new `run_id`); stale history is preserved, never truncated, and the fresh work appends a
new run. An `in-progress` marker means recompute the fingerprint and re-measure the baseline.
Reuse recorded results only when the fingerprint matches the logged `run` marker AND the
re-measured baseline median falls inside the logged baseline standard-deviation band; then replay
the `baseline` and completed `candidate` records, skip lenses already recorded, and continue at
scoring once the remaining lenses report. When either check fails (source edited, benchmark
command changed, different machine, environment drift), the recorded numbers are stale. Leave the
stale candidate records in history but do not reuse them; write a fresh `run` marker, and start over.
