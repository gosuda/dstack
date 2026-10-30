---
name: onboard
description: 'Use when the user asks for onboarding, orientation, a repository tour, or where to start. Produces an evidence-backed seven-section map, deep-reads real files, and asks for the next move.'
---

# Onboard

You give a newcomer a grounded first hour in a repository: what it does, how it is built, where execution starts, and what to try next. Everything happens in chat. You change nothing in the repository, run no paid operations, and never present a guess as an observation.

You work from the repository root (the current working directory unless told otherwise; it must be an existing directory), a depth of `quick`, `normal`, or `deep` (default `normal`, which widens collection breadth without changing the output shape), and an optional focus such as an area, feature, language, package, or entry point (which steers the deep read and follow-up guidance, not the initial map). If the root does not exist or the depth falls outside the closed set, report the rejected value with the required correction and inspect no substitute path.

## Gathering evidence first

Collect before you explain, attempting every applicable class and treating anything missing as a stated degradation rather than a failure:

- Parse the root and workspace manifests for packages, languages, scripts, binaries, and build configuration.
- Walk directories to at most three levels deep, skipping generated, dependency, cache, coverage, and version-control directories. Never look beyond the repository root.
- Read the README and any local contributor or execution instructions, following a one-line Markdown redirect when one stands in for them.
- Inspect present CI workflows, container files, service composition, process declarations, and root deployment manifests.
- When the root is a Git worktree, read branch, origin, latest commit, shallow status, commit count, recent contributors, and files changed in the last 180 days.
- Locate entry points, exported surfaces, tests, and call or import flow with structural code search where available, otherwise language-specific text search over source and manifests. Never infer architecture from filenames alone.
- A read-only whole-repository digest facility, where one exists, corroborates stack, module boundaries, and naming conventions only; its absence or failure blocks nothing.

Retry gaps only with a narrower read or another available read-only search method.

## The seven-section orientation

Synthesize what you found into these sections in this exact order, grounding each in observed evidence and stating the reason once inside any section whose evidence is unavailable:

1. What it does: one or two plain-language sentences backed by the README and manifests.
2. Tech stack + CI: observed languages, frameworks, package managers, build and test tools, and CI jobs.
3. Where execution starts: observed binaries and CLIs, application or server bootstrap, framework-loaded configuration, library exports, and test or benchmark entry points, grouped by kind.
4. Project structure, annotated: important directories with their evidenced purpose plus unusual layout details. Explain the layout; do not paste an exhaustive tree.
5. Active development (hotspots + owners): recent high-churn files and contributors where Git evidence exists.
6. Code health: only evidenced drift, debris, or test gaps. Grade `HIGH` for direct tool evidence, `MEDIUM` for repeated independent signals, `LOW` for an explicitly marked inference.
7. Getting started: exact runnable commands: commands copied from manifests, CI, build files, or the README. Leave a command out rather than invent one you cannot ground.

Where sources conflict, present the conflict with file paths or metadata origins and choose no claim without support. Keep useful findings, keep unavailable evidence and anything marked `[INFERENCE]` clearly apart, and never claim completion when a blocking gate failed.

## Reading real code

After forming the map, deep-read two or three real files in this order: the primary structural entry point, a central file in the largest observed module, and one representative test. Read every available category when fewer exist and say exactly what is missing. Connect the files through observed imports, calls, exports, or test targets, labeling any remaining inference `[INFERENCE]`.

## Asking for the next move

End by asking the user to pick exactly one next move, marking Explore an area as the recommended first step (use a single-select interaction where one is available, otherwise numbered options, then stop):

| Move | What happens next |
|---|---|
| Explore an area | The user picks a directory or package, and you inspect its central exports and most-connected implementation file |
| Trace a feature | The user gives the feature name, and you trace its entry point, call or import flow, and two or three key files |
| Make a first change | The user describes the desired change, and you map risk from hotspots, ownership, and tests before editing |
| Where can I help? | You derive file-level opportunities from hotspots, test gaps, stale documentation, low-ownership areas, and bounded cleanup candidates |

The run counts as `complete` only when the root is valid, core collection was attempted, at least one real source file was read, every command is grounded, and the next-move question is present. Otherwise it is `blocked`: name the unmet predicate and keep the useful partial orientation alongside it.
