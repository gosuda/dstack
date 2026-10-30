---
name: cybernetic-loop
description: 'Use when the caller supplies a falsifiable out-of-happy-path invariant and a finite budget. Restores via bounded patches or reverts. Not for normal feature delivery or universal retries.'
---

# Cybernetic loop

Sometimes a system leaves its happy path: a reorganization breaks an assumption, peer-to-peer behavior drifts, an index no longer recovers. This skill restores one such broken property and nothing else. The caller names a single checkable property that is currently false (the invariant) and a finite number of repair attempts you may spend (the patch budget). You freeze the checks, checkpoint the working tree, then try the smallest repair that could work, keeping a change only when the full check set measurably improves. If the budget runs out or the failure refuses to converge, you put every byte back and say so plainly.

Do not reach for this loop for normal feature delivery, for behavior that already works, or as a generic retry wrapper. It restores one named property or it reverts.

Talk about a run using only these literal concepts: `invariant`, `executable check set`, `patch budget`, `candidate patch`, `check result`, `checkpoint`, `run transcript`. Do not redescribe the work through control-theory metaphors; the words above are the whole vocabulary.

## What you need before starting

Refuse the run before touching anything unless all three hold: exactly one invariant, stated so a check can falsify it, describing behavior outside the prior happy path; a patch budget that is a finite positive integer, where every attempted candidate patch spends one unit whether it is kept or reverted; and a repository working tree with existing executable checks. No candidate patch and no result may be assumed up front. A request that is really feature work, a happy-path request, a universal retry, or an invariant whose truth no check can execute is `invalid-input`: stop before mutation.

## Freezing the run contract

Work through these in order; each one gates the next.

1. Narrow the blast radius. Derive the smallest working-tree scope that could restore the invariant and record it. No remote mutation: every write stays inside that bounded local scope and nothing in the run reaches a remote system. Anything the repair would need outside that scope is scope widening: stop the run rather than widening.
2. Turn the invariant into a check without weakening it. Give it explicit pass and fail results, combine it with the repository's existing executable checks, then freeze the complete set and echo it back as the run contract: every check, its exact command, its pass criteria, the bounded scope, and the patch budget. From here on you never add, remove, weaken, or replace a check.
3. Checkpoint every byte in the bounded scope so it can be restored exactly, including edits that predate the run. If an exact checkpoint cannot be made, the recovery mechanism is unavailable: stop before mutation as `non-converged` rather than repairing without a way back.
4. Run the full frozen check set against the unmodified tree and record every result. If everything passes in this one run, the property already holds: return `already-holds` without changing the working tree.

## Trying repairs inside the budget

While checks fail and budget remains, pick one failing result and apply the smallest candidate patch within the bounded scope that could restore it. Spend one budget unit, run the full frozen check set again, and record the patch with every result.

Then compare that run against the immediately preceding retained state. Keep the candidate only when at least one previously failing check now passes and every previously passing check still passes. Anything else is a `candidate-regression`: revert that candidate exactly. The attempt still consumed its budget unit.

After each full run, return `restored` only if every frozen check passes together in that single run. Otherwise stop as `non-converged`, naming the stop class honestly: the budget is exhausted, an equivalent failure repeated, results oscillate between prior states, a frozen check became unavailable (`unavailable-check`: a check that cannot compile or execute ends the run), or restoration would need scope widening.

## Leaving the tree as you found it on failure

Every `non-converged` stop restores the whole bounded scope to the checkpoint before returning the complete run transcript. `non-converged` never carries a partial retained patch; its only valid working-tree state is the checkpoint state. If restoration itself fails, that is a `recovery-failure`: report the failed restoration operation and the remaining working-tree delta explicitly, and never claim `already-holds`, `restored`, or a clean rollback you did not observe.

## What you hand back

The frozen run contract from above plus exactly one terminal record: `already-holds` with the pre-mutation check results and no patch attempted; `restored` with the kept candidate patches, the budget spent, the check results, and the final all-passing run; or `non-converged` with the stop class, every patch and result, the budget consumed, and proof the checkpoint was restored.
