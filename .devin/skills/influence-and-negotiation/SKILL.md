---
name: influence-and-negotiation
description: 'Use when an agreement-seeking interaction arises, including mid-conversation moments the model detects.'
disable-model-invocation: true
---
# Influence and negotiation

This skill prepares you for an agreement-seeking interaction, helps you respond while one is happening, or debriefs one that already happened. It works from interests and evidence, never from tricks. Every tactic it suggests would still work if the other side knew about it.

It is read-only. It never writes files, touches version control, uses credentials, spends money, publishes, deploys, contacts anyone, makes commitments for you, or changes anything remote. The only thing it may do beyond reasoning is send out read-only web research sub-agents to fill in missing background on a counterparty, an organization, or a domain fact.

## What you are walking into

Give it a situation description: what is being negotiated, who the parties are, and where things stand. That is the one required piece. Anything else sharpens the advice:

- Who the other side is (interests, constraints, style, power, history with you).
- Where you stand (best alternative to a deal, walk-away point, target outcome, constraints). If you skip this, the skill infers a reasonable starting position from the situation rather than stalling.
- The actual exchange so far, for a live moment or a debrief (transcript or notes).
- Which job you want: `prepare` for an upcoming talk, `live` for one happening now, or `debrief` for one already over. If you do not say, the skill picks from the evidence (a transcript or active exchange means `live`, a concluded interaction means `debrief`, otherwise `prepare`). When the state is genuinely unclear, such as an upcoming talk with a fragment of transcript, it defaults to `prepare` and notes that live scripts can follow once the interaction starts.

If your description is so vague that not even one Mandascan point below can be filled in, it stops and asks for the specific missing pieces instead of building on air.

## How it maps every side

For each party, the skill builds the Mandascan five-point map and writes the answers down.

| Mandascan point | What it captures |
|---|---|
| Interests | Underlying needs, not stated positions |
| Alternatives | Best alternative to a deal (BATNA) and walk-away threshold |
| Legitimacy | Objective criteria, precedents, or norms each side can cite |
| Commitment | What each side can credibly promise and actually enforce |
| Communication | Channel, tone, and relationship quality between the parties |

Anything without evidence is marked unknown, never invented. The map counts as done only when all five answers exist for every party, with gaps labeled unknown.

## Where a deal can live

The skill names the single dimension where the parties interests overlap most, or where the largest joint gain sits. That axis is stated outright, and the rest of the work trades around it. If the map shows the positions cannot meet anywhere, the skill says so plainly and advises strengthening the BATNA instead of forcing a deal.

## How it stays honest

Every tactic is tested before it is suggested: would it still work if the other side understood it was being used. Tactics that pass (shared value, legitimate framing, transparent reasoning) are kept. Tactics that fail (deception, coercion, exploiting cognitive biases for one-sided gain, hoarding information by concealment) are dropped. If you ask for a tactic that fails the test, the skill refuses that tactic, explains which line it crosses, and offers a transparent way to pursue the same goal.

## What you get back

The output depends on the moment. Each artifact lists every applicable requirement with a written entry. A conditional requirement that did not apply says why it was skipped, and missing evidence stays marked unknown.

Preparing for an upcoming negotiation, you get a mandate plus a mutual-gains agenda:

- Opening position, target, and reservation point with the objective criteria behind each.
- A MAP (Mutual-gains Agenda Protocol): issues ordered by joint-gain potential with proposed trades and package deals.
- A short opening statement that names shared interests and invites joint problem-solving.
- The three counterparty moves or objections to expect, each with a response that steers back to joint value.
- Where several parties or internal team dynamics matter, the coalition structure and team roles.

In the middle of one, you get a script for the latest move:

- What the other side words reveal about interests, hidden concessions, or anchoring.
- The move classified as anchor, concession signal, objection, reframing, stalling, or power play.
- A 2 to 4 sentence reply that answers the move, advances your position, and stays honest.
- Any implicit concession or newly revealed interest called out by name.
- At a decision point, a clear call to close, package-trade, or pause.

Looking back at one, you get a retrospective:

- Timeline with key moves, turning points, and outcome.
- A score for each Mandascan answer (was it right beforehand, and where was it wrong).
- Each pathology found by name (anchoring bias, reactive devaluation, escalating commitment, mythical fixed pie, premature closure, loss of face) with the moment it happened, what it cost, and what would have worked better.
- Transferable lessons on what to prepare differently, what worked, and what to avoid.

## How it checks itself

Before delivering, the skill checks that each recommendation traces to a Mandascan point or an observed move, and cuts anything that does not. If background that matters is missing, it dispatches a read-only research sub-agent and folds the findings into the map. If the research comes back empty, it proceeds with what it has while flagging which answers still lack outside grounding.
