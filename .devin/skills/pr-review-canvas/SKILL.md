---
name: pr-review-canvas
description: 'Use when asked to render a PR review as a Cursor Canvas artifact or a standalone HTML page served on localhost (mode: html), with risky hunks foregrounded.'
disable-model-invocation: true
---

# PR review canvas

Turn a pull request into a review you can read locally, with the dangerous changes up front and the harmless ones after. Two shapes: a `.canvas` artifact in the working directory (the default), or a standalone HTML page served on loopback. Everything here is reversible and local. It only writes the one named artifact, never touches anything remote (the `gh` calls in html mode are reads), and rolling back means deleting that file.

## Tell me which shape, and hand me the PR

- `format`: `canvas` (default) or `html`.
- For `canvas`: the PR's unified diff, as a file path or piped content (required). Title, description, and linked issue text help judge risk, so include them when you have them (optional).
- For `html`: a GitHub PR web URL or `owner/repo#<number>` (required), plus an installed, authenticated `gh` CLI.

## Read the diff and sort it by risk

Parse the canvas diff into hunks grouped by file. For html, pull `{owner}`, `{repo}`, `{number}` out of the URL or `owner/repo#number` string, then fetch all three of these concurrently:

```bash
gh api repos/{owner}/{repo}/pulls/{number} --jq '{title, body, user: .user.login, state, additions, deletions, changed_files, base: .base.ref, head: .head.ref}'
gh api repos/{owner}/{repo}/pulls/{number}/files --paginate --jq '.[] | {filename, status, additions, deletions, patch}'
gh api repos/{owner}/{repo}/pulls/{number}/comments --jq '.[] | {user: .user.login, body, path, line}'
```

If extraction fails, or any call fails or comes back empty, stop here. There is nothing to classify yet.

Then judge every hunk. Risky means it touches control flow, error handling, concurrency, public API boundaries, security-sensitive paths, or data-integrity logic. Safe means documentation-only, import reordering, formatting, or trivial renames with no behavioral change. In html mode, fold the fetched review comments into the judgment. If a hunk is genuinely ambiguous, call it risky, say so in its annotation, and never drop it. Within each file, risky hunks go first and file order from the diff is preserved.

Give every hunk its own review block: file path, hunk line range, the diff text, and a risk annotation explaining the call.

## Assemble the artifact for the shape you picked

- Canvas: PR metadata summary first, then the risky hunk blocks, then the safe ones, each block its own canvas section.
- HTML: one complete self-contained HTML5 document, written directly with no scratch files and no renderer or template files read from the skill directory. Shape the `<body>` to fit the PR: a header with title, PR number, author, and stats; a plain-English summary box; core file sections with annotations and diffs; boilerplate files collapsed by default; a review checklist at the bottom; `<div data-diff="<target>">` placeholders where diffs render. Embed the CSS for risk callouts, diffs, and collapsed boilerplate plus the JavaScript mapping each `data-diff` key to its patch text. Build that patch map in memory from the fetch above and embed it as JSON with `<`, `>`, and `&` escaped so patch text can never terminate the script element.

## Write it, and serve it if it is HTML

- Canvas: write to `<pr-identifier>.canvas` in the working directory, overwriting any prior canvas for the same PR.
- HTML: write to `/tmp/pr-review-<number>.html`, then serve it with `python3 -m http.server 8432 --bind 127.0.0.1` under the harness background-process manager with `/tmp` as the working directory. If 8432 is taken, try 8433, then 8434, then stop. Report the ready URL.

## When I stop instead of writing anything

 - More than 500 hunks: report the count and recommend splitting the PR. No partial canvas.

- Empty or unparseable diff: no hunks found, nothing written.
- More than ~500 hunks: report the count and recommend splitting the PR. No partial canvas.
- Write permission denied: report the path and the error (nothing was written, so nothing to roll back).
- `gh` missing or unauthenticated, PR not found, network error, or rate limit (html): report it, verbatim for API errors, and stop.
- HTML assembly fails: nothing is written or served.
- Ports 8432 through 8434 all taken: report the failure and the last port tried.

## What you get

Canvas: one `<pr-identifier>.canvas` file with a header section (title, description, file count), then risky hunk sections (path, range, diff, annotation), then safe hunks in the same shape. Local only, never published or pushed. HTML: `/tmp/pr-review-<number>.html` (self-contained HTML with embedded CSS, JS, and safely escaped JSON patch data) served at `http://127.0.0.1:8432/pr-review-<number>.html` (or the next free port), rendering the interactive risk-first review in the browser.
