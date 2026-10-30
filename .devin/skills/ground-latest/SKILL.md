---
name: ground-latest
description: 'Use when starting or scaffolding a codebase or service, migrating, refactoring, or picking language, framework, or dependency, or latest, LTS, or modern way. Not for remote or irreversible changes.'
---

# Ground latest

Pin what is stable and supported today, with dated evidence a later reader can check. You write the grounded version set into the change itself (a plan, an ADR, or a PR body), so the next reader sees not just what was picked but when, from which source, and why. Nothing here touches anything remote, and rollback is version control or undo.

## Assemble the grounding set

List every choice the change pins before grounding any of them: language edition, runtime, each framework and dependency, build and test tooling, and the platform baseline. Nothing is grounded until this list is complete.

Also collect the existing constraints: repo pins and version floors where they exist. A floor is a minimum compatibility constraint, never a frozen choice. An existing exact pin is a recorded default that can be raised, never a silent freeze.

## Look everything up today

Check each entry at its own release channel today: the project release page, changelog, or registry metadata. Recall is not a source, so record the source URL or page for every entry.

Two extra sources are mandatory:

- Support windows and LTS tracks: query the endoflife.date product record at `https://endoflife.date/api/v1/products/<product>/` in addition to the release channel.
- Security applicability: check the project advisory source for that entry (project security page, GitHub Security Advisories for the repository, OSV, or NVD) and record which source you checked. Recall is not an advisory source.

Per entry, record the current stable version with its release date, the current LTS version with its release date where the project runs an LTS track, and the end of support date for each pinned candidate, citing the release channel source and the support window source separately.

## Floors are not pins

A compatibility floor sets the lowest acceptable version. The selected version must satisfy the floor, the floor never freezes the choice at the floor version, and the preferred pick stays the latest stable LTS satisfying the floor, otherwise the latest stable satisfying the floor. An existing exact repo pin is the recorded default, not a freeze: compare it against the preferred pick, keep the old pin only when project policy or a verified incompatibility requires it, and otherwise raise it. Name every override: the old pin or floor, the selected version showing the floor is satisfied, and the reason the pin was kept or raised.

## Read the current pattern before writing code

Read the chosen version current recommended pattern from its release channel documentation before writing against it. Renamed APIs and replaced defaults are where recalled code breaks, so never write code against a recalled API.

## Treat maintenance as context

Record the last 24 months of activity history, the repository archive status, applicable unresolved critical advisories affecting the selected exact version, and evidence of ecosystem adoption and de facto use such as downstream dependents, distribution packaging, or continued integration references.

Archive status is evidence inside this assessment, never an automatic rejection. An archived project with an endorsed successor moves to the successor. An archived project with no successor, and a long quiet project with no release, stands or falls on advisory applicability plus adoption evidence, with the reasoning recorded. Never reject a stable project solely because its last commit, release, or security fix is old.

## Decide advisories at exact version scope

Check whether each known critical advisory applies to the selected exact version, not merely to the product name. Cite the advisory source, the identifier, and the affected range. When an applicable unresolved critical advisory affects the selected version, never pin that version silently: pick the patched version where one exists, or report the entry as blocked with the advisory identifier and affected range. When every available stable candidate is affected, mark the entry blocked the same way rather than pinning an affected version with a disclaimer.

## Drop and replace what is not stable

Pre-release and deprecated choices are dropped, with the maintained stable replacement pinned instead. When no maintained replacement exists, mark the choice dropped without replacement and name the gap.

## Leave the dated table in the change

Write the grounded set into the change as one per entry table with versions, dates, links, and a grounding date, so the next reader sees when it was grounded. Each entry carries its pinned version, stable or LTS status, release date, end of support date, release channel link, support window source, LTS versus latest decision, any repo pin or floor that applied with its kept or raised disposition, the maintenance context with its sources, the API pattern change consulted, and the exact version security applicability with advisory citations. Dropped choices are listed with their named replacement or as dropped without replacement. Write only entries grounded from a release channel today; list the rest as blocked, never filled from recall.

## When an entry blocks

- No release channel reachable: mark that entry ungrounded, report which entry blocked and which channel was tried, and pin nothing from recall.
- Support window source unreachable: record the release channel facts obtained, mark the support date unconfirmed with the source attempted, and continue the remaining entries without presenting the date as confirmed.
- Advisory source unreachable: record the release facts obtained, mark security applicability unconfirmed with the source attempted, and never present the version as advisory clear.
- LTS versus latest conflict with no project policy: record both candidates with dates and defer the decision to the human instead of picking silently.
