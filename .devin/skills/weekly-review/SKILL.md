---
name: weekly-review
description: 'Use when asked to summarize authored work over the last week or a named date range, commit range, or branch. Not for source or remote-system changes.'
disable-model-invocation: true
---

# Summarizing recent work

You turn git history into a readable summary of what was authored, either over the last week or over a caller-named range. You read history and write nothing: no files, no remote mutation, nothing to roll back. The report goes back as chat text.

Weekly mode ends with an executive summary plus work classification. Range mode ends with a concise dated status report as chat text.

## What you start with

| Input | Meaning |
|---|---|
| Mode | `weekly` (default) or `range` |
| `range` | Required for range mode: a date range, a commit range such as `<a>..<b>`, a branch name, or any label git accepts |
| `date_range` | Optional for weekly mode: overrides the `git log --since/--until` window, for example `"2024-01-01".."2024-01-07"`. When absent, the window is `7 days ago` to `yesterday` |

## Locating the repository

Find the repository root with `git -C <session_cwd> rev-parse --show-toplevel`. If the directory is not a git repository, abort: `"Weekly review requires a git repository."` in weekly mode, `"Not a git repository."` in range mode.

## Setting the window

In weekly mode, use `date_range` when supplied, else `since = "7 days ago"` and `until = "yesterday"`. In range mode, use the supplied `range` identifier as the git revision range; for a date range, map it to `--since`/`--until`.

## Listing commits and counting authors

List commits:

- Weekly: `git log --since="<since>" --until="<until>" --pretty=format:"%h %s" --no-merges`
- Range: `git -C <repo_root> log --oneline --date=short --format="%h %ad %s" <range>`

If the range is empty or git does not recognize it, report the empty result and stop.

Capture per-author counts:

- Weekly: `git shortlog -sne --since="<since>" --until="<until>" --no-merges`
- Range: `git -C <repo_root> shortlog -sne <range>`, omitted if the command fails

If any git command exits non-zero, stop with `"Git command failed: <stderr excerpt>."` If no commits fall in the window, return `"No commits found in the specified date range."` and fabricate no summary. When a failure interrupts gathering, return what was gathered and stop at the first failure.

## Composing the report

Weekly mode assembles four sections in order:

1. Executive summary, a 2 to 4 sentence overview.
2. Work classification, grouped by type: feature, fix, refactor, docs, test, chore.
3. Author statistics, from the shortlog.
4. Commit log, the raw `git log` output.

Range mode assembles a concise dated status update: the range label, the commit count, each commit on its own line as `<short-hash> <date> <subject>`, and author counts when available. Return it as chat output and write no file.
