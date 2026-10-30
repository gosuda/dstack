---
name: drift-detect
description: 'Use when roadmap, plans, or docs may have drifted from code, or when restarting a stalled project. Not for PR doc sync: use docs-update.'
---

# Drift detect

Plans age and code moves on. This skill examines whether the roadmap, plans, and docs still match what is actually built, and produces a Reality Check Report: executive summary, drift analysis, gap analysis, a cross reference table, and a prioritized reconstruction plan, with every item backed by cited evidence.

The scan is read only. It never mutates docs, issues, PRs, or code. If any step would mutate those, stop that step. The only file it may write is an optional local artifact under `.outline/drift-detect/` (delete that directory to roll back). For PR doc sync instead of drift analysis, use docs-update.

## What to examine

You need a target scope: the whole repo, a named plan file, a named milestone, a release branch, or a feature area. The request must supply one.

Two flags shape the scan. `--sources` takes a comma list from `github,docs,code`; when omitted, examine all three, and drop a source only when it is unavailable or irrelevant. `--depth` takes `quick` or `thorough` (the default): quick samples active surfaces, thorough follows related docs, symbols, and history. When the report is too long for chat, write it to `.outline/drift-detect/reality-check-YYYYMMDD-HHMM.md`.

## Gathering reality

Restate the target first, resolve the sources from the flags (or take all three), and open a small evidence bundle in memory, or in `.outline/drift-detect/evidence.json` when the synthesis is long. Keep it minimal: `{github, docs, code, signals, generatedAt}`. Every array item carries `{source, evidence, confidence}`, and every piece of evidence must be citeable: `README.md:42`, `issue #17`, `src/auth/session.ts`, `.github/workflows/test.yml`, or a command result.

Collect GitHub reality with `gh` JSON output, never by scraping web HTML:

```bash
gh issue list --state open --limit 200 --json number,title,labels,state,assignees,createdAt,updatedAt,milestone,url
gh pr list --state open --limit 100 --json number,title,state,isDraft,labels,createdAt,updatedAt,mergeStateStatus,reviewDecision,changedFiles,additions,deletions,files,url
gh api repos/{owner}/{repo}/milestones --paginate --jq '[.[] | {number,title,state,open_issues,closed_issues,due_on,updated_at,description}]'
```

Pull out stale issues (`updatedAt` beyond 90 days; high priority stale means 60 days), issue categories from labels and titles (`security`, `bug`, `feature`, `docs`, `infra`, `tech-debt`), PR risk (draft PRs open beyond 30 days, merge conflicted PRs, PRs attached to promised milestones), overdue milestones (due date past with `open_issues > 0`; critical when beyond 30 days overdue and release labeled), and already done candidates (issue titles semantically matching implemented files or symbols from code reality). When `gh` is unavailable or unauthenticated, mark GitHub `unavailable` and continue with docs and code. Never invent issue state.

