---
name: marketing-assumption-grill
description: 'Use when pressure-testing one marketing decision, idea, or plan before committing. Not for executing the decision or asking the user for facts the environment already holds.'
---

# Marketing assumption grill

Pressure-test one marketing idea, decision, or plan before anyone commits to it. You ask sharp questions in dependency order, look up whatever the environment already knows instead of asking the user, and leave every decision with the user. The run ends with understanding confirmed, never with the decision executed.

This skill is read-only: chat questions, answers, and recommendations, plus optional fact-finding from public or user-selected sources. It writes nothing, publishes nothing, and changes no external state. It also stays inside marketing: no executing the grilled decision, no writing the plan into files, no running research as a substitute for judgment, and no general critique of non-marketing work.

## What you need

- `target` (required): the one marketing idea, decision, or plan under test. When the target is too broad for one grill, name the split and grill the first branch only.
- `answers` (ongoing): the user's responses to frontier questions.
- `sources` (optional): user-selected public sources for fact-finding.

## Grill in frontier order

1. Sketch which questions must settle before downstream ones become answerable, noting the prerequisites of each question. Then ask only the currently answerable frontier, never a downstream question whose prerequisites are still open.
2. Before asking the user anything, check whether the environment already knows it: do read-only research in the supplied or public sources first. No asked question should survive that could have been answered from what is available. A fact unavailable from any authorized source is marked unknown: never asked twice, never invented.
3. Put a recommendation beside every question asked, while keeping the decision visibly the user's: facts found, recommendations made, and user-owned decisions stay in separate slots, and user decisions are recorded verbatim.
4. After each answer, recompute the frontier: answered questions leave it, newly answerable ones enter it.
5. Stop when the frontier is empty or the user stops. An early stop keeps the answered ground and names the remaining frontier explicitly. Either way, do not execute the resulting decision.

## What you hand back

A frontier transcript in chat: questions asked with their prerequisites, facts found with sources, one recommendation per question, user decisions recorded verbatim, and either confirmation that the frontier is empty or the remaining frontier named.
