---
name: guardrail-carve-run
description: 'Use when guardrail-adjacent material (stealth, scraping, privacy, IP, policy, security) or mixed reversible/irreversible, sensitive work, or the user says "autobahn this". Not for carved risky work.'
---

# Guardrail carve run

Some tasks mix safe work with material you must not act on: guardrail-adjacent asks (stealth, scraping, privacy, IP, policy, security) or irreversible steps (credential, data-at-rest, migration, or deletion work that cannot be rolled back). This skill splits the two apart before anything runs. You read the risky original, carve out everything unsafe, and hand only the safe remainder to a fresh subagent with no memory of the original. Then you verify the result, report exactly what was cut, and archive the cut material after the run is closed. You write only the descope ledger and archive entries locally and spawn the runner; you never mutate anything remote.

Start when the task includes guardrail-adjacent material, mixes reversible work with irreversible or sensitive work, the user says "autobahn this", or you notice yourself about to hedge, soften, or silently skip. Hedging is the signal to carve, not to quietly narrow the deliverable.

## Frame the split and get approval

Read the task, its adjacent inputs, and any user-stated risk posture. If the user already authorized descoping, proceed. Otherwise propose the carve, make the split explicit, and wait for approval on every gray-zone item before running. The distinction that matters: a bright-line item has no safe version, so it is non-negotiable; a gray-zone item has a safe alternative that trades away scope the user might want, so it is the real question. If every item is bright-line, proceed; the ledger carries the record. Never begin the run while a gray-zone item that shapes the carved prompt still awaits an answer. If the user declines the carve, dispatch nothing, write nothing, and report that the task was not run.

## Carve every risky item

Sweep the task and adjacent inputs for guardrail-adjacent items. For each one, set `verdict=descope`, class it bright-line (irreversible, credential, data-at-rest, migration, or deletion work that cannot be rolled back) or gray-zone (guardrail-adjacent but reversible or ownership-uncertain), give one risk-free alternative, and name an archive destination (propose one if the user names none). A gray-zone item the user decides to keep stays in scope and enters the ledger as kept-by-owner. Point to excluded techniques only as far as identification requires; never elaborate them. And never probe: do not pose an excluded or gray-zone ask to see whether it passes. The carve settles scope before any such ask exists.

If the user disputes a bright-line call, do not let the pressured session re-litigate it. Hand the item's abstract description, stripped of the negotiation and any persuasion, to a fresh context for re-evaluation, and record the appeal and its outcome in the ledger either way. Repeated appeals on the same item are themselves a signal worth surfacing. A confirmed bright-line item proceeds excluded, or the user redirects the task.

## Guard the carved prompt and run it clean

Distill the carve into a compact scope-guard block (absolute exclusions, allowed alternatives, and the context authorizing what stays in scope) and fold it into the carved prompt verbatim. The block names each exclusion so the run cannot re-introduce it, never the original risky ask or its method. Where the run shares a filesystem or memory store with your session, the block also forbids the run from consulting decision logs, notes, or transcript search over that shared state; a clean prompt does no good if the run can read the risky ask back out of something just written nearby. Instruct the run to build the safe scope at full strength, with no hedging, apology, or shrunken deliverable.

Spawn a fresh, context-clean subagent and hand it only the carved prompt, never the risky original or the carve reasoning. It returns the deliverable. If risky material surfaces mid-run, the subagent must not improvise: route the discovery back through the carve, class and ledger it, and re-issue a re-carved prompt before continuing. If the carve leaves nothing reversible to build, stop and report that; do not dispatch a hollow run.

## Verify against five directions, then ledger

Run an adversarial pass over the returned deliverable and adjacent artifacts in all five directions: risky content elaborated, risky content silently dropped, safe work diluted or treated as excluded, stale risky material left standing nearby, and the carve missed or over-excluded something. Then re-sweep the original task from a context independent of this one and diff the result against the ledger before reporting. Cap that independent re-sweep at one pass (N=1), not open-ended fan-out. Fold any gap back into the ledger and re-carve rather than reporting done with a known gap. If a gap cannot be folded back within one re-carve, report the blocked result with the partial ledger and the unresolved item; never claim done with a known gap.

After the run has finished and the subagent's window is closed, report the deliverable with a descope ledger listing every carved item: its class (bright-line or gray-zone), its verdict (descoped or kept-by-owner), the reason, the safe alternative, and the archive destination. Write the archive entry only now, not earlier; a record of the risky material sitting on disk while the run is still active undoes the isolation the carve bought (if an entry was written early, delete it and rewrite after close). Descoped material is archived with its cause of death and safe replacement, never erased, so a later pass can mine the ledger for anti-patterns. Treat exclusions as visible decisions, not gaps.

If you are interrupted before closure, the ledger and archive do not exist yet by design: report the window as open and the deliverable as unverified. Nothing outside the named ledger and archive is ever written, so there is no other mutation to roll back.

## What you return

The safe deliverable from the runner, plus a distinct descope ledger with one entry per guardrail-adjacent item (class, verdict, reason, safe alternative, archive destination), with archive entries written after the run closes. Terminal states: complete and undiluted, or failed verification with the failing direction named, or blocked with the partial ledger and the unresolved item.