Collect documentation intent by finding candidate files, then reading only the candidates: `README*`, `PLAN*`, `ROADMAP*`, `TODO*`, `CHANGELOG*`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING*`, `docs/**`, `documentation/**`, `.github/ISSUE_TEMPLATE/**`, `.github/PULL_REQUEST_TEMPLATE*`. For each document record the headings that name goals, phases, release targets, features, or non-goals; checkbox state (total, checked, unchecked, completion percent as checked over total); completion claims (`complete`, `done`, `shipped`, `ready`, `implemented`, `v1`, `release`); feature list items under Features, Roadmap, Plan, or API sections (strip marketing adjectives before matching); and stale doc hints (no git change in 180 or more days, old version numbers, removed symbol references, examples importing nonexistent paths). When no docs exist, record a documentation gap rather than drift.

Collect code reality, preferring indexed codegraph when available and falling back to `ast-grep` and `git grep` otherwise. Sniff the framework first: read `package.json` (Node: react, next, vue, angular, express, fastify, nestjs, hono, jest, vitest, mocha, playwright, cypress), `pyproject.toml` or `requirements*.txt` or `setup.cfg` (Python: django, flask, fastapi, pytest, unittest), `Cargo.toml` (Rust: bins, workspaces, tests, benches, axum, actix, rocket), `go.mod` (Go: gin, echo, chi, `_test.go`). Check `.github/workflows/**`, `.gitlab-ci.yml`, `circle.yml`, `Jenkinsfile`, and `buildkite/**` for CI. Then map symbols and dependencies (codegraph explore, search, callers, callees, impact when indexed), or:

```bash
ast-grep --pattern 'export $X' --lang ts src
ast-grep --pattern 'def $NAME($$$ARGS): $$$BODY' --lang python .
ast-grep --pattern 'func $NAME($$$ARGS) $$$BODY' --lang go .
git grep -nE '\b(auth|login|session|payment|route|controller|handler|model|migration|schema)\b' -- ':!node_modules' ':!dist' ':!build'
```

Collect the native drift signals too: doc drift with zero coupling (doc files whose recent changes never co-change with related source; repeated doc only commits with no matching source commits for referenced terms is MEDIUM, exact removed symbol references are HIGH); at risk areas (directories with high bug fix churn and stale or low ownership, HIGH when a planned feature maps to an area with high bug fix density and no recent owner activity); stale docs (older than 180 days describing active or changed code paths); orphan exports or dead starts (exported symbols or public endpoints nothing calls or imports; orphan plus documented feature is HIGH drift, orphan without docs is a LOW cleanup signal); test gaps (implementation exists for documented critical behavior but no matching test file, no test script, or CI never runs tests). Without codegraph, mark code evidence certainty MEDIUM or LOW. In a shallow clone, treat git history signals as unreliable, mark native signals LOW, and list them under Unknowns.

## Making the call

Classify every evidence item using `references/drift-taxonomy.md`: drift types, gap types, prioritization weighting (score from severity, category multiplier, bonuses, and penalties, then Immediate, Short term, Medium term, and Backlog buckets with tie breaks), fuzzy cross reference matching (normalize before matching, then align statuses of aligned, partial, documented only, implemented only, stale or obsolete, and unknown with HIGH, MEDIUM, or LOW certainty), native signal interpretation, and the synthesis rules (completed checkboxes stay suspect until verified against code; age alone never proves staleness; public docs outrank internal docs; milestones outrank backlog plans; security, correctness, and release blockers outrank cleanup; pattern level drift outranks isolated drift; no plan item without a named file, issue, milestone, or feature area). Delegate one synthesis pass to a semantic analyst role, handing it the evidence bundle and the taxonomy; it emits the report. Never hardcode model names. Never name or invoke a skill as a dependency.

Shape the synthesis prompt like this:

```text
Act as the semantic analyst for a plan-vs-reality drift scan.
Input: structured evidence from GitHub, docs, code, and native signals.
Task: produce a Reality Check Report.
Rules:
- Be specific. Each finding includes Evidence.
- Verify each completed checkbox/phase against code evidence.
- Verify each open issue as active, stale, already implemented, duplicate, or blocked.
- Cross-reference documented features to implemented features using fuzzy/semantic matching.
- Classify drift and gaps using the taxonomy.
- Produce Immediate / Short-term / Medium-term / Backlog plan buckets.
- No generic advice; every plan item has severity and evidence.
```

Emit the Reality Check Report with the report template in `references/drift-taxonomy.md`: executive summary, drift analysis, gap analysis, cross reference table, prioritized reconstruction plan, quick wins, and unknowns. When two documents contradict each other, record the conflict naming both documents and quoting or paraphrasing both passages; keep it unresolved in the cross reference table rather than smoothing over it. Reject any synthesis finding that cites no concrete evidence.

## What you hand back

The Reality Check Report with executive summary, drift analysis, gap analysis, cross reference table, prioritized reconstruction plan, quick wins, and unknowns, every item evidence cited. When all sources are unavailable, stop and report which sources failed and why instead of emitting a report with fabricated evidence.
