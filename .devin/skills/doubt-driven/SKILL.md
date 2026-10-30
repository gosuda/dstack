---
name: doubt-driven
description: 'Use when a non-trivial decision sits under uncertainty and correctness matters more than speed. Not for patch review: use review.'
---

# Doubt-driven development

Some decisions are too important to trust to the person who just made them, including you. This skill sets up a hostile reading of your own work: you state the decision plainly, hand the bare evidence to a critic who has not seen your reasoning, and answer every objection before the decision ships. Everything here is read-only and runs in chat. Suggested fixes come back as recommendations you may apply yourself, never as edits this skill makes.

Use it for a non-trivial decision under uncertainty, for any claim the type system or compiler cannot check, and before committing non-trivial code. Do not use it for patch review; that belongs with review.

## State the decision as a claim

Name the decision compactly so it can actually be attacked:

```
CLAIM: "<statement>"
WHY THIS MATTERS: <consequence>
```

If you cannot state it that compactly, you do not have a decision yet; you have a vibe. Surface that and stop; nothing below can review a feeling.

## Isolate what the critic gets to see

Pull out the smallest unit that fits in one read: the artifact (a diff, function, proposal, or assertion plus its supporting evidence) and the contract (the constraint the artifact must satisfy). Strip out your reasoning before handing it over. A reviewer who sees your conclusions will validate them instead of breaking them. A 500-line PR is not one unit; decompose it first.

## Get a hostile reading from a fresh mind

Spawn a fresh-context subagent with isolated context and give it this adversarial prompt verbatim, so it overrides any default balanced-response shape:

```
Adversarial review. Find what is wrong with this artifact.
Assume the author is overconfident. Look for:
- Unstated assumptions
- Edge cases not handled
- Hidden coupling or shared state
- Ways the contract could be violated
- Existing conventions this might break
- Failure modes under unexpected input

Do NOT validate. Do NOT summarize. Find issues, or state
explicitly that none could be found after thorough examination.

ARTIFACT: <paste artifact>
CONTRACT: <paste contract>
```

Pass ARTIFACT plus CONTRACT only. Never pass the CLAIM: handing the critic your conclusion biases it toward agreement. If a reviewer's default shape cannot be overridden to issues-only, fall back to a generic subagent carrying the same prompt.

This step needs the main session, where spawning a fresh-context reviewer works. From inside a subagent, spawning another subagent is blocked, so do not run this skill nested. Surface that to the user and let the main session handle it. Only as a last resort, fall back to questioning yourself: rewrite ARTIFACT plus CONTRACT as a fresh self-prompt behind a hard mental separator from your prior reasoning and walk the same steps. That is not fresh-context review, so flag the result as degraded.

## Answer every finding honestly

Re-read the artifact against each finding before classifying it. Rubber-stamping the critic fails just as surely as ignoring it. Take each finding in this order: first match wins.

1. **Contract misread.** The CONTRACT was unclear or incomplete. Fix the contract and re-classify next cycle.
2. **Valid and actionable.** A real issue. Change the artifact and loop again.
3. **Valid trade-off.** Real, but fixing costs more than accepting. Document the trade-off.
4. **Noise.** Correct under context the reviewer lacked. Note it, and consider adding that context to the contract.

For the highest-severity valid finding, name the cheapest check that would overturn it (a file read, a single command, a minimal reproduction) and run that check before looping again. When no check is cheaper than the fix, record null with the reason instead of inventing one.

Watch for doubt theater: across 2 or more cycles where the critic surfaced substantive findings, zero findings classified as actionable means the critic is validating, not doubting. Stop and escalate to the user.

## Knowing when to stop

Stop when the next iteration returns only trivial or already-considered findings, when 3 cycles are done, or when the user explicitly says to ship. Three cycles is the bound, not a suggestion: do not grind a fourth alone; escalate to the user instead. If 3 cycles still surface substantive issues, that is information about the artifact: it may not be ready, so say so. If 3 cycles is obviously insufficient because the artifact is large, the artifact is too big. Go back, decompose it, and review the pieces. Never lift the bound to fit the artifact.

A stopped cycle with every finding classified is a valid partial result. Unclassified or rubber-stamped findings are not.

## What you hand back

A report listing each CLAIM, the fresh-context findings, each finding's classification (contract misread / valid + actionable / valid trade-off / noise), and the stop condition met. Actionable findings carry a recommended artifact change, stated as a recommendation, not an applied edit.
