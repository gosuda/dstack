---
name: catchup
description: 'Use when the human returns after a gap, cannot follow the project, asks what happened, or wants a visual HTML recap page. Not for onboarding: use onboard. Not for handoff: use handoff.'
---

# Catchup

Coming back to a project after a gap means the mental model is stale and the details have moved on. This skill rebuilds it two ways. The default is a short chat briefing of what changed since the human last touched the project. The alternative is a self contained visual recap page they can read at their own pace.

Two modes, chosen up front:

*   Briefing (default): chat output only. It writes nothing.
*   Visual: writes one self contained HTML recap page to `<project-root>/diagrams/project-recap.html` and opens it.

The project working directory (inferred from the current repository when not supplied) locates everything. The visual mode also takes an optional branch name and otherwise uses the current VCS branch or HEAD.

## Briefing: what changed while you were away

Work through these in order. Each step depends on the one before it.

1. Read only live state: recent file mtimes, git log and diffs, plan and state docs, task boards, and re0-memo notes. Never brief from conversation memory alone, since that memory may have drifted.
2. Anchor on the human's last touch (their last message, judgment, or commit, inferred from session history or the most recent commit when not supplied). Everything after that point is the delta; everything before it is assumed known and stays out.
3. Compose in decision order, not chronological order:
    *   Needs you: decisions, judgments, or inputs only the human can give, each self contained enough to act on without opening another file.
    *   Changed while you were away: outcomes, not process. Prefer "The plan's scoring rule was replaced" to "I ran three analysis passes."
    *   New words: every term coined or repurposed since their last touch, one line each, with where it lives. Skip terms they already used themselves.
4. Gloss on first use: any project specific term appearing in the briefing gets an inline plain language aside at its first occurrence, even when a glossary section follows.
5. Keep the default short (a screen or less). End with drill down offers per section rather than delivering everything expanded.
6. Cold read the briefing before sending: it must parse with no pre gap memory, every coined term must be glossed, each needs you item must be actionable without opening another file, and every claim must trace to a checkable source (file, commit, or artifact path).

When the ground is shaky, say so instead of filling gaps. No readable git history, plan docs, or task artifacts means reporting the project state as unreadable and naming what was checked, never fabricating a briefing from memory. An unidentifiable last touch point means stating the assumption used (for example the most recent commit) and proceeding, never guessing silently. A claim without a source is dropped or marked explicitly as unverified, never presented as fact. A briefing that runs over a screen is trimmed to the needs you items plus one line summaries of the rest, with drill down offered. A briefing covering only some sections is still useful as long as every included claim is source grounded; state which sections were omitted and why.

## Visual: a page that rebuilds the mental model

1. Confirm the project root exists and is readable; when it does not, stop and report that.
2. Detect the VCS type (git or hg) and read the current branch name.
3. Walk the project tree and identify the file kinds the page needs: config files, source entry points, dependency declarations, test files, documentation files, build artifacts directory, and module or package roots.
4. Gather the content for all 8 sections:
    *   Section 1: project name and branch (directory name plus current branch or commit hash).
    *   Section 2: config files found (for example package.json, Cargo.toml, pyproject.toml, go.mod, Makefile, Dockerfile, .env.example, .editorconfig).
    *   Section 3: source entry points (for example src/index, main, index, app, lib, __main__).
    *   Section 4: module structure (directory tree one level deep showing the package or module layout).
    *   Section 5: dependencies (declaration files and key packages, for example requirements.txt, package-lock.json, yarn.lock, Cargo.lock, go.sum).
    *   Section 6: test files and test directory structure.
    *   Section 7: documentation (README, CONTRIBUTING, docs/ directory).
    *   Section 8: build and deploy (build scripts, CI configs, Dockerfiles, deployment configs).
5. Compose a self contained single file HTML page with all 8 sections rendered, inline CSS, and no external resources.
6. Write the page to `<project-root>/diagrams/project-recap.html`, creating `diagrams/` when it does not exist.
7. Open the file in the default browser or file viewer.

An empty project means reporting that no project files were detected, not writing a placeholder page. A directory creation or file write failure means stopping and reporting the failure, never opening a file that does not exist. If the open step fails, the file remains on disk; report the failure rather than claiming completion. A section with nothing detected stays present with a "not detected" note; all 8 sections stay on the page.

## What you hand back

Briefing: a screen length briefing in decision order (needs you, changed while you were away, new words), every claim tracing to a file, commit, or artifact path, every project specific term glossed at first use, and drill down offers per section. Visual: the self contained HTML file at `<project-root>/diagrams/project-recap.html` with all 8 labeled sections derived from evidence in the project tree.
