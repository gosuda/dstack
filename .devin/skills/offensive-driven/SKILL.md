---
name: offensive-driven
description: 'Use when the user explicitly asks for a replacement-first pass such as "rebuild it clean", "replace-first", or "offensive pass on <target>" spanning code, docs, plans, or research. Not for code-only restructuring (existing code skills already own that and stay offensive by default); not for root-cause repair or thin-slice additions.'
---

# Offensive driven

The user names a target and asks for a replacement-first pass. State the contract, expose the broken assumption, re-derive the simplest valid replacement from contract and evidence, preserve what works, remove the obsolete structure, migrate every dependent in scope, and prove the delta with a check suited to the domain. Offense describes the posture toward the broken structure. It never permits rewriting correct structure, erasing needed validation, or widening authority.

## When this applies

Only on explicit user request for a replacement-first pass on a named target (phrases like "rebuild it clean", "replace-first", or "offensive pass on <target>"). Never self-initiate it, and never infer it from bloat, duplication, or trigger phrasing alone. Code-only or architecture-only restructuring already has owners that stay fully offensive by default. This skill adds nothing to them and gates none of them. Root-cause repair and thin-slice additions belong elsewhere too.

## What you may touch

Write only inside the explicitly invoked scope (the exact disclosed path or artifact set). No remote, credential, paid, or deployed mutation. No commit, push, or publication unless the user explicitly asks for it in this invocation. Human approval is required before removing a live or consumer-facing surface, discarding stored data or history, or taking any irreversible, remote, or paid action.

The change replaces the broken structure with the re-derived form inside the invoked scope and migrates every dependent in scope in the same change. It leaves no half-migrated reference behind.

Completion requires all of these: contract stated, broken assumption exposed with evidence, simplest valid replacement derived from contract and evidence, useful behavior and detail preserved, obsolete structure removed, every in-scope dependent migrated, domain-appropriate proof exercised, and actual delta compared.

This skill is self-contained. It names no peer skill as a runtime dependency and delegates no step to one.

## What you work from

The named target, the domain it lives in (code or architecture, plan or workflow, prose or docs, or research), the desired outcome with its consumers, the invariants or obligations that must survive, and the exact surface or path set in scope. Bring the contract source when one exists (signatures plus call-site usage, schema plus stored data, approved plan plus approval boundaries, claims plus cited evidence). Otherwise derive the contract from that evidence during the work. Name the proving check when the repository or artifact type does not define one. Where any required element cannot be established from the request plus local evidence, stop rather than inventing it.

## Running the pass

1. State the contract and bound the surface. Write the desired outcome, its consumers, the invariants or obligations that must survive, and the exact surface in scope (paths, artifacts, interfaces, or claim set). Name every dependent in scope and every live, persisted, or consumer-facing surface whose removal needs human approval.
2. Expose the broken assumption with evidence. Identify the failing assumption or structure and the evidence breaking it (a failing check, contradictory usage, a violated invariant, an unsupported frame). Evidence showing the structure meets its contract ends the pass here with that report. Offense does not apply to sound structure.
3. Re-derive the simplest valid replacement. Build it from the contract and supporting evidence alone, in the smallest form satisfying it: code from signatures plus call-site usage with caller, format, and stored-data safety; prose or docs preserving every obligation and citation; research rejecting the unsupported frame without altering facts; plans or workflows preserving approval boundaries. Carry forward only behavior or detail with evidence behind it.
4. Cut the obsolete structure and migrate dependents. Remove the broken structure within the disclosed scope. Migrate every in-scope dependent in the same change so no caller, link, plan step, or claim references a removed surface. Stop and ask when a dependent falls outside the disclosed scope, when removal needs the human-approval gate, or when stored data or history would go with it.
5. Prove the delta in the domain's own terms. Exercise the narrowest check covering the change: code gets compile plus behavioral checks over the changed contract; docs or prose get obligation and citation review plus any applicable render or lint check; research gets a claim-to-evidence recheck confirming no fact changed; plans or workflows get an approval-boundary and handoff check, with a dry run where the repository defines one. Compare the actual before-and-after delta against the stated contract and report preserved, removed, and migrated items.

## When the pass fails

- Contract or evidence missing: make no replacement edit. Return `blocked` with the exact missing outcome, invariant, surface, or evidence.
- Approval withheld or scope exceeded: make no further change. Return `blocked` with the gated surface or the exact additional path. Never cut on silence and never widen scope implicitly.
- Verification failure: stop. Restore the current increment to the last green state while preserving earlier green work. Return `non-converged` with the failed check and observed result.
- Repeated attempts preserving neither the contract nor the completion condition: return `non-converged` with the last green state, the failed increment, and the evidence. Never report success from a partial replacement or leave a half-migrated dependent behind.

## What to hand back

The stated contract (outcome, consumers, invariants, exact surface), the broken assumption with its evidence, the replacement with per-item preservation citations, the removed surfaces with approvals obtained, every migrated dependent, the domain check run with its observed result, and the before-and-after delta. Terminal classification is `complete`, `blocked`, or `non-converged`. Completeness requires the bound completion condition above.
