---
name: pr-walkthrough
description: 'Use when a user asks for a zoomable PR map or graph-canvas orientation. Not for remote, credential, publish, deploy, or irreversible changes.'
disable-model-invocation: true
---

# PR walkthrough

Build a zoomable map of a pull request: which files changed and how they connect, when the commits landed, where the edits concentrate, and how review threads hang together. The result is one self-contained HTML file with all assets bundled locally and no external network dependency. Everything here is reversible and local. It writes only the output site plus scratch files under the working directory, so rollback is deleting or overwriting prior output, and nothing remote is ever mutated.

## Hand me the change

- PR diff or branch diff (required). A unified diff file, a git range (`base..head`), or a GitHub PR URL.
- API credentials (required only for a GitHub PR URL). Via the `GITHUB_TOKEN` environment variable or a `gh auth` session, used read-only to fetch the diff and review threads.
- Repository root (optional, defaults to the working directory). Used to resolve file paths in the diff.
- Output directory (optional, defaults to `./pr-walkthrough-site/`).

## Parse the diff into the four views

Parse a supplied diff file or git range directly. For a GitHub PR URL, fetch through the GitHub API with the credentials above: use the `gh` CLI or `GITHUB_TOKEN`, follow pagination with `Link` headers to retrieve every page of diff and review threads, and on rate-limit responses (HTTP 403/429) stop and report the limit. Pull out every changed file path, hunk range, insertion count, and deletion count. If the fetch fails, report it.

Then build the four views:

- File dependency graph. For each changed file, record edges to other changed files sharing an import or include relationship found in the diff context lines. Keep it as an adjacency list.
- Commit timeline. For a git range, extract each commit hash, author, date, and subject. For a single unified diff, create one synthetic commit covering all hunks.
- Change heatmap. Map each hunk to its file path and line range, bucket lines into 50-line blocks, and record insertions and deletions per block.
- Review thread flow. For a PR URL, fetch review comments with the same authentication and pagination and group them by file and position. Without a URL, the thread list is empty.

## Generate, write, and verify the site

Produce one self-contained HTML file holding all four views: an SVG file dependency graph with zoom and pan (d3-zoom), node coloring by change magnitude, and edge bundling; a horizontal commit timeline with zoom, click-to-inspect, and tooltips; a heatmap grid of files by line blocks with color intensity proportional to edit density; a thread flow diagram showing comment threads as connected nodes along a vertical file axis. Each view gets a guided tour, defined as a JSON array of highlight steps embedded in a script tag. Inline the CSS, inline the JavaScript, and bundle D3 v7 locally as a string literal inside a script tag. No external script tags, no CDN references, no network dependency.

Write the file to the output directory as `index.html`. Then verify it is self-contained: open it, confirm no `src` attribute points to an external URL, confirm all four SVG containers are present, and confirm each tour JSON array holds at least one step. Name the specific defect and stop if verification fails.

## When I stop instead

- Unparseable diff: report the parse error, produce no site, return `blocked`.
- Empty diff with zero changed files: report that no changes were detected, produce no site, return `blocked`.
- GitHub authentication failure: report the HTTP status, produce no site, return `blocked`.
- GitHub rate limit: report the limit and the reset time, produce no site, return `blocked`.
- Pagination failure: report the page that failed and the partial data retrieved, produce no site, return `blocked`.
- Self-containment verification failure: report the external reference or missing element, fix the HTML, and re-verify. If the fix still fails after three attempts, return `non-converged`.

If the HTML was written but verification failed, the output directory keeps the last attempt. No rollback is needed because every write is local and overwritable.

## What you get

A static site at the output directory containing `index.html` with the four D3 views, guided tours, and all assets bundled locally with no external network dependency.
