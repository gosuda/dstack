---
name: from-perspective
description: 'Use when an answer is wanted from one named seat only: breaking, business, career, codebase, human, impact, innovation, moat, rent-seeking, skeptic, or stability. Not for multi-lens synthesis: use prism. Not for rebuilding from primitives: use from-first-principle.'
---

# Answer from one named seat

You answer the subject from exactly one viewpoint, using only what that viewpoint can see. Blending in a second lens, even a helpful one, breaks the result. Comparing lenses happens later, after each has spoken on its own, and outside this skill.

You read only. You write no files, touch no version control, credentials, paid services, published or deployed surfaces, or remote systems. Your whole output is one chat answer (or an honest statement that this seat has nothing independent to say).

## Naming the subject and the seat

You need two things before any analysis: the subject (a question, claim, decision, design, change, system, or artifact) and the `seat`, which must be exactly one of breaking, business, career, codebase, human, impact, innovation, moat, rent-seeking, skeptic, or stability. If the subject is missing, stop and ask for it rather than inventing one. If the request names a seat outside that list, stop and report which seat was asked for. Never substitute a nearby seat.

Restate the subject in one line so the seat you are taking is unambiguous. For the skeptic seat, restate the claim as a paraphrase and confirm the target before going further.

Each seat looks through its own concerns:

| Seat | Analyze the subject as |
|---|---|
| breaking | Stakeholders, dependencies, accounting, and compatibility under destructive pressure. You may name a specific pressure (cost, removal, dependency failure, stakeholder withdrawal); if none is named, apply the full seat. |
| business | Money (revenue, cost, margin, funding), customers (who pays, who is served, demand, churn), and timing (market window, sequencing, deadlines). |
| career | Effects on human trajectories: career growth, skill acquisition, role transitions, professional risk, and human capital. |
| codebase | What the existing code tolerates or punishes, with evidence read from the actual code in a reachable working tree. |
| human | What a person can love, trust, and tolerate: lived experience, attention cost, fatigue, trust erosion, tolerable friction, and what a person would keep or abandon. |
| impact | Who and what actually moves, traced against what merely appears to move or is assumed to move. |
| innovation | Original technique, talent, and culture: what is technically original, what talent or skill it depends on, and what cultural or creative conditions enable or block it. |
| moat | What builds, keeps, or thickens defensibility: switching costs, network effects, scale, data, brand, IP, lock-in, compounding advantage, and erosion risks to each. |
| rent-seeking | Extraction without building: who captures value without creating it, where rents accrue, and what barriers protect them. |
| skeptic | The claim's load-bearing assumptions, each marked stated, unstated, or unsupported, stressed for how each could fail. |
| stability | Preservation of the working machine: regressions, load placed on proven paths, removal of working behavior, fragility introduced, and recovery lost. |

## Working the seat

Reason exclusively through the named seat's concerns. Every claim in your answer must tie to one of them.

Ground each claim in the evidence that seat admits. For the codebase seat, read the code and report tolerates and punishes findings with code evidence; if the tree is unreachable, stop and say the codebase seat has no evidence, emitting no analysis. For the impact seat, mark unverified impact as inference. For the skeptic seat, give the strongest available failure reason for each assumption, end with a conclusion or an insufficiency statement, and name the single strongest counterargument so the result is not one-sided. For every seat, say where evidence is thin instead of filling gaps, and leave out a claim you cannot ground in this seat rather than borrowing another seat's reasoning.

If the seat genuinely yields no independent answer for this subject (a question with no career dimension, nothing that actually moves, an innovation claim that cannot be grounded), say so explicitly instead of forcing an answer or smuggling in another lens.

## Keeping other seats out

No other seat's reasoning appears in the body of your answer. If another seat feels relevant, you may point to it once, in one line at the end, as a separate lens to run independently, never as content. A sentence argued from any other seat invalidates the answer: discard the blended content, re-anchor on the named seat's concerns, and re-emit from that seat only.

Emit the analysis standing alone, with no recommendation and no cross-seat synthesis. A partial-evidence pass still helps: emit only the grounded portion, label the rest unverified, and name what stayed unresolved, without presenting inference as observed fact. Since this skill never mutates anything, a failed pass needs no rollback; it leaves only chat output or a request for the missing input.
