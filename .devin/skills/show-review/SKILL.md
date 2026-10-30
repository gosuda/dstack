---
name: show-review
description: 'Use when the user wants a per-finding visual walk through a diff, PR, or MR. Not for written review reports: use review. Not for codebase tours: use show-me.'
---

# Walking a diff one finding at a time

The user has a change in front of them and wants to be walked through what is wrong with it, one finding per turn, with a small visual that carries each defect. You show, they decide Keep or Skip, and at the end you tally what survived. You write nothing to disk and patch nothing -- the walk only records what to do next with the kept findings.

If the user actually wants a written sectioned report rather than a turn-by-turn walk, stop: that is `review`. If they want the report posted on the forge (GitHub PR or GitLab MR comments), stop: this is a chat walk, not a forge report. If they want a topic explained without reviewing it, stop: this skill reviews a diff. If they want a grill-until-clean pass with no visuals, stop. If there is no diff and they want unfamiliar code toured, stop: that is `show-me`.

## What you are walking

The change set comes from the human at invocation: named files, a PR number read via `gh pr diff`, an MR IID read via read-only `glab mr diff <iid>` (scoped with `-R GROUP/PROJECT` outside the default repo), the working tree, or a branch against its base. Decide GitHub or GitLab from the verified request URL or repository remote, binding host, project, and PR number or MR IID separately; an MR is addressed by its project-scoped IID, never the global ID. When the evidence is ambiguous, stop and ask rather than defaulting to GitHub.

An empty change set ends the walk at once: report `0 findings.` and invent nothing. Binary, lockfile, and generated paths are never findings.

## How each finding goes

Rank by reachable impact and take the highest remaining finding first, without ever writing out a findings list: ship-blockers and things wrong on plausible inputs first, degraded uncommon paths next, no-behavioral-impact nits last. Keep the untaken titles unsaid -- one finding per message.

Each turn has three parts: the smallest view that carries the defect; one or two lines naming what is wrong, its reachable impact, and `file:line`; and one single-select -- Keep / Skip / Discuss, with `(Recommended)` on the first option. Put the visual in the message body next to the two lines, not in the question-tool preview. Use the harness question tool when it exists (labels only); otherwise number the three options.

Recommend Keep for a named reachable failure and Skip for a no-behavioral-impact nit. The turn ends when Keep or Skip is in hand; the next message is the answer. Discuss gets exactly one round and then collapses back to Keep / Skip only, and a new defect raised during Discuss waits until the current finding has its Keep or Skip.

## Pacing a long walk

After eight behavioral turns, offer one single-select: skip the rest (Recommended) or continue. Either phrase -- "skip the rest" or "keep the rest" -- on any turn closes the walk, counting every unseen finding as skipped or kept respectively. When the list is empty or the rest is skipped, go to Close.

## Picking the view that carries the defect

One view is the common case; cut every line the defect does not turn on:

| The defect is | Show |
|---|---|
| a change against a shape that already exists | focused diff |
| logic or an algorithm | pseudocode |
| what calls what at runtime | call tree |
| UI structure or a module boundary | component tree |
| file responsibility | shallow file tree |
| interaction or data flow between parts | diagram |
| new code, or a missing shape | whole block |

## Closing the walk

Report a one-line tally: how many kept, how many skipped, how many were discussed. If nothing was kept, stop there. Otherwise present one single-select -- Stop (Recommended), apply the kept findings, or grill the kept findings until clean -- and record the user's choice. The walk itself never patches.

If the user stops early, close with whatever was covered: count unseen findings as skipped and report the partial tally honestly, never pretending every finding was decided.
