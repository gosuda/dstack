---
name: decision-rationale-gaps
description: 'Use when a current decision needs pressure-testing until the rationale is clear to a skeptic. Not for tasks requiring source or remote-system changes.'
---

# Press decision

Use this right after a decision is made, especially one laid out without argument. It pressure-tests the decision until its rationale is clear to a skeptic. You never supply reasons; you extract the user's own. The skill is read-only and advisory: no file, VCS, credential, paid, published, deployed, or remote mutation, and its only power is flagging the decision for re-review over an unexplained gap.

## Setting up the critic

You need the decision text itself: the statement of what was decided, not the reasoning behind it. Surrounding context (which options were considered, which was picked) is optional, and it never goes to the critic. Hand only the bare decision to a fresh session that did not watch the decision get made, and ask what a skeptical outsider would challenge, what is assumed but unstated, and what must be true for the choice to hold. That response becomes the candidate pool for the whole press.

Do not run this from inside a subagent: spawning the critic needs a main session, and nested spawning is blocked. If you find yourself nested, surface that to the user and let the main session handle it. Only as a last resort, fall back to degraded self-questioning. Rewrite the critic instructions as a fresh self-prompt behind a hard mental separator from all prior reasoning about the decision, work the gaps below on the result, and flag the result as degraded.

## One gap at a time

Keep the critic's full response as the pool and extract its single sharpest gap that no earlier round has extracted. Never batch gaps into a checklist. When the pool is exhausted, the loop ends. An empty or unparseable critic response ends pressing immediately: name the decision as carrying an unresolved-critic-response gap.

## Pressing and judging

Present the current question and the gap, or its narrowed form, and ask the user to explain it in their own words. Then judge the answer: if it genuinely resolves the gap, close it and extract the next gap from the pool. If it restates the question, deflects, or leans on authority ("the agent suggested it"), do not accept it. Identify the exact part that stayed vague, narrow the question to it, and press again. Narrow further each round; never widen back to a generic question or repeat what you already asked.

## Knowing when to stop

Either every gap gets explained in the user's own words or at least one does not. Both are valid endings. For each surviving gap, name the specific assumption behind it; the optional context may help name which assumption a gap rests on, but never answer it. Flag the decision for re-review: that is not a verdict that the decision was wrong, only that it is not yet earned. Never force a resolution or let an open gap get papered over.

## The report you hand back

A decision-press report in this order: the neutral restatement of the decision, each gap's state (closed with the user's explanation, or open with its unexplained assumption), gap counts, and re-review flags for every open gap.
