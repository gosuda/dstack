---
name: fromzero
description: 'Use when replacing a greenfield attempt with a clean pad of verified requirements. Not for rebuilding from primitives: use from-first-principle. Requires a committed, VCS-recoverable attempt.'
---

# Fromzero

Sometimes the honest move is to throw the attempt away and start the pad over, carrying forward only what was actually proven. You confirm the old attempt is safely committed, filter its requirements down to the verified ones, open a fresh branch with a cleared surface, and write the new pad. The old work survives in version control the whole time.

This replaces an attempt, it never patches one. Rebuilding a design from primitives belongs to from-first-principle. Act only on an explicit human request, and change nothing remote. If any precondition below fails, change nothing at all and tell the human exactly which step is blocked and what they must do.

## What you start with

| What | Requirement |
|---|---|
| The current greenfield attempt | Under version control and committed, with a clean working tree |
| The requirements list | Each item proven, meaning tested, accepted, or otherwise demonstrated with a named citation (a surviving test, a gate result, a checked schema, or the triggering complaint) |

Speculative or unverified scope is not proven and does not travel.

## Clear the pad in order

1. Confirm the current attempt is committed and recoverable through version control. If uncommitted or untracked work exists, stop and ask the human to commit or discard it first. The old attempt must be reachable in history before anything else moves.
2. Filter requirements to verified ones only. Carry an item forward only with its citation attached, discard everything unevidenced, and record each carry and discard decision with its reason.
3. Open a new branch from the recoverable commit, then clear the working surface. Before touching anything, show the exact set of tracked targets the clearance will delete. The mutation is branch creation plus clearance of exactly that listed set, nothing else, and never some unspecified reset.
4. Write the new pad using only the proven requirement statements. Do not reintroduce discarded scope.

## What you hand back

A new greenfield attempt on a clean pad carrying only verified requirement statements, with the old attempt still reachable in version control history.
