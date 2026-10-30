---
name: council
description: 'Use when the user asks for a council, second opinions, or parallel investigation. Not for cross-examination of existing proposals: use cross-critique.'
---

# Council

Call a council when one perspective is not enough: the user wants second opinions, or a question needs investigating from several angles at once. You give each member a distinct stance, let them investigate independently in parallel, then reconcile what they found into a single decision memo.

A council investigates; it never acts. The skill is read-only (no file, VCS, credential, paid, published, deployed, or remote changes), and subagents inherit that posture unless the user explicitly scopes a narrower mutation for them. The deliverable is the memo. Never select or execute a decision unless the user explicitly authorizes further action.

## Framing the question

Take the question or decision under investigation as the required input. The user may also name the member count or the exact stances; default to three distinct stances when they do not. Scope constraints and admissible evidence sources are optional. The user's own criteria bound the investigation: restate the question, confirm scope against those criteria, and do not widen it afterward.

## Giving each member a stance

Pick investigative stances that fit the question, such as an optimist, a skeptic, a risk-auditor, a domain expert, or whatever the genuine angles are. Every member gets a different stance; overlapping stances manufacture false agreement.

## Running the round

1. Spawn one subagent per stance. Each investigates independently from its stance, gathers evidence, and comes back with a position, its supporting evidence, and the risks it sees.
2. Collect every position before reconciling any of them. Merging early buries disagreement.
3. Compare across stances and mark three things: where they agree, where they disagree, and which risks stay unresolved.
4. Synthesize the decision memo: the recommendation, the consensus behind it, dissenting views, residual risks, and the evidence supporting each point.

## When the round wobbles

- A member comes back with nothing usable: mark that stance inconclusive, carry on with the rest, and note the gap in the memo. A memo with some inconclusive stances is still valid as long as every gap is written down. Never silently drop a stance.
- Nobody converges, or the evidence is too thin: return a non-converged memo stating the blocker plainly. Never fabricate consensus or pretend the round succeeded.
- The investigation drifts past the user's criteria: stop, restate the criteria, and re-bind the scope before continuing.
- A subagent attempts a mutation the user never scoped: exclude the action as out of scope and record the violation in the memo.

## The memo you hand back

A decision memo with the recommendation, the consensus reached, dissenting views, residual risks, and evidence for each point. Classify it honestly: converged means the members reached consensus, non-converged means the evidence was insufficient or disagreement stands.
