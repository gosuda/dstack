---
name: articulate
description: 'Use when the user knows what they mean but cannot express it completely or clearly. Not for discovery, ideation, or style-only editing: use unslop for style.'
disable-model-invocation: true
---

# Articulate

Say what the user means, in the smallest complete form that is ready for its audience, without adding anything they did not supply. This skill is read-only. It makes no file, VCS, credential, paid, published, deployed, or remote change, and it works only from supplied material plus confirmed conversation context. Chat output is the default. An existing draft is replaced only when the user explicitly asks for an edit.

## What I work from

- The thought, fragment, notes, or draft to express.
- The intended audience and medium, when already known.
- Confirmed context from the current conversation.

## How the statement takes shape

First, state the thought's invariant core in one sentence. Then collect only context the user has already confirmed, never researching just to fill a blank. Anything unsupported becomes a blank, a short set of alternatives, or the minimum clarifying question needed to continue. Then write the smallest complete audience-ready form that preserves the original scope, identity, confidence, and intent. Finally, compare every sentence against the supplied material and remove any invented goal, requirement, rationale, fact, or certainty.

## Where I stop and ask

- No invariant core can be stated because the thought is too fragmentary. Ask the user for one more sentence of context. Do not invent the core.
- An invented goal or fact is detected. Remove it and mark the gap as a blank. Never substitute a plausible-sounding rationale.
- The scope drifted during expression. Restate the original scope, discard the drift, and recheck every sentence against the supplied material.
- An unsupported choice is hiding as certainty. Downgrade it to an explicit blank or alternative set. Never present an unsupported choice as settled.

## What you get back

The completed statement, followed only when needed by `Unresolved:` and the remaining explicit blanks or alternatives. The result holds when the statement is audience-ready, every sentence is supported, the user's scope and identity are unchanged, and unresolved forks stay visible.

## When a different skill owns it

- Requirements or intent still need discovering: use the planning owner.
- Several possible ideas are wanted: use `ideate-multiple-agents`.
- A reusable rule must be inferred from examples or material: use `generalize`.
- An external concept must be taught: out of scope.
- The meaning is already complete and only voice or polish changes: use `unslop`.
