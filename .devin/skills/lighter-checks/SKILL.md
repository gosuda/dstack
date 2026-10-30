---
name: lighter-checks
description: 'Use when verification is looping, would re-run untouched code, or duplicates an established proof. Not for tasks that require source or remote-system changes.'
---

# Lighter checks

You stop checking from becoming the work. When verification starts looping, threatens to re-run against code nobody touched, or would prove a second time what one tool already proved, you trim it to the smallest set that still proves every claim, run that once, and deliver on the first green gate. The run is done when each claim has exactly one proving action behind it, nothing was repeated for reassurance, and the result went out on the first complete green.

This skill is read-only. It changes no file, touches no version control, credential, payment, publication, deployment, or remote system. It hands back a delivery decision only: deliver, red, or blocked.

What you need before checking: the claims to prove, the changed files or explicitly bounded changed surface, the languages touched, and the project's typecheck, lint, and test commands for those languages. A supplied prior result counts as evidence only when you know its command, its scope, and its outcome, and only when the code it covered has not changed since it ran. Never treat an optional input as evidence, and if the changed surface or the touched languages are unknown, stop rather than inspecting or verifying unrelated scope.

## Prove each claim once

Map every claim to the narrowest action that directly proves it, reusing a supplied result wherever its command and scope genuinely cover the claim. Then cut everything redundant: any proposed re-run against unchanged code goes, and any second tool that covers the same failure class as an accepted result goes. A second action survives only when it proves a distinct claim or a distinct failure class.

Run the project's complete typecheck, lint, and test gate once for every touched language, using the narrowest project-supported scope that still covers the changed surface and reaching for a repository-wide command only when nothing narrower covers it. Treat each command's output as its evidence: do not re-read a diff, repeat a green command, or add a stricter tool just for reassurance.

If every required action is green, stop immediately and return the evidence with a deliver decision. No further check follows the first complete green gate.

## When checking stops instead

The boundary or the command is missing: return `blocked` naming the missing changed surface, language, or project command. Never guess a command or widen scope to fill the gap.

A check fails: return `red` with the exact command, scope, and failure output, and make no repair under read-only authority. Once a correction arrives, re-run only the failed action unless the correction changed another action's covered surface.

A check is unavailable or inconclusive: return `blocked` naming the unproved claim. Partial green results stay as evidence only for the claims they directly cover.

Mutation is required or observed: stop before mutating, or stop at once if a command reports one, and return `blocked` naming the affected target. Never report delivery while any required claim is failed, unavailable, inconclusive, or unproved.

## What you hand back

A chat report listing each claim with its single proving command and scope and its observed result, every omitted redundant check with why it was redundant, and exactly one terminal classification: `deliver`, `red`, or `blocked`.
