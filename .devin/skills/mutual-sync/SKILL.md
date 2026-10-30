---
name: mutual-sync
description: 'Use when the user and agent may hold different pictures of current state after a gap, sync request, or exposed stale claim. Not for persistence: use memory-update.'
---

# Reaching shared context

You and the user sometimes walk in with different pictures of what is true: after a gap, after a sync request, or after the conversation exposes a stale claim. Your job is to reconcile those pictures into one ledger you both trust, then stop. You change no files, no version control state, no credentials, nothing paid, published, deployed, or remote. You inspect only the conversation, topic-relevant files, search results, version control status, and recent history. A partial or unconfirmed ledger is diagnostic output only, never a pass. No rollback is needed because you mutate nothing.

The run is finished when the user confirms a ledger containing agreed facts, corrected beliefs, and open assumptions. Until then, you keep grounding and rechecking, and you do not start substantive work while the ledger is unconfirmed.

## What you start with

A named topic helps but is optional when the current task or the contested claims already set the scope. The conversation supplies each side's existing claims. Claims about in-repository state need the repository or other accessible local evidence available to check against. You ask the user only for what you cannot inspect: intent or external state.

## Classifying how you entered

Decide without asking which situation you are in:

- Pre-work, after a new task or a gap. Seed the claim set from task prerequisites.
- Mid-session repair, after a disputed claim. Seed it from the contested claims.
- Cold re-entry, with no usable working model. Seed it from live local state, and also inspect topic-relevant open changes, task state, in-flight branches, and newly introduced project terms.

## Bounding the topic

Keep the sync to the named or inferable topic. If a bare invocation has no inferable topic, present one blocking single-select question with two or three candidate scopes and stop until one is selected. If scope stays unselected, return `blocked — scope not selected` with the proposed scopes, and inspect nothing beyond what you needed to propose them.

## Grounding each claim

Check each in-repository claim with targeted file reads and searches, never a whole repository scan. Look at read-only version control status and the latest 15 commit summaries to catch a dirty tree or movement since the last shared point. Every in-repository claim ends with `file:line` evidence or is marked `[unverified]`. If evidence is missing or inaccessible, keep the claim under open assumptions with its owner and the exact unavailable source. Absence of evidence never becomes a fact.

## Showing your model and asking your questions

Present your model as short numbered claims, each with its `file:line` evidence or `[unverified]` label. Never ask the user for a fact a targeted read or search could supply.

Ask at most three targeted questions, and only where the user is the likely authority: intent, deployments, sibling repositories, other sessions, or recent decisions. Use a bounded choice when the known options are complete, an open question only when the answer must be narrative.

## Arbitrating fairly

Decide repository-verifiable claims by inspected code and history, correcting stale user beliefs and wrong agent assumptions on equal terms with `file:line` evidence. Treat user statements about intent or inaccessible external state as `[user-attested]`, not independently verified. If a claim stays disputed after evidence is shown, record the dissent and its owner rather than forcing consensus. If a proposed action would mutate anything, stop before it and return `blocked — requested action exceeds read-only authority`, naming the target and action.

## Writing the ledger

Emit one in-chat markdown ledger with exactly these sections:

| Section | Holds |
|---|---|
| **Agreed facts** | Each claim both sides accept, with `file:line` or `[user-attested]` |
| **Corrected beliefs** | Who held each prior belief and what the evidence established |
| **Open assumptions** | Every unverified or disputed item with its owner, including preserved dissent |

Every claim appears under exactly one section.

## Confirming, then offering persistence

Present one blocking choice: `Shared context confirmed (Recommended)` or `Corrections needed`. If corrections arrive, update the claim set, re-ground only the affected claims, re-emit the complete ledger, and ask again. If the same dispute repeats without new evidence, return `non-converged — shared context not confirmed` with the latest complete ledger; rechecks still touch only affected claims.

After confirmation, offer persistence once. This procedure itself neither writes a persistence artifact nor performs the separate action. That offer, or the end of the procedure, closes the run.

## What you return

One in-chat markdown ledger with **Agreed facts**, **Corrected beliefs**, and **Open assumptions**, followed by either `confirmed — shared context established`, `blocked — <reason>`, or `non-converged — shared context not confirmed`. Evidence labels stay attached to every claim.
