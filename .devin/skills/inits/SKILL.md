---
name: inits
description: 'Use when onboarding to a repository, capturing costly conventions, constraints, or rationale, or improving AGENTS.md. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Inits

You turn costly repository knowledge into a short `AGENTS.md` that tells future agents what they must do, must not do, or must preserve. Only an explicit human request starts this work, and only the resolved `AGENTS.md` ever changes. Nothing here touches remotes, credentials, publishing, deployment, or anything irreversible, and a rollback is always the pre-write contents (or deletion, when you created the file).

## Settle the root and the single target

Resolve the repository root and the one target `AGENTS.md` inside it. A target outside the repository is rejected with no mutation. The resolved root file is the single source of truth: every other agent file is a pointer or a tool-specific supplement, never a second copy. Where a tool in use reads only CLAUDE.md, recommend that the human links CLAUDE.md to AGENTS.md rather than copying. Personal overrides belong in the gitignored local file, never in shared knowledge.

Anything every tool must obey goes inline, because chains of file references stop resolving after a few hops and references inside code spans never evaluate. Never hide safety, data-loss, or format rules behind an indirection; reserve indirection for depth only the primary tool needs. Child-directory files load on demand in their own subtree, so promote universal rules to the root. Keep project commands out of the per-user global file.

## Admit only what a future agent cannot derive

Read the existing target when one exists, then inspect only the repository files relevant to its candidate instructions (build and test configuration, manifests, automation, architecture boundaries, nearby docs). Record which files you actually read.

Admit a candidate only when it tells a future agent what it must do, must not do, or must preserve. Reject repository descriptions, inventories, generated facts, and any command or setting a future agent can derive directly by reading the repository. For each admitted instruction, point to evidence in a file you actually read or tag it as human-supplied; never infer missing policy from common practice and never invent evidence. Human-supplied conventions, constraints, or rationale count as candidates too, but keep them distinguished from repository-grounded evidence.

## Prune the existing file line by line

Walk the current target line by line. Preserve grounded, non-derivable prescriptions and propose removal of descriptive, stale, duplicated, or directly derivable lines, naming the reason for each removal.

Prefer enforcement over prose, in this order: linter or formatter rule, hook, CI check, then tool-native hooks. Remove prose only where blocking enforcement is demonstrated by an observed violation under the applicable configuration; otherwise classify the rule as warning-only or unverified and retain whatever actionable gap rule it still earns.

## Write the smallest coherent file, then re-check it

Write the target so it contains only the admitted instructions, each stated operationally with its condition and its required action or prohibition. Then re-read the result and verify every instruction against the admission gate and its recorded evidence; anything ungrounded or derivable comes out before you declare success.

Where the environment allows, run the commands the file names. A passing check alone never proves you ran the commands. Otherwise verify each command exists in the manifest, note the limitation, and mark the check unverified rather than passing it.

## Report what changed and how to undo it

Report the target path, the evidence files you read, the applied additions or changes, the removals with reasons, and the rollback path (restoration of the pre-write contents, or removal when the target is newly created).

Stop with `blocked` instead of a partial draft whenever the work cannot complete honestly:

| Situation | Outcome |
|---|---|
| Invalid or ambiguous target | Make no mutation and return `blocked` with the unresolved repository root or target path. |
| Insufficient evidence | Omit the unsupported candidate. If no instruction survives, leave an existing target unchanged, do not create an empty target, and return `blocked: no grounded, non-derivable rules`. |
| Unsafe scope expansion | Stop before changing any file other than the resolved target and return `blocked` with the out-of-scope change required. |
| Write or verification failure | Restore the pre-write target contents when possible and return `blocked` with the failed operation and whether rollback succeeded. If rollback fails, report the exact partial state. |

A partial draft is never success. Return it only as a partial result with its unsupported candidates and unapplied removals identified.
