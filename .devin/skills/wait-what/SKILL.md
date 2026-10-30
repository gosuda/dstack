---
name: wait-what
description: 'Use when the user says "wait, what", "the explanation is unclear", "say that again", or asks to restate the last response in plain language. Not for tasks that require source or remote-system changes.'
---

# Wait, what

You re-pitch an explanation that did not land. The claim and its conclusions stay exactly the same, and you supply the context the first version assumed. The result is one plain language message in chat. Nothing touches disk, and you never soften the claim into an easier one to make it land.

The failed explanation is the last assistant message before the trigger. If a `CONTEXT.md` exists, read it. When the project keeps a `CONTEXT-MAP.md`, read the per-context `CONTEXT.md` beside the relevant source instead. When neither exists, use the names already in the code. No external file is required beyond this.

## The three ways in

One skill, three entry phrasings, one mechanism:

| The user says | What went wrong | How you respond |
|---|---|---|
| Wait, what, or say that again | The explanation did not land | Re-pitch the same claim and lead with the context it assumed |
| The explanation is unclear, or context was omitted | The prior version skipped background, definitions, assumptions, causal links, or prerequisite steps | Re-pitch from scratch in plain language, embedding the missing context where the original jumped ahead |
| Restate in plain language | Jargon or length got in the way | Restate the last response concisely, preserving its meaning and adding no new claims, opinions, or information |

All three produce a single re-pitched message in the conversation.

## How to re-pitch

1. Identify the failed explanation: the last assistant message immediately before the trigger.
2. Restate the same claim with its substance and conclusions intact, without hedging or substituting a simpler point.
3. Lead with the missing frame in one or two sentences (where the conversation is and what the message was answering), then give the claim in ISO 24495-1 English: short sentences, active voice, direct address, common words in place of jargon, and the project's own ubiquitous language for its concepts.

## When to stop instead

- If the user signals they still do not follow after one re-pitch, stop and report non-converged. The user is the authority on whether the explanation landed, so do not elaborate, restate a third time, or widen scope.
- If no prior assistant message exists, stop and say there is nothing to restate. Never invent a prior explanation.
- If the confusion signal is ambiguous about which part was hard to follow, ask which part before re-pitching.
- If the re-pitch would require teaching a whole prerequisite topic, state that boundary and offer to cover it separately instead of widening into a tutorial.
- Leave no caveats, meta-commentary, or references to the original explanation failing in the re-pitch.
