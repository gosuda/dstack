---
name: append-run-log
description: 'Use when a completed agent run must be recorded as durable, queryable evidence. Not for remote, credential, publish, deploy, or irreversible changes.'
disable-model-invocation: true
---

# Recording a finished run where it can be queried later

A run has completed and its measurements must survive as durable evidence: exactly one entry per run, in an append-only JSONL log no writer ever rewrites, with aggregate metrics derivable from the log alone. The only mutations this skill ever makes are appending that one line, pruning expired lines when told to, and updating the last-run pointer -- never remote, credential, publish, deploy, or irreversible changes.

## What you need before you touch the log

- `run_id`: non-empty, and unique within the log.
- `started_at` and `ended_at`: ISO 8601 UTC (`YYYY-MM-DDTHH:mm:ssZ`) with `ended_at` not before `started_at`. Anything not ISO-only is rejected. The entry's date guard comes from the date portion of `ended_at`.
- `metrics`: a JSON object of run measurements (duration, token count, model, outcome, and the like) sufficient to derive aggregates from these fields alone.
- `log_path`: the append-only JSONL run log.
- `last_run_pointer_path`: the last-run pointer file.
- `retention_window` (optional): an ISO 8601 duration or day count. When omitted, nothing is pruned.

## Appending without disturbing history

1. Validate everything at the trust boundary before mutating: `run_id` is non-empty, both timestamps parse as ISO-only UTC with `ended_at` after `started_at`, and `metrics` is a JSON object. Scan the log for an existing line whose parsed `run_id` matches; a match means `rejected-duplicate` -- report the existing entry and stop without mutating. Anything missing or malformed means `rejected-invalid-input` -- name the rejected field and stop, log untouched.
2. Open `log_path` in append-only mode. Prior lines are never read-modify-written or rewritten.
3. Compose the entry as a single line carrying `run_id`, `started_at`, `ended_at`, `metrics`, and `date` set to the ISO date portion of `ended_at`.
4. Append it as exactly one newline-terminated line and flush, so exactly one line with this `run_id` exists. If an interrupted append left a line that fails the parse check, treat it as malformed (ignored, never rewritten) and re-append only when no line with this `run_id` parses correctly.
5. When `retention_window` was supplied, delete whole lines whose `date` precedes current UTC date minus the window. Deletion is the only mutation prior entries ever suffer; surviving lines stay byte-identical.
6. Point `last_run_pointer_path` at an object holding the new `run_id` and `ended_at`.

A prior line that fails to parse or lacks required fields is ignored for aggregation and duplicate checks -- it corrupts nothing and is rewritten never, removed only if the retention window prunes it. Validation failures before the append leave the log untouched, and after a successful append no prior entry is ever rolled back; only retention pruning deletes, and only expired lines.

## If the entry cannot be recorded

When the log or the pointer path is unwritable so the work above cannot hold, report `blocked` with the failing path and the unrecorded entry rather than claiming the run is recorded. Otherwise the terminal classification is one of `recorded`, `rejected-duplicate`, or `rejected-invalid-input` -- and on `recorded`, the log holds one new JSONL line, an updated pointer, and any expired lines pruned.
