---
name: abstract-well
description: 'Use when the user wants to classify abstractions as useful, bad, or busy and keep one shallow level. Not for tasks requiring source or remote-system changes.'
---

# Abstract well

Good abstractions earn their keep; the rest is ceremony. This review sorts every abstraction in scope into useful, bad, or busy, then keeps a single shallow level, the one whose payoff over writing the code inline is largest. Nothing here touches the disk. The result is a judgment delivered in chat.

## What you need before judging

Ask for an explicit list of abstractions (wrappers, helpers, interfaces, layers, adapters) or a scope (file, module, function set) you can enumerate yourself. If the input gives you neither, stop and ask for one rather than guessing which wrappers count.

For each abstraction you also need two things: whose code uses it (the immediate consumer when nobody says otherwise), and what the wrapped operation actually is. When the underlying operation is unknowable, do not invent a raw form. That abstraction leaves the review marked unclassified and carries no recommendation.

## Judge cooked against raw, same caller, same task

For every abstraction in scope, write both forms at the same caller task: the raw form, what the caller writes without the abstraction, and the cooked form, what the caller writes with it. Both forms must serve the identical task for the identical caller, or the comparison is meaningless.

Then classify by asking whether the cooked form is genuinely easier (fewer concepts, less ceremony, fewer places to get wrong):

| Class | Meaning |
|---|---|
| useful | The cooked form is easier than the raw form. |
| bad | The cooked form is harder: more indirection, more concepts, or more ceremony than going inline. |
| busy | The cooked form is neither easier nor harder. It relocates complexity without reducing what the caller must get right. |
| unclassified | No concrete raw form could be written because the operation is unknown. |

## Keep one level, never a stack

From the useful pile, keep exactly one: the abstraction whose cooked-form advantage over its raw form is largest. If nothing is useful, say so plainly and select nothing. That is a valid result, not a failure.

Where two abstractions sit between the same caller and the same raw operation, keep only the stronger of the two. Stacked layers that share a caller and an operation never both survive.

## What you hand back

A table with one row per abstraction (its name, a raw-form summary, a cooked-form summary, and its class), followed by the single level you kept with its cooked-versus-raw justification, or the explicit statement that no level was selected because nothing was useful.
