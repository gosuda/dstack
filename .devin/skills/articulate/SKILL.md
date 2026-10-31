---
name: articulate
description: 'Use when the user knows what they mean but cannot express it completely or clearly. Not for discovery, ideation, or style-only editing: use unslop for style.'
disable-model-invocation: true
---

# Articulate

Say what the user means in the smallest complete form that is ready for its audience, adding nothing they did not supply.

This skill is read-only. It makes no file, VCS, credential, paid, published, deployed, or remote change, and it works only from supplied material plus context the user has confirmed in this conversation. The answer goes to chat; an existing draft is replaced only when the user explicitly asks for that edit.

## Inputs

- The thought, fragment, notes, or draft to express.
- The intended audience and medium, when already known.
- Confirmed context from the current conversation.

## Shaping the statement

1. State the thought's invariant core in one sentence.
2. Gather only context the user has already confirmed. Do not research to fill a blank.
3. Turn anything unsupported into a blank, a short set of alternatives, or the one clarifying question needed to continue.
4. Write the smallest complete audience-ready form that keeps the original scope, identity, confidence, and intent.
5. Check every sentence against the supplied material and remove any invented goal, requirement, rationale, fact, or certainty.

## Stop conditions

- The thought is too fragmentary to state a core: ask for one more sentence of context instead of inventing it.
- An invented goal or fact appears: remove it and mark the gap as a blank, never a plausible-sounding rationale.
- The scope drifted while expressing it: restate the original scope, drop the drift, and recheck every sentence.
- An unsupported choice reads as settled: downgrade it to an explicit blank or alternative set.

## Output

The completed statement, followed only when needed by `Unresolved:` and the remaining blanks or alternatives. It is done when the statement is audience-ready, every sentence is supported, the user's scope and identity are unchanged, and every unresolved fork stays visible.

## Other owners

- Intent or requirements still need discovering: use `askme`.
- Several candidate ideas are wanted: use `ideate-multiple-agents`.
- A reusable rule must be inferred from examples: use `generalize`.
- An external concept must be taught: out of scope.
- The meaning is already complete and only voice or polish changes: use `unslop`.
