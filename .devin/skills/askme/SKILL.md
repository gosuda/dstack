---
name: askme
description: 'Use when eliciting intent/scope/referents or gating long/bundled/high-stakes/hard-to-undo work: exhaustive/collaborative/adversarial/grill/gate/batch/interview/proposal/pairing. Grill me and grill batches select evidence-backed, chat-only grill mode. Not for scanning a stated request: use clarify. Not for one fork by default: use decide.'
---

# Ask me

Askme is elicitation, not execution. It draws out what the user actually wants before anything gets built: intent, scope, referents, and the decisions hiding inside a bundled or high-stakes instruction. Nine modes cover nine elicitation postures, and routing to the right one is the first half of the job. The second half is asking good questions and knowing when to stop. Answers here never authorize implementation. Silence never counts as confirmation.

The neighbors stay distinct. A request to scan a stated task or conversation for ambiguity or gaps belongs to clarify, unless it specifically asks to grill requirements or assumptions. An ordinary request to resolve one fork belongs to decide; an explicitly selected askme mode still wins over that automatic routing, so adversarial remains available to walk one fork at a time without implementing.

## Choosing the mode

An explicit mode argument always wins, even over words inside the material being examined. Keep that mode until the user changes it. `mode:batch` followed by "grill me" still runs neutral batch. An explicit `mode:scan` is not executable: explain that independent ambiguity scanning belongs to clarify and do not run a duplicate scan here. If the caller supplies several conflicting explicit modes without saying which governs, ask one mode-selector question and start neither procedure. Never resolve that conflict by argument order or by assuming a default.

Without an explicit mode, listen for these selectors in the user's operative request (not in quoted examples or in the material under review), preferring the specific grill phrasing over the generic adversarial or neutral-batch phrasing:

| What you hear | Mode |
|---|---|
| "grill me", "grill batches", grill this requirements set or these plan assumptions | grill, evidence-backed and chat-only |
| "poke holes", "stress-test", "find weaknesses", or an otherwise unqualified "grill" | adversarial, one fork at a time |
| "batch ask me", "clarify the design space", or neutral multi-fork elicitation | batch |
| "help me refine", "walk through with me", "let's brainstorm", "share tips" | collaborative |
| "interview me", "define requirements", "choose between options" | interview |
| Handed-over material with no sufficiently formed ask | proposal |
| Long, bundled, high-stakes, or hard-to-undo instruction; ambiguous scope or referents; a request to verify understanding | gate |
| Underspecified request seeking interactive intent discovery, with no other qualifier | exhaustive, the default |

If two genuinely incompatible automatic readings remain and neither is more specific, ask which should govern. Never silently promote an explicitly selected mode. For automatic collaborative selection, the escalation signals below stay guidance: propose a mode change rather than treating an unresolved signal as the user's answer.

## How every question should look

Fire clarifying questions through the ask-user tool, at most four per fire, sending larger sets as sequential batches ordered by dependency (batch and grill use the frontier rule in the next section instead). If no question tool exists, emit the questions as chat text and await replies. Missing tool support never supplies an answer.

Each question is a full sentence ending in `?`, with a `header` chip of at most 12 characters where supported. Set `multiSelect` false for single-pick mutually exclusive axes and true only for additive subset picks such as feature toggles or optional subtasks. Give each option a 1 to 5 word `label` with `(Recommended)` appended to the recommended choice and placed first, plus a one-sentence trade-off `description`. A `preview` (markdown or monospace box) is optional for visual comparisons, single-select only, skipped when the difference is purely conceptual. Never add an explicit "Other" option; free-text "Other" is automatic on every question, and free-text notes go in the `annotations` response field. Use the tool only to clarify requirements or choose between approaches during elicitation, never to ask "is the plan ready?". And never emit a single `multiSelect: true` checklist where unticked means "default stands". That intent becomes N per-axis single-select questions instead.

## Asking in rounds

Batch and grill never dump every question at once, and never dribble them out one round per tool fire. Each round asks the whole current frontier together: every open decision whose factual and decision prerequisites are already settled. A question whose answer depends on another open question belongs to a later round, not this one. A running research task is an unsettled prerequisite, so only its downstream questions wait.

When the frontier holds more than four questions, send the four highest-impact ones through the tool (rank by downstream decisions unblocked, break ties toward the least safe default to assume) and put the rest in the same message as:

```markdown
**Q<n>: <question title>**

<Question body and choices>

-> Recommended: <answer>
```

Tool and Markdown answers belong to one answer set, so do not omit overflow questions or split the ready frontier into successive tool-only rounds. Preserve stable ids across tool and Markdown forms. The three batch-family modes share this scheduling but stay distinct in method:

| Mode | Method retained |
|---|---|
| adversarial | Challenge one fork, recommend an answer with a reason, wait, then follow dependencies parents-first. Never batch implicitly. |
| batch | Neutral design-tree elicitation, holding weighted intent hypotheses and falsifiers before the first fire. Shares frontier scheduling without per-question counterexamples. |
| grill | Evidence-backed challenge of requirements and assumptions, with concrete counterexamples, recommended verdicts, and independent frontier batches. No mandatory hypothesis block. |

## The quick check before risky work: gate

Gate exists for instructions that are long, multi-part, ambiguous in scope or referents, deliberately flexible, high-stakes, or hard to undo, where a wrong read costs real work. If none of those signals is present, stop without acting.

When gate engages, paraphrase the instruction in your own words (copying the user's wording back is not understanding) and compare that restatement against all available context: the current message, session history, project memory, filesystem, and established conventions. Look for contradictions, missing antecedents, or two plausible readings context cannot choose between. If context resolves every fork, proceed silently and surface nothing. If a genuine fork survives, surface exactly one specific clarifying question anchored to the restated understanding and naming the choice, then hold substantial work until it is answered.

Gate writes nothing before it passes except, for substantial work after the decision, one durable `understood as: ...` log line. It performs no file, credential, paid, published, deployed, or remote mutation before the decision. What goes wrong here: no read signal means pass silently; a restatement that does not match the instruction becomes the first finding and stops everything until resolved; multiple genuine forks surface the highest-stakes one first with the rest held; a question later resolved by context gets retracted with a silent pass.

## The handoff with no real ask: proposal

Read every piece of the handed-over material end to end before proposing anything. State the intent read from the data in one line grounded in what the data actually shows, sketch the next action briefly, and propose only to confirm: right, wrong, or adjust. If two intents are plausible, propose the likelier and name the other in a clause. One intent per turn. If the data is too thin to propose from, say so and stop; do not fall back to asking. If the user composes the ask from scratch, the proposal was wrong or a question in disguise, so redo it grounded in the data.

## The slow interview: one assumption at a time

State that this is a requirements interview and confirm whether the goal is defining requirements, resolving a decision between options, or both. Begin no file change, build, or investigation until the decision record is approved. Ask one focused question exposing the most fundamental unstated assumption in the stated goal, wait for the response, restate what was confirmed or corrected, and add it as a row in the running decision log. After each answer ask "What else is unstated or assumed in this goal?" Stop when the user says nothing remains, explicitly declines, or confirms the record is complete. Present the complete log (each assumption, its resolution, the final agreed scope or decision, no implementation plan), ask the user to approve, amend, or reject any row, and repeat until approved. Then write the approved record to a user-named local file, defaulting to `DECISION-LOG.md` in the current working directory. What goes wrong here: an empty goal means ask for the goal and stop if declined; a mid-interview request to implement ends the interview with "no decision recorded" and no file written; a log written before approval gets deleted, since the log is written only after explicit approval.

## Hypotheses first: verbalized sampling

Exhaustive, adversarial, and batch start by sampling multiple intent hypotheses, each with a probability weight on a 0 to 1 scale and a falsifier (the specific observation or scenario that would invalidate it). Expand depth as ambiguity, risk, or architectural surface grows; keep it concise when scope is truly narrow. Render this block immediately before the first question fire of the session; later fires need not repeat it unless the survivor set materially changed:

```
1. [Weight: 0.42] hypothesis here
   - Falsifier: [observation or scenario that would invalidate this]

2. [Weight: 0.28] hypothesis here
   - Falsifier: [observation or scenario that would invalidate this]
```

In batch, seed the design-tree roots and initial frontier from the surviving hypotheses. Collaborative never runs this block. Grill has no mandatory block; its concrete evidence, counterexamples, and decision ledger provide the basis instead.

## Wide search: exhaustive

Deliberately seek unconventional, underexplored, and edge-case possibilities around the objective, drawing on context and plausible but non-obvious requirements. Include at least 3 edge cases (at least 5 when architectural) and stop expanding once additional cases no longer change decisions. Broaden sampling if no clear leader emerges; if none emerges after broadening, surface the decision point with concrete options and trade-offs rather than picking silently. Synthesize surviving hypotheses into one consolidated direction before responding.

## Trading tips: collaborative

Hold a two-way tip-sharing dialogue: surface one of your own observations or tips back to the user as a counter-tip per round, and let depth emerge through exchange. No hypothesis block, no scoring, no ranked sample. Stop when the user signals convergence.

## Walking the tree: adversarial

Take one fork at a time: state the question, recommend an answer with a one-sentence rationale, wait for the user, and do not proceed on assumed answers. Resolve dependencies parents-first and never descend into children while a parent is unresolved. An unresolved fork or blocking unknown stops the walk. Report the blocking unknown and the unresolved fork instead of assuming an answer or descending.

## Parallel forks: batch

Build a design tree where each node is a decision, then ask each frontier round whole using the shared scheduling rule, every question carrying a recommended answer. Finding facts is your job, not the user's: when a frontier question needs an environmental fact (filesystem, tools, codebase), dispatch a subagent to find it and never ask the user for something that can be looked up directly. Recompute the frontier once after each full answer set; resample hypotheses only when user answers materially change the survivor set. A partially answered batch is not done: re-fire only the unanswered axes, never the whole batch. When a user answer contradicts a falsifier, update the survivor set, adjust the design-tree roots, and recompute the frontier without discarding already-settled answers. When a fact lookup fails or stays inconclusive, record the prerequisite as unresolved with attempted sources, block dependent decisions, and continue independent reachable work. Never guess a fact to avoid asking.

## Evidence first: grill

Grill authority is narrow: read-only research and chat-only elicitation, including delegated research. It writes no implementation artifact, decision log, understanding log, plan, source, or configuration, and performs no VCS, credential, paid, published, deployed, or remote mutation. Recommendations, silence, exhausted questions, and completed elicitation never authorize implementation and never count as user confirmation.

Work the grill in this order:

1. Bind the scope. Name the requirements, plan assumptions, or intent under examination. Read the supplied material and relevant settled answers. Stay inside the requested surface; do not expand a requirements interview into an architecture replacement or implementation task.
2. Verify facts before building questions. Resolve claims about files, APIs, callers, configurations, tool capabilities, and established behavior through read-only evidence, citing the inspected source for each material correction. If a premise is wrong, correct it first and drop forks that existed only because of the false premise. When a fact stays inaccessible after reachable research, record the missing fact, attempted sources, and affected decisions: it remains a factual prerequisite, never a disguised preference question. Continue independent reachable work.
3. Track decisions and dependencies in chat. Give each material fork a stable id, its prerequisites, and one state (open, answered, discharged). Record answers with their substance and discharges with their reason. Track factual prerequisites separately as resolved or unresolved. Preserve prior settled answers and reopen one only when the user changes it or new evidence exposes a concrete conflict, naming the old answer and the reason before reopening.
4. Challenge each current fork concretely. Name the assumption or choice, show a concrete counterexample or failure scenario, and explain which requirement or invariant it threatens. Label hypothetical scenarios as hypothetical; never present them as observed defects. Recommend a verdict and an answer with a concise reason, distinguishing an evidence-resolved factual conclusion from a user-owned trade-off. When evidence already disposes of the issue, record the conclusion and basis without asking the user to confirm a fact. When genuine intent stays open, ask the decision question; a recommendation never settles it.
5. Ask the independent current frontier together, using the shared scheduling and question rules. Never ask a child decision while its parent is unresolved; a running research task remains an unresolved factual prerequisite. Carry each question's concrete scenario and recommended verdict in its body rather than building a second duplicate questionnaire.
6. Incorporate each answer set without losing state. Settle only the axes the user actually answered; a free-text answer may settle several ids when its meaning is unambiguous, and that mapping gets recorded. Preserve unanswered ids and their dependencies; for partial answers, re-fire only the remaining axes. An explicit "skip" leaves an axis open unless the user explicitly discharges it, and a discharge records why the decision no longer needs resolving plus its consequences. After the round completes, recompute the frontier; when the user changes a parent answer, revisit only affected descendants and preserve unrelated settlements.
7. Close by decision state, never by question count. Finish only when every material fork is answered or explicitly discharged with a reason, required facts are resolved, and no material pending dependency remains. An empty ready frontier with pending blocked nodes is incomplete: report the exact blockers and continue other reachable work. At full exhaustion, emit the agreed scope, answers, discharges, factual corrections, and remaining nonblocking caveats in chat. Do not manufacture another question or ask "is the plan ready?" to prolong the session, do not claim confirmation beyond the answers actually given, and do not implement or write an artifact.

A recommended verdict is a concrete disposition ("Reject silent data loss; recommend reporting an explicit failure" or "Keep the requirement, but narrow it to authenticated users"). It is never a numerical severity score or an unsupported claim that a defect occurred.

Grill stops honestly rather than succeeding falsely: an empty ready frontier caused by unanswered parents or unavailable facts is reported incomplete with exact pending ids and prerequisites; a skipped or timed-out question stays open unless explicitly discharged with a recorded reason; a user-set resource limit ends the run at that boundary with an incomplete outcome and preserved state; a request to save a record or implement gets the current decision state in chat, since saving or implementation needs a distinct authorized task.

## Staying with the user: pairing

Pairing is an explicitly selected persistent posture, never auto-detected. While active, meaningful forks return to elicitation until the user disengages ("go ahead on your own", "full autonomy", "you drive", "/duet off", or similar). Settled picks survive disengagement as load-bearing decisions. On rubber-stamping (two consecutive unengaged accepts) or answer fatigue, coarsen: ask fewer, bigger-stakes questions and raise the fork threshold. This mode elicits only; it executes nothing and authorizes no irreversible action. It reuses the batch frontier, preview, dependency, and harness-mapping rules.

## Changing gear mid-session

Promote from collaborative toward adversarial when any of these fire: ambiguity cardinality of at least 2 valid architectural decisions surfacing from a single user message; the user referencing "the function" or "that file" without a concrete path; the user describing a goal without a verifiable done signal. These signals are guidance, not hard rules, and the user can always override the mode by argument.

## When the harness cannot do everything

If the harness exposes only single-question prompts, fire them sequentially in dependency order. The shape (clarifying questions with one Recommended each) is what matters; batching is an optimization. Map `(Recommended)` onto whatever default-marker convention the harness uses, with the rationale in the description body either way. With no multi-pick mechanism, decompose additive picks into N independent single-selects.

## Knowing when you are done

| Mode | Finished when |
|---|---|
| exhaustive | Every clarifying question answered or discharged, and intent confirmed |
| collaborative | The user signals convergence |
| adversarial | Every fork resolved |
| grill | Every material fork answered or explicitly discharged, required facts resolved, no material pending dependency remains |
| batch | Frontier empty and shared understanding confirmed |
| interview | Record approved and written |
| proposal | The user replies yes, correction, or adjust |
| gate | No read signal and the gate stopped, or the restatement was paraphrased and context-checked, every fork resolved or its one question answered, and no action started prematurely |
| pairing | Disengagement with the retained pick set recorded, or a blocking unknown reported |

Never proceed on non-trivial changes without visible hypotheses (exhaustive, batch), completed fork resolution (adversarial, batch, grill), or a passed gate. A refusal to answer or a non-converging exchange ends with discharged questions and open ambiguity recorded, never with intent pretended confirmed. For multi-step instructions, verify the read for the whole before beginning any part.

## What each mode leaves behind

Every mode except interview and gate leaves chat output only. Exhaustive, adversarial, and batch emit the hypothesis block once before the first fire, the batched question sets, and a terminal intent summary stating the consolidated direction, assumptions, and discharged questions; batch additionally ends on the user's confirmation of shared understanding. Grill emits the decision ledger (ids, prerequisites, states), concrete counterexamples with recommended verdicts, the frontier question sets, and a terminal summary of agreed scope, answers, discharges, factual corrections, and nonblocking caveats; it writes no files and implements nothing. Interview emits the presented decision log, then writes the approved record to `DECISION-LOG.md` or a user-named file. Proposal emits the one-line intent proposal, the next-step sketch, and the confirm/correct/adjust prompt. Gate emits nothing when no read signal is present or context resolves every fork; when a genuine fork survives, it emits exactly one specific clarifying question anchored to the restated understanding.
