---
name: necessary-work
description: 'Use when work is about to grow past the ask, the task may already be done, or the user requests only the minimum. Not for executing the work: use tests-practices to build or grill-core to fix.'
---

# Necessary work

Decide what work is actually needed before anyone does it. Write down the outcome and the smallest proof that would show it, admit only actions that close a real gap, and stop once the minimum set is identified. This skill classifies scope. It changes nothing.

## When this applies

Use this when the work threatens to grow past the ask, when the task may already be finished, or when the request calls for the minimum, only what is needed, or stopping once it works. It does not execute anything. Building behavior belongs to tests-practices and defect repair belongs to grill-core.

## Authority you have here

Read-only. No file, version control, credential, paid, published, deployed, or remote change of any kind. Read the request, the environment, the binding policies, and the available evidence, assess them, and produce a scope decision. Nothing else.

You are done when the outcome and its proof are written down before anything is admitted, every admitted action fails the delete test below, and classification stops at the minimum sufficient set.

## What you work from

- The request and whatever evidence already shows its current state.
- Binding environmental limits or authoritative policies that constrain the outcome.
- Existing measurements only. Do not take new measurements unless the delete test proves one is necessary.
- Where the request is ambiguous and the inputs cannot resolve it, take the smallest interpretation consistent with the stated intent and record that choice openly.

## Paring the work down

1. Write the outcome and the minimum evidence that would prove it, before admitting any work. The contract exists once both are stated in writing.
2. List only candidate actions that could close a stated outcome or proof gap. No action is necessary just because it is useful, conventional, safer, cleaner, or more thorough, so admit none by default.
3. Run the delete test on each candidate: if deleting it would leave the outcome unmet or unproven, admit only its smallest reliable form. Otherwise reject it. Every candidate ends with an admit-or-reject decision and its test result.
4. Admit a limit, threshold, retry, budget, abstraction, artifact, check, process, or follow-up only when its necessity comes from the request, the environment, authoritative policy, or measured evidence. Every admitted action names its source.
5. Classify the admitted and rejected candidates without executing anything or changing any state. Never widen scope or invent evidence to cover a missing input.
6. Stop as soon as the admitted actions and minimum proof satisfy the contract. Add no speculative follow-up work.

## When the classification cannot close

- The request is ambiguous: bind the smallest interpretation consistent with stated intent, flag the ambiguity in the output, and do not widen the contract.
- A candidate has no necessity source: reject it and name the missing request, environmental limit, policy, or evidence. Never invent support for it.
- The available evidence cannot prove the contract: return `blocked` with the exact unproven part and the missing evidence. Do not claim completion, and do not run a new check under this read-only authority.
- A candidate slipped in that fails the delete test: remove it and recompute the minimum set. Since this procedure mutates nothing, no rollback is needed.

A partial classification is acceptable only with its unresolved items named. It counts as success only when the done condition above holds.

## What to hand back

A scope decision ordered by the steps that produced it: the outcome, the minimum proof, the admitted actions (each with the contract gap it closes), the rejected candidates (each with its delete-test result), and a status of `sufficient`, `already done`, or `blocked`.
